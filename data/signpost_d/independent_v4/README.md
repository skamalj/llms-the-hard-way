# signpost_independent_v4 — train_v3: training set aimed at multi-level computed score and multi-option choice questions

Fourth delivery for the Signpost-D team, requested in R19 (29 October 2026). Training only: there is no dev or test file. Built with the **train_v2 pipeline** (`signpost_independent_v2/pipeline/`, copied here and changed only where listed below) and a fresh seed draw. This delivery: 1008 cases (the first batch of 1,000 that R19 asked for).

Everything is invented; nothing comes from the Typed Decisions benchmark, any other data set or the web (R12 rules).

## Files

| File | Purpose |
|---|---|
| `train_v3.jsonl` | 1008 cases, ids `X-nnnn` (never colliding with `R-`, `V-` or `W-` ids) |
| `stats.json` | the counts below |
| `qc/per_labeller_author_and_check.jsonl` | per question: each labelling call's probabilities, the writer's own answer and declared edges (never used for the gold), the checking pass's verdict and computed value |
| `qc/review_sample_50.md` | 50 cases rendered for a human read |
| `pipeline/` | seeds, briefs, runner, assembler, validator for this run |

## Models and calls (unchanged from train_v2)

| Stage | Model | Calls per case |
|---|---|---|
| Document | Haiku (claude-haiku-5-5), effort low | 1 |
| Questions | Sonnet (claude-sonnet-5-5), effort low | 1 (up to 3 if the script rejects the set) |
| Labelling | three Haiku personas (literal reader, operator, auditor) + one Opus analyst (claude-opus-5-5) | 4, averaged |
| Checking pass | Opus, read / compare / infer only, effort high | 1 |

Each call is a separate headless Claude Code CLI call (`claude -p`, no tools, no MCP, no settings, no session persistence), exactly as in train_v2's `run.py`. The question writer never labels; its own answers are stored in `qc/` only. The labellers never see the writer's answers or each other's. The gold rule is train_v2's: the mean of the four labelling calls; where the checking pass settles a read / compare / infer question with confidence ≥ 0.9, gold 0.92 on the checked option with the rest spread in proportion to the labellers' mean. Judge questions are exactly as labelled.

## R19 guard: shift_dev_v2 (R17 pipeline) kept clean

- **No part of the R17 pipeline was used.** Documents are Haiku, questions Sonnet (not Opus documents / Fable questions); labelling is train_v2's three Haiku personas + Opus analyst (not the R17 five-stance mix); briefs, prompts, document kinds, complication list and JSON shape are train_v2's, with the R19 additions below. The R17 pipeline folder (`signpost_independent_v3/`) was never opened or checked out by the agent that built this set: only `independent_v2/pipeline` was read.
- **Domains:** only the 50 train_v2 domains (listed in `pipeline/seeds.py`); none of the six sealed-test domains (airline ground ops, tenancy disputes, payroll, customs brokerage, museum loans, sports league), and no new domains, so none of the R17 domains can appear.
- **Nothing from R17 cases:** no R17 document or question was seen, reused or paraphrased. Every document here is new.
- **Fresh seeds:** base seed 20261029 (train_v2 used 20261027), ids `X-nnnn`.

## What changed from train_v2 (R19)

