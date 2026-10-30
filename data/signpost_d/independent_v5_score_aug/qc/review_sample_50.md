# Review sample: 50 cases (10 random per flow)

## SCORE-F1-0084  ·  F1 Evidence-based scoring  ·  pharmacy dispensing  ·  email thread

```
From: Priya Nandakumar <p.nandakumar@hollinsgatepharmacy.co.uk>
To: Dispensing Desk <dispensing@hollinsgatepharmacy.co.uk>
Cc: Tomasz Wierzbicki <t.wierzbicki@hollinsgatepharmacy.co.uk>
Date: Tue 27 Oct 2026 16:42
Subject: RE: Collection query - Mrs D. Ashdown - Rx 4471-0932-7

Tom, thanks for picking this up. I know it's been a long week and the bag labels have been a nightmare since the printer swap on Thursday, so I'm not going to blame anyone for the mix-up. Just wanted it on record properly before the end of shift.

Mrs Ashdown rang at 14:10 asking why her Ramipril was "in the wrong bag". She has the tablets, they are the right strength, but the bag label showed the Amlodipine from the same surname, DOB 03/07/1951 vs 03/07/1961 on the other. Checked the PMR: both were ready at 11:30, the bag was pulled by the wrong shelf. Nobody reconciled the bag against the label before handing over. I did the counter check myself at 14:25 and it was fine after that.

Anyway, to be honest the log entry for the Ramipril handover is wrong too. It says "checked by RP" at 11:52 but I was on the phone to the GP surgery until 12:15 and Anjali did the hand-over. I've asked her to correct it.

Also, as a side note, the fridge probe on the dispensary side read 9.1°C at 15:00, which is over the limit, and the ticket to the engineer was only raised this morning. Not related to Mrs A, but it should go in the same review.

Priya

--- Original message ---
From: Tomasz Wierzbicki
Sent: Tue 27 Oct 2026 09:05
Subject: Collection query - Mrs D. Ashdown - Rx 4471-0932-7

Morning all. Mrs Ashdown has asked us to confirm which bag her meds went in. Dispensing log says Rx 4471-0932-7 (Ramipril 5mg, 28 tabs) and the second item 4471-0940-2 (Amlodipine 5mg) were both collected 27/10 at 12:04 by the patient. I can't find an RP check against the Amlodipine line. Can someone look?

Tom
Dispensary Technician, Hollingsgate Pharmacy
```

**q1 [judge]** As the locum pharmacist, rate how serious the patient-safety consequence of the bag mix-up in Mrs Ashdown's collection is, judged on the evidence in the emails as at 27 Oct 2026.  
  `0` = Negligible: no wrong-patient medicine reached the patient and nothing needs follow-up; `1` = Moderate: a wrong-patient or mislabelled item reached the patient, but no harm is indicated and the matter has been checked or contained; `2` = Severe: harm is indicated, or the wrong-patient supply remains uncorrected with an ongoing risk to a patient  
  gold: {"0": 0.035, "1": 0.8775, "2": 0.0875} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [read]** Count the corrections to dispensing log entries that the emails state have actually been completed (not merely requested) by the end of Priya's message on 27 Oct 2026.  
  `0` = None: no log correction is stated as completed; `1` = One: exactly one log correction is stated as completed; `2` = Two: exactly two log corrections are stated as completed; `3` = Three or more: at least three log corrections are stated as completed  
  gold: {"0": 0.92, "1": 0.0525, "2": 0.0175, "3": 0.01} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** Rate how strongly the emails link the fridge temperature excursion to the Ashdown bag mix-up as a cause or contributing factor, from the pharmacist's reading of the document.  
  `0` = None: the document treats the fridge issue as separate and unrelated to the mix-up; `1` = Slight: the document hints at a possible indirect connection; `2` = Substantial: the document indicates the fridge issue contributed to the mix-up; `3` = Direct: the document states the fridge issue caused the mix-up  
  gold: {"0": 0.925, "1": 0.0625, "2": 0.01, "3": 0.0025} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** Using the logged collection time and the time Mrs Ashdown phoned about the bag on 27 Oct 2026, rate the gap in minutes from collection to her call.  
  `0` = Under 30: less than 30 minutes; `1` = 30 to under 60: at least 30 but below 60 minutes; `2` = 60 to under 120: at least 60 but below 120 minutes; `3` = 120 to under 180: at least 120 but below 180 minutes; `4` = 180 or more: at least 180 minutes  
  gold: {"0": 0.0025, "1": 0.0025, "2": 0.0225, "3": 0.96, "4": 0.0125} · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F1-0105  ·  F1 Evidence-based scoring  ·  solar installation  ·  system record

```json
{
 "record_id": "SCV-2026-0917-443",
 "export_ts": "2026-10-29T16:42:08Z",
 "source_system": "SolarField Survey & Commissioning v4.7.2",
 "job_ref": "JOB-NW-08812",
 "site": {
  "site_id": "S-40177",
  "addr_line1": "14 Harrowgate Close",
  "addr_line2": null,
  "postcode": "LS17 6QP",
  "region_code": "YKS-W",
  "access_notes": "Side gate code 4471 (customer changed 12/10, confirm)"
 },
 "customer": {
  "cust_ref": "CU-227903",
  "name": "Mrs P. Abernethy-Doyle",
  "contact_tel": "0113 496 2208",
  "preferred_contact": "email",
  "vulnerability_flag": "N"
 },
 "survey": {
  "survey_date": "2026-10-14",
  "surveyor_id": "EMP-0581",
  "roof_pitch_deg": 34,
  "roof_orientation": "SSW",
  "shading_pct": "12",
  "meter_type": "SMART_SINGLE_PH",
  "consumer_unit_age_yrs": null,
  "rafter_check_done": "Y"
 },
 "system": {
  "pv_kwp": "6.12",
  "panel_count": 12,
  "panel_model": "PX-410 Mono",
  "inverter_model": "HL-5K-G3",
  "battery_kwh": null,
  "install_date": "2026-10-27",
  "install_crew": "CREW-C",
  "eic_cert_no": "EIC-88214-P"
 },
 "commissioning": {
  "commission_ts": "2026-10-28T11:15:00Z",
  "inverter_serial": "HL5G3-22091847",
  "string_voltage_v": "368.4",
  "insulation_mohm": "> 200",
  "earth_loop_ohm": "0.31",
  "dc_isolator_tested": true,
  "commission_sign_off": "EMP-0644",
  "photos_uploaded": "9"
 },
 "remarks": {
  "surveyor_note": "Consumer unit confirmed as 2009 Wylex, no RCD issue. Roof sound throughout, all 12 fixings to rafters.",
  "install_note": "Crew says consumer unit is 2019 replacement, not 2009, per homeowner. Did not see label. Customer happy with install.",
  "complaint_flag": "N",
  "complaint_detail": null
 },
 "finance": {
  "contract_value_gbp": "8640.00",
  "deposit_paid_gbp": "1728.00",
  "finance_provider": null,
  "sales_rep_id": "EMP-0212"
 },
 "notes": "Surveyor and install crew disagree on the consumer unit date and the installed board has not been photographed by either party. Commissioning completed without issue and the customer has accepted the install on the portal. Gate code to be confirmed before next visit.",
 "_legacy_ref": "SF-OLD-1190",
 "print_colour": "ff3300"
}
```

