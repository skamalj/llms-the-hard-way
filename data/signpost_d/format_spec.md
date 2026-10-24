# Signpost-D data format: System One (documented requirements only)

Our training data follows the published System One decision format exactly. These are the only sources used, all public documentation:

- **Typed Decisions dataset card:** `state` and `questions` together are exactly the body of a `POST /v1/systemone` request. It also gives the meaning of each type and states that option descriptions are part of the input.
- **Official scorer** (`bench/score_with_jobs.py`): what is compared with the gold, and how.
- **vLLM docs**, structured decisions, `/v1/systemone`: <https://docs.vllm.ai/en/v0.32.0/serving/online_serving/structured_decisions/>
- **LiteLLM docs**, System One format: <https://docs.litellm.ai/docs/decisions/systemone_format.md>

No benchmark case was used for this spec.

## 1. A case

```json
{"id": "G01-001",
 "state": "<string>  or  {<JSON object>}",
 "questions": {"<question id>": {"type": "...", "instructions": "...", "criteria": ...}, "...": "..."},
 "gold": {"<question id>": {"type": "...", "probabilities": {...}}},
 "meta": {"domain": "...", "form": "...", "kinds": {"<question id>": "read|infer|judge|compare"}, "validated": {...}}}
```

- `state` is a string, or JSON (sent as its JSON text). It is the only context; no outside facts are needed.
- `questions` maps a non-empty question id to a question. A question has exactly three fields: `type`, `instructions` and `criteria`. Any other field is not allowed.
- `gold` holds one distribution per question. It is our averaged labellers' distribution, after validation.
- `meta` is never shown to the model.

## 2. The three question types

| type | `instructions` | `criteria` | gold `probabilities` keyed by |
|---|---|---|---|
| `noul` | a **statement** (a declarative sentence, not a question) that is true or false of the state | an object with `"true"` and `"false"` descriptions | `"true"`, `"false"` |
| `choice` | the question | an object mapping each label to its description; labels unique; 2–26 labels | the labels |
| `score` | the question | an ordered list of levels, **lowest first**; 2–10 levels; each level a self-contained string, `"Name: what puts a situation at this level"` | level indices as strings, `"0"` (lowest) … `"n-1"` |

The documents allow the following. Our data uses the stricter form:

| The documents allow | Our data uses |
|---|---|
| `noul` with no criteria, or only one of `true` / `false` | both, because option descriptions are part of the input |
| choice descriptions that are `null` | always a description |
| score levels given as bare names | `"Name: description"` |

Meaning of the answers:

- **`noul`:** the probability that the statement is true (the card's definition). The scorer treats an engine's `yes` as `true` and `no` as `false`. Our items are always statements ("There is still stock in chiller 3."), never yes/no questions ("Is any stock still in chiller 3?"): a question is answered yes or no, a statement is true or false.
- **`choice`:** a probability for every label.
- **`score`:** a probability for every level. The expected level, the sum over i of i × p(i), is what an engine reports as `score`. Level 0 must be the low end of the scale.

## 3. How the gold is compared

The official scorer does the following:

1. Normalises the predicted probabilities over the gold's keys.
2. Computes four measures:
   - **accuracy:** the predicted argmax equals the gold argmax;
   - **KL(gold ‖ pred):** predictions are floored at 1e-9;
   - **Brier:** the sum of squared differences;
   - **ECE:** 10 bins over the confidence of the predicted top option.

The card adds: "Report KL or log loss and Brier next to accuracy; calibration is the point."

## 4. What a validator checks for every question

These are the documented requirements a script cannot fully check.

1. **noul:**
   - The instruction is a statement (not a question) that is exactly true or false of the state.
   - `true` means the statement as written is true.
   - The `true` description says what makes the answer true, and the `false` description says what makes it false. Neither may be swapped or inverted.
2. **choice:**
   - Every label is a real, distinct option.
   - Every description says what choosing that label means.
   - Labels are unique; neither labels nor descriptions differ only in case or punctuation.
3. **score:**
   - The levels run strictly from the lowest to the highest end of one dimension.
   - Level 0 is the lowest; "lowest" means least of the quantity the instruction asks about: least serious, least likely, least urgent, smallest.
   - Each level string makes sense on its own.
4. **Every question:**
   - The instruction is self-contained and answerable from the state alone.
   - It does not refer to "the options below" or to other questions.
5. **Gold:**
   - Keys exactly match the criteria: labels, `true`/`false`, or `"0"`…`"n-1"` in criteria order.
   - Values sum to 1.
   - The gold agrees with the question as finally worded. If a fix changes the meaning, the gold must be re-set.