1. **Composition per seed.** About 45% score, 40% choice, 15% true/false (true/false in about 72% of sets, one question). Score questions get 3–5 levels drawn 1:2:2, so about 80% have 4–5 levels; choice questions get 3–5 options drawn the same way.
2. **Score deciders.** Each score question is computed (rate, share, time gap, difference, sum, average) or, in about one in six, **rule-decided** (`computation: "rule"`: the level is the outcome of a stated rule whose exception decides between adjacent levels; no edges, no margin). Stated-value band questions are now rare (8% of seeds, down from 20%), as R19 reports bands nearly solved.
3. **Margins.** The requested band is weighted 55% close / 25% moderate / 20% far, because the writer lands the requested band only about a third of the time; `margin` and `margin_band` describe the realised value from the checking pass.
4. **Date and time gaps.** About 62% of seeds use a time gap as one of their two computations (about a third of computed score questions), and each such seed names one form: working days over a weekend, dates by weekday or relative phrase, a gap across midnight, a deadline to the minute or second, mixed time formats, or a gap across a month end.
5. **Choice questions.** Each choice question has a pattern the document must support with 4–5 alternatives carrying their own figures and conditions: cheapest after each one's adjustment, the only candidate meeting every condition, the earliest feasible slot, the highest or lowest computed rate / total / average, or a rule with an exception. The document brief gains one paragraph asking for that material (without comparing or ranking it); the question brief says choice questions are not direct lookups.
6. **Kinds target** given to the writer: about 40% compare, 35% infer, 20% judge, rest read; a choice decided by working out and comparing a figure per option is compare, one decided by conditions or a rule with an exception is infer, and rule-decided score questions are infer.
7. **Script checks** added to train_v2's: the numbers of score levels and choice options must match the seed's plan. All train_v2 checks are kept unchanged (composition, edges, computed questions present, at least 30% compare, at most two judge, no document figures quoted in descriptions except declared edges).
8. **Metadata.** As train_v2, plus `meta.score_decider[q]` (the computation, `rule` or `stated`).

## Counts

- 1008 cases, 4845 questions (4.81 per case)
- Types: score 2180 (45%), choice 1919 (40%), noul 746 (15%)
- Kinds: compare 2625 (54%), infer 1483 (31%), judge 713 (15%), read 24 (0%)
- Score levels: {"3": 431, "4": 895, "5": 854}; choice options: {"3": 389, "4": 707, "5": 823}
- Score deciders: {"difference": 252, "average": 259, "share": 199, "time_gap": 550, "rate": 252, "stated": 80, "sum": 232, "rule": 356}
- Computed score questions with a margin: {"difference": 252, "average": 259, "share": 199, "time_gap": 550, "rate": 252, "stated": 80, "sum": 232}
- Margin bands (realised, checking pass's value where given): close 976, moderate 496, far 352
- Form: text 701, JSON record 307
- Gold: mean top 0.864; by kind {"compare": 0.898, "judge": 0.797, "infer": 0.837, "read": 0.901}; clear (top ≥ 0.85) 3739 vs mixed 1106
- Checking pass: {"settled": 3091, "not_checked": 713, "open": 1041}; gold corrected on 288 questions; 0 cases flagged
- Labeller top-answer agreement of 4: {"2": 104, "3": 272, "4": 4469}
- State length (words): median 304, p10 211, p90 466
- Document kinds: {"chat log": 79, "email thread": 84, "form submission": 75, "handwritten log transcription": 60, "incident report": 80, "meeting notes": 89, "policy extract and case note": 79, "statement with cover note": 72, "system record": 307, "voicemail and CRM note": 83}

Cost (as reported by the CLI): about $138.5.

## Notes and limits

- **Kinds miss the requested mix:** compare 54% against about 40%, infer 31% against 35%, judge 15% against 20%, read 0% against 5%. These are the question writer's own labels under the convention above. Because most score and choice questions in this set work out a figure and compare it, the writer labels them compare, and the at-most-two-judge rule from train_v2 keeps judge below 20%. train_v2 had the same tilt. Re-bucket from `meta.computed` and `meta.score_decider` if you prefer another convention: a computed question that also applies a rule is the closest thing to "infer", and every `rule` score question is infer.
- **Dropped seeds and top-up:** 77 of seeds X0001–X1000 failed the question-set checks three times and were dropped, as in train_v2. To get back to about 1,000 cases, seeds X1001–X1090 (the same fixed seed list, continued) were run; 85 of them came through. Ids therefore run to X-1090 with gaps.
- **Pilot:** seeds X0001–X0020 were run first as a pilot with the same code and kept unchanged.
- The gold is model opinion averaged over four calls plus the checking pass, not ground truth; judge questions should be read as distributions.
- The checking pass is a model; where its computed value and the writer's differ, `value_source` records which one the margin uses.
- Haiku documents occasionally contain small inconsistencies (a weekday that does not match its date); they are left in.

## Licence

Released to the Signpost-D team without restriction (CC0). Keep this README with the file.
