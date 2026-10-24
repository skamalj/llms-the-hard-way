"""Builds final.jsonl for D_SET v1: the pilot's final.jsonl (300 cases, already validated) followed by the 1,200 new
cases (cases_G.jsonl, raw/gen_S01..S04.jsonl), each question's label = the three labellers' average (soft_labels.jsonl),
then the validators' verdicts (validation/validation_V01..V12.jsonl, then my final review, validation/review.jsonl,
which overrides them) applied:
  keep    -> unchanged (a genuinely mixed question, label as averaged)
  fix     -> the question replaced by the validator's fixed_question, label = the validator's label
  relabel -> label = the validator's label
  drop    -> the question removed ("qid": "*" removes the case)
A case left with fewer than 2 questions is removed. Forms are normalised to the brief's six. Prints a summary and checks
every label against its options."""
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FORMS = {"form": "form or checklist", "email": "message thread"}


def names(q):
    return [l["name"] for l in q["levels"]] if q["type"] == "score" else list(q["options"])


cases = []
for f in ["cases_G.jsonl"] + [f"raw/gen_S0{k}.jsonl" for k in range(1, 5)]:
    cases += [json.loads(l) for l in open(HERE / f, encoding="utf-8")]
soft = {r["id"]: r["soft_labels"] for r in map(json.loads, open(HERE / "soft_labels.jsonl", encoding="utf-8"))}
verdicts = {}
for f in [f"validation_V{k:02d}.jsonl" for k in range(1, 13)] + ["review.jsonl"]:
    for line in open(HERE / "validation" / f, encoding="utf-8"):
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
        final.append({**c, "form": FORMS.get(c["form"], c["form"]), "questions": qs})

pilot = [json.loads(l) for l in open(HERE.parent / "pilot" / "final.jsonl", encoding="utf-8")]
with open(HERE / "final.jsonl", "w", encoding="utf-8") as out:
    for c in pilot + final:
        out.write(json.dumps(c, ensure_ascii=False) + "\n")
allq = [q for c in pilot + final for q in c["questions"]]
print({"verdicts": dict(count), "new cases": len(final), "pilot cases": len(pilot),
       "cases": len(pilot) + len(final), "questions": len(allq)},
      collections.Counter(q["type"] for q in allq), collections.Counter(q["kind"] for q in allq),
      collections.Counter(c["form"] for c in pilot + final))
