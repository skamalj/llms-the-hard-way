#!/usr/bin/env python3
"""Assemble train_v4 (R26): gold = plain mean of the three Haiku judgments (as measured), the R26 accept rule (a
question is off plan when its measured top answer is neither the planned answer nor, for a balanced or contested plan,
the planned second answer; a record is dropped when more than --max-off-plan of its questions are off plan), selection of
--keep records per family towards R22.4.3 with no near-duplicate pairs, every check of R22.4.3 and R22.9, and the files.

Usage: python assemble.py --work WORK --per-family 45 --keep 25 --out OUT
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design  # noqa: E402
import records as R  # noqa: E402

OUT_FILE = "train_v4.jsonl"
STATS_FILE = "stats.json"
QC_SUFFIX = ""
TARGETS = {  # R22.4.3
    "noul": {"bins": {"<0.5": (0, 0), "0.5-0.7": (.30, .40), "0.7-0.9": (.28, .38), ">=0.9": (.27, .37)}, "mean_top": (.75, .81), "entropy": (.40, .50)},
    "choice": {"bins": {"<0.5": (.15, .25), "0.5-0.7": (.38, .50), "0.7-0.9": (.17, .27), ">=0.9": (.10, .18)}, "mean_top": (.62, .68), "entropy": (.75, .92)},
    "score": {"bins": {"<0.5": (.18, .28), "0.5-0.7": (.45, .57), "0.7-0.9": (.15, .25), ">=0.9": (.03, .09)}, "mean_top": (.58, .64), "entropy": (.83, .98)},
}
POS_TARGETS = {"score": {"lowest": (.10, .16), "middle": (.57, .67), "highest": (.22, .30)}, "choice": {"first": (.15, .25), "middle": (.60, .70), "last": (.10, .18)}}
CONTESTED = (.30, .40)
CONTESTED_FAMILY = (.15, .55)
NOUL_TRUE = (.45, .50)
NOUL_NULL = (.30, .36)


def binof(t):
    return "<0.5" if t < 0.5 else "0.5-0.7" if t < 0.7 else "0.7-0.9" if t < 0.9 else ">=0.9"


def entropy(d):
    return -sum(v * math.log(v) for v in d.values() if v > 0)


def position(q, top):
    opts = R.options_of(q)
    i = opts.index(top)
    if q["type"] == "score":
        return "lowest" if i == 0 else "highest" if i == len(opts) - 1 else "middle"
    return "first" if i == 0 else "last" if i == len(opts) - 1 else "middle"


def inr(x, rng):
    return rng[0] - 1e-9 <= x <= rng[1] + 1e-9


def load_candidates(work, fams, per_family):
    cands, dropped = collections.defaultdict(list), collections.Counter()
    personas = [p["id"] for p in R.PERSONAS]
    for fid, fam in fams.items():
        for i in range(1, per_family + 1):
            rid = f"{fid}-{i:04d}"
            rp = os.path.join(work, "records", f"{rid}.json")
            if not os.path.exists(rp):
                dropped["record not written"] += 1
                continue
            rec = json.load(open(rp))
            js = {}
            for pid in personas:
                jp = os.path.join(work, "judgments", rid, f"{pid}.json")
                if os.path.exists(jp):
                    js[pid] = json.load(open(jp))
            if len(js) < len(personas):
                dropped["judgments incomplete"] += 1
                continue
            qinfo = {}
            for name, q in fam["questions"].items():
                opts = R.options_of(q)
                judg = [js[pid]["probabilities"][name] for pid in personas]
                g = R.mean_gold(judg, opts)
                top = max(g, key=g.get)
                tops = [max(j, key=j.get) for j in judg]
                qinfo[name] = {"gold": g, "top": top, "top_p": g[top], "contested": len(set(tops)) > 1, "judgments": judg,
                               "entropy": entropy(g), "type": q["type"]}
            rec["judges"] = js
            rec["q"] = qinfo
            rec["misses"] = R.off_plan(rec["plan"], {n: qi["gold"] for n, qi in qinfo.items()})
            cands[fid].append(rec)
    return cands, dropped


def contributions(fam, rec):
    c = collections.Counter()
    for name, qi in rec["q"].items():
        q = fam["questions"][name]
        t = q["type"]
        c[(t, "n")] += 1
        c[(t, "bin", binof(qi["top_p"]))] += 1
        c[(t, "top_sum")] += qi["top_p"]
        c[(t, "ent_sum")] += qi["entropy"]
        c[("all", "n")] += 1
        c[("all", "contested")] += qi["contested"]
        if t == "noul":
            c[("noul", "true")] += qi["top"] == "true"
        else:
            c[(t, "pos", position(q, qi["top"]))] += 1
    return c


def mid(r):
    return (r[0] + r[1]) / 2


def loss(c):
    L = 0.0
    for t, tg in TARGETS.items():
        n = c[(t, "n")]
        if not n:
            continue
        for b, r in tg["bins"].items():
            L += (c[(t, "bin", b)] / n - mid(r)) ** 2
        L += (c[(t, "top_sum")] / n - mid(tg["mean_top"])) ** 2
        L += 0.3 * (c[(t, "ent_sum")] / n - mid(tg["entropy"])) ** 2
    for t, tg in POS_TARGETS.items():
        n = c[(t, "n")]
        if n:
            for k, r in tg.items():
                L += (c[(t, "pos", k)] / n - mid(r)) ** 2
    if c[("all", "n")]:
        L += 2 * (c[("all", "contested")] / c[("all", "n")] - mid(CONTESTED)) ** 2
    if c[("noul", "n")]:
        L += 2 * (c[("noul", "true")] / c[("noul", "n")] - mid(NOUL_TRUE)) ** 2
    return L


def near_dup(a: dict, b: dict) -> bool:
    keys = set(a) & set(b)
    allk = set(a) | set(b)
    return bool(allk) and sum(a[k] == b[k] for k in keys) / len(allk) > 0.5


def select(fams, cands, keep):
    contrib = {fid: [contributions(fams[fid], r) for r in rs] for fid, rs in cands.items()}
    leaves = {fid: [dict(leaf_values(r["state"])) for r in rs] for fid, rs in cands.items()}
    chosen = {fid: [] for fid in cands}
    total = collections.Counter()
    remaining = {fid: list(range(len(rs))) for fid, rs in cands.items()}
    while True:
        best = None
        for fid, idxs in remaining.items():
            if len(chosen[fid]) >= keep:
                continue
            for i in idxs:
                if any(near_dup(leaves[fid][i], leaves[fid][j]) for j in chosen[fid]):
                    continue  # R24: no near-duplicate pairs within a family
                L = loss(total + contrib[fid][i])
                if best is None or L < best[0]:
                    best = (L, fid, i)
        if best is None:
            break
        _, fid, i = best
        chosen[fid].append(i)
        remaining[fid].remove(i)
        total += contrib[fid][i]
    return {fid: [cands[fid][i] for i in sorted(ix)] for fid, ix in chosen.items()}, total


def leaf_values(o, prefix=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaf_values(v, f"{prefix}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaf_values(v, f"{prefix}[{i}]")
    else:
        yield prefix, json.dumps(o)


def type_stats(qs):
    n = len(qs)
    if not n:
        return None
    bins = collections.Counter(binof(q["top_p"]) for q in qs)
    return {"n": n, "bins": {b: round(bins[b] / n, 3) for b in ("<0.5", "0.5-0.7", "0.7-0.9", ">=0.9")},
            "mean_top": round(statistics.mean(q["top_p"] for q in qs), 3), "mean_entropy": round(statistics.mean(q["entropy"] for q in qs), 3)}


def check_range(name, val, rng, checks):
    ok = inr(val, rng)
    checks.append({"check": name, "value": val, "target": list(rng), "pass": ok})
    return ok


def compute_stats(fams, sel):
    checks, out = [], {}
    allq = [dict(qi, family=fid, name=n, q=fams[fid]["questions"][n]) for fid, rs in sel.items() for r in rs for n, qi in r["q"].items()]
    out["records"] = sum(len(rs) for rs in sel.values())
    out["questions"] = len(allq)
    out["by_type"] = {}
    for t, tg in TARGETS.items():
        qs = [q for q in allq if q["type"] == t]
        st = type_stats(qs)
        out["by_type"][t] = st
        if st:
            for b, r in tg["bins"].items():
                check_range(f"{t} share top {b}", st["bins"][b], r, checks)
            check_range(f"{t} mean top", st["mean_top"], tg["mean_top"], checks)
            check_range(f"{t} mean entropy", st["mean_entropy"], tg["entropy"], checks)
    cont = round(sum(q["contested"] for q in allq) / max(1, len(allq)), 3)
    out["contested_share"] = cont
    check_range("contested share (judges' tops disagree)", cont, CONTESTED, checks)
    for t, tg in POS_TARGETS.items():
        qs = [q for q in allq if q["type"] == t]
        pc = collections.Counter(position(q["q"], q["top"]) for q in qs)
        out[f"{t}_top_position"] = {k: round(pc[k] / max(1, len(qs)), 3) for k in tg}
        for k, r in tg.items():
            check_range(f"{t} top at {k}", out[f"{t}_top_position"][k], r, checks)
    nq = [q for q in allq if q["type"] == "noul"]
    out["noul_true_top"] = round(sum(q["top"] == "true" for q in nq) / max(1, len(nq)), 3)
    check_range("noul true top", out["noul_true_top"], NOUL_TRUE, checks)
    out["noul_criteria_null"] = round(sum(q["q"]["criteria"] is None for q in nq) / max(1, len(nq)), 3)
    check_range("noul criteria null", out["noul_criteria_null"], NOUL_NULL, checks)
    zeros = sum(1 for q in allq for v in q["gold"].values() if v == 0)
    out["gold_zero_probabilities"] = zeros
    sq = [q for q in allq if q["type"] == "score"]
    far = [sum(v for o, v in q["gold"].items() if abs(int(o) - int(q["top"])) >= 2) for q in sq]
    out["score_mass_two_or_more_from_top_mean"] = round(statistics.mean(far), 4) if far else None
    if far:
        checks.append({"check": "score mass >= 2 levels from top (mean)", "value": out["score_mass_two_or_more_from_top_mean"], "target": [0, 0.10],
                       "pass": out["score_mass_two_or_more_from_top_mean"] < 0.10})
    # per family
    out["by_family"] = {}
    for fid, rs in sel.items():
        fq = [q for q in allq if q["family"] == fid]
        fc = round(sum(q["contested"] for q in fq) / max(1, len(fq)), 3)
        fn = [q for q in fq if q["type"] == "noul"]
        ft = round(sum(q["top"] == "true" for q in fn) / len(fn), 3) if fn else None
        out["by_family"][fid] = {"domain": fams[fid]["domain"], "records": len(rs), "contested_share": fc, "noul_true_top": ft,
                                 "by_type": {t: type_stats([q for q in fq if q["type"] == t]) for t in TARGETS},
                                 "skills": fams[fid]["skills"], "shared_scale": fams[fid]["shared_scale"]}
        check_range(f"{fid} contested share", fc, CONTESTED_FAMILY, checks)
        if ft is not None:
            check_range(f"{fid} noul true top", ft, (.25, .70), checks)
    # format and structure (R22.5, R22.9)
    nf = len(fams)
    choice_q = [q for f in fams.values() for q in f["questions"].values() if q["type"] == "choice"]
    score_q = [q for f in fams.values() for q in f["questions"].values() if q["type"] == "score"]
    named = sum(all(":" in x for x in q["criteria"]) for q in score_q)
    out["format"] = {"families": nf, "five_questions_each": all(len(f["questions"]) == 5 for f in fams.values()),
                     "choice_options": dict(collections.Counter(len(q["criteria"]) for q in choice_q)),
                     "score_levels": dict(collections.Counter(len(q["criteria"]) for q in score_q)),
                     "score_named_levels_share": round(named / max(1, len(score_q)), 3),
                     "types": dict(collections.Counter(q["type"] for q in allq))}
    checks.append({"check": "every family has exactly 5 questions", "value": out["format"]["five_questions_each"], "target": True, "pass": out["format"]["five_questions_each"]})
    words = sorted(R.record_words(r["state"]) for rs in sel.values() for r in rs)
    secs = [len(r["state"]) for rs in sel.values() for r in rs]
    out["record_words"] = {"median": words[len(words) // 2], "p10": words[len(words) // 10], "p90": words[9 * len(words) // 10], "max": words[-1]} if words else None
    checks.append({"check": "records have 3-6 sections", "value": [min(secs), max(secs)] if secs else None, "target": [3, 6], "pass": bool(secs) and min(secs) >= 3 and max(secs) <= 6})
    if words:
        checks.append({"check": "record words max <= 320", "value": words[-1], "target": [0, 320], "pass": words[-1] <= 320})
    sk = collections.Counter(s for f in fams.values() for s in f["skills"])
    out["skills_share_of_families"] = {s: round(sk[s] / nf, 3) for s in sorted(design.SKILLS)}
    for s, need in (("S1", .40), ("S2", .25), ("S3", .50)):
        checks.append({"check": f"skill {s} share of families", "value": out["skills_share_of_families"][s], "target": [need, 1], "pass": out["skills_share_of_families"][s] >= need})
    doms = collections.Counter(f["domain"] for f in fams.values())
    out["domains"] = len(doms)
    checks.append({"check": "at least 6 domains", "value": len(doms), "target": [6, None], "pass": len(doms) >= 6})
    # near-duplicates within a family
    neardup = 0
    for fid, rs in sel.items():
        leaves = [dict(leaf_values(r["state"])) for r in rs]
        for i in range(len(leaves)):
            for j in range(i + 1, len(leaves)):
                keys = set(leaves[i]) & set(leaves[j])
                allk = set(leaves[i]) | set(leaves[j])
                if allk and sum(leaves[i][k] == leaves[j][k] for k in keys) / len(allk) > 0.5:
                    neardup += 1
    out["near_duplicate_record_pairs"] = neardup
    checks.append({"check": "no near-duplicate records in a family (>50% of field values equal)", "value": neardup, "target": 0, "pass": neardup == 0})
    out["checks_passed"] = sum(c["pass"] for c in checks)
    out["checks_total"] = len(checks)
    out["checks"] = checks
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--per-family", type=int, default=45)
    ap.add_argument("--keep", type=int, default=25)
    ap.add_argument("--max-misses", type=int, default=1, help="drop a record when more than this many of its questions are off plan (R26 accept rule)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    fams = {}
    for s in design.SLOTS:
        fp = os.path.join(args.work, "families", f"{s['id']}.json")
        if os.path.exists(fp):
            fams[s["id"]] = json.load(open(fp))
    cands, dropped = load_candidates(args.work, fams, args.per_family)
    miss_drop = collections.Counter()
    for fid in list(cands):
        keep = [r for r in cands[fid] if len(r["misses"]) <= args.max_misses]
        miss_drop[fid] = len(cands[fid]) - len(keep)
        cands[fid] = keep
    sel, _ = select(fams, cands, args.keep)
    stats = compute_stats(fams, sel)
    stats["generation"] = {"records_planned_per_family": args.per_family, "kept_per_family": args.keep,
                           "dropped_before_judging": dict(dropped), "dropped_for_plan_miss": dict(miss_drop),
                           "candidates_after_filter": {fid: len(v) for fid, v in cands.items()},
                           "plan_miss_rule": "a question is off plan when its measured top answer is neither the planned answer nor, for a balanced or contested plan, "
                                             f"the planned second answer; a record is dropped when more than {args.max_misses} of its questions are off plan"}
    ledger = os.path.join(args.work, "ledger.jsonl")
    if os.path.exists(ledger):
        rows = [json.loads(x) for x in open(ledger)]
        by, st = collections.defaultdict(float), collections.defaultdict(float)
        for x in rows:
            by[x["model"]] += x["cost"]
            st[x["tag"].split(" ")[0]] += x["cost"]
        stats["api_cost_usd"] = {"total": round(sum(by.values()), 2), "by_model": {k: round(v, 2) for k, v in by.items()},
                                 "by_stage": {k: round(v, 2) for k, v in st.items()}, "requests": len(rows),
                                 "batched_requests": sum(1 for x in rows if x.get("batch"))}
    os.makedirs(os.path.join(args.out, "qc"), exist_ok=True)
    judge_setup = ("three independent judgments per question, each a full distribution from a separate API request with no shared context: "
                   + "; ".join(f"{p['id']} ({p['model']}, effort {p['effort']})" for p in R.PERSONAS)
                   + "; gold = plain mean of the three, rounded to 4 decimals, never sharpened or smoothed")
    with open(os.path.join(args.out, OUT_FILE), "w", encoding="utf-8") as fh:
        for fid, rs in sel.items():
            fam = fams[fid]
            for r in rs:
                case = {"id": r["id"], "family": fid, "domain": fam["domain"], "state": r["state"], "questions": fam["questions"],
                        "gold": {n: {"type": fam["questions"][n]["type"], "probabilities": qi["gold"]} for n, qi in r["q"].items()},
                        "meta": {"factors": r["factors"], "skills": fam["skills"], "plan": {n: v["clarity"] for n, v in r["plan"].items()},
                                 "judgments": {n: [{o: round(v, 4) for o, v in j.items()} for j in qi["judgments"]] for n, qi in r["q"].items()},
                                 "judge_setup": judge_setup, "contested": {n: qi["contested"] for n, qi in r["q"].items()},
                                 "deciding": r.get("deciding", {}), "off_plan": r["misses"]}}
                fh.write(json.dumps(case, ensure_ascii=False) + "\n")
    json.dump(stats, open(os.path.join(args.out, STATS_FILE), "w"), indent=2)
    json.dump({fid: {k: v for k, v in f.items() if k != "design_cost"} for fid, f in fams.items()}, open(os.path.join(args.out, "qc", f"families{QC_SUFFIX}.json"), "w"), indent=1, ensure_ascii=False)
    scales = os.path.join(args.work, "scales.json")
    if os.path.exists(scales):
        json.dump(json.load(open(scales))["scales"], open(os.path.join(args.out, "qc", f"shared_scales{QC_SUFFIX}.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"records": stats["records"], "checks": f"{stats['checks_passed']}/{stats['checks_total']}",
                      "failed": [c["check"] + f" = {c['value']} (target {c['target']})" for c in stats["checks"] if not c["pass"]],
                      "by_type": stats["by_type"], "contested": stats["contested_share"], "cost": stats.get("api_cost_usd")}, indent=1))


if __name__ == "__main__":
    main()
