# old_select_v3 — the R28 selection, rejudged

The 500 old cases chosen in R28 (`selection.jsonl`: 1,947 questions, ids `OLD-<original id>`). They were given new gold with exactly the train_v4 (R26) judge setup, and reviewed against the v3 rules. Nothing in the states or questions was rewritten, and no record was dropped. No benchmark was opened.

## Files

| File | What it is |
|---|---|
| `selection.jsonl` | the input, unchanged |
| `selection_rejudged.jsonl` | the same 500 records with the fields below |
| `stats.json` | flags, label shapes, cost |
| `qc/work/` | every judgment, every review, the batch results and the cost ledger |
| `pipeline/rejudge.py`, `pipeline/finalize_flags.py` | the code |

Each record in `selection_rejudged.jsonl` has:

- the new `gold`;
- `meta.judgments` (all three);
- `meta.judge_setup`;
- `meta.contested`;
- `meta.v3_flags`, with `meta.v3_flags_withdrawn` alongside;
- `meta.old_gold`, kept for comparison.

## How

- **Gold:** three Claude Haiku 5.5 judgments per record: careful_operator, by_the_book and generalist, all at effort medium. They use the train_v4 judge prompt and personas (`independent_v7/pipeline/records.py`), each in a separate Batch API request.
  - The judges never see the old gold.
  - The records have no role field, so the role given to the judges is "a reviewer who handles records in <domain>".
  - Gold is the plain mean of the three, rounded to 4 decimals and never sharpened.
- **Review:** one Claude Sonnet 5.5 request per record (Batch API), separate from the judges. It lists v3-rule problems only, with one code per problem:
  - `excluded_setting` (R22.1, including procurement, tenders and billing);
  - `not_answerable`;
  - `mixed_dimensions` (a scale or an option set that blends two quantities);
  - `malformed` (a statement or its true/false descriptions do not cover every case).
- **Withdrawn flags:** 9 flags contradicted themselves, because their own note says there is no problem (for example "not one of the excluded settings"). They were moved to `meta.v3_flags_withdrawn` so they do not drop good records; nothing else was changed.

## Flags

- **230 of 500 records have at least one flag; 270 have none** (1038 questions). Unflagged by source: {'v1_7': 258, 'train_v3': 6, 'score_aug': 6}.
- **Records by code:**
  - mixed dimensions: 121;
  - excluded or close setting: 84;
  - a question not answerable from the record: 60;
  - malformed statement: 36.
- **Where the flags fall:** 84 flags are on the whole record (excluded setting) and 236 on single questions. A record flagged on one question could be kept with that question removed, if you prefer that to dropping it.
- **Most common reasons:**
  - **Not answerable:** usually a question that needs "today" when the record gives no current date.
  - **Mixed dimensions:** urgency levels that blend how soon with how much harm, or options that are overlapping causes rather than steps on one axis.
  - **Excluded setting:** procurement or tender exports, billing disputes, and customer-care or returns queues.
- **Domain labels are unreliable.** In many excluded-setting flags the review notes that the record does not match its `domain` label (for example a utility-billing record labelled "HR absence"). The `domain` field of the old cases is therefore unreliable, including for the at-most-8-per-domain cap used in the selection.

## Label shape (R22.4.3 bands), all 500 records

| Type | Gold | Questions | top < 0.5 | 0.5–0.7 | 0.7–0.9 | ≥ 0.9 | mean top | mean entropy |
|---|---|---|---|---|---|---|---|---|
| noul | old gold | 834 | 0% | 3% | 5% | 92% | 0.931 | 0.226 |
| noul | rejudged | 834 | 0% | 5% | 13% | 81% | 0.915 | 0.256 |
| choice | old gold | 518 | 5% | 11% | 27% | 57% | 0.844 | 0.507 |
| choice | rejudged | 518 | 7% | 19% | 40% | 35% | 0.793 | 0.639 |
| score | old gold | 595 | 4% | 10% | 18% | 68% | 0.856 | 0.475 |
| score | rejudged | 595 | 5% | 17% | 51% | 27% | 0.796 | 0.627 |

Unflagged records only:

| Type | Gold | Questions | top < 0.5 | 0.5–0.7 | 0.7–0.9 | ≥ 0.9 | mean top | mean entropy |
|---|---|---|---|---|---|---|---|---|
| noul | old gold | 459 | 0% | 1% | 3% | 96% | 0.946 | 0.197 |
| noul | rejudged | 459 | 0% | 2% | 12% | 86% | 0.929 | 0.235 |
| choice | old gold | 267 | 2% | 4% | 22% | 72% | 0.887 | 0.419 |
| choice | rejudged | 267 | 2% | 12% | 40% | 46% | 0.843 | 0.544 |
| score | old gold | 312 | 4% | 9% | 14% | 72% | 0.86 | 0.465 |
| score | rejudged | 312 | 6% | 15% | 46% | 34% | 0.806 | 0.604 |

## What this means

- **The rejudged gold is softer than the old gold, but still much sharper than R22.4.3 and train_v4.**

  | Type | Rejudged mean top | R22.4.3 target | train_v4 |
  |---|---|---|---|
  | true/false | 0.915 | 0.75–0.81 | 0.80 |
  | choice | 0.793 | 0.62–0.68 | 0.61 |
  | score | 0.796 | 0.58–0.64 | 0.68 |

- **The judges agree with the old top answer 97% of the time, and disagree among themselves on only 5% of questions** (train_v4: 19%).
- **Why:** the old cases were written to be settled, with case-specific questions and decisive facts. The same judges give soft gold only where the record is genuinely balanced, so rejudging changes the confidence but not the cases.
- **For the planned comparison:** these records add mostly clear-cut questions next to train_v4's softer ones.

## Cost

$1.9 in total (judging $0.42, review $1.48; 2000 Batch API requests), on the team's API key (cap $10).
