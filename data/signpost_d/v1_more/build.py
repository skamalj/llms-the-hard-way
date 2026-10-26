"""Builds the harder general cases (brief_v2_5_general.md) into System One form with gold.

cases_<batch>.jsonl (System One questions, no gold) + labels/labels_<batch>_<opus|sonnet|fable>.jsonl -> gold = the three
labellers' average; then validation/validation_<batch>.jsonl verdicts ("fix" and "relabel" replace a question's wording
and gold, "drop" removes a question, qid "*" a case). Only batches with a validation file are built. Checks every rule
of format_spec.md that a script can, prints agreement and sharpness, and writes systemone.jsonl here; the notebooks
combine it with v1_3. Usage: build.py"""
import collections
import json
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODELS = ("opus", "sonnet", "fable")


def keys(q):
    return ["true", "false"] if q["type"] == "noul" else (list(q["criteria"]) if q["type"] == "choice"
                                                          else [str(i) for i in range(len(q["criteria"]))])


batches = sorted(f.stem.split("_")[1] for f in (HERE / "validation").glob("validation_*.jsonl"))
cases, labs = [], {m: {} for m in MODELS}
for b in batches:
    cases += [json.loads(l) for l in open(HERE / f"cases_{b}.jsonl", encoding="utf-8")]
    for m in MODELS:
        for line in open(HERE / "labels" / f"labels_{b}_{m}.jsonl", encoding="utf-8"):
            r = json.loads(line)
            labs[m][r["id"]] = r["answers"]
agree, tops = collections.Counter(), []
for c in cases:
    c["gold"] = {}
    for qid, q in c["questions"].items():
        d = [labs[m][c["id"]][qid] for m in MODELS]
        assert all(list(x) == keys(q) for x in d), (c["id"], qid)
        g = {k: round(sum(x[k] for x in d) / 3, 4) for k in keys(q)}
        c["gold"][qid] = {"type": q["type"], "probabilities": g}
        agree["all"] += len({max(x, key=x.get) for x in d}) == 1
        agree["n"] += 1
        tops.append(max(g.values()))
    c["meta"] = {"domain": c.pop("domain", ""), "form": c.pop("form", ""), "kinds": c.pop("kinds", {}),
                 "features": c.pop("features", [])}

by_id = {c["id"]: c for c in cases}
verdicts = collections.Counter()
for b in batches:
    for line in open(HERE / "validation" / f"validation_{b}.jsonl", encoding="utf-8"):
        if not line.strip():
            continue
        v = json.loads(line)
        verdicts[v["verdict"]] += 1
        c = by_id.get(v["id"])
        if c is None:
            continue
        if v["verdict"] == "drop":
            if v["qid"] == "*":
                by_id.pop(c["id"])
            else:
                c["questions"].pop(v["qid"], None); c["gold"].pop(v["qid"], None); c["meta"]["kinds"].pop(v["qid"], None)
        elif v["verdict"] in ("fix", "relabel"):
            c["questions"][v["qid"]] = v.get("question", c["questions"][v["qid"]])
            c["gold"][v["qid"]] = v["gold"]
cases = [c for c in by_id.values() if len(c["questions"]) >= 2]


def check(c):
    errs = []
    for qid, q in c["questions"].items():
        where = f"{c['id']} {qid}"
        cr = q.get("criteria")
        if set(q) != {"type", "instructions", "criteria"} or not str(q.get("instructions", "")).strip():
            errs.append(f"{where}: fields")
        elif q["type"] == "noul" and (set(cr) != {"true", "false"} or not all(str(v).strip() for v in cr.values())
                                      or q["instructions"].rstrip().endswith("?")):
            errs.append(f"{where}: noul")
        elif q["type"] == "choice" and (not 2 <= len(cr) <= 26 or not all(str(v or "").strip() for v in cr.values())):
            errs.append(f"{where}: choice criteria")
        elif q["type"] == "score" and (not isinstance(cr, list) or not 2 <= len(cr) <= 10 or not all(": " in s for s in cr)):
            errs.append(f"{where}: score criteria")
        g = c["gold"].get(qid, {}).get("probabilities", {})
        if list(g) != keys(q) or abs(sum(g.values()) - 1) > 0.01:
            errs.append(f"{where}: gold")
    return errs


errors = [e for c in cases for e in check(c)]
with open(HERE / "systemone.jsonl", "w", encoding="utf-8") as out:
    for c in cases:
        out.write(json.dumps(c, ensure_ascii=False) + "\n")
types = collections.Counter(q["type"] for c in cases for q in c["questions"].values())
print({"batches": batches, "cases": len(cases), "questions": sum(types.values()), **types, "verdicts": dict(verdicts),
       "all three agree on top": round(agree["all"] / agree["n"], 3), "mean top": round(statistics.mean(tops), 3),
       "JSON states": sum(not isinstance(c["state"], str) for c in cases), "errors": len(errors)})
for e in errors[:20]:
    print("  ", e)
