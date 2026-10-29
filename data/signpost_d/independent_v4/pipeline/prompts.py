"""Briefs for the three stages (train_v2 briefs; R19 additions for train_v3 are marked "R19"). Written for this set only; the generator and the
labellers never see each other's instructions, and no stage sees any other
data set or benchmark.
"""
from __future__ import annotations

import json

# ----------------------------------------------------------------------------
# Stage 1: raw document, no questions in mind
# ----------------------------------------------------------------------------

DOC_SYSTEM = """You write raw workplace material for a corpus of realistic documents. You are not writing a puzzle, a test, or a summary; you are producing the kind of document that actually exists inside an organisation, with the mess that real documents have.

Rules you always follow:
- Invent everything: organisations, people, places, product names, policy clauses, reference numbers, amounts, dates and times. Never use a real company, a real person, or anything copied from somewhere else.
- Be specific. Real documents are full of concrete numbers, dates, times, amounts, references and names. Use many, and give several of them no bearing on anything important.
- Keep the realism of the format you are asked for: emails have subject lines, greetings, quoted replies and signatures; logs have timestamps; forms have labels; policies have clause numbers; system records have field names that nobody tidied up.
- Do not explain, summarise, interpret or conclude. Do not add headings like "Summary" or "Key facts". Do not pose questions to the reader. Do not resolve the situation at the end; stop where a real document would stop.
- Do not mention that anything is invented, and do not add a note to the reader.
- Write in British English."""

DOC_USER = """Produce one {doc_kind}: {doc_desc}.

Setting: {domain_desc}. The material should be the kind of thing {decider} would later have to make a decision from, but you are NOT writing the decision or any question; just the document as it would exist.

Build these features into it naturally, without flagging them:
{complications}

The document must also contain the raw inputs for these two quantities, stated as separate facts in different places, with the result itself never stated or hinted at (no totals, no percentages, no durations for them):
{computations}
Also include at least one quantity that is stated directly as a single figure with its unit.
{time_note}{choice_note}

Length: about {length_words} words{json_note}.

Return only the document."""

JSON_NOTE = " (for a system record: a single JSON object with 15 to 40 fields, nested where natural, inconsistent key naming across sections, a few nulls, some numbers stored as strings, and a free-text notes field containing two or three sentences)"

DOC_SCHEMA_TEXT = {"type": "object", "properties": {"document": {"type": "string"}}, "required": ["document"], "additionalProperties": False}
DOC_SCHEMA_JSON = {"type": "object", "properties": {"record": {"type": "object", "additionalProperties": True}}, "required": ["record"], "additionalProperties": False}


def doc_messages(seed: dict):
    comps = "\n".join(f"- {c}" for c in seed["complications"])
    calcs = "\n".join(f"- {c}" for c in seed["computation_desc"])
    user = DOC_USER.format(doc_kind=seed["doc_kind"], doc_desc=seed["doc_desc"], domain_desc=seed["domain_desc"],
                           decider=seed["decider"], complications=comps, computations=calcs, length_words=seed["length_words"],
                           json_note=JSON_NOTE if seed["form"] == "json" else "", **_doc_extras(seed))
    schema = DOC_SCHEMA_JSON if seed["form"] == "json" else DOC_SCHEMA_TEXT
    return DOC_SYSTEM, user, schema


def _doc_extras(seed: dict) -> dict:
    # R19: the time-gap flavour and the material the choice questions will need
    time_note = ""
    if seed.get("time_gap_variant"):
        time_note = f"For the time or date gap, use this form: {seed['time_gap_variant']}.\n"
    choice_note = ""
    if seed.get("choice_desc"):
        lines = "\n".join(f"- {c}" for c in seed["choice_desc"])
        choice_note = ("The document must also lay out, in its own natural form and without comparing them or saying which is best:\n"
                       f"{lines}\nGive each alternative its own figures and conditions, spread over the document.\n")
    return {"time_note": time_note, "choice_note": choice_note}


# ----------------------------------------------------------------------------
# Stage 2: typed decision questions about the document (a different model)
# ----------------------------------------------------------------------------

