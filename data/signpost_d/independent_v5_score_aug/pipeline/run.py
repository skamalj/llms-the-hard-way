#!/usr/bin/env python3
"""Score-only augmentation (independent_v5_score_aug): two-step generation, multi-call labelling, the arithmetic
checking pass and a score-scale validation pass, run through the Claude CLI in headless mode (train_v2 runner).

Stages (all resumable; each item is skipped if its output file exists):
  docs       seed -> raw document (model: haiku)
  questions  document -> typed questions (model: sonnet)
  labels     document + questions -> probabilities, one call per persona (3 x haiku, 1 x opus)
  twins      F2 only: base document + the writer's one-fact change -> twin document (haiku); questions copied from the base
  verify     document + read/compare/infer questions -> checking pass (opus)
  validate   document + questions + gold -> score-scale validation, keep / reject per question (opus)

Usage:
  python run.py --work WORK --n 20 --stage docs --workers 6
  python run.py --work WORK --n 20 --stage questions
  python run.py --work WORK --n 20 --stage labels
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import random
import subprocess
import sys
import time
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seeds import make_seeds  # noqa: E402
from prompts import doc_messages, q_messages, label_messages, verify_messages, twin_messages, validate_messages, PERSONAS  # noqa: E402
from gold import gold_for  # noqa: E402
import re  # noqa: E402

DISALLOWED = "Bash,Read,Write,Edit,MultiEdit,Glob,Grep,LS,WebSearch,WebFetch,Agent,Task,NotebookEdit,TodoWrite"


def claude_call(model: str, system: str, user: str, schema: dict, max_budget: float = 0.8, timeout: int = 240,
                effort: str = "low") -> dict:
    env = dict(os.environ)
    env.pop("CLAUDE_CODE_SESSION_ID", None)
    cmd = ["claude", "-p", user, "--model", model, "--output-format", "json", "--system-prompt", system,
           "--json-schema", json.dumps(schema), "--no-session-persistence", "--strict-mcp-config",
           "--mcp-config", '{"mcpServers":{}}', "--session-id", str(uuid.uuid4()),
           "--tools", "", "--setting-sources", "", "--exclude-dynamic-system-prompt-sections",
           "--effort", effort, "--max-budget-usd", str(max_budget)]
    last_err = None
    for attempt in range(3):
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env, cwd="/tmp")
            out = p.stdout.strip()
            data = json.loads(out)
            if data.get("structured_output") is not None:
                return {"ok": True, "data": data["structured_output"], "cost": data.get("total_cost_usd"), "model": model}
            # some versions put the JSON in result
            res = data.get("result", "")
            try:
                return {"ok": True, "data": json.loads(res), "cost": data.get("total_cost_usd"), "model": model}
            except Exception:
                last_err = f"no structured output: {res[:200]}"
        except subprocess.TimeoutExpired:
            last_err = "timeout"
        except Exception as e:  # noqa: BLE001
            last_err = f"{type(e).__name__}: {e} :: {p.stdout[:200] if 'p' in dir() else ''} {p.stderr[:200] if 'p' in dir() else ''}"
        time.sleep(2 + 3 * attempt)
    return {"ok": False, "error": last_err, "model": model}


def path(work: str, stage: str, sid: str, suffix: str = "") -> str:
    d = os.path.join(work, stage)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"{sid}{suffix}.json")


# ----------------------------------------------------------------------------
# stage workers
# ----------------------------------------------------------------------------

def do_doc(work: str, seed: dict) -> str:
    out = path(work, "docs", seed["seed_id"])
    if os.path.exists(out) or seed.get("twin_of"):
        return "skip"
    system, user, schema = doc_messages(seed)
    r = claude_call("haiku", system, user, schema)
    if not r["ok"]:
        return f"fail {seed['seed_id']}: {r['error']}"
    doc = r["data"].get("record") if seed["form"] == "json" else r["data"].get("document")
    if doc is None or (isinstance(doc, str) and len(doc.split()) < 80) or (isinstance(doc, dict) and len(doc) < 6):
        return f"fail {seed['seed_id']}: thin document"
    json.dump({"seed": seed, "document": doc, "cost": r["cost"], "model": r["model"]}, open(out, "w"), ensure_ascii=False, indent=1)
    return "ok"


NUM_RE = re.compile(r"\d[\d,]*\.?\d*")


def leaks_figures(descs: list, document, allowed=()) -> bool:
    """True if any option description quotes a multi-digit figure that also appears in the document.

    Numbers in `allowed` (declared level edges) are permitted: a band edge may legitimately
    coincide with a limit the document states.
    """
    doc = json.dumps(document, ensure_ascii=False) if isinstance(document, dict) else document
    doc_nums = set(n.replace(",", "") for n in NUM_RE.findall(doc) if len(n.replace(",", "").replace(".", "")) >= 2)
    allowed_f = set()
    for a in allowed:
        try:
            allowed_f.add(round(float(a), 6))
        except (TypeError, ValueError):
            pass
    for d in descs:
        for n in NUM_RE.findall(d):
            n2 = n.replace(",", "")
            if len(n2.replace(".", "")) >= 2 and n2 in doc_nums:
                try:
                    if round(float(n2), 6) in allowed_f:
                        continue
                except ValueError:
                    pass
                return True
    return False


def normalise_questions(raw: list, document=None, seed=None) -> dict | None:
    return check_questions(raw, document, seed)[0]


def check_questions(raw: list, document=None, seed=None):
    """Returns (questions, None) or (None, reason). Score-only checks: four score questions, levels as planned, 'Name: description', consistent numeric edges,
    distinct instructions, no document figures quoted in level descriptions (declared edges excepted)."""
    if len(raw) != 4:
        return None, f"{len(raw)} questions"
    qs = {}
    for i, q in enumerate(raw, start=1):
        if q.get("type") != "score":
            return None, "non-score question"
        instr = q["instructions"].strip()
        lv = [x.strip() for x in (q.get("score_levels") or []) if x.strip()]
        if not (3 <= len(lv) <= 5) or any(":" not in x for x in lv):
            return None, "levels count or Name: description format"
        comp = q.get("computation") or "none"
        edges = q.get("edges") or []
        if comp != "none" and edges:
            if len(edges) != len(lv) - 1 or any(edges[j] >= edges[j + 1] for j in range(len(edges) - 1)):
                return None, "inconsistent edges"
        qs[f"q{i}"] = {"type": "score", "instructions": instr, "criteria": lv, "kind": q["kind"], "author_answer": q.get("author_answer", ""),
                       "computation": comp, "computed_value": q.get("computed_value"), "unit": q.get("unit"), "edges": edges,
                       "edge_rule": q.get("edge_rule") or "lower_inclusive"}
    if seed is not None and sorted(len(q["criteria"]) for q in qs.values()) != sorted(p["levels"] for p in seed["question_plan"]):
        return None, "level counts differ from the plan"
    if len({q["instructions"].lower() for q in qs.values()}) < 4:
        return None, "repeated instruction"
    if document is not None:
        descs, allowed = [], []
        for q in qs.values():
            descs.extend(q["criteria"])
            allowed.extend(q.get("edges") or [])
        if leaks_figures(descs, document, allowed):
            return None, "level description quotes a document figure"
    return qs, None


def do_questions(work: str, seed: dict) -> str:
    sid = seed["seed_id"]
    src = path(work, "docs", sid)
    out = path(work, "questions", sid)
    if os.path.exists(out) or seed.get("twin_of"):
        return "skip"
    if not os.path.exists(src):
        return f"nodoc {sid}"
    document = json.load(open(src))["document"]
    system, user, schema = q_messages(seed, document)
    reasons = []
    for attempt in range(3):
        r = claude_call("sonnet", system, user, schema)
        if not r["ok"]:
            reasons.append(f"call failed: {r.get('error')}")
            continue
        qs, why = check_questions(r["data"]["questions"], document, seed)
        if why:
            reasons.append(why)
        if qs:
            rec = {"questions": qs, "cost": r["cost"], "model": r["model"], "attempts": attempt + 1}
            if r["data"].get("twin_change"):
                rec["twin_change"] = r["data"]["twin_change"]
                rec["twin_question"] = r["data"].get("twin_question")
            json.dump(rec, open(out, "w"), ensure_ascii=False, indent=1)
            return "ok"
    json.dump({"seed_id": sid, "reason": "question set failed the script checks three times", "attempts": reasons}, open(path(work, "rejected_questions", sid), "w"))
    return f"fail {sid}: questions invalid ({'; '.join(reasons)})"


def do_twin(work: str, seed: dict) -> str:
    """F2: the twin gets the base document with one decisive fact changed (Haiku, the document writer) and the base's questions."""
    sid = seed["seed_id"]
    base = seed.get("twin_of")
    if not base:
        return "skip"
    dout, qout = path(work, "docs", sid), path(work, "questions", sid)
    if os.path.exists(dout) and os.path.exists(qout):
        return "skip"
    bd, bq = path(work, "docs", base), path(work, "questions", base)
    if not (os.path.exists(bd) and os.path.exists(bq)):
        return f"nobase {sid}"
    bdoc, bqs = json.load(open(bd)), json.load(open(bq))
    change = bqs.get("twin_change")
    if not change:
        return f"fail {sid}: base has no twin change"
    system, user, schema = twin_messages(bdoc["seed"], bdoc["document"], change)
    r = claude_call("haiku", system, user, schema)
    if not r["ok"]:
        return f"fail {sid}: {r['error']}"
    doc = r["data"].get("record") if isinstance(bdoc["document"], dict) else r["data"].get("document")
    if not doc or doc == bdoc["document"]:
        return f"fail {sid}: twin unchanged"
    tseed = dict(bdoc["seed"], seed_id=sid, twin_of=base)
    json.dump({"seed": tseed, "document": doc, "cost": r["cost"], "model": r["model"], "twin_of": base, "twin_change": change},
              open(dout, "w"), ensure_ascii=False, indent=1)
    json.dump({"questions": bqs["questions"], "cost": 0.0, "model": bqs["model"], "copied_from": base, "twin_question": bqs.get("twin_question")},
              open(qout, "w"), ensure_ascii=False, indent=1)
    return "ok"


