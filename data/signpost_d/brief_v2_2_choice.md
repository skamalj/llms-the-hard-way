# Signpost-D: choice cases (brief v2.2, choice questions only)

Read these two files first, and follow them for everything not said here:

- **`brief_v2.md`** sets the standard for cases: situations, forms, clear-cut and mixed, wording rules, options and domains.
- **`format_spec.md`** sets the exact output form, System One. Here it matters most for **choice items:** labels, each with a description.

Where the two disagree on form, `format_spec.md` wins.

Invent everything yourself. Do not look anything up, and do not use the web.

## What is different in this batch

**Every question is a `choice` question.** There are no true/false and no score questions. Each case has **4–5 choice questions**, so the model learns to pick between named options from many angles of one situation.

The questions of one case must each ask about something different: not the same decision reworded, and no question whose answer gives away another's.

## Question kinds (shares across your batch)

The kinds are as in `brief_v2.md`, with these shares:

| Kind | Share | In a choice question, for example |
|---|---|---|
| **Read** | about 20% | which item, person, status or option the situation states, among several that are mentioned |
| **Infer** | about 20% | which conclusion follows from combining separate details (which delivery arrives first, which account is affected) |
| **Compare** | about 25% | which of several values is largest, smallest, over a limit, or closest to a deadline; which total matches; which option the numbers favour |
| **Judge** | about 35% | what should happen next, who should handle it, which risk matters most, weighing several signals |

For **compare** questions, put the numbers in the situation (amounts, quantities, dates, durations, scores), and make the options name the things being compared or the outcomes of the comparison. Do the arithmetic yourself before you write the options, and make sure exactly one option is right in a clear-cut case.

## Options

- **Option-count quotas** across your batch: about 15% with 2 options, 30% with 3, 25% with 4, 20% with 5, 10% with 6.
- Labels are short names (1–3 words); every label has a one-line description that says what choosing it means.
- Options are mutually exclusive and all real possibilities.
- Vary which option is right: not usually the first, the most dramatic, or the "sensible middle" ("hold and check").

## Situations

- **About half the states are JSON records,** written the way a real system in that domain would store them: nested objects and lists, short field names, numbers as numbers, dates as strings.
- **The other half are text:** prose notes, emails, message threads, small tables, logs, forms or checklists.
- About 70% clear-cut and 30% genuinely mixed, as in `brief_v2.md`.
- Many situations should be routine: a choice where the ordinary option is right is a valid, common case.

## Batch shape

Write **50 cases** in your batch, each with **4–5 choice questions**, over the domains you are given. Never use the same question wording in two cases.

## Output

One JSON object per line, in System One form, **without gold**:

```json
{"id": "<batch>-001", "domain": "warehouse and inventory", "form": "JSON record",
 "state": {"...": "..."},
 "questions": {"q1": {"type": "choice", "instructions": "…", "criteria": {"<label>": "<description>", "…": "…"}},
               "q2": {"type": "choice", "instructions": "…", "criteria": {"<label>": "<description>", "…": "…"}}},
 "kinds": {"q1": "compare", "q2": "judge"}}
```

`kind` is one of `read`, `infer`, `judge`, `compare`.

Work only in the private folder you are given. Before finishing, check your output by script:
- every line parses, and the ids run in order;
- every question has `"type": "choice"` and exactly the fields `type`, `instructions`, `criteria`;
- every case has 4–5 questions, and `kinds` has an entry for each;
- every choice has 2–6 labels, each with a non-empty description;
- no question text repeats.
