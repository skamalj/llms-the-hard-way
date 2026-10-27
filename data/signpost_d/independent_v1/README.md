# signpost_independent

An independent evaluation and training set of typed decision cases in the System One format, built on request for the Signpost-D team on 27 October 2026 by the external reviewer (Claude Fable 5.1 orchestrating the pipeline below). Everything in it is invented: organisations, people, places, policies, reference numbers. Nothing was taken from the Typed Decisions benchmark (no cases, labels, workflow names, field names or wording; the train split was never read for this work), from any other dataset, or from the web.

## Files

| File | Cases | Purpose |
|---|---:|---|
| `shift_dev.jsonl` | 408 | selection set: every model, data and epoch choice can be made on it |
| `sealed_test.jsonl` | 209 | use once, for the final model; about half of it comes from six domains that appear in no other file (airline ground ops, tenancy disputes, payroll, customs brokerage, museum loans, sports league) |
| `train.jsonl` | 418 | training data, if wanted |
| `stats.json` | | the counts below, per split |
| `qc/per_labeller_author_and_check.jsonl` | | per question: each labelling call's probabilities, the question writer's own answer (never used for the gold), and the checking pass's verdict |
| `qc/review_sample_*.md` | | 50 cases rendered for a human read, flagged cases first (sealed test excluded) |
| `pipeline/` | | the seed list, the three briefs, the runner, the assembler and the validator, so the set can be audited or regenerated |

Ids are `R-nnnn` and carry no information about the split. Each line has `id`, `state` (text or a JSON object), `questions` (3–6, keyed `q1`…), `gold` (probabilities keyed exactly as the criteria, in criteria order, summing to 1) and `meta`.

## How the cases were made

The pipeline has four separate stages, each a separate model call with its own brief. The briefs were written for this set without sight of the team's briefs or labelling instructions. They are in `pipeline/prompts.py`.