def do_validate(work: str, seed: dict) -> str:
    sid = seed["seed_id"]
    out = path(work, "validate", sid)
    if os.path.exists(out):
        return "skip"
    dsrc, qsrc, vsrc = path(work, "docs", sid), path(work, "questions", sid), path(work, "verify", sid)
    labels = {}
    for p in PERSONAS:
        lp = path(work, "labels", sid, f".{p}")
        if os.path.exists(lp):
            labels[p] = json.load(open(lp))
    if not (os.path.exists(dsrc) and os.path.exists(qsrc) and os.path.exists(vsrc)) or len(labels) < len(PERSONAS):
        return f"noq {sid}"
    document = json.load(open(dsrc))["document"]
    questions = json.load(open(qsrc))["questions"]
    checks = json.load(open(vsrc))["checks"]
    gold = {k: gold_for(q, labels, checks.get(k), k)[1] for k, q in questions.items()}
    public_q = {k: {"instructions": v["instructions"], "criteria": v["criteria"]} for k, v in questions.items()}
    system, user, schema = validate_messages(document, public_q, gold)
    for attempt in range(2):
        r = claude_call("opus", system, user, schema, effort="high", max_budget=1.5, timeout=420)
        if not r["ok"]:
            continue
        res = {}
        for c in r["data"]["checks"]:
            k = c["key"].strip().strip("[]")
            if k in questions:
                res[k] = {"verdict": c["verdict"], "issue": c["issue"], "note": c["note"]}
        if set(res) == set(questions):
            json.dump({"checks": res, "model": r["model"], "cost": r["cost"]}, open(out, "w"), ensure_ascii=False, indent=1)
            return "ok"
    return f"fail {sid}: validate invalid"


