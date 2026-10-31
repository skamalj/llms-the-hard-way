"""v7 (R26) stage 1: the cross-family shared scales and the family specifications (R22.2), with code checks for R22.5.

Opus designs each family from a slot: a domain idea, the skills the factors must exercise, the question-type mix,
option and level counts, which noul question has bare yes/no criteria, and whether one score question is a shared scale.
"""
from __future__ import annotations

import os
import re

SKILLS = {
    "S1": "reconciling the sections of a record: corresponding values in different sections (amount, quantity, date, unit, identifier, condition, or a term in text against listed items) must be compared; mismatches range from trivial to large, sit in varied places, are common but never announced, and some records have none",
    "S2": "absent or incomplete records: a required section missing or null, a step not yet done, or a date that shows something happened out of order; absence is evidence",
    "S3": "mitigating evidence: alarming signals often come with fields that lower concern (benign explanation, approved exception, active maintenance window, trusted source, low-impact target, recent successful check); the same alarming signal appears with and without mitigation about equally, and one alarming signal alone never settles a question that asks for more",
    "S4": "middle and partial outcomes: middle levels and middle-ground options (partial, hold, moderate) are common right answers; work done but unfinished is partial, a record needing one confirmation is hold",
    "S5": "statements as hypotheses: each true/false statement is a claim that holds only when the evidence supports it; a merely possible claim is false or contested",
    "S6": "contested judgment: some records leave sensible judges split between two defensible answers (signals in balance, a value on a boundary the scale leaves open)",
    "S7": "generic judgment questions: what to do next, how much attention, how serious, which category; the same question across very different records",
}

# 8 pilot families: 4 x (1 noul, 2 choice, 2 score) + 4 x (2 noul, 1 choice, 2 score) = 12 / 12 / 16 questions (30/30/40%)
SLOTS = [
    {"id": "F001", "domain": "clinical laboratory sample receipt", "skills": ["S1", "S2", "S3"], "types": [1, 2, 2], "choice_options": [4, 5], "score_levels": [4, 4], "null_noul": [0], "shared": None, "named_levels": [True, False]},
    {"id": "F002", "domain": "building maintenance work orders", "skills": ["S1", "S3"], "types": [1, 2, 2], "choice_options": [4, 4], "score_levels": [4, 4], "null_noul": [], "shared": 0, "named_levels": [False, False]},
    {"id": "F003", "domain": "municipal street-works permit applications", "skills": ["S2", "S3"], "types": [1, 2, 2], "choice_options": [5, 4], "score_levels": [4, 5], "null_noul": [0], "shared": None, "named_levels": [True, False]},
    {"id": "F004", "domain": "staff rosters checked against timesheets", "skills": ["S1", "S3"], "types": [1, 2, 2], "choice_options": [4, 4], "score_levels": [4, 4], "null_noul": [], "shared": None, "named_levels": [False, True]},
    {"id": "F005", "domain": "refrigerated food deliveries to schools (temperature and timing)", "skills": ["S1", "S2"], "types": [2, 1, 2], "choice_options": [4], "score_levels": [4, 4], "null_noul": [1], "shared": 1, "named_levels": [True, False]},
    {"id": "F006", "domain": "automatic weather-station data quality review", "skills": ["S1", "S3"], "types": [2, 1, 2], "choice_options": [5], "score_levels": [4, 5], "null_noul": [0], "shared": None, "named_levels": [False, True]},
    {"id": "F007", "domain": "home-care visit logs reviewed by a care coordinator", "skills": ["S2", "S3"], "types": [2, 1, 2], "choice_options": [4], "score_levels": [4, 4], "null_noul": [], "shared": 0, "named_levels": [False, False]},
    {"id": "F008", "domain": "moderation of school exam marking", "skills": ["S1", "S3"], "types": [2, 1, 2], "choice_options": [5], "score_levels": [4, 4], "null_noul": [], "shared": None, "named_levels": [True, False]},
]
ALWAYS_SKILLS = ["S4", "S5", "S6", "S7"]

