#!/usr/bin/env python3
"""Assemble the score-only augmentation from the work directory.

A case is accepted only when it has a document, four valid score questions, all four labelling calls, the
checking pass, and a "keep" from the score-scale validator on every one of its four questions. Accepted cases are
taken in seed order up to --cap per flow; the rest are reported as surplus. The gold rule is train_v2's (gold.py).

Usage: python assemble.py --work WORK --per-flow N --out OUT
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seeds import make_seeds, FLOWS  # noqa: E402
from prompts import PERSONAS  # noqa: E402
from gold import gold_for  # noqa: E402

OUT_NAME = "score_aug_v1"


def jload(p):
    return json.load(open(p)) if os.path.exists(p) else None


def margin_info(q, check):
    if q.get("computation") in (None, "none") or not q.get("edges"):
        return None
    v, src = None, "writer"
    if check and check.get("computed_value") is not None:
        v, src = float(check["computed_value"]), "check"
    elif q.get("computed_value") is not None:
        v = float(q["computed_value"])
    if v is None:
        return None
    edges = [float(e) for e in q["edges"]]
    nearest = min(edges, key=lambda e: abs(v - e))
    rel = abs(v - nearest) / abs(nearest) if nearest != 0 else abs(v - nearest)
    band = "close" if rel <= 0.05 else "moderate" if rel <= 0.25 else "far"
    return {"computation": q["computation"], "value": round(v, 4), "unit": q.get("unit"), "edges": edges, "edge_rule": q.get("edge_rule"),
            "margin": round(v / nearest, 4) if nearest != 0 else None, "margin_rel": round(rel, 4), "margin_band": band, "value_source": src}


def load_case(work, seed):
    """Returns (case, qc, None) when accepted, or (None, qc_or_None, reason) when rejected."""
    sid = seed["seed_id"]
    d = jload(os.path.join(work, "docs", f"{sid}.json"))
    qf = jload(os.path.join(work, "questions", f"{sid}.json"))
    if d is None:
        return None, None, "twin document not produced" if seed.get("twin_of") else "document not produced"
    if qf is None:
        return None, None, "question set failed the script checks three times" if not seed.get("twin_of") else "base question set missing"
    labels = {p: jload(os.path.join(work, "labels", f"{sid}.{p}.json")) for p in PERSONAS}
    labels = {p: l for p, l in labels.items() if l}
    vf = jload(os.path.join(work, "verify", f"{sid}.json"))
    va = jload(os.path.join(work, "validate", f"{sid}.json"))
    if len(labels) < len(PERSONAS) or vf is None or va is None:
        return None, None, "incomplete (labelling, check or validation call failed)"
    qs, checks, vchecks = qf["questions"], vf["checks"], va["checks"]
    seed = d["seed"]
    questions, gold, kinds, author, per_labeller, agreement, clear, verified, adjusted, flags, computed, margins = {}, {}, {}, {}, {}, {}, {}, {}, {}, [], {}, {}
    for k, q in qs.items():
        mean, g, ver, adj, overrode = gold_for(q, labels, checks.get(k), k)
        if overrode:
            flags.append(f"{k}: check ({checks[k]['answer']}) overrode a confident labeller mean")
        opts = [str(i) for i in range(len(q["criteria"]))]
        questions[k] = {"type": "score", "instructions": q["instructions"], "criteria": q["criteria"]}
        gold[k] = {"type": "score", "probabilities": g}
        kinds[k] = q["kind"]
        author[k] = q["author_answer"]
        per_labeller[k] = {p: {o: round(l["probabilities"][k][o], 3) for o in opts} for p, l in labels.items()}
        tops = [max(opts, key=lambda o: l["probabilities"][k][o]) for l in labels.values()]
        agreement[k] = max(collections.Counter(tops).values())
        clear[k] = max(g.values()) >= 0.85
        verified[k], adjusted[k] = ver, adj
        mi = margin_info(q, checks.get(k))
        if mi:
            computed[k] = {x: mi[x] for x in ("computation", "value", "unit", "edges", "edge_rule", "margin_rel", "margin_band", "value_source")}
            margins[k] = mi["margin"]
    qc = {"seed_id": sid, "flow": seed["flow"], "author_answer": author, "per_labeller": per_labeller, "verifier": checks, "validator": vchecks,
          "target_level": {f"q{i + 1}": p["target_level"] for i, p in enumerate(seed["question_plan"])},
          "question_attempts": qf.get("attempts"),
          "models": {"document": d["model"], "questions": qf["model"], **{p: l["model"] for p, l in labels.items()}, "check": vf.get("model"), "validator": va.get("model")},
          "cost_usd": round(sum((x or {}).get("cost") or 0 for x in [d, qf, vf, va, *labels.values()]), 4)}
    rejected = {k: v for k, v in vchecks.items() if v["verdict"] != "keep"}
    if rejected:
        return None, qc, "validator rejected " + ", ".join(f"{k} ({v['issue']})" for k, v in sorted(rejected.items()))
    meta = {"flow": seed["flow"], "flow_name": FLOWS[seed["flow"]]["name"], "domain": seed["domain"], "form": seed["form"], "kinds": kinds,
            "doc_kind": seed["doc_kind"], "decider": seed["decider"], "complications": seed["complications"],
            "source": "two-step model-written (document, then questions); score-only augmentation",
            "labellers": len(labels), "top_answer_agreement": agreement, "verified": verified, "gold_adjusted_by_check": adjusted, "clear_cut": clear,
            "validation": {k: {"verdict": v["verdict"], "issue": v["issue"]} for k, v in vchecks.items()}}
    if d.get("twin_of"):
        meta["twin_of"] = "SCORE-" + d["twin_of"]
        meta["twin_change"] = d["twin_change"]
        if qf.get("twin_question"):
            meta["twin_question"] = f"q{qf['twin_question']}"
    if computed:
        meta["margin"] = margins
        meta["computed"] = computed
    if flags:
        meta["flags"] = flags
    case = {"id": "SCORE-" + sid, "state": d["document"], "questions": questions, "gold": gold, "meta": meta}
    return case, qc, None


SHINGLE = re.compile(r"[a-z0-9]+")


def shingles(text, n=5):
    w = SHINGLE.findall(text.lower())
    return {" ".join(w[i:i + n]) for i in range(max(1, len(w) - n + 1))}


def jacc(a, b):
    return len(a & b) / max(1, len(a | b))


def duplicates(cases):
    sh = [shingles(json.dumps(c["state"], ensure_ascii=False) if isinstance(c["state"], dict) else c["state"]) for c in cases]
    pairs = {(c["id"], c["meta"].get("twin_of")) for c in cases if c["meta"].get("twin_of")}
    near_states, twin_sims = [], []
    for i in range(len(cases)):
        for j in range(i + 1, len(cases)):
            a, b = cases[i]["id"], cases[j]["id"]
            if (a, b) in pairs or (b, a) in pairs:
                twin_sims.append(jacc(sh[i], sh[j]))
                continue
            s = jacc(sh[i], sh[j])
            if s >= 0.5:
                near_states.append((a, b, round(s, 3)))
    instr = collections.Counter(q["instructions"].strip().lower() for c in cases if not c["meta"].get("twin_of") for q in c["questions"].values())
    qsh = [(c["id"], k, shingles(q["instructions"], 3)) for c in cases for k, q in c["questions"].items()]
    twin_ids = {x for p in pairs for x in p}
    near_q = 0
    for i in range(len(qsh)):
        for j in range(i + 1, len(qsh)):
            if qsh[i][0] == qsh[j][0] or (qsh[i][0] in twin_ids and qsh[j][0] in twin_ids):
                continue
            if jacc(qsh[i][2], qsh[j][2]) >= 0.8:
                near_q += 1
    return {"near_duplicate_state_pairs (5-gram Jaccard >= 0.5, twins excluded)": len(near_states), "near_duplicate_state_examples": near_states[:20],
            "exact_duplicate_instructions (twins excluded)": sum(v - 1 for v in instr.values() if v > 1),
            "near_duplicate_instruction_pairs (3-gram Jaccard >= 0.8, across cases, twins excluded)": near_q,
            "twin_pair_state_similarity_median": round(statistics.median(twin_sims), 3) if twin_sims else None}


def position(level, n):
    return "lowest" if level == 0 else "highest" if level == n - 1 else "middle"


def summarise(cases):
    n_q = 0
    by = collections.defaultdict(collections.Counter)
    tops, top_level, top_pos, words = [], collections.defaultdict(collections.Counter), collections.Counter(), []
    for c in cases:
        by["form"][c["meta"]["form"]] += 1
        by["doc_kind"][c["meta"]["doc_kind"]] += 1
        by["domain"][c["meta"]["domain"]] += 1
        s = c["state"]
        words.append(len((json.dumps(s) if isinstance(s, dict) else s).split()))
        for k, q in c["questions"].items():
            n_q += 1
            L = len(q["criteria"])
            g = c["gold"][k]["probabilities"]
            t = max(g.values()); tl = int(max(g, key=g.get))
            tops.append(t)
            by["scale_levels"][str(L)] += 1
            by["kind"][c["meta"]["kinds"][k]] += 1
            by["agreement_of_4"][str(c["meta"]["top_answer_agreement"][k])] += 1
            by["check"][c["meta"]["verified"][k]] += 1
            by["adjusted_by_check"]["yes" if c["meta"]["gold_adjusted_by_check"][k] else "no"] += 1
            top_level[str(L)][str(tl)] += 1
            top_pos[position(tl, L)] += 1
            if c["meta"].get("computed", {}).get(k):
                by["margin_band"][c["meta"]["computed"][k]["margin_band"]] += 1
                by["computation"][c["meta"]["computed"][k]["computation"]] += 1
    words.sort()
    bins = collections.Counter()
    for t in tops:
        bins["<0.55" if t < 0.55 else "0.55-0.70" if t < 0.70 else "0.70-0.85" if t < 0.85 else "0.85-0.95" if t < 0.95 else ">=0.95"] += 1
    return {"cases": len(cases), "score_questions": n_q,
            "scale_levels": dict(sorted(by["scale_levels"].items())),
            "gold_top_level_by_scale_size": {L: dict(sorted(v.items())) for L, v in sorted(top_level.items())},
            "gold_top_level_position": dict(top_pos),
            "gold_top_probability": {"mean": round(statistics.mean(tops), 3) if tops else None, "share_below_0.85": round(sum(t < 0.85 for t in tops) / max(1, len(tops)), 3),
                                     "bins": {b: bins[b] for b in ("<0.55", "0.55-0.70", "0.70-0.85", "0.85-0.95", ">=0.95")}},
            "labeller_top_agreement_of_4": dict(sorted(by["agreement_of_4"].items())),
            "form": dict(by["form"]), "kinds": dict(by["kind"]), "check": dict(by["check"]), "gold_adjusted_by_check": by["adjusted_by_check"]["yes"],
            "margin_bands": dict(by["margin_band"]), "computations": dict(by["computation"]),
            "state_words": {"median": words[len(words) // 2], "p10": words[len(words) // 10], "p90": words[9 * len(words) // 10]} if words else None,
            "doc_kinds": dict(sorted(by["doc_kind"].items())), "domains": len(by["domain"])}


def render_case_md(c):
    s = c["state"]
    twin = f"  ·  twin of {c['meta']['twin_of']}" if c["meta"].get("twin_of") else ""
    out = [f"## {c['id']}  ·  {c['meta']['flow']} {c['meta']['flow_name']}  ·  {c['meta']['domain']}  ·  {c['meta']['doc_kind']}{twin}", ""]
    if c["meta"].get("twin_change"):
        out.append(f"**Twin change:** {c['meta']['twin_change']}\n")
    out += ["```" + ("json" if isinstance(s, dict) else ""), json.dumps(s, indent=1, ensure_ascii=False) if isinstance(s, dict) else s, "```\n"]
    for k, q in c["questions"].items():
        out.append(f"**{k} [{c['meta']['kinds'][k]}]** {q['instructions']}  ")
        out.append("  " + "; ".join(f"`{i}` = {m}" for i, m in enumerate(q["criteria"])) + "  ")
        out.append(f"  gold: {json.dumps(c['gold'][k]['probabilities'])} · agreement {c['meta']['top_answer_agreement'][k]}/4 · check: {c['meta']['verified'][k]}  ")
        out.append("  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect\n")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--per-flow", type=int, required=True)
    ap.add_argument("--counts", default="", help="per-flow overrides, e.g. F3=200,F4=330")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cap", type=int, default=100)
    ap.add_argument("--seed", type=int, default=20261030)
    ap.add_argument("--review", type=int, default=50)
    args = ap.parse_args()

    counts_by_flow = {f: args.per_flow for f in FLOWS}
    counts_by_flow.update({k: int(v) for k, v in (x.split("=") for x in args.counts.split(",") if x)})
    seeds = [s for s in make_seeds(max(counts_by_flow.values()), args.seed) if int(s["seed_id"].split("-")[1]) <= counts_by_flow[s["flow"]]]
    accepted, qcs, report = [], [], {f: {"seeds": 0, "accepted": 0, "surplus": 0, "rejected": collections.Counter()} for f in FLOWS}
    validator_issues = {f: collections.Counter() for f in FLOWS}
    validated_q = collections.Counter()
    rejections = []
    for s in seeds:
        f = s["flow"]
        report[f]["seeds"] += 1
        case, qc, reason = load_case(args.work, s)
        if qc:
            for v in qc["validator"].values():
                validated_q[f] += 1
                if v["verdict"] != "keep":
                    validator_issues[f][v["issue"]] += 1
        if reason:
            report[f]["rejected"][reason.split(" q")[0] if reason.startswith("validator") else reason] += 1
            rejections.append({"seed_id": s["seed_id"], "flow": f, "reason": reason,
                               **({"validator": qc["validator"]} if qc and reason.startswith("validator") else {})})
            continue
        if report[f]["accepted"] >= args.cap:
            report[f]["surplus"] += 1
            continue
        report[f]["accepted"] += 1
        accepted.append(case); qcs.append(qc)
    # keep twin links only where both halves are in the set
    ids = {c["id"] for c in accepted}
    for c in accepted:
        if c["meta"].get("twin_of") and c["meta"]["twin_of"] not in ids:
            c["meta"]["twin_partner_missing"] = True

    os.makedirs(os.path.join(args.out, "qc"), exist_ok=True)
    with open(os.path.join(args.out, f"{OUT_NAME}.jsonl"), "w", encoding="utf-8") as fh:
        for c in accepted:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    with open(os.path.join(args.out, "qc", "per_labeller_author_check_validator.jsonl"), "w", encoding="utf-8") as fh:
        for q in qcs:
            fh.write(json.dumps({"id": "SCORE-" + q["seed_id"], **q}, ensure_ascii=False) + "\n")
    with open(os.path.join(args.out, "qc", "rejections.jsonl"), "w", encoding="utf-8") as fh:
        for r in rejections:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    stats = {"all": summarise(accepted), "by_flow": {}, "acceptance": {}, "duplicates": duplicates(accepted)}
    for f in FLOWS:
        cs = [c for c in accepted if c["meta"]["flow"] == f]
        stats["by_flow"][f] = summarise(cs)
        r = report[f]
        twins = sum(1 for c in cs if c["meta"].get("twin_of"))
        stats["acceptance"][f] = {"name": FLOWS[f]["name"], "seeds_run": r["seeds"], "accepted_cases": r["accepted"], "accepted_score_questions": 4 * r["accepted"],
                                  "surplus_beyond_cap": r["surplus"], "rejected_cases": sum(r["rejected"].values()), "rejection_reasons": dict(r["rejected"]),
                                  "validator_questions_checked": validated_q[f], "validator_rejected_questions_by_issue": dict(validator_issues[f]),
                                  "validator_question_reject_rate": round(sum(validator_issues[f].values()) / max(1, validated_q[f]), 3),
                                  **({"twin_cases": twins, "complete_twin_pairs": sum(1 for c in cs if c["meta"].get("twin_of") and not c["meta"].get("twin_partner_missing"))} if FLOWS[f].get("twins") else {})}
    stats["total_cost_usd_accepted_cases"] = round(sum(q["cost_usd"] for q in qcs), 2)
    json.dump(stats, open(os.path.join(args.out, "stats.json"), "w"), indent=2)

    manifest = {"name": "signpost_d score augmentation", "version": OUT_NAME, "directory": "data/signpost_d/independent_v5_score_aug",
                "file": f"{OUT_NAME}.jsonl", "brief": "signpost_d_score_augmentation_brief.md", "leaves_unchanged": "v1_7",
                "type": "score only", "id_pattern": "SCORE-F<flow>-<nnnn>", "base_seed": args.seed, "seeds_per_flow": counts_by_flow, "cap_per_flow": args.cap,
                "flows": {f: {"name": FLOWS[f]["name"], "accepted_cases": report[f]["accepted"], "accepted_score_questions": 4 * report[f]["accepted"]} for f in FLOWS},
                "generation": {"documents": "Haiku (claude-haiku-5-5)", "questions": "Sonnet (claude-sonnet-5-5)", "twin_documents_F2": "Haiku (claude-haiku-5-5)"},
                "labelling": {"calls_per_case": 4, "personas": {p: m for p, (m, _) in PERSONAS.items()}, "gold": "mean of the four calls; train_v2 checking-pass rule (gold.py)"},
                "validation": {"arithmetic_check": "Opus (claude-opus-5-5), read/compare/infer questions", "score_scale_validator": "Opus (claude-opus-5-5), every question, 10 checks of brief section 4; any reject drops the case",
                               "mechanical": "pipeline/validate.py"},
                "pipeline_base": "independent_v2/pipeline (train_v2), via independent_v4"}
    json.dump(manifest, open(os.path.join(args.out, "manifest.json"), "w"), indent=2)

    rng = random.Random(args.seed + 7)
    sample = []
    for f in FLOWS:
        cs = [c for c in accepted if c["meta"]["flow"] == f]
        rng.shuffle(cs)
        sample += cs[:args.review // len(FLOWS)]
    with open(os.path.join(args.out, "qc", f"review_sample_{len(sample)}.md"), "w", encoding="utf-8") as fh:
        fh.write(f"# Review sample: {len(sample)} cases ({args.review // len(FLOWS)} random per flow)\n\n")
        for c in sample:
            fh.write(render_case_md(c) + "\n---\n\n")
    print(json.dumps({"acceptance": stats["acceptance"], "all": {k: stats["all"][k] for k in ("cases", "score_questions", "scale_levels", "gold_top_level_position", "gold_top_probability", "form", "kinds")},
                      "duplicates": {k: v for k, v in stats["duplicates"].items() if k != "near_duplicate_state_examples"}, "cost": stats["total_cost_usd_accepted_cases"]}, indent=1))


if __name__ == "__main__":
    main()
