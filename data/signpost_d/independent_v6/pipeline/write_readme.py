#!/usr/bin/env python3
"""Write README.md for the R22 pilot from stats.json, qc/families.json and qc/shared_scales.json."""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design  # noqa: E402
import records as R  # noqa: E402

out = sys.argv[1]
st = json.load(open(os.path.join(out, "stats.json")))
fams = json.load(open(os.path.join(out, "qc", "families.json")))
scales_p = os.path.join(out, "qc", "shared_scales.json")
scales = json.load(open(scales_p)) if os.path.exists(scales_p) else []
gen = st["generation"]
cost = st.get("api_cost_usd", {})


def fmt(v):
    return json.dumps(v) if isinstance(v, (list, dict)) else str(v)


fam_rows = "\n".join(
    f"| {fid} | {f['domain']} | {f['role']} | {', '.join(f['skills'])} | {', '.join(f'{n} ({q['type']})' for n, q in f['questions'].items())} | {st['by_family'][fid]['records'] if fid in st['by_family'] else 0} |"
    for fid, f in fams.items())
check_rows = "\n".join(f"| {c['check']} | {fmt(c['value'])} | {fmt(c['target'])} | {'pass' if c['pass'] else '**miss**'} |" for c in st["checks"])
missed = [c for c in st["checks"] if not c["pass"]]
type_rows = "\n".join(
    f"| {t} | {v['n']} | {v['bins']['<0.5']:.0%} | {v['bins']['0.5-0.7']:.0%} | {v['bins']['0.7-0.9']:.0%} | {v['bins']['>=0.9']:.0%} | {v['mean_top']} | {v['mean_entropy']} |"
    for t, v in st["by_type"].items() if v)
MODEL_NAMES = {"opus": "Claude Opus 5.5", "sonnet": "Claude Sonnet 5.5", "haiku": "Claude Haiku 5.5"}
judges = "\n".join(f"| {p['id']} | {MODEL_NAMES[p['model']]} | {p['effort']} | {p['text']} |" for p in R.PERSONAS)
scale_txt = "\n".join(f"- `{s['name']}`: {s['instructions']} Levels: " + " / ".join(s["levels"]) for s in scales)

