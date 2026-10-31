#!/usr/bin/env python3
"""v8 (R30) pipeline runner: train_v5 decision records. Every model call goes to the Anthropic API with the key in
ANTHROPIC_KEY, and the whole run stops before it could exceed SIGNPOST_BUDGET_USD (cap $50 for R30) in the ledger.

Stages (resumable: finished items are skipped; a submitted batch is resumed, not resubmitted):
  scales     the three cross-family shared scales (Opus, direct call)
  families   one family specification per slot, checked against R22.5 (Opus, direct calls, up to 3 attempts)
  records    per family, N records written 5 per request by Sonnet through the Message Batches API, with the
             family brief as a cached system block; factors and plans are drawn by code; failed checks are dropped
             (no rework); requests that error at the API are resubmitted once
  judge      three Haiku judgments per record (three stances), one request each, through the Batches API;
             requests that error or return an incomplete judgment are resubmitted once

Usage:
  python run.py --work WORK --stage scales
  python run.py --work WORK --stage families [--families F201,F202]
  python run.py --work WORK --stage records --per-family 50 [--families ...]
  python run.py --work WORK --stage judge --per-family 50 [--families ...]
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import llm  # noqa: E402
from llm import call  # noqa: E402
import design  # noqa: E402
import records as R  # noqa: E402

BASE_SEED = 20261102  # fresh seeds: pilots used 20261031, train_v4 20261101
GROUP = 5             # records per writer request (R26)
REC_MAX_TOKENS = 40000
JUDGE_MAX_TOKENS = 12000
# conservative per-request cost ceilings at batch rates, used only for the budget check before a batch is submitted
EST_RECORD_REQUEST = 0.08  # train_v4 averaged $0.062 per 5-record request at batch rates
EST_JUDGE_REQUEST = 0.0008  # train_v4 averaged $0.0004 per Haiku judgment at batch rates


def p(work, *parts):
    path = os.path.join(work, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def load(path):
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else None


def save(path, obj):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)


# ----------------------------------------------------------------------------- scales and families (direct calls)

def stage_scales(work):
    out = p(work, "scales.json")
    if os.path.exists(out):
        return "skip"
    llm.check_budget(0.5, "shared scales")
    for _ in range(3):
        r = call("opus", design.SCALES_SYSTEM, design.SCALES_USER_C, design.SCALES_SCHEMA, effort="high", tag="scales")
        if not r["ok"]:
            continue
        sc = r["data"]["scales"]
        ok = len(sc) == 3 and all(len(s["levels"]) == 4 and s["instructions"].strip().endswith("?") and 5 <= design.words(s["instructions"]) <= 14
                                  and all(4 <= design.words(x) <= 10 for x in s["levels"]) for s in sc)
        if ok:
            for s in sc:
                s["name"] = design.snake(s["name"])
            save(out, {"scales": sc, "model": r["model"], "cost": r["cost"]})
            return "ok"
    return "fail scales"


def shared_for(slot, scales):
    users = [s["id"] for s in design.SLOTS if s["shared"] is not None]
    if slot["shared"] is None:
        return None
    return scales[users.index(slot["id"]) % len(scales)]


def do_family(work, slot, scales):
    out = p(work, "families", f"{slot['id']}.json")
    if os.path.exists(out):
        return "skip"
    shared = shared_for(slot, scales)
    plan = design.question_plan(slot, shared)
    text_note = "About a third of settings use 1 to 3 short free-text fields (a note, an evidence line, or a few one-sentence messages inside the JSON); this one should" + ("" if int(slot["id"][1:]) % 3 == 1 else " not") + " include such fields."
    skills = "\n".join(f"- {k}: {design.SKILLS[k]}" for k in sorted(set(slot["skills"] + design.ALWAYS_SKILLS)))
    user = design.DESIGN_USER.format(fid=slot["id"], domain=slot["domain"], text_note=text_note, question_plan=design.plan_text(plan), skills=skills,
                                     anchor_rules=design.ANCHOR_RULES)
    if shared:
        user += f'\n\nNote: this family also uses a shared score scale, added separately, named "{shared["name"]}" ({shared["instructions"]}). Do not write it among your questions, and do not duplicate it.'
    reasons = []
    for _ in range(3):
        llm.check_budget(0.6, f"family {slot['id']}")
        r = call("opus", design.DESIGN_SYSTEM, user, design.FAMILY_SCHEMA, effort="high", tag=f"family {slot['id']}")
        if not r["ok"]:
            reasons.append(r["error"])
            continue
        fam, why = design.build_family(slot, r["data"], shared)
        if fam:
            fam["design_cost"] = r["cost"]
            save(out, fam)
            return "ok"
        reasons.append(why)
        user += f"\n\nA previous attempt was rejected by the format check: {why}. Follow the rules exactly."
    save(p(work, "families_rejected", f"{slot['id']}.json"), {"reasons": reasons})
    return f"fail {slot['id']}: {reasons}"


def run_jobs(jobs, workers):
    t0, counts = time.time(), {}
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(fn, *a) for fn, a in jobs]
        for f in cf.as_completed(futs):
            try:
                res = f.result()
            except Exception as e:  # noqa: BLE001
                res = f"error {type(e).__name__}: {e}"
            tag = res.split(" ")[0]
            counts[tag] = counts.get(tag, 0) + 1
            if tag not in ("ok", "skip"):
                print(res, flush=True)
    return {"elapsed_s": round(time.time() - t0), "counts": counts}


# ----------------------------------------------------------------------------- records (batched, 5 per request)

def batch_key(items):
    """A batch is named by its exact set of request ids, so a rerun resumes it and a different set never reuses its results."""
    return hashlib.sha1("|".join(sorted(cid for cid, _, _ in items)).encode()).hexdigest()[:12]


def spec_for(fam, idx):
    rid = f"{fam['id']}-{idx:04d}"
    rng = random.Random(f"{BASE_SEED}:{rid}")
    factors = R.sample_factors(fam, rng)
    plan = R.sample_plan(fam, rng)
    return {"id": rid, "key": f"R{(idx - 1) % GROUP + 1}", "factors": factors, "plan": plan, "target_words": R.target_words(rng)}


def record_done(work, rid):
    return os.path.exists(os.path.join(work, "records", f"{rid}.json")) or os.path.exists(os.path.join(work, "records_rejected", f"{rid}.json"))


def record_requests(work, fams, per_family):
    """One request per group of 5 records whose outcome is not yet recorded."""
    items, groups = [], {}
    for fam in fams:
        n = per_family[fam["id"]]
        for g0 in range(1, n + 1, GROUP):
            idxs = [i for i in range(g0, min(g0 + GROUP, n + 1))]
            specs = [spec_for(fam, i) for i in idxs]
            todo = [s for s in specs if not record_done(work, s["id"])]
            if not todo:
                continue
            for k, s in enumerate(todo):
                s["key"] = f"R{k + 1}"
            cid = f"rec-{fam['id']}-{g0:04d}"
            system, user, schema = R.multi_messages(fam, todo)
            items.append((cid, llm.batch_params("sonnet", system, user, schema, "medium", REC_MAX_TOKENS), f"records {cid}"))
            groups[cid] = (fam, todo)
    return items, groups


def store_records(work, groups, results):
    counts, api_failed = {}, []
    for cid, (fam, todo) in groups.items():
        r = results.get(cid)
        if not r or not r["ok"]:
            api_failed.append(cid)
            continue
        got = {x["key"]: x for x in r["data"].get("records", [])}
        per = (r.get("cost") or 0) / max(1, len(todo))
        for s in todo:
            x = got.get(s["key"])
            why = None
            if x is None:
                why = "writer returned no record for this key"
            else:
                try:
                    state = json.loads(x["record_json"])
                    why = R.check_record(state, fam, s["target_words"])
                except json.JSONDecodeError as e:
                    why = f"record_json not JSON: {e}"
            if why:
                save(p(work, "records_rejected", f"{s['id']}.json"), {"id": s["id"], "reason": why, "plan": s["plan"], "target_words": s["target_words"],
                                                                      "raw": x["record_json"] if x else None})
                counts["rejected"] = counts.get("rejected", 0) + 1
                continue
            deciding = {d["question"]: d["evidence"] for d in x["deciding"]}
            save(p(work, "records", f"{s['id']}.json"), {"id": s["id"], "family": fam["id"], "state": state,
                                                         "factors": R.final_factors(fam, s["factors"], x["factors"]), "factors_sampled": s["factors"],
                                                         "plan": s["plan"], "target_words": s["target_words"], "deciding": deciding,
                                                         "request": cid, "model": r.get("model"), "cost": round(per, 6)})
            counts["ok"] = counts.get("ok", 0) + 1
    return counts, api_failed


def stage_records(work, fams, per_family):
    summary = {}
    for rnd in (1, 2):  # round 2 resubmits only requests that failed at the API (error, refusal, max_tokens, bad JSON)
        items, groups = record_requests(work, fams, per_family)
        if rnd == 2:
            items = [it for it in items if it[0] in failed]
            groups = {k: v for k, v in groups.items() if k in failed}
        if not items:
            break
        name = f"records_r{rnd}_{len(items)}_{batch_key(items)}"
        res = llm.run_batch(os.path.join(work, "batches"), name, items, EST_RECORD_REQUEST * len(items))
        counts, failed = store_records(work, groups, res)
        summary[f"round{rnd}"] = {"requests": len(items), **counts, "api_failed": len(failed)}
        if not failed:
            break
    return summary


# ----------------------------------------------------------------------------- judgments (batched, one request per judge)

def judge_requests(work, fams, per_family):
    items, meta = [], {}
    for fam in fams:
        for i in range(1, per_family[fam["id"]] + 1):
            rid = f"{fam['id']}-{i:04d}"
            rec = load(os.path.join(work, "records", f"{rid}.json"))
            if rec is None:
                continue
            for per in R.PERSONAS:
                if os.path.exists(os.path.join(work, "judgments", rid, f"{per['id']}.json")):
                    continue
                rng = random.Random(f"{BASE_SEED}:{rid}:{per['id']}")
                system, user, schema, shown = R.judge_messages(fam, rec["state"], per, rng)
                cid = f"j-{rid}-{per['id']}"
                items.append((cid, llm.batch_params(per["model"], system, user, schema, per["effort"], JUDGE_MAX_TOKENS), f"judge {rid} {per['id']}"))
                meta[cid] = (rid, per, shown)
    return items, meta


def stage_judge(work, fams, per_family):
    summary = {}
    for rnd in (1, 2):
        items, meta = judge_requests(work, fams, per_family)
        if not items:
            break
        name = f"judge_r{rnd}_{len(items)}_{batch_key(items)}"
        res = llm.run_batch(os.path.join(work, "batches"), name, items, EST_JUDGE_REQUEST * len(items))
        ok = bad = 0
        for cid, (rid, per, shown) in meta.items():
            r = res.get(cid)
            j = R.parse_judgment(r["data"], shown) if r and r["ok"] else None
            if j is None:
                bad += 1
                continue
            save(p(work, "judgments", rid, f"{per['id']}.json"), {"persona": per["id"], "model": r["model"], "effort": per["effort"],
                                                                  "probabilities": j, "cost": round(r["cost"], 6)})
            ok += 1
        summary[f"round{rnd}"] = {"requests": len(items), "ok": ok, "failed": bad}
        if not bad:
            break
    return summary


def per_family_counts(fams, default, spec):
    counts = {f["id"]: default for f in fams}
    for part in filter(None, spec.split(",")):
        fid, n = part.split(":")
        counts[fid.strip()] = int(n)
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--stage", choices=["scales", "families", "records", "judge"], required=True)
    ap.add_argument("--per-family", type=int, default=50)
    ap.add_argument("--families", default="", help="comma-separated family ids (default all)")
    ap.add_argument("--per-family-map", default="", help="per-family record counts overriding --per-family, e.g. F201:125,F203:110 (top-up runs)")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    os.makedirs(args.work, exist_ok=True)
    llm.LEDGER = os.environ.get("SIGNPOST_LEDGER") or os.path.join(args.work, "ledger.jsonl")
    only = set(args.families.split(",")) if args.families else None
    slots = [s for s in design.SLOTS if not only or s["id"] in only]
    try:
        if args.stage == "scales":
            res = {"counts": {stage_scales(args.work).split(" ")[0]: 1}}
        elif args.stage == "families":
            scales = load(p(args.work, "scales.json"))["scales"]
            res = run_jobs([(do_family, (args.work, s, scales)) for s in slots], args.workers)
        else:
            fams = [f for f in (load(p(args.work, "families", f"{s['id']}.json")) for s in slots) if f]
            counts = per_family_counts(fams, args.per_family, args.per_family_map)
            res = (stage_records if args.stage == "records" else stage_judge)(args.work, fams, counts)
    except llm.BudgetStop as e:
        res = {"stopped": str(e)}
    print(json.dumps({"stage": args.stage, **res, "spent_usd": round(llm.spent(), 2)}), flush=True)


if __name__ == "__main__":
    main()
