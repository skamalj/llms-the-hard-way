# independent_v7 — R26 training records (`train_v4.jsonl`)

Training records in pilot 2's design (the R22 brief with the R24 changes), built as R26 asks with the cheaper pipeline.

- **Size:** 997 records in 40 new families, 4985 questions, ids `F201-0001` onward.
- **Format:** `train_v4.jsonl` is in System One format, one record per line, with the same fields as pilot 2.
- **Rules:** everything is invented and the R22.1 exclusions apply. No benchmark was opened, read or used. No family, question set, shared scale, record or seed is shared with pilot 1 (`independent_v6/pilot_v3.jsonl`, evaluation only) or pilot 2 (`independent_v6/pilot_v3b.jsonl`).

**Checks:** 83 of 116 R22.4.3 / R22.9 checks pass, overall and per family. The misses are listed under *Where the set misses the targets*.

**API cost:** about **$42.58** on the team's API key, including the smoke test and every dropped record (cap $100).

## Files

| File | Purpose |
|---|---|
| `train_v4.jsonl` | the records: `id`, `family`, `domain`, `state`, `questions`, `gold`, `meta` (`factors`, `skills`, `plan`, `judgments`, `judge_setup`, `contested`, `deciding`, `off_plan`) |
| `stats.json` | every R22.4.3 and R22.9 check, overall and per family, plus generation counts and API cost by model and stage |
| `qc/families.json` | the 40 family specifications: role, setting, question set, latent factors, sections, rendering notes, skills |
| `qc/shared_scales.json` | the three cross-family shared scales, new for this set |
| `qc/work/` | everything the run produced: families, every record written (kept or not) with its sampled and final factors, plan and deciding evidence, rejected records with the reason, every judgment, the batch results and the cost ledger |
| `qc/*.log` | stage logs from the worker sessions |
| `pipeline/` | the code |

`meta.deciding` is the writer's statement, per question, of the field or fact that settles it (or that holds a balanced or contested question in balance). `meta.off_plan` lists any question whose measured gold missed its plan.

## How it was made (R26 pipeline)

All calls went through the Anthropic API, billed to the team's API key, from separate worker sessions. They used the Python SDK and structured outputs. Every request except the family designs went through the **Message Batches API** (half price).

1. **Shared scales:** Claude Opus 5.5, one call. Three new generic 4-level scales, each rating one quantity with checkable anchors:
   - `discrepancy_size`: How far does the recorded value differ from the expected value? Levels: Matches expected value, or differs by under 2% / Differs from expected value by 2% to under 10% / Differs from expected value by 10% to under 25% / Differs from expected value by 25% or more
   - `failed_checks`: How many of the standard checks on this record failed? Levels: No standard checks failed / Exactly one standard check failed / Two or three standard checks failed / Four or more standard checks failed
   - `recurrence_count`: How often has this same issue been logged in 12 months? Levels: First occurrence; not logged in prior 12 months / Logged once before within the past 12 months / Logged two to four times in 12 months / Logged five or more times in 12 months
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
| careful_operator | Claude Haiku 5.5 | medium | You are an experienced practitioner in this role: thorough, practical, and used to acting on records like this every day. |
| by_the_book | Claude Haiku 5.5 | medium | You are a by-the-book auditor: you apply the stated rules and thresholds literally and treat anything not on the record as unknown. |
| generalist | Claude Haiku 5.5 | medium | You are a sensible generalist new to this team: you read the record plainly and judge as an informed outsider would. |

   The gold is the plain mean of the three, rounded to 4 decimals, never sharpened or smoothed. All three judgments are in `meta.judgments`.
6. **Accept rule:** a question is off plan when its measured top answer is neither the planned answer nor, for a balanced or contested plan, the planned second answer. A record is kept when **at most one** of its five questions is off plan.
   - **Why one miss:** R26 suggested requiring every question to match. On pilot 2's records, that would have kept only about 19%, against 64% with one miss allowed.