def do_label(work: str, seed: dict, persona: str) -> str:
    sid = seed["seed_id"]
    out = path(work, "labels", sid, f".{persona}")
    if os.path.exists(out):
        return "skip"
    qsrc = path(work, "questions", sid)
    dsrc = path(work, "docs", sid)
    if not (os.path.exists(qsrc) and os.path.exists(dsrc)):
        return f"noq {sid}"
    document = json.load(open(dsrc))["document"]
    questions = json.load(open(qsrc))["questions"]
    public_q = {k: {"type": v["type"], "instructions": v["instructions"], "criteria": v["criteria"]} for k, v in questions.items()}
    rng = random.Random(f"{sid}:{persona}")
    model, system, user, schema, presented = label_messages(persona, document, public_q, rng)
    for attempt in range(2):
        r = claude_call(model, system, user, schema, effort="medium" if model == "sonnet" else "low")
        if not r["ok"]:
            continue
        probs = {}
        okflag = True
        for a in r["data"]["answers"]:
            k = a["key"].strip().strip("[]")
            if k not in presented:
                continue
            opts = presented[k]
            d = {o["option"].strip(): float(o["p"]) for o in a["probabilities"]}
            if not set(d) <= set(opts) or any(v < 0 for v in d.values()):
                okflag = False
                break
            for o in opts:  # options the labeller left out carry zero probability
                d.setdefault(o, 0.0)
            tot = sum(d.values())
            if tot <= 0:
                okflag = False
                break
            probs[k] = {o: d[o] / tot for o in opts}
        if okflag and set(probs) == set(presented):
            json.dump({"persona": persona, "model": model, "probabilities": probs, "presented_order": presented, "cost": r["cost"]},
                      open(out, "w"), ensure_ascii=False, indent=1)
            return "ok"
    return f"fail {sid}.{persona}: labels invalid"


