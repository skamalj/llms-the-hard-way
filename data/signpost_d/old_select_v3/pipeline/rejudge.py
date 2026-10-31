#!/usr/bin/env python3
"""R28: rejudge the 500 selected old cases with exactly the train_v4 judge setup, and flag (never fix) v3-rule problems.

Stages (resumable; a submitted batch is resumed, not resubmitted):
  judge    three Claude Haiku 5.5 judgments per record (careful_operator, by_the_book, generalist: the train_v4 personas
           and prompt from independent_v7/pipeline/records.py), one Batch API request each; the old gold is never shown
  review   one Claude Sonnet 5.5 review per record (Batch API), separate from the judges: lists v3-rule problems only
  assemble selection_rejudged.jsonl, stats.json and README.md

Usage: python rejudge.py --stage judge|review|assemble [--in ../selection.jsonl] [--work ../qc/work] [--out ..]
Every call is billed to the key in ANTHROPIC_KEY; the run stops before the ledger could pass SIGNPOST_BUDGET_USD (cap $10).
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import os
import random
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "independent_v7", "pipeline"))
os.environ.setdefault("SIGNPOST_BUDGET_USD", "10")
import llm  # noqa: E402
import records as R  # noqa: E402

BASE_SEED = 20261031_28
JUDGE_MAX_TOKENS = 12000
REVIEW_MAX_TOKENS = 8000
EST_JUDGE = 0.004   # per-request ceilings at batch rates, for the budget check only
EST_REVIEW = 0.02

REVIEW_SYSTEM = """You check records for a training set against a short list of rules. You do not answer the questions and you do not rewrite anything: you only report problems.

Report a problem only when you are fairly sure it is real. Most records have none; an empty list is the normal answer.

Problem codes:
- excluded_setting: the record's setting is, or is close to, one of these excluded settings: monitoring or reviewing runs of AI agents or automated jobs; customer support conversations or tickets of any kind (chat, email, helpdesk); vendor bills, invoices, purchase orders, procurement or tenders, accounts payable, billing, goods-received matching; security alerts, intrusion or access-anomaly triage. Use question "record".
- not_answerable: a sensible person in the role could not answer the question from the record alone (the deciding fact is not in the record, or the question refers to something absent).
- mixed_dimensions: a score scale's levels blend two different quantities (for example severity and certainty, or size and number of problems), or a choice question's options do not differ along one clear axis, so a record could fit two options or levels for different reasons.
- malformed: a true/false statement is a question rather than a claim, its true and false descriptions do not cover every case, or options and levels are duplicated or contradictory.

For each problem give the code, the question name (or "record" for the whole record) and one short sentence saying what is wrong."""

REVIEW_USER = """DOMAIN: {domain}

RECORD
{record}

QUESTIONS
{questions}