**q1 [read]** How many of the three commissioning electrical test readings (insulation resistance, earth loop impedance, string voltage) are recorded with a numeric or bounded value in the commissioning section of this record?  
  `0` = Zero or one: at most one of the three readings is recorded; `1` = Two: exactly two of the three readings are recorded; `2` = Three: all three readings are recorded  
  gold: {"0": 0.028, "1": 0.052, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [read]** How many separate entries in this record state that the customer has made a complaint or reported dissatisfaction with the installation?  
  `0` = None: no entry states a complaint or dissatisfaction; `1` = One: exactly one entry states a complaint or dissatisfaction; `2` = Two or more: at least two entries state this  
  gold: {"0": 0.92, "1": 0.0576, "2": 0.0224} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** From the sales administrator's view, how much confidence can be placed in the record's stated age of the consumer unit, given the evidence in the record?  
  `0` = Very little: the evidence is contradictory and unverified; `1` = Low: some support but substantial doubt remains; `2` = Moderate: leaning one way with some verification; `3` = High: well supported with minor doubt; `4` = Very high: verified and consistent across sources  
  gold: {"0": 0.8625, "1": 0.1225, "2": 0.015, "3": 0.0, "4": 0.0} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [read]** How many of the survey and system fields in the record hold a null (missing) value?  
  `0` = None: no such field is null; `1` = One: exactly one is null; `2` = Two: exactly two are null; `3` = Three: exactly three are null; `4` = Four or more: at least four are null  
  gold: {"0": 0.0136, "1": 0.0392, "2": 0.92, "3": 0.0181, "4": 0.0091} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F1-0069  ·  F1 Evidence-based scoring  ·  procurement  ·  incident report

```
INCIDENT REPORT – PROCUREMENT SERVICES
Ref: PS-INC-2026-0417
Tender ref: UOR/PS/26/0931 (Supply and installation of lecture capture kit, Rooms B2.14–B2.19)
Reported by: Dariusz Okonkwo, Procurement Officer (Small Tenders)
Date of report: 28/10/2026
Date of event: 22/10/2026

Background and narrative

Some of this is a bit of a long story, so bear with me. The tender closed on 9 October at 12:00 and we received three returns, which was one more than I expected given the short notice. Brightwater AV Ltd sent the bulk of their pricing schedule on the portal but their method statement arrived as a scanned PDF of what looks like a previous client's document, with the client name still visible on page 3 and page 7. Facilities (Mervyn Clough) said the photographs of the install were "lovely" but nobody asked for them. Anyway, to get to the point of the event:

Timeline (times from portal audit log and email headers)

22/10 09:14 – Brightwater site visit booked for Room B2.16 by Facilities.
22/10 10:02 – Installer (contractor, two persons) on site. Ceiling cable route surveyed.
22/10 11:40 – Ceiling tile damaged in B2.16 (approx. 600 x 600 mm). Reported verbally to Facilities duty desk.
22/10 11:52 – Contractor states tile was "already cracked". No photographic evidence taken at the time.
22/10 14:30 – Lecture capture unit tested: 3 of 6 units returned no audio on channel 2 (per test sheet, signed Clough).
22/10 16:05 – Brightwater quote revised by email from £18,450.00 to £18,540.00 (+£90.00 "mounting bracket upgrade"). Revision not on original submission.

Witness remarks

Mervyn Clough (Facilities): "I didn't see the tile go, I was in the corridor. The two lads were very polite though, and one of them made me a tea which I thought was nice of him."

Sana Lindqvist (Teaching Estates): "Room B2.16 was fine on Tuesday when I did my walkthrough. I don't know what the audio issue is, I'm not technical."

Contractor site lead (unnamed on sign-in sheet): "Tile was like that when we got there, honest."

Figures

The revised total was originally logged as £18,450.00 in the evaluation spreadsheet (cell F22). Correct figure per email of 22/10 is £18,540.00. Evaluation spreadsheet to be amended.

Actions

Facilities to log tile damage with estates. Procurement to request a written statement from Brightwater regarding the revised quote and the method statement. Retest of channel 2 scheduled for 29/10.

Signed: D. Okonkwo
```

**q1 [infer]** By how much, in pounds, did the Brightwater quote increase from the originally submitted figure to the corrected revised total, as shown by the report's email evidence of 22/10/2026?  
  `0` = Zero: no increase, or a decrease; `1` = Small: an increase above £0 but below £25; `2` = Moderate: an increase of at least £25 but below £75; `3` = Larger: an increase of £75 or more  
  gold: {"0": 0.0229, "1": 0.02, "2": 0.0371, "3": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [read]** How many of the six lecture capture units tested on 22/10/2026 returned no audio on channel 2, according to the signed test sheet reported?  
  `0` = Few: none or one unit failed; `1` = Some: at least two but fewer than four units failed; `2` = Most: at least four but fewer than six units failed; `3` = All: all six units failed  
  gold: {"0": 0.0305, "1": 0.92, "2": 0.0343, "3": 0.0152} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [read]** How much photographic evidence of the damaged ceiling tile in B2.16 does the report say was taken at the time of the incident?  
  `0` = None: the report states no photographic evidence was taken at the time; `1` = Partial: some photographs are reported but not of the tile's condition before the damage; `2` = Full: photographs of the tile before and after the damage are reported  
  gold: {"0": 0.92, "1": 0.0565, "2": 0.0235} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [read]** How many witnesses in the report say they personally saw the ceiling tile being damaged?  
  `0` = None: no witness reports seeing the damage happen; `1` = One: exactly one witness reports seeing it; `2` = Two or more: at least two witnesses report seeing it  
  gold: {"0": 0.92, "1": 0.0545, "2": 0.0255} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F1-0128  ·  F1 Evidence-based scoring  ·  residential lettings  ·  meeting notes

```
Hartwell & Lowe Lettings – Internal Meeting Notes

Meeting: Portfolio maintenance review (north side)
Date: Thursday 29 October 2026, 08:30–08:52
Location: Room 2, Unit 4 Calder Court, Bradford BD1 4QT (video link also open)
Attendees: Priya Desai (Property Manager), Tom Okonjo (Maintenance Coordinator), Leanne Briggs (Landlord Liaison), Ravi Sandhu (Contractor – Sandhu Plumbing & Heating), Mo Farrow (Inventory Clerk)
Apologies: Dan Whitcombe

1. Flat 3, 18 Ashgrove Road (rented to Mr and Mrs E. Pryce from 1 March 2025). Boiler service overdue. Ravi reports the Worcester Bosch unit was last serviced 14 months ago; gas safety certificate expires 9 November. Tom says the certificate was renewed on 14 May and the file is wrong. Not resolved – Tom to check the portal.

2. Damp reported in the rear bedroom of 42 Linden Terrace. Tenant log shows 3 calls since 2 September. Mo measured wall moisture at 19% (north wall) and 14% (party wall); Ravi says the damp is condensation, not penetrating, and quotes 2 hrs 40 mins labour for extractor fan and vent. Leanne disputes the tenant's account that the room has been "unusable since August"; the tenant's own log entries say 11 days.

3. Kitchen extractor at 7 Mill Lane: replaced 22 October. Tenant feedback recorded as "fine, a bit loud". No further action.

4. Rent arrears, Flat 1, 3 Fenton Way: £1,140 outstanding (roughly 2.5 months at £456 pcm). Leanne reports one payment of £300 received 27 October. Priya states arrears are 2 months; Leanne states 2.5. Figure to be confirmed against the ledger before the landlord letter goes out.

5. Coal-shed gate, Calder Court bin store: rehung. Weight of replacement hinge set 1.8 kg, cost £64.20. Mo noted the store was clean and the bin lids were closed. Brief.

6. Inventory check-out for Flat 2, 88 Pennine View (vacated 15 October): 14 items logged, 2 missing (cutlery set, one lamp). Deposit deduction discussion deferred.

Actions:
- Tom: check gas safety certificate file for 18 Ashgrove Road by Monday 2 November.
- Ravi: send written quote for 42 Linden Terrace, itemised, by Friday 6 November.
- Mo: re-measure damp readings at 42 Linden Terrace, 1 m from the wall, on 3 November.
- Leanne: reconcile Fenton Way ledger and confirm arrears figure to Priya.
- Priya: circulate revised maintenance schedule (v3) to the group.

Next meeting: Thursday 12 November, 08:30.

Notes taken by: Dan Whitcombe (circulated 30 October)
```

**q1 [infer]** Using the outstanding balance and monthly rent stated for Flat 1, 3 Fenton Way, how many months of rent are in arrears? Rate the balance divided by monthly rent, unrounded.  
  `0` = Under one month: less than 1.00 months; `1` = One to under two: at least 1.00 but below 2.00 months; `2` = Two to under two and a quarter: at least 2.00 but below 2.25 months; `3` = Two and a quarter or more: at least 2.25 months  
  gold: {"0": 0.02, "1": 0.02, "2": 0.04, "3": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [read]** What is the highest wall moisture reading recorded in the rear bedroom of 42 Linden Terrace at the meeting, as a percentage?  
  `0` = Low: below 10%; `1` = Moderate: at least 10% but below 15%; `2` = High: 15% or above  
  gold: {"0": 0.0267, "1": 0.0533, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [read]** How much further action does the meeting record as still needed on the kitchen extractor at 7 Mill Lane?  
  `0` = None: the record says no further action is needed; `1` = Minor follow-up: a small check, call or adjustment is still needed; `2` = Substantial work: further repair, replacement or a new visit is still needed  
  gold: {"0": 0.92, "1": 0.0622, "2": 0.0178} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [read]** How many of the six numbered agenda items contain a disagreement over the facts between named parties (including a tenant's account) that the notes leave unresolved?  
  `0` = None: no item has an unresolved factual disagreement; `1` = One: exactly one item has one; `2` = Two: exactly two items have one; `3` = Three or more: at least three items have one  
  gold: {"0": 0.0025, "1": 0.0225, "2": 0.0925, "3": 0.8825} · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F1-0049  ·  F1 Evidence-based scoring  ·  home insurance  ·  form submission

```
HOMEWISE INSURANCE PLC — CONTENTS CLAIM FORM (SUBMITTED ONLINE)

Claim reference: HW-CC-2026-048213
Date submitted: 14/10/2026 17:42
Channel: Web portal (agent-assisted: No)
Policy number: HWP-7714-220-B
Policy type: Home Contents Plus (Buildings excluded)
Cover limit (contents): £35,000
Excess applied: £250

SECTION 1 — POLICYHOLDER
Title: Mr
Full name: Tomasz Wierzbicki
Date of birth: 22/03/1971
Address line 1: 14 Harrowgate Close
Address line 2: (blank)
Town: Lowmoor
Postcode: LM9 4QT
Contact telephone: 07700 900 418
Email: t.wierzbicki@ferngrove-mail.example
Preferred contact time: Morning (09:00–12:00)

SECTION 2 — INCIDENT DETAILS
Type of loss: Escape of water
Date of loss: 09/10/2026
Time discovered: 06:15
Time reported to Homewise: 17:20
Date reported: 13/10/2026
Police reference: (blank)
Was property occupied at time of loss: Yes
Location of loss: Ground floor utility room, kitchen (rear)
Description of loss: Washing machine supply hose split overnight. Floor covered approx 3.2 m² and 4 cm depth water on laminate. Wet items moved upstairs by partner.

SECTION 3 — ITEMISED ITEMS CLAIMED
Item 1: Washing machine (Beko WTL74) | Age: 6 yrs | Value: £289.00 | Claimed: £289.00
Item 2: Laminate flooring (kitchen/utility) | Area: 31 sq ft | Value: £840.00 | Claimed: £840.00
Item 3: Sofa, 3-seater (fabric) | Weight (est.): 62 lb | Value: £1,150.00 | Claimed: £1,150.00
Item 4: Dehumidifier hire | Hours: 52 hrs | Rate: £6.50/day | Claimed: £58.50
Item 5: Television (Samsung 55") | Value: £620.00 | Claimed: £
Item 6: Drying out (professional) | Duration: 2.5 days | Claimed: £410.00
Total claimed: £3,767.50

SECTION 4 — DECLARATIONS
Previous claims in last 5 years: No
Loss reported to any other insurer: No
Signature (typed): T. Wierzbicki
Date: 13/10/2026

SECTION 5 — ASSESSOR USE ONLY
Assessor: (unassigned)
Site visit required: Yes
Site visit date: 
Moisture reading (kitchen wall, rear): 18 %WME
Moisture reading (utility floor): 22 kg/m³ (meter 2)
Assessor notes: 

SECTION 6 — COMMENTS (customer)
Hi, I reported this on Tuesday evening as soon as I could, I had been up since the early hours trying to sort the floor out so I didn't get to the phone until after work. The first call handler said someone would ring me within 48 hours and nobody has. I've now been told by the portal the claim is "under review" for 17 days with no contact. The dehumidifier was on for 52 hours, the company said I should only claim 2 days. My wife has been sleeping in the front room because of the smell and the kids have had coughs. The TV was not in the utility, it was in the lounge and was not affected, I think I put the wrong thing in the box by mistake. Please ring me before 12, I work afternoons. Thanks.

```

**q1 [read]** How many whole calendar days passed between the stated date of loss and the stated date the loss was reported to Homewise, according to the claim form's incident section?  
  `0` = Same day: zero days between loss and report; `1` = Short delay: at least 1 day but fewer than 3 days; `2` = Longer delay: 3 days or more  
  gold: {"0": 0.0311, "1": 0.0489, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [read]** According to the customer's comments, for how many days has the claim been shown as 'under review' with no contact from Homewise, as at the comment being written?  
  `0` = Under a week: fewer than 7 days; `1` = One to two weeks: at least 7 but fewer than 14 days; `2` = Two to three weeks: at least 14 but fewer than 21 days; `3` = Three weeks or more: 21 days or more  
  gold: {"0": 0.0195, "1": 0.0312, "2": 0.92, "3": 0.0293} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [read]** What is the stated total claimed on the form as a share of the contents cover limit shown, rounded to one decimal place?  
  `0` = Very small: below 5.0%; `1` = Small: at least 5.0% but below 10.0%; `2` = Moderate: at least 10.0% but below 15.0%; `3` = Large: 15.0% or more  
  gold: {"0": 0.0193, "1": 0.0386, "2": 0.92, "3": 0.0221} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [read]** How many of the itemised items does the customer's own comment say were unaffected by the water and so wrongly entered on the form?  
  `0` = None: no item is described as unaffected; `1` = One: exactly one item is described as unaffected; `2` = Two or more: at least two items are described as unaffected  
  gold: {"0": 0.0373, "1": 0.92, "2": 0.0427} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F1-0077  ·  F1 Evidence-based scoring  ·  college admissions  ·  policy extract and case note

```
Harrowgate Coast College of Further Education
Admissions Office – Policy Extract and Case Note

POLICY EXTRACT: AD/14 Conditional Offers and Mid-Course Transfer Requests
Version 3.2 | Effective 1 September 2026 | Owner: Head of Admissions (ref. HCC-ADM-POL-014)

14.1 A conditional offer may be made only where the applicant has submitted a complete Application Form (Form AF-2, all sections A to F signed) and the reference from the most recent provider has been received.

14.2 Where a prior qualification is cited as evidence of entry, the applicant must supply the awarding body's certificate or a transcript bearing the awarding body's stamp. Scanned copies are acceptable for provisional decisions only.

14.3 Transfer requests from one course to another within the same faculty shall be considered by the course leader, who shall record a grade band of 1 to 5 against each of the following: (a) academic readiness; (b) attendance and punctuality record over the preceding 12 weeks; (c) safeguarding or welfare concerns logged in the student record; (d) completion of induction tasks.

14.4 A transfer request scoring band 4 or 5 under 14.3(c) shall be referred to the Designated Safeguarding Lead before any decision is communicated.

14.5 EXCEPTION: Clause 14.3(b) does not apply to applicants who have been in custodial or hospital care for a period exceeding six weeks during the preceding 12 weeks. For such applicants the course leader shall record the attendance band as "N/A – exempt" and note the period concerned.

14.6 Decisions on transfer requests shall be communicated in writing within ten working days of receipt. Requests received after the census date of 15 October shall be deferred to the following academic year unless the Head of Admissions approves otherwise.

CASE NOTE: Transfer request TR-2026-0417, Applicant ref. 40718-B
Course: Level 2 Diploma in Motor Vehicle Technology (transferring from Level 2 Diploma in Creative Media, Ashby Road campus)
Received: 19 October 2026. Recorded by: Admissions Officer, N. Ferreira.

Application form AF-2 submitted with sections A to F signed. Provider reference from Brackenmoor Academy received 21 October, dated 3 September 2026. Previous Creative Media attendance from 2 September to 14 October: 31 sessions timetabled, 22 attended, 9 absent (4 authorised). Punctuality logged late on 6 of 22 attended sessions.

Note from tutor M. Adeyemi (Creative Media), 14 October: "Good ideas, very capable on the software, but turns up when it suits. Had a difficult week in the middle, said he'd rather not discuss it yet."

Welfare log entry 9 October, entered by pastoral team: "Student reported a period in the Sandhill Lodge unit from 22 July to 4 September. Discharged, now engaging with community nurse. Consent given for information to be shared with the course team."

Induction task completion, first week: 3 of 5 tasks submitted. Tasks 4 and 5 outstanding.

Initial entry for 14.3(c) was recorded as band 2 by the admissions officer on 20 October. Correction recorded 22 October, after reviewing the welfare log: band 4. Initial entry for 14.3(a) reading from prior qualification: 2 (Level 1 Creative Media, distinction-equivalent portfolio). Officer comment: "Entry tests not yet booked; band provisional."

Attendance band under 14.3(b) recorded as "N/A – exempt" with period noted as 22 July to 4 September (44 days), citing 14.5.

Referral to Designated Safeguarding Lead made 22 October under 14.4. Written decision outstanding; ten-working-day deadline falls on 2 November.

Course leader comments: none recorded.
```

**q1 [judge]** From the course leader's viewpoint, rate how well the case note supports the 'N/A – exempt' attendance entry under clause 14.5, judged against the 12 weeks preceding receipt of the request.  
  `0` = Unsupported: the recorded facts indicate the clause's conditions are not met, or fall short of its threshold; `1` = Arguable: the facts could be read either way, with key conditions left genuinely open; `2` = Well supported: the facts clearly meet every condition of the clause  
  gold: {"0": 0.7, "1": 0.2575, "2": 0.0425} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [judge]** From the course leader's viewpoint, rate how strongly the welfare evidence in the case note justifies the corrected band for 14.3(c), and so the referral to the Designated Safeguarding Lead.  
  `0` = Weak: the evidence points to little or no welfare concern; `1` = Moderate: the evidence shows some concern but leaves the need for referral open; `2` = Strong: the evidence clearly shows a significant, recent and continuing welfare concern  
  gold: {"0": 0.0375, "1": 0.4, "2": 0.5625} · agreement 3/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [read]** Count how many of the four 14.3 criteria (a) to (d) have a numeric grade band recorded in the case note, counting provisional bands and using the latest value where corrected. 'N/A' entries and raw task counts do not count.  
  `0` = None: no criterion has a numeric band recorded; `1` = One: exactly one criterion has a numeric band; `2` = Two: exactly two criteria have a numeric band; `3` = Three: exactly three criteria have a numeric band; `4` = Four: all four criteria have a numeric band  
  gold: {"0": 0.0053, "1": 0.0267, "2": 0.92, "3": 0.0347, "4": 0.0133} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [infer]** Applying clause 14.6 to the dates in the case note, rate how strongly the records indicate that this request must be deferred to the following academic year.  
  `0` = Not indicated: the request was clearly received in time and no deferral applies; `1` = Uncertain: deferral might apply but the records leave the position genuinely open; `2` = Indicated: the request was received late and no approval to proceed appears in the records  
  gold: {"0": 0.021, "1": 0.059, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F1-0001  ·  F1 Evidence-based scoring  ·  school office  ·  policy extract and case note

```
Harrowgate Park School — Administrative Office
Policy extract: Student Equipment Loans and Replacement (Ref: ADM/POL/14, v3.2, reviewed 02/09/2026)

14.1 Chromebook and tablet loans are made to students in Years 7–11 for home study where the Head of Year has approved the request on form ADM/F09.

14.2 Each loan is recorded in the Equipment Register (field EQ_LOAN_ID) with issue date, serial number and the signing parent or carer.

14.3 Borrowers must return the device within 5 school days of the loan end date. Devices not returned within 10 school days are reported to the Bursar as outstanding.

14.4 Where damage is reported, the Network Team inspects the device within 3 working days and grades it A (cosmetic), B (functional, repair needed) or C (write-off).

14.5 Exception: a loan may be extended beyond 10 school days without fresh approval where the student is on a Year 11 exam support plan, provided the Head of Year records the extension in the register notes field before the original end date.

14.6 Exception: grade C devices are not charged to the family where the damage is recorded as occurring on school premises.

Case note (ADM/CN/22, prepared by R. Okafor, Office Assistant, 14/10/2026)

Device CB-0417 (issued to Year 10 student, loan approved 01/09/2026, end date 15/09/2026) was returned on 20/10/2026, 19 school days late. Register notes contain no extension entry.

Student's mother, Mrs T. Lindqvist, states by phone that the device was handed in at reception on 16/09/2026 and signed for by the front desk. The reception log for that week shows 14 entries and no Chromebook intake line.

Head of Year (Mr D. Penrose) email, 15/10/2026, 08:42: "I extended this one verbally during the mock week, it should be in the notes." The register notes field is blank for CB-0417.

Inspection by Network Team (Mr L. Haddad, 16/10/2026): screen cracked, hinge loose, grade B. Device was logged with 2 charger leads, one missing.

Previous loans for this family: 2 of 3 returned on time (CB-0302 returned 4 days late, cosmetic damage grade A).

Charger replacement quoted at £18.50. Repair estimate £64.00. Family has not yet been invoiced.
```

**q1 [read]** How severe is the damage to device CB-0417 according to the Network Team's inspection grade recorded in the case note?  
  `0` = Cosmetic: the damage is graded as cosmetic only; `1` = Repairable: the damage is graded as functional and needing repair, but not a write-off; `2` = Write-off: the damage is graded as a write-off  
  gold: {"0": 0.0431, "1": 0.92, "2": 0.0369} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [read]** How many school days after its loan end date was CB-0417 returned, as stated in the case note? Count whole school days; the figure stated in the note is used.  
  `0` = None: returned on or before the end date; `1` = Short: at least 1 but no more than 5 school days late; `2` = Moderate: more than 5 but no more than 10 school days late; `3` = Long: more than 10 but no more than 20 school days late; `4` = Very long: more than 20 school days late  
  gold: {"0": 0.0156, "1": 0.0156, "2": 0.0177, "3": 0.9201, "4": 0.031} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [infer]** What is the combined sum, in pounds, of the quoted charger replacement cost and the estimated repair cost for CB-0417 in the case note, before any exemption is considered?  
  `0` = Low: below £50.00; `1` = Medium: at least £50.00 but below £100.00; `2` = High: £100.00 or more  
  gold: {"0": 0.0369, "1": 0.92, "2": 0.0431} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [read]** How many entries in the reception log for the week of 16/09/2026 record a Chromebook intake, according to the case note?  
  `0` = None: no entry records a Chromebook intake; `1` = One: exactly one entry records a Chromebook intake; `2` = Few: two or three entries record a Chromebook intake; `3` = Many: four or more entries record a Chromebook intake  
  gold: {"0": 0.92, "1": 0.038, "2": 0.021, "3": 0.021} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F1-0070  ·  F1 Evidence-based scoring  ·  school office  ·  system record

```json
{
 "record_id": "ATT-CASE-2026-04417",
 "schema_version": "3.2",
 "exported_at": "2026-10-29T16:42:11Z",
 "exported_by": "svc_sims_export",
 "school": {
  "school_code": "BRX-SEC-0912",
  "name": "Ashdown Park Secondary Academy",
  "LEA_no": "8817"
 },
 "pupil": {
  "pupilId": "P-70133",
  "surname": "Okonkwo-Reid",
  "forename": "Tamsin",
  "DOB": "2011-03-18",
  "year_group": "Y10",
  "form_tutor": "Mr D. Halloran",
  "on_roll": true,
  "pupil_premium": null
 },
 "attendance_summary": {
  "sessions_possible": "378",
  "sessions_present": "301",
  "sessions_authorised_absence": "22",
  "sessions_unauthorised_absence": "55",
  "attendance_pct": "79.6",
  "last_updated": "2026-10-28"
 },
 "incident_refs": [
  {
   "ref": "ATT-EV-88213",
   "date": "2026-09-14",
   "type": "late_arrival",
   "minutes_late": 47,
   "recorded_by": "reception_desk_2"
  },
  {
   "ref": "ATT-EV-88307",
   "date": "2026-10-02",
   "type": "absence_no_contact",
   "minutes_late": null,
   "recorded_by": "J.Pemberton"
  },
  {
   "ref": "ATT-EV-88341",
   "date": "2026-10-09",
   "type": "late_arrival",
   "minutes_late": "22",
   "recorded_by": "reception_desk_1"
  }
 ],
 "contact_log": {
  "last_contact_date": "2026-10-06",
  "method": "phone",
  "outcome": "voicemail_left",
  "parent_guardian": {
   "name": "Mrs A. Reid",
   "tel": "07700 900412",
   "email": null
  }
 },
 "safeguarding_flag": {
  "flagged": false,
  "referral_ref": null,
  "notes_ref": "SG-2026-0077"
 },
 "meeting": {
  "requested": true,
  "date_booked": "2026-11-04",
  "time": "09:30",
  "room": "Admin 2",
  "attended": null
 },
 "free_text_notes": "Mrs Reid rang on 2026-10-06 saying Tamsin had a dental appointment and a bad cold; no note received for ATT-EV-88307. Tutor reports Tamsin has been tired in registration and says she is minding a younger sibling before school on Tuesdays and Thursdays. Letter sent 2026-10-12 (ref LTR-0451) requesting medical evidence; no reply yet.",
 "system_flags": {
  "legacy_import": true,
  "migrated_from": "CMIS_v4",
  "dupe_check": "pass",
  "print_queue_id": 88121,
  "bus_pass_no": "BP-44019"
 },
 "audit": {
  "created_by": "a.fenwick",
  "updated_by": "svc_sims_export",
  "rev": 14,
  "checksum": "e91c0a7b"
 }
}
```

**q1 [read]** How many late-arrival incidents are listed in the pupil's incident references for the current record? Count only entries whose type is a late arrival; ignore absences.  
  `0` = Fewer than two: no late arrivals or only one is listed; `1` = Exactly two: two late-arrival entries are listed; `2` = Three or more: at least three late-arrival entries are listed  
  gold: {"0": 0.0376, "1": 0.92, "2": 0.0424} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [read]** How many sessions of unauthorised absence does the attendance summary record for the pupil in the current period, as stated in the summary? Use the stated count of sessions.  
  `0` = Low: fewer than 10 sessions; `1` = Moderate: at least 10 but fewer than 25 sessions; `2` = High: at least 25 but fewer than 50 sessions; `3` = Very high: 50 sessions or more  
  gold: {"0": 0.0188, "1": 0.0235, "2": 0.0376, "3": 0.9201} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** As attendance officer, how serious is the attendance concern for this pupil, judged on overall attendance, the type of absence, the contact history and any signs of cause, as shown in the record at export?  
  `0` = Negligible: no real cause for concern; `1` = Minor: slight concern needing only routine monitoring; `2` = Moderate: clear concern needing follow-up but not formal escalation; `3` = Serious: substantial concern needing active formal intervention, without evidence of immediate danger; `4` = Critical: urgent concern with evidence of immediate risk or safeguarding referral  
  gold: {"0": 0.0075, "1": 0.025, "2": 0.315, "3": 0.5825, "4": 0.07} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [read]** How far has the arrangement of a meeting with the pupil's parent or guardian progressed, according to the meeting section of the record at export?  
  `0` = Not started: no meeting has been requested; `1` = Requested only: a meeting is requested but no date is fixed; `2` = Scheduled or later: a date and time are fixed, whether or not it has yet taken place  
  gold: {"0": 0.0213, "1": 0.0587, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F1-0071  ·  F1 Evidence-based scoring  ·  planning applications  ·  form submission

```
MARLBOROUGH TOWN COUNCIL – PLANNING DEPARTMENT
Householder Planning Application: Submitted Form (Online Portal Export)

Application Ref: TC/26/0814/HH
Date Received: 14/09/2026
Portal Submission ID: PP-88213-QX
Status: Awaiting Case Officer Assessment

SECTION 1 – APPLICANT
Title: Mr
Forename: Dariusz
Surname: Okonkwo-Hale
Correspondence Address: 22 Fenner Close, Marlborough, MR3 6PD
Telephone: 01672 553190
Email: d.okonkwohale@example-mail.co.uk
Preferred Contact Method: Email

SECTION 2 – SITE
Property Name / No: 22
Street: Fenner Close
Town: Marlborough
Postcode: MR3 6PD
Site Area (m²): 384
Existing Use: Residential (C3)
Listed Building: No
Conservation Area: No
Tree Preservation Order on Site: [blank]

SECTION 3 – PROPOSAL
Description: Single-storey rear extension (kitchen/dining), approx. 4.2m depth, flat roof with 2 rooflights; new side gate.
Total Floor Area Proposed (m²): 27.5
Total Floor Area Existing (sq ft): 1,012
Maximum Height of Extension (m): 3.1
Materials – Walls: Render (through-colour, off-white)
Materials – Roof: [blank]
Construction Start (estimated): 01/11/2026
Estimated Duration (weeks): 14
Estimated Duration (hours of site access per day): 9.5

SECTION 4 – DIMENSIONS & WEIGHT
Proposed Extension Weight (kg): 11,200 (see Structural Note)
Concrete Ground Slab Volume (m³): 4.8
Existing Garden Area Lost (sq yd): 205

SECTION 5 – DECLARATIONS
Ownership Certificate: A
Agricultural Holding: No
Design & Access Statement Attached: Yes (file: DAS_22FennerCl_rev2.pdf)
Structural Survey Attached: No
Ecology Survey Attached: [blank]
Biodiversity Net Gain Metric Attached: No

APPLICANT COMMENTS (free text)
"Neighbour at 20 has raised concern about the boundary wall, we have spoken to them and agreed to move the gate 0.4m. Happy to supply a plan revision if needed. Builder says the extension will take roughly 3 months, maybe less if the weather holds. Structural note is attached in the DAS not as separate file. Weight figure is from the supplier spec sheet, lb equivalent is approx 24,692 lb. Sorry for the mess in the form, the portal kept resetting when I tried to upload the drawings. Kitchen window is on the north elevation, not south as shown in the drawing."

Form completed via: Desktop browser, Chrome 118
Last saved: 14/09/2026 17:42:08
```

**q1 [read]** Count the form fields that the applicant has left explicitly marked as blank anywhere in the submitted form (Sections 1 to 5), excluding the free-text comments. Fields answered 'No' do not count as blank.  
  `0` = None: no field is marked blank; `1` = One: exactly one field is marked blank; `2` = Two: exactly two fields are marked blank; `3` = Three or more: at least three fields are marked blank  
  gold: {"0": 0.0171, "1": 0.0229, "2": 0.04, "3": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [judge]** From the case officer's viewpoint, rate how much further information or correction the applicant must supply before this application can sensibly be assessed, judging from the gaps, contradictions and the applicant's own comments in the form.  
  `0` = Minor: at most trivial clarifications are needed and assessment could proceed; `1` = Moderate: some specific points need clarifying, but the main assessment could begin; `2` = Substantial: several material gaps or contradictions need resolving first, such as missing documents, drawings or corrections  
  gold: {"0": 0.0225, "1": 0.14, "2": 0.8375} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [infer]** Work out the absolute difference, in weeks, between the construction duration entered in the form and the builder's rough estimate quoted in the applicant's comments. Convert months to weeks at 52 weeks per 12 months.  
  `0` = Negligible: below 0.25 weeks; `1` = Small: at least 0.25 but below 0.75 weeks; `2` = Modest: at least 0.75 but below 1.5 weeks; `3` = Notable: at least 1.5 but below 3 weeks; `4` = Large: 3 weeks or more  
  gold: {"0": 0.0175, "1": 0.0275, "2": 0.9125, "3": 0.035, "4": 0.0075} · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [infer]** Rate the proposed extension's floor area as a share of the stated site area. Use the proposed floor area and the site area in the form, expressed as a percentage and rounded to one decimal place.  
  `0` = Very low: below 10%; `1` = Low: at least 10% but below 20%; `2` = Moderate: at least 20% but below 30%; `3` = High: at least 30% but below 40%; `4` = Very high: 40% or more  
  gold: {"0": 0.92, "1": 0.0659, "2": 0.0141, "3": 0.0, "4": 0.0} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F1-0062  ·  F1 Evidence-based scoring  ·  fleet maintenance  ·  system record

```json
{
 "record_id": "FLT-INSP-2026-08841",
 "record_type": "vehicle_service_and_defect_export",
 "exported_at": "2026-10-30T07:42:11Z",
 "export_src": "fleetops_core v4.7.2",
 "vehicle": {
  "veh_id": "VN-0417",
  "reg_no": "KR14 PWX",
  "make_model": "Ford Transit Custom 320 L2",
  "yr": "2022",
  "odometer_km": 88214,
  "odo_last_read": "2026-10-28",
  "depot_code": "DPT-LEEDS-N",
  "assigned_driver_id": "DRV-2291"
 },
 "inspection": {
  "insp_ref": "INS-26-10-0930",
  "insp_dt": "2026-10-29T16:05:00Z",
  "inspector_id": "TECH-0083",
  "insp_type": "pre-return weekly",
  "result": "ADVISORY",
  "brake_pad_fl_mm": "3.1",
  "brake_pad_fr_mm": "3.4",
  "brake_pad_rl_mm": null,
  "tyre_tread_fl_mm": "2.1",
  "tyre_tread_fr_mm": "2.4",
  "tyre_tread_rl_mm": "4.8",
  "tyre_tread_rr_mm": "4.6",
  "wiper_blade_ok": true,
  "headlamp_ok": true,
  "dash_warning_lamps": 0
 },
 "defects": [
  {
   "def_id": "D-7731",
   "category": "tyres",
   "severity": "advisory",
   "desc": "FL tyre tread approaching legal limit, monitor",
   "raised_by": "TECH-0083",
   "closed_dt": null
  },
  {
   "def_id": "D-7698",
   "category": "bodywork",
   "sev": "minor",
   "desc": "Nearside sliding door scuff, cosmetic",
   "raised_by": "DRV-2291",
   "closed_dt": "2026-09-14T11:20:00Z"
  }
 ],
 "driver_notes": {
  "note_txt": "Van pulled slightly to left under braking on A64 approach, reported 27/10. Rear brake pad reading not captured at last check, tech to confirm.",
  "rating_avg": null,
  "compliments_ct": "2",
  "complaints_ct": "0"
 },
 "customer_feedback": [
  {
   "fb_id": "CF-88120",
   "dt": "2026-10-21",
   "score": "4",
   "comment": "Driver polite, parcel arrived intact, a little late",
   "route_ref": "RT-LDS-0612"
  },
  {
   "fb_id": "CF-88207",
   "dt": "2026-10-27",
   "score": null,
   "comment": "Van parked across dropped kerb, no issue otherwise",
   "route_ref": "RT-LDS-0588"
  }
 ],
 "maintenance_history": {
  "last_service_dt": "2026-07-03",
  "last_service_km": 81560,
  "next_due_km": 93560,
  "svc_provider_ref": "GAR-0044",
  "parts_ordered": [
   {
    "part_no": "BP-TC320-F",
    "qty": "1",
    "status": "backordered"
   }
  ]
 },
 "telematics": {
  "hard_brake_events_30d": 9,
  "avg_speed_kph": "24.6",
  "idle_pct": "18",
  "gps_sig_ok": true,
  "fuel_l_per_100km": "11.9",
  "telemetry_fw": "2.3.1"
 },
 "admin": {
  "cost_centre": "CC-4410",
  "asset_tag": "AST-00417",
  "legacy_ref": "KR14PWX-2022-SEED",
  "last_sync_by": "batch-job-17",
  "notes_flag": null
 },
 "record_notes": "Front-left pad and tread measurements within tolerance per last check but flagged for monitoring. Rear-left pad reading missing from INS-26-10-0930. Driver reports pull under braking; hard brake events elevated against fleet average of 4.2 for the same period."
}
```

**q1 [read]** Count the defects in this vehicle's record that are still open (no closure date) as at the export. Rate how many open defects the record shows.  
  `0` = None: no defect lacks a closure date; `1` = One: exactly one defect lacks a closure date; `2` = Two or more: at least two defects lack a closure date  
  gold: {"0": 0.04, "1": 0.92, "2": 0.04} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [read]** Rate the overall result grade recorded for the most recent weekly inspection of this van, as stated by the inspection record, from least to most serious.  
  `0` = Clear: the inspection recorded no issues at all; `1` = Advisory: the inspection recorded a result short of failure but with items to monitor; `2` = Failure: the inspection recorded a result that takes the van off the road  
  gold: {"0": 0.04, "1": 0.92, "2": 0.04} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [infer]** Using the latest odometer reading and the next service due distance, rate how many kilometres remain before this van's next scheduled service falls due.  
  `0` = Under 2,000 km: remaining distance is below 2,000 km (or already overdue); `1` = Mid range: remaining distance is at least 2,000 km but below 8,000 km; `2` = 8,000 km or more: remaining distance is at least 8,000 km  
  gold: {"0": 0.0463, "1": 0.92, "2": 0.0337} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [infer]** Rate the ratio of this van's hard-brake events in the last 30 days to the fleet average for the same period, using the figures in the record.  
  `0` = Well below: ratio below 0.5; `1` = Below: ratio at least 0.5 but below 1.0; `2` = Modestly above: ratio at least 1.0 but below 1.5; `3` = Clearly above: ratio at least 1.5 but below 2.0; `4` = Double or more: ratio of 2.0 or higher  
  gold: {"0": 0.008, "1": 0.008, "2": 0.0187, "3": 0.0453, "4": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F2-0121  ·  F2 Boundary and adjacent-level discrimination  ·  cold-chain logistics  ·  chat log

```
Chat log export: #cold-chain-ops (Meridian Chilled & Frozen Logistics)
Exported 2026-11-04 09:12 GMT by R. Ostrowska

[2026-10-28 14:02] Dariusz Mbeki: DC2 dock door 7 reefer unit on trailer MFR-4417 logged 9.4°C on arrival, setpoint was -18°C. Load is frozen fish, 22 pallets, PO 884-21907.
[2026-10-28 14:05] Rhian Ostrowska: Pull the datalogger file before it gets overwritten. Serial ends 3316.
[2026-10-28 14:09] Dariusz Mbeki: Pulled. Peak 9.4 at 13:51, back under -15 by 13:58. Probe 2 was reading -4 the whole time, probe 1 looks fine.
[2026-10-28 14:11] Tomasz Yilmaz: Probe 2 is the one that sits by the door seal, known to drift. Not a food-safety call yet, Rhian to decide.
[2026-10-28 14:15] Rhian Ostrowska: Need time above -12°C for the excursion log. Who has the TR-7 SOP reference?
[2026-10-28 14:18] Tomasz Yilmaz: SOP CC-TR-7 rev D, section 4.3. Rule is: excursion counts if core probe is above -12°C for more than 30 minutes. Exactly 30 min is not an excursion. Still need the full record for MFR-4417.
[2026-10-28 14:20] Dariusz Mbeki: Core probe (probe 1) was above -12 from 13:44 to 13:58. 14 min. So below threshold on that reading.
[2026-10-28 14:22] Rhian Ostrowska: Good. Log it as a monitored event, not an excursion. Corrective action ticket CC-CA-0392 open, due 5 working days from today, bank holidays excluded.
[2026-10-28 14:23] Tomasz Yilmaz: Note 28 Oct is a Tuesday, so due date is Tuesday 4 Nov.
[2026-10-28 16:40] Lauren Pike: Random aside, is anyone covering the Thursday forklift assessment? Mine is 13:30 not 13:00 now.
[2026-10-28 16:41] Dariusz Mbeki: I can cover, swap with me on the 3 Nov rota instead.
[2026-10-28 16:44] Lauren Pike: Deal. Rota updated, ref ROTA-W44-09.
[2026-11-02 10:17] Tomasz Yilmaz: Probe 2 recalibrated, reads -18.1 against reference. Trailer MFR-4417 datalogger cross-checked, no further peaks.
[2026-11-02 10:19] Rhian Ostrowska: CC-CA-0392 still open, waiting on the calibration cert scan from supplier.
```

**q1 [judge]** Rate how serious the food-safety concern is for the frozen fish load on trailer MFR-4417 after the 28 October reading, judged from the core-probe evidence and follow-up in the log, as a cold-chain quality reviewer.  
  `0` = Negligible: no core reading above the frozen limit and no sign of any temperature problem; `1` = Low: a brief core rise above the limit that is clearly short of the SOP limit, recovered quickly, and shows no recurrence; `2` = Moderate: core time above the limit is close to or at the SOP limit, or recovery or recurrence is uncertain; `3` = High: core time above the limit clearly exceeds the SOP limit, or the load stayed warm or kept rising  
  gold: {"0": 0.03, "1": 0.785, "2": 0.1625, "3": 0.0225} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [read]** What formal classification did the operations lead give the 28 October temperature event on trailer MFR-4417 for the excursion log, according to the chat?  
  `0` = Not logged: the chat records no classification for the event; `1` = Monitored event: logged for tracking but expressly not counted as an excursion; `2` = Excursion: logged as a formal excursion under the SOP  
  gold: {"0": 0.04, "1": 0.92, "2": 0.04} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [infer]** Using the core probe (probe 1) only, what share of the SOP CC-TR-7 30-minute limit was used by the time the core was above -12°C on 28 October? Share = minutes above -12°C divided by 30, as a percentage.  
  `0` = Under 25%: less than 25% of the limit used; `1` = 25% to under 75%: at least 25% but below 75% of the limit used; `2` = 75% or more: at least 75% of the limit used  
  gold: {"0": 0.0433, "1": 0.92, "2": 0.0367} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [infer]** As at the last chat message on 2 November, how many working days remained until corrective action ticket CC-CA-0392 was due, counting the due date itself but not 2 November, with weekends excluded and no bank holidays assumed?  
  `0` = None left: fewer than 1 working day remained, or the ticket was already overdue; `1` = Short: at least 1 but fewer than 3 working days remained; `2` = Some: at least 3 but fewer than 5 working days remained; `3` = Ample: at least 5 but fewer than 8 working days remained; `4` = Long: 8 or more working days remained  
  gold: {"0": 0.0282, "1": 0.92, "2": 0.04, "3": 0.0059, "4": 0.0059} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F2-0096  ·  F2 Boundary and adjacent-level discrimination  ·  car park enforcement  ·  chat log  ·  twin of SCORE-F2-0095

**Twin change:** Change the appellant's portal reply time from 16:58 to 16:59, making it only 1 minute before the deadline.

```
Chat transcript: Appeals Queue – Northgate Parking Services Ltd
Exported 2026-11-03 09:42 GMT
Queue: PCN Appeals (Tier 2) | Case ref. NPS-APL-26-04417

[2026-10-28 14:07] Dariusz Okonedo (Appeals Clerk): Morning Priya, pulling case 04417 for the Brackley Row multistorey. Penalty notice PCN 7710293 issued 2026-09-29 at 18:52, ANPR shows vehicle in bay L2-14 for 1h 12m against a 1h max stay. Appellant says the sign at the lower entrance was obscured by a skip.

[2026-10-28 14:11] Priya Lindqvist (Team Lead): Thanks. Remember the rubric in the appeals SOP, s.4.3: a challenge is upheld where (a) the signage was defective, (b) the appellant has supplied photographs dated on the day, and (c) the contravention period is under 90 minutes. Partial upheld only if two of three are met, inclusive of the 90 min boundary? No, check the SOP wording, I think it says "not exceeding 90 minutes" for (c).

[2026-10-28 14:15] Dariusz Okonedo: Confirmed, s.4.3(c) reads "not exceeding 90 minutes". So 72 min qualifies. Photos are dated 2026-09-29 16:31, fine. Signage defect I'll need to verify on site.

[2026-10-28 14:19] Priya Lindqvist: Site visit log says the skip was removed 2026-10-01, so the obstruction was not present on the date. Not sure that counts as defective.

[2026-10-28 15:02] Dariusz Okonedo: Appellant's response window: under POPLA-style code 6.2 we have 10 working days from receipt of the representation (received Tue 2026-10-13). Working days exclude weekends and the bank holiday on 2026-10-26? That's a Monday in October, so it'd be the 26th. Cutting it close.

[2026-10-28 15:06] Priya Lindqvist: Bank holiday is not a bank holiday that year for us, Northgate uses England & Wales calendar, so 26 Oct is a bank holiday only if it is the last Monday. It is not. Count from 14 Oct: 10 working days lands on Tue 27 Oct, extended to Wed 28 Oct end of day.

[2026-10-28 15:09] Dariusz Okonedo: Understood. Logging as response due 28/10 17:00.

[2026-10-29 10:20] Dariusz Okonedo: Appellant replied at 16:59 yesterday via portal. Within window.

[2026-10-29 10:24] Priya Lindqvist: Mark 04417 as partly resolved: signage element open pending site visit, contravention element met. Refer the other 3 cases on the list to me, they are all one condition short.

[2026-10-29 10:26] Dariusz Okonedo: Ok. Also, the lunch room fridge has been moved again, please don't leave yogurts in it.
```

**q1 [judge]** How far has Northgate reached a determination of the appeal outcome for case 04417, as recorded in the chat at export (3 November 2026)? Judge from the clerk and team lead's messages.  
  `0` = Undetermined: no outcome (upheld, partly upheld or rejected) for the appeal as a whole is recorded; only interim status of elements; `1` = Provisional: an outcome is stated but expressly conditional on a pending check; `2` = Decided: a final outcome is recorded but no communication to the appellant is shown; `3` = Decided and notified: a final outcome is recorded and shown to have been communicated to the appellant  
  gold: {"0": 0.825, "1": 0.135, "2": 0.025, "3": 0.015} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [compare]** By how many whole minutes did the vehicle's recorded stay exceed the maximum stay permitted for the bay, using the ANPR duration and the stated maximum stay on the day of the penalty notice?  
  `0` = Under 12: overstay below 12 minutes; `1` = Twelve to under 30: overstay of at least 12 but below 30 minutes; `2` = Thirty to under 60: overstay of at least 30 but below 60 minutes; `3` = Sixty or more: overstay of 60 minutes or longer  
  gold: {"0": 0.0385, "1": 0.92, "2": 0.0326, "3": 0.0089} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** How inconsistent is the chat's own reasoning about the appellant's response deadline (the working-day count and the due date reached)? Judge from the clerk and team lead's messages.  
  `0` = Consistent: the reasoning is coherent and the due date follows from the stated rules; `1` = Minor slips: some confused or hesitant statements, but the due date reached is unaffected; `2` = Material conflict: statements conflict or an adjustment is unexplained, so the due date logged does not follow clearly from the stated count  
  gold: {"0": 0.04, "1": 0.235, "2": 0.725} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** How much time before the logged response deadline (28 October, 17:00) did the appellant's portal reply arrive? Measure in whole minutes from the reply time to the deadline; a late reply counts as negative.  
  `0` = Under 2 minutes early: less than 2 minutes before the deadline, or late; `1` = Two to under 30: at least 2 but below 30 minutes before the deadline; `2` = Thirty or more: at least 30 minutes before the deadline  
  gold: {"0": 0.92, "1": 0.0622, "2": 0.0178} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F2-0079  ·  F2 Boundary and adjacent-level discrimination  ·  home insurance  ·  system record

```json
{
 "record_type": "home_contents_claim",
 "claim_ref": "HCC-2026-048213",
 "source_system": "CLM-CORE v7.4.1",
 "exported_at": "2026-10-30T09:14:52Z",
 "policy": {
  "policy_no": "HO-3381157",
  "policy_holder_name": "Dilys Anwar-Pryce",
  "product_code": "HC_STD_BUNDLE",
  "inception_dt": "2019-03-14",
  "renewal_dt": "2026-03-14",
  "sum_insured_gbp": "185000",
  "excess_gbp": 250,
  "excess_applied": true,
  "endorsements": [
   "ENDT-VAL-07",
   "ENDT-JWL-02"
  ]
 },
 "loss_event": {
  "reported_dt": "2026-10-28T08:41:00Z",
  "occurred_from": "2026-10-25T22:30:00Z",
  "occurred_to": "2026-10-26T07:10:00Z",
  "cause_code": "WATER_ESCAPE_BURST_PIPE",
  "location": "kitchen_utility_void",
  "police_crime_ref": null,
  "days_to_report": "3",
  "property_unoccupied_hrs": "0"
 },
 "insured_property": {
  "addr_line_1": "14 Harrowgate Close",
  "addr_postcode": "LS17 6QJ",
  "dwelling_type": "detached",
  "year_built": "1994",
  "occupancy": "owner_occupied"
 },
 "claim_lines": [
  {
   "line_id": "L1",
   "category": "building_fabric",
   "desc": "Flooring and sub-floor joists, utility room",
   "est_gbp": "6240.00",
   "assessed_gbp": null,
   "status": "pending_survey"
  },
  {
   "line_id": "L2",
   "category": "contents",
   "desc": "Washing machine, tumble dryer, freezer",
   "est_gbp": "1875.50",
   "assessed_gbp": "1410.00",
   "status": "partly_resolved"
  },
  {
   "line_id": "L3",
   "category": "alt_accommodation",
   "desc": "Temporary accommodation",
   "est_gbp": "0",
   "assessed_gbp": null,
   "status": "not_claimed"
  }
 ],
 "handling": {
  "handler_id": "CH-0417",
  "team": "Water Damage Triage",
  "queue": "WD-2",
  "priority_flag": "N",
  "reserve_gbp": 7500,
  "sla_due_dt": "2026-11-04",
  "prev_handler_ids": [
   "CH-0302"
  ],
  "notes": "Burst copper pipe found under sink on 28 Oct; shut off at stopcock by insured's neighbour, who had a key. Insured reports water ran for roughly 8 hours overnight across the Sunday, with a damp reading of 62 percent at the skirting in the utility; a moisture survey was booked for 3 Nov but the earlier survey slot was cancelled."
 },
 "_legacy": {
  "bkp_ref": "LGCY-88213-B",
  "migrated": "Y",
  "sync_ts": 1761817320,
  "old_queue": "HO_WATER_OLD",
  "misc_flag_x": "0",
  "print_tpl": "tpl_hc_v2"
 }
}
```

**q1 [read]** How many police crime references are recorded on this claim record as at the export date? Count only references actually entered in the police crime reference field.  
  `0` = None: no police crime reference is recorded; `1` = One: exactly one police crime reference is recorded; `2` = Two: exactly two police crime references are recorded; `3` = Three or more: three or more police crime references are recorded  
  gold: {"0": 0.92, "1": 0.0354, "2": 0.0223, "3": 0.0223} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [compare]** Rate the total of the claim lines' estimated amounts (all lines, using estimates not assessments, missing treated as zero) as a percentage of the handling reserve, rounded to one decimal place.  
  `0` = Well under: below 80.0% of the reserve; `1` = Under: at least 80.0% but below 95.0% of the reserve; `2` = Close: at least 95.0% but below 105.0% of the reserve; `3` = Over: at least 105.0% but below 115.0% of the reserve; `4` = Well over: 115.0% of the reserve or more  
  gold: {"0": 0.0141, "1": 0.0188, "2": 0.0282, "3": 0.9201, "4": 0.0188} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [compare]** Rate the elapsed time from the end of the stated loss window to the time the loss was reported, in hours, using the timestamps in the loss event and not the stored day count.  
  `0` = Prompt: below 24 hours; `1` = Intermediate: at least 24 hours but below 48 hours; `2` = Delayed: 48 hours or more  
  gold: {"0": 0.024, "1": 0.056, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** Rate the whole calendar days remaining between the export date and the handling SLA due date, counting from the export date to the due date.  
  `0` = Urgent: fewer than 2 days; `1` = Short: at least 2 days but fewer than 4 days; `2` = Moderate: at least 4 days but fewer than 6 days; `3` = Ample: 6 days or more  
  gold: {"0": 0.0171, "1": 0.0286, "2": 0.92, "3": 0.0343} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F2-0074  ·  F2 Boundary and adjacent-level discrimination  ·  solar installation  ·  statement with cover note  ·  twin of SCORE-F2-0073

**Twin change:** Change the DNO submission date from 09/10/2026 to 06/10/2026, so the expected confirmation falls on 17/11/2026, four days after the due date.

```
SUNRIDGE SOLAR (UK) LTD
Survey & Commissioning Division
Unit 4, Carrowmore Business Park, Leeds LS11 5QP
VAT Reg GB 297 4413 80

ACCOUNT STATEMENT – STMT-2026-10-0447

Customer:        Mrs Helen Okonedo-Platt
Site address:    14 Larkspur Close, Pudsey, Leeds LS28 7JR
Customer ref:    CUST-88214
Statement date:  30/10/2026
Account period:  01/09/2026 – 30/10/2026
Installer job:   SRS-J-20417 (3.6 kWp PV, 10.2 kWh battery)

Date        Ref        Description                              Qty     Unit £    Net £      VAT £     Gross £
03/09/2026  INV-7731   Site survey, roof pitch 34°, south-east   1       180.00    180.00     36.00     216.00
09/09/2026  INV-7731   Structural check, rafter sample (2)        1        45.00     45.00      9.00      54.00
18/09/2026  INV-7764   Panels, 9 x 400 W monocrystalline          9       236.40   2,127.60    425.52   2,553.12
18/09/2026  INV-7764   Inverter, hybrid 4.6 kW                    1     1,094.00   1,094.00    218.80   1,312.80
02/10/2026  INV-7790   Battery module, 10.2 kWh                   1     2,850.00   2,850.00    570.00   3,420.00
14/10/2026  INV-7802   Commissioning visit, first attempt         1       150.00     150.00     30.00     180.00
21/10/2026  INV-7802   Re-attendance (isolator fault)             1        95.00      95.00     19.00     114.00
                                                                                  ---------- ---------- ----------
                                                                         Sub-total     4,491.60
                                                                         VAT @ 20%                     ---------
                                                                         Total net                      4,491.60
                                                                         VAT total                        897.52
                                                                         Gross total                    5,389.12

Payments received
12/09/2026  Deposit (pro-forma PF-1190)                                                                    -1,000.00
06/10/2026  Stage payment 1 (on delivery)                                                                  -2,500.00
Balance due                                                                                                 1,889.12

Notes
Retention of £250.00 applies until Commissioning Certificate CC-20417 is issued. Export meter (G98 notification ref G98-44190) is pending from the DNO; installer will not energise the export function until confirmation is received, expected within approximately 6 weeks of submission on 06/10/2026. Payment terms 14 days from statement date.

---

Dear Sunridge Solar,

I am writing about statement STMT-2026-10-0447. The commissioning visit on 14/10/2026 did not complete, and I was charged for it along with the return visit. The engineer said the system was "just under" the export limit but then left without the inverter running. I have not been able to get a straight answer on when the system will actually work, and I would like the £180.00 and £114.00 charges reversed, and the retention released now rather than after an unknown period.

Regards,
H. Okonedo-Platt
```

**q1 [infer]** Rate the size of the discrepancy, in pounds, between the statement's stated VAT total and 20% of its stated total net figure. Use the absolute difference, rounded to the nearest penny.  
  `0` = None: the absolute difference is less than £0.01; `1` = Small: the absolute difference is at least £0.01 but below £5.00; `2` = Large: the absolute difference is £5.00 or more  
  gold: {"0": 0.0337, "1": 0.92, "2": 0.0463} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [infer]** Rate the combined gross value of the two charges the customer asks to have reversed, as a percentage of the statement's stated gross total. Calculate it from the gross figures on the statement and round to one decimal place.  
  `0` = Minimal: below 1.0%; `1` = Low: at least 1.0% but below 3.0%; `2` = Moderate: at least 3.0% but below 5.0%; `3` = Substantial: at least 5.0% but below 8.0%; `4` = Major: 8.0% or more  
  gold: {"0": 0.0096, "1": 0.0144, "2": 0.0288, "3": 0.92, "4": 0.0272} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [infer]** Rate how many whole days after the statement's payment due date the DNO export confirmation is expected. Take the expected date as six weeks after the stated submission date, and the due date as 14 days after the statement date.  
  `0` = Not later: expected on or before the due date (less than 1 day after); `1` = Slightly later: at least 1 but fewer than 7 days after; `2` = About a week later: at least 7 but fewer than 14 days after; `3` = Much later: at least 14 but fewer than 28 days after; `4` = Far later: 28 days or more after  
  gold: {"0": 0.028, "1": 0.92, "2": 0.038, "3": 0.008, "4": 0.006} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [judge]** Rate how strongly the document's stated terms support the installer still withholding the £250.00 retention at the statement date, as opposed to releasing it now. Judge from the statement notes and the facts of the job.  
  `0` = Unsupported: no stated term links the retention to any unmet condition; `1` = Weakly supported: a term exists but the document shows its condition may already be met; `2` = Partly supported: a term exists and its condition is unmet, but the document leaves doubt about its application; `3` = Fully supported: an explicit term ties the retention to a condition that the document shows is not yet met  
  gold: {"0": 0.02, "1": 0.075, "2": 0.28, "3": 0.625} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F2-0082  ·  F2 Boundary and adjacent-level discrimination  ·  warehouse  ·  form submission  ·  twin of SCORE-F2-0081

**Twin change:** Enter a second checker ID (for example CNT-097) in the blank 'Second checker ID' field, so one verification item is completed.

```
STOCK ADJUSTMENT & CYCLE COUNT REQUEST FORM
Site: Northgate Distribution Centre (DC2)          Form ref: SCA/DC2/26-4471
Submitted by: Tomasz Wierzbicki (Shift Lead, Nights)   Submitted: 29/10/2026 05:52
Cost centre: CC-7320                                   Status: SUBMITTED – awaiting approval

Section A – Count details
Location code:           Bay R14-03  
Location type:           Pick face (case)
SKU:                     HS-40718-BLK
SKU description:         Hi-vis sleeve jacket, black, size M
Count date:              28/10/2026
Count start time:        22:10
Count end time:          23:05
Counter ID:              CNT-112
Second checker ID:       CNT-097
System quantity:         214 units
Counted quantity:        186 units
Variance (units):        -28
Variance (%):            -13.08
Approval threshold:      Variances over 10% OR over 25 units require Stock Control Manager sign-off (inclusive of 10.00% and 25 units: NO)

Section B – Adjustment request
Adjustment reason code:  DMG-02 (damaged – found on pick face)
Adjustment value (GBP):  £1,164.80
Write-off to:            Hold Zone H-01 (partly quarantined)
Pallet ID(s):            PLT-88213049, PLT-88213051
Pallets scanned on:      28/10/2026 
Photos attached:         2 of 3
Related ticket:          SC-TKT-30871

Section C – Comments
Counted 2 cases on 1 pallet short of the system record and found 4 cases on R14-03 that had been logged as moved to R14-05 on 26/10. Two of the damaged units are sitting just under the tear threshold in the handling guide (about 60% of sleeve intact) so I have not binned them yet. Recount not done as the second checker was on a break and then went home sick. Pallet PLT-88213051 may be the one from the 19:40 inbound, not sure. Value is roughly right, I used the last landed cost from the PO which might be a bit out. Will sort the rest on Thursday's early.
```

**q1 [compare]** Rate the size of the count variance as an absolute percentage of system quantity, as stated on the form for the 28/10/2026 count of the SKU at Bay R14-03. Use the form's percentage rounded to two decimals.  
  `0` = Minimal: below 10.00%; `1` = Moderate: at least 10.00% but below 15.00%; `2` = Large: at least 15.00% but below 20.00%; `3` = Severe: at least 20.00% but below 30.00%; `4` = Extreme: 30.00% or more  
  gold: {"0": 0.025, "1": 0.92, "2": 0.025, "3": 0.015, "4": 0.015} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [compare]** Rate the delay between the count ending on 28/10/2026 and the form being submitted on 29/10/2026, in hours, using the times on the form. Round to the nearest tenth of an hour.  
  `0` = Short: below 3.0 hours; `1` = Moderate: at least 3.0 but below 6.0 hours; `2` = Long: at least 6.0 but below 12.0 hours; `3` = Very long: 12.0 hours or more  
  gold: {"0": 0.0141, "1": 0.0376, "2": 0.9201, "3": 0.0282} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [compare]** Rate the implied average adjustment value per unit of variance: the adjustment value in GBP divided by the absolute unit variance on the form. Round to the nearest penny.  
  `0` = Low: below £20.00 per unit; `1` = Fair: at least £20.00 but below £30.00 per unit; `2` = High: at least £30.00 but below £40.00 per unit; `3` = Very high: £40.00 or more per unit  
  gold: {"0": 0.016, "1": 0.0213, "2": 0.0427, "3": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [infer]** Rate how many of these three verification items the form shows as completed: a second checker recorded, a recount done, and all expected photos attached. Count only what the form evidences.  
  `0` = None: none of the three items is completed; `1` = One: exactly one of the three items is completed; `2` = Two: exactly two of the three items are completed; `3` = Three: all three items are completed  
  gold: {"0": 0.06, "1": 0.9075, "2": 0.0225, "3": 0.01} · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F2-0116  ·  F2 Boundary and adjacent-level discrimination  ·  retail loyalty  ·  incident report  ·  twin of SCORE-F2-0115

**Twin change:** Change the wrongly reversed refund amount from £1.40 to £3.10 (with the recorded and corrected spends adjusted to fit, corrected remaining £61.30), making the share about 5.1%.

```
GREENFIELD FOOD GROUP – LOYALTY PROGRAMME (GreenCard Plus)
INCIDENT / EVENT REPORT

Report ref: LP-INC-2026-0412
Date of report: 29/10/2026
Reported by: Tomasz Wierzbicki, Loyalty Operations Analyst (Team 2, Leeds Contact Hub)
Store involved: Greenfield Superstore #184, Wakefield Road
Customer: Mrs Angela Dunstable, GreenCard Plus no. 9047 2215 6630
Incident type: Points adjustment dispute / bonus voucher not issued

Policy reference: LP-POL-07 Points Adjustment and Bonus Voucher Rules, clause 4.2
"A bonus voucher of £5.00 is issued where a member's qualifying spend in a single trading week is £60.00 or more (inclusive) and the member has scanned their card on at least three separate visits. Spend of £59.99 or less does not qualify. Vouchers requested more than 14 days after the qualifying week are not reissued."

Timeline (all times GMT, 24-hour clock):
17/10/2026 09:42 – Customer scanned card at till 3, transaction 0184-0917, total £61.30 (includes £3.10 refund on returned item, deducted at till).
17/10/2026 09:44 – Till system recorded qualifying spend for week 42 as £58.20 after refund netting.
19/10/2026 14:08 – Customer scanned card on second visit (£22.15).
22/10/2026 18:31 – Customer scanned card on third visit (£34.80).
23/10/2026 10:15 – Customer phoned Contact Hub, requested £5.00 bonus voucher. Advisor (ID CH-117) logged request as ineligible, weekly spend recorded at £58.20.
24/10/2026 11:02 – Customer complained by email, stating refund was not a return of goods to be netted.
27/10/2026 08:50 – Store manager L. Oyelaran reviewed transaction 0184-0917. Refund line confirmed as separate item, £3.10 reversed in error.
27/10/2026 09:20 – Corrected weekly spend recalculated at £61.30.
27/10/2026 09:25 – Voucher authorised, reference BV-88413.

Witness remarks:
L. Oyelaran (Store Manager): "The refund was keyed under the same basket. I'd have expected the system to show it separately, but it nets off on the till report unless someone checks the line."
CH-117 (Contact Hub Advisor): "She said the spend was over sixty. I checked the total on the screen, which was 58.20 after the refund, so I logged it as short."

Corrected figure: The weekly qualifying spend was initially recorded as £58.20. Following the store review on 27/10/2026 the correct figure is £61.30. Customer meets the £60.00 threshold and the three-visit condition (visits on 17/10, 19/10 and 22/10).

Outcome: Voucher BV-88413 issued 27/10/2026, value £5.00, expiry 26/01/2027. Customer informed by phone 27/10/2026 at 16:40 by T. Wierzbicki. Customer has asked whether a written apology will be sent; no decision recorded.

Related items: CRM case CR-0553871; till fault ticket TF-22907 (refund netting display) raised 28/10/2026, status open.
```

**q1 [judge]** As at the report date of 29/10/2026, how fully has the dispute been resolved from the customer's point of view, considering both her voucher claim and the follow-up matters the report leaves open?  
  `0` = Unresolved: the voucher has not been issued and the customer has not been told the claim is upheld; `1` = Substantially but not fully resolved: the voucher is issued and the customer informed, but at least one follow-up matter (such as an apology decision or the underlying fault) remains open; `2` = Fully resolved: the voucher is issued, the customer informed, and every follow-up matter is closed or decided  
  gold: {"0": 0.0175, "1": 0.9425, "2": 0.04} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [compare]** By how much, in pounds sterling, does the corrected weekly qualifying spend (after the store review) exceed the £60.00 voucher threshold? Use the corrected figure, not the initially recorded one. Round to the nearest penny.  
  `0` = Below threshold: corrected spend is under the threshold (margin below £0.00); `1` = Marginal: margin at least £0.00 but below £0.50; `2` = Small: margin at least £0.50 but below £1.00; `3` = Moderate: margin at least £1.00 but below £1.30; `4` = Larger: margin of £1.30 or more  
  gold: {"0": 0.0107, "1": 0.0133, "2": 0.0133, "3": 0.0427, "4": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [compare]** How many whole calendar days elapsed between the customer's first telephone request for the voucher and the voucher being authorised? Count by date only, ignoring times of day.  
  `0` = Under two days: fewer than 2 calendar days; `1` = Two to under seven days: at least 2 but fewer than 7 calendar days; `2` = Seven to under fourteen days: at least 7 but fewer than 14 calendar days; `3` = Fourteen days or more: 14 or more calendar days  
  gold: {"0": 0.0343, "1": 0.92, "2": 0.0343, "3": 0.0114} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** What share of the corrected weekly qualifying spend does the wrongly reversed refund amount represent? Divide the reversed amount by the corrected weekly spend, express as a percentage, and round to one decimal place.  
  `0` = Negligible: below 1.0%; `1` = Small: at least 1.0% but below 5.0%; `2` = Notable: at least 5.0% but below 10.0%; `3` = Large: 10.0% or more  
  gold: {"0": 0.0121, "1": 0.0461, "2": 0.92, "3": 0.0218} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F2-0111  ·  F2 Boundary and adjacent-level discrimination  ·  college admissions  ·  chat log

```
Admissions CRM – Chat Log
Queue: Applications / Level 3 Diploma (Health & Social Care)
Conversation ID: CH-2026-10-30-0412
Agent: R. Okonjo-Bell (Admissions Officer)
Other participant: A. Lindqvist (Applicant Support)

09:14:02 [A. Lindqvist] Morning Rena, flagging applicant ref APP-88213 (Tamsin Greaves). Prior learning claim came in yesterday, wants to be assessed against Policy ADM-7 para 4.3.
09:15:40 [R. Okonjo-Bell] Thanks. What's the total on the claim?
09:16:55 [A. Lindqvist] Attached schedule shows 118 guided learning hours evidenced across 3 sources. Two are employer letters dated 14/03/2025 and 02/09/2026. Third is a CPD certificate, undated.
09:18:31 [R. Okonjo-Bell] ADM-7 4.3 says the threshold is "at least 120 hours, inclusive of the 120th hour, evidenced within the previous 36 months". Is the undated certificate counted in that?
09:19:10 [A. Lindqvist] Not yet. Applicant says it was completed in March 2024 but the certificate has no date printed. She has a covering email from the provider that might confirm it.
09:19:48 [R. Okonjo-Bell] Send it over. Any other gaps?
09:21:05 [A. Lindqvist] The 14/03/2025 letter covers 40 hours but it only lists "care support duties", not the unit codes. Partly matches. Hours for that letter are counted at 25 in the schedule, the rest is unverified.
09:22:17 [R. Okonjo-Bell] Ok. So verified so far is 93 hours?
09:22:44 [A. Lindqvist] 93 yes. 02/09/2026 letter is 37 hours, full match to unit codes.
09:24:09 [R. Okonjo-Bell] Fair. Reminder that 36 months from today is 30/10/2023, so the March 2024 course would sit inside the window if confirmed.
09:25:30 [A. Lindqvist] Understood. Also she asked whether the fee waiver applies if PLC is approved. Fee waiver is in ADM-9, not my area.
09:26:02 [R. Okonjo-Bell] I'll answer that separately. Parking that.
09:31:48 [A. Lindqvist] Unrelated: the open day booking page is showing 14 slots for 06/11 instead of 12. Can you check the calendar sync?
09:33:20 [R. Okonjo-Bell] Raised as IT-44107. Probably a duplicate from the Tuesday import.
09:40:55 [A. Lindqvist] Provider email just arrived. It confirms the CPD course ran 11–15 March 2024, 22 contact hours. Certificate date now matches.
09:42:10 [R. Okonjo-Bell] So verified total is now 93 + 22 = 115? Are the 22 hours in the 118 already?
09:43:01 [A. Lindqvist] No, they are not. Schedule total was 118 with the CPD line at zero. Sorry, my mistake, I have 115 at present.
09:44:37 [R. Okonjo-Bell] Ok, 115 against 120. Five short. Leave the file open and tag it PLC-PENDING. I'll pull the 40-hour letter and ask the employer for unit codes.
09:45:12 [A. Lindqvist] Will do. Ref APP-88213 updated 09:45.

```

**q1 [compare]** By the end of the chat, how many guided learning hours short of the ADM-7 4.3 threshold is the applicant's verified total? Count whole hours, using the final verified figure agreed in the chat.  
  `0` = None: verified total meets or exceeds the threshold (shortfall of 0 hours or less); `1` = Marginal: shortfall of more than 0 but at most 4 hours; `2` = Small: shortfall of more than 4 but at most 5 hours; `3` = Larger: shortfall of more than 5 hours  
  gold: {"0": 0.0093, "1": 0.0186, "2": 0.92, "3": 0.0521} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [infer]** At the end of the chat, what percentage of the ADM-7 4.3 hours threshold does the applicant's final verified total represent? Divide verified hours by the threshold; do not round before applying the edges.  
  `0` = Low: below 80%; `1` = Fairly high: at least 80% but below 96%; `2` = Near complete: at least 96% but below 100%; `3` = Met: at least 100% but below 125%; `4` = Well over: 125% or more  
  gold: {"0": 0.0391, "1": 0.92, "2": 0.0249, "3": 0.0107, "4": 0.0053} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [compare]** Of the hours counted in the final verified total, how many come from evidence dated before the start of the 36-month window stated in the chat? Use the window start date given by the officer.  
  `0` = None: 0 hours; `1` = Very few: more than 0 but at most 5 hours; `2` = Some: more than 5 but at most 22 hours; `3` = Many: more than 22 but at most 60 hours; `4` = Most: more than 60 hours  
  gold: {"0": 0.9201, "1": 0.0293, "2": 0.0213, "3": 0.016, "4": 0.0133} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** How many more open day slots does the booking page show for 06/11 than the correct number stated in the chat?  
  `0` = Slight: at most 2 extra slots; `1` = Moderate: more than 2 but at most 5 extra slots; `2` = Large: more than 5 extra slots  
  gold: {"0": 0.92, "1": 0.0565, "2": 0.0235} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F2-0093  ·  F2 Boundary and adjacent-level discrimination  ·  wedding venue  ·  statement with cover note

```
Hollin Ash Estate & Barn
Ferrers Lane, Maddingley, Wiltshire SN9 4QT
VAT Reg: GB 318 6640 21

ACCOUNT STATEMENT
Statement No: HAE-ST-2026-1047
Statement Date: 30/10/2026
Account Ref: CUST-0827 (Ashworth / Penhallow wedding)
Event Date: Saturday 14/11/2026 (Harvest Barn, 14:00–23:30)
Payment Terms: 14 days from statement date

Item | Description | Date/Time | Qty | Unit (£) | Amount (£)
1 | Barn hire, Harvest Barn, Saturday rate | 14/11/2026 14:00–23:30 | 1 | 2,150.00 | 2,150.00
2 | Overrun charge, per 30 min after 23:30 (exclusive of 23:30) | 14/11/2026 23:31–00:15 | 2 | 175.00 | 350.00
3 | Ceremony chairs, ivory (per chair) | 14/11/2026 | 120 | 1.50 | 180.00
4 | Dance floor, 6m x 8m | 14/11/2026 | 1 | 240.00 | 240.00
5 | Sound system and DJ, 5 hrs (inclusive of 5.00 hrs) | 14/11/2026 18:00–23:00 | 1 | 425.00 | 425.00
6 | Deposit received 02/03/2026, ref BACS-88213 | | 1 | -500.00 | -500.00

Subtotal (net): 2,845.00
VAT @ 20%: 569.00
Total due: 3,414.00
Less payments received: -500.00 (applied to Item 6)
Balance outstanding: 2,914.00

Notes
Guest numbers confirmed 118 at 28/10/2026. Charges apply per guest above 120 (exclusive of 120). Pay by BACS, sort code 20-41-67, account 40318829, reference CUST-0827.

Cover note (received by email 30/10/2026, 17:42)
Dear Hollin Ash Accounts,
Item 2 is wrong. Our reception ran to 00:15 only because the DJ stopped at 23:00 and the overrun was agreed verbally with Pippa on 09/10. She said it would be waived if we kept the music low. We kept it low. Please remove the £350.00 and reissue.
Also the chairs were 118 not 120. We are not paying for two extra chairs.
Regards,
Joanna Penhallow
```

**q1 [infer]** Count how many times the £500.00 deposit is deducted in arriving at the 'Balance outstanding' figure on the statement, taking the line items, totals and payments lines together as printed.  
  `0` = Never: the deposit is deducted fewer than one time; `1` = Once: the deposit is deducted at least once but fewer than two times; `2` = Repeatedly: the deposit is deducted two or more times  
  gold: {"0": 0.0183, "1": 0.0617, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [judge]** From the venue's point of view, using only the document, how strong is the documentary support for the customer's claim that the £350.00 overrun charge was agreed to be waived?  
  `0` = None: nothing in the document supports the claim, or the document contradicts it; `1` = Weak: only the customer's own uncorroborated assertion supports waiver, though some surrounding details are consistent; `2` = Moderate: at least one venue-originated record supports a waiver but does not confirm it outright; `3` = Strong: a venue-originated written record confirms the waiver  
  gold: {"0": 0.2, "1": 0.705, "2": 0.0725, "3": 0.0225} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** How much of the factual content of the customer's cover note can be checked against the statement itself, as judged by the events coordinator?  
  `0` = Nothing: none of the factual claims can be checked against the statement; `1` = Partly: some claims are matched or contradicted by the statement, but others cannot be checked; `2` = Fully: every factual claim can be checked against the statement  
  gold: {"0": 0.03, "1": 0.93, "2": 0.04} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [read]** How many whole days before the event date (14/11/2026) does payment fall due, with the due date being the statement date plus the stated payment terms in days?  
  `0` = Under one day: due on or after the event date, or less than 1 day before it; `1` = Short: at least 1 day but under 3 days before the event; `2` = Moderate: at least 3 days but under 7 days before the event; `3` = Long: at least 7 days but under 14 days before the event; `4` = Very long: 14 days or more before the event  
  gold: {"0": 0.0678, "1": 0.92, "2": 0.009, "3": 0.0019, "4": 0.0013} · agreement 3/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F2-0063  ·  F2 Boundary and adjacent-level discrimination  ·  college admissions  ·  meeting notes

```
MEETING NOTES: Admissions Panel – Level 3 Engineering Apprenticeship (Intake 2027)

Ref: ADM/PN/2026/114
Date: Thursday 29 October 2026, 14:00–14:50
Location: Room 2.07, Eastfield Vocational College (also dialled in: Teams link ending 4471)
Attendees: Priya Okonkwo (Admissions Officer, chair), Tomasz Wrzesniak (Curriculum Lead), Denise Akhtar (Employer Liaison), Ben Hallam (Data & Records)
Apologies: Sian Pritchard
Notes taken by: Ben Hallam

1. Minutes of 15 October (ref ADM/PN/2026/109) approved with one amendment: applicant count for the Sept open evening corrected to 212.

2. Applicant pool. Ben reported 186 completed applications received by the 27 October closing date. Priya noted 9 of these are still missing the Level 2 maths certificate. Tomasz said the figure should be 193 once late uploads from the portal are included. Ben to reconcile against the portal export.

3. Interview threshold. Per Rule 4.3 (Admissions Policy v5, 1 Sept 2026): applicants scoring 60 or above on the aptitude test (inclusive) proceed to interview; scores below 60 are not invited. Denise asked whether 59.5 is rounded up. Priya confirmed scores are recorded to one decimal place and are not rounded. Four applicants currently sit at 59.5 or 59.8; none to be invited unless a re-sit is approved.

4. Employer placements. Denise reported that Harlow Precision has confirmed 11 placements, not 12 as previously stated. Denise said the earlier figure included one placement now withdrawn. Tomasz disagreed and believes the withdrawal is not yet confirmed in writing. Unresolved; Denise to obtain written confirmation.

5. Accessibility adjustments: two requests received, one approved, one awaiting occupational health report (expected 12 November).

Actions
- Ben Hallam: reconcile applicant count (186 vs 193) against portal export by Tuesday 3 November.
- Denise Akhtar: obtain written confirmation from Harlow Precision re withdrawn placement by 6 November.
- Priya Okonkwo: write to four borderline applicants at 59.5/59.8 confirming outcome.
- Tomasz Wrzesniak: circulate revised intake capacity (currently 24 places) to panel.

Next meeting: Thursday 12 November 2026, 14:00.
```

**q1 [compare]** Rate the size of the gap between the two completed-application totals put forward at the 29 October 2026 panel (the figure first reported and the figure Tomasz said was correct), in applications.  
  `0` = None: the two totals are identical; `1` = Small: at least 1 but fewer than 7 applications apart; `2` = Moderate: at least 7 but fewer than 12 applications apart; `3` = Large: at least 12 but fewer than 20 applications apart; `4` = Very large: 20 or more applications apart  
  gold: {"0": 0.0107, "1": 0.032, "2": 0.92, "3": 0.0293, "4": 0.008} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [compare]** Rate the waiting time, in whole calendar days, from the panel meeting on 29 October 2026 to the date the outstanding occupational health report is expected.  
  `0` = Brief: fewer than 7 days; `1` = Short: at least 7 but fewer than 10 days; `2` = Extended: at least 10 but fewer than 14 days; `3` = Long: 14 days or more  
  gold: {"0": 0.0089, "1": 0.0133, "2": 0.0578, "3": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [compare]** Rate the share of the current intake capacity that Harlow Precision's confirmed placements would cover, taking the lower figure of 11 as stated by Denise and the capacity currently stated. Round to one decimal place of a percent.  
  `0` = Minimal: below 10.0%; `1` = Low: at least 10.0% but below 20.0%; `2` = Moderate: at least 20.0% but below 30.0%; `3` = Substantial: at least 30.0% but below 45.0%; `4` = Very high: 45.0% or more  
  gold: {"0": 0.0064, "1": 0.0064, "2": 0.0128, "3": 0.0544, "4": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [judge]** Rate how unsettled the panel's position on the applicant pool and employer placement figures was at the end of the 29 October 2026 meeting, judging from the notes.  
  `0` = Settled: figures agreed with nothing outstanding; `1` = Partly open: minor points outstanding but figures broadly agreed; `2` = Largely unresolved: conflicting figures remain, with checks or written confirmation still to come  
  gold: {"0": 0.0075, "1": 0.08, "2": 0.9125} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F2-0078  ·  F2 Boundary and adjacent-level discrimination  ·  walk-in clinic  ·  meeting notes  ·  twin of SCORE-F2-0077

**Twin change:** Change item 5 so that one of the two Polish-language requests was not booked (only one of three requests fully met, 33%).

```
MEETING NOTES

Meeting: Harbour Lane Community Walk-in Clinic – Reception & Triage Huddle
Date: Thursday 29 October 2026, 13:10–13:35
Location: Triage room 2 (hybrid, dial-in ext. 4417)
Notes taken by: Priya Wendt (Charge Nurse)

Attendees: Priya Wendt (PW), Dr Tomasz Blaszczyk (TB, GP lead), Keisha Osei-Adu (KO, reception supervisor), Marcus Thorne (MT, IT liaison), Dr Hana Lindqvist (HL, locum, dial-in)
Apologies: Ruth Donnelly (RD, practice manager)

1. Walk-in volumes, week 42. KO reported 412 arrivals against 395 last week. TB quoted 388 from the triage log export; KO says the export excludes 24 people who were re-registered at the desk after a 15-minute wait. Figure to be reconciled before Friday.

2. Triage rubric. PW reminded the group of the amended rule (v3, effective 1 Oct): patients with NEWS2 score of 5 or more are seen immediately; 4 or below goes to the standard queue. TB noted the 4-point threshold is "inclusive" for the 3-hour re-check only, not for the immediate-review rule. HL asked for this in writing.

3. Waiting times. Median wait for the 13:00 block was 42 minutes (initial dashboard figure). KO corrected this to 24 minutes after the dashboard was refreshed at 13:05; the 42 figure came from a cached view. Agreed to use 24.

4. Walk-in cut-off. Current cut-off is 17:30 for new registrations; patients arriving at 17:30 exactly are registered, at 17:31 are redirected to the urgent care line. MT confirmed the kiosk clock is 2 minutes fast and will be corrected by Monday.

5. Interpreter bookings. Two Polish-language requests this week, one booked and one not met. One Tigrinya request not met; partly resolved, interpreter confirmed for Monday only.

6. Fax-to-email migration. Six of nine referring practices now live. Remaining three: two pending sign-off, one not responding.

ACTIONS
- KO: reconcile week 42 arrival count with TB, by Fri 30 Oct.
- MT: correct kiosk clock offset, by Mon 2 Nov.
- PW: circulate triage rubric v3 in writing to all locums, by Fri 30 Oct.
- RD (via PW): chase the three outstanding referring practices.
- HL: confirm availability for Tuesday 3 Nov session.

Next meeting: Thursday 5 November, 13:10.
```

**q1 [compare]** Rate the size of the gap, in people, between the reception supervisor's week 42 arrival count and the triage log export count, as reported at this huddle. Gap = larger figure minus smaller figure.  
  `0` = Negligible: fewer than 10 people; `1` = Small: at least 10 but fewer than 25 people; `2` = Moderate: at least 25 but fewer than 50 people; `3` = Large: at least 50 but fewer than 100 people; `4` = Very large: 100 people or more  
  gold: {"0": 0.0254, "1": 0.92, "2": 0.0436, "3": 0.0091, "4": 0.0019} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [compare]** Rate how far the fax-to-email migration has progressed, as the share of the referring practices listed in the notes that are already live. Use the unrounded percentage; practices pending sign-off or not responding count as not live.  
  `0` = Minority: below 50% live; `1` = Majority: at least 50% but below 66% live; `2` = Two-thirds or more: at least 66% live  
  gold: {"0": 0.0225, "1": 0.0575, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [compare]** Rate the week-on-week percentage rise in walk-in arrivals for week 42 compared with the previous week, using the reception supervisor's figures (not the export). Calculate against last week's figure; do not round before comparing.  
  `0` = Flat or low: below 2% rise (including any fall); `1` = Modest: at least 2% but below 4% rise; `2` = Notable: at least 4% but below 6% rise; `3` = Sharp: 6% rise or more  
  gold: {"0": 0.0185, "1": 0.0349, "2": 0.9199, "3": 0.0267} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** Rate how fully interpreter demand was met this week: the share of interpreter requests listed that are fully met (booked for the whole need). Partly resolved requests count as not fully met.  
  `0` = Poor: below 50% fully met; `1` = Limited: at least 50% but below 70% fully met; `2` = Good: at least 70% but below 90% fully met; `3` = Excellent: 90% or more fully met  
  gold: {"0": 0.9201, "1": 0.0516, "2": 0.0206, "3": 0.0077} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F3-0169  ·  F3 Conflicting evidence  ·  car park enforcement  ·  statement with cover note

```
HARBOURSIDE PARKING MANAGEMENT LTD
Unit 4, Quayside Business Park, Stanmore Road, Wexcombe WX3 8QP
VAT Reg GB 288 4417 09 | Company No. 09812637

ACCOUNT STATEMENT – PENALTY CHARGE NOTICES
Statement Ref: HPM/ST/2026/10/0417
Statement Date: 30/10/2026
Statement Period: 01/07/2026 – 30/10/2026
Client Account: CA-40219 (Mill Lane Residential Car Park, Site 0722)
Account Holder: Wexcombe Mill Court Management Co. Ltd
Payment Due By: 13/11/2026
Sort Code: 20-44-18  Account No: 73160892  Ref: CA-40219

PCN No.     Date Issued  Vehicle Reg   Contravention Code   Status        Amount (GBP)
HP20190817  12/07/2026  YK23 TRN      OV04 (Overstay)      Paid          0.00
HP20190822  19/07/2026  MW71 BLO      OV04 (Overstay)      Appealed      60.00
HP20190841  02/08/2026  LF19 HKD      NP01 (No Permit)     Cancelled     0.00
HP20190859  14/08/2026  YK23 TRN      OV04 (Overstay)      Unpaid        60.00
HP20190903  29/08/2026  PN22 ZVE      NP01 (No Permit)     Unpaid        60.00
HP20190917  06/09/2026  CE68 WQA      OV04 (Overstay)      Unpaid        60.00
HP20190934  21/09/2026  MW71 BLO      OV04 (Overstay)      Unpaid        60.00
HP20190951  09/10/2026  BD17 JRX      NP01 (No Permit)     Unpaid        60.00

Summary
Total issued (period):   8
Cancelled / Paid:        2
Under appeal:            1
Outstanding:             5
Total outstanding (GBP): 300.00

Account Balance Brought Forward (01/01/2026): 120.00 CR
Payments Received 15/07/2026 (BACS ref 88130217): 120.00
Balance Carried Forward: 0.00

Remarks: Site inspection log ref SI-0722-2026-088 referenced on PCN HP20190903 (Inspector: R. Tallack). Appeal HP20190822 lodged 24/07/2026, reference AP-7713-E, pending adjudication.

-----------------------------------------------------------------

Dear Accounts Team,

Please find enclosed the statement for Mill Lane for July to October. I am writing to dispute PCN HP20190859 (YK23 TRN, 14/08/2026) and PCN HP20190917 (CE68 WQA). Both vehicles are registered to residents of Flat 9 and Flat 14 and hold valid permits issued in March under our permit scheme, reference PS-0722-0061 and PS-0722-0074. The permit bays were re-marked in June and the new signage was not installed until late August, so the penalties were issued before drivers could reasonably know the bay rules had changed.

Your own Code of Practice, clause 6.4, says that a charge will not be enforced where the operator has not displayed compliant signage for the contravention. Our property manager has photographs of the signage dated 03/09/2026 only.

Regards,

Denise Okafor
Secretary, Wexcombe Mill Court Management Co. Ltd
d.okafor@millcourtmc.example | 01934 552 218
```

**q1 [infer]** Count PCNs on the statement with status 'Unpaid' that are not disputed in the secretary's letter. Judge by the status column, not the summary. Appealed, cancelled and paid PCNs are excluded. Count each PCN once.  
  `0` = None: fewer than 1 PCN; `1` = One: at least 1 but fewer than 2; `2` = Two: at least 2 but fewer than 3; `3` = Three: at least 3 but fewer than 4; `4` = Four or more: 4 or more  
  gold: {"0": 0.0114, "1": 0.018, "2": 0.031, "3": 0.92, "4": 0.0196} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [infer]** What share of the statement's total outstanding amount is covered by the PCNs the secretary's letter explicitly disputes? Use the summary's outstanding total as the base. Ignore the separate appeal. Round to the nearest whole per cent.  
  `0` = Minor: below 25%; `1` = Substantial: at least 25% but below 50%; `2` = Majority: 50% or more  
  gold: {"0": 0.0373, "1": 0.92, "2": 0.0427} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** As the site inspector, judge how strong the management company's signage defence is for the two disputed PCNs taken together. Weigh the overall balance: permit validity, the signage timing claimed, and the photographic evidence offered.  
  `0` = Very weak: the evidence gives the defence essentially no support for either PCN; `1` = Weak: the evidence supports the defence for at most one PCN, and only slightly; `2` = Moderate: the evidence clearly supports the defence for one PCN but is doubtful or contradicted for the other; `3` = Strong: the evidence clearly supports the defence for both PCNs  
  gold: {"0": 0.1325, "1": 0.28, "2": 0.5375, "3": 0.05} · agreement 3/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [judge]** Judge how internally consistent the account statement's figures and records are. Weigh the overall balance between the figures that reconcile and any unexplained or odd entries. Use only the statement section of the document.  
  `0` = Consistent: all figures reconcile and nothing needs explaining; `1` = Minor queries: the core counts and totals reconcile, but some entries are odd or unexplained; `2` = Unreliable: the main counts or totals contradict each other  
  gold: {"0": 0.1375, "1": 0.775, "2": 0.0875} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F3-0153  ·  F3 Conflicting evidence  ·  wedding venue  ·  system record

```json
{
 "rec_id": "SUP-0417",
 "record_type": "supplier_review",
 "supplier": {
  "trading_name": "Hollin & Reed Catering Ltd",
  "companyNo": "08812946",
  "contact_name": "Bronwen Afolabi",
  "email": "bookings@hollinreedcatering.example",
  "phone": "01298 554071",
  "region": null
 },
 "assessment_window": {
  "from": "2024-11-01",
  "to": "2026-10-29",
  "last_reviewed": "2025-10-14"
 },
 "scores": {
  "fsa_hygiene_rating": "4",
  "prev_hygiene_rating": "5",
  "fsa_inspection_ref": "FHR-44190-B",
  "last_inspection_date": "2026-09-22",
  "prev_inspection_date": "2025-03-07",
  "on_time_delivery_pct": "96.2",
  "complaints_12m": 2,
  "avg_review_stars": "4.6",
  "price_index": "1.08",
  "weddings_served_ytd": "31"
 },
 "insurance": {
  "public_liability_gbp": "5000000",
  "policy_no": "PL-7720-4481",
  "expiry": "2027-02-28",
  "excess_gbp": "250"
 },
 "priority_rule": "Per Procurement Standard PS-6 cl. 4.2, food safety and public liability criteria take precedence over price, delivery and guest feedback; any open improvement notice blocks approval irrespective of other scores.",
 "open_notices": [
  {
   "notice_no": "HN-2026-0331",
   "issued": "2026-09-22",
   "status": null
  }
 ],
 "reviewer_obs": {
  "src": "site visit 2026-10-02",
  "obs": "Prep area clean; walk-in chiller log complete through September."
 },
 "third_party_obs": {
  "src": "Ashcombe Parish Hall events feedback",
  "obs": "Cold food reported at two August events; supplier replaced items same evening."
 },
 "notes": "Bronwen was very good about the August complaints when I rang her, and honestly the rest of the file is strong, with the flour-dust and allergen training certificates all current and the Saturday drop-offs arriving on time for almost every wedding since spring. The bit I keep returning to, and which isn't on the form, is that the council portal shows HN-2026-0331 as closed on 2026-10-10 but the paper copy in the folder still says open and nobody has filed the closure letter, so I can't tell which is right. Rating scores 4 for Sept 2026 and the 2025 inspection was a 5, so something slipped over the summer. Will chase the inspector's email before the November committee.",
 "legacy_ref": null,
 "internal_tag": "x-old-17",
 "created_by": "dmoss",
 "last_modified": "2026-10-27T16:42:09Z"
}
```

**q1 [infer]** Rate how many of the supplier's food safety and public liability criteria (per the priority rule) are currently satisfied on the document's evidence: current hygiene rating of 4 or above, no unresolved improvement notice, public liability in date, and cover of at least £5,000,000. Count a criterion as met only if evidence is clear.  
  `0` = None: no criteria clearly met; `1` = One: exactly one criterion clearly met; `2` = Two: exactly two criteria clearly met; `3` = Three: exactly three criteria clearly met; `4` = Four: all four criteria clearly met  
  gold: {"0": 0.0058, "1": 0.0124, "2": 0.0429, "3": 0.9199, "4": 0.019} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [judge]** Judge how strongly the document supports approving this supplier now. Weigh the priority rule first: an open improvement notice blocks approval regardless of other scores. Where the notice's status is unresolved, treat it as a block until proven closed.  
  `0` = Not supported: approval should be withheld pending proof the notice is closed; `1` = Conditionally supported: approval possible subject to specific confirmed conditions; `2` = Fully supported: approval clearly justified on current evidence  
  gold: {"0": 0.895, "1": 0.0925, "2": 0.0125} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** Judge the supplier's operational reliability for weddings over the most recent season, weighing delivery punctuality, complaints, guest reviews and the August cold-food incidents together, giving most weight to recent events and how they were remedied.  
  `0` = Poor: reliability problems dominate; `1` = Mixed: good and poor evidence roughly balanced; `2` = Strong: reliability is good overall despite minor lapses  
  gold: {"0": 0.04, "1": 0.3475, "2": 0.6125} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [judge]** Judge how much the food safety trend between the 2025 and September 2026 inspections should worry the venue owner. Give priority to hygiene-rating change and the status of the notice over supportive observations such as the clean site visit; the overall balance is to be judged.  
  `0` = None: no concern; `1` = Slight: minor concern, adequately offset by other evidence; `2` = Moderate: real concern needing follow-up before relying on supplier; `3` = High: serious concern, likely a safety failing; `4` = Severe: clear and continuing safety failure  
  gold: {"0": 0.025, "1": 0.1875, "2": 0.6625, "3": 0.1125, "4": 0.0125} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F3-0037  ·  F3 Conflicting evidence  ·  energy supplier  ·  system record

```json
{
 "rec_id": "CBT-449120",
 "exported_at": "2026-10-29T16:42:07Z",
 "export_by": "svc_cbt_export",
 "account": {
  "acct_no": "70314-866",
  "supply_type": "DUAL",
  "tariff_code": "VAR-FIX12-E",
  "tariff_start": "2025-03-01",
  "mpan": "1700034998213",
  "mprn": null,
  "meter_serial": "E18G-22760",
  "addr_key": "ADR-0047-KB"
 },
 "customer": {
  "name_on_acct": "R. Oduya-Brennan",
  "contact_pref": "email",
  "vuln_flag": "N",
  "vuln_review": "PENDING",
  "complaints_12m": "2",
  "nps_bucket": null
 },
 "billing": {
  "last_inv_ref": "INV-2026-09-88012",
  "last_inv_gbp": "214.67",
  "credit_bal_gbp": "-38.10",
  "dd_status": "SUSPENDED",
  "est_reads_6m": 4,
  "act_reads_6m": 2,
  "trend_3m_kwh_per_day": "11.4"
 },
 "complaint": {
  "case_ref": "CMP-2026-1184",
  "category": "BILLING_ACCURACY",
  "opened": "2026-10-03",
  "handler_queue": "CBT-REVIEW-B",
  "criteria_weighting": "Actual reads outrank estimates; customer readings count only with a photo dated within 14 days of the period end. Vulnerability timing (VUL-3 s.2) overrides standard response times.",
  "refund_rule": "Refund under 7.4(b) applies unless a written estimate notice was issued under 5.2 before the read date, in which case the estimate stands for that period. See 5.2 notice log below."
 },
 "evidence": [
  {
   "src": "AMR_HH_FEED",
   "read_kwh": "18842",
   "read_date": "2026-08-31",
   "photo": null
  },
  {
   "src": "CUST_PORTAL",
   "read_kwh": "16210",
   "read_date": "2026-09-14",
   "photo": true
  },
  {
   "src": "FIELD_VISIT",
   "read_kwh": "16190",
   "read_date": "2026-09-16",
   "photo": null
  }
 ],
 "notice_log": [
  {
   "type": "EST_NOTICE_5.2",
   "sent": "2026-08-19",
   "addr_used": "ADR-0031-KB",
   "returned": null
  }
 ],
 "legacy_crm_colour": "teal",
 "print_batch": "PB-22-0907",
 "notes": "Customer rang on 06/10 again, very upset, saying her partner has been away since July and the house was barely used over summer, so the bills make no sense, and she has been lovely about it but the thing is the 5.2 notice went out on 19/08 to the old postal address (ADR-0031-KB) which she says she left in May, so whether she ever received it is unclear. Agent J. Pirie noted the AMR feed looks high against the portal and field readings but did not close the vulnerability review, which is still pending."
}
```

**q1 [compare]** Ignoring reading dates and order, how large is the absolute difference in kWh between the customer portal reading and the field visit reading? Use the figures as recorded; do not adjust for the days between them.  
  `0` = Small: difference of less than 100 kWh; `1` = Moderate: difference of at least 100 kWh but below 1,000 kWh; `2` = Large: difference of 1,000 kWh or more  
  gold: {"0": 0.92, "1": 0.0533, "2": 0.0267} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [infer]** Count how many of these four record facts favour the customer, each weighed equally: notice sent to an address key differing from the account's; estimated reads outnumbering actual reads in the last six months; vulnerability flag set to Y; notice log showing the notice returned undelivered.  
  `0` = None: no fact favours the customer; `1` = One: exactly one fact favours the customer; `2` = Two: exactly two facts favour the customer; `3` = Three: exactly three facts favour the customer; `4` = Four: all four facts favour the customer  
  gold: {"0": 0.0091, "1": 0.0423, "2": 0.92, "3": 0.0229, "4": 0.0057} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** Judge, on the overall balance of the record, how strongly the evidence supports the supplier's estimate standing for the disputed period under the 5.2 notice rule, as opposed to a refund. Weigh the timing of the notice against doubts about its delivery.  
  `0` = Weak: the evidence mostly points to a refund, and the estimate standing is poorly supported; `1` = Contested: supporting and opposing evidence are roughly balanced, so the estimate standing is only partly supported; `2` = Strong: the evidence mostly supports the estimate standing, with little real doubt over the notice  
  gold: {"0": 0.325, "1": 0.5925, "2": 0.0825} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [infer]** How many full calendar days had the complaint been open at the export timestamp, counting from the opened date to the export date? Later notes or call dates do not change the start point.  
  `0` = Under four weeks: fewer than 28 days; `1` = Four to under eight weeks: at least 28 days but fewer than 56 days; `2` = Eight weeks or more: 56 days or more  
  gold: {"0": 0.92, "1": 0.065, "2": 0.015} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F3-0168  ·  F3 Conflicting evidence  ·  fishing fleet  ·  meeting notes

```
MEETING NOTES — Glenmarrow Fishing Co-operative: Landing Office & Quota Review

Date: Thursday 29 October 2026
Time: 14:00–14:50
Location: Landing office, Unit 4, Harbour Quay (back room, kettle broken again)
Minutes taken by: Tamsin Okonedo (landing clerk)

Attendees: Tamsin Okonedo (TO), Rory Figgis (RF, quota secretary), Bronagh Lusk (BL, vessel liaison), Dr. Anwen Pryce (AP, stock assessment adviser, joined by phone from 14:20)
Apologies: Ewan Caddick (chair) — at the Fishermen's Hall re insurance renewals

1. Opening
TO circulated the October landings summary before the meeting. RF said he had not had time to read it properly as he was in Ardglen until Tuesday night dealing with the mackerel allocation letter, which came in on a Friday, which is always the way, and then the printer in the back office ate two pages of it. BL asked whether the tally sheets for the Morag Rose had been reconciled yet, as the skipper keeps ringing about it. TO said they had, mostly, bar one trip on 9 October where the weighbridge docket and the handwritten sheet disagree by about 40 kg of haddock. Carried to item 3.

2. Retained landings against Q3 allocation
RF reported that the co-op has landed 61.4 t of North Sea cod against a Q3 allocation of 78.0 t, leaving 16.6 t. He said this is the healthiest position the co-op has been in since the spring of 2024 and that the rolling average over the last six weeks is roughly 2.1 t per fortnight above the same period last year. He attributed most of this to the Kilbride boats fishing further north. BL pointed out that the Kilbride boats had been out for only nine days in the last fortnight owing to the gearbox fault on the Sanna Mhor and that the apparent improvement is mostly one vessel's catch. RF accepted that but said the trend line still goes up.
Note: TO's figures are from the weighbridge; RF's from the quota ledger. They do not yet match.

3. Morag Rose docket discrepancy
TO said the 9 October trip shows 1,118 kg of haddock on the weighbridge docket (ref WB-20261009-07) but 1,078 kg on the handwritten landing sheet. RF said the ledger has 1,078 kg, and that the weighbridge was recalibrated on 2 October, so the docket is the one to be distrusted. TO said the recalibration certificate is dated 6 October, which means the docket was printed before the certificate existed, and the calibration was done on the Tuesday after, not before. RF said he had been told it was the Monday. Nobody had the certificate in the room. BL asked that the difference be recorded as unresolved.

4. Stock assessment advice (AP joined)
AP said the provisional advice for the western haddock stock suggests a stable spawning biomass for 2027, but that the survey index for the last two summers has been falling and she would not want the co-op to read a stable figure as a reason to increase effort. She said the advice is provisional until the November survey report is out and that the 2026 year-class estimate is based on very few otoliths. RF asked whether that meant the co-op could carry extra haddock quota forward. AP said she could not advise on carry-forward rules as that sits with the Authority, not with her.

5. Compliance thresholds
TO asked how the co-op's compliance rating should be weighted when a trip is clean on paperwork but the catch is over the notional allocation for that species. RF said the Authority rule (Cooperative Quota Procedures, clause 7.3) is that landing documentation accuracy takes priority over the quota position, so a discrepancy of more than 2% on a single trip is recorded as a documentation fail regardless of tonnage. BL said clause 7.3 was revised in March and the 2% figure is now 5%. RF said he has the March version and it still says 2%. Not resolved; TO to check the version currently published on the Authority portal.

Actions
- TO: obtain the weighbridge recalibration certificate and confirm the date of calibration (by Mon 2 Nov).
- TO: check the current published version of Cooperative Quota Procedures clause 7.3 and confirm the discrepancy threshold (by Mon 2 Nov).
- RF: reconcile the quota ledger against the October weighbridge dockets and circulate by Fri 6 Nov.
- BL: speak to the Sanna Mhor skipper about expected return to service date.
- AP: send the November survey report summary to RF when available.

Next meeting: Thursday 12 November 2026, 14:00, same room if the kettle is still broken.

Minutes approved by: ______________________ (chair) Date: __________
```

**q1 [infer]** Using the quota secretary's reported North Sea cod figures (ledger), what share of the co-op's Q3 allocation remained unlanded at the meeting? Divide remaining tonnage by the Q3 allocation, giving a percentage; ignore the unresolved mismatch with weighbridge figures.  
  `0` = Low: below 25% of the allocation remains; `1` = Middle: at least 25% but below 50% remains; `2` = High: 50% or more remains  
  gold: {"0": 0.92, "1": 0.0655, "2": 0.0145} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [judge]** Overall, how strong is the evidence in the notes that the co-op's cod landings are genuinely improving? Weigh the quota secretary's rolling average and trend against the liaison's point about fewer fishing days and one vessel's catch; judge the overall balance.  
  `0` = Weak: the improvement is mostly explained by a single vessel or short-term effects and is not shown to be genuine; `1` = Moderate: some real signs of improvement, but significant doubts remain about how broad it is; `2` = Strong: the improvement is broad-based and not seriously challenged  
  gold: {"0": 0.5875, "1": 0.37, "2": 0.0425} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [infer]** For the 9 October Morag Rose haddock trip, work out the gap between the weighbridge docket and the handwritten landing sheet as a percentage of the handwritten sheet figure. Round to one decimal place; ignore which record is correct.  
  `0` = Negligible: below 1%; `1` = Small: at least 1% but below 2%; `2` = Moderate: at least 2% but below 3%; `3` = Notable: at least 3% but below 4%; `4` = Large: 4% or more  
  gold: {"0": 0.0064, "1": 0.0096, "2": 0.016, "3": 0.92, "4": 0.048} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [judge]** How much caution about increasing haddock fishing effort does the stock adviser's provisional advice support? Weigh the stable 2027 biomass projection against the falling survey index and thin year-class data; judge the overall balance.  
  `0` = None: evidence supports increasing effort; `1` = Slight: effort may rise with minor reservations; `2` = Clear: no increase in effort until the final survey report, though no cut is called for; `3` = Strong: evidence calls for an immediate reduction in effort  
  gold: {"0": 0.035, "1": 0.2425, "2": 0.675, "3": 0.0475} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F3-0177  ·  F3 Conflicting evidence  ·  construction site  ·  system record

```json
{
 "RecordRef": "SO-HSR-2026-1027-044",
 "site_id": "BLD-7713-KW2C",
 "Site Name": "Kestrel Wharf Phase 2, Block C",
 "reporting_date": "2026-10-27",
 "report_type": "weekly_site_safety_review",
 "compiledBy": {
  "name": "Dorota Nwachukwu",
  "role": "Site Manager",
  "ext": "2214",
  "email_domain": "kestrelbuild.example"
 },
 "hs_adviser": {
  "name": "Tomas Ellery",
  "CSCS_no": "1184230",
  "last_visit": "2026-10-23"
 },
 "metrics": {
  "headcount_on_site": "63",
  "subcontractor_firms": 9,
  "ppe_compliance_pct": "96.5",
  "inductions_completed_wk": "14",
  "lti_days_since": "0",
  "RIDDOR_reportable_ytd": "1"
 },
 "recent_period": {
  "window": "2026-10-06 to 2026-10-27",
  "near_miss_reports": "9",
  "previous_three_wk_avg": "2.3",
  "toolbox_talks_attended_pct": "91"
 },
 "permits": {
  "hot_works_open": 2,
  "lift_plan_ref": "LP-C-0931-R3",
  "hoist_H2_status": "out_of_service",
  "hoist_H2_fault_log": [
   {
    "t": "2026-10-27T07:40",
    "code": "E-117"
   },
   {
    "t": "2026-10-27T11:15",
    "code": "reset_ok"
   }
  ]
 },
 "open_actions": [
  {
   "id": "A-0418",
   "item": "Edge protection L4 east elevation",
   "Status": "disputed",
   "raised_by": "T. Ellery",
   "due": "2026-10-31",
   "photo_ref": null
  },
  {
   "id": "A-0421",
   "item": "Scaffold tag check, bay 6-9",
   "Status": "closed",
   "raised_by": "K. Oduya",
   "due": "2026-10-24"
  }
 ],
 "policy_ref": {
  "doc": "HSP-04",
  "clause": "3.2",
  "priority_rule": "Where programme dates and life-safety controls conflict, life-safety governs. Where two hazard ratings differ, the higher rating applies until physically verified."
 },
 "rating_inputs": {
  "fall_from_height": "high",
  "lifting_ops": "medium",
  "housekeeping": "low"
 },
 "sign_off": null,
 "notes": "So the Monday walk was a bit of a mad one because the hoist was out of action from about 07:40 until the engineer got it back at 11:15, and everyone kept asking whether the east edge at level 4 had been signed off. Dorota says Kieran signed it off on the 14th, but Kieran says he only looked at the north side and never got round to the east, so I've logged A-0418 as disputed until someone photographs it, and the programme wants the cladding crew on that elevation by Friday. Toolbox attendance and near-miss reporting have both picked up since the 6th, which I think is people trusting the form, though it may flatter us, so please don't close A-0418 on verbal confirmation alone."
}
```

**q1 [judge]** Rate the severity of the unresolved fall-from-height risk at the level 4 east elevation as at 27 October 2026. Weigh the policy rule (life-safety over programme; higher rating applies until physically verified) above the verbal sign-off claims.  
  `0` = Negligible: control verified and no conflicting evidence or pressure to proceed; `1` = Low: control probably in place, with only minor open doubt and no programme pressure; `2` = Moderate: control status uncertain, but no imminent exposure of workers; `3` = High: control unverified and a conflicting sign-off, with exposure possible soon; `4` = Critical: control unverified under the policy rule, a high hazard rating, and imminent work exposure with no physical evidence  
  gold: {"0": 0.0, "1": 0.0, "2": 0.055, "3": 0.3825, "4": 0.5625} · agreement 3/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [judge]** Rate how strongly the document supports the view that the rise in near-miss reporting and toolbox attendance since 6 October reflects a real improvement in site safety performance, rather than a reporting effect. Judge the overall balance of the evidence.  
  `0` = None: evidence points wholly to a reporting artefact or deterioration; `1` = Limited: the rise is shown, but the document leans towards a reporting effect or doubts its meaning; `2` = Substantial: the rise is shown and the balance favours genuine improvement, with some doubt; `3` = Conclusive: the rise is shown and corroborated by independent outcome evidence of improvement  
  gold: {"0": 0.0875, "1": 0.7625, "2": 0.145, "3": 0.005} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [infer]** Compare the near-miss reports per week in the window 6 to 27 October 2026 (three weeks) with the previous three-week average, taken as reports per week. Rate the ratio of recent weekly rate to previous average, to two decimal places.  
  `0` = Fall: ratio below 1.00; `1` = Modest rise: ratio at least 1.00 but below 1.50; `2` = Marked rise: ratio at least 1.50 but below 2.00; `3` = Large rise: ratio of 2.00 or more  
  gold: {"0": 0.0114, "1": 0.92, "2": 0.0381, "3": 0.0305} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [judge]** Rate the extent to which hoist H2 is restricted from use at the end of 27 October 2026. Where the undated status field conflicts with timestamped fault log entries and the notes, the latest timestamped evidence takes priority.  
  `0` = Unrestricted: latest evidence shows it was reset and returned to service; `1` = Restricted or uncertain: latest evidence leaves its return to service unclear or conditional; `2` = Unavailable: latest evidence shows it remains out of service  
  gold: {"0": 0.8125, "1": 0.15, "2": 0.0375} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F3-0086  ·  F3 Conflicting evidence  ·  parcel depot  ·  policy extract and case note

```
HAVERBROOK PARCEL HUB — DRIVER CONDUCT AND SERVICE RECOVERY POLICY
Document ref: HPH-OPS-DC-07 | Version 3.2 | Effective 1 September 2026 | Owner: Depot Operations Manager, Northern Sort Hub

Extract: Sections 4 to 6

4.1 Each courier driver is assessed against the Delivery Reliability Score (DRS), calculated monthly from scans, signature captures and customer contact logs.

4.2 DRS weighting: failed-first-attempt rate 40%; safe-place compliance 25%; complaint substantiation rate 25%; timing accuracy 10%.

4.3 Where two criteria conflict in a single case, Section 4.2 weighting applies. Safe-place compliance may not be overridden by timing accuracy under any circumstances.

4.4 Complaints are recorded against the driver ID on the parcel scan, not the depot ID. Shared-van scans are attributed to the driver holding the handheld at the last successful scan.

5.1 A complaint is substantiated where scan data, photographic evidence or a witness statement from a second party supports the customer account.

5.2 Where sources disagree, the handheld timestamp takes precedence over the telematics log, and the telematics log takes precedence over verbal driver statements.

5.3 EXCEPTION: A complaint is not to be recorded as unsubstantiated where the driver's handheld has been reported lost, damaged or offline for more than 20 minutes in the relevant window, provided the driver has raised a Device Incident Form (DIF) before the end of the shift in which the event occurred. Handheld records for the DIF window are then excluded from Section 5.2.

6.1 Service recovery credit of up to £15.00 may be issued by the customer service agent without supervisor approval.

6.2 Credits above £15.00, or any credit following a second complaint on the same parcel, require Team Leader sign-off.

Case note: Parcel HP4471872203, complaint logged 14 October 2026 by Mrs D. Okafor (Millbrook Lane). Customer states parcel was marked delivered at 16:42 with no safe-place photo; parcel was not on premises at 17:10 and was later found in a neighbour's porch. Driver ID HPD-0931 (R. Lindqvist). Driver's 12-month DRS is 0.91, the highest in the Northern team, with safe-place compliance at 99%. However, September DRS fell to 0.74 after a run of three substantiated complaints, and his handheld shows an offline gap 16:31–16:55 with no DIF on file. Telematics places the van stationary at Millbrook Lane 16:28–16:49. Driver states the handheld dropped signal and he left the parcel "in the usual place". Neighbour's statement, received 21 October, confirms delivery to her porch at approximately 16:50 and says she telephoned the depot on 16 October. No record of that call located. Customer requests £25.00 credit and a written apology.
```

**q1 [judge]** Judge how strongly the whole body of evidence in the case note supports Mrs Okafor's account that the parcel was wrongly marked delivered and left unsafely. Weigh handheld, telematics, neighbour statement and driver statement by the Section 5.2 precedence, and judge the overall balance.  
  `0` = Weak: the evidence mostly contradicts or fails to support the customer's account; `1` = Moderate: the evidence is evenly split or only partly supports the customer's account; `2` = Strong: the balance of evidence clearly supports the customer's account  
  gold: {"0": 0.035, "1": 0.2425, "2": 0.7225} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [read]** Rate how many of the Section 5.3 exception's stated conditions the case note shows as met, so that the complaint could not be recorded as unsubstantiated on that basis. Count only the offline duration and the DIF being raised before shift end.  
  `0` = None: neither condition is shown as met; `1` = One: exactly one condition is shown as met; `2` = Both: both conditions are shown as met  
  gold: {"0": 0.0425, "1": 0.92, "2": 0.0375} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** Judge how far the driver's strong 12-month DRS and 99% safe-place compliance should reduce the weight given to this complaint, when set against the September DRS and the case-specific evidence. Judge the overall balance for this case.  
  `0` = Negligible: the strong record should hardly affect the outcome; `1` = Some: the record is a modest mitigating factor only; `2` = Decisive: the record should largely outweigh the complaint evidence  
  gold: {"0": 0.6, "1": 0.3575, "2": 0.0425} · agreement 3/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** Rate the credit the agent may issue alone and approve without Team Leader sign-off, relative to the customer's £25.00 request. Use Section 6 limits; the complaint is the first on this parcel. Rate the shortfall of the agent's own authority below the request, in pounds.  
  `0` = No shortfall: the request is within the agent's authority (shortfall £0 or less); `1` = Small: shortfall above £0 but below £5.00; `2` = Moderate: shortfall at least £5.00 but below £10.00; `3` = Large: shortfall at least £10.00 but below £15.00; `4` = Very large: shortfall £15.00 or more  
  gold: {"0": 0.0137, "1": 0.016, "2": 0.0343, "3": 0.92, "4": 0.016} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F3-0114  ·  F3 Conflicting evidence  ·  car park enforcement  ·  handwritten log transcription

```
HARBOURSIDE CAR PARKS LTD: SITE ATTENDANT DAILY LOG
Site: Quayside MSCP, Bay Row C | Attendant: D. Pellow | Sheet 14 of 31
Per Appeals Procedure AP-4 s.3.2, where an ANPR entry time and a handwritten log conflict, the ANPR record governs. Driver history (AP-4 s.5.1) is weighed only after mitigation has been considered.

21/10/26 06:50 Shift start. Frost on ramp again, salted lower deck myself as gritter still broken since 3rd (reported FM-112, ref 88412, nobody out yet). Kiosk 2 printer jammed, fixed. Quiet day, cinema crowd thin because of rain, not complaining.

22/10/26 14:10 Round C deck. Lights out on C9, logged it. White van blocking C2 loading, moved on, no ticket, was unloading a fridge.

22/10/26 18:05 [struck through] 18:15. Silver Golf in C14, reg as PCN 4471203. Driver came to kiosk 2 approx 18:20, very apologetic, showed phone with pay-by-phone receipt, session he reckoned ran to 18:30. Screen glary, couldn't read end time properly. He was in a hurry, nephew's [illegible] at the hall. Told him to pay difference at machine, sorry for the trouble. Didn't chalk, didn't ticket.

23/10/26 09:40 Cashless operator rang re: C14 query. Their record shows session ended 17:45. Passed to office. Also PCN 4471028 (19/10) same bay, not mine, check.

28/10/26 Office note (JH): ANPR entry 17:12 on 22/10. Plate has 4 PCNs in 2025 (4470917, 4470655, 4470201, 4469988), none since 01/09/26. Appeal fee refund £25 pending. Early-bird rate was £2 not £30 that day, check.
```

**q1 [compare]** By how many minutes had the car passed the cashless operator's recorded session end when the attendant saw it, using the corrected log time (not the struck-through one) and the operator's record rather than the driver's recollection?  
  `0` = Brief: under 15 minutes past the operator's session end, or not past it; `1` = Moderate: at least 15 but under 45 minutes past the operator's session end; `2` = Long: 45 minutes or more past the operator's session end  
  gold: {"0": 0.0387, "1": 0.92, "2": 0.0413} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [infer]** How long had the Golf been on site when the attendant noted it? Measure from the ANPR entry time, which governs over any handwritten entry, to the corrected log time (not the struck-through one). Unit: whole minutes.  
  `0` = Very short: under 30 minutes; `1` = Short: at least 30 but under 45 minutes; `2` = Medium: at least 45 but under 60 minutes; `3` = Long: at least 60 but under 75 minutes; `4` = Very long: 75 minutes or more  
  gold: {"0": 0.0128, "1": 0.0144, "2": 0.0336, "3": 0.92, "4": 0.0192} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** How strong is the driver's mitigation case for cancelling the penalty, judged on the overall balance of the document's evidence (his account, receipt, attendant's remarks, operator's record), before any driver history is considered?  
  `0` = None: the evidence offers no mitigation; `1` = Weak: little mitigation, largely outweighed by contrary evidence; `2` = Moderate: real mitigation but substantially offset by contrary evidence; `3` = Strong: clear mitigation with only minor contrary evidence; `4` = Compelling: mitigation is clear and uncontradicted  
  gold: {"0": 0.1125, "1": 0.5125, "2": 0.3175, "3": 0.05, "4": 0.0075} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [judge]** How adverse to the driver is the plate's penalty history, judged on overall balance: weigh the number of confirmed earlier notices against how long ago they were, and give no weight to the unconfirmed PCN 4471028.  
  `0` = None: nothing adverse; `1` = Slight: minor adverse history; `2` = Moderate: noticeable adverse history, partly offset by a recent clean period; `3` = Substantial: heavy adverse history with little offset; `4` = Severe: extensive and recent adverse history  
  gold: {"0": 0.0175, "1": 0.1375, "2": 0.525, "3": 0.29, "4": 0.03} · agreement 3/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F3-0056  ·  F3 Conflicting evidence  ·  cold-chain logistics  ·  system record

```json
{
 "excursion_id": "EXC-2026-08817",
 "ref_no": "RT-FZ-44091",
 "createdAt": "2026-10-27T14:09:33Z",
 "status": "PENDING_REVIEW",
 "site": {
  "siteCode": "DC-NTH-02",
  "site_name": "Northmoor Cross DC",
  "zone": "FZ-B",
  "dock_door": "7",
  "paint_code": "RAL 5010"
 },
 "shipment": {
  "shipment_no": "SHP-998213407",
  "consignee": "Harrowgate Grocers Ltd",
  "product_desc": "Frozen vegetable mix 2.5kg",
  "product_code": "FVM-25-G",
  "qty_cases": 480,
  "pallets": "12",
  "prev_shipment_ref": "SHP-998207762",
  "dispatch_core_c": "-19.2"
 },
 "band": {
  "setpoint_c": -18,
  "lower_c": -22,
  "upper_c": -15,
  "max_minutes_above_upper": 45
 },
 "loggers": [
  {
   "logger_id": "TL-3381",
   "type": "wireless_probe",
   "min_c": -21.8,
   "max_c": -9.4,
   "minutes_above_upper": "42",
   "cal_cert_date": "2026-07-14"
  },
  {
   "logger_id": "TL-3390",
   "type": "wireless_probe",
   "min_c": -20.9,
   "max_c": -16.1,
   "minutes_above_upper": "0",
   "cal_cert_date": "2026-02-03"
  }
 ],
 "handheld": {
  "taken_by": "M. Obi",
  "time": "06:52",
  "reading_c": "-14.6",
  "probe_ref": "HH-07",
  "Notes": null
 },
 "carrier": {
  "name": "Brackwell Haulage",
  "trailer_reg": "KX68 HNP",
  "toll_tag_no": "70215-883",
  "excursions_prior_90d": "6",
  "excursions_last_30d": 0
 },
 "rule": {
  "rule_id": "TX-R4",
  "statement": "Cumulative time above upper band over 45 minutes triggers reject review.",
  "exception": {
   "exception_id": "TX-R4.3",
   "clause": "Does not apply where dispatch core temperature is at or below -20 and both loggers hold current calibration per section cal_status."
  }
 },
 "cal_status": {
  "validity_days": 180,
  "TL-3381_valid_to": "2027-01-10",
  "TL-3390_valid_to": null
 },
 "priority": {
  "basis": "SOP CC-7.2 section 3",
  "rule": "Where logger data and handheld readings conflict, logger data governs. Where time-above-band and core temperature criteria conflict, core temperature governs.",
  "weighting_table": "W-1"
 },
 "fuel_card_ref": "FC-4410-2291",
 "invoice_no": "INV-260917",
 "notes": "Probe TL-3381 recorded a peak of -9.4 at 05:58 while TL-3390 on the same pallet row stayed below -16.1. Handheld reading at 06:52 is inside band; driver reports door left open for approximately 9 minutes during unloading at gate 3."
}
```

**q1 [judge]** Judge, from the whole record, how much unresolved doubt remains about the reliability of the temperature evidence for this shipment. Weigh the overall balance of calibration status, logger agreement, handheld agreement and margin to the time limit. Do not rate whether rejection is warranted.  
  `0` = None: the instruments are all current and consistent, and no figure sits close to a limit; `1` = Minor: one small inconsistency exists, but the main evidence is sound and clear of the limits; `2` = Substantial: some significant inconsistencies or gaps exist, but most of the evidence remains usable; `3` = Severe: several independent problems undermine the evidence at once, such as a lapsed or missing calibration, instruments that disagree strongly, a conflicting handheld reading, and a result close to the limit  
  gold: {"0": 0.0075, "1": 0.025, "2": 0.1975, "3": 0.77} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [judge]** Judge how strongly the record supports rejecting the shipment for temperature excursion under rule TX-R4 as written. Where criteria conflict, apply the stated priority: logger data over handheld, and core temperature over time-above-band.  
  `0` = Unsupported: no logger exceeds the time limit and the core temperature is within band, so reject review is not triggered; `1` = Arguable: the evidence is split, so reject review could reasonably be triggered or not; `2` = Strongly supported: the time limit is exceeded or the governing core temperature is out of band, so reject review is clearly triggered  
  gold: {"0": 0.755, "1": 0.205, "2": 0.04} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** Judge how many of the two conditions of exception TX-R4.3 fail to be met for this shipment: dispatch core at or below -20, and both loggers holding current calibration at the excursion date. Work out a missing expiry from the certificate date and validity days.  
  `0` = None fail: both conditions are met, so the exception applies in full; `1` = One fails: exactly one of the two conditions is not met; `2` = Both fail: neither condition is met, so the exception cannot apply  
  gold: {"0": 0.01, "1": 0.065, "2": 0.925} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [judge]** Rate how severe the highest credible temperature peak was, as degrees Celsius above the upper band limit. Logger data governs over the handheld reading. Where the two loggers differ, use the higher peak from a logger whose reading is not contradicted by its own record.  
  `0` = Slight: the peak is below 2 C above the upper limit, or within band; `1` = Moderate: the peak is at least 2 C but below 5 C above the upper limit; `2` = Large: the peak is at least 5 C above the upper limit  
  gold: {"0": 0.1125, "1": 0.1375, "2": 0.75} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F3-0011  ·  F3 Conflicting evidence  ·  veterinary practice  ·  chat log

```
Riverbank Small Animal Clinic — Case Chat Log
Case ref: RSAC-26-04417 | Patient: "Biscuit" (canine, Cavalier King Charles Spaniel, M/N, 7y 2m, 9.4 kg) | Owner: M. Okonkwo | Policy: PetCare Plus 3 (PP3-0221788)

[Mon 26/10/2026 08:52] Dr Helen Brask: Morning all. Biscuit in for recheck after Thursday's collapse episode. Holter from Friday is back, sending to the file now.
[Mon 26/10/2026 08:58] Ravi Chandler (Vet Nurse): Holter summary: 3 runs of SVT, longest 11 beats, HR 212 max. No runs logged since Saturday 18:40.
[Mon 26/10/2026 09:03] Dr Helen Brask: Good. Echo result from Thursday says mild MR only, no chamber dilatation. Can someone confirm the echo was the 14th not the 17th? Reception booked the owner call off the wrong date.
[Mon 26/10/2026 09:06] Lena Ferreira (Reception): I have the echo as Thu 22nd on the PMS. Owner was told Thu 22nd too.
[Mon 26/10/2026 09:07] Ravi Chandler (Vet Nurse): It was the 22nd, I ran it myself.
[Mon 26/10/2026 09:11] Dr Helen Brask: Fine, 22nd. Clinical sign-off rule per Practice Policy CP-7 s.4.2: where echo and Holter conflict, the cardiologist report governs and the attending vet documents the reason. We don't have the cardiology report yet, so mark as provisional.
[Mon 26/10/2026 09:14] Lena Ferreira (Reception): Owner says Biscuit ate normally this morning, first time in 4 days.
[Mon 26/10/2026 09:20] Dr Helen Brask: Good sign. Still start Sotalol 20mg BID from today per CP-7 s.6.1 unless cardiology says otherwise. Note: s.6.1 does not apply where the patient has a documented bradycardia event under 60 bpm, in which case refer to s.6.3 before dosing.
[Mon 26/10/2026 09:24] Ravi Chandler (Vet Nurse): Bradycardia logged Sunday 02:15, HR 54 on the monitor. Not in the Holter summary as it was a spot check on the ward.
[Mon 26/10/2026 09:26] Dr Helen Brask: Hold dosing. Will review s.6.3.
[Mon 26/10/2026 11:48] Miguel Tavares (Cardiology, referral): Cardiology report to follow Wednesday. Bradycardia event noted, does not on its own exclude sotalol.

Owner-reported status: Good appetite, two episodes of lethargy Sunday, no collapse since 19/10.
```

**q1 [judge]** Overall balance of the log: how firmly is the clinical sign-off on Biscuit's cardiac findings established as final at the end of the log (Mon 26/10/2026, 11:48)? Weigh the stated sign-off rule against what has actually been received.  
  `0` = Provisional: sign-off is explicitly provisional because the governing report is still outstanding; `1` = Partly settled: some governing evidence is in, but sign-off remains open on a significant point; `2` = Final: all governing evidence is in and sign-off is complete  
  gold: {"0": 0.87, "1": 0.1175, "2": 0.0125} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [judge]** Judge how strongly the log supports starting Sotalol dosing for Biscuit on 26/10/2026 itself. Weigh the vet's start instruction, the bradycardia event, the hold and the cardiology comment, giving priority to the latest recorded decision on dosing.  
  `0` = Not supported: dosing is held and there is no clear basis to start that day; `1` = Weakly supported: a basis exists but important conditions remain unresolved; `2` = Moderately supported: the balance favours starting but a procedural step is outstanding; `3` = Strongly supported: little stands in the way, only minor checks remain; `4` = Fully supported: dosing is authorised and unconditional  
  gold: {"0": 0.775, "1": 0.185, "2": 0.0325, "3": 0.005, "4": 0.0025} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [infer]** Count the distinct sources in the log (Holter summary, appetite report, echo result, owner-reported status) that on balance report Biscuit's condition as improving or reassuring as at 26/10/2026. Count each source once; sources that are mixed count only if their overall tone is reassuring.  
  `0` = None: no sources; `1` = One: exactly one source; `2` = Two: exactly two sources; `3` = Three or more: at least three sources  
  gold: {"0": 0.0225, "1": 0.13, "2": 0.4075, "3": 0.44} · agreement 3/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [judge]** How severe is the remaining risk that the echo date is wrong in the case record, once staff resolved it at 09:11? Weigh the PMS, owner, nurse and vet statements together.  
  `0` = Negligible: PMS, owner and nurse all match and the vet accepted it; `1` = Minor: a small residual discrepancy remains; `2` = Moderate: a discrepancy remains that could affect the record; `3` = Serious: dates remain contradictory and affect the claim  
  gold: {"0": 0.6025, "1": 0.3275, "2": 0.06, "3": 0.01} · agreement 3/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F3-0028  ·  F3 Conflicting evidence  ·  venue hire  ·  handwritten log transcription

```
KESTREL HOUSE EVENTS — FUNCTION ROOMS
Kitchen / Catering Shift Log (handwritten, transcribed from carbon book, Vol. 14)
Transcribed by: D. Okonjo-Reyes, Ops Admin, 03/11/2026

Log kept by Sous (Eastside) — pages 61–64 of Vol. 14

Mon 12/10
06:40 Van in early, fish delivery short 2 trays hake (Brodie Marine, inv BM-44817) — rang them, they say driver got the wrong postcode again, will send Thurs. Told Ade to stock up on the chilled chicken from the Tuesday lot instead. Fine.

Tue 13/10
Big one. Wedding of the Hartigan–Lowe party, 140 covers, Pavilion Room. Client rep (Mrs Pauline Hartigan, mob 07700 900 213) came in at 11 wanting to "just taste the lamb one more time before Saturday" — which she did, twice, and then asked for the dessert to be swapped to a lemon posset. Posset is fine, we make it for the Oct 28 corporate lunch anyway. Ticket for the Saturday is ref HV-0931, deposit £1,850 paid, balance due 14 days before. Note the balance deposit schedule is in the contract folder, not the CRM, which is why I keep checking.

Wed 14/10
Walk-in cold room temp logged 4.1°C at 07:15, 3.8°C at 13:00, fine. Dishwasher 2 down again, Pieter has the engineer booked for Friday (job ref SV-2207). Bought 6kg shallots off the cash & carry, receipt in the tin. Vegan options for the Nov 2 gala still not confirmed by the client — chased by email, no reply.

Thu 15/10
Fish came, all 2 trays, plus a box of mackerel nobody ordered. Sent back. Stock sheet says 38 portions of cod short on the Tuesday count, but Tom says he counted 41 and the sheet is wrong. Left it for Tom to sort, I am not doing the stock sheet again.

Fri 16/10
Quiet lunch. Pastry section 2 hours late in — Jonah says the butter was still in the walk-in from the Thurs delivery (not ours, it went to the Bridge Lane site by mistake). Rang Bridge Lane, they say it's ours. Nobody can prove anything. Hygiene check by the council man at 3pm, passed. He didn't look in the bin store so I didn't mention the pastry.

Sat 17/10
Hartigan wedding. Honestly, the best service we have had in months. Lamb rested beautifully, the team were on it, Pauline cried at the speeches (good tears). Client feedback card (ref FB-0517) reads "exceptional, would book again". Pauline asked for Priya by name. Only real hiccup: the cod course was held too long under the lamp before going out to table 9 and table 10, so they were lukewarm, and Jonah had to re-fire 22 portions with twenty minutes to spare. Quite a stressful twenty minutes. Pauline did not notice, or at least did not say.

Note, per Mr Abdi (Head of Operations) email 08/09, the rule stands: guest feedback outranks internal checklists when we write up an event, BUT any food safety deviation overrides both regardless of how well the guests rated it. I have written the cod hold up as a deviation in the HACCP book (p.88), not the feedback folder, because that is what it was.

Mon 19/10
Not sure whose sheet it is now. The Tuesday cod count went to Tom's spreadsheet and the cod course temperature record was 58°C at 12:20, which is above what we say we hold at (63°C min is the rule, so actually this is below). Read it twice. Thinking Pieter should look at the probe.

Thu 22/10
Quiet week, staff rota short by one (Ade off, flu). Nov 2 gala menu still open. Dessert freezer door seal torn again, ordered replacement, ref PO-3392, £86.40 inc VAT.
```

**q1 [read]** Count deliveries in the log (12/10 to 22/10) that arrived wrong, short or unordered where the supplier's fault is accepted or evident, not disputed. Exclude cases where nobody can establish whose error it was.  
  `0` = Few: at most one such delivery; `1` = Two: exactly two such deliveries; `2` = Many: three or more such deliveries  
  gold: {"0": 0.0675, "1": 0.865, "2": 0.0675} · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [judge]** Judge how favourable the official write-up of the Hartigan wedding (17/10) should be. Apply the log's stated rule: guest feedback outranks internal checklists, but any food safety deviation overrides both, whatever guests said.  
  `0` = Deviation-led: recorded mainly as a food safety deviation, not a success; `1` = Mixed: success with significant caveats recorded as equals; `2` = Exceptional: recorded as an outstanding success with only minor notes  
  gold: {"0": 0.6925, "1": 0.2575, "2": 0.05} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [read]** Using the log's 63°C minimum hold rule (not its confused wording), rate how far the recorded cod course temperature fell below that minimum, in whole °C. Zero or negative shortfall means at or above the minimum.  
  `0` = None: recorded temperature at or above the minimum; `1` = Moderate: below the minimum by more than 0°C and up to and including 5°C; `2` = Large: below the minimum by more than 5°C  
  gold: {"0": 0.0356, "1": 0.92, "2": 0.0444} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [read]** Rate how settled the Nov 2 gala menu is as at the last log entry (22/10). Where entries differ over time, the latest entry counts.  
  `0` = Open: menu, including vegan options, still unconfirmed; `1` = Partly settled: some items confirmed, others still open; `2` = Settled: whole menu confirmed by the client  
  gold: {"0": 0.92, "1": 0.07, "2": 0.01} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F4-0140  ·  F4 Missing, incomplete or uncertain evidence  ·  home insurance  ·  system record

```json
{
 "claimRef": "CLM-HC-26-048831",
 "policy_no": "HCP-7741093-B",
 "ClaimStatus": "open_triage",
 "lossDetails": {
  "loss_type": "escape_of_water",
  "incident_start": "2026-10-29T21:40:00Z",
  "incident_end": "2026-11-01T06:15:00Z",
  "reported_at": "2026-10-31T08:52:00Z",
  "reported_via": "phone_line_3",
  "water_ingress_source": "",
  "room_affected": [
   "utility",
   "hall",
   "understair cupboard"
  ]
 },
 "insured": {
  "fullName": "Margaret A. Oduya",
  "postcode": "LS14 2QP",
  "occupancy": "owner_occupied",
  "contact_tel": null
 },
 "cover": {
  "sum_insured": "185000",
  "contents_limit": "42000",
  "excess_gbp": "250",
  "buildings_cover_ref": null
 },
 "reserve": {
  "reserve_gbp": "4200.00",
  "reserve_set_by": "KPrice",
  "last_changed": "2026-10-30"
 },
 "observations": [
  {
   "obs_id": "OB-1",
   "date": "2026-09-14",
   "source": "moisture_survey_v2",
   "text": "Hall skirting moisture reading elevated, 18% WME (prior visit)."
  },
  {
   "obs_id": "OB-2",
   "date": "2026-10-30",
   "source": "site_visit_notes",
   "text": "Utility floor saturated; underlay lifted near washing machine inlet. Plumber estimate of the supply hose cause is provisional, not yet verified."
  },
  {
   "obs_id": "OB-3",
   "date": "2026-10-30",
   "source": "photo_set_B",
   "text": "Understair cupboard wall damp to 40 cm; staining present."
  }
 ],
 "contractor_log": {
  "coverage_from": "2026-10-31",
  "coverage_to": "2026-10-31",
  "visits": "1",
  "drying_equipment_days": 0
 },
 "flags": {
  "legacy_batch": "B-0417",
  "print_queue_id": 88213,
  "ivr_menu_path": "2-1-4"
 },
 "notes": "Insured reports water pooling from around 21:40 Thursday with the isolation valve found closed on Saturday morning. Contractor log covers Saturday only and no drying equipment has been logged yet. Water source field is blank pending the plumber's report, which has not been received."
}
```

**q1 [infer]** Design (a): how well does the document establish that a failed washing machine supply hose was the source of the water ingress, as at the document's latest entries? Rate the evidence for that conclusion only.  
  `0` = Not established: no verified source is recorded, or the only cause given is provisional or unconfirmed; `1` = Partly established: a cause is supported by a verified report but the exact source component is not confirmed; `2` = Established: a verified source report names the failing component and is consistent with the site evidence  
  gold: {"0": 0.92, "1": 0.0632, "2": 0.0168} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [judge]** Design (b): how far is the water damage spread across the property, judged from the observations recorded? Rate the extent of damage itself. Rooms evidenced only by older, unrelated readings do not count; unrecorded rooms count as unaffected.  
  `0` = Negligible: no room is shown as damaged by this loss; `1` = Single room: damage from this loss is evidenced in one room only; `2` = Two rooms: damage from this loss is evidenced in exactly two rooms; `3` = Three or more rooms: damage from this loss is evidenced in at least three rooms  
  gold: {"0": 0.015, "1": 0.0375, "2": 0.885, "3": 0.0625} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [infer]** Design (a): how well does the document establish the duration for which water escaped before the supply was isolated? Rate the support for a firm duration figure, using start, end and reporting times and notes.  
  `0` = Not established: no start time or no isolation time can be found; `1` = Start only: a start time is recorded but isolation time is not evidenced; `2` = Bounded: start and an approximate isolation point are recorded, but they conflict or are indirect; `3` = Confirmed: start and isolation are both recorded consistently by independent entries  
  gold: {"0": 0.0225, "1": 0.08, "2": 0.85, "3": 0.0475} · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [infer]** Design (b): rate how much drying work is evidenced as done, counting equipment days logged within the contractor log. Missing or unlogged equipment days count as zero days. Rate on the log as it stands.  
  `0` = No evidence: no contractor log exists at all; `1` = None logged: a log exists but records zero equipment days and no visits; `2` = Visit only: a visit is logged but zero equipment days; `3` = Short drying: one or two equipment days are logged; `4` = Extended drying: three or more equipment days are logged  
  gold: {"0": 0.0103, "1": 0.049, "2": 0.9201, "3": 0.0129, "4": 0.0077} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F4-0302  ·  F4 Missing, incomplete or uncertain evidence  ·  corporate expenses  ·  system record

```json
{
 "record_id": "EXP-DSK-0047213",
 "record_type": "expense_claim_review_bundle",
 "schema_ver": "3.2",
 "exportedAt": "2026-10-29T16:42:08Z",
 "Export_Batch": "XB-20261029-07",
 "policy_ref": "TRV-POL-04 (Travel and Subsistence)",
 "claimant": {
  "employee_id": "E-40718",
  "full_name": "Priya Lindqvist-Nair",
  "cost_centre": "CC 3310",
  "grade": "C4",
  "manager_id": "E-22041",
  "home_office": "Leeds"
 },
 "engagement": {
  "client_code": "HRZN-0812",
  "engagementName": "Northfield Pensions Review",
  "engagement_start": "2026-07-06",
  "engagement_end": "2026-09-18",
  "billable": true,
  "partner_ref": "P-1190"
 },
 "claim_summary": {
  "claimTotalGBP": "1864.37",
  "currency_orig": "EUR",
  "amt_orig": "2090.00",
  "fx_rate_applied": 0.8921,
  "submitted_on": "2026-08-03",
  "claim_period_from": "2026-07-06",
  "claim_period_to": "2026-08-31",
  "approved_amount_GBP": null,
  "approverComment": null
 },
 "line_items_count": 14,
 "receipts_attached": 11,
 "receipt_missing_flags": [
  "2026-07-19 taxi, Frankfurt",
  "2026-08-12 hotel incidental"
 ],
 "policy_check": {
  "nightly_cap_gbp": "180",
  "nights_claimed": 9,
  "avg_hotel_per_night_gbp": "196.40",
  "exception_requested": true,
  "exception_basis": "Client-site accommodation unavailable; market rate estimated roughly 15 percent above cap, to be confirmed",
  "verified_by_travel_desk": false
 },
 "audit_trail": [
  {
   "ts": "2026-08-04T09:11Z",
   "evt": "submitted",
   "by": "E-40718"
  },
  {
   "ts": "2026-08-11T14:02Z",
   "evt": "flagged_missing_receipt",
   "by": "SYS"
  },
  {
   "ts": "2026-08-19T10:37Z",
   "evt": "note_added",
   "by": "E-22041",
   "text": "Client confirmed hotel block rate was just under 200 per night for Oct; earlier figure from July portal screenshot, may be out of date."
  }
 ],
 "notes": "Claim covers only the first seven weeks of the engagement, as later expenses were submitted under a separate batch not yet linked to this record. Hotel rate evidence is provisional and not yet verified against the supplier invoice. Taxi receipt for 19 July remains outstanding and the claimant has been asked to resubmit.",
 "internal_tags": null,
 "legacy_ref": "TRV-2025-00619",
 "print_flag": "N"
}
```

**q1 [judge]** Design (a): rate how well the record's evidence establishes the conclusion that this claim does not cover the whole engagement. Level 0 means not enough evidence to establish it. Higher levels need progressively more confirmed evidence.  
  `0` = Not established: nothing in the record bears on whether the claim covers the whole engagement, so it cannot be confirmed; `1` = Hinted: only one indirect indication exists, which could have another explanation; `2` = Asserted: a direct statement of partial coverage exists but the record's own dates are not available to check it; `3` = Partly confirmed: either a direct statement or a date comparison supports partial coverage, but not both; `4` = Confirmed: a direct statement of partial coverage and the record's own dates both agree that the claim stops before the engagement ends  
  gold: {"0": 0.0, "1": 0.0, "2": 0.01, "3": 0.095, "4": 0.895} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [judge]** Design (a): rate how well the evidence establishes that the claimed hotel rate above the nightly cap is justified as a policy exception. Level 0 means not enough evidence. Higher levels need more current, independent, verified evidence.  
  `0` = Not established: no evidence of the market rate or availability problem is given, so the exception cannot be confirmed; `1` = Provisional only: the case rests on an unverified estimate or stale or conflicting rate figures, with no current independent confirmation; `2` = Independently indicated: a current rate is confirmed by a third party or manager, but not checked against a supplier invoice or by the travel desk; `3` = Verified: the rate is checked against the supplier invoice or by the travel desk and supports the exception  
  gold: {"0": 0.04, "1": 0.805, "2": 0.1425, "3": 0.0125} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [read]** Design (b): rate the share of the claim's line items that have a receipt attached, using the stated counts. Line items without an attached receipt, flagged or not, count as lacking a receipt. Round to one decimal place.  
  `0` = Low: below 70% of line items have a receipt attached; `1` = Moderate: at least 70% but below 90% of line items have a receipt attached; `2` = High: 90% or more of line items have a receipt attached  
  gold: {"0": 0.016, "1": 0.92, "2": 0.064} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [infer]** Design (b): rate the total GBP by which claimed hotel spend exceeds the nightly cap, as nights claimed times the stated average rate minus the cap. Use the stated unverified average; ignore estimates and later rate notes. Round to the nearest pound.  
  `0` = Small: excess is below £50; `1` = Moderate: excess is at least £50 but below £100; `2` = Large: excess is £100 or more  
  gold: {"0": 0.0229, "1": 0.0571, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F4-0063  ·  F4 Missing, incomplete or uncertain evidence  ·  theatre box office  ·  system record

```json
{
 "rec_id": "FOH-2026-0917",
 "RecordType": "front_of_house_incident",
 "schema_ver": "3.2",
 "venue": {
  "venue_code": "GLT-MAIN",
  "venue_name": "Greyhythe Lyric Theatre",
  "floor_ref": "Circle"
 },
 "production": {
  "title": "The Lantern Coast",
  "run_ref": "RUN-88413",
  "perf_date": "2026-10-24",
  "perf_time": "19:30",
  "perf_no": "41"
 },
 "incident": {
  "category": "crowd_flow",
  "location": "Circle bar, stair B",
  "alarm_raised": "20:14",
  "alarm_cleared": "20:37",
  "duration_mins": "23",
  "stewards_on_duty": "4",
  "reported_by": "usher_KD_07"
 },
 "affected": {
  "seat_block": "CB-A7 to CB-A14",
  "seats_held": 61,
  "tickets_sold": "612",
  "est_circle_occupancy_at_alarm": "140 (provisional, not yet verified against scan data)"
 },
 "refunds": {
  "requested": "9",
  "issued": null,
  "amount_gbp": "138.50",
  "approved_by": ""
 },
 "cctv": {
  "camera_ids": [
   "CH-04",
   "CH-05"
  ],
  "coverage_window": "19:30-20:05",
  "retained_to": null
 },
 "observations": [
  {
   "obs_id": 1,
   "ts": "2026-10-24T20:20",
   "src": "usher",
   "text": "Stair B gate found unlatched at interval."
  },
  {
   "obs_id": 2,
   "ts": "2026-10-24T20:31",
   "src": "steward",
   "text": "Smoke haze from bar machine, no fire indication."
  },
  {
   "obs_id": 3,
   "ts": "2026-09-30T18:10",
   "src": "maintenance",
   "text": "Stair B closer tension checked, adjusted.",
   "stale": true
  }
 ],
 "prior_refs": {
  "previous_alarm_test": "2026-10-17 19:05",
  "prior_incident_ref": "FOH-2026-0903",
  "bar_invoice_ref": "BI-44721"
 },
 "status": "open",
 "notes": "Alarm sounded during Act Two after the bar machine tripped the stair B detector. Refund claims are still being matched to order records, and the occupancy figure is an estimate only. CCTV retained for the window shown and nothing after 20:05 has been pulled."
}
```

**q1 [infer]** Design (a): rate how well the record establishes the alarm's duration. Compare the two alarm times with the stated duration. A missing field means the matching cannot be done and the duration is not established.  
  `0` = Not established: either alarm time or the stated duration is missing, so no check is possible; `1` = Conflicting: all three are present but the gap between the alarm times differs from the stated duration; `2` = Confirmed: both alarm times and the stated duration are present and the gap between the times equals the stated duration  
  gold: {"0": 0.0337, "1": 0.0463, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [infer]** Design (a): rate how well the record establishes that refunds have actually been paid out for this incident. A blank, null or missing field counts as no evidence for that element.  
  `0` = Not established: no issued count is recorded, so payment of any refund cannot be confirmed; `1` = Issued but unauthorised: an issued count is recorded, but no approver is recorded; `2` = Issued and authorised: an issued count and a named approver are both recorded  
  gold: {"0": 0.92, "1": 0.0518, "2": 0.0282} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** Design (a): rate how well the retained CCTV evidence establishes what happened at stair B during the alarm period. An unrecorded retention date means retention is unconfirmed. Footage not pulled counts as unavailable.  
  `0` = Not enough evidence: no retained footage is shown to cover any of the alarm period, or retention is unconfirmed; `1` = Partial: retained footage is shown to cover only part of the alarm period; `2` = Full: retained footage is shown to cover the whole alarm period, with retention confirmed  
  gold: {"0": 0.95, "1": 0.04, "2": 0.01} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [judge]** Design (a): rate how well the record establishes the number of people in the Circle when the alarm was raised. Provisional or unverified figures count as an estimate only, not as established.  
  `0` = Not enough evidence: only an unverified or provisional figure, or none, is available; `1` = Partly checked: the figure has been cross-checked against some, but not all, scan data; `2` = Verified: the figure has been fully verified against scan data for the alarm time  
  gold: {"0": 0.9575, "1": 0.0325, "2": 0.01} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F4-0153  ·  F4 Missing, incomplete or uncertain evidence  ·  translation agency  ·  system record

```json
{
 "record_type": "vendor_performance_export",
 "export_id": "VPE-2026-10-0412",
 "exported_at": "2026-10-30T08:14:52Z",
 "exported_by": "svc_vmgr_export",
 "schema_ver": "3.2",
 "vendor": {
  "vendor_id": "VND-04471",
  "legal_name": "Halvorsen Lindqvist Language Services Ltd",
  "display_name": "HL Languages",
  "country_code": "GB",
  "vat_no": null,
  "onboarded": "2023-02-14"
 },
 "assignment": {
  "assignmentRef": "ASG-26-08839",
  "project_code": "PRJ-PHARM-RX-77",
  "source_lang": "de-DE",
  "target_lang": "en-GB",
  "word_count": "4120",
  "rate_gbp_per_word": "0.118",
  "po_number": "PO-557203",
  "po_amt_gbp": "486.16",
  "invoice_ref": "INV-HL-20261007",
  "due_dt": "2026-10-21"
 },
 "delivery": {
  "due_date": "2026-10-21",
  "delivered_at": "2026-10-23T16:42:00Z",
  "days_late": "2",
  "revision_rounds": 1,
  "qa_score": null,
  "qa_checker": "R. Osei-Tennant"
 },
 "reviews": [
  {
   "rev_id": 1,
   "dt": "2026-10-24",
   "rating_1_5": 4,
   "comment": "Terminology consistent with glossary v9. Two tense errors in section 3.",
   "reviewer": "K. Mbatha"
  },
  {
   "rev_id": 2,
   "dt": "2026-10-27",
   "rating_1_5": "3",
   "comment": "Client flagged dosage units in table 2 as provisional, not yet verified against source.",
   "reviewer": "J. Pallesen"
  }
 ],
 "period_coverage": {
  "start": "2026-09-01",
  "end": "2026-09-30",
  "note_records_present": "Q3 monthly tallies only; October not loaded"
 },
 "legacy_ref": {
  "old_asg": "ASG-25-06114",
  "old_rate": "0.104",
  "migrated": true
 },
 "misc": {
  "ui_theme": "light",
  "row_colour": "#E8F1FA",
  "print_flag": "N",
  "tz_offset": "+00:00"
 },
 "notes": "Revision round 1 covered table formatting and two glossary terms only. The dosage unit observation is provisional and has not yet been checked by the linguist of record. Delivery timestamp taken from the portal upload log, which may lag the client receipt time by up to one working day."
}
```

**q1 [judge]** Design (a): how well the export establishes that the translation's quality is acceptable for the client, judged on this one assignment at 30 October 2026. Missing or provisional evidence cannot support a higher level than its condition allows.  
  `0` = Nothing: no review, QA score or other quality evidence is recorded, so acceptability cannot be established; `1` = Minimal: only a single reviewer rating or comment exists, with no QA score and no second source; `2` = Partial: at least two reviewer ratings exist, but the formal QA score is absent or an accuracy concern remains unverified, so acceptability is not confirmed; `3` = Substantial: a formal QA score is recorded and reviews exist, but a minor concern remains open or the score is below a clear pass; `4` = Established: a formal QA score is recorded, reviews agree, and every flagged concern is verified and closed  
  gold: {"0": 0.015, "1": 0.05, "2": 0.865, "3": 0.06, "4": 0.01} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [judge]** Design (a): how firmly the export establishes the conclusion that assignment ASG-26-08839 was delivered after its due date, taking the stated timestamp caveat into account. Missing dates count as absent evidence.  
  `0` = Not established: the due date or the delivery timestamp is missing, so lateness cannot be shown; `1` = Weak: both dates are present but the records conflict with each other about whether delivery was late; `2` = Tentative: both dates are present and agree on lateness, but the stated timestamp uncertainty could by itself reverse the conclusion; `3` = Likely: both dates agree on lateness and the uncertainty only leaves a small chance of reversal, with no supporting count; `4` = Firm: due date, delivery timestamp and a recorded days-late count all agree, and lateness remains even after allowing for the full stated timestamp uncertainty  
  gold: {"0": 0.0125, "1": 0.02, "2": 0.09, "3": 0.145, "4": 0.7325} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [infer]** Design (a): how far the dosage-unit observation in table 2 has been verified, judged from the review comments and notes as of 30 October 2026. Absence of a recorded check counts as not verified.  
  `0` = Unverified: the observation is provisional and no check by the linguist of record or against the source is recorded; `1` = Partly checked: the linguist of record has looked at it, but no comparison against the source is recorded; `2` = Verified: the observation has been checked against the source and the outcome is recorded  
  gold: {"0": 0.92, "1": 0.0533, "2": 0.0267} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** Design (b): how large a body of reviewer ratings (1-5) backs this assignment's quality assessment. Count only ratings with a recorded value in the export. If fewer than three exist, rate level 0 whatever their values.  
  `0` = Insufficient: fewer than three reviewer ratings recorded; `1` = Limited: at least three but fewer than five reviewer ratings recorded; `2` = Adequate: five or more reviewer ratings recorded  
  gold: {"0": 0.92, "1": 0.0533, "2": 0.0267} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F4-0197  ·  F4 Missing, incomplete or uncertain evidence  ·  solar installation  ·  handwritten log transcription

```
Brightline Solar Ltd — Survey & Commissioning Team
Field log (handwritten, transcribed) — Engineer: R. Okonjo-Pryce
Site ref: BSL-SC-4417 | Address: 14 Alder Close, Wenbury WN7 2QH | Install crew: Team C (Varga / Dunmore)

Mon 26/10
07:40 Van 3 collected from Unit 2 yard. Fuel gauge ~1/4. Kit checked: IV curve tester, clamp meter (cal sticker due 03/27), Megger MIT.
09:15 On site. Roof survey complete, south-facing pitch approx. 34°. Roof covering = conc tile, 2 tiles cracked at SW corner, photographed (IMG_0412–0415).
11:30 Array fitted by Team C. 14 panels x 410 W = 5.74 kW DC. Inverter: 5 kW hybrid, s/n [illegible] on rating plate, photographed.
13:10 Earth bond measured at main panel: 0.09 Ω. OK.

Tue 27/10
08:55 Back on site. Strings 1 & 2 measured Voc: 412 V / 411 V. String 3 not yet connected (see note).
10:20 Insulation resistance string 1 = >200 MΩ @ 500 V. String 2 = 186 MΩ. Within limits.
14:05 Customer reports neighbour's tree shading roof after 15:00 — est. ~1 hr lost per day in Dec, unverified, need site check.
16:30 Commissioning sheet part-filled. Torque check on DC isolator: [struck through: 4.0 Nm] 2.4 Nm (corrected). Witness signature: MISSING.

Wed 28/10
Office day. Emailed Dunmore re string 3 cable route. Sheet not yet scanned.
Ref to previous survey 14/08 (Halvard, desktop only): ridge height noted as 6.2 m — pre-dates scaffold, probably out of date.

Thu 29/10
Left site 12:00. Provisional RoCoF / G99 export limit set at 3.68 kW, pending DNO reply — not yet verified.

```

**q1 [read]** Design (a): rate how well the log's evidence establishes that the commissioning sheet for this job is independently witnessed and filed, as at Thursday 29/10. Missing or unrecorded evidence counts as not established.  
  `0` = Not established: no witness signature is recorded on the commissioning sheet, or its status cannot be confirmed; `1` = Partly established: a witness signature is recorded, but the sheet is not confirmed as scanned or filed; `2` = Established: a witness signature is recorded and the sheet is confirmed as scanned or filed  
  gold: {"0": 0.92, "1": 0.0571, "2": 0.0229} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [compare]** Design (b): count how many of these four items remain unconfirmed in the log at 29/10: legible inverter serial number, witness signature, string 3 connected and tested, export limit verified. Missing or unrecorded counts as unconfirmed.  
  `0` = Zero: none of the four items is unconfirmed; `1` = One: exactly one item is unconfirmed; `2` = Two: exactly two items are unconfirmed; `3` = Three: exactly three items are unconfirmed; `4` = Four: all four items are unconfirmed  
  gold: {"0": 0.0044, "1": 0.0073, "2": 0.016, "3": 0.0524, "4": 0.9199} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** Design (a): rate how well the log's evidence establishes that the DC side of the array is electrically sound (insulation resistance), across all three strings. Untested strings count as not established.  
  `0` = Not established: no string has a recorded insulation resistance result within limits; `1` = One string: exactly one string has a recorded result within limits; `2` = Two strings: exactly two of the three strings have recorded results within limits, the rest untested; `3` = All three: every string has a recorded result within limits  
  gold: {"0": 0.0175, "1": 0.0325, "2": 0.9225, "3": 0.0275} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [infer]** Design (a): rate how well the log establishes the size of the yield loss from the neighbour's tree shading. Work from what has been recorded as checked, not merely reported. Absent checks count as not established.  
  `0` = Not established: the only evidence is the customer's unverified estimate, with no site check recorded; `1` = Partly established: a site check is recorded but the loss is not quantified over the relevant period; `2` = Established: a site check is recorded and the loss is quantified from measurement or modelling  
  gold: {"0": 0.92, "1": 0.0667, "2": 0.0133} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F4-0209  ·  F4 Missing, incomplete or uncertain evidence  ·  gym membership  ·  system record

```json
{
 "rec_id": "MBR-LDN-0048812",
 "exportTs": "2026-10-30T06:14:52Z",
 "export_src": "memadmin-prod-replica-2",
 "chain_code": "HRX",
 "homeSite": {
  "site_no": "07",
  "site_name": "Canal Wharf Fitness",
  "tz": "Europe/London",
  "region_cd": "SE-4"
 },
 "member": {
  "full_name": "Priya Dalgleish",
  "dob": "1988-02-19",
  "email_addr": "p.dalgleish88@example-mail.co.uk",
  "phone": null,
  "emergency_contact": "",
  "id_verified": true,
  "id_verified_on": "2026-08-03"
 },
 "membership": {
  "plan_cd": "ANYTIME-PLUS",
  "joinDate": "2026-08-01",
  "status": "ACTIVE",
  "freeze_days_used": "0",
  "contract_term_m": "12",
  "auto_renew": "Y",
  "cancel_req_dt": null
 },
 "billing": {
  "monthly_fee_gbp": "34.99",
  "last_charge": "2026-09-30T23:58:11Z",
  "next_charge": "2026-10-31",
  "arrears_gbp": "0.00",
  "pmt_method": "DD",
  "bank_ref": "DD-774210-B"
 },
 "usage_log": [
  {
   "evt": "CHECKIN",
   "site": "07",
   "ts": "2026-09-30T21:47:03Z",
   "door": "T2"
  },
  {
   "evt": "CHECKIN",
   "site": "07",
   "ts": "2026-10-01T00:09:40Z",
   "door": "T2"
  },
  {
   "evt": "CHECKIN",
   "site": "07",
   "ts": "2026-10-03T07:22:18Z",
   "door": "T1"
  },
  {
   "evt": "CHECKOUT_FAIL",
   "site": "07",
   "ts": "2026-10-04T18:55:02Z",
   "door": "T1"
  }
 ],
 "coverage": {
  "window_from": "2026-08-01",
  "window_to": "2026-09-27",
  "requested_from": "2026-08-01",
  "requested_to": "2026-10-29",
  "complete_flag": 0
 },
 "obs": [
  {
   "obs_id": 1,
   "author": "ops.desk",
   "dt": "2026-03-14",
   "txt": "Member reported locker key issue at prior site; resolved."
  },
  {
   "obs_id": 2,
   "author": "j.okafor",
   "dt": "2026-09-22",
   "txt": "Attended induction, self-reported two sessions per week."
  },
  {
   "obs_id": 3,
   "author": "ops.desk",
   "dt": "2026-10-05",
   "txt": "Usage pattern suggests weekend attendance; tenure estimated at 7 weeks (provisional, not yet verified)."
  }
 ],
 "flags": {
  "dup_chk": false,
  "fraud_score": "0.12",
  "legacy_seg": "B2",
  "xref_hrx_id": null
 },
 "notes": "Member joined via online channel with ID verified at induction. Check-in history after 2026-09-27 has not been loaded into the window, so usage totals are incomplete. Emergency contact field is blank and has not been chased."
}
```

**q1 [judge]** Design (a): rate how well the record establishes the conclusion that the member's identity has been verified, as at the export. Higher levels need progressively more complete, confirmed evidence; absent evidence means level 0.  
  `0` = Not established: no verification flag, date or note is present; `1` = Claimed only: the member's own statement or an unsupported remark is the sole evidence; `2` = Flag only: a verified flag is set, with no date and no narrative note; `3` = Flag and date: a verified flag and a verification date are recorded, with no separate narrative corroboration; `4` = Fully evidenced: a verified flag, a verification date and a separate narrative note all confirm it  
  gold: {"0": 0.0125, "1": 0.02, "2": 0.0375, "3": 0.23, "4": 0.7} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [judge]** Design (a): rate how well the record establishes the member's total number of gym visits from joining to the export date. Level 0 means a total cannot be established. Higher levels need more complete, reconciled and confirmed evidence.  
  `0` = Cannot be established: loaded usage history is marked incomplete for the period from joining to export, so no reliable total exists; `1` = Complete but unchecked: usage history covers the whole period, but entries are not reconciled with any other source; `2` = Reconciled: usage history covers the whole period and is reconciled with one independent source; `3` = Confirmed: usage history covers the whole period, is reconciled and is also confirmed by the member  
  gold: {"0": 0.95, "1": 0.0325, "2": 0.01, "3": 0.0075} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** Design (a): rate how well the record establishes the member's length of tenure as at the export date. Higher levels need progressively more consistent, independently confirmed evidence; level 0 means no usable evidence.  
  `0` = Not established: no join date and no tenure estimate are recorded; `1` = Recorded but uncorroborated: a join date exists, but no independent record confirms it, or a provisional estimate sits alongside it unresolved; `2` = Corroborated: a join date is recorded and one independent record agrees, with no contradicting estimate; `3` = Confirmed: a join date is corroborated by independent records and by billing history, with no contradiction  
  gold: {"0": 0.0275, "1": 0.8925, "2": 0.0625, "3": 0.0175} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [infer]** Design (b): count the CHECKIN events in the usage log whose timestamps fall inside the loaded coverage window, from its start date to the end of its end date. Events outside the window and failed checkouts are not counted.  
  `0` = None: no check-ins fall inside the loaded window; `1` = Few: at least 1 but fewer than 3 check-ins fall inside the window; `2` = Several: 3 or more check-ins fall inside the window  
  gold: {"0": 0.92, "1": 0.0571, "2": 0.0229} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F4-0253  ·  F4 Missing, incomplete or uncertain evidence  ·  hospital beds  ·  meeting notes

```
BEDS & DISCHARGE COORDINATION – MEETING NOTES

Meeting: Weekly bed flow huddle (Ward 6B / Ward 7A / Discharge Lounge)
Date: Thursday 29 October 2026
Time: 08:15–08:40
Location: Bed Bureau, Level 2, Room 2.14 (Teams link for South Site)
Chair: Gemma Okonkwo-Reid (Deputy Matron, Bed Management)
Minutes: Tariq Lindqvist

Attendees: Gemma Okonkwo-Reid; Ward 6B – Sister Bronwen Ashdown; Ward 7A – Sister Priya Mistry; Discharge Coordinator – Joanne Peverell; Bed Bureau – Callum Dwyer; Site Operations – Aisha Fenwick (Teams)

Apologies: Ward 7A Band 6 (Dev Kaur) – on leave

NOTES

1. Occupancy. Bed Bureau reported 94% occupancy at 07:00 across both wards (Ward 6B 27/28; Ward 7A 29/30). Callum noted two outliers, a boarded patient in 7A bay 4 awaiting transfer since 22 Oct and an outlier from ED in 6B side room 3.

2. Discharges before noon. Joanne reported 9 of 14 planned discharges completed by 10:00 yesterday. Sister Ashdown disputed the figure, stating 6B alone had 7 of 9 completed by 10:00 and Joanne's count should be re-checked against the EDD log. Agreed Joanne to reconcile the two counts against the e-Discharge log.

3. Date of transfer for Bed 7A-04. Sister Mistry believes the transfer to the community step-down unit is booked for Monday 2 November. Callum's system shows 3 November. Not resolved; Callum to confirm against the transfer request reference.

4. Discharge Lounge. Lounge capacity was 12 seats; currently running at 10 occupied chairs. Aisha reported the lounge kettle is out of service pending facilities. Estimated return to service Tuesday, not yet confirmed.

5. Estimated discharge dates. Several EDDs entered on the whiteboard for 6B bays 2 and 3 are dated before the consultant ward round on 27 October. Sister Ashdown to update. Joanne to check whether these were carried over from the 20 October template.

6. Escalation trigger. Gemma reminded all present that red-status escalation to the On-Call Site Manager applies at 85% occupancy or above for two consecutive hours. Current 6B and 7A readings were below this threshold on Wednesday.

7. Weekend staffing. Sister Mistry reported one vacancy across Saturday and Sunday day shifts on 7A. Bank request raised 28 October, reference BR-2026-40917. Response pending. Ward 6B reports no gaps.

8. Transport. Patient transport contract notes that Tuesday morning slots are fully booked. Afternoon slots available from 13:00.

ACTIONS

- Joanne Peverell: reconcile yesterday's discharge counts with 6B and 7A and circulate by Friday 31 October.
- Callum Dwyer: confirm transfer date for Bed 7A-04 against request reference (number not recorded at meeting).
- Sister Ashdown: update EDDs on 6B bays 2 and 3.
- Aisha Fenwick: chase facilities for Discharge Lounge kettle.
- Gemma Okonkwo-Reid: follow up BR-2026-40917 with Bank Staffing.
- All: next huddle Thursday 5 November, 08:15.

Minutes circulated: 29 October 2026, 11:52

```

**q1 [infer]** Design (a): rate how well the notes establish that the red-status escalation trigger (85% occupancy or above for two consecutive hours) was NOT met on Wednesday on Wards 6B and 7A. Missing evidence limits the level.  
  `0` = Not enough evidence: no statement or reading about Wednesday occupancy against the trigger for either ward; `1` = Partly established: Wednesday is addressed for only one ward, or only today's readings are given in place of Wednesday's; `2` = Established: a statement in the notes says that both wards' Wednesday readings were below the trigger, even though no figures or hours are listed  
  gold: {"0": 0.045, "1": 0.1675, "2": 0.7875} · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [infer]** Design (a): rate how well the notes establish the true number of planned discharges completed by 10:00 yesterday across the wards. Missing, disputed or unreconciled counts limit the level.  
  `0` = Not enough evidence: no count of completed discharges is given; `1` = Single source: one count is given and nothing else supports or contradicts it; `2` = Disputed: a count is given and a second source gives a partial figure and challenges it, with reconciliation still outstanding; `3` = Reconciled: the counts have been checked against the discharge log and agreed  
  gold: {"0": 0.0128, "1": 0.04, "2": 0.92, "3": 0.0272} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [compare]** Design (a): rate how well the notes establish the number of free Discharge Lounge seats at the time of the meeting, by setting occupied chairs against capacity. Missing figures limit the level.  
  `0` = Not enough evidence: neither seat capacity nor occupied chairs is stated; `1` = Partial: only one of capacity or occupied chairs is stated, so free seats cannot be worked out; `2` = Established: both capacity and current occupied chairs are stated, so free seats can be calculated  
  gold: {"0": 0.015, "1": 0.0725, "2": 0.9125} · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [judge]** Design (a): rate how well the notes establish that Ward 7A's Saturday and Sunday day shifts will be fully staffed this weekend. Pending or unconfirmed cover counts as not established.  
  `0` = Not enough evidence: a vacancy is reported and no cover is confirmed, so full staffing cannot be established; `1` = Partly established: cover is confirmed for some but not all of the vacant weekend shifts; `2` = Established: cover is confirmed for every vacant weekend day shift, or no vacancy exists  
  gold: {"0": 0.925, "1": 0.0575, "2": 0.0175} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F4-0036  ·  F4 Missing, incomplete or uncertain evidence  ·  IT service desk  ·  meeting notes

```
IT Service Desk — Meeting Notes
Ref: SD-MTG-2026-1027
Date: 27 October 2026
Time: 14:00–14:25
Location: Huddle room 3B / Teams
Attendees: Priya Okonkwo (Incident Manager), Tom Brightwell (Network Ops), Yusuf Demir (Service Desk Lead), Hannah Lowe (Vendor Liaison)
Apologies: Ravi Chandran (Finance Systems)
Minutes taken by: Y. Demir

Subject: P2 incident INC-48817 — VPN authentication failures, 22–27 October

1. Scope of the incident. Tom reported that failed VPN logins began around 06:40 on 22 October and affected remote users on the Leeds and Bristol concentrators. The auth log export covers 23 October 00:00 to 26 October 23:59 only; the 22 October and 27 October exports have not been pulled yet.

2. Affected users. Priya quoted the service desk tally as just under 340 tickets referencing VPN access. Hannah said the vendor portal shows about 410 failed sessions per day at peak. Priya and Hannah disagree on whether the ticket figure includes duplicates; Hannah believes it does, Priya does not. Not resolved.

3. Cause. Tom said the RADIUS shared-secret rotation on 21 October is the likely trigger. This is provisional and has not been verified against the concentrator config.

4. Workaround. Yusuf confirmed the fallback to local accounts was enabled for 14 users on 24 October (ticket SD-99213, closed). The 25 October note in the wiki still lists 9 users; the wiki is out of date.

5. Vendor. Hannah has logged case VX-220417. Vendor response target is 4 business hours; no reply recorded yet.

Actions
A1. Tom Brightwell — pull auth logs for 22 and 27 October and confirm the RADIUS secret change time. Due 29 Oct.
A2. Yusuf Demir — reconcile ticket count against duplicates and reply to Priya. Due 29 Oct.
A3. Hannah Lowe — chase VX-220417; report vendor's position on rotation. Due 28 Oct.
A4. Priya Okonkwo — update wiki fallback list. Due: [blank]

Next review: 30 October, 10:00.
```

**q1 [infer]** Design (a): rate how well the notes' evidence establishes that the 21 October RADIUS shared-secret rotation caused the VPN authentication failures. Rate as of the meeting. Missing verification or logs means the higher levels cannot be reached.  
  `0` = Nothing: no cause is put forward, or no source for one is given; `1` = Asserted only: a named person proposes the rotation as the likely cause, but it is unverified against configuration and no log evidence is cited for its timing; `2` = Config checked: the rotation is verified against the concentrator configuration, but log evidence of the start of failures is incomplete or not matched to it; `3` = Fully established: configuration verification and complete log evidence covering the start of failures both support the rotation as the cause  
  gold: {"0": 0.0267, "1": 0.92, "2": 0.0436, "3": 0.0097} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [judge]** Design (a): judging from the notes, rate how well the evidence establishes that the incident has affected many remote users, not just a handful. Exact numbers need not be settled. Rate on sources stated in the notes only.  
  `0` = Not enough evidence: no usable figure or source indicates the scale of user impact; `1` = Weakly supported: only one source indicates large impact, or the sources given cannot be relied on at all; `2` = Established as large: at least two independent sources each indicate large numbers, even though the exact count is disputed  
  gold: {"0": 0.04, "1": 0.1925, "2": 0.7675} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [read]** Design (a): rate how well the notes establish how many users were on the local-account fallback workaround on 24 October. Where sources conflict, an older source known to be out of date does not count against confirmation.  
  `0` = Not enough evidence: no record of the number of fallback users is given; `1` = Unreliable record only: the only figure comes from a source stated to be out of date or unverified; `2` = Single unconfirmed statement: a current figure is given but without a named confirmer or ticket reference; `3` = Confirmed: a named attendee confirms the figure, a ticket reference is cited, and any conflicting older figure is stated to be out of date  
  gold: {"0": 0.0126, "1": 0.0182, "2": 0.0491, "3": 0.9201} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** Design (b): count the numbered discussion items (1 to 5) in the notes that record an unresolved evidence gap (missing, disputed, provisional, out of date or no reply). An item with no stated gap does not count. Rate the count.  
  `0` = None: fewer than 1 item records an unresolved gap; `1` = Few: at least 1 but fewer than 3 items record a gap; `2` = Several: at least 3 but fewer than 5 items record a gap; `3` = All: all 5 items record a gap  
  gold: {"0": 0.0125, "1": 0.0325, "2": 0.145, "3": 0.81} · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F4-0294  ·  F4 Missing, incomplete or uncertain evidence  ·  public library  ·  system record

```json
{
 "export_id": "LSX-EXP-2026-10-30-004417",
 "exportedAt": "2026-10-30T07:52:14Z",
 "schema_ver": "3.2",
 "record_type": "loan_item_charge",
 "Item": {
  "barcode": "31745008826153",
  "title": "The Clockmaker's Daughter (hardback, large print)",
  "isbn13": "9781908000126",
  "owning_branch": "NWH",
  "shelf_loc": "LP FIC / HAR",
  "item_status": "on_loan",
  "replacement_cost_gbp": "",
  "cost_src": null
 },
 "loan": {
  "loanId": "LN-88213907",
  "issued_on": "2026-08-14",
  "due_date": "2026-09-04",
  "renewals": "2",
  "returned_at": null,
  "return_branch": null,
  "checkin_scan_ref": "CK-0928-NW-114"
 },
 "patron": {
  "member_no": "M0047215",
  "borrower_type": "adult",
  "home_branch": "NWH",
  "acct_status": "active",
  "fines_balance_gbp": "3.40",
  "notify_sms": false
 },
 "reservations": [
  {
   "resv_id": "RS-5510932",
   "queue_pos": "3",
   "placed": "2026-09-10",
   "state": "held_for_other_patron"
  }
 ],
 "charges": {
  "charge_code": "OVERDUE_LF",
  "daily_rate_gbp": "0.20",
  "days_overdue_est": "roughly 40",
  "amount_gbp": null,
  "cap_gbp": "10.00",
  "rate_status": "provisional, pending tariff check against 2026 schedule"
 },
 "condition_obs": [
  {
   "obs_id": "CO-0",
   "date": "2026-06-30",
   "by": "staff_CT_02",
   "text": "No damage noted at issue.",
   "src": "issue_scan"
  },
  {
   "obs_id": "CO-1",
   "date": "2026-09-28",
   "by": "staff_NW_07",
   "text": "Spine creased, otherwise intact.",
   "src": "checkin_scan"
  },
  {
   "obs_id": "CO-2",
   "date": "2026-10-22",
   "by": "staff_CT_02",
   "text": "Water staining pp.112-119, cause unknown, not yet verified as pre-existing.",
   "src": "photo_upload"
  }
 ],
 "activity_log_window": {
  "from": "2026-09-01",
  "to": "2026-10-30",
  "entries": "41"
 },
 "supplier_quote": {
  "quote_ref": "SQ-HB-44107",
  "unit_price_gbp": "just under 24.00",
  "quoted_on": "2026-10-12",
  "valid_to": "2026-11-11"
 },
 "notes": "Patron reports the book was left in a bag near a radiator; not confirmed. Renewal on 2026-09-02 was processed at NWH while the item was already flagged for reservation. Staff estimate of days overdue is approximate and based on the 2026-09-28 check-in timestamp, which may lag the actual return.",
 "ui_colour_theme": "green",
 "legacy_sort_key": "zz-0047",
 "print_queue_id": null,
 "last_modified_by": "svc_batch_nightly"
}
```

**q1 [read]** Design (a): rate how well the charge record establishes the final overdue amount in pounds owed on this loan, as at the export date. A blank or null field counts as not recorded.  
  `0` = Not established: no overdue amount is recorded in the charge record; `1` = Provisional: an amount is recorded but the rate is still marked provisional or unchecked; `2` = Rate confirmed: an amount is recorded at a confirmed rate, but the days overdue are only estimated; `3` = Fully established: an amount is recorded at a confirmed rate and days overdue are fixed by a confirmed return record  
  gold: {"0": 0.92, "1": 0.0622, "2": 0.0089, "3": 0.0089} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [compare]** Design (a): rate how well the condition records establish that the water staining arose during this loan, as at the export date. Compare observation dates with the issue date. Missing verification counts as not verified.  
  `0` = Not established: no condition record shows water damage; `1` = Recorded only: water damage is recorded after the loan began, but it is not verified as arising during the loan and its cause is unconfirmed; `2` = Timing verified: water damage is recorded and verified as not pre-existing, but its cause is unconfirmed; `3` = Fully established: water damage is recorded, verified as not pre-existing, and its cause is confirmed  
  gold: {"0": 0.0349, "1": 0.9199, "2": 0.0308, "3": 0.0144} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** Design (a): judge how well the evidence supports using the supplier quote as the replacement cost to bill the patron, as at the export date. Absent or expired evidence counts as not enough.  
  `0` = Not enough: no usable supplier quote exists, or it has expired; `1` = Partly usable: a current quote exists, but its price is imprecise or not yet entered as the item's recorded replacement cost; `2` = Usable: a current quote gives an exact price and is entered as the item's recorded replacement cost with its source  
  gold: {"0": 0.06, "1": 0.8875, "2": 0.0525} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [read]** Design (b): count condition observations in the record dated on or after the loan issue date, up to the export date. Observations dated before issue, or lacking a date, count as zero. Rate the count.  
  `0` = Zero: no qualifying observations; `1` = One: exactly one qualifying observation; `2` = Two: exactly two qualifying observations; `3` = Three: exactly three qualifying observations; `4` = Four or more: at least four qualifying observations  
  gold: {"0": 0.0156, "1": 0.0267, "2": 0.9199, "3": 0.0267, "4": 0.0111} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F4-0070  ·  F4 Missing, incomplete or uncertain evidence  ·  call centre QA  ·  meeting notes

```
MEETING NOTES: Call Quality Review – Complaint Rates and Call Record Sampling

Ref: CQ-MN-2026-41
Date: Thursday 29 October 2026
Time: 14:00–14:40
Location: Meeting room 3B, Eastgate contact centre / Teams bridge (dial-in 0330 555 0172, PIN 4417 88)
Attendees: Nadia Okonkwo (Quality Lead, chair); Tomasz Brennan (Complaints Escalation); Priya Ramaswamy (WFM Analyst); Dylan Foss (Team Leader, Billing Queue B); Imogen Hart (minutes)
Apologies: Kwame Asante (Telephony Platform)

1. Nadia confirmed the scope: call records for Billing Queue B and Retentions, 1 September to 25 October 2026. Complaint rate to be reported per 1,000 handled calls.

2. Tomasz reported 37 complaints logged against Billing Queue B in September. Dylan disagreed, citing 41 from the complaints log export dated 2 October. Tomasz to reconcile against the CRM extract before the next meeting. Not resolved.

3. Call recording extract for Retentions covers 1 September to 12 October only. Priya confirmed the remaining fortnight has not been pulled because the storage job failed on 14 October. Retentions figures for the later period are therefore not available.

4. Field "agent_id" is blank on 212 of 1,806 sampled records in the Billing Queue B extract. Priya noted the blanks cluster on calls routed through the IVR fallback. Cause not yet confirmed.

5. Complaint rate for Billing Queue B in September estimated at 21.4 per 1,000 calls (provisional, based on the 37 figure; will change if the count is revised).

6. Dylan noted that the 3 September re-tiering of the queue may have affected handle times. Not verified. Nadia asked for the pre-change baseline from the August WFM report (dated 4 September) to be used instead of the July report.

7. Retentions complaint volumes for October not yet compiled. Imogen to request from the complaints team.

Actions
- Tomasz Brennan: reconcile September complaint count (37 vs 41) against CRM extract by 4 November.
- Priya Ramaswamy: re-run Retentions recording pull for 13–31 October; investigate blank agent_id cause.
- Dylan Foss: send IVR fallback routing log for 1–30 September.
- Nadia Okonkwo: confirm which WFM baseline report to use.
- Imogen Hart: circulate these notes and request October Retentions complaint volumes.

Next meeting: Thursday 5 November 2026, 14:00.
```

**q1 [read]** Design (a): rate how well the document's evidence establishes Retentions call-record coverage for the full scope period (1 September to 25 October 2026), as at the meeting date.  
  `0` = None: the extract covers only part of the scope period and the rest is unavailable, so full coverage cannot be established; `1` = Partial confirmed: the document confirms the extract covers the whole period but not its completeness; `2` = Full: the document confirms the extract covers the whole scope period with a completeness check  
  gold: {"0": 0.92, "1": 0.0626, "2": 0.0174} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [read]** Design (a): rate how well the document establishes the true September 2026 complaint count for Billing Queue B, as at the meeting.  
  `0` = None: no count for September is stated at all; `1` = Conflicting: two or more different counts are stated by different sources and none is confirmed; `2` = Single unconfirmed: one count is stated with no competing figure but not reconciled; `3` = Reconciled: one count is stated and reconciled to a second source; `4` = Audited: the count is reconciled and independently signed off  
  gold: {"0": 0.0208, "1": 0.92, "2": 0.0386, "3": 0.0103, "4": 0.0103} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [read]** Design (a): rate how well the document establishes the cause of blank agent_id values in the Billing Queue B sampled extract, as at the meeting.  
  `0` = Unknown: the blanks are not described at all; `1` = Pattern only: the blanks are observed with a pattern but the cause is unconfirmed; `2` = Cause identified: a cause is stated as supported by logs or testing but not yet fixed; `3` = Resolved: the cause is confirmed and the blanks are corrected  
  gold: {"0": 0.0296, "1": 0.92, "2": 0.0385, "3": 0.0119} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [infer]** Design (a): rate how well the evidence establishes the September 2026 Billing Queue B complaint rate (per 1,000 handled calls) as a final figure, given the stated count status.  
  `0` = Not established: the figure is provisional and depends on a disputed input; `1` = Weakly established: the figure rests on a single undisputed but unreconciled count; `2` = Moderately established: the count is reconciled but the call denominator is unverified; `3` = Well established: count and denominator are both verified but not yet reviewed; `4` = Fully established: count and denominator are verified and reviewed  
  gold: {"0": 0.92, "1": 0.0593, "2": 0.0103, "3": 0.0053, "4": 0.0051} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F5-0001  ·  F5 Numerical and quantitative reasoning  ·  clinical trial site  ·  voicemail and CRM note

```
VOICEMAIL TRANSCRIPT
Line: Study Coordinator Office, Harbourside Clinical Research Unit (Site 0417)
Received: Thursday 29 October 2026, 16:52
Caller: Mrs D. Okonedo (Participant ID HRU-0417-022), callback 07700 900 318
Duration: 1 min 14 sec

"Hi, um, it's Doreen Okonedo, I'm calling about my... the blood test thing for the study. So I was meant to come in on the, er, the twenty-third? No, the twenty-fourth, sorry. And I didn't because my daughter's car broke down and I was at the garage in Whitlow for, I dunno, about four hours. I rang the number on the card but it just rang out. Anyway. I can come Monday, or Tuesday? Monday's better, I've got the grandson till about, oh, half eleven on Tuesday. I did fast, I've had nothing since last night, well, a cup of tea, and a bit of toast, it was about seven this morning. Is that all right? Sorry, I don't really know how this works. Can someone ring me back on the mobile, not the landline, the landline's my husband's. Thanks. Bye."

---

CRM NOTE
Contact: Okonedo, D. | Participant HRU-0417-022 | Visit: V4 (PK + fasting lipid panel)
Author: L. Pryce, Study Coordinator
Date: 29/10/2026 17:20

Participant left voicemail re missed V4 (scheduled 24/10/2026, window 22/10–26/10/2026 per protocol section 6.2). Reports attended late/no attendance due to family transport issue; states attended garage approx 4 hrs. Requests Mon 02/11 or Tue 03/11 AM. Reports fasting since approx 22:00 on 28/10 with tea and toast at approx 07:00 on 29/10 — NOT compliant with 10-hour fast (ref SOP CL-07 rev 4, para 3.4). Advised PI review before rebooking. Sample at V4 not to be taken until PI decision. Participant prefers mobile contact, not landline (spouse). Mobile on file to be updated to 07700 900 318 after confirming identity.

Actioned: rebook request logged in CTMS as pending. Called back 17:34, no answer, left message.
```

**q1 [compare]** Taking the participant's earlier requested rebooking date, how many calendar days after the last day of the protocol V4 window would the visit fall? Count whole calendar days; the window's final day is included in the window.  
  `0` = Within window: 0 days or fewer after the window ends; `1` = Up to one week: more than 0 but at most 7 days after; `2` = Up to two weeks: more than 7 but at most 14 days after; `3` = Over two weeks: more than 14 days after  
  gold: {"0": 0.0176, "1": 0.9199, "2": 0.0527, "3": 0.0098} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [compare]** By how much did the participant's fast fall short of the SOP 10-hour requirement, as a percentage of 10 hours? Measure from the stated start of fasting to the first food or drink other than water on the sample morning. Rate the shortfall.  
  `0` = Negligible: shortfall below 2%; `1` = Slight: at least 2% but below 5%; `2` = Moderate: at least 5% but below 8%; `3` = Substantial: 8% or more  
  gold: {"0": 0.0275, "1": 0.045, "2": 0.0875, "3": 0.84} · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [compare]** How long did the site take to make its first callback after the voicemail was received on 29 October? Measure in whole minutes from the voicemail's received time to the recorded call-back time.  
  `0` = Prompt: under 30 minutes; `1` = Moderate: at least 30 but under 60 minutes; `2` = Slow: 60 minutes or more  
  gold: {"0": 0.0415, "1": 0.92, "2": 0.0385} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [read]** How many outbound call attempts by the site to the participant are recorded in the CRM note for 29 October 2026? Count each recorded attempt, whether or not it was answered.  
  `0` = None: no outbound call attempts recorded; `1` = One: exactly one attempt recorded; `2` = Several: two or more attempts recorded  
  gold: {"0": 0.0373, "1": 0.92, "2": 0.0427} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F5-0066  ·  F5 Numerical and quantitative reasoning  ·  warehouse  ·  incident report

```
INCIDENT REPORT: IR-2026-0417
Site: Ashcombe Park Distribution Centre (ADC), Unit 4
Report type: Stock discrepancy / mis-pick event
Reported by: Tomasz Wierzbicki, Shift Supervisor (Nights B)
Date of report: 30/10/2026
Date/time of event start: Thursday 29/10/2026, 22:40
Date/time of event end: Friday 30/10/2026, 06:15

Areas affected: Aisle 14–16 (ambient), Dock 7

TIMELINE
22:40  Pallet PL-88213 (SKU 40117-B, pickle jars 12 x 340g) flagged on WMS as "short" at location 14-03-C during replenishment.
23:05  Replen operative (Kwabena Osei) confirms 9 cases on site vs 14 cases on WMS.
23:12  Stock control (Priya Lindqvist) placed hold HD-0930 on location 14-03-C.
23:50  Customer order CO-771042 (Harrowgate Foods) picked from 14-03-C prior to hold taking effect in RF handsets. Picker note: "location showed stock, scanned OK".
01:30  Cycle count of Aisle 14 started. 2 of 6 locations recounted; 1 further variance found at 14-05-A.
02:10  Ops manager (Dinesh Varghese) informed by phone. Dock 7 outbound paused pending check.
04:20  Shipment to Harrowgate Foods (trailer TR-44-19) released, 14 cases loaded. Driver remarks: trailer seal applied 04:24.
06:15  Event closed on WMS for location 14-03-C. Stock adjusted to 9 cases.

WITNESS REMARKS
Kwabena Osei (Replen): "Cases were stacked two deep on the back row. Count showed nine when I got there. Didn't go behind the front row."
Ana Rusu (Picker): "Handset showed the location as available. I didn't see a hold on it. Mistake was mine not to ask."
Gavin Shaw (Dock 7 yard): "Trailer was full before anyone told me about the hold. I checked the seal and the paperwork matched the scanner."

STOCK FIGURES
Location 14-03-C, WMS quantity before event: 14 cases.
Physical count after event: 9 cases.
Stock adjustment: -5 cases (value at £6.80 per case, net weight 4.08 kg per case).
Harrowgate Foods order CO-771042 quantity: 14 cases, 4.08 kg per case, total 57.12 kg (126 lb).
Cases shipped on TR-44-19: 14 (see above).
Previous month (September) short-picks on Aisle 14: 3 of 812 pick lines.
October short-picks on Aisle 14: 11 of 947 pick lines.
Invoice value on CO-771042: £95.20. Customer PO quoted £89.60 for the same lines.

ACTIONS
- Hold HD-0930 remains in place on 14-03-C pending full aisle recount.
- Harrowgate Foods to be contacted re: 5-case shortfall and invoice query.
- Pick-to-light calibration review requested for Aisle 14 (ref. MT-5518).

Supervisor sign-off: ______________  Date: __/__/____

```

**q1 [compare]** Rate how many times higher the Aisle 14 short-pick rate (short-picked lines divided by total pick lines) was in October than in September. Work from the stated line counts and round the ratio to two decimal places before choosing a level.  
  `0` = Lower: October ratio below 1.00 (rate fell); `1` = Similar: at least 1.00 but below 1.50; `2` = Moderately higher: at least 1.50 but below 2.50; `3` = Much higher: at least 2.50 but below 3.00; `4` = Sharply higher: 3.00 or more  
  gold: {"0": 0.0, "1": 0.0, "2": 0.0, "3": 0.08, "4": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [compare]** Rate the size of the invoice overcharge on the Harrowgate Foods order, as the invoice value minus the customer PO value, expressed as a percentage of the PO value, rounded to two decimal places.  
  `0` = Minor: invoice is no more than 2.00% above the PO value, or is at or below it; `1` = Moderate: more than 2.00% but below 10.00% above the PO value; `2` = Large: 10.00% or more above the PO value  
  gold: {"0": 0.04, "1": 0.92, "2": 0.04} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [read]** Rate how many additional stock variances, at locations other than 14-03-C, the Aisle 14 cycle count found during this event, as stated in the timeline.  
  `0` = None: no further variances found; `1` = Few: one or two further variances; `2` = Several: three to five further variances; `3` = Many: six or more further variances  
  gold: {"0": 0.0369, "1": 0.92, "2": 0.0308, "3": 0.0123} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** Rate the elapsed time from the hold being placed on location 14-03-C to the Harrowgate shipment being released, taken from the timeline, in hours rounded to one decimal place. Times fall on consecutive nights.  
  `0` = Short: under 2.0 hours; `1` = Moderate: at least 2.0 but under 4.0 hours; `2` = Long: at least 4.0 but under 6.0 hours; `3` = Very long: 6.0 hours or more  
  gold: {"0": 0.0, "1": 0.0436, "2": 0.92, "3": 0.0364} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F5-0089  ·  F5 Numerical and quantitative reasoning  ·  call centre QA  ·  voicemail and CRM note

```
VOICEMAIL TRANSCRIPT
Queue: Complaints Escalation Line
Received: Tue 27 Oct 2026, 16:42
Duration: 1 min 58 sec
Caller: Mrs D. Okonkwo-Reyes, acct ref BLD-447203817
Callback no. on file: 07700 900 418

"Hi, yeah, um, it's Denise Okonkwo-Reyes, I'm calling about the boiler service booking, reference is, hang on, BLD dash four four seven... two oh three eight one seven. So. I was told on the Thursday, the nineteenth, by somebody, I didn't catch the name, that an engineer would come between eight and twelve on the Monday. And I took the whole morning off, which, you know, I'm on about a hundred and eighty pounds a day, so that's, what, nearly two hundred quid I've lost really, and nobody came. Nobody rang. I rang you three times, I think, maybe four, and I was on hold for like, God, forty minutes the first time, then the second time it cut off after about twelve minutes. Anyway, I was then told by someone else on Wednesday that it's now the Friday, and I said I'm not doing that again. And I'd just like someone to ring me back, and I'd like to know what's happening about the, the lost money, I suppose. Um. Yeah. Thanks. Bye."

---

CRM CONTACT NOTE
Case: CMP-2026-0031588
Account: BLD-447203817
Agent: Owen Kirkland (ID 4417)
Logged: 27/10/2026 17:05

Customer rang back on 27/10 regarding missed boiler service visit booked for Mon 24/10, slot 08:00–12:00. Customer reports she took the morning off work. Customer states she was told on Thu 16/10 slot was confirmed. Engineer did not attend. Customer says she has called 3 times, possibly 4.

Checked booking history: original booking created 16/10 14:22 by agent ID 3159. Visit rescheduled 22/10 to Fri 30/10, 13:00–17:00. Reschedule notification sent by SMS 22/10 16:10 to number on file. No outbound call logged.

Customer's inbound contacts on this account since 16/10: 4 calls logged (16/10, 20/10, 22/10, 24/10). Call handling times per telephony: 6m 12s, 19m 40s, 3m 05s, 11m 48s.

Explained to customer that visit is now 30/10 afternoon. Customer said she will not be available that slot as she has booked annual leave for the week of 2 Nov only, and asked for a callback re compensation for loss of earnings. Customer quoted approx £180 per day, "nearly £200" total loss.

Advised customer I would raise with Complaints Team for review. Callback requested for Wed 28/10 after 09:00 (customer prefers mornings).

Actions: CMP case raised. Rebook request sent to scheduling. Compensation review requested (no amount offered at this stage).

Note: Customer's reference to Thursday 19th is recorded as 16/10 on system; may be a different booking date, to be checked.
```

**q1 [read]** What daily earnings figure, in pounds per working day, does the customer quote for herself in the voicemail and the CRM note? Use the stated per-day figure, not the 'nearly £200' total.  
  `0` = Under 150: below £150 per day; `1` = 150 to under 200: at least £150 but below £200 per day; `2` = 200 to under 250: at least £200 but below £250 per day; `3` = 250 to under 300: at least £250 but below £300 per day; `4` = 300 or more: £300 per day or above  
  gold: {"0": 0.0338, "1": 0.92, "2": 0.0338, "3": 0.0062, "4": 0.0062} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [compare]** What is the total telephony call handling time, in minutes, of all inbound calls logged on the account from 16/10 to 27/10 in the CRM note? Add all logged calls, convert seconds to fractions of a minute, no rounding.  
  `0` = Under 15: below 15 minutes; `1` = 15 to under 25: at least 15 but below 25 minutes; `2` = 25 to under 35: at least 25 but below 35 minutes; `3` = 35 to under 45: at least 35 but below 45 minutes; `4` = 45 or more: 45 minutes or above  
  gold: {"0": 0.0121, "1": 0.017, "2": 0.0339, "3": 0.92, "4": 0.017} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [infer]** Using the CRM booking history, how many calendar days elapsed between creation of the original booking and the rescheduled visit date now offered to the customer? Count the day difference between the two dates.  
  `0` = Short: fewer than 7 days; `1` = Moderate: at least 7 but fewer than 12 days; `2` = Long: 12 days or more  
  gold: {"0": 0.0311, "1": 0.0489, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** Compare the customer's voicemail claim of about forty minutes on hold for her first call with the longest call handling time in the CRM log. Rate the ratio of the claimed forty minutes to that longest logged time, to two decimal places.  
  `0` = Not exceeded: ratio below 1.00; `1` = Modestly exceeded: ratio at least 1.00 but below 1.50; `2` = Greatly exceeded: ratio 1.50 or above  
  gold: {"0": 0.028, "1": 0.052, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F5-0044  ·  F5 Numerical and quantitative reasoning  ·  car park enforcement  ·  system record

```json
{
 "record_id": "PCN-RX-2026-0448213",
 "record_type": "penalty_notice_case_export",
 "exported_at": "2026-10-30T08:14:52Z",
 "schema_ver": "4.2.1",
 "case": {
  "caseRef": "PCN/44821/3",
  "status": "APPEAL_RECEIVED",
  "opened_on": "2026-10-12",
  "Last Updated": "2026-10-29 16:41:07",
  "priority": "standard",
  "assigned_clerk_id": "CLK-0917",
  "appeal_stage": "stage_1_review"
 },
 "site": {
  "site_code": "MRD-07",
  "site_name": "Mill Road Deck (Level 2-4)",
  "operator": "Harcourt Parking Services Ltd",
  "bay_count": "212",
  "tariff_band": "B"
 },
 "contravention": {
  "code": "ANPR-04 Overstay",
  "issued_at": "2026-10-24T21:37:00+01:00",
  "entry_ts": "2026-10-23T23:52:18+01:00",
  "exit_ts": "2026-10-25T00:09:41+01:00",
  "grace_period_mins": "15",
  "paid_duration_mins": null,
  "charge_gbp": "70.00",
  "reduced_charge_gbp": "35.00"
 },
 "vehicle": {
  "reg": "KX71 PLW",
  "make": "Vauxhall",
  "colour": null,
  "permit_holder": false
 },
 "evidence": [
  {
   "ev_id": "E1",
   "type": "ANPR_image",
   "captured_at": "2026-10-24T21:37:02+01:00",
   "confidence_pct": "94.2"
  },
  {
   "ev_id": "E2",
   "type": "pay_record",
   "tariff_note": "Weekday 07:00-19:00 GBP 2.40/hr; overnight flat GBP 9.00 (19:00-07:00)",
   "amount_paid_gbp": "6.80",
   "paid_until": "2026-10-24T19:00:00+01:00"
  }
 ],
 "appeal": {
  "appellant_name": "Dorota Wielgus",
  "grounds_code": "G3-PAID-SHORT",
  "stated_amount_claimed_gbp": "14.50",
  "receipt_ref": "RCP-88213-B",
  "notes": "Appellant says they paid GBP 14.50 via app on 24 Oct for a stay ending 07:00 on 25 Oct, and that the entry scan was at 23:52 on Friday. Receipt total shown on screenshot is GBP 14.50 but app transaction log lists GBP 9.00. Appellant also mentions the car was moved to the upper deck at approx 00:05 for a cash machine. Clerk note: awaiting app provider reconciliation."
 },
 "history": {
  "prev_status": "NEW",
  "change_ts": "2026-10-14T09:02:11Z",
  "sla_days": "28",
  "days_elapsed_at_export": "16",
  "reminders_sent": 0
 },
 "meta": {
  "legacy_id": null,
  "import_batch": "B-2026-10-18-03",
  "src_sys": "PCN_v3",
  "checksum": "a71f9c0e"
 }
}
```

**q1 [infer]** Working from the pay record, the issue time and the grace period, how many whole minutes of unpaid time had passed when the notice was issued, after deducting the grace period? Treat a negative result as zero.  
  `0` = None: zero minutes of unpaid time after the grace period; `1` = Short: more than 0 but no more than 60 minutes after the grace period; `2` = Extended: more than 60 minutes after the grace period  
  gold: {"0": 0.032, "1": 0.048, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [judge]** From the appeals clerk's view, how strongly do the payment figures and times recorded in the case contradict the appellant's account of having paid for a stay to 07:00? Judge the record as a whole.  
  `0` = Slight: the record broadly supports the appellant's account, with only minor differences; `1` = Moderate: the record leaves the account partly supported and partly contradicted; `2` = Strong: the record clearly contradicts the appellant's account on the amount paid or its coverage  
  gold: {"0": 0.03, "1": 0.1725, "2": 0.7975} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [infer]** Taking the three payment figures in the case (amount claimed, amount in the app log, amount in the pay record), what is the gap in GBP between the highest and the lowest? Round to the nearest penny.  
  `0` = Minimal: below GBP 2.00; `1` = Moderate: at least GBP 2.00 but below GBP 8.00; `2` = Large: at least GBP 8.00 but below GBP 12.00; `3` = Very large: GBP 12.00 or more  
  gold: {"0": 0.0246, "1": 0.92, "2": 0.0431, "3": 0.0123} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** What share of the appeal service-level period had elapsed when the case was exported? Divide days elapsed by the stated service-level days, as a percentage rounded to one decimal place.  
  `0` = Very early: below 20.0%; `1` = Early: at least 20.0% but below 35.0%; `2` = Mid-way: at least 35.0% but below 50.0%; `3` = Advanced: at least 50.0% but below 60.0%; `4` = Late: 60.0% or more  
  gold: {"0": 0.0145, "1": 0.0145, "2": 0.0291, "3": 0.9201, "4": 0.0218} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F5-0027  ·  F5 Numerical and quantitative reasoning  ·  IT service desk  ·  system record

```json
{
 "rec_id": "SD-2026-07714",
 "ticket_no": "INC0047713",
 "opened_ts": "2026-10-27T08:52:14Z",
 "status_cd": "RESOLVED",
 "prio": "P3",
 "cat_path": "Network > Remote Access > VPN",
 "svc_name": "Corp VPN gateway",
 "site_code": "LDS-02",
 "reporter": {
  "emp_no": "E20417",
  "name": "Hollis, Dunya",
  "dept": "Finance Ops",
  "contact_ext": null
 },
 "impact": {
  "users_affected": "24",
  "headcount_base": 600,
  "pct_basis": "site_headcount",
  "sev_hint": "degraded"
 },
 "policy_ref": {
  "clause": "ITSM-4.2.3",
  "escalate_if_pct_gte": 4,
  "escalate_if_restore_hrs_gt": 6
 },
 "outage_window": {
  "start_utc": "2026-10-27T06:10:00Z",
  "end_utc": "2026-10-27T13:40:00Z",
  "duration_min": "450"
 },
 "restore_time": {
  "value": "7.5",
  "unit": "hours"
 },
 "latency_samples_ms": [
  412,
  388,
  455,
  401,
  17
 ],
 "latency_void_flag": [
  false,
  false,
  false,
  false,
  true
 ],
 "daily_err_count": [
  14,
  3,
  22,
  9,
  17
 ],
 "daily_err_limit": 15,
 "incidents_prev_month": 31,
 "incidents_this_month": "22",
 "licence_lines": [
  {
   "sku": "VPN-CONC",
   "amt_gbp": "1180.00"
  },
  {
   "sku": "VPN-SUP",
   "amt_gbp": "240.50"
  },
  {
   "sku": "VPN-EXT",
   "amt_gbp": "95.25"
  }
 ],
 "sla": {
  "resp_target_min": 60,
  "resp_actual_min": "48",
  "resolve_target_hrs": 8
 },
 "assignment": {
  "grp": "NET-L2",
  "agent_id": "ajp481",
  "assigned_by": null
 },
 "ui_colour": "#4A90D9",
 "legacy_tmp_flag": "x0",
 "notes": "Intermittent drops reported by Finance Ops users on the LDS-02 VPN concentrator from Monday morning; the affected count was revised twice during triage. Latency sample 5 was flagged as a probe artefact by NET-L2 and voided. Restore confirmed by change CHG-88214 rollback at 13:40 UTC."
}
```

**q1 [compare]** Rate the share of the site headcount affected by this incident: users affected divided by the headcount base, as a percentage, using the document's stated basis. No rounding before comparing with the edges.  
  `0` = Under two: below 2%; `1` = Two to under three: at least 2% but below 3%; `2` = Three to under four: at least 3% but below 4%; `3` = Four or more: 4% or above  
  gold: {"0": 0.0171, "1": 0.0229, "2": 0.04, "3": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [compare]** Rate the mean recorded latency in milliseconds for this incident, taking the arithmetic mean of the latency samples after excluding any sample flagged as voided. Do not round before comparing with the edges.  
  `0` = Very low: below 300 ms; `1` = Low: at least 300 ms but below 450 ms; `2` = Moderate: at least 450 ms but below 600 ms; `3` = High: at least 600 ms but below 750 ms; `4` = Very high: 750 ms or more  
  gold: {"0": 0.0267, "1": 0.9199, "2": 0.04, "3": 0.0067, "4": 0.0067} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [infer]** Rate how many of the two numeric escalation triggers in the cited policy clause this incident meets: affected share of headcount at or above its threshold, and restoration time in hours above its threshold. Work out both values from the record.  
  `0` = None: neither trigger is met; `1` = One: exactly one trigger is met; `2` = Both: both triggers are met  
  gold: {"0": 0.0185, "1": 0.0615, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** Rate the number of the five recorded days on which the daily error count strictly exceeded the daily error limit. A count equal to the limit does not exceed it.  
  `0` = None: no days exceeded the limit; `1` = One: exactly one day exceeded the limit; `2` = Two or more: at least two days exceeded the limit  
  gold: {"0": 0.03, "1": 0.05, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F5-0007  ·  F5 Numerical and quantitative reasoning  ·  hospital beds  ·  system record

```json
{
 "record_id": "DC-2026-10-04417",
 "ward_code": "MED-4W",
 "Ward_Name": "Medical Ward 4 West",
 "created": "2026-10-29T16:42:10Z",
 "patient": {
  "pseudo_id": "PX-887231",
  "age_yrs": 81,
  "sex": "F",
  "weight": {
   "value": "152",
   "unit": "lb"
  },
  "weight_kg_recorded": null
 },
 "admission": {
  "admitted_at": "2026-10-22T09:15",
  "source": "ED",
  "los_days_to_date": "7"
 },
 "discharge": {
  "planned_date": "2026-11-02",
  "readiness_status": "pending_package",
  "barriers": [
   "package_of_care",
   "equipment_delivery"
  ],
  "est_wait_hrs": 3.5
 },
 "pharmacy_wait_min_readings": [
  "42",
  "58",
  35
 ],
 "bed_census": {
  "beds_occupied": 27,
  "beds_staffed": "34",
  "occupancy_snapshot_date": "2026-10-29"
 },
 "delayed_discharges": {
  "this_week": 9,
  "prior_week": "6",
  "reporting_period": "wk44"
 },
 "ward_summary": {
  "delayed_pct_basis": {
   "numerator": 9,
   "denominator": "31"
  },
  "ref_month_bed_days": 812
 },
 "comparator": {
  "ward_code": "MED-3E",
  "beds_occupied": "22",
  "beds_staffed": 28
 },
 "social_care": {
  "referral_id": null,
  "assessor_name": "J. Okonkwo",
  "package_hours_wk": "14",
  "rate_gbp_per_hr": "24.10"
 },
 "equipment": {
  "item": "hospital bed mattress (pressure relieving)",
  "order_ref": "EQ-55102",
  "eta": null
 },
 "Notes": "Family requested discharge on Saturday. Package hours not yet confirmed by provider. Pharmacy discharge list reconciled at 14:20 but TTO pending.",
 "legacy_flag": "X",
 "print_queue_id": 7712,
 "updated_by": "bmo_svc"
}
```

**q1 [read]** Rate how many delayed discharges the ward reported for the current reporting week (wk44), as a count of patients stated in the delayed discharges section.  
  `0` = None: no delayed discharges reported; `1` = Few: at least 1 but fewer than 4 delayed discharges; `2` = Several: at least 4 but fewer than 7 delayed discharges; `3` = Many: 7 or more delayed discharges  
  gold: {"0": 0.0218, "1": 0.0218, "2": 0.0364, "3": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [infer]** Rate the weekly cost to the hospital's social care partner of this patient's planned care package, in pounds sterling. Multiply weekly package hours by the hourly rate. Give the cost to the nearest penny and ignore any other charges.  
  `0` = Lower: below £400.00 per week; `1` = Middle: at least £400.00 but below £600.00 per week; `2` = Higher: £600.00 per week or more  
  gold: {"0": 0.92, "1": 0.0533, "2": 0.0267} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [compare]** Rate how far Medical Ward 4 West's bed occupancy exceeds that of comparator ward MED-3E. Occupancy is beds occupied divided by beds staffed, as a percentage. Subtract the comparator's from this ward's, in percentage points, rounded to one decimal place.  
  `0` = Similar or lower: difference below 3.0 percentage points, including any negative difference; `1` = Moderately higher: difference of at least 3.0 but below 8.0 percentage points; `2` = Much higher: difference of 8.0 percentage points or more  
  gold: {"0": 0.92, "1": 0.0571, "2": 0.0229} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** Rate the week-on-week rise in the ward's delayed discharges, comparing this week's count with the prior week's. Calculate the percentage change relative to the prior week, rounded to the nearest whole percent. A fall counts as a negative change.  
  `0` = Flat or small: change below 10%, including any fall; `1` = Moderate: change of at least 10% but below 25%; `2` = Large: change of at least 25% but below 40%; `3` = Very large: change of 40% or more  
  gold: {"0": 0.024, "1": 0.024, "2": 0.032, "3": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F5-0083  ·  F5 Numerical and quantitative reasoning  ·  farm produce  ·  system record

```json
{
 "record_id": "GRN-2026-10-30-004417",
 "record_type": "inbound_delivery_grading",
 "schema_ver": "3.2.1",
 "site": {
  "site_code": "HW-PH2",
  "site_name": "Harrowfield Packhouse No.2",
  "region": "Eastern Marches",
  "timezone": "Europe/London"
 },
 "delivery": {
  "delivery_no": "DLV-881204",
  "grower_ref": "GR-0457",
  "grower_name": "Lowmere Orchards Ltd",
  "received_ts": "2026-10-30T23:41:09Z",
  "tipped_ts": "2026-11-01T00:18:52Z",
  "vehicle_reg": "YK23 PRN",
  "driver_id": "DRV-3319",
  "gross_kg": "4812.5",
  "tare_kg": "1190",
  "net_kg": null,
  "pallet_count": "38"
 },
 "commodity": {
  "commodity_code": "APL-GALA-C2",
  "desc": "Gala apples, class 2 in store",
  "variety": "Gala",
  "pack_spec": "12.5kg bulk bin",
  "unit_basis": "per_bin",
  "bin_count_declared": "41",
  "bin_count_weighed": null
 },
 "grading": {
  "sample_size": 40,
  "sampled_units": "fruit",
  "sample_bins_drawn_from": "first 8 bins",
  "defects_found": {
   "bruising": "3",
   "russet": "1",
   "scab": null,
   "codling_moth": 0
  },
  "pass_count": 31,
  "total_graded": 40,
  "grade_outcome": "HOLD_PENDING_REVIEW",
  "grader_initials": "JMT",
  "grade_version": "v2.4"
 },
 "storage": {
  "cold_room_id": "CR-7",
  "set_point_c": "1.2",
  "rh_pct": "92",
  "store_entry_ts": null,
  "prior_store_wk_cost_gbp_per_t": "6.40",
  "store_cost_basis": "per_week"
 },
 "history": {
  "prev_delivery_no": "DLV-880917",
  "prev_pass_rate_pct": "84.0",
  "prev_net_kg": "4306.0",
  "prev_received_ts": "2026-10-23T07:12:40Z",
  "season_avg_pass_rate_pct_ytd": "78.5",
  "season_avg_basis": "unweighted_mean_of_deliveries"
 },
 "system_flags": {
  "sync_state": "ok",
  "legacy_ref": "HW1-LEG-00457",
  "do_not_export": false,
  "lot_locked": null,
  "hold_reason_code": "HR-07"
 },
 "notes": "Bins received after the 23:00 cut-off at the weighbridge, so tipping was scheduled for Saturday morning but the shift rota had no weekend cover and the delivery stood on the apron until Sunday. Grader sampled 40 apples from the first 8 bins only, and the remaining bins were not checked before the hold was applied. Grower has been emailed about the weekend tipping delay and asked to confirm the bin count."
}
```

**q1 [compare]** How long did the delivery wait between weighbridge receipt and tipping, in hours, using the two timestamps on the record (both in UTC)? Round to one decimal place.  
  `0` = Brief: under 6.0 hours; `1` = Moderate: at least 6.0 but under 12.0 hours; `2` = Long: at least 12.0 but under 24.0 hours; `3` = Very long: 24.0 hours or more  
  gold: {"0": 0.0145, "1": 0.0145, "2": 0.0509, "3": 0.9201} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [infer]** How far did this delivery's sample pass rate (passes divided by total graded, as a percentage) fall below the previous delivery's pass rate? Use percentage points, rounded to one decimal place. A rise counts as no fall.  
  `0` = Small: under 2.0 points fall, or no fall; `1` = Moderate: at least 2.0 but under 5.0 points fall; `2` = Large: 5.0 points fall or more  
  gold: {"0": 0.0243, "1": 0.0557, "2": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [judge]** How representative of the whole delivery is the grading sample, in your judgement as packhouse manager, given how and where the sample was drawn? Rate the sample's representativeness only, not the grade outcome.  
  `0` = Poor: drawn from a small part of the delivery, so conclusions about the whole are weak; `1` = Fair: covers a fair part of the delivery, with some gaps; `2` = Good: drawn across the delivery, so conclusions about the whole are sound  
  gold: {"0": 0.905, "1": 0.085, "2": 0.01} · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [infer]** Using the net weight (gross minus tare) and the prior weekly cold-store cost per tonne, what would one week of storage for this whole delivery cost, in pounds? Round to the nearest pound.  
  `0` = Low: under £20; `1` = Middle: at least £20 but under £25; `2` = High: £25 or more  
  gold: {"0": 0.045, "1": 0.92, "2": 0.035} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F5-0056  ·  F5 Numerical and quantitative reasoning  ·  bank branch  ·  system record

```json
{
 "record_id": "ASV-REC-0448217",
 "export_ts": "2026-10-29T16:42:11Z",
 "source_system": "CoreBank_AcctServ v7.3.1",
 "branch": {
  "branch_code": "NRW-044",
  "branch_name": "Harrowgate Lane Branch",
  "region_cd": "NE-2",
  "sort_code": "40-17-29"
 },
 "account": {
  "acct_no": "61483907",
  "acct_type": "BUS_CURRENT",
  "product_ref": "PRD-BC-220",
  "opened_dt": "2019-03-14",
  "status": "ACTIVE",
  "overdraft_limit_gbp": "12500.00",
  "arranged_od_flag": "Y"
 },
 "balances": {
  "ledger_bal_gbp": "8342.67",
  "avail_bal_gbp": "7910.15",
  "uncleared_chq_gbp": "432.52",
  "pending_debits": [
   {
    "ref": "PD-7731",
    "amt_gbp": "1204.00",
    "desc": "BACS DD - Lindqvist Fleet Leasing"
   },
   {
    "ref": "PD-7732",
    "amt_gbp": "389.90",
    "desc": "Card auth - Northgate Fuel"
   },
   {
    "ref": "PD-7739",
    "amt_gbp": null,
    "desc": "Standing order hold - pending amount"
   }
  ]
 },
 "servicing_case": {
  "case_id": "SC-2026-10-0093",
  "queue": "Business Lending Review",
  "opened_ts": "2026-10-27T09:15:00Z",
  "agent_id": "OPS-4417",
  "priority": 2,
  "sla_hrs": 48,
  "elapsed_hrs": "31.5",
  "contact_ref": "CT-0028841"
 },
 "turnover": {
  "period": "2026-Q3",
  "credits_gbp": "58210.40",
  "debits_gbp": "55987.10",
  "prior_period_credits_gbp": "49834.00",
  "credits_basis": "gross_incl_transfers"
 },
 "fleet_meta": {
  "vehicles": 14,
  "avg_weekly_mileage_mi": "1865",
  "fuel_spend_gbp_mo": "6210.00",
  "weight_kg_sample": "1450"
 },
 "ops_notes": "Customer requested temporary overdraft extension ahead of quarterly VAT payment due 2026-11-07. Pending standing order amount not yet confirmed by payee; hold flagged for manual release. Turnover figures are gross and include internal sweep transfers between sub-accounts.",
 "legacy_ref": "LGCY-NRW-00912",
 "tmp_flag_x": "N",
 "print_fmt_cd": "A4P",
 "last_updated_by": "svc_batch_nightly",
 "rec_version": 4
}
```

**q1 [read]** How many hours remain on the servicing case's SLA at export time, from the case's stated SLA allowance and elapsed hours? Round to one decimal place; use hours.  
  `0` = Short: under 24.0 hours remain; `1` = Moderate: at least 24.0 but under 36.0 hours remain; `2` = Long: 36.0 hours or more remain  
  gold: {"0": 0.92, "1": 0.0533, "2": 0.0267} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [read]** How large is the customer's fleet, by the number of vehicles stated in the fleet metadata?  
  `0` = Very small: fewer than 5 vehicles; `1` = Small: at least 5 but fewer than 10 vehicles; `2` = Medium: at least 10 but fewer than 13 vehicles; `3` = Large: at least 13 but fewer than 17 vehicles; `4` = Very large: 17 or more vehicles  
  gold: {"0": 0.0, "1": 0.0, "2": 0.0343, "3": 0.92, "4": 0.0457} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [compare]** How strong is the percentage growth in gross credit turnover in the stated quarter compared with the prior period's credits? Use the stated gross figures as given, and round to one decimal place.  
  `0` = Decline: below 0.0% (credits fell); `1` = Flat: at least 0.0% but below 5.0%; `2` = Modest: at least 5.0% but below 10.0%; `3` = Solid: at least 10.0% but below 15.0%; `4` = Strong: 15.0% or more  
  gold: {"0": 0.0, "1": 0.0, "2": 0.0, "3": 0.08, "4": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** How high is the monthly fuel spend per vehicle, in pounds, found by dividing the stated monthly fuel spend by the number of vehicles? Round to the nearest whole pound.  
  `0` = Minimal: under £100; `1` = Low: at least £100 but under £200; `2` = Moderate: at least £200 but under £300; `3` = High: at least £300 but under £400; `4` = Very high: £400 or more  
  gold: {"0": 0.0, "1": 0.0, "2": 0.0, "3": 0.08, "4": 0.92} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F5-0067  ·  F5 Numerical and quantitative reasoning  ·  clinical trial site  ·  system record

```json
{
 "rec_id": "VSW-2026-0417",
 "rec_type": "visit_window_deviation",
 "created_ts": "2026-10-29T16:42:11Z",
 "modified_by": "rtanaka.bell",
 "site": {
  "siteCode": "GB-14-LDN-03",
  "site_name": "Harrowgate Clinical Research Unit",
  "pi_name": "Dr A. Okonkwo-Reyes",
  "coord_name": "R. Tanaka-Bell",
  "legacy_site_no": "3317"
 },
 "protocol": {
  "protocolNo": "HX-221-PH2",
  "version": "4.1",
  "amend_date": "2026-08-12",
  "ethics_ref": "REC/26/1184"
 },
 "subject": {
  "subjId": "1047-0093",
  "initials": "M.P.",
  "yob": "1971",
  "sex": "F",
  "randomArm": null,
  "icf_version": "3.0"
 },
 "visit": {
  "visit_code": "V6",
  "visitName": "Week 12",
  "day0_dt": "2026-07-30",
  "target_day": 84,
  "window_before_days": "3",
  "window_after_days": "3",
  "sched_dt": "2026-10-22",
  "actual_dt": "2026-10-29",
  "actual_day": "91",
  "window_status": "OUT_OF_WINDOW",
  "deviation_cat": "minor"
 },
 "samples": {
  "pk_tubes_required": 8,
  "pk_tubes_received": "5",
  "pk_freezer_temp_C": "-63.9",
  "freezer_limit_C": -70,
  "transit_minutes": "1460",
  "transit_limit_hrs": 24,
  "lab_batch_ref": "LB-88213",
  "aliquot_note": null
 },
 "enrolment": {
  "enrol_sep_2026": "12",
  "enrol_oct_2026": "17",
  "icf_signed_pts": 31,
  "icf_required_pts": 40
 },
 "prior_devs": [
  {
   "ref": "VSW-2026-0391",
   "visit_code": "V4",
   "dev_dt": "2026-09-03",
   "amt_gbp": "0.00"
  },
  {
   "ref": "VSW-2026-0312",
   "visit_code": "V2",
   "dev_dt": "2026-07-21",
   "amt_gbp": null
  }
 ],
 "reimb": {
  "visit_fee_gbp": "145.00",
  "travel_claim_gbp": "38.50",
  "invoice_ref": "INV-7731-A",
  "paid_dt": null
 },
 "misc": {
  "printer_queue_id": "PQ-04",
  "legacy_import_flag": false,
  "tz": "Europe/London",
  "ver_hash": "a9f3c1e"
 },
 "notes": "Participant attended on 29 October after rescheduling from the 22 October slot due to a family bereavement. Pharmacokinetic sample collection was incomplete, with three tubes not received; courier logged the shipment as delayed at the hub. Coordinator to confirm with sponsor monitor before the next visit is booked."
}
```

**q1 [compare]** For visit V6, how many whole calendar days outside the permitted protocol window was the actual visit? Count days from the nearest window limit (target day plus or minus the stated tolerance) to the actual study day. Inside the window counts as zero.  
  `0` = None: 0 days outside the window; `1` = Slight: more than 0 but no more than 2 days outside; `2` = Moderate: more than 2 but no more than 4 days outside; `3` = Large: more than 4 days outside  
  gold: {"0": 0.0165, "1": 0.0235, "2": 0.92, "3": 0.04} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [compare]** What percentage of the required consent forms had been signed by participants at the site, using signed participants divided by required participants, as recorded in the enrolment block? Do not round before comparing with the edges.  
  `0` = Low: below 80%; `1` = Fair: at least 80% but below 95%; `2` = High: 95% or more  
  gold: {"0": 0.92, "1": 0.0587, "2": 0.0213} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [read]** How many of the listed prior deviation records show a monetary amount greater than zero pounds? A blank or missing amount does not count as greater than zero.  
  `0` = None: no prior record shows an amount above zero; `1` = One: exactly one prior record shows an amount above zero; `2` = Two: exactly two prior records show an amount above zero; `3` = Three or more: at least three prior records show an amount above zero  
  gold: {"0": 0.9201, "1": 0.0401, "2": 0.0199, "3": 0.0199} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [compare]** By how many minutes did the recorded sample transit time exceed the stated transit limit? Convert the limit from hours to minutes first. A transit within the limit counts as zero excess.  
  `0` = None: no excess, at or within the limit; `1` = Marginal: more than 0 but no more than 10 minutes over; `2` = Small: more than 10 but no more than 30 minutes over; `3` = Substantial: more than 30 but no more than 120 minutes over; `4` = Severe: more than 120 minutes over  
  gold: {"0": 0.0175, "1": 0.025, "2": 0.92, "3": 0.0275, "4": 0.01} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## SCORE-F5-0106  ·  F5 Numerical and quantitative reasoning  ·  residential lettings  ·  system record

```json
{
 "job_ref": "MNT-26-07712",
 "created_at": "2026-10-30T16:52:00Z",
 "property": {
  "prop_id": "PR-0418",
  "address_line_1": "Flat 3, 14 Carrow Lane",
  "postcode": "NR3 4LT",
  "type": "flat",
  "bedrooms": 2,
  "rent_pw": "186.50",
  "landlord_ref": "LL-2291"
 },
 "fault": {
  "category": "heating",
  "description_raw": "Boiler losing pressure every 2-3 days, tenant topping up via filling loop",
  "priority": "P2",
  "repeatCallouts12m": 3,
  "callouts_total_12m": 17,
  "gas_safe_cert_expiry": "2027-03-14"
 },
 "scheduling": {
  "reported_by": "tenant",
  "reported_on": "Fri 30/10/2026 17:40",
  "attended_on": "Mon 02/11/2026 09:15",
  "sla_days": "3",
  "visit_no": 1
 },
 "tenantContact": {
  "name": "R. Okonedo",
  "phone_mob": "07700 900418",
  "prefContact": "text",
  "access_notes": null
 },
 "contractor": {
  "name": "Hollis & Pryce Heating Ltd",
  "contractor_id": "CTR-0093",
  "quote_parts_gbp": "142.80",
  "quote_labour_gbp": "96.00",
  "quote_callout_fee_gbp": "45.00",
  "labour_minutes_onsite": "210",
  "rate_gbp_per_hr": "48.00",
  "po_number": null
 },
 "spend_history": {
  "fy2025_gbp": "1184.50",
  "fy2026_to_date_gbp": "1622.10",
  "fy_basis": "Apr-Mar"
 },
 "legacy_import_flag": "N",
 "print_template": "JOB_V2",
 "internal_colour_code": "amber",
 "notes": "Tenant reports pressure drop after the bleed on Sunday. Contractor says the expansion vessel may be undersized; not yet confirmed. Landlord approval requested if quote exceeds £250."
}
```

**q1 [infer]** By how much does the total quote for this job (parts, labour and call-out fee added together) exceed the landlord-approval threshold stated in the notes? Give the excess in pounds, rounded to the nearest penny.  
  `0` = Not over: the total is at or below the approval threshold, so no excess; `1` = Modest excess: more than £0 but no more than £50.00 above the threshold; `2` = Large excess: more than £50.00 above the threshold  
  gold: {"0": 0.0256, "1": 0.92, "2": 0.0544} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [compare]** How far did the first attendance overrun the service-level window, measured in whole elapsed hours from the tenant's reported time to the attended time, with the window taken as the stated SLA days at 24 hours per day? Zero or negative means no overrun.  
  `0` = None: attended within the window, overrun of 0 hours or less; `1` = Slight: overrun of more than 0 but no more than 12 hours; `2` = Substantial: overrun of more than 12 but no more than 24 hours; `3` = Severe: overrun of more than 24 hours  
  gold: {"0": 0.92, "1": 0.0424, "2": 0.0188, "3": 0.0188} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [read]** How many repeat callouts for this property does the job record show for the last 12 months, using the repeat-callout count field (not the total callouts)?  
  `0` = Few: three or fewer repeat callouts; `1` = Several: four to six repeat callouts; `2` = Many: seven to ten repeat callouts; `3` = Very many: more than ten repeat callouts  
  gold: {"0": 0.92, "1": 0.0368, "2": 0.0216, "3": 0.0216} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [infer]** What share of this property's callouts in the last 12 months were repeat callouts, being repeat callouts divided by total callouts, as a percentage rounded to one decimal place?  
  `0` = Low: below 20.0%; `1` = Moderate: at least 20.0% but below 35.0%; `2` = High: at least 35.0% but below 50.0%; `3` = Dominant: 50.0% or more  
  gold: {"0": 0.9201, "1": 0.0533, "2": 0.0133, "3": 0.0133} · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

