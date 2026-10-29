#!/usr/bin/env python3
"""Mechanical checks on the delivered JSONL files (format and key rules only).

Usage: python validate.py shift_dev.jsonl sealed_test.jsonl train.jsonl
"""
from __future__ import annotations

import json
import sys


def check_case(c, errors):
    cid = c.get("id", "?")
    for f in ("id", "state", "questions", "gold", "meta"):
        if f not in c:
            errors.append(f"{cid}: missing field {f}")
            return
    if not isinstance(c["state"], (str, dict)):
        errors.append(f"{cid}: state must be text or a JSON object")
    qs, gold = c["questions"], c["gold"]
    if not (3 <= len(qs) <= 6):
        errors.append(f"{cid}: {len(qs)} questions (expected 3-6)")
    if set(qs) != set(gold):
        errors.append(f"{cid}: question keys and gold keys differ")
    for k, q in qs.items():
        t = q.get("type")
        instr = q.get("instructions", "")
        g = gold.get(k, {})
        if g.get("type") != t:
            errors.append(f"{cid} {k}: gold type mismatch")
        probs = g.get("probabilities", {})
        if t == "noul":
            crit = q.get("criteria", {})
            if set(crit) != {"true", "false"}:
                errors.append(f"{cid} {k}: noul criteria must be true/false")
            if instr.strip().endswith("?"):
                errors.append(f"{cid} {k}: noul instructions should be a statement, not a question")
            expected = ["true", "false"]
        elif t == "choice":
            crit = q.get("criteria", {})
            if not isinstance(crit, dict) or not (2 <= len(crit) <= 6):
                errors.append(f"{cid} {k}: choice needs 2-6 labelled options")
            expected = list(crit.keys()) if isinstance(crit, dict) else []
        elif t == "score":
            crit = q.get("criteria", [])
            if not isinstance(crit, list) or not (3 <= len(crit) <= 5):
                errors.append(f"{cid} {k}: score needs 3-5 levels")
            if any(":" not in lvl for lvl in crit):
                errors.append(f"{cid} {k}: score levels must be 'Name: description'")
            expected = [str(i) for i in range(len(crit))]
        else:
            errors.append(f"{cid} {k}: unknown type {t}")
            continue
        if list(probs.keys()) != expected:
            errors.append(f"{cid} {k}: gold keys {list(probs.keys())} do not match criteria order {expected}")
        tot = sum(probs.values())
        if abs(tot - 1.0) > 0.002:
            errors.append(f"{cid} {k}: probabilities sum to {tot:.4f}")
        if any(v < 0 for v in probs.values()):
            errors.append(f"{cid} {k}: negative probability")
        kind = c["meta"].get("kinds", {}).get(k)
        if kind not in ("read", "infer", "compare", "judge"):
            errors.append(f"{cid} {k}: kind {kind!r} not in read/infer/compare/judge")
    for f in ("domain", "form", "kinds"):
        if f not in c["meta"]:
            errors.append(f"{cid}: meta.{f} missing")


def main(paths):
    seen = set()
    total_err = 0
    for p in paths:
        errors = []
        n = 0
        for line in open(p, encoding="utf-8"):
            if not line.strip():
                continue
            n += 1
            c = json.loads(line)
            if c.get("id") in seen:
                errors.append(f"{c.get('id')}: duplicate id across files")
            seen.add(c.get("id"))
            check_case(c, errors)
        print(f"{p}: {n} cases, {len(errors)} errors")
        for e in errors[:30]:
            print("  ", e)
        total_err += len(errors)
    sys.exit(1 if total_err else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