7. **Selection:** from the accepted records, 25 per family were chosen greedily so the set's measured statistics come as close as possible to R22.4.3, with no near-duplicate pair within a family. Gold values were never changed.

### Generation counts

- **Written:**
  - 2700 records written in total (per-family counts in `stats.json`, `generation.records_written_per_family`);
  - 50 records per family first, then a top-up for the families that fell short of 25.
- **Dropped:**
  - 255 records failed the code checks (over 200 words: 173; top-level keys outside the family sections: 32; more than 6 top-level sections: 20; writer left out a record: 12; over 320 words: 8; over its length target (smoke test, before the rule became a 200-word ceiling): 8; record_json not valid JSON: 2);
  - 1114 records failed the accept rule.
- **Kept:** 997.
- **Passed every check but not needed** (their family already had 25 closer to the targets): 334.
- **Families below 25 records:** F205 (24), F214 (24), F221 (24).

## Families

| Family | Domain | Skills | Questions | Records |
|---|---|---|---|---|
| F201 | veterinary practice controlled-drug registers | S1, S2, S3, S4, S5, S6, S7 | `unexplained_shortfall` (noul); `line_disposition` (choice); `variance_cause` (choice); `variance_size` (score); `auth_gaps` (score) | 25 |
| F202 | railway track patrol inspection reports | S1, S3, S4, S5, S6, S7 | `priority_supported` (noul); `next_step` (choice); `worst_category` (choice); `discrepancy_size` (score); `response_urgency` (score) | 25 |
| F203 | inter-library loan requests between public libraries | S2, S3, S4, S5, S6, S7 | `borrower_good_standing` (noul); `disposition` (choice); `loan_restriction` (choice); `time_slack` (score); `replacement_difficulty` (score) | 25 |
| F204 | community pharmacy prescription accuracy checks | S1, S3, S4, S5, S6, S7 | `strength_differs` (noul); `next_step` (choice); `error_category` (choice); `open_discrepancies` (score); `supply_urgency` (score) | 25 |
| F205 | airport ground-handling aircraft turnaround logs | S1, S2, S4, S5, S6, S7 | `load_reconciled` (noul); `delay_code_supported` (noul); `log_disposition` (choice); `offblock_delay` (score); `failed_checks` (score) | 24 |
| F206 | concrete pour records on construction sites | S1, S3, S4, S5, S6, S7 | `mix_conforms` (noul); `overrun_unmitigated` (noul); `disposition` (choice); `volume_gap` (score); `strength_progress` (score) | 25 |
| F207 | museum object loan condition reports | S2, S3, S4, S5, S6, S7 | `new_damage` (noul); `transit_breach` (noul); `disposition` (choice); `recurrence_count` (score); `change_severity` (score) | 25 |
| F208 | university thesis submission checks | S1, S3, S4, S5, S6, S7 | `ethics_covered` (noul); `overlap_explained` (noul); `next_step` (choice); `failed_reqs` (score); `urgency` (score) | 25 |
| F209 | fire extinguisher service records in office buildings | S1, S2, S3, S4, S5, S6, S7 | `left_compliant` (noul); `next_step` (choice); `service_level_due` (choice); `visit_lateness` (score); `mismatch_count` (score) | 25 |
| F210 | milk collection tanker tests at dairy farms | S1, S3, S4, S5, S6, S7 | `temp_compliant` (noul); `intake_disposition` (choice); `issue_source` (choice); `discrepancy_size` (score); `unexplained_breaches` (score) | 25 |
| F211 | ambulance daily vehicle readiness checks | S2, S3, S4, S5, S6, S7 | `defects_controlled` (noul); `readiness_status` (choice); `limiting_area` (choice); `check_completeness` (score); `defect_severity` (score) | 25 |
| F212 | court hearing bundle readiness checks | S1, S3, S4, S5, S6, S7 | `directed_docs_covered` (noul); `bundle_disposition` (choice); `agreement_status` (choice); `index_mismatch` (score); `lodging_lateness` (score) | 25 |
| F213 | public swimming pool water testing logs | S1, S2, S4, S5, S6, S7 | `test_frequency_met` (noul); `readings_reconcile` (noul); `log_disposition` (choice); `action_delay` (score); `failed_checks` (score) | 25 |
| F214 | highway bridge structural inspection records | S1, S3, S4, S5, S6, S7 | `ratings_consistent` (noul); `active_deterioration` (noul); `record_disposition` (choice); `defect_severity` (score); `next_inspection` (score) | 24 |
| F215 | grain store temperature and moisture monitoring | S2, S3, S4, S5, S6, S7 | `hotspot_active` (noul); `moisture_safe` (noul); `next_action` (choice); `recurrence_count` (score); `temp_excess` (score) | 25 |
| F216 | vaccination clinic cold-chain session logs | S1, S3, S4, S5, S6, S7 | `dosed_uncleared` (noul); `stock_reconciles` (noul); `stock_disposition` (choice); `excursion_duration` (score); `followup_urgency` (score) | 25 |
| F217 | theatre stage rigging inspections | S1, S2, S3, S4, S5, S6, S7 | `load_within_swl` (noul); `signoff` (choice); `limiting_issue` (choice); `defect_severity` (score); `checklist_completion` (score) | 25 |
| F218 | tree felling licence applications to a forestry authority | S1, S3, S4, S5, S6, S7 | `consent_established` (noul); `disposition` (choice); `consultation_tier` (choice); `discrepancy_size` (score); `restock_shortfall` (score) | 25 |
| F219 | fishing vessel catch landing declarations | S2, S3, S4, S5, S6, S7 | `within_tolerance` (noul); `disposition` (choice); `quota_standing` (choice); `submission_lateness` (score); `dispatch_urgency` (score) | 25 |
| F220 | surgical instrument tray sterilisation records | S1, S3, S4, S5, S6, S7 | `cycle_in_limits` (noul); `disposition` (choice); `failure_stage` (choice); `count_gaps` (score); `sterility_doubt` (score) | 25 |
| F221 | bus fleet brake and tyre inspections | S1, S2, S4, S5, S6, S7 | `prior_defects_closed` (noul); `within_interval` (noul); `disposition` (choice); `rectify_urgency` (score); `failed_checks` (score) | 24 |
| F222 | research ethics application screening | S1, S3, S4, S5, S6, S7 | `procedures_disclosed` (noul); `retention_within_consent` (noul); `screening_disposition` (choice); `screening_urgency` (score); `residual_risk` (score) | 25 |
| F223 | allotment plot tenancy inspections | S2, S3, S4, S5, S6, S7 | `cultivation_breach` (noul); `notice_ladder_met` (noul); `next_action` (choice); `recurrence_count` (score); `uncultivated_extent` (score) | 25 |
| F224 | dental radiograph quality audits | S1, S3, S4, S5, S6, S7 | `justified` (noul); `operator_retake` (noul); `follow_up` (choice); `dose_position` (score); `unjustified_count` (score) | 25 |
| F225 | waste transfer notes at a recycling centre | S1, S2, S3, S4, S5, S6, S7 | `code_matches_load` (noul); `load_disposition` (choice); `follow_up` (choice); `weight_variance` (score); `doc_gaps` (score) | 25 |
| F226 | scaffold handover inspections | S1, S3, S4, S5, S6, S7 | `design_conformity` (noul); `handover_decision` (choice); `limiting_issue` (choice); `discrepancy_size` (score); `releasable_share` (score) | 25 |
| F227 | apprenticeship progress reviews | S2, S3, S4, S5, S6, S7 | `gateway_on_track` (noul); `review_disposition` (choice); `slippage_source` (choice); `otj_shortfall` (score); `ksb_coverage` (score) | 25 |
| F228 | shipping container weight verification at a port | S1, S3, S4, S5, S6, S7 | `vgm_understated` (noul); `disposition` (choice); `gap_source` (choice); `gap_magnitude` (score); `time_pressure` (score) | 25 |
| F229 | vineyard harvest and pressing logs | S1, S2, S4, S5, S6, S7 | `yield_consistent` (noul); `chain_intact` (noul); `release_decision` (choice); `pick_press_delay` (score); `failed_checks` (score) | 25 |
| F230 | care home medication rounds | S1, S3, S4, S5, S6, S7 | `dose_mismatch` (noul); `stock_reconciles` (noul); `next_step` (choice); `open_discrepancies` (score); `error_severity` (score) | 25 |
| F231 | film location permit applications to a council | S2, S3, S4, S5, S6, S7 | `insurance_valid` (noul); `consultation_met` (noul); `next_step` (choice); `recurrence_count` (score); `highway_impact` (score) | 25 |
| F232 | observatory night observing logs | S1, S3, S4, S5, S6, S7 | `weather_only_loss` (noul); `claims_supported` (noul); `night_disposition` (choice); `usable_share` (score); `fault_followup` (score) | 25 |
| F233 | medical tent logs at a marathon | S1, S2, S3, S4, S5, S6, S7 | `heat_stroke_supported` (noul); `review_action` (choice); `presentation_category` (choice); `obs_completeness` (score); `worst_consciousness` (score) | 25 |
| F234 | seed bank germination tests | S1, S3, S4, S5, S6, S7 | `result_valid` (noul); `next_step` (choice); `shortfall_cause` (choice); `discrepancy_size` (score); `germ_decline` (score) | 25 |
| F235 | river level gauge maintenance visits | S2, S3, S4, S5, S6, S7 | `sensor_fault_cause` (noul); `visit_disposition` (choice); `data_treatment` (choice); `offset_size` (score); `residual_defect` (score) | 25 |
| F236 | bakery allergen changeover records | S1, S3, S4, S5, S6, S7 | `swabs_cleared` (noul); `line_disposition` (choice); `worst_deficiency` (choice); `exposed_product` (score); `residue_evidence` (score) | 25 |
| F237 | electrical installation test certificates | S1, S2, S4, S5, S6, S7 | `results_match_install` (noul); `tested_before_signing` (noul); `submission_disposition` (choice); `untested_circuits` (score); `failed_checks` (score) | 25 |
| F238 | sports pitch condition inspections before matches | S1, S3, S4, S5, S6, S7 | `playable_as_is` (noul); `readings_agree` (noul); `fixture_decision` (choice); `failing_zones` (score); `hazard_severity` (score) | 25 |
| F239 | archive digitisation quality checks | S2, S3, S4, S5, S6, S7 | `pages_complete` (noul); `defects_original` (noul); `disposition` (choice); `recurrence_count` (score); `recapture_share` (score) | 25 |
| F240 | solar farm inverter fault logs | S1, S3, S4, S5, S6, S7 | `genuine_defect` (noul); `post_repair_repeat` (noul); `next_step` (choice); `yield_loss` (score); `capacity_unavailable` (score) | 25 |

