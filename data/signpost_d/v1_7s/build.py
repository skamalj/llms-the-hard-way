"""v1_7s = v1_7 + the reviewers' score-only augmentation, independent_v5_score_aug/score_aug_v1.jsonl (409 cases, 1,636 score
questions, ids SCORE-F<flow>-nnnn; R21). The independent file is copied unchanged (never edited or relabelled); SCORE- cases
are training only (notebook 11 lists the prefix "SCORE" in TRAIN_ONLY, so v1_6's dev split is unchanged). The one-variable
test against A11 (v1_7). Writes systemone.jsonl here; usage: build.py"""
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SD = HERE.parent
SOURCES = [SD / "v1_7" / "systemone.jsonl", SD / "independent_v5_score_aug" / "score_aug_v1.jsonl"]

cases = [json.loads(l) for f in SOURCES for l in open(f, encoding="utf-8")]
ids = collections.Counter(c["id"] for c in cases)
assert all(n == 1 for n in ids.values()), [i for i, n in ids.items() if n > 1][:5]
assert all("domain" in c["meta"] and set(c["meta"].get("kinds", {})) == set(c["questions"]) for c in cases)
with open(HERE / "systemone.jsonl", "w", encoding="utf-8") as out:
    for c in cases:
        out.write(json.dumps(c, ensure_ascii=False) + "\n")
types = collections.Counter(q["type"] for c in cases for q in c["questions"].values())
print({"cases": len(cases), "questions": sum(types.values()), **types,
       "by source": dict(collections.Counter("SCORE" if c["id"].startswith("SCORE") else c["id"][0] if c["id"][0] in "RV" else "v1_6"
                                             for c in cases))})
