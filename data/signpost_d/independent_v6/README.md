# independent_v6 — R22 pilot: decision records with honest uncertainty

Pilot for the R22 brief (Signpost-D data brief v3, 31 October 2026): **200 records in 8 families, 1000 questions**. `pilot_v3.jsonl` is in System One format, one record per line, as in R22.5. Everything is invented. No benchmark was opened, read or used, and no document or question from an earlier delivery was reused. The R22.1 exclusions were applied: no AI-agent monitoring, customer support, purchasing or invoices, or security triage.

**Checks:** 32 of 52 R22.4.3 / R22.9 checks pass. The ones that miss are listed under *Where the pilot misses the targets*. The team chose to run the pilot with the current families and report those deviations, rather than redesign first.

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
- `time_pressure`: How soon must someone act on this record? Levels: No deadline; can wait for routine handling / Should be handled within the normal cycle / Needs action within the next working day / Requires action immediately, ahead of anything else queued
- `attention_needed`: How much reviewer effort does this record realistically require? Levels: Can pass through without any human look / A brief check of key fields suffices / Needs careful reading and some follow-up questions / Demands thorough examination and input from specialists
- `consequence_if_wrong`: How serious would the harm be if this decision were wrong? Levels: Negligible effect, easily corrected later on / Minor inconvenience or a small avoidable cost / Noticeable harm, costly or slow to reverse / Severe or lasting harm to people or property
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
| careful_operator | Claude Opus 5.5 | medium | You are an experienced practitioner in this role: thorough, practical, and used to acting on records like this every day. |
| cautious_reviewer | Claude Sonnet 5.5 | medium | You are a cautious reviewer: you take discrepancies and gaps seriously and hesitate to clear a record that has an open point, but you do not invent problems. |
| pragmatic_operator | Claude Sonnet 5.5 | medium | You are a pragmatic operator under time pressure: you look for what actually matters for the decision and give reasonable benefit of the doubt where a mitigating explanation is on the record. |
| by_the_book | Claude Haiku 5.5 | medium | You are a by-the-book auditor: you apply the stated rules and thresholds literally and treat anything not on the record as unknown. |
| generalist | Claude Haiku 5.5 | medium | You are a sensible generalist new to this team: you read the record plainly and judge as an informed outsider would. |

   Sampling temperature cannot be set on these models, so independence comes from different models and stances in separate calls. The base instruction asks for a competent person in the role reading the record once, carefully, with calibrated probabilities. It also tells judges to give mitigating evidence its weight and to treat statements as claims.
5. **Gold:** the plain mean of the five judgments, rounded to 4 decimals. It is never sharpened, smoothed or forced towards a plan.
6. **Selection:** 36 records were generated per family and 25 kept.
   - **Dropped for missing their plan** (R22.4.2 step 4): a question misses badly when planned clear and measured top < 0.6, or planned contested and measured top >= 0.9; a record is dropped when more than 2 of its questions miss.
   - **Selection:** the kept records were chosen greedily so that the batch's measured statistics come as close as possible to the R22.4.3 targets. Gold values were never changed.
   - **Counts:** dropped before judging {"record not written": 9}; dropped for plan miss {"F001": 0, "F002": 0, "F003": 1, "F004": 0, "F005": 0, "F006": 0, "F007": 0, "F008": 0}.

## Families