readme = f"""# independent_v6 — R22 pilot: decision records with honest uncertainty

Pilot for the R22 brief (Signpost-D data brief v3, 31 October 2026): **{st['records']} records in {len(fams)} families, {st['questions']} questions**. `pilot_v3.jsonl` is in System One format, one record per line, as in R22.5. Everything is invented. No benchmark was opened, read or used, and no document or question from an earlier delivery was reused. The R22.1 exclusions were applied: no AI-agent monitoring, customer support, purchasing or invoices, or security triage.

**Checks:** {st['checks_passed']} of {st['checks_total']} R22.4.3 / R22.9 checks pass. The ones that miss are listed under *Where the pilot misses the targets*. The team chose to run the pilot with the current families and report those deviations, rather than redesign first.

## Files

| File | Purpose |
|---|---|
| `pilot_v3.jsonl` | the records: `id`, `family`, `domain`, `state`, `questions`, `gold`, `meta` (`factors`, `skills`, `plan`, `judgments` (the five individual distributions), `judge_setup`, `contested`) |
| `stats.json` | every check of R22.4.3 and R22.9, overall and per family, plus generation counts and API cost |
| `qc/families.json` | the eight family specifications: role, setting, question set, latent factors, sections, rendering notes, skills |
| `qc/shared_scales.json` | the three cross-family generic scales |
| `qc/work/` | every generated record (kept or not), with its sampled and final factors and plan, every judgment, and the API cost ledger |
| `pipeline/` | the code |

## How it was made

All model calls went through the Anthropic API, billed to the team's API key. They ran in separate worker sessions, through the Python SDK, with structured outputs.

1. **Shared scales** (Claude Opus 5.5, one call): three generic 4-level scales, worded once and used identically wherever a family uses one.
{scale_txt}
2. **Families** (Claude Opus 5.5, one call per family, up to 3 attempts). Each family is designed from a slot that fixes:
   - the domain;
   - the skills its factors must exercise;
   - the type mix (1 / 2 / 2 or 2 / 1 / 2);
   - option and level counts;
   - which true/false question is bare yes/no;
   - which score question, if any, is a shared scale;
   - which score questions use "Name: description" levels.

   Code checks every R22.5 rule (word counts, "?" endings, statements, option and level counts, snake_case names, 8–14 factors, 3–6 sections, excluded settings) and sends a failing design back.
3. **Records** (Claude Sonnet 5.5, one call per record, up to 3 attempts).
   - **Code samples:** the latent factors from the family's definitions, a target length (lognormal, median 70 words, maximum 300), and a per-question plan following R22.4.2. The plan has a clarity (clear / leaning / balanced / contested), drawn with the R22.4.3 shares, and an intended top answer, drawn with the R22.4.3 position shares (true in 47.5% of true/false questions).
   - **The writer:** writes the record JSON to the plan. Where the drawn factors would contradict the plan, it may change them, and it returns the values it used. Those values are `meta.factors`; the original draw is kept in `qc/work`.
   - **Code checks:** 3–6 top-level keys, all from the family's sections; at most 320 words; and not far over the target length.
4. **Judgments:** five per record, each a separate call with no shared context. Judges see only the record, the role and the question set, never the factors, the plan or each other's answers. Each gives a full probability distribution for every question.

| Judge | Model | Effort | Stance |
|---|---|---|---|
{judges}

   Sampling temperature cannot be set on these models, so independence comes from different models and stances in separate calls. The base instruction asks for a competent person in the role reading the record once, carefully, with calibrated probabilities. It also tells judges to give mitigating evidence its weight and to treat statements as claims.
5. **Gold:** the plain mean of the five judgments, rounded to 4 decimals. It is never sharpened, smoothed or forced towards a plan.
6. **Selection:** {gen['records_planned_per_family']} records were generated per family and {gen['kept_per_family']} kept.
   - **Dropped for missing their plan** (R22.4.2 step 4): {gen['plan_miss_rule']}.
   - **Selection:** the kept records were chosen greedily so that the batch's measured statistics come as close as possible to the R22.4.3 targets. Gold values were never changed.
   - **Counts:** dropped before judging {fmt(gen['dropped_before_judging'])}; dropped for plan miss {fmt(gen['dropped_for_plan_miss'])}.

## Families

| Family | Domain | Role | Skills | Questions (type) | Records |
|---|---|---|---|---|---|
{fam_rows}

Skill shares of families: {fmt(st['skills_share_of_families'])}. Domains: {st['domains']}.

## Label shape (R22.4.3)

| Type | Questions | top < 0.5 | 0.5–0.7 | 0.7–0.9 | ≥ 0.9 | mean top | mean entropy |
|---|---|---|---|---|---|---|---|
{type_rows}

- **Contested share** (the five judges' individual top answers disagree): {st['contested_share']:.0%}.
- **Top-answer position:** score {fmt(st['score_top_position'])}; choice {fmt(st['choice_top_position'])}.
- **True/false:** `true` is top in {st['noul_true_top']:.0%}; `criteria: null` in {st['noul_criteria_null']:.0%}.
- **Score mass two or more levels from the top level:** {st['score_mass_two_or_more_from_top_mean']} on average.
- **Gold zeros:** {st['gold_zero_probabilities']}.
- **Records:** median {st['record_words']['median']} words (p10 {st['record_words']['p10']}, p90 {st['record_words']['p90']}, maximum {st['record_words']['max']}). Near-duplicate record pairs within a family: {st['near_duplicate_record_pairs']}.

## Every check

| Check | Value | Target | Result |
|---|---|---|---|
{check_rows}

## Where the pilot misses the targets

{len(missed)} checks miss. The main pattern, measured in two smoke tests before the pilot, is that **the judges' gold is softer than R22.4.3 asks for on score and choice questions**:
- Each judge individually puts only about 0.5–0.6 on its own top level of a 4- or 5-level scale, even for records written to be clear.
- Their mean therefore rarely reaches 0.7 on score questions.
- Two fixes were tried on the same records and neither moved this:
  - judge-prompt calibration anchors (score mean top 0.50 → 0.50);
  - one round of plan-guided record rewriting with the judges' measured distributions as feedback (0.50 → 0.51).
- The likely cause is the scales themselves. Several family scales combine more than one dimension (for example "substantial doubt over several tests" against "results probably invalid"), so a record can fit two neighbouring levels at once. Judges are right to split.

The same softness pushes the contested share above 40%. The record writer also often fails to make a planned-true statement read as true to sceptical judges, so `true` is top less often than the target.

Two smaller deviations:
- **Records are longer than asked.** The median is {st['record_words']['median']} words against R22.2.2's "about 70", and p90 is {st['record_words']['p90']} against about 160, although none exceeds 320. The writer adds context fields.
- **Near-duplicate pairs:** {st['near_duplicate_record_pairs']} record pairs within a family share more than half their field values; they are left in and counted here.

The team chose to run this pilot as it stands and judge it by the R22.7 model ranges. If the label shape must match R22.4.3 more closely, the fix to try next is a family redesign with one-dimensional, anchored scales (crisp level boundaries a record can sit clearly inside), followed by another smoke test.

## Cost

API cost of the pilot run: about ${cost.get('total', '?')} ({fmt(cost.get('by_model', {}))}; {cost.get('calls', '?')} calls). Earlier smoke tests on the same key cost about $9.

## Licence

Released to the Signpost-D team without restriction (CC0).
"""
open(os.path.join(out, "README.md"), "w", encoding="utf-8").write(readme)
print("README written")
