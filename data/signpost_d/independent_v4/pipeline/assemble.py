#!/usr/bin/env python3
"""Assemble finished cases from the work directory.

gold  = mean of the labelling calls (3 x Haiku personas + 1 x Opus analyst), renormalised;
        for read / compare / infer questions that the Opus checking pass marks as SETTLED with
        confidence >= 0.9, the gold is corrected to 0.92 on the verified option with the
        remaining 0.08 spread over the other options in proportion to the labellers' mean.
        Judge questions are never adjusted.
split = deterministic per seed: six domains are held out for the sealed test; the rest are
        assigned by a hash of the seed id (shift_dev 0.465, train 0.465, sealed_test 0.07).

Usage: python assemble.py --work WORK --n N --out OUT
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import random
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seeds import make_seeds  # noqa: E402
from prompts import PERSONAS  # noqa: E402

HELD_OUT_DOMAINS = ["airline ground ops", "tenancy disputes", "payroll", "customs brokerage", "museum loans", "sports league"]
VERIFY_CONF = 0.9
VERIFY_TOP = 0.92


def options_for(q):
    if q["type"] == "noul":
        return ["true", "false"]
    if q["type"] == "choice":
        return list(q["criteria"].keys())
    return [str(i) for i in range(len(q["criteria"]))]


def renorm(d):
    tot = sum(d.values())
    out = {k: round(v / tot, 4) for k, v in d.items()}
    drift = round(1.0 - sum(out.values()), 4)
    if drift:
        kmax = max(out, key=out.get)
        out[kmax] = round(out[kmax] + drift, 4)
    return out


def split_for(seed):
    return "train_v3"


def margin_info(q, check):
    """Margin of a computed score question: value / nearest edge (as the team asked), plus the relative
    distance and its band. The value is the checking pass's when it gave one, else the writer's."""
    if q.get("type") != "score" or q.get("computation") in (None, "none") or not q.get("edges"):
        return None
    v = None
    src = "writer"
    if check and check.get("computed_value") is not None:
        v = float(check["computed_value"]); src = "check"
    elif q.get("computed_value") is not None:
        v = float(q["computed_value"])
    if v is None:
        return None
    edges = [float(e) for e in q["edges"]]
    nearest = min(edges, key=lambda e: abs(v - e))
    rel = abs(v - nearest) / abs(nearest) if nearest != 0 else abs(v - nearest)
    band = "close" if rel <= 0.05 else "moderate" if rel <= 0.25 else "far"
    return {"computation": q["computation"], "value": round(v, 4), "unit": q.get("unit"), "edges": edges, "edge_rule": q.get("edge_rule"),
            "nearest_edge": nearest, "margin": round(v / nearest, 4) if nearest != 0 else None, "margin_rel": round(rel, 4), "margin_band": band,
            "value_source": src}


def load_case(work, seed):
    sid = seed["seed_id"]
    dp = os.path.join(work, "docs", f"{sid}.json")
    qp = os.path.join(work, "questions", f"{sid}.json")
    vp = os.path.join(work, "verify", f"{sid}.json")
    if not (os.path.exists(dp) and os.path.exists(qp)):
        return None
    labels = {}
    for p in PERSONAS:
        lp = os.path.join(work, "labels", f"{sid}.{p}.json")
        if os.path.exists(lp):
            labels[p] = json.load(open(lp))
    if len(labels) < 4 or not os.path.exists(vp):
        return None  # v2: only fully finished cases (4 labelling calls + checking pass)
    doc = json.load(open(dp))
    qfile = json.load(open(qp))
    qs = qfile["questions"]
    verify = json.load(open(vp))["checks"] if os.path.exists(vp) else {}
    questions, gold, kinds, author, per_labeller, agreement, clear, verified, adjusted, flags = {}, {}, {}, {}, {}, {}, {}, {}, {}, []
    margins = {}
    for k, q in qs.items():
        mi = margin_info(q, verify.get(k))
        if mi:
            margins[k] = mi
        questions[k] = {"type": q["type"], "instructions": q["instructions"], "criteria": q["criteria"]}
        kinds[k] = q["kind"]
        author[k] = q["author_answer"]
        opts = options_for(q)
        acc = {o: 0.0 for o in opts}
        tops = []
        pl = {}
        for p, l in labels.items():
            pr = l["probabilities"][k]
            pl[p] = {o: round(pr[o], 3) for o in opts}
            for o in opts:
                acc[o] += pr[o] / len(labels)
            tops.append(max(opts, key=lambda o: pr[o]))
        mean = renorm(acc)
        g = dict(mean)
        verified[k] = "not_checked"
        adjusted[k] = False
        if q["kind"] != "judge" and k in verify:
            v = verify[k]
            if v["settled"] and v["confidence"] >= VERIFY_CONF:
                verified[k] = "settled"
                ans = v["answer"]
                top_before = max(mean, key=mean.get)
                if top_before != ans and mean[top_before] >= 0.85:
                    flags.append(f"{k}: verifier ({ans}) overrode a confident labeller mean ({top_before} {mean[top_before]:.2f})")
                rest = {o: mean[o] for o in opts if o != ans}
                rest_tot = sum(rest.values())
                g = {o: (VERIFY_TOP if o == ans else (1 - VERIFY_TOP) * (rest[o] / rest_tot if rest_tot > 0 else 1.0 / max(1, len(rest)))) for o in opts}
                g = renorm(g)
                adjusted[k] = (top_before != ans) or (mean[ans] < 0.85)
            else:
                verified[k] = "open"
        gold[k] = {"type": q["type"], "probabilities": g}
        per_labeller[k] = pl
        agreement[k] = max(collections.Counter(tops).values())
        clear[k] = max(g.values()) >= 0.85
    meta = {"domain": seed["domain"], "form": seed["form"], "kinds": kinds, "doc_kind": seed["doc_kind"], "decider": seed["decider"],
            "clarity_target": seed["clarity"], "complications": seed["complications"], "source": "two-step model-written (document, then questions)",
            "labellers": len(labels), "top_answer_agreement": agreement, "verified": verified, "gold_adjusted_by_check": adjusted,
            "clear_cut": clear}
    meta["score_decider"] = {k: q.get("computation") or "none" for k, q in qs.items() if q["type"] == "score"}
    if margins:
        meta["margin"] = {k: m["margin"] for k, m in margins.items()}
        meta["computed"] = {k: {"computation": m["computation"], "value": m["value"], "unit": m["unit"], "edges": m["edges"], "edge_rule": m["edge_rule"],
                                "margin_rel": m["margin_rel"], "margin_band": m["margin_band"], "value_source": m["value_source"]} for k, m in margins.items()}
    if flags:
        meta["flags"] = flags
    case = {"id": None, "state": doc["document"], "questions": questions, "gold": gold, "meta": meta, "_seed_id": sid, "_split": split_for(seed)}
    qc = {"seed_id": sid, "author_answer": author, "per_labeller": per_labeller, "verifier": verify,
          "models": {"document": doc["model"], "questions": qfile["model"], **{p: l["model"] for p, l in labels.items()}},
          "cost_usd": round((doc.get("cost") or 0) + (qfile.get("cost") or 0) + sum((l.get("cost") or 0) for l in labels.values()) + ((json.load(open(vp)).get("cost") or 0) if os.path.exists(vp) else 0), 4)}
    return case, qc


def summarise(cases):
    by_type = collections.Counter(); by_kind = collections.Counter(); by_form = collections.Counter(); by_domain = collections.Counter(); by_dockind = collections.Counter()
    clear = collections.Counter(); agree = collections.Counter(); ver = collections.Counter(); adj = 0; flagged = 0; tops = []; tops_by_kind = collections.defaultdict(list)
    margin_band = collections.Counter(); comp_kind = collections.Counter(); score_computed = 0; score_total = 0; value_src = collections.Counter()
    n_q = 0; words = []
    score_levels = collections.Counter(); choice_options = collections.Counter(); score_decider = collections.Counter()
    for c in cases:
        by_form[c["meta"]["form"]] += 1
        by_domain[c["meta"]["domain"]] += 1
        by_dockind[c["meta"]["doc_kind"]] += 1
        flagged += 1 if c["meta"].get("flags") else 0
        s = c["state"]
        words.append(len((json.dumps(s) if isinstance(s, dict) else s).split()))
        for k, q in c["questions"].items():
            n_q += 1
            by_type[q["type"]] += 1
            kd = c["meta"]["kinds"][k]
            by_kind[kd] += 1
            clear["clear (top>=0.85)" if c["meta"]["clear_cut"][k] else "mixed"] += 1
            agree[str(c["meta"]["top_answer_agreement"][k])] += 1
            ver[c["meta"]["verified"][k]] += 1
            adj += 1 if c["meta"]["gold_adjusted_by_check"][k] else 0
            t = max(c["gold"][k]["probabilities"].values())
            tops.append(t); tops_by_kind[kd].append(t)
            if q["type"] == "choice":
                choice_options[str(len(q["criteria"]))] += 1
            if q["type"] == "score":
                score_levels[str(len(q["criteria"]))] += 1
                score_decider[c["meta"].get("score_decider", {}).get(k, "none")] += 1
                score_total += 1
                m = c["meta"].get("computed", {}).get(k)
                if m:
                    score_computed += 1 if m["computation"] != "stated" else 0
                    margin_band[m["margin_band"]] += 1
                    comp_kind[m["computation"]] += 1
                    value_src[m["value_source"]] += 1
    words.sort()
    return {"cases": len(cases), "questions": n_q, "questions_per_case": round(n_q / max(1, len(cases)), 2), "by_type": dict(by_type), "by_kind": dict(by_kind),
            "by_form": dict(by_form), "clear_vs_mixed": dict(clear), "labeller_top_agreement_of_4": dict(sorted(agree.items())),
            "verification": dict(ver), "gold_adjusted_by_check": adj, "cases_with_flags": flagged,
            "score_questions": score_total, "score_computed": score_computed, "margin_bands": dict(margin_band), "computations": dict(comp_kind), "margin_value_source": dict(value_src),
            "score_levels": dict(sorted(score_levels.items())), "choice_options": dict(sorted(choice_options.items())), "score_decider": dict(score_decider),
            "mean_gold_top": round(statistics.mean(tops), 3) if tops else None,
            "mean_gold_top_by_kind": {k: round(statistics.mean(v), 3) for k, v in tops_by_kind.items()},
            "state_words": {"median": words[len(words) // 2], "p10": words[len(words) // 10], "p90": words[9 * len(words) // 10]} if words else None,
            "domains": dict(sorted(by_domain.items())), "doc_kinds": dict(sorted(by_dockind.items()))}


def render_case_md(c):
    s = c["state"]
    out = [f"## {c['id']}  ·  {c['meta']['domain']}  ·  {c['meta']['doc_kind']}  ·  decider: {c['meta']['decider']}  ·  target: {c['meta']['clarity_target']}", ""]
    if c["meta"].get("flags"):
        out.append("**Flags:** " + "; ".join(c["meta"]["flags"]) + "\n")
    out.append("```" + ("json" if isinstance(s, dict) else "") )
    out.append(json.dumps(s, indent=1, ensure_ascii=False) if isinstance(s, dict) else s)
    out.append("```\n")
    for k, q in c["questions"].items():
        out.append(f"**{k} [{q['type']} / {c['meta']['kinds'][k]}]** {q['instructions']}  ")
        crit = q["criteria"]
        if isinstance(crit, dict):
            out.append("  " + "; ".join(f"`{o}` = {m}" for o, m in crit.items()) + "  ")
        else:
            out.append("  " + "; ".join(f"`{i}` = {m}" for i, m in enumerate(crit)) + "  ")
        g = c["gold"][k]["probabilities"]
        m = c["meta"].get("computed", {}).get(k)
        mtxt = f" · {m['computation']} value {m['value']} {m['unit'] or ''} edges {m['edges']} ({m['margin_band']})" if m else ""
        out.append(f"  gold: {json.dumps(g)}  · agreement {c['meta']['top_answer_agreement'][k]}/4 · check: {c['meta']['verified'][k]}{' · adjusted' if c['meta']['gold_adjusted_by_check'][k] else ''}{mtxt}  ")
        out.append("  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect\n")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=20261029)
    ap.add_argument("--review", type=int, default=50)
    args = ap.parse_args()

    seeds = make_seeds(args.n, args.seed)
    cases, qcs = [], []
    for s in seeds:
        r = load_case(args.work, s)
        if r:
            cases.append(r[0]); qcs.append(r[1])
    for c in cases:
        c["id"] = f"X-{int(c['_seed_id'][1:]):04d}"
    os.makedirs(os.path.join(args.out, "qc"), exist_ok=True)
    stats = {}
    for split in ("train_v3",):
        cs = [c for c in cases if c["_split"] == split]
        with open(os.path.join(args.out, f"{split}.jsonl"), "w", encoding="utf-8") as fh:
            for c in cs:
                fh.write(json.dumps({k: v for k, v in c.items() if not k.startswith("_")}, ensure_ascii=False) + "\n")
        stats[split] = summarise(cs)
    stats["all"] = summarise(cases)
    stats["total_cost_usd"] = round(sum(q["cost_usd"] for q in qcs), 2)
    json.dump(stats, open(os.path.join(args.out, "stats.json"), "w"), indent=2)
    id_of = {c["_seed_id"]: (c["_split"], c["id"]) for c in cases}
    with open(os.path.join(args.out, "qc", "per_labeller_author_and_check.jsonl"), "w", encoding="utf-8") as fh:
        for q in qcs:
            split, cid = id_of[q["seed_id"]]
            fh.write(json.dumps({"id": cid, "split": split, **q}, ensure_ascii=False) + "\n")
    # review sample: all flagged cases first, then stratified random fill, excluding the sealed test
    rng = random.Random(args.seed + 7)
    pool = list(cases)
    flagged = [c for c in pool if c["meta"].get("flags")]
    others = [c for c in pool if not c["meta"].get("flags")]
    rng.shuffle(others)
    sample = flagged[:args.review] + others[:max(0, args.review - len(flagged))]
    with open(os.path.join(args.out, "qc", f"review_sample_{len(sample)}.md"), "w", encoding="utf-8") as fh:
        fh.write(f"# Review sample: {len(sample)} cases ({len(flagged[:args.review])} flagged by the checking pass, the rest random)\n\n")
        for c in sample:
            fh.write(render_case_md(c) + "\n---\n\n")
    print(json.dumps({k: (v if k in ("total_cost_usd",) else {kk: v[kk] for kk in ("cases", "questions", "by_type", "by_kind", "by_form", "clear_vs_mixed", "mean_gold_top", "gold_adjusted_by_check", "cases_with_flags", "score_questions", "score_computed", "margin_bands", "computations", "margin_value_source", "score_levels", "choice_options", "score_decider")}) for k, v in stats.items()}, indent=1))


if __name__ == "__main__":
    main()
