---
license: apache-2.0
base_model: answerdotai/ModernBERT-large
language:
- en
pipeline_tag: text-classification
tags:
- routing
- multi-agent
- agent-routing
- cross-encoder
- modernbert
- lora
- zero-shot-classification
---

# Signpost

Signpost is a **router for multi-agent chat**. You give it the conversation, the agent that answered last, and your agents with a one-line description each. It tells you which agent should handle the user's latest message.

The same model also answers **grounded questions about a text**:

- **yes / no** — "Does this convey urgency?"
- **choice** — "Which team should handle this?"
- **score on an ordered scale** — "How frustrated is the writer? calm / frustrated / furious"

The options are yours and can change on every call. They aren't fixed classes, so new agents or labels need no retraining.

It is fine-tuned from [answerdotai/ModernBERT-large](https://huggingface.co/answerdotai/ModernBERT-large) (395M parameters, encoder only). LoRA adapters (r 16) were trained and then merged into the weights, and a 0.26M-parameter scoring head was added. That is about one fifth of the size of a 2B decoder-based decider, and on a GPU it takes about 50–70 ms per decision.

## How it works

Signpost is a **cross-encoder**. It reads each option together with the conversation and the question, one forward pass per option (all options in one batch). It gives each option a score, and a softmax over the scores gives the probabilities. Every call, including routing, is the same "pick one of these options" task:

```
user: <msg> [SEP] assistant: <msg> [SEP] … [SEP] user: <latest msg> [SEP] current agent: <name or none> [SEP] question: <question> [SEP] candidate: <option>. <description>
```

- **Routing** uses the fixed question `Which agent should handle the user's latest message?`, with each agent's description in the candidate.
- **Yes / no** uses the options `yes` and `no`.
- **Score** reads the levels in order, from low to high, and also returns the expected level (Σ index × p).

`signpost.py`, included in this repo, builds this input exactly as it was in training. Use it rather than writing your own input format.

## Usage

Requirements: `torch` and `transformers` (tested with 5.17.0; ModernBERT needs ≥ 4.48). `signpost.py` has no other dependencies.

```python
import sys
from huggingface_hub import snapshot_download

path = snapshot_download("skamalj/signpost")
sys.path.insert(0, path)
from signpost import Signpost

sp = Signpost(path)        # CUDA in fp16 if available, else CPU in fp32
```

The examples below were run on the exported model, on CPU in fp32, using [`card_examples.py`](card_examples.py). Each `# ->` line is the actual recorded output, not an illustration.

### 1. Route a first message

```python
agents = {
    "Orders Agent": "Handles order status, delivery dates, tracking and changing a delivery address.",
    "Returns Agent": "Handles returns, exchanges, return labels and refunds for returned items.",
    "Billing Agent": "Handles payments, invoices, double charges and saved cards.",
    "Tech Support Agent": "Fixes problems with the app, logins and devices.",
}
messages = [{"role": "user", "content": "I was charged twice for my last order."}]
agent, probs = sp.route(messages, agents)
print(agent, {a: round(p, 3) for a, p in probs.items()})
# -> Billing Agent {'Orders Agent': 0.0, 'Returns Agent': 0.0, 'Billing Agent': 1.0, 'Tech Support Agent': 0.0}
```

### 2. Route inside a conversation

Pass the history, oldest first and ending with the user's latest message, and set `current_agent` to the agent that answered last. Signpost then decides whether to **stay** with that agent or **switch** to another.

```python
messages = [
    {"role": "user", "content": "I need to send back a jacket, it's the wrong colour."},
    {"role": "assistant", "content": "Sorry about that! Which colour did you receive?"},
    {"role": "user", "content": "the green one"},
]
agent, probs = sp.route(messages, agents, current_agent="Returns Agent")
print(agent, round(probs[agent], 3))          # a short answer stays with the current agent
# -> Returns Agent 1.0

messages += [
    {"role": "assistant", "content": "Thanks, I've emailed you a free return label for the green jacket."},
    {"role": "user", "content": "and my app keeps logging me out, can someone look at that?"},
]
agent, probs = sp.route(messages, agents, current_agent="Returns Agent")
print(agent, round(probs[agent], 3))          # a new topic moves to another agent
# -> Tech Support Agent 1.0
```

### 3. Choice

```python
pick, probs = sp.choice("Help! My payouts have been failing for 3 days!",
                        "Which team should handle this?", ["billing", "sales", "retail"])
print(pick, {o: round(p, 3) for o, p in probs.items()})
# -> billing {'billing': 0.908, 'sales': 0.019, 'retail': 0.073}

print(sp.choice("The blue sofa is £899 and the grey one is £749.", "Which sofa is cheaper?", ["blue", "grey"])[0])
# -> grey
```

### 4. Yes / no

`yes_no` returns P(yes); use 0.5 as the threshold.

```python
print(round(sp.yes_no("Help! My payouts have been failing for 3 days!", "Does this convey urgency?"), 3))
# -> 0.987

print(round(sp.yes_no("I'll pay by bank transfer this time instead of card.", "Will the customer pay by card?"), 3))
# -> 0.0
```

### 5. Score on an ordered scale

List the levels from low to high. You get back the most likely level, the expected level index (0 = first level), and the probabilities.

```python
level, expected, probs = sp.score("Help! My payouts have been failing for 3 days!",
                                  "How frustrated is the writer?", ["calm", "frustrated", "furious"])
print(level, round(expected, 2), {l: round(p, 3) for l, p in probs.items()})
# -> frustrated 1.2 {'calm': 0.01, 'frustrated': 0.778, 'furious': 0.211}

print(sp.score("No rush, whenever you get a moment.", "How urgent is this?", ["low", "medium", "high"])[0])
# -> low
```

### Use it in a LangGraph app

Signpost sits in front of the agents as the first node, and the graph jumps to the agent it picks (`Command(goto=…)`). The current agent is kept in the graph state. A full example has five agents (Claude), a DynamoDB checkpointer and a message-window reducer: [`signpost_app/`](https://github.com/skamalj/llms-the-hard-way/tree/exp/signpost-langgraph/signpost_app).

## Training

| | |
|---|---|
| Base | `answerdotai/ModernBERT-large`, frozen |
| Trained | LoRA r 16, alpha 32 on the encoder's linear layers (7.2M, merged at export) + head: mean pooling → Linear(1024, 256) → GELU → Linear(256, 1) (0.26M) |
| Data | 6,319 routing conversations (multi-turn, with the current agent and 5 agents with descriptions, many synthetic companies) + 9,586 grounded questions (yes / no balanced per family, choice, ordered score) |
| Loss | Listwise cross-entropy over 2–5 options. For score questions, an ordinal loss: label smoothing 0.1 onto neighbouring levels + 0.5 × \|expected − true\| / (L − 1) |
| Setup | 2 epochs, max length 320 tokens (if too long, the oldest history is cut), one seed (42), Kaggle T4, about 33 minutes |

All the training data is synthetic and was written for this project. Before training, it was checked for overlap with the test sets (5-gram and content-word guards).

## Evaluation

The numbers are counts correct. The reference model is the 2B **Strands decider**, zero-shot on the same questions. Each model gets them in its own input format, but the content is identical.

| Test | What it is | Signpost | Decider |
|---|---|---|---|
| E10 routing, unseen companies (83) · all (193) | Multi-turn chats, routed live turn by turn | **78** · **181** | 62 / 69 · 151 / 163 ¹ |
| E11 first message (100) | One message, 5 agents | **97** | 96 |
| Banking (50 · 225) | Banking routing | 48 · 210 | 48 · **214** ² |
| E12 (170): yes / no · choice · score | Grounded questions; the answer is in the text | **161**: 58 · 58 · 45 | 160: 56 · 56 · 48 |
| Independent questions (300): yes / no (100) · choice (108) · score (92) | Written by a separate author | 221: 75 · 103 · 43 | **253**: 77 · 106 · 70 |
| Independent routing, live turns (172) · first message (200) | Separate author | **133** · **180** | 113 / 121 ¹ · 178 |

¹ The decider answered fewer items: some outputs could not be parsed. ² banking77 is in the decider's training data.

**Live in a LangGraph app:** five agents, with real LLM replies in the history, DynamoDB persistence and a pruned history. 67 of 71 turns were routed correctly: first messages 19/20, conversations 31/32, resumed after restore 7/7, long chat with a 8/4-message window 10/12.

**Latency:** on a T4 GPU, about 50–70 ms per decision (p50), which is 4–7× faster than the decider measured the same way. On a laptop CPU in fp32, about 1.3 s for a first message and about 4 s with a long history.

### Caveats

- The routing and E10–E12 test sets were written by the same author as the training data. The independent sets are the fairest comparison.
- These are single-seed results. Three runs of the same recipe varied by about ±4 on most tests, and by 43–53 on independent score.
- The decider ran in bf16 on a T4 without its optimised kernels, so its latency is an upper bound.

## Limitations

- **Score precision is the weak spot.** On out-of-distribution text, Signpost often picks the level next to the right one (independent score 43/92 vs the decider's 70/92). Use `expected` rather than the top level if a near miss is acceptable.
- **It sometimes switches too eagerly.** A short follow-up whose topic belongs to another agent ("can I use them on the repair?") can be routed away from the current agent. Clear agent descriptions help.
- **The probabilities are not calibrated.** They are usually close to 0 or 1, so don't treat them as confidence.
- English only. Trained with 2–5 options per question; more options work, but have not been tested much.
- Answers come only from the given text, by design. Questions that need world knowledge or arithmetic are not supported.
- Inputs longer than 320 tokens lose their oldest history.
- CPU latency grows with history length. Keep a window of recent messages, or use a GPU.

## Provenance

- Code, data builders, notebooks and the experiment ledger: [github.com/skamalj/llms-the-hard-way](https://github.com/skamalj/llms-the-hard-way)
- The exact state that trained and exported this model: tag [`signpost-v1.0`](https://github.com/skamalj/llms-the-hard-way/tree/signpost-v1.0), `lora_combined.ipynb` with `TRAIN_MODE=combined`, `EXPORT=1`

## License

Apache 2.0, the same as the base model [answerdotai/ModernBERT-large](https://huggingface.co/answerdotai/ModernBERT-large).
