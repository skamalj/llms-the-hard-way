# Brief: independent test cases for a routing and choice model

You are writing an **independent test set**. We will run two systems on exactly your cases and compare them. Please do not look at our data or code, and keep your cases private until you hand them over.

## Revision request (after the first delivery)

Thank you for the first files. `first_turn.jsonl` is good as it is: 200 distinct, natural messages. The other two files need a rewrite, because most cases came from a few templates and some labels can't be worked out from the text. Here is what we found:

| File | What we found | What we need |
|---|---|---|
| `questions.jsonl` | Only **20 distinct texts** for 300 questions. **81 of the 100 choice questions** were the same question ("Which exact number is explicitly stated in the text, if any?"). Yes / no answers were 26 yes vs 74 no. | At least **150 distinct texts**, each used for **at most 3** questions. **No question wording used more than 10 times.** Yes / no answers **close to 50 / 50** (45–55 yes). Choice questions should mostly be about the content (who, what, which item, which day), not about the text itself. |
| `routing.jsonl` | Only **26 distinct user messages** across 160 turns. Every first message was "I need help with a … at your <company>", which names no need, so no agent can be picked from it. **20 turns contradicted their type**: e.g. "Also, can you send the written details with it?" was labelled `also_stay` but went to a different agent. Assistant replies were generic ("I can help with that…"). Every conversation had exactly 4 turns, and only 6 turn types were used. | Every user message **written for its conversation**: no repeated sentences across conversations. The **first message must state the need**, so the right agent can be chosen from it. **Labels must follow the turn type:** `answer`, `follow`, `aspect`, `closing` and `also_stay` keep the previous turn's agent; `switch`, `short_switch` and `return` change it. Assistant replies must say something specific to the conversation. Conversations should have **4–8 turns, of varied length**, and use **every turn type** at least 5 times across the file. |

Please run the self-check at the end of this brief before sending.

## General rules

- **Everything must be answerable from the text given.** No world knowledge, no trick questions, and exactly one correct answer per case.
- **Write naturally**, the way real customers write. Vary length, tone and style, and include short replies ("yes", "ok thanks", "the blue one"), typos and informal wording.
- **Use your own businesses and scenarios.** Do **not** use any of these, which we already used for training:
  airline, car rental, car service, clinic, cloud hosting, coworking, event tickets, food delivery, government services, gym, home services, hotel, HR, IT helpdesk, library, mobile network, museum, public transport, rentals, restaurant, SaaS product, school, shipping, streaming, university, vet clinic, wedding planning, art supplies shop, band merch store, boat hire, boiler servicing, bowling alley, bridal shop, cake bakery, campsite, car leasing, car wash, children's nursery, coach tour operator, coffee chain app, dental clinic, dry cleaner, email provider, escape rooms, florist, garden centre, golf club, hearing clinic, holiday cottages, home alarm company, home cinema installer, kitchen fitter, language-learning app, laundry pickup service, leisure centre, locksmith, meal-kit delivery, motorbike rental, music school, opticians, password manager, pet sitting service, physiotherapy clinic, printer ink subscription, removals company, self storage, ski resort, tailor, theme park, tutoring agency, tyre fitting, VPN app, wedding venue, window cleaning company, wine club, yoga studio, zoo.
- **Do not copy from public datasets.**
- **If you use an AI tool to help, tell us which one.** Ideally the cases are written by hand.
- Deliver **three UTF-8 JSON Lines files** (one JSON object per line), as described below.

## 1. `questions.jsonl`: yes / no, choice and score questions about a short text

At least **100 of each type** (300 or more lines).

```json
{"id": "q001", "type": "yes_no", "text": "Third reminder this week and still no invoice from you.", "question": "Is the writer annoyed?", "options": ["yes", "no"], "answer": "yes", "group": "g01"}
{"id": "q002", "type": "choice", "text": "Third reminder this week and still no invoice from you.", "question": "What is the writer waiting for?", "options": ["a refund", "an invoice", "a delivery"], "answer": "an invoice", "group": "g01"}
{"id": "q003", "type": "score", "text": "Third reminder this week and still no invoice from you.", "question": "How urgent is this?", "options": ["low", "medium", "high"], "answer": "high", "group": "g01"}
```

| Field | Rule |
|---|---|
| `type` | `yes_no`, `choice` or `score` |
| `text` | 1–4 sentences: a message, review, note or short notice |
| `options` | `yes_no`: exactly `["yes", "no"]`. `choice`: 2–5 options, any order. `score`: 3–5 levels **ordered from low to high**, clearly separable |
| `answer` | exactly one of the options, written identically |
| `group` | optional. Give the same group id to different questions about the **same text**: please make about 20 such groups |

- **Yes / no:** keep the answers roughly 50% yes and 50% no.
- **Mix the kinds of question:** tone and feelings, urgency, intent, facts stated in the text, picking the stated detail among several mentioned, comparing numbers in the text, counting, and turning a stated number or phrase into a level (size, duration, frequency, intensity).

