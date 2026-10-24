# Signpost-D: validators (v2.1, content and System One format)

You are checking training data for a small model that makes decisions about situations. Read these two files first; they set the standards:

- **`brief_v2.md`** sets what a good case is.
- **`format_spec.md`** sets the exact form, System One.

Each case is a `state` plus questions. Three independent labellers gave every question a probability per option, and their **average** will be the training label (`gold`). Judge by reading and working things out yourself. Do not use the web, other datasets, or any API or model.

## Your input

One JSON object per line:
- the case: `id`, `state`, `questions` in System One form;
- `labels`: each labeller's probabilities, from `opus` (cautious), `sonnet` (pragmatic) and `fable` (neutral);
- `gold`: their average;
- `look_closely`: questions you must give a verdict on, with the reason. The reasons are:
  - **sharp disagreement:** one labeller put its top answer where both others put under 0.15;
  - **low agreement:** the average's top is under 0.55;
  - **labeller note:** a labeller flagged the question.

## Check every question of every case

**Content:**
1. Is the question answerable from the state alone?
2. Are the options distinct and real?
3. Does the gold agree with a careful reading?
   - If one labeller misread or miscalculated, correct the gold.
   - If the case is genuinely mixed, keep the split.

**Format** (`format_spec.md`):
4. **`noul`:**
   - The instruction is a statement, not a question.
   - `true` and `false` together cover every case, with no gap and no overlap, including boundary values.
   - Both descriptions match the statement.
5. **`choice`:** every label has a description that says what choosing it means. No two labels mean the same action.
6. **`score`:**
   - The instruction names one quantity.
   - The levels run from the least of it (level `"0"`) to the most, on one dimension.
   - Each `"Name: description"` level makes sense on its own.
7. **Every question:** the instruction refers to nothing outside the state, such as "the options below" or another question.

## Verdicts

Write a line **for every `look_closely` question** (use `keep` if it is fine). Write a line for **any other question that needs a change**.

| verdict | when | extra fields |
|---|---|---|
| `keep` | fine as it is; for a mixed question, the split is honest | none |
| `relabel` | the question is fine, but the gold is wrong | `gold` |
| `fix` | the wording or format must change: reword the instruction or the options, without editing the state | `question`, `gold` |
| `drop` | the question can't be repaired (`"qid": "*"` drops the whole case) | none |

```json
{"id": "I1-007", "qid": "q2", "verdict": "fix", "note": "…",
 "question": {"type": "choice", "instructions": "…", "criteria": {"…": "…"}},
 "gold": {"type": "choice", "probabilities": {"…": 0.0}}}
```

- **`gold` keys:** `true`/`false` for `noul`, the labels for `choice`, `"0"`…`"n-1"` for `score`. The values sum to 1.
- **If a fix keeps the meaning,** for example a reordered scale or reworded descriptions, carry the probabilities over to the new keys.
- **If a fix changes the meaning,** set the gold yourself and say so in `note`.

Before finishing, check your output by script:
- every line parses, and every id and qid is in your input;
- every `look_closely` question has a line;
- the gold keys match the (fixed) question, and the values sum to 1 within 0.01;
- a fixed question has exactly `type`, `instructions` and `criteria`.

Then report:
- the counts per verdict;
- the five most notable problems.

Work only in the private folder you are given.
