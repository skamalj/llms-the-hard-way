# Rewording number questions (wording only)

Each case below is a situation (`state`) with questions that a script wrote about it. The script's answers are exact, but its wording is clumsy ("The units is more than 44.", "after the billed of the plan"). Your job is to **reword each question so it reads naturally, as a careful professional in that field would write it, without changing what it asks.** You never answer the questions and never change an answer.

## Your input

One JSON object per line: `id`, `state`, `questions` (System One form: `noul` statements with `true` / `false` descriptions, `choice` labels with descriptions, `score` levels lowest first), and `fields`: for each question, the state's field paths it is about and the template that built it (`threshold`, `twohop`, `ratio`, `difference`, `dates`, `extreme`, `band`).

## Rules

1. **Same meaning, same answer.** The reworded question must be true or false (or pick the same option or level) in exactly the same situations as the original. Keep the comparison and its direction ("more than", "at least", "below", "more than N days after").
2. **Keep every limit exactly:** every number, percentage, day count and date written in the original question stays, written the same way.
3. **Refer to fields by their meaning in the situation, never by their key or path.** No `snake_case` keys, no dotted paths, no brackets, no backticks. Use what the field means there: "the electrician's call-out fee", "the reserve fund balance", "the date the customer asked for the refund".
4. **Never add the answer or the deciding value.** Do not write the field's actual value, and do not add a calculation or a hint.
5. **Keep each type's form.**
   - `noul`: the instruction stays a statement ending with a full stop, never a question. Reword the `true` and `false` descriptions to match it; together they still cover every case.
   - `choice`: keep every label **exactly** as it is (character for character); you may reword the instruction and the descriptions.
   - `score`: keep the number of levels, their order and every threshold number; reword the instruction (it names the quantity: "How large is …", "How high is …") and the text of each level as `"Name: description"`.
   - `twohop` questions identify a row by one of its own values ("the entry whose sku is K-22"): keep that identifying value exactly; you may phrase it naturally ("For item K-22, …").
6. **Plain, varied wording.** Do not start every question the same way.
7. If a question cannot be reworded faithfully (the field's meaning is unclear from the situation), leave it out of your output; the script's wording will be kept.

## Output

One JSON object per case, one per line, in input order, with only the questions you reworded:

```json
{"id": "U-G09-009", "questions": {"q1": {"type": "noul", "instructions": "…", "criteria": {"true": "…", "false": "…"}},
                                  "q3": {"type": "score", "instructions": "…", "criteria": ["…: …", "…"]}}}
```

Work only in the private folder you are given. Before finishing, check your output by script:
- every line parses, ids are in input order and every qid exists in the input;
- every question keeps its `type`; `choice` labels are identical to the input; `score` has the same number of levels;
- every number in an original instruction appears in the reworded one;
- no reworded text contains a backtick, an underscore, a "[" or a dotted path.