## 2. `routing.jsonl`: which agent should handle the user's latest message (conversations)

At least **20 businesses × 2 conversations** (40 or more lines), each with 4–8 user turns.

```json
{"id": "r001", "company": "piano repair shop",
 "agents": {"Repairs Agent": "Fixes and services pianos: tuning, broken keys, pedals.",
            "Bookings Agent": "Books, moves and cancels technician visits.",
            "Payments Agent": "Handles quotes, invoices, payments and refunds."},
 "turns": [
   {"user": "One of the middle keys sticks when I play.", "expected_agent": "Repairs Agent", "turn_type": "start", "assistant": "Sorry to hear that. Is it upright or grand?"},
   {"user": "upright", "expected_agent": "Repairs Agent", "turn_type": "answer", "assistant": "That's usually a swollen key bushing. We can fix it on a visit."},
   {"user": "ok can someone come thursday?", "expected_agent": "Bookings Agent", "turn_type": "switch", "assistant": "Thursday 2pm is free. Shall I book it?"},
   {"user": "and how much will that be", "expected_agent": "Payments Agent", "turn_type": "short_switch", "assistant": null}]}
```

- **`agents`:** 3–5 agents per business, each with a one-sentence description, as a real support desk would have. Include at least one pair of **closely related agents**.
- **`assistant`:** the reply after that user turn, written as if the expected agent answered. Use `null` on the last turn.
- **`turn_type`:** one of:

| Type | Meaning |
|---|---|
| `start` | the first message |
| `answer` | a short answer to the agent's question ("Tuesday", "BA-2291") |
| `follow` | a follow-up on the same request |
| `aspect` | the same agent, a different part of its topic |
| `closing` | "ok thanks", "great, cheers" |
| `also_stay` | "Also …" or "And …", but it stays with the same agent |
| `switch` | a clear move to another agent |
| `short_switch` | a move to another agent in a few words ("and my bill?") |
| `return` | back to an earlier topic or agent |
| `handoff_ok` | "ok" right after the assistant handed the user to another agent |

Please include plenty of **switches that sound like follow-ups** ("And is my other order in that box too?"), and some `also_stay` and `return` turns.

## 3. `first_turn.jsonl`: route a single first message

At least **100 lines**, for 10 or more businesses with **5 agents each**.

```json
{"id": "f001", "company": "piano repair shop", "agents": {"Repairs Agent": "...", "Bookings Agent": "...", "Payments Agent": "...", "Sales Agent": "Sells new and second-hand pianos.", "Lessons Agent": "Books piano lessons."}, "message": "do you have any used uprights under 2k", "expected_agent": "Sales Agent", "kind": "short"}
```

`kind` is one of:
- `clear`: names the need;
- `short`: 1–4 words;
- `indirect`: describes the situation without the obvious keyword;
- `close`: sits between two similar agents;
- `noisy`: typos, lower case.

## Before you send

- Every `answer` or `expected_agent` exactly matches one of its options or agent names.
- Every line is valid JSON.
- No business or scenario from the excluded list above.
- **No templates.** Each text and each user message is written for its own case. Read 20 random lines: if two of them look alike apart from a name or a number, rewrite one.
- **Every label can be justified from the text alone.** A reader who sees only the text (or the conversation so far) and the options should pick your answer.

**Self-check** (Python 3, run it in the folder with your three files; it must print `OK`):

```python
import json, collections
L = lambda f: [json.loads(l) for l in open(f, encoding="utf-8") if l.strip()]
Q, R, F = L("questions.jsonl"), L("routing.jsonl"), L("first_turn.jsonl")
STAY, SWITCH = {"answer", "follow", "aspect", "closing", "also_stay"}, {"switch", "short_switch", "return"}
assert all(q["answer"] in q["options"] for q in Q)
texts = collections.Counter(q["text"] for q in Q)
assert len(texts) >= 150 and max(texts.values()) <= 3, "need 150+ distinct texts, each used at most 3 times"
assert max(collections.Counter(q["question"] for q in Q).values()) <= 10, "no question wording more than 10 times"
yes = sum(q["answer"] == "yes" for q in Q if q["type"] == "yes_no")
assert 45 <= yes <= 55, f"yes / no balance: {yes} yes of 100"
users = [t["user"] for r in R for t in r["turns"]]
assert len(set(users)) == len(users), "every user message must be unique"
types = collections.Counter(t["turn_type"] for r in R for t in r["turns"])
assert all(types[t] >= 5 for t in STAY | SWITCH), f"each turn type at least 5 times: {dict(types)}"
for r in R:
    prev = None
    for t in r["turns"]:
        assert t["expected_agent"] in r["agents"]
        if prev and t["turn_type"] in STAY: assert t["expected_agent"] == prev, (r["id"], t["user"])
        if prev and t["turn_type"] in SWITCH: assert t["expected_agent"] != prev, (r["id"], t["user"])
        prev = t["expected_agent"]
assert all(f["expected_agent"] in f["agents"] for f in F)
print("OK")
```
