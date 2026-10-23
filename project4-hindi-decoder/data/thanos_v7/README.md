# thanos_v7 — thanos_v6 + 459 everyday pairs in the user's style

| Split | Rows | From |
|---|---|---|
| train | 1,157 | thanos_v6 train (698) + 248 generated + 211 from the user's files |
| validation | 25 | thanos_v6 (the curated interpretive set), unchanged |
| test | 25 | thanos_v6, unchanged |
| **validation_daily** | 24 | **new**: the user's held-out everyday examples (`thanos_lingo_validation_examples_25.md`), less one input already in training |

**Style.** Everyday, conversational inputs (running late, food, chores, phones, work, family, weather) rewritten in a grave, formal voice, as in the user's five examples (`raw/style_examples.md`): "I'm running 10 minutes late. Please start without me." → "I have been delayed by ten minutes. Proceed without me… do not wait." Looser than the handwritten v5/v6 pairs: a second clause may add a mood ("when the path permits"), never a fact; "…" pauses are common.

**How it was made** (`build_v7.py`):

1. **Generation:** a Claude subagent wrote 250 pairs (`raw/generated_pairs_2.jsonl`, g001–g250).
2. **The user's files:** `thanos_lingo_test_dataset.md` (150) and `thanos_lingo_daily_examples_75.md` (75), parsed into `raw/user_pairs.jsonl` (215 rows). The 5 sentences that open both files are the user's **manual end-of-run test**, so they are excluded from all training.
3. **Validation:** a second subagent judged all 465 pairs (`raw/verdicts.jsonl`):

   | | pass | fix | drop |
   |---|---|---|---|
   | generated | 243 | 7 | 0 |
   | user file of 150 | 32 | 111 | 2 (duplicate inputs) |
   | user file of 75 | 53 | 17 | 0 |

   The file of 150 needed most fixes: objects turned into riddles ("mastication substance" for gum), numbers and times dropped ("one hundred unread emails" → "a mountain of decrees"), and cosmic clichés ("destiny", "balance", "Perfectly balanced"). The fixes restore the fact and keep the grandeur.
4. **My review:** read every fix and the passes; one override (`REVIEW`: u150_137, whose fix added "the journey halts"). Excluded (`EXCLUDE`): three pairs close to a validation_daily sentence, and g076 (the same input as the user's d75_039).

**Checks** (all pass): no duplicate inputs; no target equals its input, contains a digit, or uses a banned cliché; no new input resembles a validation, test, validation_daily, demo or manual-test sentence (word overlap < 0.5).

The notebooks do not read `validation_daily` yet.
