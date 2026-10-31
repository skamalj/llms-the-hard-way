# Pilot 2 (R24) — `pilot_v3b.jsonl`

Second pilot for the R22 brief, built as R24 asks: **195 records in 8 new families, 975 questions**, ids `F101-0001` onward. It shares no family, question set, record or seed with pilot 1 (`pilot_v3.jsonl`, kept for evaluation only).

**Checks:** 41 of 52 R22.4.3 / R22.9 checks pass, plus the four R24 sharpness checks below. Everything else in R22 holds as for pilot 1: everything is invented, the R22.1 exclusions apply, no benchmark was opened, and nothing was reused from earlier deliveries.

## What changed from pilot 1 (R24)

- **Fresh families and domains:** hospital blood bank stock and issue checks, passenger lift service visit logs, drinking-water quality sampling at treatment works, primary school admission applications, hotel housekeeping room turnovers, warehouse cycle counts against the stock system, laboratory instrument calibration records, wildlife survey records submitted by field volunteers. They have the same type mix (12 true/false / 12 choice / 16 score), option and level counts, bare yes/no share and skill shares as pilot 1. The three shared scales were redesigned too.
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

- `action_due`: How soon must the next action on this record take place? Levels: No action needed within the next 30 days / Action needed within 8 to 30 days / Action needed within 1 to 7 days / Action needed today or already overdue
- `open_items`: How many required items on this record remain unresolved? Levels: No required items remain unresolved / One or two required items remain unresolved / Three to five required items remain unresolved / Six or more required items remain unresolved
- `check_age`: How long since this record's key details were last verified? Levels: Last verified within the past 7 days / Last verified between 8 and 30 days ago / Last verified between 31 and 90 days ago / Last verified over 90 days ago, or never

## Families

| Family | Domain | Skills | Questions |
|---|---|---|---|
| F101 | hospital blood bank stock and issue checks | S1, S2, S3, S4, S5, S6, S7 | `sample_valid` (noul); `issue_action` (choice); `discrepancy_type` (choice); `issue_urgency` (score); `storage_exposure` (score) |
| F102 | passenger lift service visit logs | S1, S3, S4, S5, S6, S7 | `fit_for_service` (noul); `log_disposition` (choice); `fault_category` (choice); `action_due` (score); `mismatch_count` (score) |
| F103 | drinking-water quality sampling at treatment works | S2, S3, S4, S5, S6, S7 | `genuine_failure` (noul); `disposition` (choice); `anomaly_source` (choice); `exceedance_severity` (score); `record_gaps` (score) |
| F104 | primary school admission applications | S1, S3, S4, S5, S6, S7 | `address_confirmed` (noul); `disposition` (choice); `priority_category` (choice); `unexplained_discrepancies` (score); `priority_support` (score) |
| F105 | hotel housekeeping room turnovers | S1, S2, S4, S5, S6, S7 | `bed_setup_match` (noul); `blocking_defect` (noul); `room_disposition` (choice); `arrival_slack` (score); `open_items` (score) |
| F106 | warehouse cycle counts against the stock system | S1, S3, S4, S5, S6, S7 | `variance_real` (noul); `recount_confirms` (noul); `disposition` (choice); `variance_value` (score); `service_urgency` (score) |
| F107 | laboratory instrument calibration records | S2, S3, S4, S5, S6, S7 | `ref_traceable` (noul); `prior_impact` (noul); `disposition` (choice); `check_age` (score); `found_deviation` (score) |
| F108 | wildlife survey records submitted by field volunteers | S1, S3, S4, S5, S6, S7 | `id_supported` (noul); `protocol_met` (noul); `verification_action` (choice); `local_rarity` (score); `discrepancy_count` (score) |

The full specifications (role, setting, factors, sections, rendering notes) are in `qc/families_v3b.json`.

## Label shape against pilot 1

| Type | pilot 1 mean top | pilot 2 mean top | pilot 1 top < 0.5 | pilot 2 top < 0.5 | pilot 1 top ≥ 0.7 | pilot 2 top ≥ 0.7 | pilot 2 mean entropy |
|---|---|---|---|---|---|---|---|
| noul | 0.805 | 0.788 | 0% | 0% | 74% | 68% | 0.445 |
| choice | 0.577 | 0.617 | 36% | 25% | 20% | 29% | 0.959 |
| score | 0.532 | 0.657 | 36% | 21% | 4% | 38% | 0.859 |

| R24 sharpness check | Pilot 2 | Target | Result |
|---|---|---|---|
| score questions at gold top >= 0.7 | 38% | >= 0.18 | pass |
| choice questions at gold top >= 0.7 | 29% | >= 0.27 | pass |
| score questions under 0.5 | 21% | <= 0.28 | pass |
| choice questions under 0.5 | 25% | <= 0.25 | pass |

- **Contested share:** 40% (pilot 1 37%).
- **Score top position:** {"lowest": 0.146, "middle": 0.631, "highest": 0.223} (pilot 1 {"lowest": 0.048, "middle": 0.815, "highest": 0.138}).
- **Choice top position:** {"first": 0.095, "middle": 0.705, "last": 0.2}.
- **True/false:** `true` is top in 44% (pilot 1 38%).
- **Records:** median 82 words (p10 56, p90 148, maximum 190); pilot 1 had a median of 118. Near-duplicate pairs: 0.

## Every check

