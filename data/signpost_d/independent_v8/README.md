# independent_v8 — R30 training records, batch 2 (`train_v5.jsonl`)

Batch 2 of the training records in pilot 2's design (the R22 brief with the R24 changes), built as R30 asks with exactly the R26/R27 pipeline that made train_v4, plus one tweak: more balanced and contested plans.

- **Size:** 979 records in 40 new families, 4895 questions, ids `F301-0001` onward.
- **Format:** `train_v5.jsonl` is in System One format, one record per line, with the same fields as train_v4.
- **Rules:** everything is invented and the R22.1 exclusions apply. No benchmark was opened, read or used. No family, question set, shared scale, record or seed is shared with pilot 1 (`independent_v6/pilot_v3.jsonl`, evaluation only), pilot 2 (`independent_v6/pilot_v3b.jsonl`) or train_v4 (`independent_v7/train_v4.jsonl`). The 40 domains are new: none of the 56 used before.

**Checks:** 89 of 116 R22.4.3 / R22.9 checks pass, overall and per family. The misses are listed under *Where the set misses the targets*.

**API cost:** about **$41.28** on the team's API key, including every dropped record and retry (cap $50).

## Files

| File | Purpose |
|---|---|
| `train_v5.jsonl` | the records: `id`, `family`, `domain`, `state`, `questions`, `gold`, `meta` (`factors`, `skills`, `plan`, `judgments`, `judge_setup`, `contested`, `deciding`, `off_plan`) |
| `stats.json` | every R22.4.3 and R22.9 check, overall and per family, plus generation counts and API cost by model and stage |
| `qc/families.json` | the 40 family specifications: role, setting, question set, latent factors, sections, rendering notes, skills |
| `qc/shared_scales.json` | the three cross-family shared scales, new for this set |
| `qc/work/` | everything the run produced: families, every record written (kept or not) with its sampled and final factors, plan and deciding evidence, rejected records with the reason, every judgment, the batch results and the cost ledger |
| `qc/*.log` | stage logs from the worker sessions |
| `pipeline/` | the code |

`meta.deciding` is the writer's statement, per question, of the field or fact that settles it (or that holds a balanced or contested question in balance). `meta.off_plan` lists any question whose measured gold missed its plan.

## How it was made (the R26/R27 pipeline, unchanged except the plans)

All calls went through the Anthropic API, billed to the team's API key, from separate worker sessions. They used the Python SDK and structured outputs. Every request except the family designs went through the **Message Batches API** (half price).

1. **Shared scales:** Claude Opus 5.5, one call. Three new generic 4-level scales, each rating one quantity with checkable anchors:
   - `affected_scope`: How many people or units does this issue directly affect? Levels: Affects one person or unit only / Affects two to five people or units / Affects six to twenty people or units / Affects more than twenty people or units
   - `pending_age`: How long has this record been waiting without any decision? Levels: Logged less than 24 hours ago / Waiting between one and seven days / Waiting between eight and thirty days / Waiting more than thirty days without decision
   - `source_support`: How many independent sources confirm the information in this record? Levels: No independent source confirms the information / Exactly one independent source confirms it / Two or three independent sources confirm it / Four or more independent sources confirm it
2. **Families:** Claude Opus 5.5, one direct call per family, up to 3 attempts.
   - **Slots:** each of the 40 slots copies the structure of one pilot-2 slot, so the set keeps pilot 2's mix: type mix, option and level counts, bare yes/no question, shared-scale use and skills. Each slot has a new domain.
   - **Design rules:** the designer follows pilot 2's anchoring rules. Every score question rates one quantity, each level is a checkable condition, and choice options differ along one axis.
   - **Checks:** code checks every R22.5 rule and the R22.1 exclusions.
3. **Plans:** in code. Per record, code draws the latent factors, a target length and a per-question plan: clarity, intended top answer and position. Changed from train_v4, as R30 asks (train_v4 measured 19% contested):
   - true/false: balanced 40% (train_v4 30%);
   - score: contested 22% (14%), leaning 20% (26%), clear 8% (10%), so score comes out a little softer;
   - choice, positions and planned-true share (62%) unchanged;
   - the writer is told that contested decisions are common and must be honestly two-sided;
   - selection weighs the contested-share target 5 times (train_v4: 2).