Q_SYSTEM = """You write decision questions about a document you are given. A separate panel of readers will answer them later with probabilities, using only the document; you will never see their answers and your own answer is not used as the key.

There are three question types, and the output format is strict.

1. "noul": a statement about the situation whose truth is to be judged. The "instructions" field must BE the statement itself: one declarative sentence such as "The consignment weighs more than the service allows." Never write "Judge whether...", "Decide if...", "Is it the case that..." or any other framing. Provide a short description of what "true" means and what "false" means, phrased so that between them they cover every possible case.
2. "choice": a question answered by exactly one of 2 to 6 labelled options. Labels are short snake_case tokens; each has a one-line meaning. Options must be mutually exclusive and together cover every possibility (add a catch-all option if needed).
3. "score": a rating of one named quantity on an ordered scale of 3 to 5 levels. The instructions must say what quantity is being rated and from whose point of view. Levels are listed from the least of that quantity to the most, each written as "Name: description". In this set, score questions are mostly COMPUTED: the level is decided by a numeric value that the document gives only as inputs (a rate, a share of a count, a gap between two times or dates, a difference, a sum of parts, or an average), and the question must never state the result. Each level description states its own edges with inclusive or exclusive limits ("at least 5% but below 8%"; "more than 90 minutes"), so that a reader who works the value out can place it; the edges must be consistent, non-overlapping and cover every possible value. Pick the edges so that the computed value lands at the requested distance from the nearest edge ("close": within 5% of the edge value, "moderate": 5% to 25% away, "far": more than 25% away). A score question may instead be RULE-DECIDED (computation "rule"): each level is an outcome of a stated rule with its exception (for example the refund tier a policy assigns), so the level follows from applying the rule to the facts; give no edges for it. A "stated-value band" question is the exception: the value is given directly in the document, and the band edges are uneven, awkward numbers (for example under 6.6; 6.6 to under 10; 10 to under 13.5).

Each question also has a kind:
- "read": the answer is stated directly in the document;
- "compare": the answer needs one figure compared with another or with a stated limit;
- "infer": the answer needs a rule applied, an exception checked, or a value worked out from others;
- "judge": the answer is a matter of judgement (urgency, severity, reasonableness, risk) that the document informs but does not settle.

Quality rules:
- Follow the requested composition exactly: the number of score, true/false and choice questions, which computations the score questions use, and the margin band for each score question.
- For every score question also return: "computation" (rate / share / time_gap / difference / sum / average / stated / rule), "computed_value" (the number you worked out, in "unit"), "edges" (the numeric level edges in ascending order, one fewer than the levels, in the same unit; empty for a rule-decided question) and "edge_rule" ("lower_inclusive" if level k runs from edges[k-1] inclusive to edges[k] exclusive, "upper_inclusive" if the reverse). These numbers are recorded for quality control, never shown to the model being tested.
- Every question must be answerable from the document alone, in the sense that a careful reader can commit to probabilities; it is fine, and wanted, that some questions have no certain answer because the document is incomplete, approximate or self-contradictory.
- Questions must be about the specific situation in the document, written from the decider's point of view, and must not rely on outside knowledge beyond common sense.
- Do not reuse the document's exact field names or headings in the wording; refer to things by their meaning.
- Do not ask about trivia (the colour of a van, a person's job title) unless it decides something.
- The option descriptions ("true"/"false" descriptions, choice meanings, score levels) must describe the condition in general terms. They must not quote figures, dates or names from the document and must not show the working (never "22 Oct plus 3 gives 27 Oct"); the reader has to do that work.
- At most two "judge" questions per set. At least 30% of the questions must be "compare" (one when writing 3 questions, two when writing 4 to 6): a number, date, time, count or amount set against a limit, a deadline or another value in the document. At least one question must need a calculation or a rule-with-exception.
- Mix the kinds. Include at least one "compare" or "infer" that needs a small calculation or a rule-with-exception, and at least one "judge".
- Choice questions in this set are NOT direct lookups: picking the right option needs a calculation across the options (the cheapest after each one's discount, the only candidate meeting every condition, the earliest feasible slot) or applying a rule with its exception. Each option is one of the alternatives (or outcomes), plus a catch-all only if needed for coverage; follow the requested number of options exactly.
- For "choice", the "instructions" field is a direct question ending in a question mark. For "score", it names the quantity being rated and from whose point of view.
- Write in British English. Keep instructions under 40 words."""

