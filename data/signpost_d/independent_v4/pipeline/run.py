#!/usr/bin/env python3
"""Two-step generation plus multi-call labelling, run through the Claude CLI in headless mode.

Stages (all resumable; each item is skipped if its output file exists):
  docs       seed -> raw document (model: haiku)
  questions  document -> typed questions (model: sonnet)
  labels     document + questions -> probabilities, one call per persona (3 x haiku, 1 x opus)
  verify     document + read/compare/infer questions -> checking pass (opus)

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
from prompts import doc_messages, q_messages, label_messages, verify_messages, PERSONAS  # noqa: E402
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
    if os.path.exists(out):
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
    qs = {}
    for i, q in enumerate(raw, start=1):
        key = f"q{i}"
        t = q["type"]
        instr = q["instructions"].strip()
        if t == "noul":
            if not q.get("true_desc") or not q.get("false_desc"):
                return None
            low = instr.lower()
            if low.endswith("?") or low.startswith(("judge", "decide", "is ", "does ", "do ", "did ", "compare", "determine", "assess", "state whether", "whether", "can ", "should ", "has ", "have ", "was ", "were ", "are ", "will ")):
                return None
            crit = {"true": q["true_desc"].strip(), "false": q["false_desc"].strip()}
        elif t == "choice":
            if not instr.endswith("?"):
                return None
            opts = q.get("choice_options") or []
            labels = []
            crit = {}
            for o in opts:
                lab = o["label"].strip().lower().replace(" ", "_").replace("-", "_")
                lab = "".join(ch for ch in lab if ch.isalnum() or ch == "_")
                if not lab or lab in crit:
                    return None
                crit[lab] = o["meaning"].strip()
                labels.append(lab)
            if not (2 <= len(crit) <= 6):
                return None
        else:
            lv = [s.strip() for s in (q.get("score_levels") or []) if s.strip()]
            if not (3 <= len(lv) <= 5) or any(":" not in s for s in lv):
                return None
            crit = lv
            comp = q.get("computation") or "none"
            edges = q.get("edges") or []
            if comp not in ("none", "rule"):
                if len(edges) != len(lv) - 1 or any(edges[i] >= edges[i + 1] for i in range(len(edges) - 1)):
                    return None
                if q.get("computed_value") is None:
                    return None
        extra = {}
        if t == "score":
            extra = {"computation": q.get("computation") or "none", "computed_value": q.get("computed_value"), "unit": q.get("unit"),
                     "edges": q.get("edges") or [], "edge_rule": q.get("edge_rule") or "lower_inclusive"}
        qs[key] = {"type": t, "instructions": instr, "criteria": crit, "kind": q["kind"], "author_answer": q.get("author_answer", ""), **extra}
    n = len(qs)
    kinds = [q["kind"] for q in qs.values()]
    types = [q["type"] for q in qs.values()]
    if seed is not None:
        if types.count("score") != seed["n_score"] or types.count("noul") != seed["n_noul"] or types.count("choice") != seed["n_choice"]:
            return None
        n_computed = sum(1 for q in qs.values() if q["type"] == "score" and q.get("computation") not in ("none", "stated", "rule", None))
        planned_computed = sum(1 for sp in seed["score_plan"] if sp["decider"] not in ("stated", "rule"))
        if n_computed < planned_computed:
            return None
        # R19: the planned numbers of score levels and choice options
        levels = sorted(len(q["criteria"]) for q in qs.values() if q["type"] == "score")
        options = sorted(len(q["criteria"]) for q in qs.values() if q["type"] == "choice")
        if levels != sorted(sp["levels"] for sp in seed["score_plan"]) or options != sorted(c["options"] for c in seed["choice_plan"]):
            return None
    if kinds.count("compare") < max(1, round(0.3 * n)) or kinds.count("judge") > 2:
        return None
    if document is not None:
        descs, allowed = [], []
        for q in qs.values():
            c = q["criteria"]
            descs.extend(list(c.values()) if isinstance(c, dict) else list(c))
            allowed.extend(q.get("edges") or [])
        if leaks_figures(descs, document, allowed):
            return None
    return qs


def do_questions(work: str, seed: dict) -> str:
    sid = seed["seed_id"]
    src = path(work, "docs", sid)
    out = path(work, "questions", sid)
    if os.path.exists(out):
        return "skip"
    if not os.path.exists(src):
        return f"nodoc {sid}"
    document = json.load(open(src))["document"]
    system, user, schema = q_messages(seed, document)
    for attempt in range(3):
        r = claude_call("sonnet", system, user, schema)
        if not r["ok"]:
            continue
        qs = normalise_questions(r["data"]["questions"], document, seed)
        if qs:
            json.dump({"questions": qs, "cost": r["cost"], "model": r["model"]}, open(out, "w"), ensure_ascii=False, indent=1)
            return "ok"
    return f"fail {sid}: questions invalid"


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
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--stage", choices=["docs", "questions", "labels", "verify"], required=True)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--seed", type=int, default=20261029)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--limit-seconds", type=int, default=540, help="stop launching new jobs after this many seconds")
    args = ap.parse_args()

    seeds = make_seeds(args.n, args.seed)[args.start:]
    jobs = []
    if args.stage == "docs":
        jobs = [(do_doc, (args.work, s)) for s in seeds]
    elif args.stage == "questions":
        jobs = [(do_questions, (args.work, s)) for s in seeds]
    elif args.stage == "verify":
        jobs = [(do_verify, (args.work, s)) for s in seeds]
    else:
        for s in seeds:
            for persona in PERSONAS:
                jobs.append((do_label, (args.work, s, persona)))

    t0 = time.time()
    counts = {}
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = []
        for fn, a in jobs:
            if time.time() - t0 > args.limit_seconds:
                break
            futs.append(ex.submit(fn, *a))
            # gentle pacing so we don't flood the CLI
            time.sleep(0.05)
        for f in cf.as_completed(futs):
            res = f.result()
            tag = res.split(" ")[0]
            counts[tag] = counts.get(tag, 0) + 1
            if tag not in ("ok", "skip"):
                print(res, flush=True)
    print(json.dumps({"stage": args.stage, "elapsed_s": round(time.time() - t0), "counts": counts}), flush=True)


if __name__ == "__main__":
    main()