- **Skill shares of families:** {"S1": 0.75, "S2": 0.5, "S3": 0.875, "S4": 1.0, "S5": 1.0, "S6": 1.0, "S7": 1.0}.
- **Domains:** 40.

## Label shape (R22.4.3)

| Type | Questions | top < 0.5 | 0.5–0.7 | 0.7–0.9 | ≥ 0.9 | mean top | pilot 2 mean top | mean entropy |
|---|---|---|---|---|---|---|---|---|
| noul | 1494 | 0% | 26% | 38% | 36% | 0.803 | 0.788 | 0.433 |
| choice | 1497 | 26% | 48% | 23% | 3% | 0.608 | 0.617 | 0.991 |
| score | 1994 | 16% | 38% | 37% | 9% | 0.679 | 0.657 | 0.839 |

- **Contested share** (the three judges' top answers disagree): 19%.
- **Top-answer position:** score {"lowest": 0.159, "middle": 0.62, "highest": 0.22}; choice {"first": 0.106, "middle": 0.713, "last": 0.181}.
- **True/false:** `true` is top in 48%; `criteria: null` in 33%.
- **Score mass two or more levels from the top:** 0.07 on average.
- **Gold zeros:** 0.
- **Records:** median 119 words (p10 71, p90 173, maximum 200).
- **Near-duplicate pairs within a family:** 0.

## Every check

| Check | Value | Target | Result |
|---|---|---|---|
| noul share top <0.5 | 0.0 | [0, 0] | pass |
| noul share top 0.5-0.7 | 0.262 | [0.3, 0.4] | **miss** |
| noul share top 0.7-0.9 | 0.375 | [0.28, 0.38] | pass |
| noul share top >=0.9 | 0.363 | [0.27, 0.37] | pass |
| noul mean top | 0.803 | [0.75, 0.81] | pass |
| noul mean entropy | 0.433 | [0.4, 0.5] | pass |
| choice share top <0.5 | 0.26 | [0.15, 0.25] | **miss** |
| choice share top 0.5-0.7 | 0.476 | [0.38, 0.5] | pass |
| choice share top 0.7-0.9 | 0.23 | [0.17, 0.27] | pass |
| choice share top >=0.9 | 0.033 | [0.1, 0.18] | **miss** |
| choice mean top | 0.608 | [0.62, 0.68] | **miss** |
| choice mean entropy | 0.991 | [0.75, 0.92] | **miss** |
| score share top <0.5 | 0.157 | [0.18, 0.28] | **miss** |
| score share top 0.5-0.7 | 0.384 | [0.45, 0.57] | **miss** |
| score share top 0.7-0.9 | 0.373 | [0.15, 0.25] | **miss** |
| score share top >=0.9 | 0.086 | [0.03, 0.09] | pass |
| score mean top | 0.679 | [0.58, 0.64] | **miss** |
| score mean entropy | 0.839 | [0.83, 0.98] | pass |
| contested share (judges' tops disagree) | 0.192 | [0.3, 0.4] | **miss** |
| score top at lowest | 0.159 | [0.1, 0.16] | pass |
| score top at middle | 0.62 | [0.57, 0.67] | pass |
| score top at highest | 0.22 | [0.22, 0.3] | pass |
| choice top at first | 0.106 | [0.15, 0.25] | **miss** |
| choice top at middle | 0.713 | [0.6, 0.7] | **miss** |
| choice top at last | 0.181 | [0.1, 0.18] | **miss** |
| noul true top | 0.483 | [0.45, 0.5] | pass |
| noul criteria null | 0.333 | [0.3, 0.36] | pass |
| score mass >= 2 levels from top (mean) | 0.07 | [0, 0.1] | pass |
| F201 contested share | 0.32 | [0.15, 0.55] | pass |
| F201 noul true top | 0.32 | [0.25, 0.7] | pass |
| F202 contested share | 0.28 | [0.15, 0.55] | pass |
| F202 noul true top | 0.76 | [0.25, 0.7] | **miss** |
| F203 contested share | 0.368 | [0.15, 0.55] | pass |
| F203 noul true top | 0.32 | [0.25, 0.7] | pass |
| F204 contested share | 0.232 | [0.15, 0.55] | pass |
| F204 noul true top | 0.36 | [0.25, 0.7] | pass |
| F205 contested share | 0.142 | [0.15, 0.55] | **miss** |
| F205 noul true top | 0.25 | [0.25, 0.7] | pass |
| F206 contested share | 0.128 | [0.15, 0.55] | **miss** |
| F206 noul true top | 0.5 | [0.25, 0.7] | pass |
| F207 contested share | 0.112 | [0.15, 0.55] | **miss** |
| F207 noul true top | 0.44 | [0.25, 0.7] | pass |
| F208 contested share | 0.208 | [0.15, 0.55] | pass |
| F208 noul true top | 0.46 | [0.25, 0.7] | pass |
| F209 contested share | 0.224 | [0.15, 0.55] | pass |
| F209 noul true top | 0.08 | [0.25, 0.7] | **miss** |
| F210 contested share | 0.184 | [0.15, 0.55] | pass |
| F210 noul true top | 0.8 | [0.25, 0.7] | **miss** |
| F211 contested share | 0.136 | [0.15, 0.55] | **miss** |
| F211 noul true top | 0.56 | [0.25, 0.7] | pass |
| F212 contested share | 0.128 | [0.15, 0.55] | **miss** |
| F212 noul true top | 0.68 | [0.25, 0.7] | pass |
| F213 contested share | 0.208 | [0.15, 0.55] | pass |
| F213 noul true top | 0.52 | [0.25, 0.7] | pass |
| F214 contested share | 0.175 | [0.15, 0.55] | pass |
| F214 noul true top | 0.312 | [0.25, 0.7] | pass |
| F215 contested share | 0.192 | [0.15, 0.55] | pass |
| F215 noul true top | 0.62 | [0.25, 0.7] | pass |
| F216 contested share | 0.128 | [0.15, 0.55] | **miss** |
| F216 noul true top | 0.54 | [0.25, 0.7] | pass |
| F217 contested share | 0.088 | [0.15, 0.55] | **miss** |
| F217 noul true top | 0.56 | [0.25, 0.7] | pass |
| F218 contested share | 0.128 | [0.15, 0.55] | **miss** |
| F218 noul true top | 0.48 | [0.25, 0.7] | pass |
| F219 contested share | 0.128 | [0.15, 0.55] | **miss** |
| F219 noul true top | 0.88 | [0.25, 0.7] | **miss** |
| F220 contested share | 0.16 | [0.15, 0.55] | pass |
| F220 noul true top | 0.56 | [0.25, 0.7] | pass |
| F221 contested share | 0.225 | [0.15, 0.55] | pass |
| F221 noul true top | 0.646 | [0.25, 0.7] | pass |
| F222 contested share | 0.2 | [0.15, 0.55] | pass |
| F222 noul true top | 0.64 | [0.25, 0.7] | pass |
| F223 contested share | 0.184 | [0.15, 0.55] | pass |
| F223 noul true top | 0.44 | [0.25, 0.7] | pass |
| F224 contested share | 0.264 | [0.15, 0.55] | pass |
| F224 noul true top | 0.46 | [0.25, 0.7] | pass |
| F225 contested share | 0.12 | [0.15, 0.55] | **miss** |
| F225 noul true top | 0.44 | [0.25, 0.7] | pass |
| F226 contested share | 0.28 | [0.15, 0.55] | pass |
| F226 noul true top | 0.8 | [0.25, 0.7] | **miss** |
| F227 contested share | 0.2 | [0.15, 0.55] | pass |
| F227 noul true top | 0.16 | [0.25, 0.7] | **miss** |
| F228 contested share | 0.192 | [0.15, 0.55] | pass |
| F228 noul true top | 0.44 | [0.25, 0.7] | pass |
| F229 contested share | 0.176 | [0.15, 0.55] | pass |
| F229 noul true top | 0.46 | [0.25, 0.7] | pass |
| F230 contested share | 0.2 | [0.15, 0.55] | pass |
| F230 noul true top | 0.72 | [0.25, 0.7] | **miss** |
| F231 contested share | 0.152 | [0.15, 0.55] | pass |
| F231 noul true top | 0.42 | [0.25, 0.7] | pass |
| F232 contested share | 0.128 | [0.15, 0.55] | **miss** |
| F232 noul true top | 0.14 | [0.25, 0.7] | **miss** |
| F233 contested share | 0.184 | [0.15, 0.55] | pass |
| F233 noul true top | 0.44 | [0.25, 0.7] | pass |
| F234 contested share | 0.28 | [0.15, 0.55] | pass |
| F234 noul true top | 0.24 | [0.25, 0.7] | **miss** |
| F235 contested share | 0.224 | [0.15, 0.55] | pass |
| F235 noul true top | 0.48 | [0.25, 0.7] | pass |
| F236 contested share | 0.176 | [0.15, 0.55] | pass |
| F236 noul true top | 0.36 | [0.25, 0.7] | pass |
| F237 contested share | 0.216 | [0.15, 0.55] | pass |
| F237 noul true top | 0.56 | [0.25, 0.7] | pass |
| F238 contested share | 0.168 | [0.15, 0.55] | pass |
| F238 noul true top | 0.28 | [0.25, 0.7] | pass |
| F239 contested share | 0.232 | [0.15, 0.55] | pass |
| F239 noul true top | 0.56 | [0.25, 0.7] | pass |
| F240 contested share | 0.2 | [0.15, 0.55] | pass |
| F240 noul true top | 0.66 | [0.25, 0.7] | pass |
| every family has exactly 5 questions | True | True | pass |
| records have 3-6 sections | [3, 6] | [3, 6] | pass |
| record words max <= 320 | 200 | [0, 320] | pass |
| skill S1 share of families | 0.75 | [0.4, 1] | pass |
| skill S2 share of families | 0.5 | [0.25, 1] | pass |
| skill S3 share of families | 0.875 | [0.5, 1] | pass |
| at least 6 domains | 40 | [6, null] | pass |
| no near-duplicate records in a family (>50% of field values equal) | 0 | 0 | pass |

## Where the set misses the targets

33 of 116 checks miss. 13 are overall checks and 20 are per-family checks (11 contested share, 9 `true` top share).

- **Fewer contested questions than asked:** 19% against 30–40%, with 11 families below 15%. Pilot 2 had 40% with five judges from three models. The cause is the R26 judge setup:
  - Three stances of one model (Haiku) disagree on the top answer much less often than five judges from three models.
  - Sampling temperature cannot be set on these models, so the three samples cannot be spread further that way.
  - The gold is still the plain mean of the three; nothing was adjusted towards the target.
- **Score gold is sharper than asked:** mean top 0.679 against 0.58–0.64. 37% of score questions have a top at 0.7–0.9, against 15–25%; 16% are under 0.5, against 18–28%.
  - The plans were already softened from pilot 2 (which measured 0.657).
  - The Haiku judges settle clear anchored scale records more firmly than the mixed panel did.
- **Choice gold is slightly soft:** mean top 0.608 against 0.62–0.68; 3% of choice questions at ≥ 0.9 against 10–18%; entropy 0.99 against 0.75–0.92.
  - More choice plans were made clear than in pilot 2.
  - A single Haiku judge rarely puts more than 0.85 on one option of four or five.
- **Choice top position:** the first option is top in 11% of choice questions (target 15–25%), middle options in 71% (60–70%) and the last in 18% (10–18%). Code planned 32% first-option answers, but the judges often move first-option ("no action") plans to a middle option.
- **True/false:** the 0.5–0.7 band holds 26% against 30–40%. `true` is top in 48% overall, inside the target, but outside 25–70% in 9 families.
- **Records are longer than R22.2.2's "about 70 words":** median 119, p90 173.
  - The smoke test showed that a length band tied to each record's target dropped most records in some families.
  - With no rework allowed, the rule became a plain 200-word ceiling.
- **Three families have 24 records instead of 25:** F205, F214 and F221. The top-up was sized from the main run's yield; for these three it came out one short.

Everything else passes:
- format and structure;
- the `true`/`false` overall share and `criteria: null` share;
- score positions;
- skill shares;
- no gold zeros and no near-duplicate pairs;
- score mass two or more levels from the top at 7%.

## Cost

| Stage | Cost (USD) |
|---|---|
| scales | 0.02 |
| family | 6.08 |
| records | 33.3 |
| judge | 3.18 |
| **total** | **42.58** |

- **By model:** {"claude-opus-5-5": 6.1, "claude-sonnet-5-5": 33.3, "claude-haiku-5-5": 3.18}.
- **Requests:** 7917 in total, 7875 of them through the Batches API.
- **Includes:** the smoke test and the top-up, and every dropped record and retry.

## Licence

Released to the Signpost-D team without restriction (CC0).
