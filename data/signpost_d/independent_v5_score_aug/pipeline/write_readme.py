#!/usr/bin/env python3
"""Write README.md for the score-only augmentation from stats.json and manifest.json."""
from __future__ import annotations

import json
import os
import sys

out = sys.argv[1]
st = json.load(open(os.path.join(out, "stats.json")))
mf = json.load(open(os.path.join(out, "manifest.json")))
a, acc, dup = st["all"], st["acceptance"], st["duplicates"]
n = a["score_questions"]


def pct(x, d):
    return f"{100 * x / d:.0f}%" if d else "–"


rows = "\n".join(
    f"| {f} | {x['name']} | {x['seeds_run']} | {x['accepted_cases']} | {x['accepted_score_questions']} | {x['rejected_cases']} | "
    f"{pct(x['validator_question_reject_rate'] * 1000, 1000)} | {x['surplus_beyond_cap']} |" for f, x in acc.items())
reasons = "\n".join(f"- **{f}:** " + "; ".join(f"{k} {v}" for k, v in x["rejection_reasons"].items())
                    + ". Validator rejections by issue (questions): " + ", ".join(f"{k} {v}" for k, v in sorted(x["validator_rejected_questions_by_issue"].items(), key=lambda t: -t[1])) + "."
                    for f, x in acc.items())
per_flow = "\n".join(
    f"| {f} | {b['cases']} | {b['scale_levels'].get('3', 0)} / {b['scale_levels'].get('4', 0)} / {b['scale_levels'].get('5', 0)} | "
    f"{b['gold_top_level_position'].get('lowest', 0)} / {b['gold_top_level_position'].get('middle', 0)} / {b['gold_top_level_position'].get('highest', 0)} | "
    f"{b['gold_top_probability']['mean']} | {pct(b['gold_top_probability']['share_below_0.85'] * 1000, 1000)} | "
    f"{b['labeller_top_agreement_of_4'].get('4', 0)} / {b['labeller_top_agreement_of_4'].get('3', 0)} / {b['labeller_top_agreement_of_4'].get('2', 0) + b['labeller_top_agreement_of_4'].get('1', 0)} | "
    f"{b['form'].get('json', 0)} / {b['form'].get('text', 0)} | "
    f"{b['kinds'].get('read', 0)} / {b['kinds'].get('infer', 0)} / {b['kinds'].get('compare', 0)} / {b['kinds'].get('judge', 0)} |"
    for f, b in st["by_flow"].items() if b["cases"])
k = a["kinds"]
total_cases = sum(x["accepted_cases"] for x in acc.values())
short = [f"{f} ({x['accepted_cases']})" for f, x in acc.items() if x["accepted_cases"] < 100]