Q_USER = """The decider is {decider} at {domain_desc}.

Write exactly {n_questions} questions about the document below: {n_score} score, {n_noul} true/false (noul) and {n_choice} choice.

Score questions: {score_plan}

Choice questions: {choice_plan}

Kinds target across the set: about 40% compare, about 35% infer, about 20% judge, the rest read. A computed score question whose core is working out one value and placing it against edges counts as "compare"; one that also needs a rule or exception applied, and every rule-decided score question, counts as "infer". A choice question decided by working out a figure for each option and comparing them counts as "compare"; one decided by checking conditions or applying a rule with its exception counts as "infer". Use the true/false question, if any, for a compare or infer about a date or time where natural.

Target for the non-score questions: {clarity_target}

For each question also give "author_answer": your own best answer in one short line. It is recorded separately for quality checks only and is never used as the answer key.

DOCUMENT
--------
{document}
--------
Return only the JSON."""

CLARITY_TARGETS = {
    "mostly clear": "most questions should have a determinable answer; at most one may be genuinely debatable.",
    "mixed": "about half of the questions should be determinable and about half genuinely debatable because of missing, approximate or conflicting detail in the document.",
    "mostly debatable": "most questions should be genuinely debatable, with at most one or two that a careful reader could answer with confidence.",
}

Q_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "minItems": 3, "maxItems": 6,
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["noul", "choice", "score"]},
                    "kind": {"type": "string", "enum": ["read", "compare", "infer", "judge"]},
                    "instructions": {"type": "string"},
                    "true_desc": {"type": "string"},
                    "false_desc": {"type": "string"},
                    "choice_options": {"type": "array", "items": {"type": "object", "properties": {"label": {"type": "string"}, "meaning": {"type": "string"}}, "required": ["label", "meaning"], "additionalProperties": False}},
                    "score_levels": {"type": "array", "items": {"type": "string"}},
                    "computation": {"type": "string", "enum": ["rate", "share", "time_gap", "difference", "sum", "average", "stated", "rule", "none"]},
                    "computed_value": {"type": "number"},
                    "unit": {"type": "string"},
                    "edges": {"type": "array", "items": {"type": "number"}},
                    "edge_rule": {"type": "string", "enum": ["lower_inclusive", "upper_inclusive"]},
                    "author_answer": {"type": "string"},
                },
                "required": ["type", "kind", "instructions", "author_answer"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["questions"],
    "additionalProperties": False,
}


def score_plan_text(seed: dict) -> str:
    # R19: per-question decider and number of levels
    lines = []
    for i, sp in enumerate(seed["score_plan"]):
        n = sp["levels"]
        if sp["decider"] == "stated":
            lines.append(f'score question {i + 1}: {n} levels; a STATED-VALUE band question (computation "stated") with uneven band edges; margin band "{sp["margin"]}".')
        elif sp["decider"] == "rule":
            lines.append(f'score question {i + 1}: {n} levels; RULE-DECIDED (computation "rule"): the level is the outcome of a rule stated in the document applied to the facts, where an exception clause or condition decides between adjacent levels; no edges.')
        else:
            c = sp["decider"]
            lines.append(f'score question {i + 1}: {n} levels; computed from the document\'s inputs by a {c.replace("_", " ")} (computation "{c}"); choose the edges so the computed value lands "{sp["margin"]}" to the nearest edge.')
    return " ".join(lines)


