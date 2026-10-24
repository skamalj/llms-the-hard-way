# Signpost-D: true/false descriptions that cover every case (System One `noul`)

Read `format_spec.md` (in this folder) first. Every `noul` item is a statement with two descriptions:
- `true`: what makes the statement true;
- `false`: what makes it false.

You check **one rule only**:

> **Between them, the two descriptions cover every possible case, with no gap and no overlap, and they mean exactly what the statement means.**

Earlier validators found this broken in several ways:
- **A boundary left out:** the statement says "on or before 30 September", but `false` says "after 30 September" and `true` says "before 30 September", so 30 September itself is in neither.
- **A boundary in both:** `true` says "30 days or more" and `false` says "30 days or fewer".
- **`false` narrower than "not true":** for the statement "Anya's shift is confirmed", `false` says only "It is not yet known whether Anya will work", which leaves out "Anya is confirmed as not working".
- **A description that disagrees with the statement:** the statement says "by midday Monday", but `true` says "noon today".

## What to do for every `noul` item

1. Read the statement and both descriptions, and the state where needed.
2. If the descriptions are exact complements and match the statement, do nothing.
3. Otherwise, rewrite **only the description(s) that need it**, so that:
   - `true` describes exactly the situations in which the statement is true;
   - `false` describes exactly all the others. "Not true" covers everything else, including boundary values and unknowns where the statement claims something definite.
4. **Never change the statement, and never change the gold.** If the description fix would change what the gold should be, write the line with `"verdict": "report"` and explain why, instead of fixing it.
5. Keep descriptions short, one sentence each. Use the statement's own words for limits: "on or before", "at least", "more than".

## Output

Write a line **only for an item you fix or report**, in the same form as before:

```json
{"id": "G11-008", "qid": "q4", "verdict": "fix", "rule": 2,
 "note": "false left out 30 September itself",
 "question": {"type": "noul", "instructions": "<the statement, unchanged>",
              "criteria": {"true": "…", "false": "…"}},
 "gold": {"type": "noul", "probabilities": {"true": 0.9, "false": 0.1}}}
```

Before you finish, check your output by script:
- every line parses, and every id and qid is in your input;
- every instruction is identical to the input;
- every gold is identical to the input;
- the criteria keys are exactly `true` and `false`, and neither description is empty.

Then report:
- how many items you checked;
- the counts of fixes and reports;
- every report, with its reason;
- five examples of fixes.

Work only in the private folder you are given. Do not use the web or any other file.
