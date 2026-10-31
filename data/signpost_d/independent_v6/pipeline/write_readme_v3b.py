#!/usr/bin/env python3
"""Write README_pilot_v3b.md for the R24 pilot 2 from stats_v3b.json and qc/families_v3b.json, and add a pointer section
to README.md (pilot 1's README is otherwise left as it is)."""
from __future__ import annotations

import json
import os
import sys

out = sys.argv[1]
st = json.load(open(os.path.join(out, "stats_v3b.json")))
p1 = json.load(open(os.path.join(out, "stats.json")))
fams = json.load(open(os.path.join(out, "qc", "families_v3b.json")))
scales = json.load(open(os.path.join(out, "qc", "shared_scales_v3b.json")))
gen, cost = st["generation"], st.get("api_cost_usd", {})
extra_cost = sys.argv[2] if len(sys.argv) > 2 else ""


def fmt(v):
    return json.dumps(v) if isinstance(v, (list, dict)) else str(v)


def trow(t, a, b):
    if not a:
        return ""
    return (f"| {t} | {b['mean_top']} | {a['mean_top']} | {b['bins']['<0.5']:.0%} | {a['bins']['<0.5']:.0%} | "
            f"{b['bins']['0.7-0.9'] + b['bins']['>=0.9']:.0%} | {a['bins']['0.7-0.9'] + a['bins']['>=0.9']:.0%} | {a['mean_entropy']} |")


fam_rows = "\n".join(
    f"| {fid} | {f['domain']} | {', '.join(f['skills'])} | " + "; ".join(f"`{n}` ({q['type']})" for n, q in f["questions"].items()) + " |"
    for fid, f in fams.items())
scale_txt = "\n".join(f"- `{s['name']}`: {s['instructions']} Levels: " + " / ".join(s["levels"]) for s in scales)
check_rows = "\n".join(f"| {c['check']} | {fmt(c['value'])} | {fmt(c['target'])} | {'pass' if c['pass'] else '**miss**'} |" for c in st["checks"])
missed = [c for c in st["checks"] if not c["pass"]]
type_rows = "\n".join(trow(t, st["by_type"].get(t), p1["by_type"].get(t)) for t in ("noul", "choice", "score"))
sc, ch = st["by_type"]["score"], st["by_type"]["choice"]
r24 = [
    ("score questions at gold top >= 0.7", sc["bins"]["0.7-0.9"] + sc["bins"][">=0.9"], ">= 0.18"),
    ("choice questions at gold top >= 0.7", ch["bins"]["0.7-0.9"] + ch["bins"][">=0.9"], ">= 0.27"),
    ("score questions under 0.5", sc["bins"]["<0.5"], "<= 0.28"),
    ("choice questions under 0.5", ch["bins"]["<0.5"], "<= 0.25"),
]
r24_ok = [r24[0][1] >= 0.18 - 1e-9, r24[1][1] >= 0.27 - 1e-9, r24[2][1] <= 0.28 + 1e-9, r24[3][1] <= 0.25 + 1e-9]
r24_rows = "\n".join(f"| {n} | {v:.0%} | {t} | {'pass' if ok else '**miss**'} |" for (n, v, t), ok in zip(r24, r24_ok))

