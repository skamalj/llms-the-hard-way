# Signpost-D: harder general cases (brief v2.5, all three question types)

Read these two files first, and follow them for everything not said here:

- **`brief_v2.md`** sets the standard for cases: situations, forms, wording rules, options and domains.
- **`format_spec.md`** sets the exact output form, System One: `noul` statements with `true` / `false` descriptions, `choice` labels with descriptions, `score` levels lowest first as `"Name: description"` strings.

Where the two disagree on form, `format_spec.md` wins. Invent everything yourself. Do not look anything up, and do not use the web.

## What is different in this batch

A small model trained on earlier cases answers well when the answer is stated, but often answers from **signal words** ("leaks", "urgent", "compromised", "late") instead of the number, date or rule that actually decides. These cases are written so that careful reading is needed and signal words are not enough.

**Every case has at least two of these features**, chosen to fit the situation:

1. **Several numbers of the same kind**, of which only one decides (three quotes, four deadlines, two balances, an old and a new limit).
2. **A rule with a condition or exception stated apart from the trigger**: the refund rule says faulty items get a full refund within 30 days, and the customer's message says the bottle "leaks" without using the word "faulty".
3. **A small calculation**: a rate (returns per units sold against a percentage limit), a total of 2–4 parts, a difference, days or hours between two dates or times, an average of two or three values. Do the arithmetic yourself and give the inputs, never the result.
4. **Misleading tone**: alarming words where the facts are within limits, or calm, reassuring words where a fact breaks a rule. Use this in both directions about equally.
5. **Information in two places**: the deciding fact is in a different part of the state from the question's topic (a date in a header, an exception in a footnote, a figure in a second message).
6. **Irrelevant but plausible details**: extra fields, side remarks or older figures that do not change the answer.

## Questions

- **3 to 6 questions per case**, mixing the three types. Across your batch, roughly: `noul` 35%, `choice` 35%, `score` 30%.
- **Kinds** (put each question's kind in `kinds`): read about 15%, infer about 20%, **compare about 30%**, judge about 35%.
- **Compare questions** set a number, date or count against a limit or against another number. Put the inputs in the state; never quote the deciding value or the result in the question.
- Each question of a case asks something different; no question gives away another's answer.
- Follow every wording rule of `brief_v2.md` section 2a: inclusive or exclusive limits, how days are counted, one reading per rule, never a value exactly on a threshold unless the wording settles it.
- `noul` instructions are statements, never questions, and `true` / `false` together cover every case.
- **Option counts** across the batch: choice about 15% with 2 options, 30% with 3, 25% with 4, 20% with 5, 10% with 6; score about 40% with 3 levels, 35% with 4, 25% with 5.
- Vary which option is right. In clear-cut questions the extreme options win about as often as the middle ones, `true` and `false` about equally, and the first option no more often than others.

## Situations

- **About half the states are JSON records** (nested objects and lists, field names a real system would use, numbers as numbers, dates as strings), the rest text: prose notes, emails, message threads, small tables, logs, forms or checklists.
- **Length:** 80–450 words, or an equivalent amount of data. Longer than earlier cases on average, because of the extra numbers and details.
- **About 60% clear-cut and 40% genuinely mixed.** Clear-cut means a careful reader who does the reading and the arithmetic is sure; a hasty reader may well be wrong. Mixed means a careful reader would still hesitate between two options, or lean only moderately.
- Many situations should be routine: "no action", "within limit" and "low" are valid, common answers.

## Batch shape

Write **50 cases** in your batch, over the domains you are given (about evenly). Never use the same question wording in two cases.

## Output

One JSON object per line, in System One form, **without gold** (separate labellers answer every question):

```json
{"id": "<batch>-001", "domain": "warehouse and inventory", "form": "JSON record",
 "state": {"...": "..."},
 "questions": {"q1": {"type": "noul", "instructions": "<a statement>", "criteria": {"true": "…", "false": "…"}},
               "q2": {"type": "choice", "instructions": "…?", "criteria": {"<label>": "<what choosing it means>", "…": "…"}},
               "q3": {"type": "score", "instructions": "How urgent is …?", "criteria": ["Low: …", "Moderate: …", "High: …"]}},
 "kinds": {"q1": "compare", "q2": "judge", "q3": "infer"},
 "features": [1, 3]}
```

`kind` is one of `read`, `infer`, `judge`, `compare`; `features` lists the numbers of the features above that the case uses.

Work only in the private folder you are given. Before finishing, check your output by script:
- every line parses, and the ids run in order;
- every question has exactly the fields `type`, `instructions`, `criteria`, with a valid type;
- `noul`: criteria exactly `true` and `false`, non-empty, and the instruction does not end with "?";
- `choice`: 2–6 labels, each with a non-empty description; `score`: 3–5 levels, each a string containing ": ";
- every case has 3–6 questions, `kinds` has an entry for each, and `features` lists at least two numbers from 1–6;
- no question text repeats across the batch.
