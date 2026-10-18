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
- bert
- modernbert
- lora
- zero-shot-classification
---

# Signpost one-pass

Signpost one-pass is a **BERT-based router for multi-agent chat** that reads **all your agents in one pass**. You give it the conversation, the agent that answered last, and your agents with a one-line description each; it tells you which agent should handle the user's latest message. Because every option goes into one input, its speed hardly changes with the number of agents: about 60 ms on a T4 GPU for 2 or 50 options.

It is the one-pass sibling of [**Signpost**](https://huggingface.co/skamalj/signpost), which reads the conversation once **per option**. Same base model, same kinds of questions, same calls; use this one when you have many agents or options, or need a fixed latency budget, and Signpost when you have a handful of options and want the last bit of accuracy on grounded questions.

The same model also answers **grounded questions about a text**:

- **yes / no** — "Does this convey urgency?"
- **choice** — "Which team should handle this?", with up to 50 options
- **score on an ordered scale** — "How frustrated is the writer? calm / frustrated / furious"

The options are yours and can change on every call. They aren't fixed classes, so new agents or labels need no retraining.

It is fine-tuned from [answerdotai/ModernBERT-large](https://huggingface.co/answerdotai/ModernBERT-large) (395M parameters, encoder only): LoRA adapters (r 16) were trained and then merged into the weights, and a 0.26M-parameter scoring head was added.

## How it works

All options go into **one input**, after the conversation and the question:

```
user: <msg> [SEP] … [SEP] user: <latest msg> [SEP] current agent: <name or none> [SEP] question: <question> [SEP] option: <name>. <description> [SEP] option: <name>. <description> [SEP] …
```

The encoder runs **once**. Each option's vector is the mean of that option's own tokens, the same head scores every option, and a softmax over the scores gives the probabilities. Inside the encoder the options also see each other, so the model can compare them directly.

- **Routing** uses the fixed question `Which agent should handle the user's latest message?`, with each agent's description in its option.
- **Choice**, **yes / no** (options `yes` and `no`) and **score** (ordered levels, low to high; also returns the expected level, Σ index × p) work the same way with your question and options.
- Up to **50 options**, and up to 1,536 tokens in total. If the input is longer, the oldest messages are dropped; options never are.

`signpost_one_pass.py`, included in this repo, builds this input exactly as it was in training. Use it rather than writing your own input format.

## Usage

Requirements: `torch` and `transformers` (tested with 5.17.0; ModernBERT needs ≥ 4.48). `signpost_one_pass.py` has no other dependencies.

```python
import sys
from huggingface_hub import snapshot_download

path = snapshot_download("skamalj/signpost-one-pass")
sys.path.insert(0, path)
from signpost_one_pass import SignpostOnePass

sp = SignpostOnePass(path)        # CUDA in fp16 if available, else CPU in fp32
```

The examples below were run on the exported model, on CPU in fp32, using [`card_examples_one_pass.py`](card_examples_one_pass.py). Each `# ->` line is the actual recorded output, not an illustration.

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

Pass the history, oldest first and ending with the user's latest message, and set `current_agent` to the agent that answered last. The model then decides whether to **stay** with that agent or **switch** to another.

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

### 3. Many agents, one pass

```python
store = {   # 12 agents: Orders, Returns, Refunds, Billing, Gift Cards, Loyalty, Product Advice,
            # Repairs, Store Locations, Account, Business Sales, Complaints (each with a description)
    ...
}
agent, probs = sp.route([{"role": "user", "content": "The zip on my backpack broke after two weeks, can you fix it under warranty?"}], store)
# -> Repairs Agent 1.0   (12 agents, one forward pass: 833 ms on a laptop CPU)
```

The full agent list is in `card_examples_one_pass.py`.

### 4. Choice, including many options

```python
pick, probs = sp.choice("Help! My payouts have been failing for 3 days!",
                        "Which team should handle this?", ["billing", "sales", "retail"])
print(pick, {o: round(p, 3) for o, p in probs.items()})
# -> billing {'billing': 1.0, 'sales': 0.0, 'retail': 0.0}

print(sp.choice("The blue sofa is £899 and the grey one is £749.", "Which sofa is cheaper?", ["blue", "grey"])[0])
# -> grey

cities = ["Lisbon", "Oslo", "Prague", "Dublin", "Vienna", "Krakow", "Seville", "Bergen", "Porto", "Zagreb",
          "Tallinn", "Ghent", "Lyon", "Turin", "Malmo", "Riga", "Bilbao", "Bruges", "Graz", "Split"]
print(sp.choice("We flew into Oslo on Friday, then took the train west to Bergen, where the conference was.",
                "In which city was the conference?", cities)[0])
# -> Bergen
```

### 5. Yes / no

`yes_no` returns P(yes); use 0.5 as the threshold.

```python
print(round(sp.yes_no("Help! My payouts have been failing for 3 days!", "Does this convey urgency?"), 3))
# -> 1.0

print(round(sp.yes_no("I'll pay by bank transfer this time instead of card.", "Will the customer pay by card?"), 3))
# -> 0.0
```

### 6. Score on an ordered scale

List the levels from low to high. You get back the most likely level, the expected level index (0 = first level), and the probabilities.

```python
level, expected, probs = sp.score("Help! My payouts have been failing for 3 days!",
                                  "How frustrated is the writer?", ["calm", "frustrated", "furious"])
print(level, round(expected, 2), {l: round(p, 3) for l, p in probs.items()})
# -> frustrated 1.0 {'calm': 0.0, 'frustrated': 1.0, 'furious': 0.0}

print(sp.score("No rush, whenever you get a moment.", "How urgent is this?", ["low", "medium", "high"])[0])
# -> low
```

### Use it in your multi-agent setup

Exactly as with Signpost: call `route()` before each user turn, send the turn to the agent it picks, and remember that agent as `current_agent` for the next turn. The LangGraph example in [`apps/langgraph/`](https://github.com/skamalj/llms-the-hard-way/tree/signpost-apps/apps/langgraph) uses Signpost; swapping in `SignpostOnePass` needs only the import and the path.

## Training

| | |
|---|---|
| Base | `answerdotai/ModernBERT-large`, frozen |
| Trained | LoRA r 16, alpha 32 on the encoder's linear layers (7.2M, merged at export) + head: mean of each option's tokens → Linear(1024, 256) → GELU → Linear(256, 1) (0.26M) |
| Data | 6,319 routing conversations (multi-turn, with the current agent and 5 agents; at training time agents from other businesses are added, up to 10–15 agents for 2,500 of them) + 11,730 grounded questions: yes / no, choice, ordered score, and 2,500 hand-written questions with 2–50 options |
| Setup | 2 epochs, plain cross-entropy over each question's options, batches by token budget, max length 1,536 tokens, one seed (42), Kaggle T4, about 29 minutes |

All the training data is synthetic and was written for this project. Before training, it was checked for overlap with the test sets (5-gram and content-word guards); the many-option tests use words and names that never appear in training.

## Evaluation

Compared with Signpost (one pass per option) and the Strands decider ([StrandsAgents/strands-decider-2B-hobson-v19](https://huggingface.co/StrandsAgents/strands-decider-2B-hobson-v19), 2B, zero-shot). All three get **exactly the same test items**; each gets its own input format. Every number is **correct answers / total items**. For routing in conversations, the models see the full chat history, and Signpost and this model route live (their own previous pick becomes the current agent).

| Test | Signpost one-pass | Signpost | Decider |
|---|---|---|---|
| Routing in conversations, unseen companies | 76 / 83 | **78 / 83** | 62 / 83 |
| Routing in conversations, all companies | 175 / 193 | **181 / 193** | 151 / 193 |
| First message | **98 / 100** | 97 / 100 | 96 / 100 |
| Banking, benchmark · all | 47 / 50 · 210 / 225 | 48 / 50 · 210 / 225 | 48 / 50 · **214 / 225** ¹ |
| Grounded questions, total | 152 / 170 | **161 / 170** | 160 / 170 |
| Independent questions, total | 226 / 300 | 221 / 300 | **253 / 300** |
| — yes / no · choice · score | **80** · **106** · 40 | 75 · 103 · 43 | 77 · **106** · **70** |
| Independent routing in conversations | **134 / 172** | 133 / 172 | 113 / 172 |
| Independent first message | 178 / 200 | **180 / 200** | 178 / 200 |
| Independent set 2 questions (incl. 10–50 options) | 184 / 200 | **188 / 200** | 185 / 200 |
| Independent set 2 routing (8–11 agents) · first message | 56 / 70 · **50 / 50** | **62 / 70** · 47 / 50 | 55 / 70 · **50 / 50** |
| **Many-option questions (10–50 options)** | **152 / 162** | 150 / 162 | **160 / 162** |
| **Many-agent routing in conversations (9–15 agents)** | 102 / 120 | **103 / 120** | 83 / 120 |
| Many-agent first message | 62 / 72 | 62 / 72 | **70 / 72** |
| Same pick with the agents listed in reverse order | 71 / 72 | — | — |

¹ banking77 is in the decider's training data, so this set is not unseen for it.

The test sets are described on [Signpost's card](https://huggingface.co/skamalj/signpost#test-sets); the many-option tests were written for this model: 162 questions with 10–50 options, and 12 new businesses with 9–15 agents (24 conversations, 72 first messages).

**Latency** (T4 GPU, p50, one question at a time):

| | Signpost one-pass | Signpost | Decider |
|---|---|---|---|
| Questions with 2–5 options | 56 ms | 55 ms | ~200 ms |
| Routing, 5 agents | 60 ms | 58 ms | 316 ms |
| Routing, 8–11 agents | **62 ms** | 187 ms | 654 ms |
| Questions with 10–50 options | **61 ms** | 63 ms | 382 ms |

### Caveats

- The conversation, first-message and grounded-question sets were written by the same author as the training data; the independent sets are the fairest comparison (the first was written outside the project, the second by an AI author working from a neutral brief).
- These are single-seed results; runs of the same recipe varied by about ±4 on most tests and by up to ±6 on the grounded questions (152–158 / 170 across three runs).
- The decider ran in bf16 on a T4 without its optimised kernels, so its latency is an upper bound. Signpost's and the decider's numbers were measured on the same items in the project's notebooks, not in the run that trained this model.

## Limitations

- **Score precision is the weak spot**, as for Signpost: answers are almost always within one level (90 / 92 on the independent set), but on scales written by someone outside the project the exact level is often off by one (40 / 92 exact, against the decider's 70).
- **Slightly behind Signpost on grounded questions** written in the project's own style (152 vs 161 / 170).
- **The probabilities are not calibrated.** They are nearly always 0 or 1, so don't treat them as confidence.
- English only. At most 50 options per call, and 1,536 tokens per input (the oldest history is dropped first).
- Answers come only from the given text, by design. Questions that need world knowledge or arithmetic are not supported.
- On CPU, one call takes about 0.8 s with a dozen agents; use a GPU for interactive use.

## Provenance

- Code, data builders, notebooks and the experiment ledger: [github.com/skamalj/llms-the-hard-way](https://github.com/skamalj/llms-the-hard-way)
- The notebook that trained and exported this model: `05_one_pass_signpost.ipynb` on branch [`signpost`](https://github.com/skamalj/llms-the-hard-way/tree/signpost) (the run is recorded in `experiments/modernbert_router_ledger.md`, "05 — 2026-10-18"; the experiments that led to it are runs 26–29).

## License

Apache 2.0, the same as the base model [answerdotai/ModernBERT-large](https://huggingface.co/answerdotai/ModernBERT-large).
