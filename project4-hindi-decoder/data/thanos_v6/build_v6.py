"""Builds thanos_v6 = thanos_v5 + raw/handwritten_pairs_2.jsonl (100 more pairs written by hand, h101-h200, same strict,
weighty voice as v5's h001-h100). Validation and test unchanged. Same checks as build_v5.py, now also against v5's
handwritten pairs."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
V5 = HERE.parent / "thanos_v5"
DEMO = [                                    # the notebook's final-cell sentences (as in build_v5.py)
    "I worked all weekend to fix the bug, and nobody noticed.",
    "We can still win this game if we don't give up in the second half.",
    "My brother borrowed my car and returned it with an empty tank.",
    "I'm not angry that you lied; I'm disappointed that you thought you had to.",
    "The project is three weeks late, but the client still wants it by Friday.",
    "I trained for a year, and I missed the medal by one second.",
]


def load(path):
    return [json.loads(line) for line in open(path, encoding="utf-8")]


def similarity(a, b):
    a, b = (set(re.findall(r"[a-z']+", t.lower())) for t in (a, b))
    return len(a & b) / max(1, len(a | b))


splits = {s: load(V5 / f"{s}.jsonl") for s in ("train", "validation", "test")}
hand = [{"id": h["id"], "source_id": h["id"], "split": "train", "persona_id": "thanos", "source": h["source"],
         "target": h["target"], "references": [h["target"]], "origin": "handwritten"}
        for h in load(HERE / "raw" / "handwritten_pairs_2.jsonl")]

protected = [r["source"] for s in ("validation", "test") for r in splits[s]] + DEMO
for r in hand:
    assert r["source"] != r["target"] and not re.search(r"\d", r["target"]), r["id"]
    assert max(similarity(r["source"], p) for p in protected) < 0.5, ("too close to an evaluation or demo sentence", r["id"])
    assert max(similarity(r["source"], t["source"]) for t in splits["train"]) < 0.6, ("repeats a training input", r["id"])
for d in DEMO:
    assert max(similarity(d, t["source"]) for t in splits["train"] + hand) < 0.5, ("demo sentence near training", d)
splits["train"] += hand

manifest = json.load(open(V5 / "manifest.json"))
manifest.update(dataset="thanos_v6", files={})
for s, rows in splits.items():
    with open(HERE / f"{s}.jsonl", "w", encoding="utf-8") as out:
        for r in rows:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
    manifest["files"][s] = len(rows)
json.dump(manifest, open(HERE / "manifest.json", "w"), ensure_ascii=False, indent=1)
print(manifest["files"])
