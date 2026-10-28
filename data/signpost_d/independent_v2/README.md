# signpost_independent_v2 — training set weighted towards computed score questions

Second delivery for the Signpost-D team, requested in R15 (28 October 2026), built with the same pipeline as `signpost_independent` (see that folder's README for the method) with the changes listed below. Training only: there is no new dev or test file. This is the complete delivery; it replaces the first batch of 1,013 cases delivered earlier (those cases are included unchanged, with the same ids).

Everything is invented; nothing comes from the Typed Decisions benchmark, any other data set or the web. The six domains reserved for the first delivery's sealed test (airline ground ops, tenancy disputes, payroll, customs brokerage, museum loans, sports league) do not appear here; twelve new domains were added (call centre QA, pharmacy dispensing, ride-share support, solar installation, freight forwarding, clinical trial site, university timetabling, wedding venue, fishing fleet, parcel locker network, theatre box office, cold-chain logistics). Every document is new; none is reused from the first delivery, and the seed list is a fresh draw.

## Files

| File | Purpose |
|---|---|
| `train_v2.jsonl` | 2085 cases, ids `V-nnnn` (never colliding with the `R-` ids of the first delivery) |
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

- 2085 cases, 10049 questions (4.82 per case)
- Types: score 4328 (43%), noul 2917 (29%), choice 2804 (28%)
- Kinds: compare 5407 (54%), infer 1781 (18%), judge 2064 (21%), read 797 (8%)
- Score questions: 4328, of which computed 3900 and stated-value band 428
- Computations: {"rate": 659, "difference": 661, "share": 658, "time_gap": 620, "average": 655, "sum": 647, "stated": 428}
- Margin bands (by the checking pass's value): close 1423, moderate 1432, far 1473
- Form: text 1455, JSON record 630
- Gold: mean top 0.872; by kind {"compare": 0.909, "infer": 0.863, "judge": 0.766, "read": 0.915}; clear (top ≥ 0.85) 8145 vs mixed 1904
- Checking pass: {"open": 1340, "settled": 6645, "not_checked": 2064}; gold corrected on 265 questions; 0 cases flagged
- Labeller top-answer agreement of 4: {"2": 132, "3": 451, "4": 9466}
- State length (words): median 258, p10 146, p90 434
- Document kinds: {"chat log": 174, "email thread": 180, "form submission": 141, "handwritten log transcription": 132, "incident report": 152, "meeting notes": 149, "policy extract and case note": 167, "statement with cover note": 180, "system record": 630, "voicemail and CRM note": 180}

Cost so far: about $251.24.

## Notes and limits

- The writer lands the *requested* margin band only about a third of the time, but the realised distribution is close to a third each, which is what matters; the `margin` and `margin_band` fields describe the realised value, computed by the checking pass, not the request.
- Kinds are the question writer's labels under the rule given to it: a computed score question whose core is working out one value and placing it against edges is "compare"; one that also applies a rule or exception is "infer". Infer therefore sits below the requested 30% and compare above 40%.
- Because most score questions are computable and the checking pass settles them, the gold is sharper than in the first delivery (mean top about 0.87 against 0.80). Judge questions are untouched and remain soft.
- The checking pass is a model; on a few questions its computed value and the writer's differ, and the file records which one the margin uses (`value_source`). Where the checker gave no value the writer's is used.
- Haiku documents occasionally contain small inconsistencies (a weekday that does not match its date); they are left in.

## Licence

Released to the Signpost-D team without restriction (CC0). Keep this README with the file.