4. **Records:** Claude Sonnet 5.5, effort medium, **five records of one family per request**.
   - **Prompt:** the writing rules and the family brief are a **cached system prompt**. The writer returns each record, the final factor values it used, and the deciding field per question.
   - **Code checks:** 3–6 top-level keys, all from the family's sections, and at most 200 words.
   - **No rework:** a failing record is dropped. Requests that fail at the API are resubmitted once.
5. **Gold:** **three Claude Haiku 5.5 judgments per record**, each a separate batch request with no shared context. Judges see only the record, the role and the question set, and each gives a full distribution for every question. Sampling temperature cannot be set on these models, so the three samples differ by stance instead:

| Judge | Model | Effort | Stance |
|---|---|---|---|
| careful_operator | Claude Haiku 5.5 | medium | You are an experienced practitioner in this role: thorough, practical, and used to acting on records like this every day. |
| by_the_book | Claude Haiku 5.5 | medium | You are a by-the-book auditor: you apply the stated rules and thresholds literally and treat anything not on the record as unknown. |
| generalist | Claude Haiku 5.5 | medium | You are a sensible generalist new to this team: you read the record plainly and judge as an informed outsider would. |

   The gold is the plain mean of the three, rounded to 4 decimals, never sharpened or smoothed. All three judgments are in `meta.judgments`.
6. **Accept rule:** a question is off plan when its measured top answer is neither the planned answer nor, for a balanced or contested plan, the planned second answer. A record is kept when **at most one** of its five questions is off plan.
   - **Why one miss:** as in train_v4. Requiring every question to match keeps only about one record in five.
7. **Selection:** from the accepted records, 25 per family were chosen greedily so the set's measured statistics come as close as possible to R22.4.3, with no near-duplicate pair within a family. Gold values were never changed.

### Generation counts

- **Written:**
  - 2785 records written in total (per-family counts in `stats.json`, `generation.records_written_per_family`);
  - 55 records per family first, then a top-up for any family that fell short of 25.
- **Dropped:**
  - 335 records failed the code checks (over 200 words: 152; more than 6 top-level sections: 91; top-level keys outside the family sections: 72; writer left out a record: 17; record_json not valid JSON: 2; over 320 words: 1);
  - 1183 records failed the accept rule.
- **Kept:** 979.
- **Passed every check but not needed** (their family already had 25 closer to the targets): 288.
- **Families below 25 records:** F316 (24), F318 (10), F338 (20).

## Families

