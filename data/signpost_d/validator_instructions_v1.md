# Signpost-D: instructions for validators

You are checking training data for a small model that makes decisions about situations. Each **case** is a situation ("state") plus 3–6 questions about it. Each question has options (yes/no, a choice, or ordered score levels). Three independent labellers gave every question a probability for each option, and their **average** will be the training label.

Your job: make sure every question is answerable, well written, and that its final label matches a careful professional reading of the situation. Judge by reading and working things out yourself. Do not use the web, other datasets, or any API or model.

Read `brief_v2.md` (in the same folder as this file) first: it is the standard the cases were written to.

## Your input

One JSON object per line. Each holds the case (`id`, `domain`, `form`, `state`, `questions`, where each question has a `kind`), then:
- `labels`: each labeller's probabilities (`opus` cautious stance, `sonnet` pragmatic stance, `fable` neutral stance);
- `average`: the label that will be used unless you change it;
- `look_closely`: questions that need your verdict, with the reason: a labeller's note, a **sharp disagreement** (one labeller put its top answer where the other two put under 0.15), or **low agreement** (the average's top is under 0.55).

## What to do

1. For **every** question in `look_closely`, write one verdict line.
2. Read every other case and question as well, more quickly. Write a line only if you find a problem: an unanswerable question, an answer given away, overlapping options, levels out of order, a wrong average.

## Verdicts

| verdict | when | extra fields |
|---|---|---|
| `keep` | the question is fine and the average is right, including genuinely mixed questions where a careful reader would honestly split | none |
| `relabel` | the question is fine but the average is wrong, e.g. one labeller misread or miscalculated, or the spread is wider or narrower than the case deserves | `label` |
| `fix` | the question is ambiguous or badly worded but can be repaired by rewording the question or its options; never edit the state | `fixed_question`, `label` |
| `drop` | the question cannot be repaired | none |

To drop a whole case, use `"qid": "*"`.

### Sharp disagreements

Work the answer out yourself.
- If the outlier misread or miscounted, `relabel`. Use roughly the two other labellers' average, or your own distribution.
- If the outlier found something the others missed, `relabel` towards the outlier.
- If the question genuinely supports both readings, `fix` it so it has one reading, or `keep` it with an honest split.

### Boundaries

Where a value sits exactly on an edge between options or levels (e.g. "48 to 72 hours" vs "more than 72 hours" at exactly 72), read the wording strictly.
- If the wording settles the question, the label should be confident.
- If the wording does not settle it, `fix` the options or levels so it does.

### Rules for a fixed question

A fixed question keeps the same `type` and `kind`, and must answer the problem in your note.
- **Options and levels:** keep the same number of options and the same names where possible.
- **Score questions:** levels still run from low to high and do not overlap.
- **Wording:** do not reveal the answer in the question.

### Rules for labels

- A label has every option or level name exactly as in the (fixed) question, in the same order.
- Its probabilities sum to 1.
- Clear-cut answers get about 0.9 or more.

## Output

Write JSON Lines, one verdict per line:

```json
{"id": "G01-003", "qid": "q2", "verdict": "relabel", "note": "Policy note: P2 for one team with a workaround; sonnet missed the workaround", "label": {"P3": 0.08, "P2": 0.9, "P1": 0.02}}
{"id": "G13-017", "qid": "q2", "verdict": "fix", "note": "Load ran 29 min 44 s; say whether a few seconds short counts", "fixed_question": {"qid": "q2", "type": "yes_no", "kind": "read", "question": "…", "options": {"yes": "…", "no": "…"}}, "label": {"yes": 0.05, "no": 0.95}}
{"id": "S02-036", "qid": "q2", "verdict": "keep", "note": "Exactly half is 'Partly' under the level wording 'half or more'"}
```

`note` is one sentence saying why.

Before you finish, check your output with a script:
- every line parses;
- every id and qid exists in your input;
- every `look_closely` question has a line;
- the label names match the question, in order, and sum to 1 within 0.01.

Work only in your private folder, given in your task. Do not write anywhere else except your output file.