# R24 pilot 2 (SIGNPOST_PROFILE=v3b): eight fresh families in new domains, same type, option and level structure as pilot 1
SLOTS_B = [
    {"id": "F101", "domain": "hospital blood bank stock and issue checks", "skills": ["S1", "S2", "S3"], "types": [1, 2, 2], "choice_options": [4, 5], "score_levels": [4, 4], "null_noul": [0], "shared": None, "named_levels": [True, False]},
    {"id": "F102", "domain": "passenger lift service visit logs", "skills": ["S1", "S3"], "types": [1, 2, 2], "choice_options": [4, 4], "score_levels": [4, 4], "null_noul": [], "shared": 0, "named_levels": [False, False]},
    {"id": "F103", "domain": "drinking-water quality sampling at treatment works", "skills": ["S2", "S3"], "types": [1, 2, 2], "choice_options": [5, 4], "score_levels": [4, 5], "null_noul": [0], "shared": None, "named_levels": [True, False]},
    {"id": "F104", "domain": "primary school admission applications", "skills": ["S1", "S3"], "types": [1, 2, 2], "choice_options": [4, 4], "score_levels": [4, 4], "null_noul": [], "shared": None, "named_levels": [False, True]},
    {"id": "F105", "domain": "hotel housekeeping room turnovers", "skills": ["S1", "S2"], "types": [2, 1, 2], "choice_options": [4], "score_levels": [4, 4], "null_noul": [1], "shared": 1, "named_levels": [True, False]},
    {"id": "F106", "domain": "warehouse cycle counts against the stock system", "skills": ["S1", "S3"], "types": [2, 1, 2], "choice_options": [5], "score_levels": [4, 5], "null_noul": [0], "shared": None, "named_levels": [False, True]},
    {"id": "F107", "domain": "laboratory instrument calibration records", "skills": ["S2", "S3"], "types": [2, 1, 2], "choice_options": [4], "score_levels": [4, 4], "null_noul": [], "shared": 0, "named_levels": [False, False]},
    {"id": "F108", "domain": "wildlife survey records submitted by field volunteers", "skills": ["S1", "S3"], "types": [2, 1, 2], "choice_options": [5], "score_levels": [4, 4], "null_noul": [], "shared": None, "named_levels": [True, False]},
]

# R26 train_v4: 40 fresh families (F201-F240) in new domains. Each copies the type, option, level, bare yes/no,
# shared-scale and skill structure of one pilot-2 slot (cycling F101-F108), so the set keeps pilot 2's mix.
DOMAINS_C = ['veterinary practice controlled-drug registers', 'railway track patrol inspection reports', 'inter-library loan requests between public libraries', 'community pharmacy prescription accuracy checks', 'airport ground-handling aircraft turnaround logs', 'concrete pour records on construction sites', 'museum object loan condition reports', 'university thesis submission checks', 'fire extinguisher service records in office buildings', 'milk collection tanker tests at dairy farms', 'ambulance daily vehicle readiness checks', 'court hearing bundle readiness checks', 'public swimming pool water testing logs', 'highway bridge structural inspection records', 'grain store temperature and moisture monitoring', 'vaccination clinic cold-chain session logs', 'theatre stage rigging inspections', 'tree felling licence applications to a forestry authority', 'fishing vessel catch landing declarations', 'surgical instrument tray sterilisation records', 'bus fleet brake and tyre inspections', 'research ethics application screening', 'allotment plot tenancy inspections', 'dental radiograph quality audits', 'waste transfer notes at a recycling centre', 'scaffold handover inspections', 'apprenticeship progress reviews', 'shipping container weight verification at a port', 'vineyard harvest and pressing logs', 'care home medication rounds', 'film location permit applications to a council', 'observatory night observing logs', 'medical tent logs at a marathon', 'seed bank germination tests', 'river level gauge maintenance visits', 'bakery allergen changeover records', 'electrical installation test certificates', 'sports pitch condition inspections before matches', 'archive digitisation quality checks', 'solar farm inverter fault logs']
SLOTS_C = []
for _i, _dom in enumerate(DOMAINS_C):
    _t = dict(SLOTS_B[_i % 8])
    _t.update({"id": f"F{201 + _i}", "domain": _dom})
    SLOTS_C.append(_t)
SLOTS = SLOTS_C
PROFILE = "v4"

