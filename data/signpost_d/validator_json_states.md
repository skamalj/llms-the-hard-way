# Signpost-D: record-like states as JSON (System One `state`)

Read `format_spec.md` (in this folder) first. A System One `state` is either a string or JSON. Most of our states are text. Your job is to convert states that are already **records written as text**, forms or checklists and tables, into **JSON**, the way a real system would store them. Nothing may be lost or added.

## Rules

1. **Every fact is kept, and nothing is added.**
   - Every name, number, unit, currency, date, time, status, flag and code is kept.
   - So is every free-text note or comment. A note becomes a string field, such as `"note"` or `"comments"`, word for word.
   - Never compute, summarise, round or infer a value. If the text says "Total: 112", the JSON has `"total": 112`, even if the rows add up to something else; a mismatch may be the point of a question.
2. **The shape:**
   - **A form or checklist** (field: value lines) becomes an object. Group related fields into nested objects where a real system would (`"patient": {...}`, `"appointments": [...]`).
   - **A table** becomes an object holding a list of row objects, one per row, with the column names as keys: `{"shift_log": [{"shift": "A", "units": 412, ...}, ...]}`. A title, caption or notes under the table become fields of the outer object.
   - Any lines of text before or after the record (a heading, a policy line, a note) go in as string fields such as `"policy"` or `"note"`, word for word.
3. **Field names** are short and `snake_case`, as a real system would use (`received_qty`, `due_date`, `status`).
4. **Values** take their natural JSON type: numbers as numbers (with units kept in the key or as a separate field, never lost), true/false as booleans, a missing value as `null`. Dates and times stay exactly as written, as strings.
5. **The questions and the gold stay as they are.**
   - Read every question of the case. If a question still makes sense with the JSON state, do nothing to it.
   - If it refers to the text layout ("the third row of the table", "the checklist above"), reword only that reference so it fits the JSON, without changing the meaning. Give the reworded question as a separate fix line (see Output).
6. If a state can't be converted without losing or bending its meaning, don't convert it. Report it instead.

## Output

One line **per case** you were given:

```json
{"id": "G02-014", "verdict": "convert", "note": "form -> object",
 "state": {"...": "..."}}
```

or `{"id": …, "verdict": "report", "note": "<why>"}`.

Where a question needs rewording, add a line in the usual fix format, with the gold unchanged:

```json
{"id": "G02-014", "qid": "q3", "verdict": "fix", "rule": 9, "note": "refers to the JSON fields instead of 'the form'",
 "question": {"type": "...", "instructions": "...", "criteria": "..."}, "gold": {"type": "...", "probabilities": {}}}
```

Before you finish, check by script:
- every input case has exactly one convert or report line;
- every `state` is a JSON object or list, not a string;
- **every number in the original text state appears in your JSON**: compare the multisets of digit sequences, and explain any difference in `note`;
- every question fix keeps its type, criteria keys and gold exactly.

Then report:
- the counts of converts, reports and question fixes;
- every report, with its reason;
- three examples, before and after.

Work only in the private folder you are given. Do not use the web or any other file.
