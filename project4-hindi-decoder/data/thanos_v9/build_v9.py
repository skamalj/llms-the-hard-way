"""Builds thanos_v9: the user's own style throughout, with the user's own lines weighted.

1. The 1,088 non-d75 training targets and the 25 test targets of thanos_v8 are rewritten towards the user's signature
   moves (raw/rewrite_brief.md: the situation as subject, a "…" before a closing clause, a mood clause where it fits)
   by three rewriter subagents (raw/out_*.jsonl); three validator subagents check facts, thin "…" to about 1 target in
   5 (the user's own lines use it rarely) and fix readability (raw/verdicts_*.jsonl).
2. The user's file of 500 daily examples (raw/user_daily_500.json): 69 rows are the file of 75 already in v8 (d75_*);
   13 are excluded as too close to a protected sentence (the user's five manual-test sentences and near-copies, and
   validation/test sentences); 418 are new (raw/d500_new.jsonl), fact-checked by a subagent (raw/d500_verdicts.jsonl,
   22 minimal fixes); DROP removes 7 garbled or nonsensical template rows; REVIEW holds my overrides.
3. 100 new handwritten pairs h201-h300 (raw/handwritten_pairs_3.jsonl).
4. The user's own lines (d75_* and d500_*) appear twice in train (WEIGHT).
validation.jsonl and validation_daily.jsonl are unchanged; test inputs unchanged, targets rewritten as above."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
V8 = HERE.parent / "thanos_v8"
DROP = {"d500_452", "d500_458", "d500_471", "d500_476", "d500_480",   # garbled template rows
        "d500_463", "d500_491"}                                         # nonsensical ("buy the keys", "leave by the appointment")
REVIEW = {"d500_237": "This library's silence is too deep for a phone call.",
          "d500_365": "The API answers only with errors."}   # the fact fix had left it equal to its input
WEIGHT = 2
MANUAL = [
    "I'll be late to the office because of traffic.",
    "I'm running 10 minutes late. Please start without me.",
    "I'm really hungry. Let's get something to eat.",
    "I'm exhausted after today's work. I need some rest.",
    "I'm stuck in a meeting. I'll call you when I'm free.",
]
DEMO = [
    "I worked all weekend to fix the bug, and nobody noticed.",
    "We can still win this game if we don't give up in the second half.",
    "My brother borrowed my car and returned it with an empty tank.",
    "I'm not angry that you lied; I'm disappointed that you thought you had to.",
    "The project is three weeks late, but the client still wants it by Friday.",
    "I trained for a year, and I missed the medal by one second.",
]
BANNED = re.compile(r"\b(inevitab\w*|destiny|universe|equilibrium|snap|infinity|stones)\b|(?<!bank )\bbalance\w*", re.I)


def load(path):
    return [json.loads(line) for line in open(path, encoding="utf-8")]


def similarity(a, b):
    a, b = (set(re.findall(r"[a-z']+", t.lower())) for t in (a, b))
    return len(a & b) / max(1, len(a | b))


def final_targets(outs, verdicts):
    rows = {r["id"]: r for r in outs}
    return {v["id"]: v["fixed_target"] if v["verdict"] == "fix" else rows[v["id"]]["target"] for v in verdicts}


splits = {s: load(V8 / f"{s}.jsonl") for s in ("train", "validation", "test", "validation_daily")}

# 1. restyled targets
RESTYLE_REVIEW = {"u150_064": "I gather my belongings and pack them for the journey ahead."}   # validator's fix read awkwardly
new_target = {}
for k in (1, 2, 3):
    new_target.update(final_targets(load(HERE / "raw" / f"out_{k}.jsonl"), load(HERE / "raw" / f"verdicts_{k}.jsonl")))
new_target.update(RESTYLE_REVIEW)
used = set()
for s, key in (("train", lambda r: r["id"]), ("test", lambda r: "test_" + r["id"])):
    for r in splits[s]:
        k = key(r)
        if k in new_target:
            r.update(previous_target=r["target"], target=new_target[k], references=[new_target[k]])
            r["origin"] = r.get("origin", "").replace("+dramatic", "") + "+v9style"
            used.add(k)
assert used == set(new_target), "a rewritten id was not found"


def row(i, source, target, origin):
    return {"id": i, "source_id": i, "split": "train", "persona_id": "thanos", "source": source, "target": target,
            "references": [target], "origin": origin}


# 2. the user's 500-file, new rows
d500 = final_targets(load(HERE / "raw" / "d500_new.jsonl"), load(HERE / "raw" / "d500_verdicts.jsonl"))
d500.update(REVIEW)
src500 = {r["id"]: r["source"] for r in load(HERE / "raw" / "d500_new.jsonl")}
new = [row(i, src500[i], t, "user_daily_500") for i, t in d500.items() if i not in DROP]
# 3. handwritten
new += [row(h["id"], h["source"], h["target"], "handwritten") for h in load(HERE / "raw" / "handwritten_pairs_3.jsonl")]

SUPERSEDED = {"n328", "n083", "u150_008"}   # same input as the user's d500_080, d500_178, d500_314: the user's version kept
splits["train"] = [r for r in splits["train"] if r["id"] not in SUPERSEDED]
protected = [r["source"] for s in ("validation", "test", "validation_daily") for r in splits[s]] + MANUAL + DEMO
train_inputs = {r["source"].lower() for r in splits["train"]}
for r in new:
    assert r["source"].lower() not in train_inputs, ("input already in train", r["id"])
    assert max(similarity(r["source"], p) for p in protected) < 0.5, ("too close to a protected sentence", r["id"])
splits["train"] += new

# 4. weight the user's own lines
user_rows = [r for r in splits["train"] if r["id"].startswith(("d75_", "d500_"))]
splits["train"] += [{**r, "id": f"{r['id']}#{k}"} for k in range(2, WEIGHT + 1) for r in user_rows]

for r in splits["train"] + splits["test"]:
    assert r["source"] != r["target"] and not re.search(r"\d", r["target"]) and not BANNED.search(r["target"]), r["id"]

manifest = json.load(open(V8 / "manifest.json"))
manifest.update(dataset="thanos_v9", files={})
for s, rows in splits.items():
    with open(HERE / f"{s}.jsonl", "w", encoding="utf-8") as out:
        for r in rows:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
    manifest["files"][s] = len(rows)
json.dump(manifest, open(HERE / "manifest.json", "w"), ensure_ascii=False, indent=1)
print(manifest["files"], "| restyled", len(used), "| user rows", len(user_rows), "x", WEIGHT, "| new", len(new))