ANCHOR_RULES = """
ONE DIMENSION, ANCHORED (these rules decide whether the family is usable)
- Every score question rates exactly ONE quantity. Never blend two criteria (for example severity and certainty, or size and number of problems) in one scale.
- Each level is a distinct, observable condition a reader can check in the record, such as a count, a size, a time or a state ("one discrepancy, under 5% of value"; "fault cleared, retest not yet logged"). It is not a feeling ("moderate concern").
- Neighbouring levels are separated by a checkable anchor: a threshold, a count, or the presence or absence of one thing. A record that meets a level's condition cannot also meet its neighbour's.
- Choice options differ along ONE clear axis (for example how much action, or which single cause). Each description says what makes that option apply. Two options must never both fit the same facts.
- A true/false statement is one specific, checkable claim.
"""

SCALES_USER_C = """Define three generic score scales that can be used, worded identically, by decision settings in very different domains (care, maintenance, sampling, admissions, stock, field surveys). Each rates exactly ONE quantity, for example how large a discrepancy is, or how many checks have failed. Each has a short snake_case name, an instruction that is a question of 5 to 14 words ending in "?", and exactly 4 levels from lowest to highest. Each level is a plain description of 4 to 10 words (no "Name:" prefix) stating a checkable condition, with neighbouring levels separated by a clear anchor (a time window, a count, a size). Word them freshly. Do not rate how soon action is due, how many required items remain open, or how long since details were last verified (those scales are already used elsewhere); choose three other generic quantities.

Return only the JSON."""

EXCLUDED = re.compile(r"\b(ai agent|agent run|automated job|support ticket|helpdesk|help desk|customer support|customer service|live chat|invoice|purchase order|accounts payable|goods[- ]received|vendor bill|security alert|intrusion|access anomal|phishing|malware)\b", re.I)

DESIGN_SYSTEM = """You design decision settings for a training set of structured records. Each setting (a "family") is one role in one domain making the same five decisions about many different records. Everything you write is invented and worded freshly by you: no real organisations or people, no wording copied from anywhere.

Never use these settings or anything close to them: monitoring or reviewing runs of AI agents or automated jobs; customer support conversations or tickets of any kind; vendor bills, invoices, purchase orders, accounts payable or goods-received matching; security alerts, intrusion or access-anomaly triage.

Write in British English. Be concrete and realistic: field names terse, the way a real system would name them."""

DESIGN_USER = """Design family {fid} for this domain: {domain}.

THE ROLE AND SETTING
Name one specific role that reviews one record at a time in this domain and must make decisions about it. Records are small JSON objects with 3 to 6 top-level sections (nested objects and lists; numbers as numbers, ISO dates, booleans, null for unknown values). {text_note}

THE FIVE QUESTIONS (the same for every record, decided by different signals each time)
Write exactly these questions, in this order:
{question_plan}
Rules for all questions:
- They are generic decisions a person in that role makes about every record: what to do with it (a disposition or next step), how serious, risky or time-sensitive it is, what outcome or category it represents, whether a specific hypothesis holds.
- Instructions are 5 to 14 words. Choice and score instructions are questions ending in "?". True/false (noul) instructions are statements, never questions: a claim about the record that holds only when the evidence supports it.
- Choice: option names 1 to 3 words (snake_case allowed); each description 5 to 12 words saying what the option means, not whether it applies. List options in a natural order (for example from least to most action), not by likelihood. Include middle-ground options such as hold, partial or proceed-with-conditions where natural.
- Score: levels from lowest to highest of the quantity named; each level text 4 to 10 words. Where asked for "Name: description" levels, write each level as a short name, a colon and a description; otherwise write plain descriptions without names.
- True/false with criteria: "true" and "false" descriptions of 3 to 12 words each. Where asked for bare yes/no, leave both descriptions empty.
- Each question has a short snake_case name (one to three words), unique within the family.

{anchor_rules}
LATENT FACTORS (8 to 14)
Define the hidden factors that vary between records and decide the answers. Each factor has a name, a description, and how it is sampled:
- "categorical" with values and weights, "integer" with min and max, "number" with min and max, or "boolean" with p_true.
The factors must exercise these skills:
{skills}
Make the deciding signals indirect: a value compared with its counterpart in another section, a flag, a missing section, a count in history. For mitigation, give the mitigating factor a probability near 0.5 so the same alarming signal appears with and without it about equally. Note for each factor which skills it serves.

SECTIONS AND RENDERING
List the 3 to 6 top-level sections of a record with a one-line description each, and write rendering notes: how each factor shows up in the record (which section and field, directly or indirectly), which fields carry decoys, and how a record must never state the answer to a question (no field like "risk: high" unless a real system would show it).

List the skills this family exercises (codes S1 to S7).

Return only the JSON."""

