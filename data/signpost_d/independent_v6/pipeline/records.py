"""Stage 2 and 3: records and judgments.

Per record: code samples the latent factors and a plan per question (R22.4.2: a target clarity and an intended top
answer drawn so the batch can meet R22.4.3); Sonnet writes the record JSON from the factors and the plan; five
independent judges (different models and stances, separate calls, no shared context) each give a full probability
distribution for every question. The delivered gold is the plain mean of the five judgments, as measured.
"""
from __future__ import annotations

import json
import math
import random
import re

# Target share of questions by the gold's top probability (midpoints of the R22.4.3 ranges)
CLARITY = {
    "noul": {"balanced": 0.35, "leaning": 0.33, "clear": 0.32},
    "choice": {"contested": 0.20, "balanced": 0.44, "leaning": 0.22, "clear": 0.14},
    "score": {"contested": 0.23, "balanced": 0.51, "leaning": 0.20, "clear": 0.06},
}
CLARITY_TEXT = {
    "clear": "clear: the record settles it; sensible readers would all give the same answer with high confidence (about 0.9 or more)",
    "leaning": "leaning: the record points to one answer, but a reader could reasonably hold some doubt (top answer about 0.7 to 0.9)",
    "balanced": "balanced: the evidence favours one answer only modestly; a second answer remains quite plausible (top answer about 0.5 to 0.7)",
    "contested": "contested: two answers are both defensible and sensible readers would split between them (no answer above about 0.5)",
}
# Intended top-answer position (R22.4.3)
POSITION = {"score": {"lowest": 0.13, "middle": 0.62, "highest": 0.25}, "choice": {"first": 0.20, "middle": 0.65, "last": 0.15}}
NOUL_TRUE = 0.475


def options_of(q: dict) -> list:
    if q["type"] == "noul":
        return ["true", "false"]
    if q["type"] == "choice":
        return list(q["criteria"].keys())
    return [str(i) for i in range(len(q["criteria"]))]


def sample_factors(fam: dict, rng: random.Random) -> dict:
    out = {}
    for f in fam["factors"]:
        k = f["kind"]
        if k == "categorical":
            out[f["name"]] = rng.choices(f["values"], f["weights"])[0]
        elif k == "integer":
            out[f["name"]] = rng.randint(int(f["min"]), int(f["max"]))
        elif k == "number":
            out[f["name"]] = round(rng.uniform(f["min"], f["max"]), 2)
        else:
            out[f["name"]] = rng.random() < (f["p_true"] if 0 < f["p_true"] < 1 else 0.5)
    return out


def sample_plan(fam: dict, rng: random.Random) -> dict:
    plan = {}
    for name, q in fam["questions"].items():
        t = q["type"]
        cl = rng.choices(list(CLARITY[t]), list(CLARITY[t].values()))[0]
        opts = options_of(q)
        if t == "noul":
            target = "true" if rng.random() < NOUL_TRUE else "false"
        else:
            pos = rng.choices(list(POSITION[t]), list(POSITION[t].values()))[0]
            if pos in ("lowest", "first"):
                target = opts[0]
            elif pos in ("highest", "last"):
                target = opts[-1]
            else:
                target = rng.choice(opts[1:-1])
        second = None
        if cl in ("contested", "balanced"):
            i = opts.index(target)
            neigh = [opts[j] for j in (i - 1, i + 1) if 0 <= j < len(opts)] if t == "score" else [o for o in opts if o != target]
            second = rng.choice(neigh)
        plan[name] = {"clarity": cl, "target": target, "second": second}
    return plan


def target_words(rng: random.Random) -> int:
    # lognormal with median about 70, p10 about 35, p90 about 160 (R22.2.2), capped at 300
    return int(min(300, max(25, math.exp(rng.gauss(math.log(70), 0.6)))))


def record_words(state) -> int:
    return len(re.findall(r"[A-Za-z0-9]+", json.dumps(state, separators=(",", ":"), ensure_ascii=False)))


RENDER_SYSTEM = """You write one realistic record for a training set: a compact JSON object of the kind an operational system in the given domain would hold. You are given starting values for the hidden factors of the situation and a plan: how sensible reviewers should find each decision. Write the record so that a competent reviewer, reading only the record, would reach those judgments.

The plan comes first. The starting factor values are a draw; where they would push a decision away from its plan (for example several independent alarms in a record planned as a mild hold, or a decisive problem in a record planned as clean), change those factor values so the record can meet the plan, and keep the rest. Return the final factor values you actually used, one entry per factor, as plain strings.

Rules:
- Everything is invented. Field names are terse and realistic; numbers as numbers, ISO dates, booleans, null for unknown values; nested objects and lists where natural.
- The top-level keys are only the family's listed sections (a section may be left out, or null, when it is absent or not yet done); never add other top-level keys.
- The record never states an answer to any decision ("risk": "high", "action": "hold") unless a real system would show such a field. Deciding signals are indirect: a value against its counterpart in another section, a flag, a missing or null section, a count in history, a short note.
- Express every factor value faithfully in the record (directly or through the fields that imply it). Add a few realistic fields that decide nothing.
- For a statement planned true, the record must actually support it; for one planned false, the record must undermine it or leave it unsupported.
- Low and lowest levels, first options and "no problem" outcomes are often the plan: then the record is genuinely clean on that point.
- For a "clear" decision make the deciding signal unmistakable. For "leaning", give one answer the weight of evidence with a real reason for doubt. For "balanced" and "contested", put signals in genuine balance (an aggravating and a mitigating signal of similar weight, or a value near a boundary the question leaves open) so that the planned answers are both defensible. Never resolve a planned contest with a decisive extra field.
- Short free text, where the family uses it, is one or two sentences per field.
- Keep to the target length (count every key and value word): records are short. Leave out anything a reviewer does not need."""