1. **Seed.** A seed is sampled from a list of 44 invented domains × the deciders in that domain × 10 document kinds (email thread, chat log, form submission, system record export, policy extract with case note, incident report, meeting notes, statement with cover note, handwritten log transcription, voicemail with CRM note) × 1–3 complications (a corrected figure, an exception clause far from the facts, a figure that must be derived, a missing field, an approximate figure, a cross-midnight or month-end gap, mixed units, distractor numbers, two conflicting accounts, working-day deadlines, a threshold the facts land close to, a chatty style) × a clarity target (mostly clear 45%, mixed 35%, mostly debatable 20%). `pipeline/seeds.py`.
2. **Document.** `claude-haiku-5-5` writes the document with no questions in mind: just the material, as it would exist, with the complications built in and nothing explained or resolved. JSON records are about 30% of cases.
3. **Questions.** `claude-sonnet` (a different model from the document writer) writes 3–6 typed questions about the document: noul statements with true/false descriptions, choice questions with 2–6 snake_case options and meanings, score questions with 3–5 ordered levels written "Name: description". Rules enforced by script and regenerated on failure: at least one compare question (two when there are five or more questions), at most two judge questions, and option descriptions that do not quote any multi-digit figure appearing in the document (so descriptions define the condition without showing the working). The writer also records its own best answer, which is stored in `qc/` and is **never** used for the gold.
4. **Labelling.** Four separate calls per case, each seeing only the document and the questions (choice option order shuffled per call) and nothing from the writer: three `claude-haiku-5-5` personas (a literal reader, a practical operator, a cautious auditor) and one `claude-opus` analyst. Each returns a probability per option; the gold is the plain mean of the four, renormalised. The question writer's model (Sonnet) never labels. The labelling instructions, in brief: use only the document plus common sense; commit when the document settles the answer; spread probability when it does not (missing, approximate or contradictory information); keep score mass on one or two adjacent levels; no commentary.
5. **Checking pass** (at the team's request after the pilot). For read, compare and infer questions only, one `claude-opus` call per case works the answer out (arithmetic, date and working-day counting, unit conversion, rule-with-exception) without writing its working out, and reports whether the document settles the question. Where it says settled with confidence ≥ 0.9, the gold is corrected to 0.92 on the verified option with the remaining 0.08 spread over the other options in proportion to the labellers' mean. Judge questions are never touched. `meta.verified` records settled / open / not_checked per question and `meta.gold_adjusted_by_check` whether the correction changed the top answer or sharpened a soft one. Where the checker overrode a confident labeller majority the case carries `meta.flags`; those cases head the review sample.

Models are named as the Claude CLI resolves them on 27 October 2026 (`haiku` → claude-haiku-5-5; `sonnet` and `opus` → the current Sonnet and Opus). Per-call cost is recorded in `qc/`.

## Meta fields

`domain`, `form` (text / json), `doc_kind`, `decider`, `clarity_target`, `complications` (the seed's list; the writer was asked to build them in, not guaranteed to appear), `kinds` per question (read / compare / infer / judge), `labellers` (4), `top_answer_agreement` per question (how many of the four calls agreed on the top option), `verified`, `gold_adjusted_by_check`, `clear_cut` (top ≥ 0.85), and `flags` where present. `source` is the same for every case: two-step model-written. No case is template-filled.

## Counts

### shift_dev

- 408 cases, 1833 questions (4.49 per case)
- Types: noul 844, choice 554, score 435
- Kinds: read 45 (2%), compare 704 (38%), infer 601 (33%), judge 483 (26%)
- Form: text 290, JSON record 118
- Gold: mean top probability 0.798; by kind {"compare": 0.89, "infer": 0.85, "judge": 0.589, "read": 0.917}; clear (top ≥ 0.85) 1126 vs mixed 707
- Labeller agreement on the top answer (of 4 calls): {"2": 83, "3": 181, "4": 1569}
- Checking pass: {"settled": 994, "open": 356, "not_checked": 483}; gold corrected on 72 questions; 0 cases carry a flag
- State length (words, JSON serialised for records): median 293, p10 156, p90 469
- Document kinds: {"chat log": 37, "email thread": 26, "form submission": 36, "handwritten log transcription": 25, "incident report": 27, "meeting notes": 35, "policy extract and case note": 32, "statement with cover note": 32, "system record": 118, "voicemail and CRM note": 40}

### sealed_test

- 209 cases, 962 questions (4.6 per case)
- Types: noul 447, choice 295, score 220
- Kinds: read 43 (4%), compare 374 (39%), infer 300 (31%), judge 245 (25%)
- Form: text 146, JSON record 63
- Gold: mean top probability 0.798; by kind {"compare": 0.883, "infer": 0.854, "judge": 0.583, "read": 0.906}; clear (top ≥ 0.85) 589 vs mixed 373
- Labeller agreement on the top answer (of 4 calls): {"2": 49, "3": 95, "4": 818}
- Checking pass: {"settled": 520, "not_checked": 245, "open": 197}; gold corrected on 35 questions; 0 cases carry a flag
- State length (words, JSON serialised for records): median 280, p10 168, p90 465
- Document kinds: {"chat log": 19, "email thread": 20, "form submission": 18, "handwritten log transcription": 18, "incident report": 14, "meeting notes": 9, "policy extract and case note": 12, "statement with cover note": 14, "system record": 63, "voicemail and CRM note": 22}

### train

- 418 cases, 1861 questions (4.45 per case)
- Types: noul 857, choice 557, score 447
- Kinds: read 55 (3%), compare 706 (38%), infer 617 (33%), judge 483 (26%)
- Form: text 305, JSON record 113
- Gold: mean top probability 0.792; by kind {"infer": 0.845, "compare": 0.89, "judge": 0.57, "read": 0.895}; clear (top ≥ 0.85) 1132 vs mixed 729
- Labeller agreement on the top answer (of 4 calls): {"2": 99, "3": 217, "4": 1545}
- Checking pass: {"settled": 1007, "not_checked": 483, "open": 371}; gold corrected on 78 questions; 0 cases carry a flag
- State length (words, JSON serialised for records): median 299, p10 152, p90 479
- Document kinds: {"chat log": 41, "email thread": 32, "form submission": 30, "handwritten log transcription": 40, "incident report": 37, "meeting notes": 30, "policy extract and case note": 30, "statement with cover note": 39, "system record": 113, "voicemail and CRM note": 26}


Total pipeline cost: about $104.98 across all calls.

## Known limits

- All writers and labellers are Claude models, as agreed with the team; the independence comes from separate briefs, a different writer model from the team's (Haiku and Sonnet rather than Opus), the two-step construction, the seed list, and a Haiku-weighted labelling mix. Haiku's documents sometimes contain small internal inconsistencies (a weekday that does not match the date, for instance); these are left in, because real documents have them, and the labellers and the checking pass see the same text the model under test sees.
- The gold is model opinion averaged over four calls plus the checking pass; it is not ground truth. Judge questions in particular are soft by design (mean top around 0.65) and should be read as a distribution, not a key.
- Complications listed in `meta.complications` are instructions to the writer, not verified properties of the document.
- Length: states are longer than the team's own cases (median about 300 words); the 1,536-token limit noted in R2 of the review page may truncate some JSON records.
- No human has read every case. The review sample in `qc/` is the place to start if a human check is wanted.

## Licence

Released to the Signpost-D team without restriction (CC0). Please keep this README with the files.