| Check | Value | Target | Result |
|---|---|---|---|
| noul share top <0.5 | 0.0 | [0, 0] | pass |
| noul share top 0.5-0.7 | 0.317 | [0.3, 0.4] | pass |
| noul share top 0.7-0.9 | 0.355 | [0.28, 0.38] | pass |
| noul share top >=0.9 | 0.328 | [0.27, 0.37] | pass |
| noul mean top | 0.788 | [0.75, 0.81] | pass |
| noul mean entropy | 0.445 | [0.4, 0.5] | pass |
| choice share top <0.5 | 0.247 | [0.15, 0.25] | pass |
| choice share top 0.5-0.7 | 0.468 | [0.38, 0.5] | pass |
| choice share top 0.7-0.9 | 0.268 | [0.17, 0.27] | pass |
| choice share top >=0.9 | 0.017 | [0.1, 0.18] | **miss** |
| choice mean top | 0.617 | [0.62, 0.68] | **miss** |
| choice mean entropy | 0.959 | [0.75, 0.92] | **miss** |
| score share top <0.5 | 0.208 | [0.18, 0.28] | pass |
| score share top 0.5-0.7 | 0.415 | [0.45, 0.57] | **miss** |
| score share top 0.7-0.9 | 0.264 | [0.15, 0.25] | **miss** |
| score share top >=0.9 | 0.113 | [0.03, 0.09] | **miss** |
| score mean top | 0.657 | [0.58, 0.64] | **miss** |
| score mean entropy | 0.859 | [0.83, 0.98] | pass |
| contested share (judges' tops disagree) | 0.397 | [0.3, 0.4] | pass |
| score top at lowest | 0.146 | [0.1, 0.16] | pass |
| score top at middle | 0.631 | [0.57, 0.67] | pass |
| score top at highest | 0.223 | [0.22, 0.3] | pass |
| choice top at first | 0.095 | [0.15, 0.25] | **miss** |
| choice top at middle | 0.705 | [0.6, 0.7] | **miss** |
| choice top at last | 0.2 | [0.1, 0.18] | **miss** |
| noul true top | 0.445 | [0.45, 0.5] | **miss** |
| noul criteria null | 0.345 | [0.3, 0.36] | pass |
| score mass >= 2 levels from top (mean) | 0.0757 | [0, 0.1] | pass |
| F101 contested share | 0.512 | [0.15, 0.55] | pass |
| F101 noul true top | 0.56 | [0.25, 0.7] | pass |
| F102 contested share | 0.472 | [0.15, 0.55] | pass |
| F102 noul true top | 0.36 | [0.25, 0.7] | pass |
| F103 contested share | 0.304 | [0.15, 0.55] | pass |
| F103 noul true top | 0.4 | [0.25, 0.7] | pass |
| F104 contested share | 0.408 | [0.15, 0.55] | pass |
| F104 noul true top | 0.36 | [0.25, 0.7] | pass |
| F105 contested share | 0.304 | [0.15, 0.55] | pass |
| F105 noul true top | 0.44 | [0.25, 0.7] | pass |
| F106 contested share | 0.4 | [0.15, 0.55] | pass |
| F106 noul true top | 0.38 | [0.25, 0.7] | pass |
| F107 contested share | 0.376 | [0.15, 0.55] | pass |
| F107 noul true top | 0.6 | [0.25, 0.7] | pass |
| F108 contested share | 0.4 | [0.15, 0.55] | pass |
| F108 noul true top | 0.4 | [0.25, 0.7] | pass |
| every family has exactly 5 questions | True | True | pass |
| records have 3-6 sections | [3, 6] | [3, 6] | pass |
| record words max <= 320 | 190 | [0, 320] | pass |
| skill S1 share of families | 0.75 | [0.4, 1] | pass |
| skill S2 share of families | 0.5 | [0.25, 1] | pass |
| skill S3 share of families | 0.875 | [0.5, 1] | pass |
| at least 6 domains | 8 | [6, null] | pass |
| no near-duplicate records in a family (>50% of field values equal) | 0 | 0 | pass |

**Checks that miss:** choice share top >=0.9 = 0.017 (target [0.1, 0.18]); choice mean top = 0.617 (target [0.62, 0.68]); choice mean entropy = 0.959 (target [0.75, 0.92]); score share top 0.5-0.7 = 0.415 (target [0.45, 0.57]); score share top 0.7-0.9 = 0.264 (target [0.15, 0.25]); score share top >=0.9 = 0.113 (target [0.03, 0.09]); score mean top = 0.657 (target [0.58, 0.64]); choice top at first = 0.095 (target [0.15, 0.25]); choice top at middle = 0.705 (target [0.6, 0.7]); choice top at last = 0.2 (target [0.1, 0.18]); noul true top = 0.445 (target [0.45, 0.5]).

## Generation

- **Records:** 36 written per family, 25 kept.
- **Dropped before judging:** {"record not written": 41}.
- **Dropped for plan miss:** {"F101": 0, "F102": 1, "F103": 1, "F104": 0, "F105": 0, "F106": 0, "F107": 0, "F108": 0}.
- **Plan-miss rule:** a question misses badly when planned clear and measured top < 0.6, or planned contested and measured top >= 0.9; a record is dropped when more than 2 of its questions miss.
- **Raw outputs:** every record (kept or not), every judgment and the cost ledger are in `qc/work_v3b/`.

**API cost of pilot 2:** about $32.84 ({"claude-opus-5-5": 6.75, "claude-sonnet-5-5": 25.67, "claude-haiku-5-5": 0.42}; 2212 calls), on the team's API key. Pilot 1 (R22) cost about $31 on the same key, including its smoke tests. F108 (wildlife surveys) has 20 records instead of 25: 16 of its 36 planned records failed the tighter length check three times and a retry recovered only 4, so the pilot is 195 records rather than 200; the other seven families have 25 each.