def do_verify(work: str, seed: dict) -> str:
    sid = seed["seed_id"]
    out = path(work, "verify", sid)
    if os.path.exists(out):
        return "skip"
    qsrc = path(work, "questions", sid)
    dsrc = path(work, "docs", sid)
    if not (os.path.exists(qsrc) and os.path.exists(dsrc)):
        return f"noq {sid}"
    document = json.load(open(dsrc))["document"]
    questions = json.load(open(qsrc))["questions"]
    to_check = {k: {"type": v["type"], "instructions": v["instructions"], "criteria": v["criteria"]} for k, v in questions.items() if v["kind"] != "judge"}
    if not to_check:
        json.dump({"checks": {}, "model": "opus", "cost": 0.0}, open(out, "w"))
        return "ok"
    system, user, schema = verify_messages(document, to_check)
    for attempt in range(2):
        r = claude_call("opus", system, user, schema, effort="high", max_budget=1.5, timeout=420)
        if not r["ok"]:
            continue
        checks = {}
        for c in r["data"]["checks"]:
            k = c["key"].strip().strip("[]")
            if k not in to_check:
                continue
            q = to_check[k]
            opts = ["true", "false"] if q["type"] == "noul" else (list(q["criteria"].keys()) if q["type"] == "choice" else [str(i) for i in range(len(q["criteria"]))])
            ans = c["answer"].strip()
            if ans not in opts:
                continue
            checks[k] = {"settled": bool(c["settled"]), "answer": ans, "confidence": float(c["confidence"]),
                         "computed_value": c.get("computed_value"), "unit": c.get("unit")}
        if set(checks) == set(to_check):
            json.dump({"checks": checks, "model": r["model"], "cost": r["cost"]}, open(out, "w"), ensure_ascii=False, indent=1)
            return "ok"
    return f"fail {sid}: verify invalid"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--per-flow", type=int, required=True, help="seeds per flow (the first N of each flow's fixed list)")
    ap.add_argument("--flows", default="F1,F2,F3,F4,F5")
    ap.add_argument("--stage", choices=["docs", "questions", "twins", "labels", "verify", "validate"], required=True)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--seed", type=int, default=20261030)
    ap.add_argument("--limit-seconds", type=int, default=540, help="stop launching new jobs after this many seconds")
    args = ap.parse_args()

    flows = set(args.flows.split(","))
    seeds = [s for s in make_seeds(args.per_flow, args.seed) if s["flow"] in flows]
    fns = {"docs": do_doc, "questions": do_questions, "twins": do_twin, "verify": do_verify, "validate": do_validate}
    if args.stage == "labels":
        jobs = [(do_label, (args.work, s, persona)) for s in seeds for persona in PERSONAS]
    else:
        jobs = [(fns[args.stage], (args.work, s)) for s in seeds]

    t0 = time.time()
    counts = {}
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = []
        for fn, a in jobs:
            if time.time() - t0 > args.limit_seconds:
                break
            futs.append(ex.submit(fn, *a))
            time.sleep(0.05)
        for f in cf.as_completed(futs):
            res = f.result()
            tag = res.split(" ")[0]
            counts[tag] = counts.get(tag, 0) + 1
            if tag not in ("ok", "skip", "noq", "nodoc"):
                print(res, flush=True)
    print(json.dumps({"stage": args.stage, "elapsed_s": round(time.time() - t0), "counts": counts}), flush=True)


if __name__ == "__main__":
    main()
