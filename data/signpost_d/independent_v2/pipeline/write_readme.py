#!/usr/bin/env python3
"""Write README.md for the v2 training set from stats.json."""
from __future__ import annotations

import json
import os
import sys

out = sys.argv[1]
batch_note = sys.argv[2] if len(sys.argv) > 2 else ""
st = json.load(open(os.path.join(out, "stats.json")))
s = st["train_v2"]
n = s["questions"]
bk, bt = s["by_kind"], s["by_type"]
mb = s["margin_bands"]
cm = s["clear_vs_mixed"]


def pct(x, d):
    return f"{100 * x / d:.0f}%" if d else "–"


readme = f"""# signpost_independent_v2 — training set weighted towards computed score questions

Second delivery for the Signpost-D team, requested in R15 (28 October 2026), built with the same pipeline as `signpost_independent` (see that folder's README for the method) with the changes listed below. Training only: there is no new dev or test file. {batch_note}

Everything is invented; nothing comes from the Typed Decisions benchmark, any other data set or the web. The six domains reserved for the first delivery's sealed test (airline ground ops, tenancy disputes, payroll, customs brokerage, museum loans, sports league) do not appear here; twelve new domains were added (call centre QA, pharmacy dispensing, ride-share support, solar installation, freight forwarding, clinical trial site, university timetabling, wedding venue, fishing fleet, parcel locker network, theatre box office, cold-chain logistics). Every document is new; none is reused from the first delivery, and the seed list is a fresh draw.

## Files

| File | Purpose |
|---|---|
| `train_v2.jsonl` | {s['cases']} cases, ids `V-nnnn` (never colliding with the `R-` ids of the first delivery) |
| `stats.json` | the counts below |
| `qc/per_labeller_author_and_check.jsonl` | per question: each labelling call's probabilities, the writer's own answer and declared edges (never used for the gold), the checking pass's verdict and computed value |
| `qc/review_sample_50.md` | 50 cases rendered for a human read, with the computed value, edges and margin band shown per score question |
| `pipeline/` | seeds, briefs, runner, assembler, validator for this run |

## What changed from the first delivery

1. **Seeds.** Each seed now fixes the question composition (score / true-false / choice counts, about 40 / 35 / 25), names two computations the document must support (rate, share of a count, time or date gap, difference, sum of 2–4 parts, average), draws a margin band per score question (close / moderate / far, one third each), and in a fifth of cases asks for one stated-value band question with uneven edges.
2. **Document brief.** Haiku must state the raw inputs for the two computations as separate facts in different places and never state the result; it must also include at least one directly stated quantity.
3. **Question brief.** Sonnet writes the composed set. Score questions are computed: the level is decided by a value the document gives only as inputs; the question never states the result; every level description states its own edges with inclusive or exclusive limits; descriptions never show the working. The writer also returns, for quality control only, the computation type, its computed value, the numeric edges and the edge rule. A script rejects sets that break the composition, have inconsistent edges, lack the computed questions, fall below 30% compare, exceed two judge questions, or quote document figures in descriptions (declared edges are allowed, since an edge may coincide with a stated limit).
4. **Checking pass.** Unchanged in method (Opus, read / compare / infer only, judge never touched), and it now also returns the computed value for a computed question. That value, not the writer's, feeds the `margin` field.
5. **Metadata.** Per computed score question, `meta.margin[q]` = computed value ÷ nearest edge (as requested) and `meta.computed[q]` carries the computation type, value, unit, edges, edge rule, relative distance to the nearest edge (`margin_rel`), its band (`close` ≤ 5%, `moderate` ≤ 25%, `far` beyond) and whether the value came from the checking pass or the writer.

Labelling is unchanged: four separate calls per case (three Haiku personas, one Opus analyst), averaged. The question writer (Sonnet) never labels.

## Counts

- {s['cases']} cases, {n} questions ({s['questions_per_case']} per case)
- Types: score {bt.get('score', 0)} ({pct(bt.get('score', 0), n)}), noul {bt.get('noul', 0)} ({pct(bt.get('noul', 0), n)}), choice {bt.get('choice', 0)} ({pct(bt.get('choice', 0), n)})
- Kinds: compare {bk.get('compare', 0)} ({pct(bk.get('compare', 0), n)}), infer {bk.get('infer', 0)} ({pct(bk.get('infer', 0), n)}), judge {bk.get('judge', 0)} ({pct(bk.get('judge', 0), n)}), read {bk.get('read', 0)} ({pct(bk.get('read', 0), n)})
- Score questions: {s['score_questions']}, of which computed {s['score_computed']} and stated-value band {s['computations'].get('stated', 0)}
- Computations: {json.dumps(s['computations'])}
- Margin bands (by the checking pass's value): close {mb.get('close', 0)}, moderate {mb.get('moderate', 0)}, far {mb.get('far', 0)}
- Form: text {s['by_form'].get('text', 0)}, JSON record {s['by_form'].get('json', 0)}
- Gold: mean top {s['mean_gold_top']}; by kind {json.dumps(s['mean_gold_top_by_kind'])}; clear (top ≥ 0.85) {cm.get('clear (top>=0.85)', 0)} vs mixed {cm.get('mixed', 0)}
- Checking pass: {json.dumps(s['verification'])}; gold corrected on {s['gold_adjusted_by_check']} questions; {s['cases_with_flags']} cases flagged
- Labeller top-answer agreement of 4: {json.dumps(s['labeller_top_agreement_of_4'])}
- State length (words): median {s['state_words']['median']}, p10 {s['state_words']['p10']}, p90 {s['state_words']['p90']}
- Document kinds: {json.dumps(s['doc_kinds'])}

Cost so far: about ${st['total_cost_usd']}.

## Notes and limits

- The writer lands the *requested* margin band only about a third of the time, but the realised distribution is close to a third each, which is what matters; the `margin` and `margin_band` fields describe the realised value, computed by the checking pass, not the request.
- Kinds are the question writer's labels under the rule given to it: a computed score question whose core is working out one value and placing it against edges is "compare"; one that also applies a rule or exception is "infer". Infer therefore sits below the requested 30% and compare above 40%.
- Because most score questions are computable and the checking pass settles them, the gold is sharper than in the first delivery (mean top about 0.87 against 0.80). Judge questions are untouched and remain soft.
- The checking pass is a model; on a few questions its computed value and the writer's differ, and the file records which one the margin uses (`value_source`). Where the checker gave no value the writer's is used.
- Haiku documents occasionally contain small inconsistencies (a weekday that does not match its date); they are left in.

## Licence

Released to the Signpost-D team without restriction (CC0). Keep this README with the file.
"""
open(os.path.join(out, "README.md"), "w", encoding="utf-8").write(readme)
print("README written")
