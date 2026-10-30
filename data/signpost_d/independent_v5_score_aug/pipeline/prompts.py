"""Briefs for the score-only augmentation: train_v2 document, labelling and checking briefs; a score-only question
brief with per-flow instructions; a twin-edit brief (F2) and a score-scale validation brief. Written for this set only; the generator and the
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

Setting: {domain_desc}. The material should be the kind of thing {decider} would later have to rate or assess from, but you are NOT writing any assessment or question; just the document as it would exist.

Build these features into it naturally, without flagging them:
{complications}

{flow_doc}
{computations}
Length: about {length_words} words{json_note}.

Return only the document."""

JSON_NOTE = " (for a system record: a single JSON object with 15 to 40 fields, nested where natural, inconsistent key naming across sections, a few nulls, some numbers stored as strings, and a free-text notes field containing two or three sentences)"

DOC_SCHEMA_TEXT = {"type": "object", "properties": {"document": {"type": "string"}}, "required": ["document"], "additionalProperties": False}
DOC_SCHEMA_JSON = {"type": "object", "properties": {"record": {"type": "object", "additionalProperties": True}}, "required": ["record"], "additionalProperties": False}


def doc_messages(seed: dict):
    from seeds import FLOWS
    comps = "\n".join(f"- {c}" for c in seed["complications"])
    calcs = ""
    if seed["computation_desc"]:
        calcs = "Include the raw inputs for these quantities, as separate facts in different places, never stating the results:\n" + "\n".join(f"- {c}" for c in seed["computation_desc"]) + "\n"
    user = DOC_USER.format(doc_kind=seed["doc_kind"], doc_desc=seed["doc_desc"], domain_desc=seed["domain_desc"],
                           decider=seed["decider"], complications=comps, flow_doc=FLOWS[seed["flow"]]["doc"], computations=calcs,
                           length_words=seed["length_words"], json_note=JSON_NOTE if seed["form"] == "json" else "")
    schema = DOC_SCHEMA_JSON if seed["form"] == "json" else DOC_SCHEMA_TEXT
    return DOC_SYSTEM, user, schema


TWIN_USER = """Below is a document and a description of ONE change to make to it. Rewrite the document with exactly that change and nothing else: keep every other fact, figure, name, date, wording and the format identical. Where the change means another figure in the document must also be different to stay consistent (for example a total that includes the changed item), make that consequential change too, but no other. Do not flag or explain the change.

CHANGE
{change}

DOCUMENT
--------
{document}
--------
Return only the rewritten document."""


def twin_messages(seed: dict, document, change: str):
    doc = json.dumps(document, indent=1, ensure_ascii=False) if isinstance(document, dict) else document
    schema = DOC_SCHEMA_JSON if isinstance(document, dict) else DOC_SCHEMA_TEXT
    return DOC_SYSTEM, TWIN_USER.format(change=change, document=doc), schema


# ----------------------------------------------------------------------------
# Stage 2: typed decision questions about the document (a different model)
# ----------------------------------------------------------------------------

Q_SYSTEM = """You write score questions about a document you are given. A separate panel of readers will answer them later with probabilities over the levels, using only the document; you will never see their answers and your own answer is not used as the key.

Every question is of type "score": a rating of ONE named quantity or property on an ordered scale.
- The "instructions" name exactly what is rated, from whose point of view and over what period or scope. Keep them under 45 words.
- The levels are listed from the LEAST of that quantity (level 0) to the MOST, each as "Name: description". Higher levels must mean monotonically more of the named quantity. If the natural wording is a "goodness" scale, name the quantity so that level 0 is the least of it (for example "How severe is the risk" with level 0 = negligible).
- The levels must not overlap and must leave no gap: every possible state of the facts falls into exactly one level. For numeric scales give exact edges with inclusive/exclusive wording ("at least 5% but below 8%"), the unit, the denominator or base, the time window, the rounding rule where it matters, and how missing observations are handled where they could matter.
- Level descriptions define conditions in general terms. They must not quote figures, dates or names from the document (declared numeric edges are allowed) and must never show the working.
- The four questions in a set rate four DIFFERENT quantities on four different scales; never ask the same thing twice in different words.
- Every question must be answerable from the document alone plus common sense; do not rely on outside knowledge. It is fine, and sometimes wanted, that the document leaves two neighbouring levels genuinely open.

Each question has a kind:
- "read": the evidence for the level is stated directly in the document;
- "compare": a figure, date, count or amount must be set against an edge or another value;
- "infer": a rule must be applied, an exception checked, or a value worked out from others;
- "judge": the level is a matter of judgement that the document informs but does not settle.

For every question also return: "computation" (rate / share / time_gap / difference / sum / average / ratio / change / aggregate / conversion / stated, or none for a non-numeric scale), and for a numeric scale "computed_value" (the value you worked out, in "unit"), "edges" (numeric edges ascending, one fewer than the levels) and "edge_rule" ("lower_inclusive" or "upper_inclusive"). These are recorded for quality control only.

Write in British English."""

Q_USER = """The decider is {decider} at {domain_desc}.

Write exactly 4 score questions about the document below.

Flow: {flow_q}

Plan for the four questions (follow the number of levels exactly; aim for the kind and for the level that the document's evidence should point to, counting from 0 = least):
{plan}

{twin_note}For each question also give "author_answer": your own best level and why, in one short line. It is recorded separately for quality checks only and is never used as the answer key.

DOCUMENT
--------
{document}
--------
Return only the JSON."""

TWIN_NOTE = """Also return "twin_change": ONE minimal, realistic change to a single fact in the document (a figure, a date, a count, or one condition being met or not) that would move the correct level of exactly one of your questions by one level, up or down, and name that question in "twin_question" (1-4). Describe the change precisely ("change the second reading from 4.8 to 5.1 mg/L"). The other questions may move only if the fact genuinely bears on them.

"""