RENDER_USER = """DOMAIN: {domain}
ROLE: {role}
SETTING: {setting}

SECTIONS
{sections}

RENDERING NOTES
{notes}

THE DECISIONS THE REVIEWER WILL MAKE (do not answer them in the record)
{questions}

HIDDEN FACTOR VALUES FOR THIS RECORD
{factors}

PLAN (how a sensible reviewer should find each decision from your record)
{plan}

TARGET LENGTH: about {words} words of compact JSON.

Return the record as a JSON string in "record_json", and the final factor values in "factors"."""

RENDER_SCHEMA = {"type": "object", "properties": {"record_json": {"type": "string"},
                 "factors": {"type": "array", "items": {"type": "object", "properties": {"name": {"type": "string"}, "value": {"type": "string"}}, "required": ["name", "value"], "additionalProperties": False}}},
                 "required": ["record_json", "factors"], "additionalProperties": False}


def final_factors(fam: dict, sampled: dict, returned: list) -> dict:
    """The factor values the record actually expresses: the writer's returned values, typed like the factor definitions."""
    kinds = {f["name"]: f["kind"] for f in fam["factors"]}
    out = dict(sampled)
    for x in returned:
        n, v = x["name"].strip(), x["value"].strip()
        if n not in kinds:
            continue
        k = kinds[n]
        try:
            if k == "integer":
                out[n] = int(float(v))
            elif k == "number":
                out[n] = float(v)
            elif k == "boolean":
                out[n] = v.lower() in ("true", "yes", "1")
            else:
                out[n] = v
        except ValueError:
            out[n] = v
    return out


def describe_questions(fam: dict) -> str:
    lines = []
    for name, q in fam["questions"].items():
        if q["type"] == "noul":
            c = q["criteria"]
            extra = f' (true = {c["true"]}; false = {c["false"]})' if c else " (yes / no)"
            lines.append(f'- {name} [true/false statement]: "{q["instructions"]}"{extra}')
        elif q["type"] == "choice":
            opts = "; ".join(f"{k} = {v}" for k, v in q["criteria"].items())
            lines.append(f'- {name} [choice]: {q["instructions"]} Options: {opts}')
        else:
            lv = "; ".join(f"{i} = {v}" for i, v in enumerate(q["criteria"]))
            lines.append(f'- {name} [score, lowest first]: {q["instructions"]} Levels: {lv}')
    return "\n".join(lines)


def describe_plan(fam: dict, plan: dict) -> str:
    lines = []
    for name, p in plan.items():
        q = fam["questions"][name]
        tgt = p["target"] if q["type"] != "score" else f"level {p['target']}"
        sec = (p["second"] if q["type"] != "score" else f"level {p['second']}") if p["second"] else None
        s = f"- {name}: {CLARITY_TEXT[p['clarity']]}. Leading answer: {tgt}" + (f"; the other defensible answer: {sec}" if sec else "") + "."
        lines.append(s)
    return "\n".join(lines)


def render_messages(fam: dict, factors: dict, plan: dict, n_words: int):
    sections = "\n".join(f"- {s['name']}: {s['description']}" for s in fam["sections"])
    facs = "\n".join(f"- {k} = {json.dumps(v)}" for k, v in factors.items())
    user = RENDER_USER.format(domain=fam["domain"], role=fam["role"], setting=fam["setting"], sections=sections, notes=fam["rendering_notes"],
                              questions=describe_questions(fam), factors=facs, plan=describe_plan(fam, plan), words=n_words)
    return RENDER_SYSTEM, user, RENDER_SCHEMA


def check_record(state, fam: dict | None = None, n_words: int | None = None) -> str | None:
    if not isinstance(state, dict):
        return "record is not a JSON object"
    if not (3 <= len(state) <= 6):
        return f"{len(state)} top-level sections (3 to 6 allowed)"
    if fam is not None:
        extra = set(state) - {s["name"] for s in fam["sections"]}
        if extra:
            return f"top-level keys not among the family sections: {sorted(extra)}"
    w = record_words(state)
    if w > 320:
        return f"{w} words (maximum 320)"
    if n_words is not None and w > max(2 * n_words, n_words + 60):
        return f"{w} words against a target of about {n_words}"
    return None


# ----------------------------------------------------------------------------- judges

