"""Builds thanos_v4: English in, Thanos-voice English out.
- validation, test: thanos_v3 unchanged in targets; rows whose input was Roman Hinglish take its English meaning
  (source_meaning) as input instead, so every input is English (PLAIN: three rows whose meaning equals the target).
- train: the 100 thanos_v3 training pairs (same rule) + the generated pairs in raw/generated_pairs.jsonl, less DROP
  (too close to an evaluation sentence or to a demo sentence of the notebook)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V3 = HERE.parent / "thanos_v3"
DROP = {"n086", "n221"}
PLAIN = {  # the English meaning equals the v3 target here, so a plainer everyday wording is the input
    "s114": "I can help you move on Sunday if you book the van.",
    "s116": "I'll take the library book back tomorrow morning.",
    "s138": "I need the original file, not a screenshot.",
}


def load(path):
    return [json.loads(line) for line in open(path, encoding="utf-8")]


def english(r, split):
    return {"id": r["id"], "source_id": r["source_id"], "split": split, "persona_id": "thanos",
            "source": PLAIN.get(r["source_id"]) or (r["source"] if r["input_language"] == "English" else r["source_meaning"]),
            "target": r["target"], "references": r["references"], "origin": "thanos_v3"}


splits = {s: [english(r, s) for r in load(V3 / f"{s}.jsonl")] for s in ("train", "validation", "test")}
splits["train"] += [{"id": g["id"], "source_id": g["id"], "split": "train", "persona_id": "thanos", "source": g["source"],
                     "target": g["target"], "references": [g["target"]], "origin": "generated"}
                    for g in load(HERE / "raw" / "generated_pairs.jsonl") if g["id"] not in DROP]

held = {r["source"].lower() for s in ("validation", "test") for r in splits[s]}
assert not held & {r["source"].lower() for r in splits["train"]}, "a training input repeats an evaluation input"
assert all(r["source"] != r["target"] for rs in splits.values() for r in rs), "a target copies its input"

manifest = {"dataset": "thanos_v4", "personas": {"thanos": {"name": "Thanos", "description":
            "Restrained, solemn, strategic and commanding; formal diction; preserves every fact, name, quantity, "
            "negation, condition and timing; no added events, threats or conclusions."}}, "files": {}}
for s, rows in splits.items():
    with open(HERE / f"{s}.jsonl", "w", encoding="utf-8") as out:
        for r in rows:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
    manifest["files"][s] = len(rows)
json.dump(manifest, open(HERE / "manifest.json", "w"), ensure_ascii=False, indent=1)
print(manifest["files"])