List the problems (an empty list if there are none)."""


def review_schema(qnames):
    return {"type": "object", "properties": {"flags": {"type": "array", "items": {"type": "object", "properties": {
        "code": {"type": "string", "enum": ["excluded_setting", "not_answerable", "mixed_dimensions", "malformed"]},
        "question": {"type": "string", "enum": ["record"] + list(qnames)},
        "note": {"type": "string"}}, "required": ["code", "question", "note"], "additionalProperties": False}}},
        "required": ["flags"], "additionalProperties": False}


def fam_of(rec):
    """The judge code expects a family: here each record is its own, with a generic role from its domain."""
    return {"id": rec["id"], "role": f"a reviewer who handles records in {rec['domain']}", "domain": rec["domain"], "questions": rec["questions"]}


def load_records(path):
    return [json.loads(x) for x in open(path, encoding="utf-8") if x.strip()]


def jpath(work, rid, pid):
    return os.path.join(work, "judgments", rid, f"{pid}.json")


def stage_judge(recs, work):
    out = {}
    for rnd in (1, 2):  # round 2 resubmits only failed or unparseable judgments
        items, meta = [], {}
        for rec in recs:
            fam = fam_of(rec)
            for per in R.PERSONAS:
                if os.path.exists(jpath(work, rec["id"], per["id"])):
                    continue
                rng = random.Random(f"{BASE_SEED}:{rec['id']}:{per['id']}")
                system, user, schema, shown = R.judge_messages(fam, rec["state"], per, rng)
                cid = f"j-{rec['id']}-{per['id']}"[:64]
                items.append((cid, llm.batch_params(per["model"], system, user, schema, per["effort"], JUDGE_MAX_TOKENS), f"judge {rec['id']} {per['id']}"))
                meta[cid] = (rec["id"], per, shown)
        if not items:
            break
        res = llm.run_batch(os.path.join(work, "batches"), f"judge_r{rnd}_{len(items)}", items, EST_JUDGE * len(items))
        ok = bad = 0
        for cid, (rid, per, shown) in meta.items():
            r = res.get(cid)
            j = R.parse_judgment(r["data"], shown) if r and r["ok"] else None
            if j is None:
                bad += 1
                continue
            os.makedirs(os.path.dirname(jpath(work, rid, per["id"])), exist_ok=True)
            json.dump({"persona": per["id"], "model": r["model"], "effort": per["effort"], "probabilities": j, "cost": round(r["cost"], 6)},
                      open(jpath(work, rid, per["id"]), "w"), indent=1)
            ok += 1
        out[f"round{rnd}"] = {"requests": len(items), "ok": ok, "failed": bad}
        if not bad:
            break
    return out


def stage_review(recs, work):
    out = {}
    os.makedirs(os.path.join(work, "reviews"), exist_ok=True)
    for rnd in (1, 2):
        items, meta = [], {}
        for rec in recs:
            if os.path.exists(os.path.join(work, "reviews", f"{rec['id']}.json")):
                continue
            qtext, _ = R.judge_questions_text(fam_of(rec), None)
            user = REVIEW_USER.format(domain=rec["domain"], record=json.dumps(rec["state"], indent=1, ensure_ascii=False), questions=qtext)
            cid = f"r-{rec['id']}"[:64]
            items.append((cid, llm.batch_params("sonnet", REVIEW_SYSTEM, user, review_schema(rec["questions"]), "medium", REVIEW_MAX_TOKENS), f"review {rec['id']}"))
            meta[cid] = rec["id"]
        if not items:
            break
        res = llm.run_batch(os.path.join(work, "batches"), f"review_r{rnd}_{len(items)}", items, EST_REVIEW * len(items))
        ok = bad = 0
        for cid, rid in meta.items():
            r = res.get(cid)
            if not r or not r["ok"]:
                bad += 1
                continue
            json.dump({"flags": r["data"]["flags"], "model": r["model"], "cost": round(r["cost"], 6)},
                      open(os.path.join(work, "reviews", f"{rid}.json"), "w"), indent=1)
            ok += 1
        out[f"round{rnd}"] = {"requests": len(items), "ok": ok, "failed": bad}
        if not bad:
            break
    return out


def binof(t):
    return "<0.5" if t < 0.5 else "0.5-0.7" if t < 0.7 else "0.7-0.9" if t < 0.9 else ">=0.9"


def entropy(d):
    return -sum(v * math.log(v) for v in d.values() if v > 0)


def shape(qs):
    out = {}
    for t in ("noul", "choice", "score"):
        tops = [max(g.values()) for tt, g in qs if tt == t]
        ents = [entropy(g) for tt, g in qs if tt == t]
        if not tops:
            continue
        b = collections.Counter(binof(x) for x in tops)
        out[t] = {"n": len(tops), "bins": {k: round(b[k] / len(tops), 3) for k in ("<0.5", "0.5-0.7", "0.7-0.9", ">=0.9")},
                  "mean_top": round(statistics.mean(tops), 3), "mean_entropy": round(statistics.mean(ents), 3)}
    return out


def stage_assemble(recs, work, outdir):
    personas = [p["id"] for p in R.PERSONAS]
    setup = ("three independent judgments per question, each a full distribution from a separate Batch API request with no shared context and "
             "without the old gold: " + "; ".join(f"{p['id']} ({p['model']}, effort {p['effort']})" for p in R.PERSONAS)
             + "; the train_v4 (R26) judge prompt and personas; gold = plain mean of the three, rounded to 4 decimals, never sharpened or smoothed")
    new_q, old_q, flagged, codes, missing, contested, agree, n_q = [], [], 0, collections.Counter(), [], 0, 0, 0
    rows = []
    for rec in recs:
        js = [json.load(open(jpath(work, rec["id"], pid))) if os.path.exists(jpath(work, rec["id"], pid)) else None for pid in personas]
        rv = os.path.join(work, "reviews", f"{rec['id']}.json")
        if any(j is None for j in js) or not os.path.exists(rv):
            missing.append(rec["id"])
            continue
        flags = json.load(open(rv))["flags"]
        gold, judg, cont = {}, {}, {}
        for n, q in rec["questions"].items():
            opts = R.options_of(q)
            jj = [j["probabilities"][n] for j in js]
            g = R.mean_gold(jj, opts)
            gold[n] = {"type": q["type"], "probabilities": g}
            judg[n] = [{o: round(v, 4) for o, v in x.items()} for x in jj]
            cont[n] = len({max(x, key=x.get) for x in jj}) > 1
            contested += cont[n]
            n_q += 1
            og = rec["meta"]["old_gold"][n]["probabilities"]
            agree += max(g, key=g.get) == max(og, key=og.get)
            new_q.append((q["type"], g))
            old_q.append((q["type"], og))
        if flags:
            flagged += 1
            for f in flags:
                codes[f["code"]] += 1
        out = dict(rec)
        out["gold"] = gold
        out["meta"] = dict(rec["meta"], judgments=judg, judge_setup=setup, contested=cont, v3_flags=flags)
        rows.append(out)
    with open(os.path.join(outdir, "selection_rejudged.jsonl"), "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    ledger = os.path.join(work, "ledger.jsonl")
    led = [json.loads(x) for x in open(ledger)] if os.path.exists(ledger) else []
    by = collections.defaultdict(float)
    for x in led:
        by[x["tag"].split(" ")[0]] += x["cost"]
    flagged_q = collections.Counter()
    for r in rows:
        for f in r["meta"]["v3_flags"]:
            flagged_q[f["question"] == "record"] += 1
    stats = {"records": len(rows), "questions": n_q, "missing": missing, "flagged_records": flagged, "unflagged_records": len(rows) - flagged,
             "flag_codes": dict(codes), "flags_on_whole_record": flagged_q[True], "flags_on_a_question": flagged_q[False],
             "contested_share": round(contested / max(1, n_q), 3), "top_answer_same_as_old_gold": round(agree / max(1, n_q), 3),
             "new_gold": shape(new_q), "old_gold": shape(old_q),
             "new_gold_unflagged": shape([(q["type"], r["gold"][n]["probabilities"]) for r in rows if not r["meta"]["v3_flags"] for n, q in r["questions"].items()]),
             "api_cost_usd": {"total": round(sum(by.values()), 2), "by_stage": {k: round(v, 2) for k, v in by.items()}, "requests": len(led)}}
    json.dump(stats, open(os.path.join(outdir, "stats.json"), "w"), indent=2)
    print(json.dumps({k: stats[k] for k in ("records", "questions", "flagged_records", "flag_codes", "contested_share", "top_answer_same_as_old_gold", "api_cost_usd")}))
    print(json.dumps({"new": stats["new_gold"], "old": stats["old_gold"]}))
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["judge", "review", "assemble"], required=True)
    ap.add_argument("--in", dest="inp", default=os.path.join(HERE, "..", "selection.jsonl"))
    ap.add_argument("--work", default=os.path.join(HERE, "..", "qc", "work"))
    ap.add_argument("--out", default=os.path.join(HERE, ".."))
    ap.add_argument("--limit", type=int, default=0, help="first N records only (testing)")
    args = ap.parse_args()
    os.makedirs(args.work, exist_ok=True)
    llm.LEDGER = os.environ.get("SIGNPOST_LEDGER") or os.path.join(args.work, "ledger.jsonl")
    recs = load_records(args.inp)
    if args.limit:
        recs = recs[:args.limit]
    try:
        if args.stage == "judge":
            res = stage_judge(recs, args.work)
        elif args.stage == "review":
            res = stage_review(recs, args.work)
        else:
            stage_assemble(recs, args.work, args.out)
            return
    except llm.BudgetStop as e:
        res = {"stopped": str(e)}
    print(json.dumps({"stage": args.stage, **res, "spent_usd": round(llm.spent(), 2)}))


if __name__ == "__main__":
    main()