CHOICE_TEXT = {
    "cheapest_after_adjustment": "which alternative costs least once each one's own discount, surcharge, minimum or fee is applied",
    "only_one_meets_all": "which single candidate meets every stated condition",
    "earliest_feasible": "which is the earliest slot, date or route that satisfies every constraint",
    "largest_or_smallest_computed": "which item ranks highest or lowest on a rate, total or average worked out from its stated parts",
    "rule_with_exception": "which outcome the stated rule gives once its exception clause is checked",
}


def choice_plan_text(seed: dict) -> str:
    if not seed["choice_plan"]:
        return "none."
    return " ".join(f'choice question {i + 1}: exactly {c["options"]} options; asks {CHOICE_TEXT[c["pattern"]]}.' for i, c in enumerate(seed["choice_plan"]))


def q_messages(seed: dict, document):
    doc = json.dumps(document, indent=1, ensure_ascii=False) if isinstance(document, dict) else document
    user = Q_USER.format(decider=seed["decider"], domain_desc=seed["domain_desc"], n_questions=seed["n_questions"],
                         n_score=seed["n_score"], n_noul=seed["n_noul"], n_choice=seed["n_choice"], score_plan=score_plan_text(seed), choice_plan=choice_plan_text(seed),
                         clarity_target=CLARITY_TARGETS[seed["clarity"]], document=doc)
    return Q_SYSTEM, user, Q_SCHEMA


# ----------------------------------------------------------------------------
# Stage 3: labelling (several separate calls, averaged)
# ----------------------------------------------------------------------------

LABEL_SYSTEM_BASE = """You answer decision questions about a document by giving a probability for each possible answer. You see only the document and the questions; there is no answer key and nobody will explain the document to you.

How to answer:
- Use only what the document says, plus ordinary common sense. Do not assume facts it does not give.
- When the document settles the answer, say so with a high probability on that option.
- When the document does not settle it (information is missing, approximate, or contradictory), spread your probability to reflect how you actually weigh the possibilities. Do not pretend to certainty you do not have, and do not spread probability out of politeness when the document is clear.
- For a "score" scale, the levels are ordered from least to most; probabilities should usually sit on one or two adjacent levels.
- Probabilities for one question must sum to 1.
- Answer every question. Do not add commentary."""

PERSONAS = {
    "literal": ("haiku", "You are a literal reader: you take the document at its word, trust explicit statements and stated rules, and treat anything not written down as unknown."),
    "operator": ("haiku", "You are an experienced operator in this kind of workplace: you read documents the way a practical person who has to act on them does, filling small gaps with what usually happens in practice, and you are comfortable committing when the practical answer is obvious."),
    "auditor": ("haiku", "You are a cautious auditor: you check every number and date, notice corrections and contradictions, apply rules exactly as written including their exceptions, and you flag uncertainty with spread probabilities rather than guessing."),
    "analyst": ("opus", "You are a careful analyst: you reason through each question step by step in your head before committing, calculate any figures that need calculating, and give calibrated probabilities."),
}

LABEL_USER = """DOCUMENT
--------
{document}
--------

QUESTIONS
{questions}

Return probabilities for every question, using the option names exactly as given."""


def format_questions_for_labeller(questions: dict, rng) -> tuple:
    """Render questions with option order shuffled for choice; returns (text, mapping) where mapping
    records per question the option names as presented."""
    lines = []
    presented = {}
    for key, q in questions.items():
        if q["type"] == "noul":
            opts = ["true", "false"]
            lines.append(f'[{key}] Statement: "{q["instructions"]}"\n  true = {q["criteria"]["true"]}\n  false = {q["criteria"]["false"]}\n  Options: true, false')
        elif q["type"] == "choice":
            opts = list(q["criteria"].keys())
            rng.shuffle(opts)
            desc = "\n".join(f"  {o} = {q['criteria'][o]}" for o in opts)
            lines.append(f'[{key}] {q["instructions"]}\n{desc}\n  Options: {", ".join(opts)}')
        else:
            opts = [str(i) for i in range(len(q["criteria"]))]
            desc = "\n".join(f"  {i} = {lvl}" for i, lvl in enumerate(q["criteria"]))
            lines.append(f'[{key}] {q["instructions"]} (ordered scale, lowest first)\n{desc}\n  Options: {", ".join(opts)}')
        presented[key] = opts
    return "\n\n".join(lines), presented


