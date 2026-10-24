# Signpost-D: format validation (System One)

You are checking training data against a published decision format. Read `format_spec.md` (in the same folder as this file) first. It is the standard, and you apply it **exactly**.

Your task is **only the format**: whether every question is a correct System One question whose gold matches it. Do not re-judge whether the answers are right, unless a fix changes a question's meaning.

## Your input

One JSON object per line, in System One form: `id`, `state`, `questions` (`{qid: {type, instructions, criteria}}`), `gold` (`{qid: {type, probabilities}}`), and `meta`. Ignore `meta`.

A script has already checked:
- the field names;
- the label and level counts;
- that no description is empty;
- that labels are unique;
- that the gold's keys and sums are right.

You check what needs reading.

## Check every question, every case

### noul
1. Can the instruction be answered exactly true or false from the state? It must be a closed question ("Has the payment arrived?") or a statement ("The payment has arrived."). It must not be an open question, or two questions in one.
2. **Polarity.**
   - `true` must be the affirmative answer to the instruction as written.
   - The `true` description must say what makes the answer true, and the `false` description what makes it false.
   - A swapped or inverted pair is an error. Examples: the instruction asks "Is the order late?" while the `true` description reads "The order arrived on time"; or the instruction contains a negation ("Has the tenant not paid?") whose descriptions do not follow it.
3. The gold `true` probability must be the probability of the affirmative answer to the instruction as written.

### choice
4. Every label is a distinct, real option, and its description says what choosing it means. No two labels may mean the same action, and no label may cover another.
5. The gold has one value per label.

### score
6. **Order.**
   - The levels run strictly from the **lowest** to the **highest** end of one dimension. Level `"0"` is the least of the quantity the instruction asks about: least serious, urgent, likely, large, good or well.
   - Error: a scale written highest first.
   - Error: a scale that is not monotone, for example "Low, Critical, Medium".
   - Error: levels that mix two dimensions.
7. Each level string, `"Name: description"`, makes sense on its own, without the other levels.
8. The gold indices follow the criteria order.

### every question
9. The instruction is self-contained and answerable from the state alone.
   - It must not refer to "the options above", "the previous question", or another question's answer.
   - An instruction that names one of its own options ("Should the order be held or released?") is fine.

## Verdicts

Write a line **only for a question that needs a fix**:

```json
{"id": "G01-004", "qid": "q3", "verdict": "fix", "rule": 6,
 "note": "Levels ran Critical -> Low; reversed so level 0 is Low",
 "question": {"type": "score", "instructions": "…", "criteria": ["Low: …", "Medium: …", "High: …", "Critical: …"]},
 "gold": {"type": "score", "probabilities": {"0": 0.05, "1": 0.15, "2": 0.6, "3": 0.2}}}
```

- **`question`:** the complete corrected question in System One form, with exactly `type`, `instructions` and `criteria`.
- **`gold`:** the complete corrected gold, keyed as the spec requires.
- **When the meaning does not change** (reordering, a reworded label, swapped descriptions): carry the same probabilities over to the right keys. If you reverse a scale, reverse the gold. If you correct swapped `noul` descriptions without changing the instruction, the gold stays as it is.
- **When the meaning changes** (for example, you must reword an instruction to make it a closed question): set the gold yourself from a careful reading of the state, and say so in `note`.
- **Keep the type and the question id.** Change as little as possible: never edit the state.

## Before you finish

Check your output with a script:
- every line parses;
- the ids and qids exist in your input;
- every fixed question has exactly `type`, `instructions` and `criteria`;
- the counts are allowed: `noul` has a `true` and a `false` description; `choice` has 2–26 labels; `score` has 2–10 levels;
- the gold keys match the fixed criteria, and the values sum to 1 within 0.01.

Then report:
- how many cases and questions you checked;
- the number of fixes per rule (1–9);
- the five most notable fixes.

Work only in the private folder you are given. Do not use the web or any other file.
