"""Builds thanos_v7 = thanos_v6 + new everyday pairs, in the style of the user's five examples (raw/style_examples.md):
- raw/generated_pairs_2.jsonl: 250 pairs written by a Claude subagent (g001-g250);
- raw/user_pairs.jsonl: 215 pairs from the user's files thanos_lingo_test_dataset.md (150) and
  thanos_lingo_daily_examples_75.md (75), less the 5 manual-test sentences that appear in both;
- raw/verdicts.jsonl: a second subagent's verdict on each of these 465 pairs (pass / fix with a corrected target / drop);
- REVIEW: my overrides after reading every fix; EXCLUDE: pairs too close to a protected sentence.
Also writes validation_daily.jsonl: the user's 25 held-out everyday examples (raw/user_validation_25.jsonl), less
any input that is already a training input. validation.jsonl and test.jsonl are thanos_v6's, unchanged."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
V6 = HERE.parent / "thanos_v6"
REVIEW = {"u150_137": "My tire has fallen flat. The wheel… fails me."}   # validator's fix added "the journey halts"
EXCLUDE = {"g084", "u150_053", "d75_026",     # word overlap >= 0.5 with a validation_daily sentence
           "g076"}                           # same input as d75_039 (the user's version kept)
MANUAL = [                                    # the user's manual end-of-run test: never trained on
    "I'll be late to the office because of traffic.",
    "I'm running 10 minutes late. Please start without me.",
    "I'm really hungry. Let's get something to eat.",
    "I'm exhausted after today's work. I need some rest.",
    "I'm stuck in a meeting. I'll call you when I'm free.",
]
DEMO = [                                      # the notebooks' final-cell sentences
    "I worked all weekend to fix the bug, and nobody noticed.",
    "We can still win this game if we don't give up in the second half.",
    "My brother borrowed my car and returned it with an empty tank.",
    "I'm not angry that you lied; I'm disappointed that you thought you had to.",
    "The project is three weeks late, but the client still wants it by Friday.",
    "I trained for a year, and I missed the medal by one second.",
]
BANNED = re.compile(r"\b(inevitab\w*|destiny|universe|balance\w*|equilibrium|snap|infinity|stones)\b", re.I)


def load(path):
    return [json.loads(line) for line in open(path, encoding="utf-8")]


def similarity(a, b):
    a, b = (set(re.findall(r"[a-z']+", t.lower())) for t in (a, b))
    return len(a & b) / max(1, len(a | b))


splits = {s: load(V6 / f"{s}.jsonl") for s in ("train", "validation", "test")}
verdict = {v["id"]: v for v in load(HERE / "raw" / "verdicts.jsonl")}
new = []
for name, origin in (("generated_pairs_2.jsonl", "generated_2"), ("user_pairs.jsonl", "user_files")):
    for r in load(HERE / "raw" / name):
        v = verdict[r["id"]]
        if v["verdict"] == "drop" or r["id"] in EXCLUDE:
            continue
        target = REVIEW.get(r["id"]) or (v["fixed_target"] if v["verdict"] == "fix" else r["target"])
        new.append({"id": r["id"], "source_id": r["id"], "split": "train", "persona_id": "thanos", "source": r["source"],
                    "target": target, "references": [target], "origin": origin})

train_inputs = {r["source"].lower() for r in splits["train"] + new}
daily = [{"id": u["id"], "source_id": u["id"], "split": "validation_daily", "persona_id": "thanos", "source": u["source"],
          "target": u["target"], "references": [u["target"]], "origin": "user_files"}
         for u in load(HERE / "raw" / "user_validation_25.jsonl") if u["source"].lower() not in train_inputs]

protected = [r["source"] for s in ("validation", "test") for r in splits[s]] + [r["source"] for r in daily] + MANUAL + DEMO
assert len({r["source"].lower() for r in new}) == len(new), "duplicate input among new pairs"
for r in new:
    assert r["source"] != r["target"] and not re.search(r"\d", r["target"]) and not BANNED.search(r["target"]), r["id"]
    assert max(similarity(r["source"], p) for p in protected) < 0.5, ("too close to a protected sentence", r["id"])
splits["train"] += new
splits["validation_daily"] = daily

manifest = json.load(open(V6 / "manifest.json"))
manifest.update(dataset="thanos_v7", files={})
for s, rows in splits.items():
    with open(HERE / f"{s}.jsonl", "w", encoding="utf-8") as out:
        for r in rows:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
    manifest["files"][s] = len(rows)
json.dump(manifest, open(HERE / "manifest.json", "w"), ensure_ascii=False, indent=1)
print(manifest["files"], {o: sum(r.get("origin") == o for r in splits["train"]) for o in ("generated_2", "user_files", "handwritten")})
