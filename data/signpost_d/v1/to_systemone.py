"""Converts final.jsonl (our working form) to systemone.jsonl, the System One form of data/signpost_d/format_spec.md:
  yes_no -> noul: criteria {"true": <yes description>, "false": <no description>}, gold keyed true/false
  choice -> choice: criteria {label: description}, gold keyed by label
  score  -> score: criteria ["Name: description", ...] lowest first, gold keyed "0".."n-1"
Then checks every mechanical rule of the spec and prints a summary. With --apply FILE..., validator format verdicts
(format_validation/*.jsonl) are applied first: each line {"id", "qid", "verdict": "ok"|"fix", "question": {...System One
question...}, "gold": {...}} replaces that question (and its gold) in System One form."""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def convert(c):
    questions, gold, kinds = {}, {}, {}
    for q in c["questions"]:
        kinds[q["qid"]] = q.get("kind")
        lab = q["label"]
        if q["type"] == "yes_no":
            questions[q["qid"]] = {"type": "noul", "instructions": q["question"],
                                   "criteria": {"true": q["options"]["yes"], "false": q["options"]["no"]}}
            gold[q["qid"]] = {"type": "noul", "probabilities": {"true": lab["yes"], "false": lab["no"]}}
        elif q["type"] == "choice":
            questions[q["qid"]] = {"type": "choice", "instructions": q["question"], "criteria": dict(q["options"])}
            gold[q["qid"]] = {"type": "choice", "probabilities": {k: lab[k] for k in q["options"]}}
        else:
            questions[q["qid"]] = {"type": "score", "instructions": q["question"],
                                   "criteria": [f"{l['name']}: {l['description']}" for l in q["levels"]]}
            gold[q["qid"]] = {"type": "score", "probabilities": {str(i): lab[l["name"]] for i, l in enumerate(q["levels"])}}
    return {"id": c["id"], "state": c["state"], "questions": questions, "gold": gold,
            "meta": {"domain": c["domain"], "form": c["form"], "kinds": kinds,
                     "validated": {q["qid"]: q.get("validated") for q in c["questions"]}}}


def keys(q):
    return ["true", "false"] if q["type"] == "noul" else (list(q["criteria"]) if q["type"] == "choice"
                                                          else [str(i) for i in range(len(q["criteria"]))])


def check(c):
    errs = []
    if not isinstance(c["state"], (str, dict, list)) or not c["state"]:
        errs.append("state")
    for qid, q in c["questions"].items():
        where = f"{c['id']} {qid}"
        if set(q) != {"type", "instructions", "criteria"} or not qid:
            errs.append(f"{where}: fields {sorted(q)}")
        if not str(q.get("instructions", "")).strip():
            errs.append(f"{where}: no instructions")
        cr = q["criteria"]
        if q["type"] == "noul":
            if set(cr) != {"true", "false"} or not all(str(v).strip() for v in cr.values()):
                errs.append(f"{where}: noul criteria")
        elif q["type"] == "choice":
            if not isinstance(cr, dict) or not 2 <= len(cr) <= 26 or not all(str(v or "").strip() for v in cr.values()) \
                    or len({k.strip().lower() for k in cr}) != len(cr):
                errs.append(f"{where}: choice criteria")
        elif q["type"] == "score":
            if not isinstance(cr, list) or not 2 <= len(cr) <= 10 or not all(isinstance(s, str) and s.strip() for s in cr):
                errs.append(f"{where}: score criteria")
        else:
            errs.append(f"{where}: type {q['type']}")
        g = c["gold"].get(qid, {}).get("probabilities", {})
        if list(g) != keys(q) or abs(sum(g.values()) - 1) > 0.01 or min(g.values(), default=-1) < 0:
            errs.append(f"{where}: gold")
    return errs


cases = [convert(json.loads(l)) for l in open(HERE / "final.jsonl", encoding="utf-8")]
fixes = 0
for f in sorted((HERE / "format_validation").glob("validation_F*.jsonl")) if "--apply" in sys.argv else []:
    for line in open(f, encoding="utf-8"):
        if not line.strip():
            continue
        v = json.loads(line)
        if v["verdict"] == "convert":                    # a record-like text state, now JSON (same facts)
            c = next(c for c in cases if c["id"] == v["id"])
            if not c["meta"]["form"].startswith("JSON record"):
                c["meta"]["form"] = f"JSON record (from {c['meta']['form']})"
            c["state"] = v["state"]
            fixes += 1
        elif v["verdict"] == "fix":
            c = next(c for c in cases if c["id"] == v["id"])
            c["questions"][v["qid"]] = v["question"]
            c["gold"][v["qid"]] = v["gold"]
            c["meta"]["validated"][v["qid"]] = "format fix"
            fixes += 1
errors = [e for c in cases for e in check(c)]
with open(HERE / "systemone.jsonl", "w", encoding="utf-8") as out:
    for c in cases:
        out.write(json.dumps(c, ensure_ascii=False) + "\n")
types = collections.Counter(q["type"] for c in cases for q in c["questions"].values())
print({"cases": len(cases), "questions": sum(types.values()), **types, "format fixes applied": fixes, "errors": len(errors)})
for e in errors[:20]:
    print("  ", e)
