"""Offline stand-in for llm.call (SIGNPOST_FAKE=1): schema-valid random outputs, for testing the pipeline without a key."""
from __future__ import annotations

import json
import random
import re

import design


def fake_call(model, system, user, schema, tag):
    rng = random.Random(tag)
    if tag == "scales":
        return _ok({"scales": [{"name": f"shared scale {i}", "instructions": "How much attention does this record need today?",
                                "levels": ["very little attention needed at all", "some attention needed this week", "prompt attention needed today", "immediate attention needed right now"]} for i in range(3)]})
    if tag.startswith("family"):
        fid = tag.split()[1]
        slot = next(s for s in design.SLOTS + design.SLOTS_B if s["id"] == fid)
        shared = {"name": "x"} if slot["shared"] is not None else None
        qs = []
        for k, p in enumerate(design.question_plan(slot, shared)):
            if p.get("shared"):
                continue
            q = {"name": f"q{k} item", "type": p["type"], "instructions": "", "true_desc": "", "false_desc": "", "options": [], "levels": []}
            if p["type"] == "noul":
                q["instructions"] = "The record shows the sample was kept cold throughout."
                if not p["bare"]:
                    q["true_desc"], q["false_desc"] = "the record supports the claim", "the record does not support it"
            elif p["type"] == "choice":
                q["instructions"] = "What should the reviewer do with this record next?"
                q["options"] = [{"name": f"option {c}", "description": f"the reviewer takes course of action number {c}"} for c in "abcde"[:p["options"]]]
            else:
                q["instructions"] = "How serious is the issue shown in this record?"
                q["levels"] = [("Level%d: " % i if p["named"] else "") + f"the issue is of grade {i} seriousness" for i in range(p["levels"])]
            qs.append(q)
        facs = [{"name": f"f{i}", "description": "a factor", "kind": ["categorical", "integer", "number", "boolean"][i % 4], "values": ["a", "b", "c"],
                 "weights": [1, 1, 1], "min": 0, "max": 10, "p_true": 0.5, "skills": ["S1"]} for i in range(10)]
        return _ok({"role": "a reviewer", "setting": "a setting", "questions": qs, "factors": facs,
                    "sections": [{"name": n, "description": "d"} for n in ("header", "detail", "history", "notes")], "rendering_notes": "notes", "skills": ["S1"]})
    if tag.startswith("record") or tag.startswith("rework"):
        st = {"header": {"ref": tag, "date": "2026-10-01"}, "detail": {"qty": rng.randint(1, 9), "unit": "box"},
              "history": [{"n": rng.randint(0, 5)}], "notes": {"text": "word " * rng.randint(2, 15)}}
        return _ok({"record_json": json.dumps(st), "factors": [{"name": "f0", "value": "b"}]})
    if tag.startswith("judge"):
        out = {}
        for name, sub in schema["properties"].items():
            os_ = list(sub["properties"])
            w = [rng.random() ** 3 for _ in os_]
            out[name] = {o: x / sum(w) for o, x in zip(os_, w)}
        return _ok(out)
    raise ValueError(tag)


def _ok(d):
    return {"ok": True, "data": d, "cost": 0.0, "model": "fake", "usage": {}}
