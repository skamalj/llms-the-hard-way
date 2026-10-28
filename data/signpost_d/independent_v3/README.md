# signpost_independent_v3 — a referee set from a third pipeline

Evaluation-only set built on request for the Signpost-D team (R17, 28 October 2026) by the external reviewer (Claude Fable 5.1 orchestrating the pipeline below). It exists so that the team has a selection set whose makers, briefs, labellers and domains overlap with neither their own training data nor the two earlier deliveries (`signpost_independent`, `signpost_independent_v2`), which now sit in their training mix. **Do not train on it.**

Everything is invented: organisations, people, places, policies, reference numbers. Nothing comes from the Typed Decisions benchmark (no cases, labels, workflow names, field names or wording; the train split was never read for this work), from any other data set, or from the web. The zero-shot rules of R12 apply.

## Files

| File | Purpose |
|---|---|
| `shift_dev_v2.jsonl` | 440 cases, ids `W-nnnn` (never colliding with `R-` or `V-`), assigned after a shuffle so the id says nothing about the seed |
| `stats.json` | the counts below |
| `qc/per_labeller_author_and_check.jsonl` | per item: each of the five labelling calls' probabilities, the item writer's own answer (never used for the gold), the arithmetic check's verdict and computed value, the models used and the cost |
| `qc/review_sample_50.md` | 50 cases rendered for a human read, cases flagged by the check first |
| `pipeline/` | the seed list, the four briefs, the runner, the driver, the assembler and the validator |

Each line has `id`, `state` (text or a JSON object), `questions` (3–6, keyed `q1`…), `gold` (probabilities keyed exactly as the criteria, in criteria order, summing to 1) and `meta`. The format is the System One format used in the two earlier deliveries.

## How it differs from the earlier pipelines

| | team's own data | `signpost_independent` / `_v2` | **this set** |
|---|---|---|---|
| document writer | Opus (whole case) | Haiku | **Opus**, fresh brief |
| question writer | Opus (whole case) | Sonnet | **Fable**, fresh brief; never labels |
| labelling calls | Opus, Sonnet, Fable | 3 × Haiku personas + 1 × Opus | **3 × Sonnet stances + 1 × Haiku + 1 × Opus**, five new stances |
| checking pass | – | Opus on read / compare / infer | **Opus on compare / infer only**; read and judge left as labelled |
| domains | theirs | 44 / 50 (56 distinct) | **40 new**, none shared with any earlier file |
| document kinds | theirs | 10 kinds, single-record JSON | **11 rewritten kinds**, two JSON shapes (sheet export with rows; nested service response) |
| question mix | natural | natural / weighted to computed score | **natural: ~40% true-false, ~35% choice, ~25% score**, compare ≥ 25%, judge ≤ 2 per case |

The four briefs in `pipeline/prompts.py` were written from scratch for this set; none is adapted from an earlier brief. The seed list (`pipeline/seeds.py`) is a new draw with a new base seed, new domains, deciders, matters, document kinds, complications, locales and name pools.

## How the cases were made

1. **Seed.** 40 domains × their deciders × 12 matters (a request to approve, a complaint about a charge, an incident, a booking change, an invoice query, an inspection result, a rota clash, eligibility, a damage claim, lateness, a renewal or cut-off, a count that does not match) × 11 document kinds × 1–3 complications from a list of 14 (a superseded figure, a rule that applies only to a category stated elsewhere, a quantity spread over several lines, a date given by weekday or relative phrase, a figure promised and never supplied, a percentage and an amount on different bases, two units, one reference used twice, two records that disagree, a cut-off time, a total that does not add up, the deciding detail in a postscript, rounded versus exact, an earlier similar case with its own numbers) × a settledness target (mostly settled 50%, some open points 30%, largely a matter of judgement 20%) × a locale × a question composition drawn per seed at 40 / 35 / 25.
2. **Document.** `claude-opus` writes the paperwork with no questions in mind: raw material only, nothing explained, nothing flagged. JSON states are about a quarter of cases.
3. **Items.** `claude-fable` writes the exact composition the seed fixes: true/false statements (noul), choice questions with snake_case options, score scales of 3–5 ordered levels; each with a kind (read / compare / infer / judge). Rules enforced by script, with regeneration on failure: the composition; at least ⌈n/4⌉ compare items; at most two judge; descriptions that do not quote multi-digit figures from the document (reference numbers, clock times, dates and years excepted); no duplicate items. The writer's own answer is stored in `qc/` and never used.
4. **Labelling.** Five separate calls per case, each seeing only the document and the items (choice options shuffled per call) and nothing from the writer: `claude-sonnet` as a desk clerk, as a team lead and as the applicant's advocate; `claude-haiku` as an outsider with no trade knowledge; `claude-opus` as a second reader re-checking every figure. Each returns a probability per option; the gold is the plain mean of the five, renormalised.
5. **Arithmetic check.** For compare and infer items only, one `claude-opus` call per case works out the answer (arithmetic, dates, units, ordering, a rule with its exceptions) without writing its working out and says whether the document settles it. Where it says settled with confidence ≥ 0.9, the gold is corrected to 0.90 on the checked option with the remaining 0.10 spread over the other options in proportion to the labellers' mean. Read and judge items are never touched. `meta.verified` records settled / open / not_checked per item; `meta.gold_adjusted_by_check` whether the correction changed the top answer or sharpened a soft one; `meta.flags` lists items where the check overrode a labeller majority (those cases head the review sample).

