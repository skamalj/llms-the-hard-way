# thanos_v8 — one dramatic Thanos voice throughout

| Split | Rows | Notes |
|---|---|---|
| train | 1,157 | same inputs as thanos_v7; 1,088 targets rewritten in the dramatic voice, 69 from the user's own file of 75 kept as written |
| validation_daily | 24 | the user's everyday held-out set: **early stopping and the main score** |
| validation | 25 | the earlier curated interpretive set: a reference score only |
| test | 25 | same inputs; targets rewritten in the dramatic voice |

**Why.** v7 mixed three voices (light rewording from v3/v4, strict handwritten h001–h200, the user's everyday grand style). The user asked for one dramatic voice, and set the bar:

> "We're throwing Tom a farewell dinner on Friday, but he doesn't know yet."
> → "We shall gather on Friday to honor Tom with a farewell feast… yet he remains unaware of what awaits him."

The bar means: reshape the sentence; use grand verbs and a personified situation; let a closing phrase grow out of the input; keep every fact; use "…" rarely, at a natural turn. The lines from the user's file of 75 (`d75_*`, by the same author) already meet it and are kept.

**How** (`build_v8.py`):

1. A first, milder rewrite (mostly "…" and "shall" added) was rejected.
2. **Second pass:**
   - **Rewriters:** three subagents rewrote 1,113 targets (the 1,088 non-`d75` training targets and the 25 test targets) from the inputs to the bar (`raw/pass2_brief.md`, `raw/pass2_out_*.jsonl`).
   - **Validators:** three more subagents checked facts strictly and lifted any flat target (`raw/pass2_verdicts_*.jsonl`). Fixes per batch:

     | Batch | for drama | for facts |
     |---|---|---|
     | 1 | 49 | 1 |
     | 2 | 83 | 1 |
     | 3 | 32 | 4 |

     The test set: 7 fixes, all for drama; the facts were already right.
   - **My review:** automated checks and samples (below).

**Checks** (all pass):
- no target contains a digit, a banned cliché (inevitable, destiny, universe, balance, …), or equals its input;
- no "…" end echoes; "…" appears in 79 of 1,182 targets;
- questions kept, or turned into a polite request in 5 "…, would you?" / "Can I…?" cases;
- median word overlap between target and input is 0.38, down from about 0.6 for the first pass.

Each rewritten row keeps its v7 target as `previous_target`.

Examples:
- "Meera's parents are visiting on Sunday afternoon, not Saturday." → "Sunday afternoon shall bring Meera's parents to our door. Saturday is not their day."
- "Every promise he made, he broke." → "Every promise he made, he shattered."
- "I'm trying to drink less coffee, but it's hard." → "I seek to loosen coffee's hold upon me, yet the struggle is a hard one."
