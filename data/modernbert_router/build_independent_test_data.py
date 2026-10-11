"""Independent test set (written outside this project, from experiments/independent_test_brief.md) -> our test formats.

Run from the repo root: python data/modernbert_router/build_independent_test_data.py

Input (as delivered, unchanged): independent/questions.jsonl, routing.jsonl, first_turn.jsonl = the writer's V1 (2026-10-11),
which passes the brief's self-check. The first delivery (template-made, see the ledger) is kept as *_v0.jsonl.
Output: independent/questions.json (E12 format), routing.json (E10 format), first_turn.json.
Nothing is dropped. Questions are FLAGGED where an item tests something other than reading the text:
  claim_check      a yes / no "does the text contradict / support the opposite of the claim" item (in V1 all 22 answer "yes",
                   so a model could pass them by pattern)
  unordered_scale  a "score" item whose options are not one dimension ordered low -> high (reversed or not a scale);
                   exact accuracy still counts, but "within one level" / expected level are meaningless for it
Routing turns are FLAGGED where the delivered label cannot be judged from the text:
  label_conflict  a stay-type turn (answer / follow / also_stay) whose expected agent differs from the previous turn's,
                  or a switch-type turn that keeps the previous agent
  vague_start     a templated first message that names no need ("I need help with a ... at your <company>")
"""
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent / "independent"
read = lambda f: [json.loads(l) for l in open(HERE / f, encoding="utf-8") if l.strip()]
TYPE = {"yes_no": "noul", "choice": "choice", "score": "score"}
STAY, SWITCH = {"answer", "follow", "also_stay", "aspect", "closing"}, {"switch", "short_switch", "return", "handoff_ok"}

# ---- questions -> E12 format
UNORDERED = [   # reviewed by hand in V1: not a single low -> high scale (not a scale, reversed, or two dimensions mixed)
    ["strong evidence of rejects", "no rejects reported", "counts are missing"], ["spread across all sections", "limited to one section", "no clear pattern"],
    ["paper sample", "envelope stock", "same weight"], ["copper", "brass", "same amount"], ["equal quantities", "twice as many oak", "twice as many ash"],
    ["definitely unnecessary", "may be needed", "definitely completed"], ["matches", "partly matches", "does not match"],
    ["closely", "partly", "not at all"], ["passed both", "passed one and failed one", "failed both"],
    ["complete", "partly complete", "not compliant"], ["occurs at all tested speeds", "only one tested speed", "no speed stated"]]
items, qflags = [], Counter()
for q in read("questions.jsonl"):
    assert q["answer"] in q["options"], q["id"]
    flag = ("claim_check" if q["type"] == "yes_no" and re.search(r"contradict|opposite|claim", q["question"], re.I) else
            "unordered_scale" if q["type"] == "score" and q["options"] in UNORDERED else None)
    qflags[flag] += 1
    it = {"id": q["id"], "type": TYPE[q["type"]], "category": flag or TYPE[q["type"]], "flag": flag, "state": q["text"],
          "question": q["question"], "options": q["options"], "answer": q["answer"]}
    if it["type"] == "score":
        it["answer_index"] = q["options"].index(q["answer"])
    if q.get("group"):
        it["pair"] = q["group"]
    items.append(it)
json.dump({"items": items}, open(HERE / "questions.json", "w"), indent=1, ensure_ascii=False)

# ---- routing -> E10 format, with flags
convs, flags = [], Counter()
for r in read("routing.jsonl"):
    messages, user_turns, prev = [], [], None
    for k, t in enumerate(r["turns"]):
        assert t["expected_agent"] in r["agents"], (r["id"], k)
        messages.append({"role": "user", "content": t["user"]})
        flag = None
        if k == 0 and re.match(r"I need help with an? .* at your ", t["user"]):
            flag = "vague_start"
        elif prev is not None and ((t["turn_type"] in STAY and t["expected_agent"] != prev) or
                                   (t["turn_type"] in SWITCH and t["expected_agent"] == prev)):
            flag = "label_conflict"
        flags[flag] += 1
        user_turns.append({"message_index": len(messages) - 1, "expected_agent": t["expected_agent"], "turn_type": t["turn_type"], "flag": flag})
        if t.get("assistant"):
            messages.append({"role": "assistant", "content": t["assistant"]})
        prev = t["expected_agent"]
    convs.append({"id": r["id"], "company": r["company"], "agents": r["agents"], "messages": messages, "user_turns": user_turns})
json.dump(convs, open(HERE / "routing.json", "w"), indent=1, ensure_ascii=False)

# ---- first turn
ft = [{"id": f["id"], "company": f["company"], "agents": f["agents"], "message": f["message"], "target_agent": f["expected_agent"],
       "type": f.get("kind", "")} for f in read("first_turn.jsonl")]
assert all(f["target_agent"] in f["agents"] for f in ft)
json.dump({"messages": ft}, open(HERE / "first_turn.json", "w"), indent=1, ensure_ascii=False)

print(f"questions {len(items)} ({dict(Counter(i['type'] for i in items))}, flags {dict(qflags)}) | routing {len(convs)} conversations, "
      f"{sum(len(c['user_turns']) for c in convs)} turns, flags {dict(flags)} | first turn {len(ft)}")