| Family | Domain | Role | Skills | Questions (type) | Records |
|---|---|---|---|---|---|
| F001 | clinical laboratory sample receipt | Specimen reception officer in a hospital pathology laboratory | S1, S2, S3, S4, S5, S6, S7 | same_patient (noul), disposition (choice), main_problem (choice), time_pressure (score), result_doubt (score) | 25 |
| F002 | building maintenance work orders | Facilities maintenance supervisor reviewing reactive work orders submitted for close-out on a mixed-use estate | S1, S3, S4, S5, S6, S7 | fault_resolved (noul), closure_disposition (choice), asset_action (choice), time_pressure (score), residual_risk (score) | 25 |
| F003 | municipal street-works permit applications | Street works permit officer at a local highway authority, reviewing one utility or contractor permit application at a time | S2, S3, S4, S5, S6, S7 | genuine_clash (noul), disposition (choice), true_category (choice), disruption_level (score), scrutiny_needed (score) | 25 |
| F004 | staff rosters checked against timesheets | Payroll rota auditor for a regional residential care group, checking each employee's pay-period roster against their submitted timesheet before payroll runs | S1, S3, S4, S5, S6, S7 | overclaim_supported (noul), disposition (choice), variance_category (choice), pay_impact (score), resolution_urgency (score) | 25 |
| F005 | refrigerated food deliveries to schools (temperature and timing) | School meals cold-chain compliance officer at a local authority catering service, reviewing one chilled or frozen delivery drop to one school kitchen at a time | S1, S2, S4, S5, S6, S7 | cold_chain_breach (noul), qty_reconciled (noul), stock_disposition (choice), food_safety_risk (score), attention_needed (score) | 25 |
| F006 | automatic weather-station data quality review | Network data quality analyst at a national meteorological service, reviewing one automatic weather station's 24-hour data batch at a time before it is released to the climate archive and forecast feeds | S1, S3, S4, S5, S6, S7 | rain_total_bad (noul), temp_drift (noul), release_action (choice), visit_urgency (score), user_confidence (score) | 25 |
| F007 | home-care visit logs reviewed by a care coordinator | Home-care coordinator reviewing each submitted carer visit log for a domiciliary care branch | S2, S3, S4, S5, S6, S7 | delivered_in_full (noul), client_decline (noul), next_step (choice), consequence_if_wrong (score), follow_up_urgency (score) | 25 |
| F008 | moderation of school exam marking | Senior coursework moderator at an awarding body, reviewing one centre's moderation sample for one component at a time | S1, S3, S4, S5, S6, S7 | outside_tolerance (noul), clerical_cause (noul), centre_outcome (choice), deviation_severity (score), follow_up_urgency (score) | 25 |

Skill shares of families: {"S1": 0.75, "S2": 0.5, "S3": 0.875, "S4": 1.0, "S5": 1.0, "S6": 1.0, "S7": 1.0}. Domains: 8.

## Label shape (R22.4.3)

| Type | Questions | top < 0.5 | 0.5–0.7 | 0.7–0.9 | ≥ 0.9 | mean top | mean entropy |
|---|---|---|---|---|---|---|---|
| noul | 300 | 0% | 26% | 37% | 37% | 0.805 | 0.419 |
| choice | 300 | 36% | 44% | 18% | 2% | 0.577 | 1.023 |
| score | 400 | 36% | 60% | 4% | 0% | 0.532 | 1.062 |

