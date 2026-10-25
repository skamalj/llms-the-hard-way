# Signpost-D: score cases (brief v2.3, score questions only)

Read these two files first, and follow them for everything not said here:

- **`brief_v2.md`** sets the standard for cases: situations, forms, clear-cut and mixed, wording rules, options and domains.
- **`format_spec.md`** sets the exact output form, System One. Here it matters most for **score items:** an ordered list of levels, lowest first, each a self-contained `"Name: description"` string.

Where the two disagree on form, `format_spec.md` wins.

Invent everything yourself. Do not look anything up, and do not use the web.

## What is different in this batch

**Every question is a `score` question.** There are no true/false and no choice questions. Each case has **exactly 4 score questions**, each placing the situation on a different scale (for example how urgent, how serious, how likely, how far over budget).

The questions of one case must each measure something different: not the same scale reworded, and no question whose answer gives away another's.

## The rule every score question must meet

> **The instruction names one quantity. The levels run from the least of that quantity (level 0, first in the list) to the most.**

- Name the quantity in the instruction: "How urgent is…", "How serious is…", "How likely is…", "How far over the limit is…", "How ready is…". Never a neutral question such as "What is the status of…" or "Which band…".
- Every level sits on that one quantity. No level from another dimension (no "Correct" in the middle of an error scale).
- Each level is `"Name: description"`, where the description says what puts a situation at that level, and makes sense on its own.
- Neighbouring levels differ in **what they mean for the decision**, ideally with thresholds ("under 2 hours", "2–24 hours", "more than a day"). A careful reader can place the situation at exactly one level in a clear-cut case.

## Question kinds (shares across your batch)

The kinds are as in `brief_v2.md`, with these shares:

| Kind | Share | In a score question, for example |
|---|---|---|
| **Read** | about 20% | a level the situation nearly states: how many items are affected, how late the delivery already is, with levels as ranges |
| **Infer** | about 20% | a level that follows from combining separate details: how likely the order arrives in time, how exposed the account is |
| **Compare** | about 25% | a level set by numbers against limits: how far over budget, how far short of the target, how close to the deadline, with the thresholds in the levels |
| **Judge** | about 35% | a level a professional weighs from several signals: how urgent, how serious, how much risk, how strongly to escalate |

For **read** and **compare** questions, put the numbers in the situation and the thresholds in the levels. Do the arithmetic yourself, make every threshold say whether it is inclusive, and never put a value exactly on a threshold unless the wording settles it.

## Levels

- **Level-count quotas** across your batch: about 40% with 3 levels, 35% with 4, 25% with 5.
- Vary which level is right: in clear-cut cases the lowest and the highest levels should win about as often as the middle ones. Do not make the "sensible middle" usually right.

## Situations

- **About half the states are JSON records,** written the way a real system in that domain would store them: nested objects and lists, short field names, numbers as numbers, dates as strings.
- **The other half are text:** prose notes, emails, message threads, small tables, logs, forms or checklists.
- About 70% clear-cut and 30% genuinely mixed, as in `brief_v2.md`. A mixed score question is one where a careful reader would hesitate between two neighbouring levels.
- Many situations should be routine: a low level is a valid, common answer.

## Batch shape

Write **50 cases** in your batch, each with **exactly 4 score questions**, over the domains you are given. Never use the same question wording in two cases.

## Output

One JSON object per line, in System One form, **without gold**:

```json
{"id": "<batch>-001", "domain": "warehouse and inventory", "form": "JSON record",
 "state": {"...": "..."},
 "questions": {"q1": {"type": "score", "instructions": "How urgent is …?", "criteria": ["Low: …", "Moderate: …", "High: …"]},
               "q2": {"type": "score", "instructions": "How far over …?", "criteria": ["Within limit: …", "Slightly over: …", "Well over: …", "Far over: …"]}},
 "kinds": {"q1": "judge", "q2": "compare"}}
```

`kind` is one of `read`, `infer`, `judge`, `compare`.

Work only in the private folder you are given. Before finishing, check your output by script:
- every line parses, and the ids run in order;
- every question has `"type": "score"` and exactly the fields `type`, `instructions`, `criteria`;
- every case has exactly 4 questions, and `kinds` has an entry for each;
- every score has 3–5 levels, each a non-empty string containing ": ";
- no instruction is a neutral question without a quantity ("What is the status", "Which band", "Which level");
- no question text repeats.