| Family | Domain | Skills | Questions | Records |
|---|---|---|---|---|
| F301 | clinic referral triage | S1, S2, S3, S4, S5, S6, S7 | `fast_track_met` (noul); `vetting_outcome` (choice); `first_contact` (choice); `clinical_urgency` (score); `record_agreement` (score) | 25 |
| F302 | clinical-trial screening visits | S1, S3, S4, S5, S6, S7 | `eligibility_proven` (noul); `next_step` (choice); `primary_issue` (choice); `affected_scope` (score); `window_left` (score) | 25 |
| F303 | home oxygen equipment deliveries | S2, S3, S4, S5, S6, S7 | `rx_match` (noul); `next_step` (choice); `fulfilment` (choice); `supply_runway` (score); `open_hazards` (score) | 25 |
| F304 | hospital patient transport bookings | S1, S3, S4, S5, S6, S7 | `vehicle_fit` (noul); `disposition` (choice); `crew_config` (choice); `time_pressure` (score); `delay_impact` (score) | 25 |
| F305 | dialysis unit session logs | S1, S2, S4, S5, S6, S7 | `uf_reconciles` (noul); `checks_before_start` (noul); `log_disposition` (choice); `time_shortfall` (score); `pending_age` (score) | 25 |
| F306 | school trip risk assessments | S1, S3, S4, S5, S6, S7 | `consent_complete` (noul); `staffing_adequate` (noul); `disposition` (choice); `mismatch_count` (score); `medical_coverage` (score) | 25 |
| F307 | university lab chemical inventory checks | S2, S3, S4, S5, S6, S7 | `qty_reconciled` (noul); `storage_permitted` (noul); `next_action` (choice); `source_support` (score); `review_overdue` (score) | 25 |
| F308 | exam access arrangement requests | S1, S3, S4, S5, S6, S7 | `normal_working` (noul); `assessor_valid` (noul); `disposition` (choice); `time_pressure` (score); `unsupported_items` (score) | 25 |
| F309 | rare books reading room requests | S1, S2, S3, S4, S5, S6, S7 | `reg_valid` (noul); `disposition` (choice); `access_form` (choice); `items_blocked` (score); `handling_risk` (score) | 25 |
| F310 | benefits eligibility reassessments | S1, S3, S4, S5, S6, S7 | `undeclared_change` (noul); `next_step` (choice); `change_category` (choice); `affected_scope` (score); `affected_duration` (score) | 25 |
| F311 | polling-station closing reports | S2, S3, S4, S5, S6, S7 | `custody_unbroken` (noul); `box_disposition` (choice); `figure_problem` (choice); `unexplained_gap` (score); `paperwork_shortfall` (score) | 25 |
| F312 | community project grant progress reports | S1, S3, S4, S5, S6, S7 | `unapproved_spend` (noul); `tranche_decision` (choice); `variance_cause` (choice); `evidence_gap` (score); `milestone_delay` (score) | 25 |
| F313 | building control site inspections | S1, S2, S4, S5, S6, S7 | `inspected_before_cover` (noul); `matches_spec` (noul); `next_step` (choice); `defect_severity` (score); `pending_age` (score) | 25 |
| F314 | gas safety certificates for rented homes | S1, S3, S4, S5, S6, S7 | `covers_all_appliances` (noul); `engineer_valid` (noul); `next_step` (choice); `renewal_urgency` (score); `open_hazard` (score) | 25 |
| F315 | street lighting fault reports | S2, S3, S4, S5, S6, S7 | `supply_side_fault` (noul); `repeat_failure` (noul); `next_action` (choice); `source_support` (score); `repair_progress` (score) | 25 |
| F316 | road gritting run logs | S1, S3, S4, S5, S6, S7 | `treated_before_freeze` (noul); `salt_reconciles` (noul); `follow_up` (choice); `deficient_length` (score); `freeze_proximity` (score) | 24 |
| F317 | tram depot vehicle checks | S1, S2, S3, S4, S5, S6, S7 | `sc_defects_cleared` (noul); `release_decision` (choice); `worst_subsystem` (choice); `exam_completion` (score); `exam_mileage` (score) | 25 |
| F318 | canal lock maintenance visits | S1, S3, S4, S5, S6, S7 | `safe_to_reopen` (noul); `record_disposition` (choice); `return_urgency` (choice); `affected_scope` (score); `section_mismatches` (score) | 10 |
| F319 | wind turbine blade inspections | S2, S3, S4, S5, S6, S7 | `damage_worsened` (noul); `disposition` (choice); `damage_mechanism` (choice); `defect_depth` (score); `repair_urgency` (score) | 25 |
| F320 | water main leak repairs | S1, S3, S4, S5, S6, S7 | `third_party_cause` (noul); `closeout_action` (choice); `asset_followup` (choice); `interruption_duration` (score); `reinstatement_stage` (score) | 25 |
| F321 | telecom mast site access visits | S1, S2, S4, S5, S6, S7 | `within_scope` (noul); `certs_in_date` (noul); `closeout_action` (choice); `scope_completion` (score); `pending_age` (score) | 25 |
| F322 | crop scouting reports | S1, S3, S4, S5, S6, S7 | `id_supported` (noul); `resistance_suspected` (noul); `next_step` (choice); `window_urgency` (score); `pressure_level` (score) | 25 |
| F323 | beehive inspection records | S2, S3, S4, S5, S6, S7 | `notifiable_confirmed` (noul); `queenright` (noul); `next_action` (choice); `source_support` (score); `mite_load` (score) | 25 |
| F324 | greenhouse irrigation logs | S1, S3, S4, S5, S6, S7 | `under_dosed` (noul); `emitter_clogging` (noul); `next_action` (choice); `drain_deviation` (score); `off_plan_cycles` (score) | 25 |
| F325 | fish farm water quality checks | S1, S2, S3, S4, S5, S6, S7 | `genuine_do_breach` (noul); `next_step` (choice); `deviation_cause` (choice); `persistence` (score); `evidence_completeness` (score) | 25 |
| F326 | tree preservation order applications | S1, S3, S4, S5, S6, S7 | `evidence_supports_works` (noul); `decision` (choice); `inspection_priority` (choice); `affected_scope` (score); `works_extent` (score) | 25 |
| F327 | community hall booking requests | S2, S3, S4, S5, S6, S7 | `cover_valid` (noul); `disposition` (choice); `supervision` (choice); `doc_completeness` (score); `attendance_load` (score) | 25 |
| F328 | fleet telematics driving reports | S1, S3, S4, S5, S6, S7 | `driver_attributed` (noul); `follow_up` (choice); `worst_event_cause` (choice); `speed_excess` (score); `hours_exposure` (score) | 25 |
| F329 | job application screening | S1, S2, S4, S5, S6, S7 | `meets_mandatory` (noul); `experience_consistent` (noul); `next_step` (choice); `discrepancy_count` (score); `pending_age` (score) | 25 |
| F330 | expense-policy exception requests | S1, S3, S4, S5, S6, S7 | `preapproval_covers` (noul); `outside_control` (noul); `excess_disposition` (choice); `excess_size` (score); `discrepancy_count` (score) | 25 |
| F331 | storm damage insurance claim intake | S2, S3, S4, S5, S6, S7 | `weather_corroborated` (noul); `pre_existing_damage` (noul); `intake_route` (choice); `source_support` (score); `makesafe_urgency` (score) | 25 |
| F332 | credit union loan application screening | S1, S3, S4, S5, S6, S7 | `income_supported` (noul); `debts_disclosed` (noul); `next_step` (choice); `dti_level` (score); `arrears_depth` (score) | 25 |
| F333 | student accommodation room inspections | S1, S2, S3, S4, S5, S6, S7 | `checkin_clean` (noul); `disposition` (choice); `main_cause` (choice); `defect_severity` (score); `charge_gap` (score) | 25 |
| F334 | football match officiating reports | S1, S3, S4, S5, S6, S7 | `identity_confirmed` (noul); `next_step` (choice); `incident_category` (choice); `affected_scope` (score); `mismatch_count` (score) | 25 |
| F335 | radio station content scheduling | S2, S3, S4, S5, S6, S7 | `asset_fits` (noul); `disposition` (choice); `main_blocker` (choice); `lock_urgency` (score); `open_checks` (score) | 25 |
| F336 | film archive restoration checks | S1, S3, S4, S5, S6, S7 | `master_complete` (noul); `job_disposition` (choice); `element_handling` (choice); `steps_outstanding` (score); `decay_stage` (score) | 25 |
| F337 | seismograph station data quality reviews | S1, S2, S4, S5, S6, S7 | `response_valid` (noul); `gaps_explained` (noul); `disposition` (choice); `usable_fraction` (score); `pending_age` (score) | 25 |
| F338 | air quality monitor calibration visits | S1, S3, S4, S5, S6, S7 | `data_accepted` (noul); `reference_valid` (noul); `next_step` (choice); `flag_extent` (score); `return_urgency` (score) | 20 |
| F339 | animal shelter adoption applications | S2, S3, S4, S5, S6, S7 | `home_visit_valid` (noul); `species_consent` (noul); `disposition` (choice); `source_support` (score); `requirement_conflicts` (score) | 25 |
| F340 | kennel boarding intake checks | S1, S3, S4, S5, S6, S7 | `vacc_cover_valid` (noul); `declaration_consistent` (noul); `admission_disposition` (choice); `discrepancy_count` (score); `action_urgency` (score) | 25 |