JUDGE_BASE = """You read one record from an operational system and answer a fixed set of questions about it, as a competent person in the stated role who reads the record once, carefully. For every question give a probability for every option: how likely each option is to be the right answer, given only what the record shows.

How to judge:
- Weigh the signals, notice what is missing, compare values across sections, and apply any rule the record states. Signals that lower concern (a benign explanation, an approved exception, a recent successful check) count as much as signals that raise it.
- A true/false statement is a claim: put most probability on true only when the record supports it. A claim that is merely possible is not true.
- Be calibrated and decisive where the record allows. Read each probability as how often careful people in your role, reading this record, would land on that answer. Typical shapes:
  * the record settles it: 0.85 to 0.95 on one answer, the rest small;
  * one answer is clearly better but a reasonable person could see it differently: 0.65 to 0.8 on it, most of the rest on the nearest alternative;
  * two answers genuinely in balance: roughly 0.4 to 0.55 on each, little elsewhere.
- On an ordered scale, first decide which level's description fits best and commit to it. A neighbouring level gets only what real doubt about the fit justifies, not mass by default; do not spread probability across three or more levels unless the record truly leaves that open. The same holds for choice options: a plausible-sounding option the record does not point to gets little.
- Give a small probability (0.005 to 0.03) to options that are implausible but not impossible; zero only when the record makes an option impossible. For an ordered scale, most probability sits on one level and its neighbours.
- Use the option names exactly as given. Probabilities for each question sum to 1."""

PERSONAS = [
    {"id": "careful_operator", "model": "opus", "effort": "medium",
     "text": "You are an experienced practitioner in this role: thorough, practical, and used to acting on records like this every day."},
    {"id": "cautious_reviewer", "model": "sonnet", "effort": "medium",
     "text": "You are a cautious reviewer: you take discrepancies and gaps seriously and hesitate to clear a record that has an open point, but you do not invent problems."},
    {"id": "pragmatic_operator", "model": "sonnet", "effort": "medium",
     "text": "You are a pragmatic operator under time pressure: you look for what actually matters for the decision and give reasonable benefit of the doubt where a mitigating explanation is on the record."},
    {"id": "by_the_book", "model": "haiku", "effort": "medium",
     "text": "You are a by-the-book auditor: you apply the stated rules and thresholds literally and treat anything not on the record as unknown."},
    {"id": "generalist", "model": "haiku", "effort": "medium",
     "text": "You are a sensible generalist new to this team: you read the record plainly and judge as an informed outsider would."},
]

JUDGE_USER = """ROLE: {role} ({domain})

RECORD
{record}

QUESTIONS
{questions}

Return a probability for every option of every question."""

def judge_schema(fam: dict) -> dict:
    """One fixed key per question and per option, so every judgment is complete and uses the exact option names."""
    props = {}
    for name, q in fam["questions"].items():
        opts = options_of(q)
        props[name] = {"type": "object", "properties": {o: {"type": "number"} for o in opts}, "required": opts, "additionalProperties": False}
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def judge_questions_text(fam: dict, rng: random.Random) -> tuple[str, dict]:
    """Questions as shown to one judge; choice options in their natural order (positions matter for the targets)."""
    lines, shown = [], {}
    for name, q in fam["questions"].items():
        opts = options_of(q)
        if q["type"] == "noul":
            c = q["criteria"]
            body = f'[{name}] Statement: "{q["instructions"]}"' + (f'\n  true = {c["true"]}\n  false = {c["false"]}' if c else "") + "\n  Options: true, false"
        elif q["type"] == "choice":
            body = f'[{name}] {q["instructions"]}\n' + "\n".join(f"  {k} = {v}" for k, v in q["criteria"].items()) + f"\n  Options: {', '.join(opts)}"
        else:
            body = f'[{name}] {q["instructions"]} (ordered, lowest first)\n' + "\n".join(f"  {i} = {v}" for i, v in enumerate(q["criteria"])) + f"\n  Options: {', '.join(opts)}"
        lines.append(body)
        shown[name] = opts
    return "\n\n".join(lines), shown


def judge_messages(fam: dict, state: dict, persona: dict, rng: random.Random):
    qtext, shown = judge_questions_text(fam, rng)
    user = JUDGE_USER.format(role=fam["role"], domain=fam["domain"], record=json.dumps(state, indent=1, ensure_ascii=False), questions=qtext)
    return JUDGE_BASE + "\n\n" + persona["text"], user, judge_schema(fam), shown


def parse_judgment(data: dict, shown: dict) -> dict | None:
    out = {}
    for k, opts in shown.items():
        d = data.get(k)
        if not isinstance(d, dict) or any(o not in d for o in opts):
            return None
        vals = {o: float(d[o]) for o in opts}
        if any(v < 0 for v in vals.values()) or sum(vals.values()) <= 0:
            return None
        tot = sum(vals.values())
        out[k] = {o: v / tot for o, v in vals.items()}
    return out


def mean_gold(judgments: list, opts: list) -> dict:
    g = {o: sum(j[o] for j in judgments) / len(judgments) for o in opts}
    tot = sum(g.values())
    g = {o: round(v / tot, 4) for o, v in g.items()}
    drift = round(1 - sum(g.values()), 4)
    if drift:
        k = max(g, key=g.get)
        g[k] = round(g[k] + drift, 4)
    return g
