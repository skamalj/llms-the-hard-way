# independent_v5_score_aug — score-only augmentation (`score_aug_v1.jsonl`)

Built for `signpost_d_score_augmentation_brief.md` (30 October 2026). It is a **new augmentation version**: `v1_7` is untouched. Every question is `type: "score"`, four per case, in the same System One format and metadata as the earlier deliveries. Ids are `SCORE-F<flow>-<nnnn>`, and `meta.flow` / `meta.flow_name` name the flow. Everything is invented: nothing is copied, paraphrased or derived from the Typed Decisions benchmark, its test cases, workflows, schemas or field names, and no web content is used.

**Accepted: 409 cases / 1636 score questions** against the target of 500 / 2,000. Short of 100: F1 (73), F2 (67), F3 (76), F4 (93); see Rejections.

## Files

| File | Purpose |
|---|---|
| `score_aug_v1.jsonl` | the accepted cases |
| `manifest.json` | flows, counts, models and calls, versions |
| `stats.json` | everything in section 5 of the brief, overall, by flow and per-flow acceptance |
| `qc/per_labeller_author_check_validator.jsonl` | per question: each labelling call, the writer's own answer and intended level, the arithmetic check, the validator's verdict, issue and note |
| `qc/rejections.jsonl` | every rejected case with its reason (and the validator's per-question notes) |
| `qc/review_sample_50.md` | 10 random accepted cases per flow, rendered for a human read |
| `pipeline/` | seeds, briefs, runner, gold rule, assembler, validator, this README writer |

## Method: the train_v2 pipeline with five flows

| Stage | Model | Calls |
|---|---|---|
| Document | Haiku (claude-haiku-5-5) | 1 per case, from a flow-specific document brief |
| Questions | Sonnet (claude-sonnet-5-5) | 1 per case, up to 3 if the script rejects the set |
| F2 twin document | Haiku | 1 per twin: the base document with one decisive fact changed |
| Labelling | three Haiku personas (literal reader, operator, auditor) + one Opus analyst (claude-opus-5-5) | 4 per case, averaged |
| Arithmetic check | Opus | 1 per case, read / compare / infer questions only |
| Score-scale validation | Opus | 1 per case, every question |

Each call is a separate headless Claude Code CLI call: no tools, no MCP, no settings, no session persistence, exactly as in train_v2's runner. The question writer never labels; its own answers are in `qc/` only. Labellers never see the writer's answers, each other's answers or the intended level.

- **Gold:** train_v2's rule, unchanged (`pipeline/gold.py`). It is the mean of the four calls. Where the arithmetic check settles a read / compare / infer question with confidence ≥ 0.9, the checked level gets 0.92 and the rest is spread in proportion to the labellers' mean. Judge questions are exactly as labelled, never sharpened or flattened.
- **Seeds:** each seed fixes the flow, the number of levels per question (drawn 40 / 35 / 25 for 3 / 4 / 5), a kind per question (flow-specific mixes that average about 20 / 22 / 25 / 33 read / infer / compare / judge), and an *intended* level per question, drawn uniformly over the scale. The intended level only steers the writer, so that low, middle and high answers all occur; the gold comes only from the labellers. JSON records are weighted to about half of the states. Domains, document kinds and complications are train_v2's; none of the six sealed-test domains, and nothing from the R17 / `independent_v3` pipeline, was used.
- **Flow briefs** (`pipeline/seeds.py`, `FLOWS`): each flow adds a paragraph to the document brief (what evidence the document must contain) and to the question brief (what the scales must do).
  - **F2:** explicit inclusive/exclusive edges placed just below, at or above the document's value.
  - **F3:** any weighting between conflicting criteria is stated.
  - **F4:** the scale states how missing evidence is treated. Either it rates how well the evidence supports a conclusion, with level 0 = not enough evidence, or it applies an explicit rule for the missing part. "Low" is never conflated with "unknown".
  - **F5:** at least two multi-step calculations per set, with units, denominators, rounding and windows stated.
- **F2 twins:** odd seeds are bases. For each base, the question writer names one minimal change to a single fact that moves one named question by one level. Haiku applies it to a copy of the document, keeping everything else identical, and the twin reuses the base's questions. The twin is labelled independently: its gold comes from the labellers, not from the intended change. `meta.twin_of`, `meta.twin_change` and `meta.twin_question` record the pair.
- **Script checks** on every question set:
  - exactly four score questions with the planned numbers of levels;
  - every level written as "Name: description";
  - consistent numeric edges;
  - four distinct instructions;
  - no document figure quoted in a level description (declared edges excepted).

  A failing set is regenerated up to three times, then the case is dropped.
- **Score-scale validator** (Opus, every question, after the gold is formed): it runs the ten checks of brief section 4, plus whether a missing-evidence or weighting policy is stated where the answer depends on it. The checks are type, completeness, monotonicity, coverage, non-overlap, grounding, arithmetic, distribution validity, uncertainty and originality. Its verdict is keep or reject, with an issue category and a note, recorded in `meta.validation` and `qc/`. **A case is accepted only if all four of its questions are kept.** Rejected cases are never repaired by hand and do not count towards the target.
- **Selection:** accepted cases are taken in seed order, up to 100 per flow. Accepted cases beyond 100 are left out and counted as surplus.

## Acceptance by flow

| Flow | Name | Seeds run | Accepted cases | Accepted score questions | Rejected cases | Validator question reject rate | Surplus |
|---|---|---|---|---|---|---|---|
| F1 | Evidence-based scoring | 130 | 73 | 292 | 57 | 14% | 0 |
| F2 | Boundary and adjacent-level discrimination | 130 | 67 | 268 | 63 | 13% | 0 |
| F3 | Conflicting evidence | 200 | 76 | 304 | 124 | 22% | 0 |
| F4 | Missing, incomplete or uncertain evidence | 330 | 93 | 372 | 237 | 27% | 0 |
| F5 | Numerical and quantitative reasoning | 130 | 100 | 400 | 19 | 4% | 11 |

## Rejections

- **F1:** validator rejected 54; incomplete (labelling, check or validation call failed) 2; question set failed the script checks three times 1. Validator rejections by issue (questions): overlap 25, coverage 15, monotonicity 7, weighting 7, uncertainty 5, grounding 4, distribution 4, arithmetic 2, type 1, missingness_policy 1, completeness 1.
- **F2:** validator rejected 57; question set failed the script checks three times 2; twin document not produced 3; incomplete (labelling, check or validation call failed) 1. Validator rejections by issue (questions): overlap 22, coverage 19, weighting 11, grounding 7, distribution 4, missingness_policy 1, uncertainty 1, originality 1.
- **F3:** validator rejected 115; question set failed the script checks three times 1; incomplete (labelling, check or validation call failed) 8. Validator rejections by issue (questions): overlap 66, weighting 23, grounding 20, coverage 14, monotonicity 11, uncertainty 10, missingness_policy 9, distribution 7, type 4, arithmetic 3, originality 2.
- **F4:** validator rejected 206; question set failed the script checks three times 31. Validator rejections by issue (questions): overlap 164, coverage 118, distribution 13, monotonicity 12, uncertainty 6, missingness_policy 4, arithmetic 3, grounding 3, type 1.
- **F5:** validator rejected 18; question set failed the script checks three times 1. Validator rejections by issue (questions): overlap 10, distribution 7, weighting 2, grounding 2.

The validator is strict on purpose. Most rejections are scales whose neighbouring levels could both fit the same facts (overlap) or that leave a plausible state with no level (coverage). Those are exactly the defects the brief rules out. F4 (missing evidence) has the highest rejection rate, because writing a scale that is monotone, gap-free and explicit about missingness is the hardest of the five tasks. Raising the number of seeds was preferred to loosening the validator.

## Balance and quality (brief section 5)

- **Questions by scale size:** 3 levels 683 (42%), 4 levels 531 (32%), 5 levels 422 (26%).
- **Gold top level by scale size:** {"3": {"0": 223, "1": 245, "2": 215}, "4": {"0": 113, "1": 132, "2": 153, "3": 133}, "5": {"0": 67, "1": 92, "2": 98, "3": 84, "4": 81}}. By position: lowest 403, middle 804, highest 429. Every level, including the extremes and the middle levels, is the gold answer for many questions.
- **Gold top probability:** mean 0.872; below 0.85 for 20% of questions; bins {"<0.55": 46, "0.55-0.70": 106, "0.70-0.85": 172, "0.85-0.95": 1285, ">=0.95": 27}.
- **Labeller top-answer agreement of 4:** {"2": 11, "3": 52, "4": 1573}.
- **States:** JSON 191, text 218; median 284 words (p10 172, p90 472); 50 domains.
- **Kinds:** read 374 (23%), infer 390 (24%), compare 419 (26%), judge 453 (28%), against the suggested 20 / 20 / 25 / 35.
- **Arithmetic check:** {"settled": 1093, "open": 90, "not_checked": 453}; gold corrected (relabelled) on 35 questions.
- **Numeric questions with a computed value:** margin bands {"close": 344, "moderate": 347, "far": 280}; computations {"stated": 160, "sum": 51, "share": 170, "rate": 33, "time_gap": 146, "aggregate": 103, "difference": 143, "average": 23, "change": 85, "ratio": 37, "conversion": 20}.
- **Duplicates:**
  - near-duplicate state pairs (5-gram Jaccard ≥ 0.5, twins excluded): 0;
  - exact duplicate instructions (twins excluded): 0;
  - near-duplicate instruction pairs across cases: 0;
  - median similarity within a twin pair: 0.962 (one fact changed, as intended).

### By flow

| Flow | Cases | Levels 3 / 4 / 5 | Gold top lowest / middle / highest | Mean top | Top < 0.85 | Agreement 4 / 3 / ≤2 of 4 | JSON / text | Read / infer / compare / judge |
|---|---|---|---|---|---|---|---|---|
| F1 | 73 | 124 / 96 / 72 | 79 / 144 / 69 | 0.879 | 17% | 282 / 10 / 0 | 40 / 33 | 157 / 55 / 14 / 66 |
| F2 | 67 | 106 / 82 / 80 | 53 / 128 / 87 | 0.888 | 13% | 262 / 4 / 2 | 22 / 45 | 21 / 49 / 128 / 70 |
| F3 | 76 | 127 / 102 / 75 | 77 / 165 / 62 | 0.778 | 51% | 265 / 31 / 8 | 42 / 34 | 32 / 72 / 33 / 167 |
| F4 | 93 | 154 / 128 / 90 | 89 / 188 / 95 | 0.886 | 19% | 367 / 5 / 0 | 43 / 50 | 104 / 93 / 41 / 134 |
| F5 | 100 | 172 / 123 / 105 | 105 / 179 / 116 | 0.913 | 3% | 397 / 2 / 1 | 44 / 56 | 60 / 121 / 203 / 16 |

## Notes and limits

- **Judge share:** judge questions are below the suggested 35% because the validator rejects judge scales more often (their level boundaries are harder to make non-overlapping). The kinds are the question writer's labels.
- **Gold:** it is model opinion averaged over four calls plus the arithmetic check, not ground truth. Where the document leaves neighbouring levels open, the gold stays spread.
- **F2 twins:** both halves of a pair are accepted only if both pass the validator independently. A twin whose partner was rejected keeps `twin_of` and is marked `twin_partner_missing`.
- **Seed order:** the seed lists are fixed (base seed 20261030), and later seeds only extend them. Seeds run per flow: {"F1": 130, "F2": 130, "F3": 200, "F4": 330, "F5": 130}.
- **Before training:** run `pipeline/validate.py` (schema, probabilities, score-only, flow id) and compare v1_7 against v1_7 + this set with everything else held constant, as the brief's section 6 says. No benchmark test content was used to write, label, filter or tune this set.

Cost (as reported by the CLI): about $61.62 for the accepted cases, and about $138 for the whole run, including rejected cases and a top-up batch for F1–F4 that was stopped before labelling. That batch contributes no cases here.

## Licence

Released to the Signpost-D team without restriction (CC0).
