#!/usr/bin/env python3
"""Write README.md for independent_v7 (R26 train_v4) from stats.json, qc/families.json, qc/shared_scales.json and the ledger.

Usage: python write_readme.py OUT_DIR
"""
from __future__ import annotations

import collections
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import records as R  # noqa: E402

out = sys.argv[1]
st = json.load(open(os.path.join(out, "stats.json")))
fams = json.load(open(os.path.join(out, "qc", "families.json")))
scales = json.load(open(os.path.join(out, "qc", "shared_scales.json")))
work = os.path.join(out, "qc", "work")
gen, cost = st["generation"], st.get("api_cost_usd", {})
p2 = json.load(open(os.path.join(out, "..", "independent_v6", "stats_v3b.json"))) if os.path.exists(os.path.join(out, "..", "independent_v6", "stats_v3b.json")) else None

MODEL_NAMES = {"opus": "Claude Opus 5.5", "sonnet": "Claude Sonnet 5.5", "haiku": "Claude Haiku 5.5"}


def fmt(v):
    return json.dumps(v) if isinstance(v, (list, dict)) else str(v)


written = len(glob.glob(os.path.join(work, "records", "*.json")))
rejected = glob.glob(os.path.join(work, "records_rejected", "*.json"))
reasons = collections.Counter()
for f in rejected:
    r = json.load(open(f))["reason"]
    key = ("over 200 words" if "maximum 200" in r else "over 320 words" if "maximum 320" in r
           else "over its length target (smoke test, before the rule became a 200-word ceiling)" if "against a target" in r else "top-level keys outside the family sections" if "not among the family sections" in r
           else "more than 6 top-level sections" if "top-level sections" in r else "writer left out a record" if "no record for this key" in r
           else "record_json not valid JSON" if "not JSON" in r else r[:60])
    reasons[key] += 1
off_plan = sum(gen["dropped_for_plan_miss"].values())
kept = {fid: v["records"] for fid, v in st["by_family"].items()}
short = {fid: n for fid, n in kept.items() if n < gen["kept_per_family"]}

type_rows = []
for t in ("noul", "choice", "score"):
    v = st["by_type"][t]
    b = p2["by_type"][t] if p2 else None
    type_rows.append(f"| {t} | {v['n']} | {v['bins']['<0.5']:.0%} | {v['bins']['0.5-0.7']:.0%} | {v['bins']['0.7-0.9']:.0%} | {v['bins']['>=0.9']:.0%} | "
                     f"{v['mean_top']} | {b['mean_top'] if b else '–'} | {v['mean_entropy']} |")
fam_rows = "\n".join(f"| {fid} | {f['domain']} | {', '.join(f['skills'])} | " + "; ".join(f"`{n}` ({q['type']})" for n, q in f["questions"].items())
                     + f" | {kept.get(fid, 0)} |" for fid, f in fams.items())
scale_txt = "\n".join(f"   - `{s['name']}`: {s['instructions']} Levels: " + " / ".join(s["levels"]) for s in scales)
check_rows = "\n".join(f"| {c['check']} | {fmt(c['value'])} | {fmt(c['target'])} | {'pass' if c['pass'] else '**miss**'} |" for c in st["checks"])
judges = "\n".join(f"| {p['id']} | {MODEL_NAMES[p['model']]} | {p['effort']} | {p['text']} |" for p in R.PERSONAS)
by_stage = cost.get("by_stage", {})
reason_txt = "; ".join(f"{k}: {v}" for k, v in reasons.most_common())

