# Signpost in LangGraph: a real-setting test of the router

A small customer-support app for a fictional retailer, **Northwind Outdoor Gear**, with five agents. **Signpost** (our fine-tuned ModernBERT-large router, [skamalj/signpost](https://huggingface.co/skamalj/signpost), downloaded from the Hugging Face Hub on first use) picks the agent for every user message. The chat memory is stored in **DynamoDB** with `langgraph-dynamodb-checkpoint`, and its **reducer** (`agentstate-reducer`) prunes old messages.

```text
user message -> [signpost]  reads the thread (messages + current agent), picks 1 of 5 agents
                    |  Command(goto=agent)
                    v
                [agent]  Claude answers as that agent, sets current_agent -> END
checkpoint per thread in DynamoDB; the reducer prunes the stored history (default: above 12 messages, down to 6)
```

| Agent | Handles |
|---|---|
| Orders & Delivery | order status, delivery dates, tracking, address changes, missing parcels |
| Returns & Refunds | returns, exchanges, return labels, refunds |
| Product Advice | choosing tents, sleeping bags, jackets, boots; sizes; specs |
| Repairs & Warranty | broken or faulty gear, warranty claims, repairs |
| Billing & Membership | payments, invoices, gift cards, loyalty points, membership |

## Running (Windows PowerShell)

```powershell
cd apps\langgraph                        # on the signpost-apps branch
uv sync                                   # first time only
aws sso login                             # if the SSO session has expired
$env:ANTHROPIC_API_KEY = "..."            # or set it in your profile
uv run python run_tests.py                # all tests (A-D), report in reports/
uv run python run_tests.py --router-only  # routing only, no Claude calls
uv run python chat.py                     # chat yourself; --thread <id> to resume
```

## Settings (environment variables)

| Variable | Default | Meaning |
|---|---|---|
| `AGENT_MODEL` | `claude-opus-5-5` | the model the agents answer with (e.g. `claude-haiku-5-5` for a cheaper run) |
| `AGENT_EFFORT` | `low` | effort for the agents' replies |
| `CHECKPOINT_TABLE` | `signpost-checkpoints` | DynamoDB table (created on first use, on-demand billing) |
| `CHECKPOINT_TTL` | `86400` | checkpoint expiry in seconds |
| `REDUCER_MAX_MESSAGES`, `REDUCER_MIN_MESSAGES` | 12, 6 | prune above max, down to min |
| `SIGNPOST_REPO` | `skamalj/signpost` | the Hugging Face repo Signpost is downloaded from |
| `SIGNPOST_PATH` | (unset) | a local exported Signpost folder to use instead of the Hub |
| `AWS_PROFILE` | the first profile in `~/.aws/config` | AWS credentials for DynamoDB |

## Tests (`run_tests.py`)

- **A. First messages:** 20 opening messages, each on a new thread.
- **B. Conversations:** 6 conversations of 5–7 turns, routed live. Signpost sees the real history (with Claude's replies) and the current agent.
- **C. Persistence:** half a conversation, then a **new** checkpointer and graph continue the thread from what DynamoDB holds.
- **D. Reducer:** a 12-turn conversation with a small window (prune above 8 messages, down to 4), so Signpost routes from a pruned history.

The report (`reports/report_<time>.md` + `.json`) lists every turn: expected agent, Signpost's pick and probability, the current agent, how many messages Signpost saw, how many DynamoDB stores after pruning, latency, and the agent's reply.