Q_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "minItems": 4, "maxItems": 4,
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["score"]},
                    "kind": {"type": "string", "enum": ["read", "compare", "infer", "judge"]},
                    "instructions": {"type": "string"},
                    "true_desc": {"type": "string"},
                    "false_desc": {"type": "string"},
                    "choice_options": {"type": "array", "items": {"type": "object", "properties": {"label": {"type": "string"}, "meaning": {"type": "string"}}, "required": ["label", "meaning"], "additionalProperties": False}},
                    "score_levels": {"type": "array", "items": {"type": "string"}},
                    "computation": {"type": "string", "enum": ["rate", "share", "time_gap", "difference", "sum", "average", "ratio", "change", "aggregate", "conversion", "stated", "none"]},
                    "computed_value": {"type": "number"},
                    "unit": {"type": "string"},
                    "edges": {"type": "array", "items": {"type": "number"}},
                    "edge_rule": {"type": "string", "enum": ["lower_inclusive", "upper_inclusive"]},
                    "author_answer": {"type": "string"},
                },
                "required": ["type", "kind", "instructions", "author_answer"],
                "additionalProperties": False,
            },
        },
        "twin_change": {"type": "string"},
        "twin_question": {"type": "integer"},
    },
    "required": ["questions"],
    "additionalProperties": False,
}


def plan_text(seed: dict) -> str:
    return "\n".join(f'- question {i + 1}: {p["levels"]} levels; kind "{p["kind"]}"; evidence should point to level {p["target_level"]} of 0-{p["levels"] - 1}.'
                     for i, p in enumerate(seed["question_plan"]))


def q_messages(seed: dict, document):
    from seeds import FLOWS
    doc = json.dumps(document, indent=1, ensure_ascii=False) if isinstance(document, dict) else document
    twin = FLOWS[seed["flow"]].get("twins") and not seed.get("twin_of")
    user = Q_USER.format(decider=seed["decider"], domain_desc=seed["domain_desc"], flow_q=FLOWS[seed["flow"]]["q"], plan=plan_text(seed),
                         twin_note=TWIN_NOTE if twin else "", document=doc)
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


# ----------------------------------------------------------------------------
# Stage 5: score-scale validation (Opus, all questions, after gold is formed)
# ----------------------------------------------------------------------------

VALIDATE_SYSTEM = """You validate score questions for a training set. For each question you see the document, the question, its ordered levels (0 = least) and the gold probability distribution (an average of several independent readers, possibly corrected by an arithmetic check). Check each question against all of these, doing any arithmetic yourself, silently:

1. type: it is an ordered rating of one named quantity;
2. completeness: instruction, levels and gold are all present and meaningful;
3. monotonicity: level 0 is the least of the named quantity and levels increase consistently;
4. coverage: every plausible state of the facts falls into some level;
5. overlap: neighbouring levels are distinguishable, with no ambiguous or overlapping boundary (numeric edges explicit about inclusive/exclusive, units, denominator, window and rounding where these matter);
6. grounding: the document contains the facts needed to rate it, without outside knowledge;
7. arithmetic: any calculation behind the gold's top level is right;
8. distribution: probabilities refer only to the listed levels and sum to 1;
9. uncertainty: the gold's sharpness fits the evidence (sharp where the document settles it, spread over neighbours where it genuinely does not);
10. originality: the question is not a restatement of another question in the same set;
plus, where relevant: missing-evidence policy stated (when evidence is missing, the scale says how that is treated); weighting stated (when criteria conflict and the level depends on how they are weighed, the instruction or levels say how).

Verdict per question:
- "keep" if it passes, including when the gold is soft because the document is genuinely open;
- "reject" if any check fails in a way that makes the question unfit to train on (an ambiguous or overlapping scale, a gap, a non-monotonic scale, missing facts, an unstated missingness or weighting policy that decides the answer, a wrong gold top level that the document clearly settles otherwise, a duplicate).
Give the main issue category (none, type, completeness, monotonicity, coverage, overlap, grounding, arithmetic, distribution, uncertainty, originality, missingness_policy, weighting) and a note of at most 25 words. Be strict but fair: do not reject for style."""

VALIDATE_USER = """DOCUMENT
--------
{document}
--------

QUESTIONS WITH GOLD
{questions}

For each question return: key, verdict, issue, note."""

VALIDATE_SCHEMA = {
    "type": "object",
    "properties": {
        "checks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "verdict": {"type": "string", "enum": ["keep", "reject"]},
                    "issue": {"type": "string", "enum": ["none", "type", "completeness", "monotonicity", "coverage", "overlap", "grounding", "arithmetic",
                                                          "distribution", "uncertainty", "originality", "missingness_policy", "weighting"]},
                    "note": {"type": "string"},
                },
                "required": ["key", "verdict", "issue", "note"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["checks"],
    "additionalProperties": False,
}


def validate_messages(document, questions: dict, gold: dict):
    doc = json.dumps(document, indent=1, ensure_ascii=False) if isinstance(document, dict) else document
    lines = []
    for key, q in questions.items():
        desc = "\n".join(f"  {i} = {lvl}" for i, lvl in enumerate(q["criteria"]))
        g = ", ".join(f"{k}: {v:.2f}" for k, v in gold[key].items())
        lines.append(f'[{key}] {q["instructions"]} (ordered scale, lowest first)\n{desc}\n  Gold: {g}')
    return VALIDATE_SYSTEM, VALIDATE_USER.format(document=doc, questions="\n\n".join(lines)), VALIDATE_SCHEMA