- **Contested share** (the five judges' individual top answers disagree): 37%.
- **Top-answer position:** score {"lowest": 0.048, "middle": 0.815, "highest": 0.138}; choice {"first": 0.067, "middle": 0.707, "last": 0.227}.
- **True/false:** `true` is top in 38%; `criteria: null` in 33%.
- **Score mass two or more levels from the top level:** 0.061 on average.
- **Gold zeros:** 0.
- **Records:** median 118 words (p10 72, p90 210, maximum 314). Near-duplicate record pairs within a family: 3.

## Every check

| Check | Value | Target | Result |
|---|---|---|---|
| noul share top <0.5 | 0.0 | [0, 0] | pass |
| noul share top 0.5-0.7 | 0.263 | [0.3, 0.4] | **miss** |
| noul share top 0.7-0.9 | 0.37 | [0.28, 0.38] | pass |
| noul share top >=0.9 | 0.367 | [0.27, 0.37] | pass |
| noul mean top | 0.805 | [0.75, 0.81] | pass |
| noul mean entropy | 0.419 | [0.4, 0.5] | pass |
| choice share top <0.5 | 0.363 | [0.15, 0.25] | **miss** |
| choice share top 0.5-0.7 | 0.437 | [0.38, 0.5] | pass |
| choice share top 0.7-0.9 | 0.183 | [0.17, 0.27] | pass |
| choice share top >=0.9 | 0.017 | [0.1, 0.18] | **miss** |
| choice mean top | 0.577 | [0.62, 0.68] | **miss** |
| choice mean entropy | 1.023 | [0.75, 0.92] | **miss** |
| score share top <0.5 | 0.365 | [0.18, 0.28] | **miss** |
| score share top 0.5-0.7 | 0.6 | [0.45, 0.57] | **miss** |
| score share top 0.7-0.9 | 0.035 | [0.15, 0.25] | **miss** |
| score share top >=0.9 | 0.0 | [0.03, 0.09] | **miss** |
| score mean top | 0.532 | [0.58, 0.64] | **miss** |
| score mean entropy | 1.062 | [0.83, 0.98] | **miss** |
| contested share (judges' tops disagree) | 0.373 | [0.3, 0.4] | pass |
| score top at lowest | 0.048 | [0.1, 0.16] | **miss** |
| score top at middle | 0.815 | [0.57, 0.67] | **miss** |
| score top at highest | 0.138 | [0.22, 0.3] | **miss** |
| choice top at first | 0.067 | [0.15, 0.25] | **miss** |
| choice top at middle | 0.707 | [0.6, 0.7] | **miss** |
| choice top at last | 0.227 | [0.1, 0.18] | **miss** |
| noul true top | 0.377 | [0.45, 0.5] | **miss** |
| noul criteria null | 0.333 | [0.3, 0.36] | pass |
| score mass >= 2 levels from top (mean) | 0.061 | [0, 0.1] | pass |
| F001 contested share | 0.424 | [0.15, 0.55] | pass |
| F001 noul true top | 0.32 | [0.25, 0.7] | pass |
| F002 contested share | 0.384 | [0.15, 0.55] | pass |
| F002 noul true top | 0.28 | [0.25, 0.7] | pass |
| F003 contested share | 0.376 | [0.15, 0.55] | pass |
| F003 noul true top | 0.68 | [0.25, 0.7] | pass |
| F004 contested share | 0.496 | [0.15, 0.55] | pass |
| F004 noul true top | 0.52 | [0.25, 0.7] | pass |
| F005 contested share | 0.24 | [0.15, 0.55] | pass |
| F005 noul true top | 0.6 | [0.25, 0.7] | pass |
| F006 contested share | 0.44 | [0.15, 0.55] | pass |
| F006 noul true top | 0.16 | [0.25, 0.7] | **miss** |
| F007 contested share | 0.288 | [0.15, 0.55] | pass |
| F007 noul true top | 0.3 | [0.25, 0.7] | pass |
| F008 contested share | 0.336 | [0.15, 0.55] | pass |
| F008 noul true top | 0.3 | [0.25, 0.7] | pass |
| every family has exactly 5 questions | True | True | pass |
| records have 3-6 sections | [3, 6] | [3, 6] | pass |
| record words max <= 320 | 314 | [0, 320] | pass |
| skill S1 share of families | 0.75 | [0.4, 1] | pass |
| skill S2 share of families | 0.5 | [0.25, 1] | pass |
| skill S3 share of families | 0.875 | [0.5, 1] | pass |
| at least 6 domains | 8 | [6, null] | pass |
| no near-duplicate records in a family (>50% of field values equal) | 3 | 0 | **miss** |

## Where the pilot misses the targets

20 checks miss. The main pattern, measured in two smoke tests before the pilot, is that **the judges' gold is softer than R22.4.3 asks for on score and choice questions**:
- Each judge individually puts only about 0.5–0.6 on its own top level of a 4- or 5-level scale, even for records written to be clear.
- Their mean therefore rarely reaches 0.7 on score questions.
- Two fixes were tried on the same records and neither moved this:
  - judge-prompt calibration anchors (score mean top 0.50 → 0.50);
  - one round of plan-guided record rewriting with the judges' measured distributions as feedback (0.50 → 0.51).
- The likely cause is the scales themselves. Several family scales combine more than one dimension (for example "substantial doubt over several tests" against "results probably invalid"), so a record can fit two neighbouring levels at once. Judges are right to split.

The same softness pushes the contested share above 40%. The record writer also often fails to make a planned-true statement read as true to sceptical judges, so `true` is top less often than the target.

Two smaller deviations:
- **Records are longer than asked.** The median is 118 words against R22.2.2's "about 70", and p90 is 210 against about 160, although none exceeds 320. The writer adds context fields.
- **Near-duplicate pairs:** 3 record pairs within a family share more than half their field values; they are left in and counted here.

The team chose to run this pilot as it stands and judge it by the R22.7 model ranges. If the label shape must match R22.4.3 more closely, the fix to try next is a family redesign with one-dimensional, anchored scales (crisp level boundaries a record can sit clearly inside), followed by another smoke test.

## Cost

API cost of the pilot run: about $22.42 ({"claude-sonnet-5-5": 15.48, "claude-haiku-5-5": 0.45, "claude-opus-5-5": 6.49}; 1905 calls). Earlier smoke tests on the same key cost about $9.

## Licence

Released to the Signpost-D team without restriction (CC0).

## Pilot 2 (R24)

A second pilot built for R24 is in `pilot_v3b.jsonl` (ids `F101-0001` onward): eight new families with one-dimensional, anchored scales, and its own `stats_v3b.json`, `qc/families_v3b.json`, `qc/shared_scales_v3b.json` and `qc/work_v3b/`. See `README_pilot_v3b.md`. Pilot 1 above is unchanged and kept for evaluation only.
