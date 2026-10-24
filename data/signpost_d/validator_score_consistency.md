# Signpost-D: score consistency pass (System One)

Read `format_spec.md` (in this folder) first. You check only `score` questions. Each one must meet one rule exactly, which earlier validators applied unevenly:

> **The instruction names one quantity. The levels run from the least of that quantity (level `"0"`) to the most.**

## Check every score question you are given

1. **What quantity does the instruction name?** For example: how serious, how urgent, how likely, how late, how far short, how much over budget, how ready, how well, how many.
2. **If the instruction names a quantity:** level 0 must be the least of it.
   - If the levels run the other way, **reverse** the levels and the gold.
   - If the levels already fit a different quantity, you may instead **reword the instruction** to name that quantity.
3. **If the instruction is neutral and names no quantity** ("How does X compare with Y?", "Which band…", "What is the status…", "How did X change?", "What grade…", "Which tag…"): **reword the instruction** so it names the single quantity the levels rise in. Reverse the levels first if they fall.
   - A trend scale ("rising … falling sharply") measures change, from the largest fall at level 0 up to the largest rise. Alternatively, reword it to "how far has X fallen", with the levels from the smallest fall up.
   - Grades (A–D, pass/fail): the instruction names what rises. Use "how poor is the result", with level 0 the best result, or "how good is the result", with level 0 the worst. Order the levels to match.
4. **One dimension only:** every level must sit on the named quantity. A level that belongs to another dimension breaks the scale. Examples: "Too modest" on a realism scale; "Correct" sitting in the middle of an error scale, where it can only be the low end. Fix it by rewording the instruction and reordering the levels, or by rewording a level.
5. **Each level string, "Name: description", must make sense on its own.**

## Fix lines

Write a line **only when something must change**, using the format of `validator_format_instructions.md`: `id`, `qid`, `"verdict": "fix"`, `rule` (use 6), `note`, the complete corrected `question`, and the complete corrected `gold`.

- **Meaning is unchanged** (reversing, or rewording the instruction to name the quantity the levels already follow): the gold probabilities follow their levels exactly. Never invent new probabilities.
- **Meaning changes:** set the gold from a careful reading of the state, and say so in `note`.
- Keep the type and the qid, and never edit the state.

## Before you finish

Check your output by script:
- every line parses, and every id and qid exists in your input;
- every fixed question has exactly `type`, `instructions` and `criteria`, with 2–10 levels;
- the gold keys are `"0"`…`"n-1"`, and the values sum to 1 within 0.01;
- unless your note says the meaning changed, the fixed gold holds the same multiset of probabilities as the input gold.

Then report:
- how many score questions you checked;
- how many fixes there were of each kind: reversed, instruction reworded, level reworded;
- five examples.

Work only in the private folder you are given. Do not use the web or any other file.