- **Skill shares of families:** {"S1": 0.75, "S2": 0.5, "S3": 0.875, "S4": 1.0, "S5": 1.0, "S6": 1.0, "S7": 1.0}.
- **Domains:** 40.

## Label shape (R22.4.3)

| Type | Questions | top < 0.5 | 0.5–0.7 | 0.7–0.9 | ≥ 0.9 | mean top | train_v4 mean top | mean entropy |
|---|---|---|---|---|---|---|---|---|
| noul | 1473 | 0% | 26% | 36% | 37% | 0.805 | 0.803 | 0.429 |
| choice | 1464 | 27% | 48% | 22% | 4% | 0.6 | 0.608 | 1.005 |
| score | 1958 | 21% | 39% | 33% | 8% | 0.651 | 0.679 | 0.88 |

- **Contested share** (the three judges' top answers disagree): 21%.
- **Top-answer position:** score {"lowest": 0.168, "middle": 0.62, "highest": 0.213}; choice {"first": 0.137, "middle": 0.68, "last": 0.182}.
- **True/false:** `true` is top in 48%; `criteria: null` in 34%.
- **Score mass two or more levels from the top:** 0.0742 on average.
- **Gold zeros:** 0.
- **Records:** median 110 words (p10 65, p90 167, maximum 200).
- **Near-duplicate pairs within a family:** 0.

## Every check

| Check | Value | Target | Result |
|---|---|---|---|
| noul share top <0.5 | 0.0 | [0, 0] | pass |
| noul share top 0.5-0.7 | 0.265 | [0.3, 0.4] | **miss** |
| noul share top 0.7-0.9 | 0.365 | [0.28, 0.38] | pass |
| noul share top >=0.9 | 0.371 | [0.27, 0.37] | **miss** |
| noul mean top | 0.805 | [0.75, 0.81] | pass |
| noul mean entropy | 0.429 | [0.4, 0.5] | pass |
| choice share top <0.5 | 0.273 | [0.15, 0.25] | **miss** |
| choice share top 0.5-0.7 | 0.475 | [0.38, 0.5] | pass |
| choice share top 0.7-0.9 | 0.215 | [0.17, 0.27] | pass |
| choice share top >=0.9 | 0.037 | [0.1, 0.18] | **miss** |
| choice mean top | 0.6 | [0.62, 0.68] | **miss** |
| choice mean entropy | 1.005 | [0.75, 0.92] | **miss** |
| score share top <0.5 | 0.209 | [0.18, 0.28] | pass |
| score share top 0.5-0.7 | 0.39 | [0.45, 0.57] | **miss** |
| score share top 0.7-0.9 | 0.327 | [0.15, 0.25] | **miss** |
| score share top >=0.9 | 0.075 | [0.03, 0.09] | pass |
| score mean top | 0.651 | [0.58, 0.64] | **miss** |
| score mean entropy | 0.88 | [0.83, 0.98] | pass |
| contested share (judges' tops disagree) | 0.213 | [0.3, 0.4] | **miss** |
| score top at lowest | 0.168 | [0.1, 0.16] | **miss** |
| score top at middle | 0.62 | [0.57, 0.67] | pass |
| score top at highest | 0.213 | [0.22, 0.3] | **miss** |
| choice top at first | 0.137 | [0.15, 0.25] | **miss** |
| choice top at middle | 0.68 | [0.6, 0.7] | pass |
| choice top at last | 0.182 | [0.1, 0.18] | **miss** |
| noul true top | 0.483 | [0.45, 0.5] | pass |
| noul criteria null | 0.336 | [0.3, 0.36] | pass |
| score mass >= 2 levels from top (mean) | 0.0742 | [0, 0.1] | pass |
| F301 contested share | 0.328 | [0.15, 0.55] | pass |
| F301 noul true top | 0.28 | [0.25, 0.7] | pass |
| F302 contested share | 0.088 | [0.15, 0.55] | **miss** |
| F302 noul true top | 0.0 | [0.25, 0.7] | **miss** |
| F303 contested share | 0.304 | [0.15, 0.55] | pass |
| F303 noul true top | 0.52 | [0.25, 0.7] | pass |
| F304 contested share | 0.272 | [0.15, 0.55] | pass |
| F304 noul true top | 0.76 | [0.25, 0.7] | **miss** |
| F305 contested share | 0.224 | [0.15, 0.55] | pass |
| F305 noul true top | 0.5 | [0.25, 0.7] | pass |
| F306 contested share | 0.168 | [0.15, 0.55] | pass |
| F306 noul true top | 0.52 | [0.25, 0.7] | pass |
| F307 contested share | 0.2 | [0.15, 0.55] | pass |
| F307 noul true top | 0.58 | [0.25, 0.7] | pass |
| F308 contested share | 0.192 | [0.15, 0.55] | pass |
| F308 noul true top | 0.44 | [0.25, 0.7] | pass |
| F309 contested share | 0.24 | [0.15, 0.55] | pass |
| F309 noul true top | 0.6 | [0.25, 0.7] | pass |
| F310 contested share | 0.104 | [0.15, 0.55] | **miss** |
| F310 noul true top | 0.44 | [0.25, 0.7] | pass |
| F311 contested share | 0.216 | [0.15, 0.55] | pass |
| F311 noul true top | 0.72 | [0.25, 0.7] | **miss** |
| F312 contested share | 0.096 | [0.15, 0.55] | **miss** |
| F312 noul true top | 0.44 | [0.25, 0.7] | pass |
| F313 contested share | 0.096 | [0.15, 0.55] | **miss** |
| F313 noul true top | 0.44 | [0.25, 0.7] | pass |
| F314 contested share | 0.336 | [0.15, 0.55] | pass |
| F314 noul true top | 0.7 | [0.25, 0.7] | pass |
| F315 contested share | 0.224 | [0.15, 0.55] | pass |
| F315 noul true top | 0.6 | [0.25, 0.7] | pass |
| F316 contested share | 0.2 | [0.15, 0.55] | pass |
| F316 noul true top | 0.312 | [0.25, 0.7] | pass |
| F317 contested share | 0.088 | [0.15, 0.55] | **miss** |
| F317 noul true top | 0.64 | [0.25, 0.7] | pass |
| F318 contested share | 0.3 | [0.15, 0.55] | pass |
| F318 noul true top | 0.0 | [0.25, 0.7] | **miss** |
| F319 contested share | 0.208 | [0.15, 0.55] | pass |
| F319 noul true top | 0.84 | [0.25, 0.7] | **miss** |
| F320 contested share | 0.136 | [0.15, 0.55] | **miss** |
| F320 noul true top | 0.4 | [0.25, 0.7] | pass |
| F321 contested share | 0.16 | [0.15, 0.55] | pass |
| F321 noul true top | 0.56 | [0.25, 0.7] | pass |
| F322 contested share | 0.344 | [0.15, 0.55] | pass |
| F322 noul true top | 0.5 | [0.25, 0.7] | pass |
| F323 contested share | 0.168 | [0.15, 0.55] | pass |
| F323 noul true top | 0.56 | [0.25, 0.7] | pass |
| F324 contested share | 0.224 | [0.15, 0.55] | pass |
| F324 noul true top | 0.36 | [0.25, 0.7] | pass |
| F325 contested share | 0.248 | [0.15, 0.55] | pass |
| F325 noul true top | 0.28 | [0.25, 0.7] | pass |
| F326 contested share | 0.224 | [0.15, 0.55] | pass |
| F326 noul true top | 0.64 | [0.25, 0.7] | pass |
| F327 contested share | 0.248 | [0.15, 0.55] | pass |
| F327 noul true top | 0.44 | [0.25, 0.7] | pass |
| F328 contested share | 0.16 | [0.15, 0.55] | pass |
| F328 noul true top | 0.56 | [0.25, 0.7] | pass |
| F329 contested share | 0.312 | [0.15, 0.55] | pass |
| F329 noul true top | 0.34 | [0.25, 0.7] | pass |
| F330 contested share | 0.264 | [0.15, 0.55] | pass |
| F330 noul true top | 0.34 | [0.25, 0.7] | pass |
| F331 contested share | 0.184 | [0.15, 0.55] | pass |
| F331 noul true top | 0.56 | [0.25, 0.7] | pass |
| F332 contested share | 0.16 | [0.15, 0.55] | pass |
| F332 noul true top | 0.8 | [0.25, 0.7] | **miss** |
| F333 contested share | 0.16 | [0.15, 0.55] | pass |
| F333 noul true top | 0.6 | [0.25, 0.7] | pass |
| F334 contested share | 0.336 | [0.15, 0.55] | pass |
| F334 noul true top | 0.24 | [0.25, 0.7] | **miss** |
| F335 contested share | 0.256 | [0.15, 0.55] | pass |
| F335 noul true top | 0.32 | [0.25, 0.7] | pass |
| F336 contested share | 0.192 | [0.15, 0.55] | pass |
| F336 noul true top | 0.44 | [0.25, 0.7] | pass |
| F337 contested share | 0.208 | [0.15, 0.55] | pass |
| F337 noul true top | 0.4 | [0.25, 0.7] | pass |
| F338 contested share | 0.23 | [0.15, 0.55] | pass |
| F338 noul true top | 0.325 | [0.25, 0.7] | pass |
| F339 contested share | 0.264 | [0.15, 0.55] | pass |
| F339 noul true top | 0.46 | [0.25, 0.7] | pass |
| F340 contested share | 0.208 | [0.15, 0.55] | pass |
| F340 noul true top | 0.44 | [0.25, 0.7] | pass |
| every family has exactly 5 questions | True | True | pass |
| records have 3-6 sections | [3, 6] | [3, 6] | pass |
| record words max <= 320 | 200 | [0, 320] | pass |
| skill S1 share of families | 0.75 | [0.4, 1] | pass |
| skill S2 share of families | 0.5 | [0.25, 1] | pass |
| skill S3 share of families | 0.875 | [0.5, 1] | pass |
| at least 6 domains | 40 | [6, null] | pass |
| no near-duplicate records in a family (>50% of field values equal) | 0 | 0 | pass |

## Where the set misses the targets

27 of 116 checks miss: 14 overall and 13 per family (7 `true` top share, 6 contested share).

- **Contested share 21%** against 30–40% (train_v4 19%). The extra contested and balanced plans helped only a little.
  - Three stances of one model (Haiku) seldom disagree on the top answer, and sampling temperature cannot be set to spread them.
  - The gold is the plain mean of the three, with nothing adjusted to reach the target.
  - Adding one Sonnet judge (about $5 per 1,000 records through the Batch API) would likely bring it near pilot 2's 40%. R30 asked for the train_v4 judges unchanged, so this was not done.
- **Score gold is still slightly sharp:** mean top 0.651 against 0.58–0.64 (train_v4 0.679).
  - 33% of score questions sit at 0.7–0.9 (target 15–25%) and 39% at 0.5–0.7 (target 45–57%).
  - The lowest level is top in 17% (target 10–16%) and the highest in 21% (target 22–30%).
- **Choice gold is slightly soft, as in train_v4:**
  - mean top 0.600 (target 0.62–0.68);
  - 4% of questions at ≥ 0.9 (target 10–18%);
  - entropy 1.00 (target 0.75–0.92);
  - first option top in 14% (target 15–25%) and last in 18% (target 10–18%, just over).
  - R30 asked to leave choice as it was.
- **True/false:**
  - the 0.5–0.7 band is 27% (target 30–40%) and ≥ 0.9 is 37.1% (target 27–37%);
  - `true` is top in 48% overall, inside the target, but outside 25–70% in 7 families.
- **Records are longer than R22.2.2's "about 70 words":** median 110, p90 167, maximum 200, under the plain 200-word ceiling, as in train_v4.
- **Three families are short of 25:** F316 has 24, F338 20 and F318 10.
  - F318 (gritting run logs) yields very few records that pass the accept rule, even after a top-up to 135 written.
  - A further top-up would cost about $3. It was not run, to stay well inside the cap.

Everything else passes:
- format and structure;
- `true` top 48% overall and `criteria: null` 34%;
- the middle score positions;
- skill shares;
- no gold zeros and no near-duplicate pairs;
- score mass two or more levels from the top at 7%.

## Cost

| Stage | Cost (USD) |
|---|---|
| scales | 0.02 |
| family | 5.83 |
| records | 32.29 |
| judge | 3.13 |
| **total** | **41.28** |

- **By model:** {"claude-opus-5-5": 5.85, "claude-sonnet-5-5": 32.29, "claude-haiku-5-5": 3.13}.
- **Requests:** 7948 in total, 7907 of them through the Batches API.
- **Includes:** every dropped record, retry and top-up.

## Licence

Released to the Signpost-D team without restriction (CC0).