readme = f"""# Pilot 2 (R24) — `pilot_v3b.jsonl`

Second pilot for the R22 brief, built as R24 asks: **{st['records']} records in {len(fams)} new families, {st['questions']} questions**, ids `F101-0001` onward. It shares no family, question set, record or seed with pilot 1 (`pilot_v3.jsonl`, kept for evaluation only).

**Checks:** {st['checks_passed']} of {st['checks_total']} R22.4.3 / R22.9 checks pass, plus the four R24 sharpness checks below. Everything else in R22 holds as for pilot 1: everything is invented, the R22.1 exclusions apply, no benchmark was opened, and nothing was reused from earlier deliveries.

## What changed from pilot 1 (R24)

- **Fresh families and domains:** {', '.join(f['domain'] for f in fams.values())}. They have the same type mix (12 true/false / 12 choice / 16 score), option and level counts, bare yes/no share and skill shares as pilot 1. The three shared scales were redesigned too.
- **One-dimensional, anchored scales.** The family designer (Claude Opus 5.5) is required to follow these rules:
  - every score question rates exactly one quantity;
  - each level is a checkable condition in the record (a count, a size, a time window, a state);
  - neighbouring levels are separated by an anchor a judge can check;
  - choice options differ along one axis, and each says what makes it apply.

  The record writer is told to place clear and leaning records squarely inside the planned level's condition, and balanced or contested ones at the anchor between the two planned answers.
- **Plans adjusted for pilot 1's measured shift** (pilot 1's gold came out about one band softer than planned, and bunched on middle levels):
  - more clear and leaning plans;
  - more planned answers at the ends of each scale;
  - planned-true statements at 56%, with a rule that a planned-true statement needs direct, explicit evidence a sceptical reviewer accepts.

  The delivered gold is still only the judges' measured mean.
- **Shorter records:** target lognormal median 55 words (maximum 220), with a tighter length check.
- **No near-duplicates:** selection never keeps two records in a family that share more than half their field values.
- **Unchanged from pilot 1:** the models, the five independent judges, the gold rule (plain mean of five, never sharpened or smoothed), the plan-miss filter and the selection towards R22.4.3.

## Shared scales

{scale_txt}

## Families

| Family | Domain | Skills | Questions |
|---|---|---|---|
{fam_rows}

The full specifications (role, setting, factors, sections, rendering notes) are in `qc/families_v3b.json`.

## Label shape against pilot 1

| Type | pilot 1 mean top | pilot 2 mean top | pilot 1 top < 0.5 | pilot 2 top < 0.5 | pilot 1 top ≥ 0.7 | pilot 2 top ≥ 0.7 | pilot 2 mean entropy |
|---|---|---|---|---|---|---|---|
{type_rows}

| R24 sharpness check | Pilot 2 | Target | Result |
|---|---|---|---|
{r24_rows}

- **Contested share:** {st['contested_share']:.0%} (pilot 1 {p1['contested_share']:.0%}).
- **Score top position:** {fmt(st['score_top_position'])} (pilot 1 {fmt(p1['score_top_position'])}).
- **Choice top position:** {fmt(st['choice_top_position'])}.
- **True/false:** `true` is top in {st['noul_true_top']:.0%} (pilot 1 {p1['noul_true_top']:.0%}).
- **Records:** median {st['record_words']['median']} words (p10 {st['record_words']['p10']}, p90 {st['record_words']['p90']}, maximum {st['record_words']['max']}); pilot 1 had a median of {p1['record_words']['median']}. Near-duplicate pairs: {st['near_duplicate_record_pairs']}.

## Every check

| Check | Value | Target | Result |
|---|---|---|---|
{check_rows}

{('**Checks that miss:** ' + '; '.join(f"{c['check']} = {fmt(c['value'])} (target {fmt(c['target'])})" for c in missed) + '.') if missed else 'Every check passes.'}

## Generation

- **Records:** {gen['records_planned_per_family']} written per family, {gen['kept_per_family']} kept.
- **Dropped before judging:** {fmt(gen['dropped_before_judging'])}.
- **Dropped for plan miss:** {fmt(gen['dropped_for_plan_miss'])}.
- **Plan-miss rule:** {gen['plan_miss_rule']}.
- **Raw outputs:** every record (kept or not), every judgment and the cost ledger are in `qc/work_v3b/`.

**API cost of pilot 2:** about ${cost.get('total', '?')} ({fmt(cost.get('by_model', {}))}; {cost.get('calls', '?')} calls), on the team's API key. {extra_cost}
"""
open(os.path.join(out, "README_pilot_v3b.md"), "w", encoding="utf-8").write(readme)

main = open(os.path.join(out, "README.md"), encoding="utf-8").read()
marker = "\n## Pilot 2 (R24)\n"
if marker not in main:
    main += marker + f"""
A second pilot built for R24 is in `pilot_v3b.jsonl` (ids `F101-0001` onward): eight new families with one-dimensional, anchored scales, and its own `stats_v3b.json`, `qc/families_v3b.json`, `qc/shared_scales_v3b.json` and `qc/work_v3b/`. See `README_pilot_v3b.md`. Pilot 1 above is unchanged and kept for evaluation only.
"""
    open(os.path.join(out, "README.md"), "w", encoding="utf-8").write(main)
print("README_pilot_v3b.md written")
