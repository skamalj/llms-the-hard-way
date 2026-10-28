"""v1_7 = v1_6 + the reviewers' independent training cases: independent_v1/train.jsonl (418, ids R-) and
independent_v2/train_v2.jsonl (2,085, ids V-; R15, weighted towards computed score questions). The independent files are
copied unchanged (never edited or relabelled); R- and V- cases are training only (notebook 11 keeps them out of dev, so
v1_6's dev split is unchanged). Writes systemone.jsonl here; usage: build.py"""
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SD = HERE.parent
SOURCES = [SD / "v1_6" / "systemone.jsonl", SD / "independent_v1" / "train.jsonl", SD / "independent_v2" / "train_v2.jsonl"]

cases = [json.loads(l) for f in SOURCES for l in open(f, encoding="utf-8")]
ids = collections.Counter(c["id"] for c in cases)
assert all(n == 1 for n in ids.values()), [i for i, n in ids.items() if n > 1][:5]
assert all("domain" in c["meta"] and set(c["meta"].get("kinds", {})) == set(c["questions"]) for c in cases)
with open(HERE / "systemone.jsonl", "w", encoding="utf-8") as out:
    for c in cases:
        out.write(json.dumps(c, ensure_ascii=False) + "\n")
types = collections.Counter(q["type"] for c in cases for q in c["questions"].values())
print({"cases": len(cases), "questions": sum(types.values()), **types,
       "by source": dict(collections.Counter(c["id"][0] if c["id"][0] in "RV" else "v1_6" for c in cases))})
