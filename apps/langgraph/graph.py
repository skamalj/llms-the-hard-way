"""The LangGraph app: Signpost routes each user message to one of five agents; each agent answers with Claude.

    START -> signpost --(Command goto)--> <agent node> -> END

State is checkpointed per thread in DynamoDB (DynamoDBSaver), and the agentstate-reducer prunes the stored message
history inside every checkpoint save, so a long conversation keeps only its most recent messages.
"""
from typing import Annotated, TypedDict

import anthropic
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.types import Command

from northwind import AGENTS, node_id, system_prompt
from router import message_text
from settings import AGENT_EFFORT, AGENT_MODEL, MAX_MESSAGES, MIN_MESSAGES, TABLE_NAME, TTL_SECONDS, use_aws_profile

# Models that take the server-side refusal fallback (`fallbacks: "default"`); Haiku models do not.
FALLBACK_MODELS = {"claude-fable-5-1", "claude-opus-5-5", "claude-opus-5", "claude-sonnet-5-5"}


class State(TypedDict):
    messages: Annotated[list, add_messages]
    current_agent: str | None          # the agent that answered the previous turn (Signpost's "current agent")
    route: dict | None                 # Signpost's decision for the latest turn: agent, probabilities, latency


def build_checkpointer(max_messages=MAX_MESSAGES, min_messages=MIN_MESSAGES):
    """DynamoDB checkpointer with the message reducer (prunes oldest whole messages when a thread grows past max)."""
    use_aws_profile()
    from agentstate_reducer import MessageReducer, ReducerConfig
    from langgraph_dynamodb_checkpoint import DynamoDBSaver

    # preserve_first=False: our threads have no system message at index 0 to protect
    reducer = MessageReducer(config=ReducerConfig(max_messages=max_messages, min_messages=min_messages, preserve_first=False))
    return DynamoDBSaver(TABLE_NAME, max_read_request_units=10, max_write_request_units=10, ttl_seconds=TTL_SECONDS,
                         reducer=reducer)


def _claude_history(messages):
    """The thread as Anthropic messages; the request must start with a user turn (pruning can leave an assistant first)."""
    out = [{"role": "user" if isinstance(m, HumanMessage) else "assistant", "content": message_text(m)}
           for m in messages if isinstance(m, (HumanMessage, AIMessage))]
    while out and out[0]["role"] != "user":
        out.pop(0)
    return out


def _agent_reply(client, agent, messages):
    kwargs = dict(model=AGENT_MODEL, max_tokens=4000, system=system_prompt(agent), messages=_claude_history(messages))
    if not AGENT_MODEL.startswith("claude-haiku-4"):
        kwargs["output_config"] = {"effort": AGENT_EFFORT}
    if AGENT_MODEL in FALLBACK_MODELS:
        response = client.beta.messages.create(betas=["server-side-fallback-2026-07-01"], fallbacks="default", **kwargs)
    else:
        response = client.messages.create(**kwargs)
    if response.stop_reason == "refusal":
        return "Sorry, I can't help with that request."
    return "".join(b.text for b in response.content if b.type == "text").strip()


def build_graph(router, checkpointer, call_llm=True):
    """call_llm=False replaces the agents' Claude calls with a fixed stub reply (routing-only tests, no API cost)."""
    client = anthropic.Anthropic() if call_llm else None
    builder = StateGraph(State)

    def signpost(state: State) -> Command:
        agent, probs, ms, seen = router.route(state["messages"], AGENTS, state.get("current_agent"))
        return Command(goto=node_id(agent),
                       update={"route": {"agent": agent, "p": probs[agent], "probs": probs, "ms": ms, "messages_seen": seen}})

    builder.add_node("signpost", signpost)
    builder.add_edge(START, "signpost")

    for agent in AGENTS:
        def answer(state: State, agent=agent):
            text = _agent_reply(client, agent, state["messages"]) if call_llm else f"({agent} would answer here.)"
            return {"messages": [AIMessage(content=text, name=node_id(agent))], "current_agent": agent}
        builder.add_node(node_id(agent), answer)
        builder.add_edge(node_id(agent), END)

    return builder.compile(checkpointer=checkpointer)


def send(graph, thread_id, text):
    """One user turn on a thread -> the final state of that turn (route, current_agent, messages)."""
    return graph.invoke({"messages": [HumanMessage(content=text)]}, {"configurable": {"thread_id": thread_id}})


def stored_messages(graph, thread_id):
    """How many messages the checkpoint in DynamoDB holds for the thread (after the reducer's pruning)."""
    snap = graph.get_state({"configurable": {"thread_id": thread_id}})
    return len(snap.values.get("messages", [])) if snap and snap.values else 0
