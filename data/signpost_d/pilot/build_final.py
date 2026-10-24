"""Builds final.jsonl: cases.jsonl with each question's label = the three labellers' average (soft_labels.jsonl), then the
validators' verdicts (validation_1.jsonl, validation_2.jsonl) applied:
  keep    -> unchanged (a genuinely mixed question, label as averaged)
  fix     -> the question replaced by the validator's fixed_question, label = the validator's label
  relabel -> label = the validator's label
  drop    -> the question removed ("qid": "*" removes the case)
A case left with fewer than 2 questions is removed. Prints a summary and checks every label against its options."""
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def names(q):
    return [l["name"] for l in q["levels"]] if q["type"] == "score" else list(q["options"])


cases = [json.loads(l) for l in open(HERE / "cases.jsonl", encoding="utf-8")]
soft = {r["id"]: r["soft_labels"] for r in map(json.loads, open(HERE / "soft_labels.jsonl", encoding="utf-8"))}
verdicts = {}
for k in (1, 2):
    for line in open(HERE / f"validation_{k}.jsonl", encoding="utf-8"):
        if line.strip():
            v = json.loads(line)
            verdicts[(v["id"], v["qid"])] = v
count = collections.Counter(v["verdict"] for v in verdicts.values())

final = []
for c in cases:
    if verdicts.get((c["id"], "*"), {}).get("verdict") == "drop":
        continue
    qs = []
    for q in c["questions"]:
        v = verdicts.get((c["id"], q["qid"]))
        label = soft[c["id"]][q["qid"]]
        if v and v["verdict"] == "drop":
            continue
        if v and v["verdict"] == "fix":
            q = {**v["fixed_question"], "qid": q["qid"], "kind": v["fixed_question"].get("kind", q.get("kind"))}
            label = v["label"]
        elif v and v["verdict"] == "relabel":
            label = v["label"]
        assert list(label) == names(q), (c["id"], q["qid"], list(label), names(q))
        assert abs(sum(label.values()) - 1) < 0.01, (c["id"], q["qid"])
        qs.append({**q, "label": label, "validated": v["verdict"] if v else "pass"})
    if len(qs) >= 2:
        final.append({**c, "questions": qs})
with open(HERE / "final.jsonl", "w", encoding="utf-8") as out:
    for c in final:
        out.write(json.dumps(c, ensure_ascii=False) + "\n")
print({"verdicts": dict(count), "cases": len(final), "questions": sum(len(c["questions"]) for c in final)},
      collections.Counter(q["type"] for c in final for q in c["questions"]))