SCALES_SYSTEM = DESIGN_SYSTEM
SCALES_USER = """Define three generic score scales that can be used, worded identically, by decision settings in very different domains (care, maintenance, permits, deliveries, data quality, education). For example a scale of time pressure, or of how much attention a record needs. Each scale has a short snake_case name, an instruction that is a question of 5 to 14 words ending in "?", and exactly 4 levels from lowest to highest, each a plain description of 4 to 10 words (no "Name:" prefix). Word them freshly.

Return only the JSON."""

SCALES_SCHEMA = {"type": "object", "properties": {"scales": {"type": "array", "items": {
    "type": "object", "properties": {"name": {"type": "string"}, "instructions": {"type": "string"}, "levels": {"type": "array", "items": {"type": "string"}}},
    "required": ["name", "instructions", "levels"], "additionalProperties": False}}}, "required": ["scales"], "additionalProperties": False}

FAMILY_SCHEMA = {
    "type": "object",
    "properties": {
        "role": {"type": "string"}, "setting": {"type": "string"},
        "questions": {"type": "array", "items": {"type": "object", "properties": {
            "name": {"type": "string"}, "type": {"type": "string", "enum": ["noul", "choice", "score"]}, "instructions": {"type": "string"},
            "true_desc": {"type": "string"}, "false_desc": {"type": "string"},
            "options": {"type": "array", "items": {"type": "object", "properties": {"name": {"type": "string"}, "description": {"type": "string"}}, "required": ["name", "description"], "additionalProperties": False}},
            "levels": {"type": "array", "items": {"type": "string"}}},
            "required": ["name", "type", "instructions", "true_desc", "false_desc", "options", "levels"], "additionalProperties": False}},
        "factors": {"type": "array", "items": {"type": "object", "properties": {
            "name": {"type": "string"}, "description": {"type": "string"}, "kind": {"type": "string", "enum": ["categorical", "integer", "number", "boolean"]},
            "values": {"type": "array", "items": {"type": "string"}}, "weights": {"type": "array", "items": {"type": "number"}},
            "min": {"type": "number"}, "max": {"type": "number"}, "p_true": {"type": "number"}, "skills": {"type": "array", "items": {"type": "string"}}},
            "required": ["name", "description", "kind", "values", "weights", "min", "max", "p_true", "skills"], "additionalProperties": False}},
        "sections": {"type": "array", "items": {"type": "object", "properties": {"name": {"type": "string"}, "description": {"type": "string"}}, "required": ["name", "description"], "additionalProperties": False}},
        "rendering_notes": {"type": "string"},
        "skills": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["role", "setting", "questions", "factors", "sections", "rendering_notes", "skills"], "additionalProperties": False,
}


def question_plan(slot: dict, shared: dict | None) -> list:
    """The ordered list of question specifications the designer must write (the shared scale is inserted by code)."""
    plan = []
    n_noul, n_choice, n_score = slot["types"]
    for i in range(n_noul):
        plan.append({"type": "noul", "bare": i in slot["null_noul"]})
    for i in range(n_choice):
        plan.append({"type": "choice", "options": slot["choice_options"][i]})
    for i in range(n_score):
        if slot["shared"] == i and shared:
            plan.append({"type": "score", "shared": shared["name"]})
        else:
            plan.append({"type": "score", "levels": slot["score_levels"][i], "named": slot["named_levels"][i]})
    return plan


def plan_text(plan: list) -> str:
    lines = []
    k = 0
    for p in plan:
        if p.get("shared"):
            continue
        k += 1
        if p["type"] == "noul":
            lines.append(f"{k}. a true/false (noul) statement" + (" with bare yes/no criteria (empty descriptions)" if p["bare"] else " with short true and false descriptions"))
        elif p["type"] == "choice":
            lines.append(f"{k}. a choice question with exactly {p['options']} options")
        else:
            lines.append(f"{k}. a score question with exactly {p['levels']} levels" + (', each written as "Name: description"' if p["named"] else ", plain descriptions without names"))
    return "\n".join(lines)


def words(s: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+", s))


def snake(s: str) -> str:
    s = re.sub(r"[^a-z0-9_]+", "_", s.strip().lower()).strip("_")
    return re.sub(r"_+", "_", s)


def build_family(slot: dict, spec: dict, shared: dict | None) -> tuple[dict | None, str | None]:
    """Normalise a designer spec into the delivered question set and check R22.5. Returns (family, None) or (None, reason)."""
    plan = question_plan(slot, shared)
    written = [p for p in plan if not p.get("shared")]
    qs = spec["questions"]
    if len(qs) != len(written):
        return None, f"{len(qs)} questions written, {len(written)} asked"
    out, it = {}, iter(qs)
    for p in plan:
        if p.get("shared"):
            q = {"type": "score", "instructions": shared["instructions"], "criteria": list(shared["levels"])}
            out[shared["name"]] = q
            continue
        w = next(it)
        if w["type"] != p["type"]:
            return None, f"question {w['name']} is {w['type']}, asked {p['type']}"
        name = snake(w["name"])
        if not name or name in out or len(name.split("_")) > 3:
            return None, f"bad or repeated question name {w['name']!r}"
        instr = w["instructions"].strip()
        if not (5 <= words(instr) <= 14):
            return None, f"{name}: instruction has {words(instr)} words"
        if p["type"] == "noul":
            if instr.endswith("?"):
                return None, f"{name}: noul instruction is a question"
            if p["bare"]:
                crit = None
            else:
                t, f = w["true_desc"].strip(), w["false_desc"].strip()
                if not (3 <= words(t) <= 12 and 3 <= words(f) <= 12):
                    return None, f"{name}: true/false descriptions out of 3-12 words"
                crit = {"true": t, "false": f}
        elif p["type"] == "choice":
            if not instr.endswith("?"):
                return None, f"{name}: choice instruction does not end in ?"
            opts = w["options"]
            if len(opts) != p["options"]:
                return None, f"{name}: {len(opts)} options, asked {p['options']}"
            crit = {}
            for o in opts:
                on = snake(o["name"])
                if not on or on in crit or len(on.split("_")) > 3:
                    return None, f"{name}: bad option name {o['name']!r}"
                if not (5 <= words(o["description"]) <= 12):
                    return None, f"{name}: option {on} description has {words(o['description'])} words"
                crit[on] = o["description"].strip()
        else:
            if not instr.endswith("?"):
                return None, f"{name}: score instruction does not end in ?"
            lv = [x.strip() for x in w["levels"] if x.strip()]
            if len(lv) != p["levels"]:
                return None, f"{name}: {len(lv)} levels, asked {p['levels']}"
            for x in lv:
                body = x.split(":", 1)[1] if (p["named"] and ":" in x) else x
                if p["named"] and ":" not in x:
                    return None, f"{name}: level {x!r} lacks Name:"
                if not p["named"] and re.match(r"^\s*[A-Z][A-Za-z ]{0,20}:", x):
                    return None, f"{name}: plain level written with a name"
                if not (4 <= words(body) <= 10 + (2 if p["named"] else 0)):
                    return None, f"{name}: level text {x!r} out of 4-10 words"
            crit = lv
        out[name] = {"type": p["type"], "instructions": instr, "criteria": crit}
    facs = spec["factors"]
    if not (8 <= len(facs) <= 14):
        return None, f"{len(facs)} factors"
    for f in facs:
        if f["kind"] == "categorical" and (len(f["values"]) < 2 or len(f["weights"]) != len(f["values"]) or sum(f["weights"]) <= 0):
            return None, f"factor {f['name']}: bad categorical"
        if f["kind"] in ("integer", "number") and f["max"] < f["min"]:
            return None, f"factor {f['name']}: max < min"
    if not (3 <= len(spec["sections"]) <= 6):
        return None, f"{len(spec['sections'])} sections"
    text = " ".join([slot["domain"], spec["role"], spec["setting"]])
    if EXCLUDED.search(text):
        return None, f"excluded setting term: {EXCLUDED.search(text).group(0)}"
    skills = sorted(set(slot["skills"] + ALWAYS_SKILLS))
    fam = {"id": slot["id"], "domain": slot["domain"], "role": spec["role"], "setting": spec["setting"], "questions": out,
           "factors": facs, "sections": spec["sections"], "rendering_notes": spec["rendering_notes"], "skills": skills,
           "shared_scale": shared["name"] if (slot["shared"] is not None and shared) else None}
    return fam, None
