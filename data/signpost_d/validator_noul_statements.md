# Signpost-D: true/false items as statements (System One `noul`)

Read `format_spec.md` (in this folder) first.

The published definition of `noul` is **"the probability that the statement is true"**. Our true/false items were written as yes/no questions ("Is any stock still in chiller 3?"). A question is answered yes or no; a statement is true or false. Your job is to rewrite **every** `noul` instruction you are given as a **statement**.

## Rules

1. **The statement is the affirmative form of the question,** so `true` means exactly what "yes" meant:
   - "Is any stock still in chiller 3?" → "There is still stock in chiller 3."
   - "Has the supplier confirmed the delivery date?" → "The supplier has confirmed the delivery date."
   - "Did the driver claim the first cod reading came from the outer pack?" → "The driver claimed the first cod reading came from the outer pack."
   - "Will the order arrive before the event on 14 May?" → "The order will arrive before the event on 14 May."
   - "Is the total within the GBP 500 limit?" → "The total is within the GBP 500 limit."
2. **Never negate or flip the question.** "Is the order late?" becomes "The order is late.", not "The order is on time."
   - If the question itself contains a negation ("Has the tenant not paid?"), keep it: "The tenant has not paid."
3. **Keep every detail:**
   - names, numbers, dates, times and units;
   - limits and how they are counted ("at least", "more than", "on or before", "business days");
   - conditions ("If the courier is late, …"), timing ("by the 16:00 check") and hedges ("likely", "probably").
   - A question about likelihood stays one: "Is the order likely to arrive in time?" → "The order is likely to arrive in time."
4. **One statement,** written as a plain declarative sentence ending with a full stop. No question mark, and no "true or false:" prefix.
5. **The descriptions.** `criteria` keeps exactly the keys `"true"` and `"false"`.
   - `true` must say what makes the statement true, and `false` what makes it false, covering every way it can be false.
   - Rewrite a description only if it refers to "yes", "no" or "the answer", or no longer fits the statement. Otherwise keep it word for word.
6. **The gold stays exactly as it is.** `true` = the old "yes" probability, `false` = the old "no" probability.
   - If you think a rewrite cannot keep the meaning, do not rewrite that item. Report it instead, with `verdict` `"report"` and a note.

## Output

One line for **every** `noul` question in your input:

```json
{"id": "A-001", "qid": "q1", "verdict": "fix", "rule": 1,
 "note": "statement form",
 "question": {"type": "noul", "instructions": "There is still dairy stock in chiller 3 at the end of the report.",
              "criteria": {"true": "Some stock remains in chiller 3 at the end of the report", "false": "Chiller 3 has been fully emptied"}},
 "gold": {"type": "noul", "probabilities": {"true": 0.97, "false": 0.03}}}
```

Before you finish, check your output by script:
- there is one line per `noul` question in your input, with the ids and qids matching;
- every instruction ends with "." and contains no "?";
- the criteria keys are exactly `true` and `false`, and neither description is empty;
- every gold is identical to the input gold.

Then report:
- the counts of fixes and reports;
- every report, with its reason;
- five examples, before and after.

Work only in the private folder you are given. Do not use the web or any other file.
