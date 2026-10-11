"""Chat with Northwind Outdoor Gear in the terminal; Signpost picks the agent for every message.

    uv run python chat.py                 # a new conversation
    uv run python chat.py --thread my-id  # continue a conversation stored in DynamoDB (also after a restart)

Commands: /state shows what DynamoDB holds for the thread; /quit ends.
"""
import argparse
import uuid

from graph import build_checkpointer, build_graph, send, stored_messages
from router import SignpostRouter


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--thread", default=None)
    ap.add_argument("--router-only", action="store_true", help="stub agent replies instead of Claude")
    args = ap.parse_args()
    thread = args.thread or f"chat-{uuid.uuid4().hex[:8]}"
    print("loading Signpost ...", flush=True)
    graph = build_graph(SignpostRouter(), build_checkpointer(), call_llm=not args.router_only)
    held = stored_messages(graph, thread)
    print(f"thread {thread}" + (f" (continuing: {held} messages stored)" if held else " (new)") + " | /state, /quit\n")
    while True:
        try:
            text = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not text:
            continue
        if text == "/quit":
            break
        if text == "/state":
            snap = graph.get_state({"configurable": {"thread_id": thread}}).values
            print(f"  stored: {len(snap.get('messages', []))} messages | current agent: {snap.get('current_agent')}\n")
            continue
        out = send(graph, thread, text)
        r = out["route"]
        top = sorted(r["probs"].items(), key=lambda kv: -kv[1])[:3]
        print(f"  [Signpost -> {r['agent']} (p {r['p']:.2f}) | runner-up: "
              + ", ".join(f"{a.replace(' Agent', '')} {p:.2f}" for a, p in top[1:]) + f" | {r['ms']:.0f} ms | saw {r['messages_seen']} messages]")
        print(f"{r['agent']}> {out['messages'][-1].content}\n")
    print(f"bye. Resume later with: uv run python chat.py --thread {thread}")


if __name__ == "__main__":
    main()
