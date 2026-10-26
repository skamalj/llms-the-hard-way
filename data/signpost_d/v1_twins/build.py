"""Builds the twin cases (brief_v2_4_twins.md) into System One form with gold, then D_SET v1_4 = v1_3 + these.

cases_TA1, TA2 (new base cases and their twins) and cases_TB1, TB2 (twins of v1_3 training cases), with
labels/labels_<batch>_<opus|sonnet|fable>.jsonl -> gold = the three labellers' average; then validation/validation_*.jsonl
verdicts ("fix" replaces a question and its gold, "relabel" the gold, "drop" removes a question, qid "*" a case). Each
twin keeps twin_of and the change note in meta (never shown to the model). All twin cases are for training only: a
notebook must keep the "T" cases out of dev. Writes systemone.jsonl here and ../v1_4/systemone.jsonl (v1_3's cases
followed by these)."""
import collections
import json
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODELS = ("opus", "sonnet", "fable")
BATCHES = ("TA1", "TA2", "TB1", "TB2")


def keys(q):
    return ["true", "false"] if q["type"] == "noul" else (list(q["criteria"]) if q["type"] == "choice"
                                                          else [str(i) for i in range(len(q["criteria"]))])


cases, labs = [], {m: {} for m in MODELS}
for k in BATCHES:
    cases += [json.loads(l) for l in open(HERE / f"cases_{k}.jsonl", encoding="utf-8")]
    for m in MODELS:
        for line in open(HERE / "labels" / f"labels_{k}_{m}.jsonl", encoding="utf-8"):
            r = json.loads(line)
            labs[m][r["id"]] = r["answers"]
agree, tops = collections.Counter(), []
for c in cases:
    c["gold"] = {}
    for qid, q in c["questions"].items():
        d = [labs[m][c["id"]][qid] for m in MODELS]
        assert all(list(x) == keys(q) for x in d), (c["id"], qid, [list(x) for x in d], keys(q))
        g = {k: round(sum(x[k] for x in d) / 3, 4) for k in keys(q)}
        c["gold"][qid] = {"type": q["type"], "probabilities": g}
        agree["all"] += len({max(x, key=x.get) for x in d}) == 1
        agree["n"] += 1
        tops.append(max(g.values()))
    c["meta"] = {"domain": c.pop("domain", ""), "form": c.pop("form", ""), "kinds": c.pop("kinds", {}),
                 "twin_of": c.pop("twin_of", None), "change": c.pop("change", "")}

verdicts = collections.Counter()
for f in sorted((HERE / "validation").glob("validation_*.jsonl")):
    for line in open(f, encoding="utf-8"):
        if not line.strip():
            continue
        v = json.loads(line)
        verdicts[v["verdict"]] += 1
        c = next(c for c in cases if c["id"] == v["id"])
        if v["verdict"] == "drop":
            if v["qid"] == "*":
                cases.remove(c)
            else:
                c["questions"].pop(v["qid"]); c["gold"].pop(v["qid"])
        elif v["verdict"] in ("fix", "relabel"):
            c["questions"][v["qid"]] = v.get("question", c["questions"][v["qid"]])
            c["gold"][v["qid"]] = v["gold"]
cases = [c for c in cases if len(c["questions"]) >= 2]

def check(c):
    """The mechanical checks of v1/to_systemone.py (copied: importing that script would rebuild v1)."""
    errs = []
    for qid, q in c["questions"].items():
        where = f"{c['id']} {qid}"
        cr = q.get("criteria")
        if set(q) != {"type", "instructions", "criteria"} or not str(q.get("instructions", "")).strip():
            errs.append(f"{where}: fields")
        elif q["type"] == "noul" and (set(cr) != {"true", "false"} or not all(str(v).strip() for v in cr.values())):
            errs.append(f"{where}: noul criteria")
        elif q["type"] == "choice" and (not 2 <= len(cr) <= 26 or not all(str(v or "").strip() for v in cr.values())):
            errs.append(f"{where}: choice criteria")
        elif q["type"] == "score" and (not isinstance(cr, list) or not 2 <= len(cr) <= 10):
            errs.append(f"{where}: score criteria")
        g = c["gold"].get(qid, {}).get("probabilities", {})
        if list(g) != keys(q) or abs(sum(g.values()) - 1) > 0.01:
            errs.append(f"{where}: gold")
    return errs


errors = [e for c in cases for e in check(c)]
errors += [f"{c['id']} {qid}: noul not a statement" for c in cases for qid, q in c["questions"].items()
           if q["type"] == "noul" and "?" in q["instructions"]]
with open(HERE / "systemone.jsonl", "w", encoding="utf-8") as out:
    for c in cases:
        out.write(json.dumps(c, ensure_ascii=False) + "\n")
base = open(HERE.parent / "v1_3" / "systemone.jsonl", encoding="utf-8").read()
(HERE.parent / "v1_4").mkdir(exist_ok=True)
with open(HERE.parent / "v1_4" / "systemone.jsonl", "w", encoding="utf-8") as out:
    out.write(base)
    for c in cases:
        out.write(json.dumps(c, ensure_ascii=False) + "\n")
types = collections.Counter(q["type"] for c in cases for q in c["questions"].values())
print({"twin-batch cases": len(cases), "twins": sum(bool(c["meta"]["twin_of"]) for c in cases), "questions": sum(types.values()), **types, "verdicts": dict(verdicts),
       "all three agree on top": round(agree["all"] / agree["n"], 3), "mean top": round(statistics.mean(tops), 3),
       "JSON states": sum(not isinstance(c["state"], str) for c in cases), "errors": len(errors)})
for e in errors[:20]:
    print("  ", e)