readme = f"""# independent_v7 — R26 training records (`train_v4.jsonl`)

Training records in pilot 2's design (the R22 brief with the R24 changes), built as R26 asks with the cheaper pipeline.

- **Size:** {st['records']} records in {len(fams)} new families, {st['questions']} questions, ids `F201-0001` onward.
- **Format:** `train_v4.jsonl` is in System One format, one record per line, with the same fields as pilot 2.
- **Rules:** everything is invented and the R22.1 exclusions apply. No benchmark was opened, read or used. No family, question set, shared scale, record or seed is shared with pilot 1 (`independent_v6/pilot_v3.jsonl`, evaluation only) or pilot 2 (`independent_v6/pilot_v3b.jsonl`).

**Checks:** {st['checks_passed']} of {st['checks_total']} R22.4.3 / R22.9 checks pass, overall and per family. The misses are listed under *Where the set misses the targets*.

**API cost:** about **${cost.get('total', '?')}** on the team's API key, including the smoke test and every dropped record (cap $100).

## Files

| File | Purpose |
|---|---|
| `train_v4.jsonl` | the records: `id`, `family`, `domain`, `state`, `questions`, `gold`, `meta` (`factors`, `skills`, `plan`, `judgments`, `judge_setup`, `contested`, `deciding`, `off_plan`) |
| `stats.json` | every R22.4.3 and R22.9 check, overall and per family, plus generation counts and API cost by model and stage |
| `qc/families.json` | the {len(fams)} family specifications: role, setting, question set, latent factors, sections, rendering notes, skills |
| `qc/shared_scales.json` | the three cross-family shared scales, new for this set |
| `qc/work/` | everything the run produced: families, every record written (kept or not) with its sampled and final factors, plan and deciding evidence, rejected records with the reason, every judgment, the batch results and the cost ledger |
| `qc/*.log` | stage logs from the worker sessions |
| `pipeline/` | the code |

`meta.deciding` is the writer's statement, per question, of the field or fact that settles it (or that holds a balanced or contested question in balance). `meta.off_plan` lists any question whose measured gold missed its plan.

## How it was made (R26 pipeline)

All calls went through the Anthropic API, billed to the team's API key, from separate worker sessions. They used the Python SDK and structured outputs. Every request except the family designs went through the **Message Batches API** (half price).

1. **Shared scales:** Claude Opus 5.5, one call. Three new generic 4-level scales, each rating one quantity with checkable anchors:
{scale_txt}
2. **Families:** Claude Opus 5.5, one direct call per family, up to 3 attempts.
   - **Slots:** each of the 40 slots copies the structure of one pilot-2 slot, so the set keeps pilot 2's mix: type mix, option and level counts, bare yes/no question, shared-scale use and skills. Each slot has a new domain.
   - **Design rules:** the designer follows pilot 2's anchoring rules. Every score question rates one quantity, each level is a checkable condition, and choice options differ along one axis.
   - **Checks:** code checks every R22.5 rule and the R22.1 exclusions.
3. **Plans:** in code. Per record, code draws the latent factors, a target length and a per-question plan: clarity, intended top answer and position. The plan shares are nudged from pilot 2's measured result, as R26 asks:
   - fewer clear and leaning score plans;
   - more clear choice plans and more first-option choice answers;
   - planned-true statements at 62%.
4. **Records:** Claude Sonnet 5.5, effort medium, **five records of one family per request**.
   - **Prompt:** the writing rules and the family brief are a **cached system prompt**. The writer returns each record, the final factor values it used, and the deciding field per question.
   - **Code checks:** 3–6 top-level keys, all from the family's sections, and at most 200 words.
   - **No rework:** a failing record is dropped. Requests that fail at the API are resubmitted once.
5. **Gold:** **three Claude Haiku 5.5 judgments per record**, each a separate batch request with no shared context. Judges see only the record, the role and the question set, and each gives a full distribution for every question. Sampling temperature cannot be set on these models, so the three samples differ by stance instead:

| Judge | Model | Effort | Stance |
|---|---|---|---|
{judges}

   The gold is the plain mean of the three, rounded to 4 decimals, never sharpened or smoothed. All three judgments are in `meta.judgments`.
6. **Accept rule:** a question is off plan when its measured top answer is neither the planned answer nor, for a balanced or contested plan, the planned second answer. A record is kept when **at most one** of its five questions is off plan.
   - **Why one miss:** R26 suggested requiring every question to match. On pilot 2's records, that would have kept only about 19%, against 64% with one miss allowed.
7. **Selection:** from the accepted records, 25 per family were chosen greedily so the set's measured statistics come as close as possible to R22.4.3, with no near-duplicate pair within a family. Gold values were never changed.

### Generation counts

- **Written:**
  - {written + len(rejected)} records written in total (per-family counts in `stats.json`, `generation.records_written_per_family`);
  - 50 records per family first, then a top-up for the families that fell short of 25.
- **Dropped:**
  - {len(rejected)} records failed the code checks ({reason_txt});
  - {off_plan} records failed the accept rule.
- **Kept:** {st['records']}.
- **Passed every check but not needed** (their family already had 25 closer to the targets): {written + len(rejected) - len(rejected) - off_plan - st['records']}.
- **Families below 25 records:** {', '.join(f'{k} ({v})' for k, v in sorted(short.items())) or 'none'}.

## Families

| Family | Domain | Skills | Questions | Records |
|---|---|---|---|---|
{fam_rows}

- **Skill shares of families:** {fmt(st['skills_share_of_families'])}.
- **Domains:** {st['domains']}.

## Label shape (R22.4.3)

| Type | Questions | top < 0.5 | 0.5–0.7 | 0.7–0.9 | ≥ 0.9 | mean top | pilot 2 mean top | mean entropy |
|---|---|---|---|---|---|---|---|---|
{chr(10).join(type_rows)}

- **Contested share** (the three judges' top answers disagree): {st['contested_share']:.0%}.
- **Top-answer position:** score {fmt(st['score_top_position'])}; choice {fmt(st['choice_top_position'])}.
- **True/false:** `true` is top in {st['noul_true_top']:.0%}; `criteria: null` in {st['noul_criteria_null']:.0%}.
- **Score mass two or more levels from the top:** {st['score_mass_two_or_more_from_top_mean']} on average.
- **Gold zeros:** {st['gold_zero_probabilities']}.
- **Records:** median {st['record_words']['median']} words (p10 {st['record_words']['p10']}, p90 {st['record_words']['p90']}, maximum {st['record_words']['max']}).
- **Near-duplicate pairs within a family:** {st['near_duplicate_record_pairs']}.

## Every check

| Check | Value | Target | Result |
|---|---|---|---|
{check_rows}

## Where the set misses the targets

READ_MISSES

## Cost

| Stage | Cost (USD) |
|---|---|
""" + "\n".join(f"| {k} | {v} |" for k, v in by_stage.items()) + f"""
| **total** | **{cost.get('total', '?')}** |

- **By model:** {fmt(cost.get('by_model', {}))}.
- **Requests:** {cost.get('requests', '?')} in total, {cost.get('batched_requests', '?')} of them through the Batches API.
- **Includes:** the smoke test and the top-up, and every dropped record and retry.

## Licence

Released to the Signpost-D team without restriction (CC0).
"""
misses_path = os.path.join(out, "qc", "misses.md")
readme = readme.replace("READ_MISSES", open(misses_path).read().strip() if os.path.exists(misses_path) else "See the table above.")
open(os.path.join(out, "README.md"), "w", encoding="utf-8").write(readme)
print("README.md written")