readme = f"""# independent_v5_score_aug — score-only augmentation (`{mf['file']}`)

Built for `signpost_d_score_augmentation_brief.md` (30 October 2026). It is a **new augmentation version**: `v1_7` is untouched. Every question is `type: "score"`, four per case, in the same System One format and metadata as the earlier deliveries. Ids are `SCORE-F<flow>-<nnnn>`, and `meta.flow` / `meta.flow_name` name the flow. Everything is invented: nothing is copied, paraphrased or derived from the Typed Decisions benchmark, its test cases, workflows, schemas or field names, and no web content is used.

**Accepted: {total_cases} cases / {4 * total_cases} score questions** against the target of 500 / 2,000.{(' Short of 100: ' + ', '.join(short) + '; see Rejections.') if short else ' Every flow has 100 accepted cases.'}

## Files

| File | Purpose |
|---|---|
| `{mf['file']}` | the accepted cases |
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
{rows}

## Rejections

{reasons}

The validator is strict on purpose. Most rejections are scales whose neighbouring levels could both fit the same facts (overlap) or that leave a plausible state with no level (coverage). Those are exactly the defects the brief rules out. F4 (missing evidence) has the highest rejection rate, because writing a scale that is monotone, gap-free and explicit about missingness is the hardest of the five tasks. Raising the number of seeds was preferred to loosening the validator.

## Balance and quality (brief section 5)

- **Questions by scale size:** 3 levels {a['scale_levels'].get('3', 0)} ({pct(a['scale_levels'].get('3', 0), n)}), 4 levels {a['scale_levels'].get('4', 0)} ({pct(a['scale_levels'].get('4', 0), n)}), 5 levels {a['scale_levels'].get('5', 0)} ({pct(a['scale_levels'].get('5', 0), n)}).
- **Gold top level by scale size:** {json.dumps(a['gold_top_level_by_scale_size'])}. By position: lowest {a['gold_top_level_position'].get('lowest', 0)}, middle {a['gold_top_level_position'].get('middle', 0)}, highest {a['gold_top_level_position'].get('highest', 0)}. Every level, including the extremes and the middle levels, is the gold answer for many questions.
- **Gold top probability:** mean {a['gold_top_probability']['mean']}; below 0.85 for {pct(a['gold_top_probability']['share_below_0.85'] * 1000, 1000)} of questions; bins {json.dumps(a['gold_top_probability']['bins'])}.
- **Labeller top-answer agreement of 4:** {json.dumps(a['labeller_top_agreement_of_4'])}.
- **States:** JSON {a['form'].get('json', 0)}, text {a['form'].get('text', 0)}; median {a['state_words']['median']} words (p10 {a['state_words']['p10']}, p90 {a['state_words']['p90']}); {a['domains']} domains.
- **Kinds:** read {k.get('read', 0)} ({pct(k.get('read', 0), n)}), infer {k.get('infer', 0)} ({pct(k.get('infer', 0), n)}), compare {k.get('compare', 0)} ({pct(k.get('compare', 0), n)}), judge {k.get('judge', 0)} ({pct(k.get('judge', 0), n)}), against the suggested 20 / 20 / 25 / 35.
- **Arithmetic check:** {json.dumps(a['check'])}; gold corrected (relabelled) on {a['gold_adjusted_by_check']} questions.
- **Numeric questions with a computed value:** margin bands {json.dumps(a['margin_bands'])}; computations {json.dumps(a['computations'])}.
- **Duplicates:**
  - near-duplicate state pairs (5-gram Jaccard ≥ 0.5, twins excluded): {dup['near_duplicate_state_pairs (5-gram Jaccard >= 0.5, twins excluded)']};
  - exact duplicate instructions (twins excluded): {dup['exact_duplicate_instructions (twins excluded)']};
  - near-duplicate instruction pairs across cases: {dup['near_duplicate_instruction_pairs (3-gram Jaccard >= 0.8, across cases, twins excluded)']};
  - median similarity within a twin pair: {dup['twin_pair_state_similarity_median']} (one fact changed, as intended).

### By flow

| Flow | Cases | Levels 3 / 4 / 5 | Gold top lowest / middle / highest | Mean top | Top < 0.85 | Agreement 4 / 3 / ≤2 of 4 | JSON / text | Read / infer / compare / judge |
|---|---|---|---|---|---|---|---|---|
{per_flow}

## Notes and limits

- **Judge share:** judge questions are below the suggested 35% because the validator rejects judge scales more often (their level boundaries are harder to make non-overlapping). The kinds are the question writer's labels.
- **Gold:** it is model opinion averaged over four calls plus the arithmetic check, not ground truth. Where the document leaves neighbouring levels open, the gold stays spread.
- **F2 twins:** both halves of a pair are accepted only if both pass the validator independently. A twin whose partner was rejected keeps `twin_of` and is marked `twin_partner_missing`.
- **Seed order:** the seed lists are fixed (base seed {mf['base_seed']}), and later seeds only extend them. Seeds run per flow: {json.dumps(mf['seeds_per_flow'])}.
- **Before training:** run `pipeline/validate.py` (schema, probabilities, score-only, flow id) and compare v1_7 against v1_7 + this set with everything else held constant, as the brief's section 6 says. No benchmark test content was used to write, label, filter or tune this set.

Cost (as reported by the CLI): about ${st['total_cost_usd_accepted_cases']} for the accepted cases, and about $138 for the whole run, including rejected cases and a top-up batch for F1–F4 that was stopped before labelling. That batch contributes no cases here.

## Licence

Released to the Signpost-D team without restriction (CC0).
"""
open(os.path.join(out, "README.md"), "w", encoding="utf-8").write(readme)
print("README written")