Models are named as the Claude CLI resolved them on 28 October 2026: `claude-opus-5-5`, `claude-fable-5-1`, `claude-sonnet-5-5`, `claude-haiku-5-5`. Per-call models and costs are in `qc/`.

## Meta fields

`domain`, `form` (text / json), `doc_kind`, `decider`, `matter`, `settledness_target`, `complications` (instructions to the writer, not verified properties), `locale`, `kinds` per item, `labellers` (5), `labeller_models`, `top_answer_agreement` per item (how many of the five calls put their top probability on the gold's top option), `verified`, `gold_adjusted_by_check`, `clear_cut` (gold top ≥ 0.85), `flags` where present, and `source`.

## Counts

- 440 cases, 1938 items (4.4 per case; cases by item count {"3": 84, "4": 155, "5": 140, "6": 61})
- Types: noul 799 (41%), choice 666 (34%), score 473 (24%)
- Kinds: read 397 (20%), compare 806 (42%), infer 279 (14%), judge 456 (24%)
- Form: text 331, JSON 109
- Settledness targets: {"some open points": 146, "mostly settled": 213, "largely a matter of judgement": 81}
- Gold: mean top 0.881; by kind {"compare": 0.937, "read": 0.956, "judge": 0.707, "infer": 0.897}; by type {"noul": 0.947, "score": 0.779, "choice": 0.874}; clear (top ≥ 0.85) 1495 vs mixed 443
- Labeller top-answer agreement of 5: {"1": 1, "2": 22, "3": 39, "4": 124, "5": 1752}
- Arithmetic check: {"settled": 941, "not_checked": 853, "open": 144}; gold corrected on 117 items; 0 cases flagged
- State length (words; JSON serialised): median 407, p10 340, p90 493
- Document kinds: {"booking ledger extract": 37, "committee paper": 28, "control room log": 36, "fee schedule and query": 40, "inspection checklist": 36, "job sheet": 41, "letter and file note": 32, "service response": 52, "sheet export": 57, "shift handover sheet": 35, "text message exchange": 46}
- Domains (40): allotment society, amateur dramatics society, auction house, bicycle courier co-op, blood donation centre, boarding kennels, botanic garden seed bank, campsite, canal navigation authority, community food bank, community radio station, coworking space, crane hire, dental surgery, driving school, escape room venue, ferry terminal, film location office, funeral directors, household recycling centre, ice rink, laundrette chain, lift maintenance firm, microbrewery, mountain rescue team, music exam board, optician, pest control firm, phone repair shop, podcast studio, riding stables, ski lift operations, small harbour office, street market, student housing co-op, tattoo studio, tree surgery contractor, tyre fitting branch, vineyard estate, zoo animal section

Total pipeline cost: about $154.05.

## Known limits

- All writers and labellers are Claude models, as agreed. The independence from the earlier sets comes from different models in every role, separate briefs, a Sonnet-led labelling mix with new stances, and disjoint domains, kinds and seeds; it is not independence from the Claude family.
- The gold is model opinion averaged over five calls plus the arithmetic check; it is not ground truth. Judge items are soft by design and should be read as distributions.
- Opus writes longer and denser documents than Haiku did (median about 407 words); a model with a short context limit may truncate some states.
- Fable's items lean harder than the earlier sets' (more compare, fewer plain read items), so absolute scores are not comparable across the three deliveries; rankings are what this set is for.
- No human has read every case. `qc/review_sample_50.md` is the place to start.

## Licence

Released to the Signpost-D team without restriction (CC0). Keep this README with the file.
