# thanos_v9 — the user's own voice throughout, the user's lines weighted

| Split | Rows | Notes |
|---|---|---|
| train | 2,145 (1,665 unique) | the user's own lines ×2 (480 → 960 rows), 1,085 restyled earlier targets, 100 new handwritten pairs |
| validation_daily | 24 | the user's everyday held-out set: early stopping and main score (unchanged) |
| validation | 25 | earlier curated interpretive set: reference only (unchanged) |
| test | 25 | inputs unchanged; targets restyled as below |

**Sources of the unique training rows:**

| Source | Rows | Notes |
|---|---|---|
| user's file of 500 (`d500_*`, new) | 411 | |
| user's file of 75 (`d75_*`) | 69 | |
| restyled earlier targets: generated (v4) | 396 | |
| restyled earlier targets: generated (v7) | 248 | |
| restyled earlier targets: user's file of 150 | 141 | |
| restyled earlier targets: thanos_v3 | 100 | |
| handwritten | 300 | h001–h200 restyled, plus the new h201–h300 |

**What changed from v8** (`build_v9.py`):

1. **The user's 500 daily examples** (`raw/user_daily_500.json`):
   - 69 rows are the file of 75 already in v8.
   - 13 are excluded as too close to a protected sentence: the user's five manual-test sentences, two near-copies of them, and six validation or test sentences.
   - 7 garbled or nonsensical template rows are dropped (`DROP`), e.g. "I'll finish finish the report after the lunch.", "Can we move the meeting to the meeting?".
   - 3 rows replace older rows with the same input (`SUPERSEDED`).
   - The remaining 411 were fact-checked by a subagent (22 minimal fixes, `raw/d500_verdicts.jsonl`), plus two overrides of mine (`REVIEW`).
2. **The restyle:** three rewriter subagents pushed the other targets towards the user's moves (`raw/rewrite_brief.md`: the situation as subject, a pause before a closing clause, a mood clause). Three validators checked facts, fixed readability, and **thinned "…" to about 1 target in 5**, because the user's own 500 lines use it rarely and the set should read as one author. The result is the user's measured, formal voice, not a more theatrical one. One override (`RESTYLE_REVIEW`).
3. **Handwritten h201–h300** (`raw/handwritten_pairs_3.jsonl`), in the same voice.
4. **Weighting:** the user's own lines appear twice in train (`WEIGHT = 2`); duplicates carry ids like `d500_017#2`.

**Checks** (all pass):
- no digits, no banned clichés ("bank balance" allowed), no target equal to its input;
- no new input equal to a training input or close to a protected sentence (word overlap < 0.5);
- "…" appears in 239 of 1,665 unique targets.
