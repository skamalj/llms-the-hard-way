#!/usr/bin/env python3
"""v6 pipeline runner (R22 decision records). Every model call goes to the Anthropic API with the key in ANTHROPIC_KEY.

Stages (resumable: an item is skipped when its output file exists):
  scales     the three cross-family shared scales (Opus)
  families   one family specification per slot, checked against R22.5 (Opus, up to 3 attempts)
  records    per family, N records: factors and plan sampled by code, record written by Sonnet (up to 3 attempts)
  judge      five independent judgments per record (Opus, 2 x Sonnet, 2 x Haiku; separate calls)

Usage:
  python run.py --work WORK --stage scales
  python run.py --work WORK --stage families
  python run.py --work WORK --stage records --per-family 36
  python run.py --work WORK --stage judge --per-family 36
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm import call  # noqa: E402
import design  # noqa: E402
import records as R  # noqa: E402

BASE_SEED = 20261031


def p(work, *parts):
    path = os.path.join(work, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def load(path):
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else None


def save(path, obj):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)


def stage_scales(work):
    out = p(work, "scales.json")
    if os.path.exists(out):
        return "skip"
    for _ in range(3):
        r = call("opus", design.SCALES_SYSTEM, design.SCALES_USER, design.SCALES_SCHEMA, effort="high", tag="scales")
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
    user = design.DESIGN_USER.format(fid=slot["id"], domain=slot["domain"], text_note=text_note, question_plan=design.plan_text(plan), skills=skills)
    if shared:
        user += f'\n\nNote: this family also uses a shared score scale, added separately, named "{shared["name"]}" ({shared["instructions"]}). Do not write it among your questions, and do not duplicate it.'
    reasons = []
    for _ in range(3):
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


def do_record(work, fam, idx):
    rid = f"{fam['id']}-{idx:04d}"
    out = p(work, "records", f"{rid}.json")
    if os.path.exists(out):
        return "skip"
    rng = random.Random(f"{BASE_SEED}:{rid}")
    factors = R.sample_factors(fam, rng)
    plan = R.sample_plan(fam, rng)
    n_words = R.target_words(rng)
    system, user, schema = R.render_messages(fam, factors, plan, n_words)
    reasons = []
    for _ in range(3):
        r = call("sonnet", system, user, schema, effort="medium", tag=f"record {rid}")
        if not r["ok"]:
            reasons.append(r["error"])
            continue
        try:
            state = json.loads(r["data"]["record_json"])
        except json.JSONDecodeError as e:
            reasons.append(f"record_json not JSON: {e}")
            continue
        why = R.check_record(state, fam, n_words)
        if why is None:
            save(out, {"id": rid, "family": fam["id"], "state": state, "factors": R.final_factors(fam, factors, r["data"]["factors"]),
                       "factors_sampled": factors, "plan": plan, "target_words": n_words, "model": r["model"], "cost": r["cost"]})
            return "ok"
        reasons.append(why)
        user = user.split("\n\nA previous attempt")[0] + f"\n\nA previous attempt was rejected: {why}. Fix that."
    save(p(work, "records_rejected", f"{rid}.json"), {"reasons": reasons})
    return f"fail {rid}: {reasons}"


def do_judge(work, fam, idx, persona):
    rid = f"{fam['id']}-{idx:04d}"
    out = p(work, "judgments", rid, f"{persona['id']}.json")
    if os.path.exists(out):
        return "skip"
    rec = load(p(work, "records", f"{rid}.json"))
    if rec is None:
        return "norecord"
    rng = random.Random(f"{BASE_SEED}:{rid}:{persona['id']}")
    system, user, schema, shown = R.judge_messages(fam, rec["state"], persona, rng)
    for _ in range(3):
        r = call(persona["model"], system, user, schema, effort=persona["effort"], tag=f"judge {rid} {persona['id']}")
        if not r["ok"]:
            continue
        j = R.parse_judgment(r["data"], shown)
        if j:
            save(out, {"persona": persona["id"], "model": r["model"], "effort": persona["effort"], "probabilities": j, "cost": r["cost"]})
            return "ok"
    return f"fail judge {rid} {persona['id']}"


def run_jobs(jobs, workers, limit):
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
            if tag not in ("ok", "skip", "norecord"):
                print(res, flush=True)
    return {"elapsed_s": round(time.time() - t0), "counts": counts}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--stage", choices=["scales", "families", "records", "judge"], required=True)
    ap.add_argument("--per-family", type=int, default=36)
    ap.add_argument("--families", default="", help="comma-separated family ids (default all)")
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args()
    os.environ.setdefault("SIGNPOST_LEDGER", os.path.join(args.work, "ledger.jsonl"))
    import llm
    llm.LEDGER = os.environ["SIGNPOST_LEDGER"]
    os.makedirs(args.work, exist_ok=True)
    only = set(args.families.split(",")) if args.families else None
    slots = [s for s in design.SLOTS if not only or s["id"] in only]

    if args.stage == "scales":
        res = {"counts": {stage_scales(args.work).split(" ")[0]: 1}}
    elif args.stage == "families":
        scales = load(p(args.work, "scales.json"))["scales"]
        res = run_jobs([(do_family, (args.work, s, scales)) for s in slots], min(args.workers, 8), None)
    else:
        fams = [load(p(args.work, "families", f"{s['id']}.json")) for s in slots]
        fams = [f for f in fams if f]
        if args.stage == "records":
            jobs = [(do_record, (args.work, f, i)) for f in fams for i in range(1, args.per_family + 1)]
        else:
            jobs = [(do_judge, (args.work, f, i, per)) for f in fams for i in range(1, args.per_family + 1) for per in R.PERSONAS]
        res = run_jobs(jobs, args.workers, None)
    print(json.dumps({"stage": args.stage, **res}), flush=True)


if __name__ == "__main__":
    main()
