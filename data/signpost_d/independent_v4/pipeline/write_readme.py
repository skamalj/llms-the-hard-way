#!/usr/bin/env python3
"""Write README.md for the v3 training set (signpost_independent_v4, R19) from stats.json."""
from __future__ import annotations

import json
import os
import sys

out = sys.argv[1]
batch_note = sys.argv[2] if len(sys.argv) > 2 else ""
st = json.load(open(os.path.join(out, "stats.json")))
s = st["train_v3"]
n = s["questions"]
bk, bt = s["by_kind"], s["by_type"]
mb = s["margin_bands"]
cm = s["clear_vs_mixed"]


def pct(x, d):
    return f"{100 * x / d:.0f}%" if d else "–"


readme = f"""# signpost_independent_v4 — train_v3: training set aimed at multi-level computed score and multi-option choice questions

Fourth delivery for the Signpost-D team, requested in R19 (29 October 2026). Training only: there is no dev or test file. Built with the **train_v2 pipeline** (`signpost_independent_v2/pipeline/`, copied here and changed only where listed below) and a fresh seed draw. {batch_note}

Everything is invented; nothing comes from the Typed Decisions benchmark, any other data set or the web (R12 rules).

## Files

| File | Purpose |
|---|---|
| `train_v3.jsonl` | {s['cases']} cases, ids `X-nnnn` (never colliding with `R-`, `V-` or `W-` ids) |
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

- {s['cases']} cases, {n} questions ({s['questions_per_case']} per case)
- Types: score {bt.get('score', 0)} ({pct(bt.get('score', 0), n)}), choice {bt.get('choice', 0)} ({pct(bt.get('choice', 0), n)}), noul {bt.get('noul', 0)} ({pct(bt.get('noul', 0), n)})
- Kinds: compare {bk.get('compare', 0)} ({pct(bk.get('compare', 0), n)}), infer {bk.get('infer', 0)} ({pct(bk.get('infer', 0), n)}), judge {bk.get('judge', 0)} ({pct(bk.get('judge', 0), n)}), read {bk.get('read', 0)} ({pct(bk.get('read', 0), n)})
- Score levels: {json.dumps(s['score_levels'])}; choice options: {json.dumps(s['choice_options'])}
- Score deciders: {json.dumps(s['score_decider'])}
- Computed score questions with a margin: {json.dumps(s['computations'])}
- Margin bands (realised, checking pass's value where given): close {mb.get('close', 0)}, moderate {mb.get('moderate', 0)}, far {mb.get('far', 0)}
- Form: text {s['by_form'].get('text', 0)}, JSON record {s['by_form'].get('json', 0)}
- Gold: mean top {s['mean_gold_top']}; by kind {json.dumps(s['mean_gold_top_by_kind'])}; clear (top ≥ 0.85) {cm.get('clear (top>=0.85)', 0)} vs mixed {cm.get('mixed', 0)}
- Checking pass: {json.dumps(s['verification'])}; gold corrected on {s['gold_adjusted_by_check']} questions; {s['cases_with_flags']} cases flagged
- Labeller top-answer agreement of 4: {json.dumps(s['labeller_top_agreement_of_4'])}
- State length (words): median {s['state_words']['median']}, p10 {s['state_words']['p10']}, p90 {s['state_words']['p90']}
- Document kinds: {json.dumps(s['doc_kinds'])}

Cost (as reported by the CLI): about ${st['total_cost_usd']}.

## Notes and limits

- Kinds are the question writer's labels under the rules above; re-bucket from `meta.computed` and `meta.score_decider` if you prefer another convention.
- The gold is model opinion averaged over four calls plus the checking pass, not ground truth; judge questions should be read as distributions.
- The checking pass is a model; where its computed value and the writer's differ, `value_source` records which one the margin uses.
- Haiku documents occasionally contain small inconsistencies (a weekday that does not match its date); they are left in.

## Licence

Released to the Signpost-D team without restriction (CC0). Keep this README with the file.
"""
open(os.path.join(out, "README.md"), "w", encoding="utf-8").write(readme)
print("README written")