LABEL_SCHEMA = {
    "type": "object",
    "properties": {
        "answers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "probabilities": {"type": "array", "items": {"type": "object", "properties": {"option": {"type": "string"}, "p": {"type": "number"}}, "required": ["option", "p"], "additionalProperties": False}},
                },
                "required": ["key", "probabilities"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["answers"],
    "additionalProperties": False,
}


def label_messages(persona: str, document, questions: dict, rng):
    model, persona_text = PERSONAS[persona]
    doc = json.dumps(document, indent=1, ensure_ascii=False) if isinstance(document, dict) else document
    qtext, presented = format_questions_for_labeller(questions, rng)
    system = LABEL_SYSTEM_BASE + "\n\n" + persona_text
    user = LABEL_USER.format(document=doc, questions=qtext)
    return model, system, user, LABEL_SCHEMA, presented


# ----------------------------------------------------------------------------
# Stage 4: checking pass for read / compare / infer questions (a separate model from the writer)
# ----------------------------------------------------------------------------

VERIFY_SYSTEM = """You check answer keys for questions about a document. You will see the document and some questions of kind read, compare or infer. For each question, work the answer out properly and in full: quote the facts that matter, do any arithmetic, date or working-day counting explicitly, convert units where needed, and apply any stated rule exactly as written, including its exceptions and the order of precedence.

Do that working silently; do not write it out. Then decide whether the document SETTLES the question:
- settled = true when a careful reader who did the working would commit to one option with little doubt. Give that option and a confidence from 0.85 to 1.0.
- settled = false when the document leaves genuine doubt (a needed fact is missing, a figure is only approximate, two statements conflict and neither is authoritative, or the rule does not clearly cover the case). Give your best option and a confidence under 0.85.

Be strict about what "settled" means: a question is not settled just because one answer seems likely; it is settled when the facts in the document determine it. Do not add outside facts. Use the option names exactly as given. Answer every question listed."""

VERIFY_USER = """DOCUMENT
--------
{document}
--------

QUESTIONS TO CHECK
{questions}

For a question whose level or truth depends on a value you had to work out from the document's inputs, also return that value as "computed_value" (a number only; otherwise null) and its unit as "unit".

For each question return: key, settled, answer, confidence, computed_value, unit."""

VERIFY_SCHEMA = {
    "type": "object",
    "properties": {
        "checks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "settled": {"type": "boolean"},
                    "answer": {"type": "string"},
                    "confidence": {"type": "number"},
                    "computed_value": {"type": ["number", "null"]},
                    "unit": {"type": ["string", "null"]},
                },
                "required": ["key", "settled", "answer", "confidence", "computed_value", "unit"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["checks"],
    "additionalProperties": False,
}


def verify_messages(document, questions: dict):
    doc = json.dumps(document, indent=1, ensure_ascii=False) if isinstance(document, dict) else document
    lines = []
    for key, q in questions.items():
        if q["type"] == "noul":
            lines.append(f'[{key}] Statement: "{q["instructions"]}"\n  true = {q["criteria"]["true"]}\n  false = {q["criteria"]["false"]}\n  Options: true, false')
        elif q["type"] == "choice":
            desc = "\n".join(f"  {o} = {m}" for o, m in q["criteria"].items())
            lines.append(f'[{key}] {q["instructions"]}\n{desc}\n  Options: {", ".join(q["criteria"].keys())}')
        else:
            desc = "\n".join(f"  {i} = {lvl}" for i, lvl in enumerate(q["criteria"]))
            lines.append(f'[{key}] {q["instructions"]} (ordered scale, lowest first)\n{desc}\n  Options: {", ".join(str(i) for i in range(len(q["criteria"])))}')
    return VERIFY_SYSTEM, VERIFY_USER.format(document=doc, questions="\n\n".join(lines)), VERIFY_SCHEMA
