# Review sample: 50 cases (0 flagged by the checking pass, the rest random)

## X-0344  ·  translation agency  ·  form submission  ·  decider: the project manager  ·  target: mostly clear

```
LINGUAWAVE TRANSLATION LTD — FREELANCE ASSIGNMENT CHANGE REQUEST
Form ref: FAC-2026-0417   Status: SUBMITTED
Submitted: 27/10/2026 16:42   Submitted by: Tomasz Berezowski (Linguist ID LW-0882)

Section A — Assignment details
Client account:            Halvorsen Logistics (HL-0031)
Project code:              HLG-TR-2291
Source language:           English (UK)
Target language:           Polish
Word count (counted):      4,870 words
Assignment deadline:       06/11/2026 17:00 (working days)
Original delivery date:    04/11/2026
Rate card band:            B2
Rate (GBP per word):       0.082
Agreed rate per word:      0.075
Assignment manager:        Priya Ndlovu

Section B — Reason for change
Change requested:          Deadline extension
Reference to original terms: Clause 4.2(b) — see Section D
Days requested:            3 working days
Revised delivery date:     10/11/2026 17:00
Previous QA batch return:  22/10/2026 09:15 — 24/10/2026 14:30
QA errors logged (batch 2): 17 errors in 1,240 segments checked
Client portal reference:   PORTAL-88213

Section C — Payment (for information)
Invoice ref:               LW-INV-20261027-14
Amount invoiced:           GBP 396.74
Amount approved:           [blank]
Payment terms:             30 days from receipt of invoice
PO number:                 HL-PO-77410

Section D — Comments
Client's glossary was updated on 26/10 (v3.2 → v3.4). The assignment was accepted on 14/10 under the v3.2 glossary. Clause 4.2(b) of the Framework Agreement (rev. 2) states that deadline changes are permitted without fee adjustment where the glossary is revised after acceptance, except where the revision affects fewer than 5% of the segments already delivered. I have not yet been able to confirm the proportion. The batch 1 segments delivered 19/10 were 1,060 out of a total of 4,870. Terms glossary update affects 61 terms. Linguist availability is limited after 30/10 due to a prior commitment (Ref. PC-0093). Please advise whether a fee adjustment applies, and the rate to use for batch 3.

Office use only
Reviewed by:   [blank]
Date reviewed: [blank]
Decision:      [blank]
Fee outcome:   Revised rate GBP 0.075 — no change
Notes:         Rate band B2 vs. Section A rate 0.082 to be confirmed
```

**q1 [score / compare]** Rate the error rate in the checked QA batch (errors per segments checked), from the project manager's point of view.  
  `0` = Low: below 0.5% of segments checked; `1` = Moderate: at least 0.5% but below 1%; `2` = Elevated: at least 1% but below 2%; `3` = High: 2% or more  
  gold: {"0": 0.014, "1": 0.036, "2": 0.92, "3": 0.03}  · agreement 4/4 · check: settled · rate value 1.371 percent edges [0.5, 1.0, 2.0] (far)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the length of time, in calendar days, from when the change request was submitted to the requested revised delivery time, from the project manager's point of view.  
  `0` = Very short: less than 3 days; `1` = Short: at least 3 days but less than 7 days; `2` = Medium: at least 7 days but less than 12 days; `3` = Long: at least 12 days but less than 18 days; `4` = Very long: 18 days or more  
  gold: {"0": 0.0055, "1": 0.0073, "2": 0.0491, "3": 0.9199, "4": 0.0182}  · agreement 4/4 · check: settled · time_gap value 14.01 days edges [3.0, 7.0, 12.0, 18.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / infer]** The revised delivery date is more than three working days after the original assignment deadline.  
  `true` = The revised delivery falls more than three working days after the assignment deadline.; `false` = The revised delivery falls three working days or fewer after the assignment deadline, or not after it at all.  
  gold: {"true": 0.07, "false": 0.93}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / judge]** Given the agreement's exception, which outcome is best supported for the extension request?  
  `extension_no_fee_change` = Extension granted with no fee adjustment because the exception clearly does not apply.; `extension_with_fee_adjustment` = Extension granted but a fee adjustment applies because the exception clearly applies.; `extension_refused` = The extension is refused outright.; `revert_to_card_rate` = The higher rate card rate replaces the agreed rate for the remaining work.; `cannot_determine` = The document does not settle the outcome because the key proportion is unconfirmed.  
  gold: {"extension_no_fee_change": 0.0775, "extension_with_fee_adjustment": 0.0525, "extension_refused": 0.0225, "revert_to_card_rate": 0.015, "cannot_determine": 0.8325}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / compare]** Which of these figures is the highest?  
  `full_at_card_rate` = All counted words priced at the rate card rate.; `full_at_agreed_rate` = All counted words priced at the agreed rate.; `amount_invoiced` = The amount shown as invoiced.; `remaining_at_card_rate` = Only the words not in the first delivered batch, priced at the rate card rate.  
  gold: {"full_at_card_rate": 0.92, "full_at_agreed_rate": 0.0296, "amount_invoiced": 0.0326, "remaining_at_card_rate": 0.0178}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0877  ·  accounts payable  ·  system record  ·  decider: the finance controller  ·  target: mostly clear

```json
{
 "recordId": "APX-2026-004417",
 "src_system": "P2P-ERP 9.4",
 "Doc Type": "SUPPLIER_INVOICE",
 "supplierCode": "V-20871",
 "supplier_name": "Brackley Fasteners & Components Ltd",
 "invoice_no": "BFC/INV/26-1182",
 "invoice_date": "2026-10-26",
 "po_ref": "PO-55091",
 "quote_ref": "QT-7741",
 "quoted_total_gbp": "12480.00",
 "invoice_total_gbp": "12905.40",
 "currency": "GBP",
 "receipt": {
  "received_date": "2026-10-30",
  "received_time": "23:40",
  "channel": "email-inbox-ap",
  "scanned_by": "ibarnes"
 },
 "goods_receipt": {
  "grn_no": "GRN-88213",
  "posted_at": "2026-11-02T00:12:00",
  "posted_by": "mrowe",
  "qty_received": 3
 },
 "consignment": {
  "pallet_count": 3,
  "gross_weight": "roughly 1,840 kg",
  "net_weight_kg": "1812.5",
  "customs_value_gbp": "about 9,600"
 },
 "freight_options": [
  {
   "option_id": "FO-A",
   "carrier": "Northway Haulage",
   "base_rate_gbp": "1140.00",
   "fuel_surcharge_pct": 6.5,
   "minimum_charge_gbp": "180.00",
   "discount": null
  },
  {
   "option_id": "FO-B",
   "carrier": "Coldline Logistics",
   "base_rate_gbp": "1065.00",
   "admin_fee_gbp": "45.00",
   "discount": "3% if booked 48h ahead"
  },
  {
   "option_id": "FO-C",
   "carrier": "Estuary Freight",
   "base_rate_gbp": "1210.00",
   "discount": "10% on 2+ pallets",
   "fuel_surcharge_pct": 0
  },
  {
   "option_id": "FO-D",
   "carrier": "Brackley Express",
   "rate_per_pallet_gbp": "395.00",
   "min_pallets": 2,
   "collection_fee_gbp": "30.00"
  }
 ],
 "Approval": {
  "approved_by": null,
  "approval_level": "L2",
  "threshold_gbp": 10000
 },
 "payment_terms": "30 days from receipt",
 "payment_due_note": "ten days before the 14th of November",
 "ui_row_colour": "amber",
 "print_template_v": 3,
 "legacy_flag": "N",
 "notes": "Carrier collection was booked for the Friday after the 23rd of October and the supplier confirms dispatch on the Monday after. Invoice was queried by buyer on the Tuesday after the goods were received, and the reply is awaited. Freight option not yet confirmed by logistics."
}
```

**q1 [score / compare]** Rate, from the accounts payable controller's view, the delay between the invoice arriving in the inbox and the goods receipt being posted in the system.  
  `0` = Minimal: under 12 hours; `1` = Short: at least 12 hours but under 24 hours; `2` = Moderate: at least 24 hours but under 36 hours; `3` = Long: at least 36 hours but under 60 hours; `4` = Very long: 60 hours or more  
  gold: {"0": 0.008, "1": 0.0107, "2": 0.0347, "3": 0.9199, "4": 0.0267}  · agreement 4/4 · check: settled · time_gap value 48.53 hours edges [12.0, 24.0, 36.0, 60.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate, from the finance controller's view, how far the invoiced total exceeds the quoted total.  
  `0` = Negligible: under £100; `1` = Small: at least £100 but under £250; `2` = Noticeable: at least £250 but under £420; `3` = Substantial: at least £420 but under £600; `4` = Severe: £600 or more  
  gold: {"0": 0.0053, "1": 0.008, "2": 0.0533, "3": 0.9201, "4": 0.0133}  · agreement 4/4 · check: settled · difference value 425.4 GBP edges [100.0, 250.0, 420.0, 600.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / judge]** The invoice should be held back rather than approved for payment as it currently stands.  
  `true` = Open issues with the invoice mean it should be held pending resolution rather than approved now.; `false` = The invoice is in order and can reasonably be approved now despite any minor points.  
  gold: {"true": 0.9425, "false": 0.0575}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** For the three pallets, assuming every stated discount applies, which freight option costs least after its own surcharge, discount, minimum or fee?  
  `northway` = The first haulage option, with a fuel surcharge on its base rate; `coldline` = The logistics option with an advance-booking discount and an admin fee; `estuary` = The freight option with a multi-pallet percentage discount; `brackley_express` = The per-pallet option with a collection fee  
  gold: {"northway": 0.0098, "coldline": 0.92, "estuary": 0.0573, "brackley_express": 0.0129}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0884  ·  home insurance  ·  meeting notes  ·  decider: the claims handler  ·  target: mixed

```
MEETING NOTES
Home Contents Claims: Weekly Huddle
Ref: HCC-MN-2026-1029 | Date: 29/10/2026 | 09:30-09:50 | Room 4B

Attendees: Priya Nandakumar (chair), Tom Ashdown, Sofia LeBlanc, Kwame Osei
Apologies: Ruth Hallam

1. Claim HC-774219 (policy HP-30871462, Mrs D. Whitlock), lounge flood. Tom says the field inspection is booked for 3/11/2026. Sofia's diary shows 2/11/2026. Sofia to confirm with the field agent.

2. Moisture reading at inspection: 18% (north wall). Excess on the schedule is £250 per Tom; Priya recalls £300 following the April endorsement. Priya to check schedule HP-30871462-R2.

3. Survey score for CL-55102: 4/5. Kwame reports 7 complaints from 412 claims closed in September (complaint refs CMP-2026-0931 to -0937).

4. Contractor shortlist for drying and repair. Conditions: accredited; response within 48 hours; liability cover £5m or more; quote not above £2,500.
- Hartley & Vane Restoration: accredited, 72 hours, £5m, £2,410.
- Brightwater Drying Co: accredited, 24 hours, £2m, £2,150.
- Ormsby Property Services: not accredited, 24 hours, £5m, £2,300.
- Keel & Sons: accredited, 36 hours, £5m, £2,990.
- Marrow Damp Solutions: accredited, 48 hours, £5m, £2,380.

5. Survey score for CL-55118: 3/5. Late acknowledgements in October: North 38 of 610 cases; Midlands 22 of 480; Coastal 19 of 355; Thames 41 of 702; Border 12 of 260. Kwame to rank queues before next huddle.

6. Survey score for CL-55131: 5/5. Tom to chase the outstanding survey returns.

Actions
- Sofia: confirm inspection date with field agent (by 30/10).
- Priya: check excess on HP-30871462-R2.
- Tom: request written quote QT-88214 from Marrow Damp Solutions.
- Kwame: rank regional queues on late acknowledgements.
```

**q1 [score / compare]** Rate the average quoted price across all five shortlisted contractors, from the claims handler's point of view, as a cost for drying and repair.  
  `0` = Very low: under £1,000; `1` = Low: at least £1,000 but under £1,800; `2` = Moderate: at least £1,800 but under £3,500; `3` = High: at least £3,500 but under £4,500; `4` = Very high: £4,500 or more  
  gold: {"0": 0.012, "1": 0.028, "2": 0.92, "3": 0.032, "4": 0.008}  · agreement 4/4 · check: settled · average value 2446.0 GBP edges [1000.0, 1800.0, 3500.0, 4500.0] (far)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the September complaint rate (complaints as a share of claims closed), from the claims department's point of view.  
  `0` = Negligible: under 0.5%; `1` = Low: at least 0.5% but under 1.0%; `2` = Moderate: at least 1.0% but under 1.75%; `3` = High: at least 1.75% but under 3.0%; `4` = Severe: 3.0% or more  
  gold: {"0": 0.0092, "1": 0.0338, "2": 0.92, "3": 0.0308, "4": 0.0062}  · agreement 4/4 · check: settled · rate value 1.699 percent edges [0.5, 1.0, 1.75, 3.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [score / infer]** Rate how far the Hartley & Vane Restoration entry falls short of the contractor shortlist conditions, from the claims handler's point of view.  
  `0` = None: meets every condition; `1` = Minor: fails exactly one condition; `2` = Moderate: fails exactly two conditions; `3` = Major: fails exactly three conditions; `4` = Total: fails all four conditions  
  gold: {"0": 0.0255, "1": 0.9199, "2": 0.0364, "3": 0.0109, "4": 0.0073}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Which single contractor meets every stated shortlist condition?  
  `hartley_vane` = Hartley & Vane Restoration meets all conditions; `keel_sons` = Keel & Sons meets all conditions; `marrow_damp` = Marrow Damp Solutions meets all conditions; `other_candidate` = Some other shortlisted contractor, or none, meets all conditions  
  gold: {"hartley_vane": 0.0126, "keel_sons": 0.0211, "marrow_damp": 0.92, "other_candidate": 0.0463}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / compare]** Which of these three queues has the highest share of late acknowledgements in October?  
  `north` = North queue has the highest late share; `thames` = Thames queue has the highest late share; `coastal` = Coastal queue has the highest late share  
  gold: {"north": 0.92, "thames": 0.0533, "coastal": 0.0267}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-1079  ·  warehouse  ·  policy extract and case note  ·  decider: a shift supervisor  ·  target: mostly clear

```
HALDEN CROSS DISTRIBUTION CENTRE
Stock Control Procedure SC-14: Short-Dated and Damaged Stock Handling
Rev 3 | Effective 2026-09-01 | Owner: Inventory Control Manager (K. Odunlami)

1. Scope
1.1 This procedure applies to all pallets and cases held in Bays A1–D9 and the Returns Cage, Unit 4.

2. Short-dated stock
2.1 Stock with 30 or fewer calendar days' shelf life remaining on receipt is quarantined to location QZ-02 pending supervisor release.
2.2 Supervisor review must be completed within 3 working days of quarantine. Bank holidays are not working days for this purpose.
2.3 Exception: Chilled lines on the Northfield account may be released on day of receipt without review where the account's written waiver (ref NF-W-0412) is on file.

3. Damaged stock
3.1 Damaged units are logged on form DS-7 within the same shift.
3.2 Damage rate for a supplier lot is calculated as damaged units recorded divided by units inspected at goods-in, reported as a percentage to one decimal place.
3.3 Lots with a damage rate above 2.0% are referred to Supplier Quality within 2 working days.
3.4 Exception: Lots where damage is attributable to the carrier (signed POD notation "carrier damage") are referred to the carrier claims desk and are excluded from the rate in 3.2.

4. Case note: Lot HX-88217 (Brightmere Foods), received 2026-10-20
Inspected at goods-in: 1,240 units across three receiving shifts (Mon 420, Tue 515, Wed 305). Damaged units logged on DS-7: 9 (Mon 2, Tue 4, Wed 3). Two units on DS-7 #4471 were noted "carrier damage" on the POD. Lot remaining shelf life on receipt: 27 days. Quarantined to QZ-02 on 2026-10-20 at 14:10. Supervisor review booked for 2026-10-22.
```

**q1 [score / compare]** Rate the total volume of units inspected at goods-in for this lot, adding the three receiving shifts, from the shift supervisor's point of view.  
  `0` = Very small: fewer than 400 units; `1` = Small: at least 400 but fewer than 800 units; `2` = Moderate: at least 800 but fewer than 1,000 units; `3` = Large: at least 1,000 but fewer than 1,250 units; `4` = Very large: 1,250 units or more  
  gold: {"0": 0.0, "1": 0.0, "2": 0.0, "3": 0.92, "4": 0.08}  · agreement 3/4 · check: settled · adjusted · sum value 1240.0 units edges [400.0, 800.0, 1000.0, 1250.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / infer]** Rate the lot's damage rate for supplier-quality purposes, after applying the procedure's treatment of carrier-caused damage, from the supervisor's point of view.  
  `0` = Negligible: below 0.5%; `1` = Low: at least 0.5% but below 1.0%; `2` = Elevated: at least 1.0% but below 2.0%; `3` = Critical: 2.0% or more  
  gold: {"0": 0.0391, "1": 0.92, "2": 0.0353, "3": 0.0056}  · agreement 4/4 · check: settled · rate value 0.6 % edges [0.5, 1.0, 2.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [choice / compare]** Which receiving shift had the highest damage rate, using damaged units logged divided by units inspected on that shift?  
  `monday` = The first shift has the highest rate; `tuesday` = The second shift has the highest rate; `wednesday` = The third shift has the highest rate; `tied` = Two or more shifts share the highest rate  
  gold: {"monday": 0.017, "tuesday": 0.0485, "wednesday": 0.92, "tied": 0.0145}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Which single handling outcome correctly follows from the procedure for this lot?  
  `release_on_receipt` = Released the same day without review; `review_only` = Quarantine and supervisor review, no referrals; `review_and_supplier_quality` = Quarantine and review, plus referral to Supplier Quality only; `review_and_carrier_claims` = Quarantine and review, plus carrier claims desk referral only, no Supplier Quality referral; `review_supplier_and_carrier` = Quarantine and review, plus both Supplier Quality and carrier claims referrals  
  gold: {"release_on_receipt": 0.0036, "review_only": 0.0473, "review_and_supplier_quality": 0.01, "review_and_carrier_claims": 0.92, "review_supplier_and_carrier": 0.0191}  · agreement 4/4 · check: settled · adjusted  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [noul / judge]** The damage record for this lot is not serious enough to justify referring the supplier to Supplier Quality.  
  `true` = The lot's damage record, as the procedure treats it, gives no sufficient reason to refer the supplier.; `false` = The lot's damage record gives sufficient reason to refer the supplier, or the position is otherwise unsafe to dismiss.  
  gold: {"true": 0.875, "false": 0.125}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0828  ·  translation agency  ·  chat log  ·  decider: the project manager  ·  target: mostly debatable

```
Chat log: Lindqvist & Marr Translation – Assignment Desk
Channel: #jobs-open (exported 29/10/2026)

[09:02:14] Ruth Okonedo: morning all. Sorry for the mess on the Halvorsen brochure job from last week, I know Dmitri is still waiting on his remittance. Anyway, the big one today is the Ferrante pharma leaflet set, 14 pages EN>IT, deadline Fri 06/11, 17:00 CET. Need to pick a freelancer by Monday latest.
[09:04:50] Tomasz Wieczorek: ok. I've got three names who said they could take it. Sending the sheet now. Note Pilar's rate went up again, she mentioned it on the phone on Tuesday when I was trying to get hold of her about PO 4471.
[09:05:31] Ruth Okonedo: PO 4471 was the Harwood invoice, yes? Did that get paid in the end? I'm still not sure whether the 1,180.00 went out on the 14th or the 21st.
[09:07:02] Tomasz Wieczorek: Paid on the 21st I think, reference BP-20261021-07. Anyway, the sheet: https://share.example/forms/fl-sheet-0412
[09:09:40] Ruth Okonedo: Got it. Pilar Estrada is at 0.14/word, I've got her down as having the CAT tool licence, she's ISO 17100 listed but I think the certificate expired in March. Does anyone know if the Ferrante client needs ISO 17100 specifically or just "qualified"?
[09:11:18] Tomasz Wieczorek: Client brief says "qualified linguist, EN-IT medical, preferably ISO". Not mandatory. Oh and Elif Demirci just replied, she says she can do it but needs the Ferrante glossary, which we don't have yet. She's got Trados and everything.
[09:13:55] Ruth Okonedo: Glossary is with Chiara at the client, I'll chase her. Pricing sheet row 6 is the one I need to check, Elif quoted 0.11/word plus a 35.00 setup fee for the glossary build. Is that flat or per language pair?
[09:15:22] Tomasz Wieczorek: Flat I think. Also the Pilar figure is 0.14 but she had a 10% rush surcharge on top if it's under 5 days, which it is. Sorry, forgot to put that in the sheet.
[09:16:47] Ruth Okonedo: fine. Also unrelated, has anyone seen the Q3 vendor review template? Gareth wanted it by 02/11 and I can't find it on the drive.
[09:18:03] Tomasz Wieczorek: Try the folder called "Vendor Reviews (old)". Third candidate is Sandor Kiss, 0.12/word, minimum charge 80.00, native EN>IT, has the medical cert, no CAT tool. Available from Wed 04/11.
[09:20:30] Ruth Okonedo: Right. Word counts from the client are 4,912 for the whole set. Please confirm Sandor's availability and whether Elif's glossary fee is refundable if the job is cancelled. Also who is covering the Thursday call with Ferrante?
[09:21:11] Tomasz Wieczorek: Will check. Elif's terms say non-refundable. Thursday call is me.

Pricing sheet (as at 29/10/2026):
Freelancer | Rate/word | Fee | Surcharge | Min charge | CAT | Medical cert | Available from
Pilar Estrada | 0.14 | none | 10% (under 5 days) | none | yes | yes (exp. ?) | Mon 02/11
Elif Demirci | 0.11 | 35.00 glossary | none | none | yes | yes | Tue 03/11
Sandor Kiss | 0.12 | none | none | 80.00 | no | yes | Wed 04/11
Client ref: FER-2026-0931 | Job no. 88214 | PO pending
```

**q1 [score / compare]** Rate the average quoted total cost of the three candidates for the whole set, from the agency's budget point of view, including each one's own fee, surcharge or minimum.  
  `0` = Low: average below 650; `1` = Medium: average of at least 650 but below 800; `2` = High: average of 800 or more  
  gold: {"0": 0.92, "1": 0.0594, "2": 0.0206}  · agreement 4/4 · check: settled · adjusted · average value 640.4 currency units edges [650.0, 800.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate how much more the agency would pay for the most expensive candidate than for the cheapest, once each one's own fee and surcharge are included.  
  `0` = Small: difference below 150; `1` = Moderate: difference of at least 150 but below 250; `2` = Large: difference of at least 250 but below 400; `3` = Very large: difference of 400 or more  
  gold: {"0": 0.0292, "1": 0.9201, "2": 0.0415, "3": 0.0092}  · agreement 4/4 · check: settled · difference value 181.13 currency units edges [150.0, 250.0, 400.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [score / compare]** Rate the average base per-word rate across the three candidates, before fees and surcharges, from the agency's cost point of view.  
  `0` = Very low: average below 0.10; `1` = Low: average of at least 0.10 but below 0.12; `2` = Medium: average of at least 0.12 but below 0.15; `3` = High: average of 0.15 or more  
  gold: {"0": 0.0059, "1": 0.0563, "2": 0.92, "3": 0.0178}  · agreement 4/4 · check: settled · average value 0.1233 currency per word edges [0.1, 0.12, 0.15] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [noul / judge]** Waiting for the client's glossary puts Elif's delivery by the deadline at real risk.  
  `true` = The missing glossary, with no confirmed arrival, is a real threat to Elif delivering on time.; `false` = The missing glossary is not a real threat to on-time delivery, because there is ample slack or it is likely to arrive in time.  
  gold: {"true": 0.625, "false": 0.375}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** Which single candidate has a CAT tool, a medical certificate listed, can start by Tuesday 03/11, and needs nothing further from the client first?  
  `pilar` = Pilar Estrada is the only candidate meeting every condition; `elif` = Elif Demirci is the only candidate meeting every condition; `sandor` = Sandor Kiss is the only candidate meeting every condition; `none_qualify` = No candidate meets every condition; `cannot_tell` = More than one candidate qualifies, or the document cannot settle it  
  gold: {"pilar": 0.7, "elif": 0.025, "sandor": 0.015, "none_qualify": 0.105, "cannot_tell": 0.155}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q6 [choice / compare]** Which candidate is cheapest for the whole set once each one's own fee, surcharge or minimum charge is applied?  
  `pilar` = Pilar Estrada is cheapest after her surcharge; `elif` = Elif Demirci is cheapest after her fee; `sandor` = Sandor Kiss is cheapest after any minimum charge; `tie` = Two or more candidates cost exactly the same; `cannot_tell` = The document does not allow the cheapest to be determined  
  gold: {"pilar": 0.0122, "elif": 0.9199, "sandor": 0.0296, "tie": 0.0122, "cannot_tell": 0.0261}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0361  ·  recruitment  ·  system record  ·  decider: the compliance checker  ·  target: mostly debatable

```json
{
 "recordId": "RC-26-004417",
 "rec_type": "hire_readiness_check",
 "status": "PENDING_REVIEW",
 "createdAt": "2026-10-27T16:42:09Z",
 "legacy_import_flag": false,
 "candidate": {
  "candidateRef": "CND-88210",
  "full_name": "Owen Halvorsen",
  "dob": null,
  "contactPhone": null,
  "src": "agency_NW"
 },
 "role": {
  "title": "HGV Class 2 Driver (Trainee)",
  "site_code": "BRM-DC2",
  "contract_hours_pw": "37.5",
  "shiftPattern": "early",
  "shift_length": "7.5 hr"
 },
 "endorsements": {
  "signatures_received": 31,
  "signatures_required": "40",
  "signatoryGroup": "site_supervisors"
 },
 "docs": {
  "licence_received_on": "2026-10-28",
  "medical_cleared_on": "2026-11-02",
  "right_to_work_check": "ok",
  "printer_tray": "B"
 },
 "loadTest": {
  "pallet_gross_lb": 2600,
  "pallet_gross_kg": "1179",
  "tail_lift_rating_kg": 1000,
  "dwell_time": "35 min"
 },
 "response_sla": {
  "basis": "working_days",
  "days": "5",
  "clock_start": "2026-10-27"
 },
 "policy": {
  "ref": "HR-VET-07 v3",
  "clauses": [
   "1. A trainee driver must hold a provisional category C licence before any practical assessment.",
   "2. Occupational health clearance must be recorded within 28 calendar days of the offer date.",
   "3. Endorsement requires signatures from the site supervisor panel equal to the number held in signatures_required.",
   "4. Exception: where the licence was issued outside the UK, clause 2 is extended to 60 working days, and clause 3 applies only if the panel has not already met."
  ]
 },
 "practical_slots": [
  {
   "slot": "A",
   "date": "2026-11-03",
   "open": "06:00-14:00",
   "lead_time_h": "48",
   "capacity_left": 2,
   "notice": "none"
  },
  {
   "slot": "B",
   "date": "2026-11-04",
   "open": "08:00-12:00",
   "lead_time_h": "72",
   "capacity_left": 0,
   "notice": null
  },
  {
   "slot": "C",
   "date": "2026-11-06",
   "open": "07:00-15:30",
   "lead_time_h": 24,
   "capacity_left": 3,
   "notice": "2 working days"
  },
  {
   "slot": "D",
   "date": "2026-11-09",
   "open": "Mon-Sat 06:00-13:00",
   "lead_time_h": "96",
   "capacity_left": "4",
   "notice": "5 working days"
  },
  {
   "slot": "E",
   "date": "2026-11-10",
   "open": "09:00-11:30",
   "lead_time_h": 48,
   "capacity_left": 1,
   "notice": "1 working day"
  }
 ],
 "irrelevant": {
  "uiTheme": "light",
  "colWidth": 14
 },
 "notes": "Candidate asked by email on 27 Oct whether the non-UK licence exception applies to his licence. Panel secretary has not yet confirmed this, and diary holds are provisional until 16:00 on the working day before each slot."
}
```

**q1 [score / compare]** Rate the length of the wait between the licence arriving and the medical clearance being recorded, from the compliance checker's point of view.  
  `0` = Brief: under 24 hours; `1` = Short: at least 24 hours but under 72 hours; `2` = Moderate: at least 72 hours but under 122 hours; `3` = Long: 122 hours or more  
  gold: {"0": 0.0175, "1": 0.0375, "2": 0.9075, "3": 0.0375}  · agreement 4/4 · check: open · time_gap value 120.0 hours edges [24.0, 72.0, 122.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate how complete the supervisor endorsement is, as a proportion of the signatures required, from the compliance checker's point of view.  
  `0` = Minimal: under 20%; `1` = Partial: at least 20% but under 40%; `2` = Substantial: at least 40% but under 55%; `3` = Near complete: 55% or more  
  gold: {"0": 0.0148, "1": 0.0237, "2": 0.0415, "3": 0.92}  · agreement 4/4 · check: settled · share value 77.5 percent edges [20.0, 40.0, 55.0] (far)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / compare]** The medical clearance is recorded after the five-working-day response deadline has expired.  
  `true` = The clearance date is later than the deadline obtained by counting the working days from the clock start.; `false` = The clearance date is on or before that deadline.  
  gold: {"true": 0.08, "false": 0.92}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Once the exception clause is checked, what is the position on the signature requirement for this candidate's endorsement?  
  `not_endorsed` = The full signature requirement applies and has not been met.; `requirement_waived` = The exception removes the signature requirement.; `undetermined` = The exception's applicability is not confirmed, so the outcome cannot be fixed.  
  gold: {"not_endorsed": 0.0709, "requirement_waived": 0.0091, "undetermined": 0.92}  · agreement 3/4 · check: settled · adjusted  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / compare]** Which is the earliest practical slot that has capacity, follows the medical clearance, and whose opening window fits a full early shift plus the load-test dwell time?  
  `slot_a` = The first slot listed; `slot_b` = The second slot listed; `slot_c` = The third slot listed; `slot_d` = The fourth slot listed; `slot_e` = The fifth slot listed  
  gold: {"slot_a": 0.026, "slot_b": 0.014, "slot_c": 0.92, "slot_d": 0.022, "slot_e": 0.018}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q6 [choice / infer]** If the booking is made on 5 November, which is the earliest slot with capacity that meets both its lead time and its working-day notice?  
  `slot_a` = The first slot listed; `slot_b` = The second slot listed; `slot_c` = The third slot listed; `slot_d` = The fourth slot listed; `slot_e` = The fifth slot listed  
  gold: {"slot_a": 0.011, "slot_b": 0.0083, "slot_c": 0.0303, "slot_d": 0.0303, "slot_e": 0.9201}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0261  ·  car park enforcement  ·  chat log  ·  decider: the appeals clerk  ·  target: mixed

```
Chat log: Riverside MSCP, Site 14 (appeal PCN-448213)

09:12 Dana Whitcombe: Morning Priya. Appeal on PCN-448213 says the pay machine on Level 2 was out of order on 14 Oct. Can you confirm?
09:15 Priya Raval: L2-PM3 logged faulty 08:30 on 16 Oct, engineer attended 17 Oct. Nothing recorded for the 14th.
09:18 Tom Berrow: I was on L2 about 14:40 that day and that machine took my card. Printed a receipt.
09:21 Dana Whitcombe: Terminal log shows £3.60 paid 14:05 on L2-PM3. ANPR entry 13:52:07, exit 15:31:55. Tariff £2.40/hr, grace 15 min after expiry. PCN issued 15:49.
09:24 Priya Raval: Quarter figures: 9 barrier faults logged against 4,512 cycles. Three appeals still open on this site: £3.60, £8.00 and £2.80.
09:31 Tom Berrow: Barrier repair quotes in.
- Ostrow Barrier Services: PL cover £2m, 24h callout, £385 plus £60 parts surcharge.
- Kettering Access: not on maintainer scheme, 20h callout, £340.
- Fenmoor Systems: PL £5m, scheme accredited, 36h callout, £350 less 10% if booked before 31 Oct, minimum charge £200.
- Brackley Gates: 31 miles, £395 flat, call-out fee £45.
- Ellery Automation: PL £5m, scheme accredited, 24h callout, 18 miles, £410 plus VAT, callout waived over £300.
09:38 Priya Raval: Fine by me. Book Ellery for Thursday. Dana, attach the terminal log to the appeal file.
```

**q1 [score / infer]** Rate how far the driver's stay exceeded what was paid for, from the appeals clerk's point of view, applying the tariff, payment and grace rule to the recorded times.  
  `0` = Within_paid_time: the vehicle left before the paid period ended; `1` = Within_grace: the paid period had ended but the vehicle left inside the grace allowance; `2` = Beyond_grace: the vehicle left after the grace allowance had also ended; `3` = Unpaid: no payment covering the stay was recorded  
  gold: {"0": 0.5375, "1": 0.375, "2": 0.0425, "3": 0.045}  · agreement 3/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [noul / compare]** The vehicle left the car park before the penalty notice was issued.  
  `true` = The recorded exit time is earlier than the time the penalty notice was issued.; `false` = The recorded exit time is the same as or later than the time the penalty notice was issued.  
  gold: {"true": 0.92, "false": 0.08}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [choice / infer]** Which single repair firm meets every condition: scheme accredited, public liability cover of at least £5m, callout within 24 hours, and under 20 miles away?  
  `ostrow` = Ostrow Barrier Services; `fenmoor` = Fenmoor Systems; `brackley` = Brackley Gates; `ellery` = Ellery Automation  
  gold: {"ostrow": 0.0209, "fenmoor": 0.0383, "brackley": 0.0209, "ellery": 0.9199}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Booking today, which firm's barrier repair costs least once its own surcharge, discount, minimum or fee is applied (ignoring VAT)?  
  `ostrow` = Ostrow Barrier Services; `fenmoor` = Fenmoor Systems; `brackley` = Brackley Gates; `ellery` = Ellery Automation  
  gold: {"ostrow": 0.0145, "fenmoor": 0.9201, "brackley": 0.0236, "ellery": 0.0418}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0547  ·  energy supplier  ·  system record  ·  decider: a billing agent  ·  target: mostly clear

```json
{
 "record_id": "BIL-CUST-004471",
 "export_ts": "2026-10-29T08:14:52Z",
 "source_system": "TidewaterBill v5.2.1",
 "account_ref": "ACC-20093-KV",
 "customer": {
  "cust_name": "Harrowgate Veg Packing Ltd",
  "contactPerson": "Dilys Okonkwo-Reyes",
  "cust_type": "SME_NONDOM",
  "vat_reg_no": "GB 284 1109 37"
 },
 "supply_site": {
  "siteId": "SITE-EF-04",
  "mpan_core": "1900 2274 8813 5",
  "postcode": "LS14 6QR",
  "meter_type": "HH_SMART",
  "peak_kva_est": "roughly 42"
 },
 "tariff": {
  "tariffCode": "BUS-FIX-24M-v3",
  "unit_rate_p_kwh": "21.84",
  "standing_chg_p_day": "38.10",
  "contract_end": "2027-03-31",
  "early_exit_fee_gbp": null,
  "exitFeeNote": "Fee waived where account has been on fixed term 24 full months"
 },
 "readings": {
  "period_from": "2026-09-01",
  "period_to": "2026-09-30",
  "kwh_total": "18642",
  "band_limit_kwh": 20000,
  "prev_read_kwh": "503118",
  "curr_read_kwh": "521760"
 },
 "quality_scores": [
  "88",
  "91",
  "84"
 ],
 "alt_quotes": [
  {
   "alt_code": "ALT-A",
   "unit_rate_p_kwh": "22.15",
   "discount_pct": "3",
   "min_spend_gbp": null,
   "fee_gbp": "0"
  },
  {
   "alt_code": "ALT-B",
   "unit_rate_p_kwh": "21.40",
   "discount_pct": null,
   "min_spend_gbp": "3000",
   "fee_gbp": "45"
  },
  {
   "alt_code": "ALT-C",
   "unit_rate_p_kwh": "20.95",
   "discount_pct": "0",
   "surcharge_p_day": "12.50",
   "fee_gbp": "0"
  },
  {
   "alt_code": "ALT-D",
   "unit_rate_p_kwh": "22.60",
   "discount_pct": "5",
   "min_spend_gbp": "2500",
   "fee_gbp": null
  }
 ],
 "site_rows": [
  {
   "site": "SITE-EF-04",
   "kwh": "18642",
   "cost_gbp": "4187.66"
  },
  {
   "site": "SITE-EF-07",
   "kwh": "9120",
   "cost_gbp": "2286.14",
   "standing_days": "30"
  },
  {
   "site": "SITE-EF-09",
   "kwh": "5614",
   "cost_gbp": "1517.90",
   "standing_days": "30"
  },
  {
   "site": "SITE-EF-11",
   "kwh": "12876",
   "cost_gbp": "3152.00",
   "standing_days": "30"
  },
  {
   "site": "SITE-EF-12",
   "kwh": "7300",
   "cost_gbp": "1868.42",
   "standing_days": "28"
  }
 ],
 "billing": {
  "invoice_no": "INV-2026-09-88213",
  "gross_gbp": "4187.66",
  "net_gbp": "3493.05",
  "vat_gbp": "694.61",
  "due_date": "2026-10-21",
  "status": "OVERDUE_1",
  "dd_flag": "N"
 },
 "notes": "Customer queried September usage after a site survey and asked whether the 20,000 kWh band still applies to the fixed rate. Adjustment request logged as BC-7712, not yet actioned. Customer has been told a reply is due by early November.",
 "misc_legacy_code": "X7",
 "ext_ref_old": "HVP-LEG-0082",
 "print_batch": "PB-2026-10-B",
 "created_by": "svc_import"
}
```

**q1 [score / compare]** Rate how much headroom the customer's September consumption at the site leaves below the stated fixed-rate band limit, from the billing agent's point of view.  
  `0` = Negligible: less than 250 kWh below the limit; `1` = Small: at least 250 kWh but less than 700 kWh below the limit; `2` = Moderate: at least 700 kWh but less than 1,400 kWh below the limit; `3` = Large: at least 1,400 kWh but less than 3,000 kWh below the limit; `4` = Very large: 3,000 kWh or more below the limit  
  gold: {"0": 0.0143, "1": 0.0229, "2": 0.9199, "3": 0.0343, "4": 0.0086}  · agreement 4/4 · check: settled · difference value 1358.0 kWh edges [250.0, 700.0, 1400.0, 3000.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / judge]** Rate the overall data quality of this account record, based on the average of its quality scores, from the billing agent's point of view.  
  `0` = Poor: average below 70; `1` = Fair: average at least 70 but below 80; `2` = Good: average at least 80 but below 88; `3` = Excellent: average of 88 or more  
  gold: {"0": 0.0075, "1": 0.0225, "2": 0.9325, "3": 0.0375}  · agreement 4/4 · check: not_checked · average value 87.67 points edges [70.0, 80.0, 88.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [choice / infer]** Assuming the standing charge is the same everywhere, which alternative quote would cost least for September's usage once its own discount, surcharge, minimum spend and fee are applied?  
  `alt_a` = The first alternative quote is cheapest after its adjustments.; `alt_b` = The second alternative quote is cheapest after its adjustments.; `alt_c` = The third alternative quote is cheapest after its adjustments.; `alt_d` = The fourth alternative quote is cheapest after its adjustments.  
  gold: {"alt_a": 0.0343, "alt_b": 0.0171, "alt_c": 0.92, "alt_d": 0.0286}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Among the four other sites on the group account, which one has the highest cost per kWh for the period?  
  `site_07` = The second listed other site has the highest cost per kWh.; `site_09` = The third listed other site has the highest cost per kWh.; `site_11` = The fourth listed other site has the highest cost per kWh.; `site_12` = The fifth listed other site has the highest cost per kWh.  
  gold: {"site_07": 0.0246, "site_09": 0.92, "site_11": 0.0246, "site_12": 0.0308}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0419  ·  charity grants  ·  system record  ·  decider: the grants officer  ·  target: mostly clear

```json
{
 "rec_id": "GA-2026-0412",
 "Programme": "Community Spaces Fund, round 7",
 "status_code": "SUBMITTED",
 "windowCloseAt": "2026-10-31 00:00",
 "portal_log_ts": "2026-10-31 00:02:09",
 "applicant": {
  "org_name": "Tollbridge Community Kitchen CIO",
  "charity_no": "1187340",
  "lead_contact": {
   "name": "Priya Ostrowska",
   "tel": null,
   "email_addr": "p.ostrowska@tollbridgekitchen.example"
  }
 },
 "request": {
  "amount_requested_gbp": 84500,
  "revised_amount_gbp": "76200",
  "revision_log": [
   {
    "rev": 2,
    "field": "amount_requested_gbp",
    "value": "76200",
    "by": "applicant",
    "at": "2026-10-30 21:14:55"
   }
  ],
  "project_months": "18",
  "premises_floor_area_m2": "212"
 },
 "support": {
  "signatures_collected": 31,
  "signatures_required": 40,
  "letters_attached": 2,
  "ref_letters": [
   {
    "ref_no": "RL-88",
    "from": "Dunmere Ward Councillor"
   },
   {
    "ref_no": "RL-91",
    "from": null
   }
  ]
 },
 "criteria": {
  "min_capacity_persons": 60,
  "max_rent_pcm_gbp": "2200",
  "min_lease_yrs": 5,
  "step_free_required": true
 },
 "premises_options": [
  {
   "opt_id": "P1",
   "address": "Unit 4, Wharf Yard, Dunmere",
   "rent_pcm_gbp": "2100",
   "lease_yrs": 7,
   "step_free": true,
   "capacity_persons": 48
  },
  {
   "opt_id": "P2",
   "address": "7 Gaol Lane, Dunmere",
   "rent_pcm_gbp": "2350",
   "lease_yrs": 10,
   "step_free": true,
   "capacity_persons": 72
  },
  {
   "opt_id": "P3",
   "address": "Former Parcel Office, Station Rd",
   "rent_pcm_gbp": "2180",
   "lease_yrs": 5,
   "step_free": true,
   "capacity_persons": 64
  },
  {
   "opt_id": "P4",
   "address": "Hollins Annex, Mill Street",
   "rent_pcm_gbp": "1990",
   "lease_yrs": 3,
   "step_free": true,
   "capacity_persons": 80
  },
  {
   "opt_id": "P5",
   "address": "Chapel Hall, Vicar's Row",
   "rent_pcm_gbp": "2000",
   "lease_yrs": 8,
   "step_free": false,
   "capacity_persons": 90
  }
 ],
 "ui_theme": "teal",
 "legacy_form_v": "3.1",
 "print_batch": null,
 "assessor_ref": null,
 "notes": "Applicant emailed on 2026-10-30 at 21:14 to revise the request following a trustee meeting, and the revised figure has been entered in the revision log. Heads of terms for premises P3 were attached by the applicant, with the lease length still to be confirmed in writing. The signature sheet was scanned separately and has not yet been checked against the portal count."
}
```

**q1 [score / compare]** Rate how complete the applicant's collected community signatures are against the number the foundation requires, from the grants officer's point of view, using the portal count.  
  `0` = Minimal: less than 40% of the required signatures; `1` = Low: at least 40% but less than 60%; `2` = Moderate: at least 60% but less than 70%; `3` = Substantial: at least 70% but less than 90%; `4` = Full: at least 90% of the required signatures  
  gold: {"0": 0.0042, "1": 0.0063, "2": 0.0421, "3": 0.92, "4": 0.0274}  · agreement 4/4 · check: settled · share value 77.5 percent edges [40.0, 60.0, 70.0, 90.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / infer]** Rate how confident the grants officer can be that the applicant's third-listed premises option meets every stated premises criterion, given the criteria and the notes.  
  `0` = Fails: at least one criterion is clearly breached; `1` = Doubtful: no clear breach but a criterion is probably unmet; `2` = Probable: all criteria appear met on the figures, but one item awaits written confirmation; `3` = Certain: all criteria met and all evidence confirmed  
  gold: {"0": 0.0102, "1": 0.0391, "2": 0.9201, "3": 0.0306}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [score / judge]** Rate how fully the supporting evidence (signatures and referee letters) satisfies the foundation's requirements, from the grants officer's point of view.  
  `0` = Absent: no usable supporting evidence; `1` = Weak: evidence largely missing or unusable; `2` = Partial: some evidence usable but a stated requirement is unmet or unverified; `3` = Nearly complete: only minor verification outstanding; `4` = Complete: all requirements met and verified  
  gold: {"0": 0.015, "1": 0.125, "2": 0.8075, "3": 0.05, "4": 0.0025}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Which single premises option meets every stated criterion on capacity, rent, lease length and step-free access?  
  `p1` = The first listed premises option; `p2` = The second listed premises option; `p3` = The third listed premises option; `p4` = The fourth listed premises option; `p5` = The fifth listed premises option  
  gold: {"p1": 0.0342, "p2": 0.0143, "p3": 0.92, "p4": 0.0186, "p5": 0.0129}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0314  ·  college admissions  ·  chat log  ·  decider: the admissions officer  ·  target: mostly debatable

```
ADM-2291 Admissions Office chat log, 29/10/2026

08:47 Priya Lakhani: Morning. Applicant AP-3307 (Dylan Okafor), Plumbing L2: referee form signature date is blank. Can't file without it.
08:49 Ben Oduya: Chasing the referee. Open-day minibus log: out 22:40 on 27/10, back 06:15 on 28/10. Mileage claim 212 mi, which rate do I use?
08:52 Priya Lakhani: Finance say 0.45 per mile, but hold it until they confirm.
08:55 Ben Oduya: AP-3307 practical scores: 62, 71, 58. Kit box weighs 2.3 kg (5.1 lb) per spec sheet.
09:01 Priya Lakhani: Catering placement hosts, need one by Friday. Conditions: 10 mi or less, DBS valid, liability £5m or more, Mon–Fri available.
- Crane & Brook Kitchens: 9 mi, DBS valid, liability £5m, Mon–Fri
- Harbour Bistro: 4 mi, DBS valid, liability £2m, Mon–Fri
- Westfield Pantry: 12 mi, DBS expired 03/2026, liability £5m, Mon–Fri
- Oakmere Hotel: 7 mi, DBS valid, liability £5m, weekends only
09:06 Ben Oduya: Panel interview slots for AP-3307, 72 h notice rule applies:
Mon 02/11 14:00, room B2 (capacity 8, 6 booked)
Tue 03/11 09:30, room C1 (capacity 4, 4 booked)
Thu 05/11 11:00, room B2 (capacity 8, 5 booked)
09:09 Priya Lakhani: Thanks. Lunch order for the open day is 14 portions at 3.80 each, can you add it to the budget sheet?
```

**q1 [score / compare]** Rate how long the open-day minibus was away on its overnight trip, from the admissions officer's point of view.  
  `0` = Short: under 240 minutes; `1` = Medium: at least 240 minutes but under 720 minutes; `2` = Long: 720 minutes or more  
  gold: {"0": 0.04, "1": 0.92, "2": 0.04}  · agreement 4/4 · check: settled · time_gap value 455.0 minutes edges [240.0, 720.0] (far)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the applicant's overall practical performance, from the admissions officer's point of view, using the mean of the applicant's practical marks.  
  `0` = Weak: mean below 60; `1` = Fair: mean at least 60 but below 70; `2` = Good: mean at least 70 but below 80; `3` = Excellent: mean 80 or more  
  gold: {"0": 0.04, "1": 0.92, "2": 0.03, "3": 0.01}  · agreement 4/4 · check: settled · average value 63.67 marks edges [60.0, 70.0, 80.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [choice / compare]** Which proposed interview slot is the least full, as a share of room capacity already booked?  
  `mon_slot` = The first proposed slot has the lowest booked share; `tue_slot` = The second proposed slot has the lowest booked share; `thu_slot` = The third proposed slot has the lowest booked share  
  gold: {"mon_slot": 0.0747, "tue_slot": 0.0053, "thu_slot": 0.92}  · agreement 3/4 · check: settled · adjusted  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Which catering host meets every stated placement condition?  
  `crane_brook` = The first listed host meets all conditions; `other_host` = One of the other listed hosts meets all conditions; `no_host` = No listed host meets every condition  
  gold: {"crane_brook": 0.92, "other_host": 0.032, "no_host": 0.048}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / judge]** What is the earliest sensible way to proceed with the applicant's panel interview, given the notice rule, room availability and the unsigned referee form?  
  `mon_slot` = Book the earliest slot, which has notice and space; `tue_slot` = Book the second slot; `thu_slot` = Book the last slot; `no_slot_feasible` = No slot satisfies the notice rule and capacity; `hold_for_form` = Book nothing until the missing signature is obtained  
  gold: {"mon_slot": 0.6225, "tue_slot": 0.0225, "thu_slot": 0.05, "no_slot_feasible": 0.02, "hold_for_form": 0.285}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0864  ·  pharmacy dispensing  ·  email thread  ·  decider: the dispensing technician  ·  target: mostly clear

```
From: Tomasz Wirth
Sent: Wed 28 Oct 2026 16:40
To: Priya Nandakumar
Subject: Returns review – October counts

Priya,

Unclaimed owing items against scripts dispensed 1–27 Oct:

Westgate 11 / 298
Ashby Road 7 / 176
Cale Street 9 / 240
Mill Green 5 / 131

Mrs Okafor's owing item at Ashby Road was ready Tuesday 20 October and is still on the shelf.

Tomasz Wirth
Dispensing Technician
Hollins Road Pharmacy | 0161 555 0142

> From: Priya Nandakumar
> Sent: Wed 28 Oct 2026 17:05
> To: Tomasz Wirth
> Subject: RE: Returns review – October counts
>
> Tomasz,
>
> Cale Street figure is wrong. Till report shows 264 dispensed, not 240. Please correct before the run.
>
> DSP-07 section 4, as it stands:
> 1. Owing items unclaimed 10 days after ready date are returned to wholesaler.
> 2. Care-home residents' items are held 21 days.
> 3. Where a signed owing slip is on file, hold 28 days from ready date.
> 4. Controlled drugs need pharmacist sign-off before return.
>
> Mrs Okafor's slip is dated 15/10 and is in the folder.
>
> Priya Nandakumar
> Dispensary Manager

From: Tomasz Wirth
Sent: Thu 29 Oct 2026 08:52
To: Priya Nandakumar
Subject: RE: Returns review – October counts

Priya,

Corrected: Cale Street 9 / 264. Revised sheet attached.

Mrs Okafor's item is still in bay C at Ashby Road, bag label 20/10. Fridge 2 at Westgate read 5.1 °C at 08:10 this morning.

Tomasz
```

**q1 [score / compare]** Rate the unclaimed owing-item rate at Ashby Road for 1–27 October (unclaimed items as a share of scripts dispensed), from the dispensing technician's viewpoint.  
  `0` = Low: below 2% of scripts dispensed; `1` = Moderate: at least 2% but below 4%; `2` = High: 4% or more of scripts dispensed  
  gold: {"0": 0.0295, "1": 0.92, "2": 0.0505}  · agreement 4/4 · check: settled · rate value 3.98 percent edges [2.0, 4.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate how much time remains before Mrs Okafor's owing item reaches the end of its applicable hold period, counted from today, from the technician's viewpoint.  
  `0` = Short: fewer than 10 days remaining; `1` = Medium: at least 10 but fewer than 20 days remaining; `2` = Long: at least 20 but fewer than 28 days remaining; `3` = Very long: 28 days or more remaining  
  gold: {"0": 0.085, "1": 0.8425, "2": 0.0525, "3": 0.02}  · agreement 4/4 · check: open · time_gap value 19.0 days edges [10.0, 20.0, 28.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [score / compare]** Rate the corrected unclaimed owing-item rate at Cale Street for 1–27 October (unclaimed items as a share of scripts dispensed), from the dispensing technician's viewpoint.  
  `0` = Low: below 2% of scripts dispensed; `1` = Elevated: at least 2% but below 3.5%; `2` = High: at least 3.5% but below 5%; `3` = Very high: 5% or more of scripts dispensed  
  gold: {"0": 0.0313, "1": 0.92, "2": 0.0383, "3": 0.0104}  · agreement 4/4 · check: settled · rate value 3.41 percent edges [2.0, 3.5, 5.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Using the corrected counts, which of these three branches has the highest rate of unclaimed owing items per script dispensed?  
  `westgate` = Westgate has the highest rate of the three; `cale_street` = Cale Street has the highest rate of the three; `mill_green` = Mill Green has the highest rate of the three  
  gold: {"westgate": 0.0552, "cale_street": 0.0248, "mill_green": 0.92}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** Under the return policy, what happens to Mrs Okafor's owing item today once the exception clauses are checked?  
  `return_now` = Return to the wholesaler today under the standard period; `hold_care_home` = Hold under the care-home extended period; `hold_longer_slip` = Hold under the longer period for a signed owing slip on file; `await_signoff` = Hold pending pharmacist sign-off before any return  
  gold: {"return_now": 0.0365, "hold_care_home": 0.0182, "hold_longer_slip": 0.92, "await_signoff": 0.0253}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q6 [noul / judge]** It is reasonable to leave Mrs Okafor's owing item on the shelf rather than return it today.  
  `true` = Leaving the item on the shelf is reasonable given the policy and its circumstances.; `false` = Leaving the item on the shelf is not reasonable; it should be returned or otherwise actioned today.  
  gold: {"true": 0.8725, "false": 0.1275}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0790  ·  walk-in clinic  ·  chat log  ·  decider: the triage nurse  ·  target: mixed

```
**Walk-in Triage Desk: Chat Log (channel #triage-front)**

**Fri 30 Oct 2026**

21:48 **Ines Vartanian (Reception):** Clinic closes at 22:00 but there's a mother in the waiting room with a boy, 4, temp she says is 39.2 on the thermometer at home. Do you want him through?

21:51 **Imogen Fairbrother (Triage RN):** Yes, bring them to room 2. Protocol TRI-7 cl. 4.2 applies to under-5s with temp ≥38.0°C, unless a GP review is recorded within the previous 72 hours, in which case Amber not Red.

21:53 **Ines Vartanian:** Mum says Dr Okafor saw him Wed 28th at the Elmfield surgery. Not sure it's on our system.

21:55 **Imogen Fairbrother:** Please check the shared record before I rely on that.

21:58 **Ines Vartanian:** Nothing on our system. Reg says the Elmfield letter is in the post.

22:04 **Tomasz Wierzbicki (Clinic Coordinator):** Interpreter needed for Mr Hussain in room 4 (Pashto). I've left a message with three agencies. Mr Hussain's weight on the scale was 71.4 kg, but his chart says 157 lb on the old sheet, so please reconcile.

**Sat 31 Oct 2026**

09:12 **Imogen Fairbrother:** Handover from Friday: boy in room 2 was re-triaged to Red at 23:40 after his temperature came back at 38.9, 39.1 and 38.4 on the three recheck readings. Still waiting on the Elmfield record.

**Sun 1 Nov 2026**

16:30 **Tomasz Wierzbicki:** Interpreter status for Mr Hussain. I checked four agencies against the Pashto/Urdu accreditation, DBS, arrival time within 60 min and rate ≤ £35/hr:
- Ferrous Language Services: DBS expired 14 Sept, rest fine.
- Civic Interpret Direct: £41/hr, rest fine.
- Northgate Linguists: Urdu only, no Pashto accreditation.
- Bellweather Interpreting: arrival 110 min, rest fine.
- Harrow Ridge Interpreting: accredited, DBS current, 35 min, £34/hr.

**Mon 2 Nov 2026**

08:15 **Ines Vartanian:** Shift hours for the cover rota this week: Tomasz 4h 30min Fri, 6h Sat, 3h 45min Sun. Can you confirm the week's total before payroll? Also Mr Hussain's weight is confirmed at 14.2 kg for the child's dose sheet, not the adult figure.

08:20 **Imogen Fairbrother:** Boy's Elmfield letter has arrived. Dr Okafor's review is dated 28 Oct, so cl. 4.2 gives Amber. Re-triaging now.
```

**q1 [score / compare]** Rate the average of the boy's three recheck temperatures on Friday night, from the triage nurse's point of view, as a level of fever.  
  `0` = Lower: average below 38.5°C; `1` = Intermediate: average at least 38.5°C but below 39.0°C; `2` = Higher: average 39.0°C or above  
  gold: {"0": 0.0337, "1": 0.92, "2": 0.0463}  · agreement 4/4 · check: settled · average value 38.8 °C edges [38.5, 39.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the total cover-rota hours worked by the clinic coordinator across the three listed days, from the triage nurse's point of view as the amount of cover needing payroll confirmation.  
  `0` = Minimal: under 8 hours; `1` = Low: at least 8 but under 12 hours; `2` = Moderate: at least 12 but under 14 hours; `3` = High: at least 14 but under 18 hours; `4` = Very high: 18 hours or more  
  gold: {"0": 0.0121, "1": 0.017, "2": 0.0315, "3": 0.92, "4": 0.0194}  · agreement 4/4 · check: settled · sum value 14.25 hours edges [8.0, 12.0, 14.0, 18.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [score / compare]** Rate the average hourly rate of the agencies that quoted a figure for the Pashto interpreter, from the triage nurse's point of view as cost level.  
  `0` = Cheap: average below £30/hr; `1` = Fair: average at least £30 but below £35/hr; `2` = Elevated: average at least £35 but below £40/hr; `3` = Expensive: average £40/hr or more  
  gold: {"0": 0.0225, "1": 0.0675, "2": 0.87, "3": 0.04}  · agreement 4/4 · check: open · average value 37.5 £/hr edges [30.0, 35.0, 40.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Which single Pashto-accredited agency meets every stated condition for Mr Hussain's interpreter: current DBS, arrival within 60 minutes, and rate within the hourly limit?  
  `ferrous_language` = Ferrous Language Services; `civic_interpret` = Civic Interpret Direct; `bellweather` = Bellweather Interpreting; `harrow_ridge` = Harrow Ridge Interpreting  
  gold: {"ferrous_language": 0.0321, "civic_interpret": 0.024, "bellweather": 0.024, "harrow_ridge": 0.9199}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0142  ·  software release  ·  system record  ·  decider: the on-call engineer  ·  target: mostly clear

```json
{
 "rel_id": "REL-2026-1187",
 "record_type": "release_change",
 "status": "pending_go_no_go",
 "svc_name": "edge-gateway",
 "changeRef": "CHG-44092",
 "deployed_build": "gw-5.14.3-rc2",
 "rollback_build": "gw-5.14.1",
 "owner": {
  "team": "Release Management",
  "oncall_handle": "rmt-oncall-b",
  "contact_ext": null
 },
 "window": {
  "start_utc": "2026-10-30T23:40:00Z",
  "end_utc": "2026-11-02T06:15:00Z",
  "freeze_exempt": false
 },
 "payload_size": {
  "value": 38.5,
  "unit": "MB"
 },
 "approx_sessions_at_cutover": "just under 2,100",
 "sites": [
  {
   "site_id": "LDN-E2",
   "err_5xx": "412",
   "requests_total": "9180240"
  },
  {
   "site_id": "MAN-E1",
   "err_5xx": "266",
   "requests_total": "5102877"
  },
  {
   "site_id": "EDB-E3",
   "err_5xx": "97",
   "requests_total": "1894320"
  },
  {
   "site_id": "CDF-E1",
   "err_5xx": "151",
   "requests_total": "2640015"
  },
  {
   "site_id": "BHM-E4",
   "err_5xx": "58",
   "requests_total": "1103390"
  }
 ],
 "policy": {
  "policy_ref": "RM-POL-7.3(b)",
  "rollback_threshold_5xx_pct": 0.5,
  "review_required": true
 },
 "ticket": {
  "opened_utc": "2026-10-29T16:20:00Z",
  "response_due_working_days": 5,
  "public_holiday_excluded": "2026-11-02",
  "due_date": "2026-11-06"
 },
 "bridge_cover_options": [
  {
   "opt": "A",
   "vendor": "Tallis Bridge Ops",
   "rate_gbp_per_hr": "85.00",
   "min_hours": 4,
   "weekend_surcharge_pct": "25",
   "setup_fee_gbp": "120"
  },
  {
   "opt": "B",
   "vendor": "Harrowgate Remote",
   "rate_gbp_per_hr": "72.50",
   "min_hours": 6,
   "prepaid_discount_pct": "10",
   "setup_fee_gbp": null
  },
  {
   "opt": "C",
   "vendor": "Quorum NOC",
   "rate_gbp_per_hr": "79.00",
   "min_hours": null,
   "night_surcharge_gbp_hr": "12",
   "setup_fee_gbp": "0"
  },
  {
   "opt": "D",
   "vendor": "Pellow Systems",
   "flat_gbp_per_window": "540",
   "included_hours": 8,
   "overage_gbp_per_hr": "95"
  },
  {
   "opt": "E",
   "vendor": "Sidcup Assure",
   "rate_gbp_per_hr": "68.00",
   "min_fee_gbp": "300",
   "amounts_ex_vat": true
  }
 ],
 "legacy_jira_sync": "pending",
 "printer_queue": null,
 "ui_colour_theme": "amber",
 "notes": "Canary on LDN-E2 showed a rise in 503 responses after the 22:00 deploy and was held at 10 percent traffic. The on-call engineer has not yet confirmed whether the MAN-E1 figures include the retry storm from 02:10. Bridge cover quotes are valid until 2026-11-03 and have not been accepted."
}
```

**q1 [score / compare]** Rate the overall 5xx error rate across all five sites combined, in errors per million requests, from the release engineer's point of view when weighing a rollback.  
  `0` = Minimal: below 20 errors per million requests; `1` = Low: at least 20 but below 50 errors per million requests; `2` = Moderate: at least 50 but below 100 errors per million requests; `3` = High: at least 100 but below 250 errors per million requests; `4` = Severe: 250 or more errors per million requests  
  gold: {"0": 0.0175, "1": 0.92, "2": 0.0475, "3": 0.01, "4": 0.005}  · agreement 4/4 · check: open · rate value 49.4 errors per million requests edges [20.0, 50.0, 100.0, 250.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the length of the change window, from its start to its end, as the on-call engineer must staff it.  
  `0` = Very short: less than 12 hours; `1` = Short: at least 12 but less than 24 hours; `2` = Medium: at least 24 but less than 36 hours; `3` = Long: at least 36 but less than 54 hours; `4` = Very long: 54 hours or more  
  gold: {"0": 0.0, "1": 0.0, "2": 0.0, "3": 0.08, "4": 0.92}  · agreement 4/4 · check: settled · time_gap value 54.58 hours edges [12.0, 24.0, 36.0, 54.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [choice / judge]** Which site should the on-call engineer investigate first, being the one with the highest 5xx error rate as a share of its own requests?  
  `ldn_e2` = The London site has the highest error share; `man_e1` = The Manchester site has the highest error share; `edb_e3` = The Edinburgh site has the highest error share; `cdf_e1` = The Cardiff site has the highest error share; `bhm_e4` = The Birmingham site has the highest error share  
  gold: {"ldn_e2": 0.0075, "man_e1": 0.055, "edb_e3": 0.015, "cdf_e1": 0.885, "bhm_e4": 0.0375}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** For a single 8-hour daytime bridge session on Saturday 31 October, prepaid where a discount exists and ignoring VAT, which cover option costs least?  
  `opt_a` = Tallis Bridge Ops after weekend surcharge and setup fee; `opt_b` = Harrowgate Remote after prepaid discount; `opt_c` = Quorum NOC at its hourly rate; `opt_d` = Pellow Systems flat fee with included hours; `opt_e` = Sidcup Assure at hourly rate or minimum fee  
  gold: {"opt_a": 0.01, "opt_b": 0.92, "opt_c": 0.015, "opt_d": 0.0325, "opt_e": 0.0225}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0990  ·  theatre box office  ·  policy extract and case note  ·  decider: the duty house manager  ·  target: mostly clear

```
HARLOW PLAIN REGIONAL THEATRE
Box Office Operations Manual, Section 7: Cancellation, Reschedule and Refund Procedure (Rev. 4, issued 12/03/2026)

7.1 A performance may be rescheduled only where the Duty House Manager (DHM) has confirmed a technical or safety reason in writing.
7.2 Reschedule offers must be sent to ticket holders not less than 10 working days before the new date.
7.3 Reschedule dates must fall within public opening hours (10:00 to 23:00) and within the seated capacity of the venue used.
7.4 Refunds for cancelled performances are calculated as face value plus booking fee, per order.
7.5 Exception: clause 7.2 does not apply where a patron has signed Form BO-14 accepting a substitute date and the form reached the box office at least 48 hours before the offer is issued. Forms must be countersigned by the DHM.
7.6 Studio holds not confirmed within 72 hours of placement are released automatically.

Case note BO/CN/2026/0417
Logged: Friday 30 October 2026, 23:40
Matinee of "The Glass Orchard" (Sat 7 November, 14:30, Main House) cancelled following flying bar fault. Safe working load recorded at 450 kg. 286 orders affected.
BO-14 forms returned to date: 31 (40 requested).
Refund lines on sample orders: £84.00 (order 88213), £37.50 (order 88240), £19.25 (order 88419).
Logged: Monday 2 November 2026, 09:15
Hold request placed for Studio, Tue 10 November 19:30. Studio capacity 120. Studio hold lapses if unconfirmed by 17:00 Thursday.
Alternative dates noted by staff:
- Sun 15 November, 16:00, Main House (10 working days' notice required)
- Thu 3 December, 14:30, Main House (lighting plot clash on Wed 2 December)
- Sat 28 November, 22:45, Main House (staff overtime approval needed 48 hours ahead)
- Mon 2 November, 10:00, Studio (no notice requirement if announced same day)
```

**q1 [score / infer]** Rate how freely the box office may offer the Sunday 15 November Main House date to ordinary ticket holders on Monday 2 November, from the duty house manager's viewpoint, under the manual's notice rule and its exception.  
  `0` = Barred: the rules forbid making the offer at all; `1` = Blocked: notice is too short and no exemption is available to the patron; `2` = Exempt only: notice is too short, but the offer is allowed to patrons with a valid, timely, countersigned substitute-date form; `3` = Open: every condition is met and the offer may go to everyone  
  gold: {"0": 0.035, "1": 0.4725, "2": 0.4275, "3": 0.065}  · agreement 2/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / judge]** Rate how urgent it is for the duty house manager to confirm the Studio hold, judged from the automatic release rule and the time of the case note.  
  `0` = Minimal: no confirmation is needed; `1` = Low: release is more than five days away; `2` = Moderate: release is at least two days but no more than five days away; `3` = High: release is less than two days away but not yet passed; `4` = Critical: release has already happened or is imminent  
  gold: {"0": 0.02, "1": 0.0825, "2": 0.71, "3": 0.165, "4": 0.0225}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / compare]** Fewer than ten working days separate an offer issued on Monday 2 November from the Sunday 15 November performance date.  
  `true` = The count of working days between the offer day and the performance date is below the required notice period.; `false` = The count of working days between the offer day and the performance date meets or exceeds the required notice period.  
  gold: {"true": 0.75, "false": 0.25}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Which is the earliest alternative date that meets every constraint, including notice, opening hours, capacity and clashes, for patrons without exemption forms?  
  `studio_2_nov` = The Studio slot on the first day, announced same day; `main_15_nov` = The Sunday afternoon Main House slot in mid-November; `main_28_nov` = The late-evening Saturday Main House slot at the end of November; `main_3_dec` = The Thursday afternoon Main House slot in early December  
  gold: {"studio_2_nov": 0.05, "main_15_nov": 0.0775, "main_28_nov": 0.5875, "main_3_dec": 0.285}  · agreement 3/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0410  ·  school office  ·  system record  ·  decider: the head of year  ·  target: mixed

```json
{
 "rec_id": "HOY9-0417",
 "rec_type": "yr_group_case_file",
 "school": {
  "name": "Hollinbrook Park Academy",
  "urn": "139482",
  "site_code": "HPA-S",
  "timezone": "Europe/London"
 },
 "year_group": "Y9",
 "head_of_year": {
  "staff_id": "S-2284",
  "surname": "Okonedo-Reid",
  "ext": 4417
 },
 "created_ts": "2026-10-19T08:42:11Z",
 "lastUpdated": "2026-10-27 16:05",
 "status": "open",
 "trip": {
  "trip_ref": "RES-26-09",
  "destination": "Llanfair Outdoor Centre",
  "coach_capacity_seats": 52,
  "pupils_booked": "47",
  "deposit_paid_gbp": "250.00",
  "trip_cost_gbp": 1840.5,
  "coach_op": null
 },
 "transport_routes": [
  {
   "route_code": "R1",
   "runs_operated": "38",
   "late_arrivals": "4",
   "avg_delay_min": 6
  },
  {
   "route_code": "R2",
   "runs_operated": "41",
   "late_arrivals": "9",
   "avg_delay_min": 11
  },
  {
   "route_code": "R3",
   "runs_operated": "29",
   "late_arrivals": "3",
   "avg_delay_min": null
  },
  {
   "route_code": "R4",
   "runs_operated": "44",
   "late_arrivals": "12",
   "avg_delay_min": 8
  },
  {
   "route_code": "R5",
   "runs_operated": "36",
   "late_arrivals": "5",
   "avg_delay_min": 4
  }
 ],
 "supervision": {
  "period": "2026-09",
  "staff_hours_logged": 61.5,
  "unit_note": "hrs"
 },
 "parent_comms": {
  "messages_sent": 214,
  "complaints_logged": "6",
  "last_complaint_ts": "2026-10-23T14:10:00Z"
 },
 "lateness": {
  "lates_recorded": 38,
  "total_late_mins": "1140",
  "pupils_affected": 22
 },
 "response": {
  "window_basis": "working_days_excl_bank_hols",
  "window_wd": 7,
  "responded_by": null,
  "response_due": "2026-11-03"
 },
 "roll_count": {
  "initial": 186,
  "revised": 168,
  "source": "MIS_export_0927"
 },
 "equipment": {
  "coach_bag_weight_lb": "62",
  "tent_kit_kg": 14.2
 },
 "ui_theme": "light",
 "export_batch": "B-0031",
 "legacy_flag": null,
 "notes": "Parent complaints relate mainly to R2 and R4 late arrivals during September. The trip deposit balance is still outstanding for three families. The roll figure above was re-checked against the register after the initial export."
}
```

**q1 [score / infer]** Rate how urgent the response deadline is for the head of year today, given the stated working-day rule and the deadline recorded, with no response yet made.  
  `0` = Relaxed: more than five working days remain before the deadline; `1` = Approaching: three to five working days remain before the deadline; `2` = Pressing: fewer than three working days remain, but the deadline has not passed; `3` = Overdue: the deadline has already passed without a response  
  gold: {"0": 0.0275, "1": 0.5875, "2": 0.2325, "3": 0.1525}  · agreement 3/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the size of the year group's confirmed roll, from the head of year's point of view, using the stated roll figure after the register re-check.  
  `0` = Small: under 142.5 pupils; `1` = Medium: 142.5 to under 205 pupils; `2` = Large: 205 pupils or more  
  gold: {"0": 0.04, "1": 0.92, "2": 0.04}  · agreement 4/4 · check: settled · stated value 168.0 pupils edges [142.5, 205.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / infer]** The response deadline recorded is later than the end of the stated working-day window counted from the case file's creation date.  
  `true` = The recorded deadline falls after the date the stated number of working days (excluding bank holidays) from creation would end.; `false` = The recorded deadline falls on or before the date the stated working-day window from creation would end.  
  gold: {"true": 0.92, "false": 0.08}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Among the routes with a recorded average delay, which has the highest proportion of runs arriving late?  
  `route_r1` = The first route has the highest late-arrival proportion.; `route_r2` = The second route has the highest late-arrival proportion.; `route_r4` = The fourth route has the highest late-arrival proportion.; `route_r5` = The fifth route has the highest late-arrival proportion.  
  gold: {"route_r1": 0.0108, "route_r2": 0.0454, "route_r4": 0.92, "route_r5": 0.0238}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0337  ·  public library  ·  form submission  ·  decider: the fines and fees desk  ·  target: mixed

```
HARLOW CENTRAL LIBRARY SERVICE
Fines, Fees & Waivers Desk: Case Submission Form
Form ref: FFW-2026-0418    Status: SUBMITTED    Submitted: 27/10/2026 14:52

Section A: Applicant
Applicant name: Mr Dariusz Wojcik
Library card no.: HCL-40817732
Home branch: Eastfield Branch
Contact phone: 07700 900 418
Email: d.wojcik@mailbox-example.co.uk
Date of birth: 14/03/1971

Section B: Item(s) concerned
Item barcode: 31002004871190
Title: The Salt Road (hardback)
Date due: 02/10/2026
Date returned: 
Return method: Drop box, Eastfield
Item condition on return: Spine damage noted by staff (see comments)
Replacement cost quoted by supplier: £18.50
Overdue days (as recorded): 27

Section C: Fine calculation
Daily overdue rate: £0.25
Fine capped at: £10.00
Fine accrued to date (system): £6.75
Processing fee: £2.50
Amount requested for waiver: £9.25
Waiver type requested: [ ] Partial  [X] Full  [ ] Hardship
Previous waivers in last 12 months: 1 (ref FFW-2026-0102, 14/05/2026)
Reservation hold on account: Yes (ref RSV-88104, Eastfield, expired 16/10/2026)

Section D: Reservation details
Reservation ref: RSV-88104
Item requested: The Glass Orchard (paperback)
Date placed: 06/09/2026
Ready for collection: 09/10/2026
Collection deadline: 16/10/2026
Collected: No
Hold extended: [ ] Yes  [ ] No
Nearest alternative branch: Westmoor Branch (collection by 19/11/2026 if requested)

Section E: Supporting evidence
Receipt attached: [ ] Yes  [X] No
Doctor's letter attached: [ ] Yes  [ ] No
Other: Photo of item spine (uploaded 27/10/2026, file IMG_4471.jpg)

Section F: Staff use only
Assessed by: 
Date assessed: 
Decision: 
Authorised by: 
Reference of decision letter: 

Section G: Applicant comments
I returned The Salt Road on 4 October at the Eastfield drop box, a day after it was due... actually it was the 4th I'm fairly sure. The spine was already loose when I took it out of the bag, I did not do that. I was at my sister's in Leeds for most of the second half of September, which is why it was late. I could not collect The Glass Orchard as I was not back until the 15th, I rang the branch on the 13th and was told the hold would still be there. Please can someone look at this as I am on a fixed income and the reservation is the only thing I was waiting for.

```

**q1 [score / compare]** Rate, from the desk's point of view, how much the system's overdue fine exceeds the fine that would apply if the applicant's own stated return date were accepted.  
  `0` = Negligible: less than £2.00; `1` = Small: at least £2.00 but below £5.50; `2` = Large: at least £5.50 but below £8.00; `3` = Very large: £8.00 or more  
  gold: {"0": 0.0147, "1": 0.0376, "2": 0.9199, "3": 0.0278}  · agreement 4/4 · check: settled · difference value 6.25 GBP edges [2.0, 5.5, 8.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate, from the desk's point of view, the average size of the three amounts the applicant faces on the item: the accrued fine, the processing fee and the replacement cost.  
  `0` = Low: below £5.00 on average; `1` = Moderate: at least £5.00 but below £15.00 on average; `2` = High: £15.00 or more on average  
  gold: {"0": 0.0451, "1": 0.92, "2": 0.0349}  · agreement 4/4 · check: settled · average value 9.25 GBP edges [5.0, 15.0] (far)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / infer]** The reservation hold had already expired by the date the applicant says he got back from Leeds.  
  `true` = The collection deadline fell before the date the applicant says he returned.; `false` = The collection deadline fell on or after the date the applicant says he returned.  
  gold: {"true": 0.045, "false": 0.955}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / judge]** Which is the earliest route by which the applicant can still obtain the reserved book on the document's evidence?  
  `eastfield_extension` = Collect at the home branch under an extended hold.; `westmoor_branch` = Collect at the alternative branch within its stated window.; `no_route` = No route to collection is supported by the document.  
  gold: {"eastfield_extension": 0.075, "westmoor_branch": 0.8, "no_route": 0.125}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / compare]** Which scenario gives the highest total charge to the applicant once the damaged item's replacement cost is included?  
  `replacement_only` = Replacement cost alone, with no fine or fee.; `system_fine_plus_replacement` = System fine, processing fee and replacement cost together.; `stated_return_plus_replacement` = Fine recalculated from applicant's return date, plus fee and replacement cost.  
  gold: {"replacement_only": 0.0282, "system_fine_plus_replacement": 0.92, "stated_return_plus_replacement": 0.0518}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0393  ·  freight forwarding  ·  chat log  ·  decider: the bookings clerk  ·  target: mostly clear

```
Chat log – Bookings desk / Harbourline Freight Forwarding (Ops channel #bookings-uk)
Exported 2026-10-29

09:02:14 Priya Lakhani: morning all. Ref HLF-44817 (Tarnow Steel, sea LCL Felixstowe to Gdansk) – shipper has sent a revised packing list, can someone look before cut-off? Their cut-off for the box is 17:00 today, not tomorrow, I checked twice.
09:04:51 Dariusz Wojcik: ok reading now. Honestly the list is a mess, they've put pallets in one line and cartons in another and the weights are a bit all over the place. Will try to make sense of it after the Kettering run is booked, which is a pain because the driver wanted to swap to the 14:30 slot and I said I'd check with the depot first, and the depot manager Sanjana is off until Monday so I've left her a voicemail on the landline that may or may not get listened to.
09:07:30 Priya Lakhani: fine. What's the gross on the revised list?
09:09:02 Dariusz Wojcik: Line 1, 4 pallets at 412 kg each. Line 2, 11 cartons at 18.5 kg. Line 3 is the loose drums, 3 drums at 61 lb each (they've written it in pounds, not kilos, which is why I'm paranoid). So I'm not sure if the 61 is the drum or the drum pack, will ask.
09:11:40 Priya Lakhani: ok. Also the earlier version said line 1 was 3 pallets at 380 kg. Obviously the revised one supersedes that.
09:12:55 Dariusz Wojcik: yes, the 380 was the old quote, ignore it.
10:38:09 Gareth Lindqvist: unrelated, does anyone have the spare key for the cage at Bay 4? The forklift keeper has gone missing again.
10:39:20 Priya Lakhani: try the hook behind the door in the office. Not sure about the cage.
10:41:03 Gareth Lindqvist: found it, thanks. It was in the fire extinguisher box, which is not where it goes.
13:52:47 Dariusz Wojcik: Ok, the shipper's Monday collection time for the Kettering road leg was 06:30, now they've asked for 05:45 start. Also the sea booking gate closes 17:00 today and the last Felixstowe pick-up email I can see is logged 17:01:47 yesterday, so I'm not sure what's happening there. I'll ring the carrier.
13:55:10 Priya Lakhani: ring them and get the 17:00 confirmed in writing please.

```

**q1 [score / compare]** Rate the total gross weight of the revised consignment, in kilograms, from the bookings clerk's point of view. Add all three revised lines, converting pounds to kilograms.  
  `0` = Light: under 1500 kg; `1` = Medium: at least 1500 kg but below 1950 kg; `2` = Heavy: at least 1950 kg but below 2400 kg; `3` = Very heavy: 2400 kg or more  
  gold: {"0": 0.02, "1": 0.9, "2": 0.07, "3": 0.01}  · agreement 4/4 · check: open · sum value 1934.5 kg edges [1500.0, 1950.0, 2400.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate how long the gap is, from the bookings clerk's point of view, between the last logged Felixstowe pick-up email and the closing of today's sea booking gate.  
  `0` = Brief: under 720 minutes; `1` = Moderate: at least 720 minutes but under 1440 minutes; `2` = Long: at least 1440 minutes but under 2160 minutes; `3` = Very long: 2160 minutes or more  
  gold: {"0": 0.0229, "1": 0.92, "2": 0.048, "3": 0.0091}  · agreement 4/4 · check: settled · time_gap value 1438.22 minutes edges [720.0, 1440.0, 2160.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / judge]** The logged Felixstowe pick-up email gives the clerk enough assurance that the consignment will make today's sea booking gate.  
  `true` = The email record is enough to rely on the box making today's gate without further confirmation.; `false` = The email record is not enough, so further confirmation is needed before relying on today's gate.  
  gold: {"true": 0.035, "false": 0.965}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Which line of the revised packing list has the lowest total weight in kilograms?  
  `pallets` = The palletised line has the lowest total weight.; `cartons` = The cartons line has the lowest total weight.; `drums` = The loose drums line has the lowest total weight once converted to kilograms.; `tie` = Two or more lines have the same lowest total weight.  
  gold: {"pallets": 0.0139, "cartons": 0.0452, "drums": 0.92, "tie": 0.0209}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0596  ·  venue hire  ·  form submission  ·  decider: the bookings coordinator  ·  target: mixed

```
HARROWGATE MILL EVENTS — VENUE BOOKING REQUEST
Form ref: HM-BR-2026-0417    Submitted: 29/10/2026 16:42 (online)

Organisation: Pennine Logistics Forum
Contact name: Dilys Okonedo
Contact phone: 14/11/2026
Email: d.okonedo@penninelf.example
Event type: Conference
Event date: Sat 14/11/2026    Set-up from: Fri 13/11/2026
Start time: 09:30    Finish time: 22:15
Expected attendance: 180 persons
Hall required: Hall B
Hire package selected: Package C (full day, bar)
Discount code:
Purchase order no.:

Hire line items:
  Projector and screen: £285.00
  Staffing (2 x 8 hrs): £312.00
  Cloakroom attendant: £96.00
  Hall B hire: 
Deposit due: 5 working days from receipt (weekends and public holidays excluded)
Finance sign-off required (Y/N): 

Catering shortlist (tick if met):
  Supplier          Halal   Free 14/11   Liability cover   Per head
  Crestline Foods    Y        Y           £2m               £26.50
  Oakhurst Kitchen   N        Y           £5m               £24.00
  Bramley & Vine     Y        N           £5m               £27.20
  Tallis Catering    Y        Y           £5m               £29.10
  Quill Hospitality  Y        Y           £10m              £25.80
Supplier selected:

Comments: Dietary sheet to follow by email. Set-up on Friday is for the staging crew only and should not be charged at the Saturday rate. Please note the treasurer has asked that the deposit is paid from the Forum account and not the Trust account.
```

**q1 [score / compare]** Rate the total of the priced extras already itemised on this request (excluding the blank hall hire), from the venue coordinator's point of view.  
  `0` = Minimal: under £400; `1` = Modest: at least £400 but below £700; `2` = Substantial: at least £700 but below £1,000; `3` = Heavy: £1,000 or more  
  gold: {"0": 0.0311, "1": 0.92, "2": 0.0311, "3": 0.0178}  · agreement 4/4 · check: settled · sum value 693.0 GBP edges [400.0, 700.0, 1000.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the lead time, from the coordinator's point of view, between the request being submitted and the event's start time.  
  `0` = Short: less than 7 days; `1` = Moderate: at least 7 days but less than 28 days; `2` = Ample: 28 days or more  
  gold: {"0": 0.044, "1": 0.92, "2": 0.036}  · agreement 4/4 · check: settled · time_gap value 15.7 days edges [7.0, 28.0] (far)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [score / infer]** Rate the combined cost, from the coordinator's point of view, of the itemised extras plus catering for the full expected attendance if Quill Hospitality is chosen (hall hire excluded).  
  `0` = Very low: under £3,000; `1` = Low: at least £3,000 but below £4,500; `2` = Medium: at least £4,500 but below £6,000; `3` = High: at least £6,000 but below £7,500; `4` = Very high: £7,500 or more  
  gold: {"0": 0.0128, "1": 0.0256, "2": 0.92, "3": 0.0288, "4": 0.0128}  · agreement 4/4 · check: settled · sum value 5337.0 GBP edges [3000.0, 4500.0, 6000.0, 7500.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Which single caterer is halal, free on the event date and carries at least £10m liability cover?  
  `crestline_foods` = Crestline Foods meets every condition; `bramley_vine` = Bramley & Vine meets every condition; `tallis_catering` = Tallis Catering meets every condition; `quill_hospitality` = Quill Hospitality meets every condition  
  gold: {"crestline_foods": 0.0267, "bramley_vine": 0.0267, "tallis_catering": 0.0267, "quill_hospitality": 0.9199}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / judge]** With the dietary sheet still to come, which caterer is cheapest for the full attendance among those that are halal and free on the event date?  
  `crestline_foods` = Crestline Foods gives the lowest total among eligible caterers; `oakhurst_kitchen` = Oakhurst Kitchen gives the lowest total among eligible caterers; `bramley_vine` = Bramley & Vine gives the lowest total among eligible caterers; `quill_hospitality` = Quill Hospitality gives the lowest total among eligible caterers  
  gold: {"crestline_foods": 0.035, "oakhurst_kitchen": 0.015, "bramley_vine": 0.0175, "quill_hospitality": 0.9325}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0367  ·  gym membership  ·  incident report  ·  decider: the club manager  ·  target: mixed

```
INCIDENT REPORT: MEMBERSHIP RECORDS AND BILLING
Report ref: IR-2026-1147
Site: Ferndale Fitness, Harrowgate Road branch (Site code HG-04)
Reported by: Tomasz Wierzbicki, Duty Supervisor
Date of report: 30/10/2026
Incident window: 28/10/2026 21:40 to 29/10/2026 07:15

1. Timeline (times from access control log, unless stated)
21:40 28/10 Last staff member (T. Wierzbicki) closes front desk. Night cleaner badge in at 21:52.
22:05 28/10 Membership system batch "MBR_DD_NIGHTLY" starts on server FF-HG04-DB.
23:58 28/10 Batch still running; progress at 61%.
00:14 29/10 Batch reports "TIMEOUT - retry queued", no alert raised to on-call.
00:31 29/10 Direct debit file HGDD_2610 generated with 412 records (expected 438).
07:15 29/10 Front desk opened by R. Adeyemi; first member query logged at 07:22.

2. Witness remarks
Night cleaner (K. Lindqvist, by phone 29/10 09:10): "Lights were on in the back office at midnight, I didn't go in. Nobody I saw."
R. Adeyemi: "Screen said retry queued. I assumed it would run again overnight like it did last month."

3. Billing figures
Standard monthly direct debit per member: £34.99.
Family plan per member: £27.50 (subject to minimum of 3 members).
Failed records were recalculated manually on 29/10 at 10:00 and the file total corrected to £14,932.46 (initially recorded as £15,314.88 in the summary of the 00:31 run; corrected figure supersedes).

4. Policy reference
Clause 4.2 Billing Continuity: Where a nightly batch does not complete before 00:00, the duty supervisor must hold the affected file. Exception 4.2(b): where the batch failure is confirmed as non-recoverable by the systems team before 06:00, the file may be released without hold.
Systems team confirmation received 29/10 05:48 (ticket SYS-7731), stated as "recoverable: NO".

5. Immediate actions
29/10 07:30 File HGDD_2610 released to bank without hold (see 4.2(b)).
29/10 10:00 Manual recalculation of 26 failed records.
29/10 11:20 Ticket SYS-7731 reopened by systems team; status now "recoverable: UNDER REVIEW".

Report prepared by T. Wierzbicki. Review pending.
```

**q1 [score / compare]** Rate how prolonged the nightly batch run was, from the club manager's view: the time from the batch starting to the batch reporting its timeout.  
  `0` = Brief: under 60 minutes; `1` = Short: at least 60 but under 100 minutes; `2` = Moderate: at least 100 but under 150 minutes; `3` = Long: at least 150 but under 240 minutes; `4` = Very long: 240 minutes or more  
  gold: {"0": 0.0119, "1": 0.0267, "2": 0.9199, "3": 0.0326, "4": 0.0089}  · agreement 4/4 · check: settled · time_gap value 129.0 minutes edges [60.0, 100.0, 150.0, 240.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the size of the billing correction, from the club manager's view: the amount by which the initially recorded file total exceeded the corrected total.  
  `0` = Minor: under £100; `1` = Noticeable: at least £100 but under £250; `2` = Substantial: at least £250 but under £500; `3` = Severe: £500 or more  
  gold: {"0": 0.0114, "1": 0.0434, "2": 0.9201, "3": 0.0251}  · agreement 4/4 · check: settled · difference value 382.42 GBP edges [100.0, 250.0, 500.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [score / compare]** Rate how long the direct debit file stood released to the bank before the systems team reopened the ticket, from the club manager's view.  
  `0` = Very short: under 60 minutes; `1` = Short: at least 60 but under 120 minutes; `2` = Moderate: at least 120 but under 180 minutes; `3` = Long: at least 180 but under 240 minutes; `4` = Very long: 240 minutes or more  
  gold: {"0": 0.0062, "1": 0.0123, "2": 0.0431, "3": 0.9199, "4": 0.0185}  · agreement 4/4 · check: settled · time_gap value 230.0 minutes edges [60.0, 120.0, 180.0, 240.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** For a household of five people joining, which arrangement costs least per month once the family plan rate and its minimum are applied, while covering all five?  
  `all_standard` = All five join individually at the standard rate.; `family_of_five` = All five join together on the family plan.; `three_family_two_standard` = Three on the family plan and two at the standard rate.; `four_family_one_standard` = Four on the family plan and one at the standard rate.; `three_family_two_family_separate` = Three on a family plan and the other two on a second family plan below the minimum.  
  gold: {"all_standard": 0.0165, "family_of_five": 0.92, "three_family_two_standard": 0.0188, "four_family_one_standard": 0.0188, "three_family_two_family_separate": 0.0259}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** Under the billing continuity clause and its exception, what was the position when the file was released to the bank at 07:30?  
  `release_permitted` = The exception applied at the time, so release without hold was allowed.; `hold_required` = The exception was not met, so the file had to be held.; `hold_required_after_reopening` = Later reopening of the confirmation means a hold was required.; `clause_not_triggered` = The clause did not apply because the batch was not affected.  
  gold: {"release_permitted": 0.9201, "hold_required": 0.0283, "hold_required_after_reopening": 0.0383, "clause_not_triggered": 0.0133}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q6 [choice / judge]** What monthly total would a two-member household most plausibly be charged, given the family plan's stated minimum?  
  `standard_both` = Both are charged the standard rate.; `family_both` = Both are charged the family rate regardless of the minimum.; `one_each` = One is charged each rate.; `not_accepted` = The household cannot be enrolled or billed at all.; `unclear` = The document does not allow a reasonable commitment.  
  gold: {"standard_both": 0.725, "family_both": 0.0225, "one_each": 0.0325, "not_accepted": 0.0375, "unclear": 0.1825}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0711  ·  college admissions  ·  policy extract and case note  ·  decider: an appeals panel member  ·  target: mostly clear

```
ASHDOWN PARK COLLEGE OF TECHNICAL SKILLS
Admissions Policy ADM-14: Late Enrolment and Re-Admission Appeals
Version 3.2, effective 1 September 2026

1. Scope
1.1 This policy applies to applicants refused re-admission or late enrolment on grounds of attendance or prior assessment.
1.2 Appeals must be lodged within 10 working days of the decision letter.

2. Attendance
2.1 Applicants must have attended at least 80% of scheduled sessions in the previous course to be considered for re-admission.
2.2 Attendance below this threshold is grounds for refusal unless clause 3.1 applies.

3. Exceptions
3.1 Where documented medical or caring circumstances affected attendance, the panel may apply a threshold of 70%, provided dated evidence is submitted with the appeal.
3.2 Evidence must relate to the period of absence.

4. Reassessment
4.1 Applicants with prior assessment readings averaging below 55 marks may request reassessment.
4.2 Reassessment fee is £45.00 per unit, waived under clause 3.1.

CASE NOTE CN-2026-0912
Applicant: Rhiannon Oduya (ADM/26/4471)
Course: Level 3 Diploma in Electrical Installation
Decision letter issued 14 October 2026. Appeal lodged 21 October 2026.

Attendance: 159 of 200 scheduled sessions attended (prior year). GP note dated 3 March 2026 submitted, covering absence in weeks 4 to 9 of term.
Unit 3 practical readings: 52, 58, 61 marks.

Reassessment slots offered:
S1 Tue 3 Nov 2026, 09:00-10:30, Room B14. Notice: 5 working days. Capacity 12, booked 11.
S2 Thu 5 Nov 2026, 13:00-14:30, Workshop 2. Notice: 10 working days. Capacity 8, booked 8.
S3 Mon 9 Nov 2026, 09:30-11:00, Room B14. Notice: 10 working days. Centre hours 08:30-17:00.
S4 Fri 20 Nov 2026, 10:00-11:30, Room B14. Notice: 10 working days. Capacity 12, booked 12.

Re-enrolment options:
A. Standard re-enrolment £180.00. 5% discount if paid by 30 October 2026. £20.00 card surcharge.
B. Part-time route £95.00 per module, minimum of 3 modules. No discount.
C. Employer-sponsored £240.00 flat. £25.00 administration fee.
D. Clause 3.1 route: tuition £0.00. Non-refundable registration fee £30.00.
E. Three instalments totalling £210.00, with 8% instalment surcharge.

Panel notes: Applicant contacted admissions by phone 27 October 2026. Callback requested.
```

**q1 [score / infer]** Rate how far the applicant's appeal succeeds on attendance grounds under the policy, from the appeals panel's point of view.  
  `0` = Out_of_time: the appeal was lodged after the permitted period, so it cannot be heard; `1` = Refused_no_exception: attendance is below the standard threshold and no exception can be applied; `2` = Refused_below_lower: attendance is below even the reduced threshold, so the exception does not help; `3` = Upheld_by_exception: attendance is below the standard threshold but meets the reduced threshold with qualifying evidence; `4` = Upheld_outright: attendance meets the standard threshold without needing any exception  
  gold: {"0": 0.0175, "1": 0.08, "2": 0.035, "3": 0.825, "4": 0.0425}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the applicant's average practical reading in the prior unit, from the appeals panel's point of view.  
  `0` = Weak: average below 50 marks; `1` = Low: average at least 50 but below 56 marks; `2` = Moderate: average at least 56 but below 65 marks; `3` = Strong: average of 65 marks or more  
  gold: {"0": 0.0114, "1": 0.0533, "2": 0.9201, "3": 0.0152}  · agreement 4/4 · check: settled · average value 57.0 marks edges [50.0, 56.0, 65.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [choice / infer]** Booking on 29 October 2026 and counting only full working days after that date as notice, which is the earliest reassessment slot that has enough notice, space and fits centre hours?  
  `s1` = The first slot offered; `s2` = The second slot offered; `s3` = The third slot offered; `s4` = The fourth slot offered; `none` = No offered slot meets every constraint  
  gold: {"s1": 0.02, "s2": 0.02, "s3": 0.0233, "s4": 0.0167, "none": 0.92}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Paying by card on 29 October 2026 for a standard module count, which of these four routes costs least after its own discount, surcharge, minimum or fee?  
  `standard` = Standard re-enrolment route; `part_time` = Part-time per-module route; `employer` = Employer-sponsored route; `instalments` = Three-instalment route  
  gold: {"standard": 0.9201, "part_time": 0.0187, "employer": 0.0221, "instalments": 0.0391}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / judge]** Assuming the panel accepts the medical evidence as adequate and she pays on 2 November 2026 by card, which route costs her least overall?  
  `standard` = Standard re-enrolment route; `employer` = Employer-sponsored route; `exception_route` = Route available under the medical exception; `instalments` = Three-instalment route  
  gold: {"standard": 0.0325, "employer": 0.02, "exception_route": 0.92, "instalments": 0.0275}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-1090  ·  public library  ·  voicemail and CRM note  ·  decider: the fines and fees desk  ·  target: mixed

```
VOICEMAIL TRANSCRIPT
Line: Central Library main desk extension 4417
Received: Tue 27 Oct 2026, 16:52
Caller: Mrs D. Okonkwo-Hale (reservations customer, card ending 3381)
Duration: 2 min 14 sec

"Hi, um, yes, it's Denise Hale, I'm ringing about the fine on my account, the one for the, the large print atlas, the one I put a hold on at Eastside and then, well, I didn't go in to collect it, which I know, I know, and then it came back on the Thursday, the nineteenth I think, or was it the twentieth, I've got the slip somewhere. Anyway the thing is the letter says three pounds forty and I thought the cap was lower than that, because my neighbour had something similar and hers was capped at two pounds ten, I think, but she's at Westbrook so it might be different. I was also a bit poorly that week, I had the chest infection, the one that took about nine days off me, and I did phone on the Monday to say I couldn't get in but I think I got the answerphone, and I left a message with the reference, which I think was RSV-20417 or maybe 20471, I'm not sure. Sorry, I'm rambling. If you could ring me back on 01632 960 118, or just leave a message, that would be marvellous. I'm usually in after twelve on weekdays. Thanks very much. Bye."

CRM NOTE
Ref: CRM-88215
Logged by: A. Pemberton (Fines & Fees desk)
Date: 28/10/2026 09:14
Linked record: Reservation RSV-20471 (Eastside branch, hold placed 06/10/2026)

Customer returned voicemail of 27/10 re overdue reservation charge. Customer states charge quoted as £3.40; believes cap is lower. Customer states she phoned branch on 12/10/2026 to report non-collection due to illness (chest infection, approx. 9 days absence). Customer unsure whether reference is RSV-20417 or RSV-20471; linked record used. Customer states item returned to shelf 19/10 or 20/10.

Notes: Callback number on voicemail differs from number held on account (held: 01632 960 081). Customer asked for callback after 12:00 weekdays. No callback made yet. Charge ledger shows £3.40 (13 days x £0.20 + £0.80 admin). Neighbour reference (Westbrook) not verified against this account.
```

**q1 [score / compare]** Rate the all-in daily cost of the overdue reservation charge, as felt by the customer: the total charge divided by the days it covers.  
  `0` = Low: below £0.20 per day; `1` = Moderate: at least £0.20 but below £0.32 per day; `2` = High: at least £0.32 but below £0.45 per day; `3` = Severe: £0.45 per day or more  
  gold: {"0": 0.0206, "1": 0.9199, "2": 0.0526, "3": 0.0069}  · agreement 4/4 · check: settled · rate value 0.2615 £ per day edges [0.2, 0.32, 0.45] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate how much of the total overdue charge is made up by the flat administration element, from the fines desk's point of view.  
  `0` = Minor: below 10% of the charge; `1` = Moderate: at least 10% but below 24%; `2` = Substantial: at least 24% but below 40%; `3` = Dominant: 40% or more  
  gold: {"0": 0.0157, "1": 0.9201, "2": 0.0571, "3": 0.0071}  · agreement 4/4 · check: settled · share value 23.53 percent edges [10.0, 24.0, 40.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / infer]** The customer's description of the item returning to the shelf on a Thursday the nineteenth fits the 2026 calendar.  
  `true` = The weekday and date she gives match each other in October 2026.; `false` = The weekday and date she gives do not match in October 2026.  
  gold: {"true": 0.08, "false": 0.92}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Which reading of the facts gives the highest total charge for the customer?  
  `return_19th_full_rate` = Item returned on the earlier date, charged at the ledger rate with the admin element.; `return_20th_full_rate` = Item returned on the later date, charged at the ledger rate with the admin element.; `neighbour_cap` = The lower cap the customer believes applies is used instead.; `return_19th_admin_waived` = Earlier date, with the admin element removed.  
  gold: {"return_19th_full_rate": 0.265, "return_20th_full_rate": 0.6475, "neighbour_cap": 0.0475, "return_19th_admin_waived": 0.04}  · agreement 3/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / judge]** Which outcome would cost the customer least if applied in full?  
  `ledger_charge` = The charge stands as currently recorded.; `neighbour_cap` = The lower cap the customer believes applies is used.; `illness_days_waived` = Daily fees for her stated days of illness are waived, admin element kept.; `admin_waived` = Only the flat administration element is removed.  
  gold: {"ledger_charge": 0.02, "neighbour_cap": 0.19, "illness_days_waived": 0.7375, "admin_waived": 0.0525}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0264  ·  parcel locker network  ·  system record  ·  decider: the overdue-collection rule  ·  target: mostly debatable

```json
{
 "export_id": "pkx-exp-20261029-0913",
 "record_type": "parcel_hold",
 "recordId": "PH-2026-0048213",
 "Parcel": {
  "parcel_ref": "ZX7-448213-GB",
  "weight_kg": "17.4",
  "weight_lb": "38.4",
  "carrier_code": "NRV",
  "dims_mm": {
   "l": 420,
   "w": 310,
   "h": 260
  }
 },
 "locker": {
  "lockerId": "LK-14B",
  "site_id": "SITE-07",
  "compartment_height_mm": 450,
  "max_load_kg": 15
 },
 "deposit": {
  "deposited_at": "2026-10-27T18:05:00+00:00",
  "deposit_channel": "app-qr",
  "depositor_ref": "cust-88130"
 },
 "hold": {
  "free_hold_expires": "2026-11-03T23:59:59+00:00",
  "collected_at": null,
  "overdue_flag": "N",
  "override_by": null,
  "fee_gbp": "0.00"
 },
 "site_throughput": [
  {
   "site": "SITE-02",
   "collected": 118,
   "open_hours": "11.0"
  },
  {
   "site": "SITE-07",
   "collected": 96,
   "open_min": 660
  },
  {
   "site": "SITE-11",
   "collected": 141,
   "open_hours": "13.5"
  },
  {
   "site": "SITE-04",
   "collected": 77,
   "open_min": 450
  },
  {
   "site": "SITE-09",
   "collected": "102",
   "open_hours": 9.25
  }
 ],
 "alt_collection_points": {
  "min_accept_kg": 20,
  "saturday_open_required": true,
  "max_distance_km": 2.5,
  "min_free_lockers": 3,
  "candidates": [
   {
    "cp": "CP-A",
    "accepts_kg": 25,
    "saturday_open": true,
    "distance_km": 1.8,
    "free_lockers": 0
   },
   {
    "cp": "CP-B",
    "accepts_kg": 18,
    "saturday_open": true,
    "distance_km": 2.2,
    "free_lockers": 4
   },
   {
    "cp": "CP-C",
    "accepts_kg": 22,
    "saturday_open": false,
    "distance_km": 1.2,
    "free_lockers": 5
   },
   {
    "cp": "CP-D",
    "accepts_kg": 30,
    "saturday_open": true,
    "distance_km": 3.4,
    "free_lockers": 6
   },
   {
    "cp": "CP-E",
    "accepts_kg": 21,
    "saturday_open": true,
    "distance_km": 2,
    "free_lockers": 3
   }
  ]
 },
 "notify": {
  "sms_sent": "2026-10-27T18:06:12Z",
  "email_bounce": null,
  "retry_count": "2"
 },
 "ui_theme": "amber-2",
 "export_batch_tag": "nightly-ops-v3",
 "last_modified_by": "svc_locker_sync",
 "notes": "Customer requested the hold be extended before the free period ends, but the request has not been logged against the record. Locker LK-14B reported a door sensor fault on 2026-10-28 and was taken out of rotation until re-certified. The parcel was not moved to the alternative collection point list at deposit."
}
```

**q1 [score / compare]** Rate how far the parcel's weight exceeds the locker's maximum load, from the operations team's point of view.  
  `0` = Within_limit: below 0 kg over the limit (parcel is lighter than the limit); `1` = Marginal: at least 0 kg but below 1 kg over; `2` = Modest: at least 1 kg but below 3 kg over; `3` = Substantial: at least 3 kg but below 5 kg over; `4` = Severe: 5 kg or more over  
  gold: {"0": 0.0155, "1": 0.0232, "2": 0.92, "3": 0.0284, "4": 0.0129}  · agreement 4/4 · check: settled · difference value 2.4 kg edges [0.0, 1.0, 3.0, 5.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the length of the free hold period granted to this parcel, measured from deposit to the end of the free period, from the operations team's point of view.  
  `0` = Brief: less than 2 days; `1` = Short: at least 2 days but less than 5 days; `2` = Standard: at least 5 days but less than 7.5 days; `3` = Extended: 7.5 days or more  
  gold: {"0": 0.0178, "1": 0.0237, "2": 0.92, "3": 0.0385}  · agreement 4/4 · check: settled · time_gap value 7.25 days edges [2.0, 5.0, 7.5] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [choice / compare]** Which site has the highest number of collections per open hour?  
  `site_02` = The first listed site has the highest rate; `site_09` = The fifth listed site has the highest rate; `site_11` = The third listed site has the highest rate; `other_site` = A site not named in the other options has the highest rate  
  gold: {"site_02": 0.0372, "site_09": 0.92, "site_11": 0.0279, "other_site": 0.0149}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Which single alternative collection point meets every stated requirement for this parcel?  
  `cp_a` = The first candidate meets every requirement; `cp_d` = The fourth candidate meets every requirement; `cp_e` = The fifth candidate meets every requirement; `other_or_none` = A different candidate, or none, meets every requirement  
  gold: {"cp_a": 0.02, "cp_d": 0.02, "cp_e": 0.92, "other_or_none": 0.04}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [noul / judge]** The parcel is likely to be collected by the customer before the free hold period ends.  
  `true` = Collection within the free period is more likely than not given the locker's status and the record.; `false` = Collection within the free period is not likely, or is no more likely than not, given the locker's status and the record.  
  gold: {"true": 0.2375, "false": 0.7625}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0945  ·  veterinary practice  ·  system record  ·  decider: the practice receptionist  ·  target: mostly clear

```json
{
 "export_id": "VXP-261029-0442",
 "exported_at": "2026-10-29T08:14:52Z",
 "sys_ver": "6.4.1-rc2",
 "patient": {
  "pt_no": 8817,
  "name": "Biscuit",
  "species": "canine",
  "breed": "Cocker Spaniel x",
  "dob": "2019-03-11",
  "weight_kg": "12.4",
  "microchip": null
 },
 "owner": {
  "ownerRef": "OWN-20931",
  "full_name": "Hannah Okafor-Reid",
  "mob": "07700 900417",
  "email": null,
  "membership": {
   "plan_code": "MPL-PLUS",
   "status": "active",
   "valid_to": "2027-01-31"
  }
 },
 "case": {
  "case_no": "CS-26-1193",
  "vet_init": "RLM",
  "ward": "K2",
  "status_cd": "PEND_AUTH"
 },
 "procedure": {
  "booked_for": "2026-10-27",
  "recheck_dt": "2026-11-03T09:00",
  "sx_code": "SX-014",
  "desc": "TPLO, right hind"
 },
 "estimate": {
  "est_ref": "EST-4471",
  "lines": [
   {
    "code": "SX-014",
    "amt": "1180.00"
   },
   {
    "code": "AN-02",
    "amt": "214.50"
   },
   {
    "code": "RX-07",
    "amt": "96.00"
   }
  ],
  "subtotal": null,
  "vat_applied": false
 },
 "alternatives": [
  {
   "opt": "A",
   "label": "Pay in full at discharge",
   "price": "1490.50",
   "disc_pct": "5",
   "min_dep": null
  },
  {
   "opt": "B",
   "label": "Three monthly instalments",
   "price": "1490.50",
   "surch_pct": "3.5",
   "min_dep": "300.00"
  },
  {
   "opt": "C",
   "label": "Insurer direct, excess applies",
   "excess": "250.00",
   "cover_pct": "80",
   "admin_fee": "22.00"
  },
  {
   "opt": "D",
   "label": "Deferred finance, 6 months",
   "price": "1490.50",
   "arr_fee": "45",
   "min_spend": "1200.00"
  },
  {
   "opt": "E",
   "label": "Charity grant referral",
   "grant": "400.00",
   "assess_fee": "35.00"
  }
 ],
 "pricing_rule": {
  "rule_id": "PR-7",
  "clauses": [
   "1. Discounts apply to the estimate subtotal only.",
   "2. Surcharges apply to instalment plans and are calculated on the discounted balance.",
   "3. Minimum deposit is due before surgery.",
   "4. Except where the owner holds an active MPL-PLUS membership on the procedure date, in which case clause 2 is waived."
  ]
 },
 "deposit": {
  "held": "75.00",
  "unit": "GBP",
  "taken_by": "RLM"
 },
 "notes": "Owner rang at 17:40 on Friday to say the insurer has not replied and she may want to pay part by card, then changed her mind twice on the phone. Her membership renewal letter was posted to the wrong address, so the plan_code above may be out of date on the day, and she asked for it to be checked against the portal before anything is confirmed. She also wants the recheck moved if the 3 November slot clashes with her shift."
}
```

**q1 [score / compare]** Rate the size of the total of the estimate lines for the planned surgery, anaesthesia and medication, from the owner's point of view, before any discount, surcharge or fee.  
  `0` = Small: less than 1,000 pounds; `1` = Moderate: at least 1,000 pounds but less than 1,500 pounds; `2` = Large: at least 1,500 pounds but less than 2,000 pounds; `3` = Very large: 2,000 pounds or more  
  gold: {"0": 0.0235, "1": 0.92, "2": 0.0424, "3": 0.0141}  · agreement 4/4 · check: settled · sum value 1490.5 GBP edges [1000.0, 1500.0, 2000.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate how much notice the practice has before the recheck, measured from the time this record was exported, from the receptionist's point of view.  
  `0` = Immediate: less than 2 days; `1` = Short: at least 2 days but less than 7 days; `2` = Ample: at least 7 days but less than 14 days; `3` = Long: 14 days or more  
  gold: {"0": 0.0246, "1": 0.92, "2": 0.0431, "3": 0.0123}  · agreement 4/4 · check: settled · time_gap value 5.03 days edges [2.0, 7.0, 14.0] (far)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [choice / compare]** Which payment alternative would cost the owner least once its own discount, surcharge, fee, excess or grant is applied?  
  `option_a` = Pay in full at discharge with the percentage discount; `option_b` = Three monthly instalments, with surcharge as the rule allows; `option_c` = Insurer direct, owner pays excess, uncovered share and admin fee; `option_d` = Deferred finance with its arrangement fee; `option_e` = Charity grant referral net of grant, plus assessment fee  
  gold: {"option_a": 0.02, "option_b": 0.0175, "option_c": 0.8875, "option_d": 0.02, "option_e": 0.055}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** What happens to the instalment surcharge under plan B once the pricing rule's exception clause is checked against the owner's membership?  
  `on_discounted_balance` = Surcharge is charged on the discounted balance; `on_full_subtotal` = Surcharge is charged on the undiscounted subtotal; `waived` = Surcharge is waived by the exception; `plan_unavailable` = Plan cannot be offered because of the deposit condition; `unresolved` = Document gives no basis to decide the surcharge  
  gold: {"on_discounted_balance": 0.05, "on_full_subtotal": 0.0225, "waived": 0.4575, "plan_unavailable": 0.02, "unresolved": 0.45}  · agreement 3/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [noul / judge]** The recorded membership status is reliable enough to confirm the surcharge waiver to the owner without first checking the portal.  
  `true` = The record can be relied on as it stands, so the waiver can be confirmed straight away.; `false` = The record may be out of date or unverified, so the waiver should not be confirmed until it is checked.  
  gold: {"true": 0.0775, "false": 0.9225}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0273  ·  wedding venue  ·  voicemail and CRM note  ·  decider: the venue owner  ·  target: mixed

```
HOLLIN PARK BARNS - VOICEMAIL TRANSCRIPT
Received: Thu 29/10/2026 17:52  Line: 01423 556018  Caller: Gareth Pulley (07700 900412)  Length: 2 min 14 sec

"Hi, yeah, it's Gareth Pulley, the Pulley-Osei wedding, booking HB-2611. Sorry, I've been trying since Tuesday and it's always the answerphone, anyway. So the marquee firm you put us onto, Tallis Canopy, they've come back with a number and I don't really follow it. They said four hundred and ten quid for the hire, but then there's a weekend thing, a surcharge, sort of... I think it's about a hundred and twenty? Dev reckons it's a fee for the drive over, I don't know. And the marquee's twelve metres, not ten, I checked with my dad. The bar has to finish at half one because of the licence, that's what the venue said on the phone in September, and the setup crew are coming in at twenty to five on the Friday, the thirtieth, and the dancing's supposed to be done by quarter past one on the Saturday morning, which, is that the same night? Also the deposit, you said two thousand, but the invoice came through for two thousand three hundred and fifteen, it's on my desk now. Could you ring me back, I'm around after seven. Thanks, bye."

CRM NOTE
29/10/2026 18:20  Author: JM  Ref: HB-2611  Status: Open

Caller left voicemail re marquee hire and invoice query. Spoke to Tallis Canopy earlier, they were quoting for a 10 m marquee, will re-check size. Options gathered so far:
- Tallis Canopy: £410/day, weekend surcharge 25%, min 2 days, delivery £95
- Fenwick Marquees: £465 flat for 2 days, 10% off if booked by 31/10, delivery £60
- Ashgrove Event Tents: £380/day, weekend surcharge £120 flat, late collection £45
- Brackley Hire: £520 all-in, 5% off if deposit paid by 30/10, min 3 days
- In-house tent: £350/day, no surcharge, needs 15 kVA generator hire at £140

Caterer shortlist checked against: FHRS 5, PLI £5m+, available Fri 30/10 and Sat 31/10, 140+ guests.
- Brinsley & Co: capacity 120
- Oakhurst Kitchen: FHRS 4
- Wren Table: PLI £2m
- Marlow Fare: Sat 31/10 only
- Sable & Rowe: all four met

Times per booking form: setup 16:30 Fri 30/10, bar and music end 01:00 Sat 31/10. Deposit recorded as £2,000 (paid 14/09). Invoice INV-40927 issued £2,315.00, due 12/11. Caller to be called back after 19:00.
```

**q1 [score / compare]** Rate the size of the shortfall between the deposit the venue recorded as paid and the amount the client's invoice demands, from the venue owner's point of view.  
  `0` = Negligible: under £50; `1` = Small: at least £50 but below £150; `2` = Modest: at least £150 but below £280; `3` = Notable: at least £280 but below £500; `4` = Large: £500 or more  
  gold: {"0": 0.0067, "1": 0.0083, "2": 0.0467, "3": 0.92, "4": 0.0183}  · agreement 4/4 · check: settled · difference value 315.0 GBP edges [50.0, 150.0, 280.0, 500.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the length of the booking-form working window, from the setup crew's start until the bar and music end, from the venue owner's point of view.  
  `0` = Short: under 420 minutes; `1` = Medium: at least 420 minutes but under 600 minutes; `2` = Long: 600 minutes or more  
  gold: {"0": 0.0381, "1": 0.92, "2": 0.0419}  · agreement 4/4 · check: settled · time_gap value 510.0 minutes edges [420.0, 600.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / judge]** The bar's finish time is still unconfirmed, because the client's account conflicts with the venue's own booking record.  
  `true` = The client's stated finish time differs from the booking record, so the finish time remains uncertain and needs confirming.; `false` = The client's stated finish time matches the booking record, or the conflict is not enough to leave it uncertain.  
  gold: {"true": 0.8425, "false": 0.1575}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** For a Friday-to-Saturday event, which marquee option costs least once its own discount, surcharge, minimum or fee is applied?  
  `fenwick` = Fenwick Marquees with its early-booking discount and delivery charge; `brackley` = Brackley Hire with its deposit discount, subject to its minimum hire period; `ashgrove` = Ashgrove Event Tents with its flat weekend surcharge and any collection fee; `in_house` = The in-house tent with its generator hire  
  gold: {"fenwick": 0.7875, "brackley": 0.12, "ashgrove": 0.0375, "in_house": 0.055}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** Which single caterer meets every stated condition on the shortlist checks?  
  `oakhurst` = Oakhurst Kitchen; `marlow` = Marlow Fare; `sable_rowe` = Sable & Rowe  
  gold: {"oakhurst": 0.04, "marlow": 0.04, "sable_rowe": 0.92}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0687  ·  gym membership  ·  system record  ·  decider: the direct-debit retry process  ·  target: mixed

```json
{
 "MemberRef": "FLX-448207",
 "member_name": "Tamsin Okonedo-Reyes",
 "siteCode": "BRM-02",
 "joined": "2023-03-14",
 "plan": {
  "planId": "CORE-M",
  "monthly_fee_gbp": "24.99",
  "addOns": [
   "crèche",
   null
  ],
  "contract_end": null
 },
 "DirectDebit": {
  "mandate_ref": "DD-88310-FX",
  "status": "failed_retry_pending",
  "failed_attempts": "2",
  "last_failure": "2026-10-30T23:40:12Z",
  "next_attempt_at": "2026-11-02T09:15:00Z",
  "fee_lines": [
   {
    "desc": "monthly",
    "amt": "24.99"
   },
   {
    "desc": "late_fee",
    "amt": "6.50"
   },
   {
    "desc": "joining_top_up",
    "amt": "12.00"
   }
  ]
 },
 "arrears": {
  "amount_gbp": "just under 60",
  "currency": "GBP",
  "aged_days": 9
 },
 "grace_period": "5 days",
 "policy_ref": "DDR-7.2",
 "clauses": [
  "1. Retry a failed collection on the next business day, up to three attempts.",
  "2. After the third failure, send written notice and suspend booking access after 5 days.",
  "3. A card fallback may be offered once per billing cycle.",
  "4. Exception: where a membership pause was requested in writing within the current cycle, clauses 1 and 2 do not apply and status is held for review."
 ],
 "pause_request": {
  "requested": "2026-10-12",
  "channel": "email",
  "in_writing": true,
  "Logged_By": "R. Lindqvist"
 },
 "cancellation": {
  "requested": "2026-10-12",
  "channel": "phone",
  "logged_by": "J. Okafor",
  "confirmed": null
 },
 "satisfaction_readings": [
  "4",
  "3.5",
  "4.5"
 ],
 "fallback_candidates": [
  {
   "id": "FB-1",
   "card": "VISA ending 4417",
   "expiry_ok": false,
   "postcode_match": true,
   "no_decline_30d": true,
   "consent_on_file": true
  },
  {
   "id": "FB-2",
   "card": "MC ending 0082",
   "expiry_ok": true,
   "postcode_match": false,
   "no_decline_30d": true,
   "consent_on_file": true
  },
  {
   "id": "FB-3",
   "card": "AMEX ending 9031",
   "expiry_ok": true,
   "postcode_match": true,
   "no_decline_30d": false,
   "consent_on_file": true
  },
  {
   "id": "FB-4",
   "card": "DEBIT ending 1186",
   "expiry_ok": true,
   "postcode_match": true,
   "no_decline_30d": true,
   "consent_on_file": false
  },
  {
   "id": "FB-5",
   "card": "VISA ending 2210",
   "expiry_ok": true,
   "postcode_match": true,
   "no_decline_30d": true,
   "consent_on_file": true
  }
 ],
 "crm_legacy_flag": "Y",
 "print_tpl_ver": 3,
 "last_contact": {
  "date": "27/10/2026",
  "by": "front desk",
  "note_id": null
 },
 "notes": "J. Okafor logged a cancellation by phone on 12 Oct. R. Lindqvist says the call was a pause request, that no cancellation is on file, and that the member confirmed the pause by email the same day. The member's card was last updated approximately three weeks ago and the balance figure has not been reconciled since."
}
```

**q1 [score / compare]** Rate the member's overall satisfaction, from the gym's point of view, using the average of the satisfaction readings recorded for her.  
  `0` = Low: average below 2; `1` = Middling: average at least 2 but below 3; `2` = High: average of 3 or more  
  gold: {"0": 0.0329, "1": 0.0471, "2": 0.92}  · agreement 4/4 · check: settled · average value 4.0 points edges [2.0, 3.0] (far)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the size of the total charges currently listed against the member's direct debit, from the member's point of view, by adding all the listed fee lines.  
  `0` = Minimal: total below £20; `1` = Small: total at least £20 but below £35; `2` = Moderate: total at least £35 but below £50; `3` = Large: total at least £50 but below £65; `4` = Very large: total of £65 or more  
  gold: {"0": 0.0165, "1": 0.0282, "2": 0.92, "3": 0.0235, "4": 0.0118}  · agreement 4/4 · check: settled · sum value 43.49 GBP edges [20.0, 35.0, 50.0, 65.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [choice / infer]** Which single fallback card meets every stated condition for being offered as the card fallback?  
  `fb_1` = The first candidate card meets every condition.; `fb_2` = The second candidate card meets every condition.; `fb_3` = The third candidate card meets every condition.; `fb_4` = The fourth candidate card meets every condition.; `fb_5` = The fifth candidate card meets every condition.  
  gold: {"fb_1": 0.0218, "fb_2": 0.0182, "fb_3": 0.0182, "fb_4": 0.0218, "fb_5": 0.92}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / judge]** Once the exception clause is checked, what outcome does the retry policy give for this member's failed collection?  
  `retry_next_day` = Normal rule applies: retry the collection on the next business day.; `suspend_access` = Normal rule applies: send notice and suspend booking access after the grace period.; `hold_for_review` = The exception applies: the retry and suspension steps are not applied and the status is held for review.  
  gold: {"retry_next_day": 0.07, "suspend_access": 0.0675, "hold_for_review": 0.8625}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0925  ·  freight forwarding  ·  chat log  ·  decider: the operations manager  ·  target: mostly clear

```
Chat log export: OPS-BRIDGE / Consignment desk
Channel: #ops-bookings  |  Exported 2026-10-29 16:42 GMT

[09:04] Priya Raghunathan: Morning all. HBL-44813 (FCL, Felixstowe to Rotterdam) still shows no VGM from the shipper. Cut-off is 14:00 tomorrow.
[09:07] Tomasz Wierzbicki: VGM came in last night, I saw it in the portal. Gross 11,840 kg per the packing list, weighbridge ticket attached says 11,790 kg. Booking ref BKG-7720-R.
[09:09] Priya Raghunathan: Portal shows 11,920 kg for the same container, not 11,790. Which one are we filing with?
[09:11] Tomasz Wierzbicki: Weighbridge is the certified one. Use that.
[09:15] Dhruv Okafor: Road leg for the same load, Hull to Antwerp, booked on TRK-2291. Driver is running about 40 minutes behind on the M62, ETA roughly 13:20 now, was 12:40.
[09:18] Priya Raghunathan: Thanks Dhruv. Rotterdam terminal rate just came through: £2,315.00 for the lift, invoice says £2,380.00 — flagging the gap, need a credit note or it stays on the quote.
[09:22] Tomasz Wierzbicki: Shipper's cargo is just under 24,000 lb net on the second pallet set, so do not put that on the BL as kilos.
[10:01] Dhruv Okafor: Unrelated: the Antwerp yard has the hazmat lock-up closed Thursday for fire-door testing, 08:00 to 12:00. Nothing of ours is in it.
[10:03] Priya Raghunathan: Noted. Ticket OPS-5518 raised for the credit note.
[10:05] Tomasz Wierzbicki: Booking confirmation says 2 of 3 documents signed by the consignee. Still waiting on the third signature for the POD on the road leg.
[10:06] Dhruv Okafor: The rest are chasing. Will update at 12:00.
[12:00] Dhruv Okafor: TRK-2291 at Immingham, now ETA 13:35. Consignee still short on signatures.
[12:04] Priya Raghunathan: Which weight goes on the VGM form, 11,790 or 11,920? Need to submit before 14:00.

```

**q1 [score / compare]** Rate the size of the terminal lift overcharge, the gap between the invoiced and quoted amounts, from the operations manager's point of view.  
  `0` = Trivial: under £10; `1` = Minor: at least £10 but under £30; `2` = Moderate: at least £30 but under £63; `3` = Significant: at least £63 but under £120; `4` = Severe: £120 or more  
  gold: {"0": 0.0031, "1": 0.0031, "2": 0.04, "3": 0.92, "4": 0.0338}  · agreement 4/4 · check: settled · difference value 65.0 GBP edges [10.0, 30.0, 63.0, 120.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate how complete the consignee's document signing is on the booking, based on the share of documents signed, from the operations manager's point of view.  
  `0` = Barely signed: under 25% signed; `1` = Partly signed: at least 25% but under 50%; `2` = Mostly signed: at least 50% but under 70%; `3` = Nearly complete: 70% or more signed  
  gold: {"0": 0.0121, "1": 0.0242, "2": 0.9201, "3": 0.0436}  · agreement 4/4 · check: settled · share value 66.67 percent edges [25.0, 50.0, 70.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / judge]** The missing third consignee signature puts timely completion of the road-leg proof of delivery at real risk.  
  `true` = The outstanding signature, given the delays and the consignee's slowness, makes timely proof of delivery doubtful.; `false` = The outstanding signature is unlikely to hold up timely proof of delivery.  
  gold: {"true": 0.6925, "false": 0.3075}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Which weight should go on the VGM form, given the stated preference for the certified source?  
  `weighbridge_ticket` = The certified weighbridge ticket figure.; `portal_figure` = The figure the shipper portal displays.; `packing_list` = The gross figure from the packing list.  
  gold: {"weighbridge_ticket": 0.935, "portal_figure": 0.0375, "packing_list": 0.0275}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0842  ·  parcel depot  ·  system record  ·  decider: a customer service agent handling a complaint  ·  target: mostly clear

```json
{
 "record_id": "CMP-2026-048817",
 "export_ver": "3.2.1",
 "exported_at": "2026-10-29T08:14:52Z",
 "depot_ref": "DEP-NW-04 Carlisle Sorting Hub",
 "case_status": "open_pending_review",
 "customer": {
  "cust_id": "C-773190",
  "full_name": "Ffion Adeyemi-Crowe",
  "tel": "01228 554017",
  "pref_channel": "email",
  "postcode": "CA3 0PX"
 },
 "shipment": {
  "waybill_no": "WB4471906621",
  "service": "Next Day Plus",
  "parcel_count": "2",
  "declared_wt": "14.6 kg",
  "ship_date": "2026-10-23",
  "promised_by": "2026-10-24T13:00",
  "delivered_at": null,
  "attempts": [
   {
    "no": 1,
    "ts": "2026-10-24T14:37",
    "drv": "DRV-0219",
    "result": "NOT_DELIVERED_NO_ACCESS"
   },
   {
    "no": 2,
    "ts": "2026-10-27T09:05",
    "drv": "DRV-0342",
    "result": "DELIVERED_SAFE_PLACE"
   }
  ]
 },
 "claim": {
  "claim_ref": "CLM-88201",
  "value_gbp_initial": "340.00",
  "value_gbp_corrected": "286.50",
  "corrected_by": "agent_ntoa",
  "corrected_on": "2026-10-28",
  "lodged_by": "customer_portal",
  "lodged_on": "2026-10-27",
  "refund_hold_from": "2026-10-30",
  "refund_hold_to": "2026-11-04",
  "compensation_offer": null,
  "line_items": [
   {
    "desc": "kiln shelf pin set",
    "amt": "42.50"
   },
   {
    "desc": "glaze sample tray",
    "amt": "18.75"
   },
   {
    "desc": "crating labour",
    "amt": "9.00"
   }
  ]
 },
 "depot_handling": {
  "inbound_scan_ts": "2026-10-23T21:48",
  "sort_batch": "SB-1023-N",
  "pallet_id": "PL-7741",
  "approx_dwell_h": "just under 7",
  "exc_code": "EX-07",
  "old_exc_code": "EX-02",
  "corrected_by": "shift_supervisor_IB",
  "nested_geo": {
   "lat": 54.8951,
   "lng": -2.9382,
   "zone": "NW-3",
   "geofence_v": 2
  }
 },
 "driver_notes": {
  "drv_id": "DRV-0342",
  "vehicle_reg": "KX71 PRW",
  "signature_captured": false,
  "photo_ref": "IMG_20261027_0917.jpg",
  "free_text": "Left at rear porch under safe place option. Hall light off. Door not re-checked after first card left on 24th at 14:37."
 },
 "redelivery_options": [
  {
   "slot": "2026-10-30 08:00-10:00",
   "min_notice_h": "24",
   "hub_open": "07:00-18:00",
   "capacity_left": "0"
  },
  {
   "slot": "2026-10-30 16:00-18:00",
   "min_notice_h": "6",
   "hub_open": "07:00-17:30",
   "capacity_left": "4"
  },
  {
   "slot": "2026-11-02 10:00-12:00",
   "min_notice_h": "72",
   "hub_open": "08:00-16:00",
   "capacity_left": "2"
  },
  {
   "slot": "2026-11-03 13:00-15:00",
   "min_notice_h": "12",
   "hub_open": "08:00-16:00",
   "capacity_left": "1"
  },
  {
   "slot": "2026-11-04 09:00-11:00",
   "min_notice_h": "36",
   "hub_open": "07:00-18:00",
   "capacity_left": "3"
  }
 ],
 "criteria_req": {
  "min_cover_gbp": "300",
  "fragile_cert": true,
  "zone_required": "CA3",
  "saturday_collect": true
 },
 "alt_courier_candidates": [
  {
   "candidate": "Border Relay Ltd",
   "cover_limit_gbp": "250",
   "fragile_cert": true,
   "zones": [
    "CA3",
    "CA4"
   ],
   "saturday_collect": true
  },
  {
   "candidate": "Solway Parcel Co",
   "cover_limit_gbp": "500",
   "fragile_cert": false,
   "zones": [
    "CA3",
    "CA2"
   ],
   "saturday_collect": true
  },
  {
   "candidate": "Eden Fragile Haulage",
   "cover_limit_gbp": "400",
   "fragile_cert": true,
   "zones": [
    "CA5",
    "CA6"
   ],
   "saturday_collect": true
  },
  {
   "candidate": "Pennine Last Mile",
   "cover_limit_gbp": "350",
   "fragile_cert": true,
   "zones": [
    "CA3",
    "LA9"
   ],
   "saturday_collect": false
  },
  {
   "candidate": "Caldew Specialist Carriers",
   "cover_limit_gbp": "360",
   "fragile_cert": true,
   "zones": [
    "CA3",
    "CA1"
   ],
   "saturday_collect": true
  }
 ],
 "internal": {
  "legacy_flag": "ignore",
  "sys_ver": "4.1",
  "tmp_hold": "N/A",
  "queue": "CS-TIER2",
  "last_update_by": "agent_ntoa",
  "ticket_hint": null
 },
 "notes": "Customer reports the parcel was not received and that the rear porch was not a safe place. Driver recorded that a neighbour saw a delivery van earlier that day. Refund hold remains in place pending review."
}
```

**q1 [score / infer]** Rate how fully Pennine Last Mile satisfies the agent's stated requirements for a replacement courier, from the customer service agent's point of view.  
  `0` = None: meets none of the stated requirements; `1` = Minimal: meets exactly one of the stated requirements; `2` = Partial: meets exactly two of the stated requirements; `3` = Nearly full: meets exactly three of the stated requirements, failing one; `4` = Full: meets every stated requirement  
  gold: {"0": 0.01, "1": 0.0133, "2": 0.0333, "3": 0.9201, "4": 0.0233}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the total value of the itemised claim lines, from the customer service agent's point of view.  
  `0` = Minor: under £50; `1` = Modest: at least £50 but below £150; `2` = Substantial: at least £150 but below £250; `3` = Major: £250 or more  
  gold: {"0": 0.0276, "1": 0.9199, "2": 0.0359, "3": 0.0166}  · agreement 4/4 · check: settled · sum value 70.25 GBP edges [50.0, 150.0, 250.0] (far)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [score / compare]** Rate how late the first delivery attempt was against the promised delivery time, from the customer's point of view.  
  `0` = On time: under 15 minutes late; `1` = Slightly late: at least 15 but under 60 minutes late; `2` = Noticeably late: at least 60 but under 95 minutes late; `3` = Seriously late: at least 95 but under 240 minutes late; `4` = Extremely late: 240 minutes or more late  
  gold: {"0": 0.0077, "1": 0.0129, "2": 0.0439, "3": 0.92, "4": 0.0155}  · agreement 4/4 · check: settled · time_gap value 97.0 minutes edges [15.0, 60.0, 95.0, 240.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Which is the earliest redelivery slot that has spare capacity, enough notice from the export time, and fits fully within hub opening hours?  
  `oct30_morning` = The first slot on the earliest offered day, in the morning.; `oct30_afternoon` = The second slot on the earliest offered day, in the late afternoon.; `nov2_slot` = The mid-morning slot on the first Monday-type date after the earliest day.; `nov3_or_later` = One of the two slots offered on the last two offered dates.  
  gold: {"oct30_morning": 0.0143, "oct30_afternoon": 0.0286, "nov2_slot": 0.92, "nov3_or_later": 0.0371}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** Which single alternative courier meets every stated requirement for cover, fragile certification, zone and Saturday collection?  
  `border_relay` = Border Relay Ltd; `pennine_last_mile` = Pennine Last Mile; `caldew_specialist` = Caldew Specialist Carriers  
  gold: {"border_relay": 0.04, "pennine_last_mile": 0.04, "caldew_specialist": 0.92}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0356  ·  fishing fleet  ·  statement with cover note  ·  decider: the cooperative manager  ·  target: mixed

```
SKERROW BAY FISHERMEN'S CO-OPERATIVE LTD
Landing Office, Harbour Road, Skerrow Bay SK4 9QT
Tel 01632 960217 | landing@skerrowbaycoop.example

MEMBER STATEMENT OF ACCOUNT
Statement ref: SBFC-ST-2610-017
Period: 01/10/2026 to 28/10/2026
Member: M. Ardagh, FV Kittiwake Rose (reg. BF 412)
Quota stock: COD/7A allocation 6.250 t (Direct Quota Statement 2026, issue 3)

Date        Ref            Description                              Qty        Rate (GBP/kg)   Amount (GBP)
03/10/2026  LO/2026/0391  Landing, cod, grade A                    1,118 kg   3.42            3,822.56
09/10/2026  LO/2026/0408  Landing, cod, grade B                      642 kg   2.87            1,842.54
14/10/2026  LO/2026/0419  Landing, haddock, grade A                  380 kg   2.95            1,121.00
23/10/2026  LO/2026/0437  Landing, cod, grade A                    1,204 kg   3.38            4,069.52
23/10/2026  LO/2026/0437  Ice supplied                               120 kg   0.18               21.60
27/10/2026  LO/2026/0446  Landing, cod, grade A                    1,401 kg   3.40            4,763.40
                          Less levy 1.5% on gross                                                -350.85
                          Less handling charge (per landing x 5)                                 -125.00

Cod landed to date (all grades, COD/7A): 5,745 kg
Quota remaining under clause 4.3: see manager note
Crew declarations on file (clause 6.1): 31 of 40 required
Net payable this period: GBP 14,164.17
Payment date: 05/11/2026

Clause 4.3: Where cumulative landings reach 92% of allocation, further landings require manager sign-off before sale is released.

COVER NOTE

To: Landing Office Manager
From: M. Ardagh
Date: 28/10/2026

I have had the statement. The levy line is 1.5% on gross but the 27th landing was weighed at the sea-side scale, not the quay weighbridge, and I was told at the time this would be reconciled. Please confirm the figure is the quay weight. I also note the cod on 23rd was discharged from 22:15 Friday and not sealed until twenty to two in the morning, so the seal log will show the hold was open far longer than the standard. My crew were stood on the quay for all of it.

Crew declarations: I have Donal and two others still outstanding and I was told at the August meeting this would be cleared before the next quota period. Can you say which crew are missing.

I am not happy with the handling charge, which I was not notified of.

Regards,
Mick Ardagh
Kittiwake Rose
```

**q1 [score / compare]** Rate, from the manager's viewpoint, how long the cod hold stood open during the 23rd discharge, from start of discharge to sealing, using the member's account.  
  `0` = Brief: under 90 minutes; `1` = Moderate: at least 90 but under 150 minutes; `2` = Long: at least 150 but under 200 minutes; `3` = Very long: 200 minutes or more  
  gold: {"0": 0.013, "1": 0.0205, "2": 0.0465, "3": 0.92}  · agreement 4/4 · check: settled · time_gap value 205.0 minutes edges [90.0, 150.0, 200.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / infer]** Rate, from the manager's viewpoint, how much control the quota clause places on the release of sale for the member's next cod landing, given the cod landed to date and the allocation.  
  `0` = None: threshold not approached, sale released freely; `1` = Watch: threshold not reached but close, no sign-off needed; `2` = Sign-off: threshold reached, manager approval needed before release; `3` = Sign-off with excess: allocation itself exceeded, approval needed and overage questioned; `4` = Blocked: sale cannot be released at all  
  gold: {"0": 0.06, "1": 0.6675, "2": 0.2275, "3": 0.0275, "4": 0.0175}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [score / compare]** Rate, from the member's viewpoint, how long he waits for payment on the haddock landing, measured from that landing to the stated payment date.  
  `0` = Very short: under 7 days; `1` = Short: at least 7 but under 14 days; `2` = Moderate: at least 14 but under 21 days; `3` = Long: at least 21 but under 28 days; `4` = Very long: 28 days or more  
  gold: {"0": 0.0083, "1": 0.0124, "2": 0.04, "3": 0.92, "4": 0.0193}  · agreement 4/4 · check: settled · time_gap value 22.0 days edges [7.0, 14.0, 21.0, 28.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Which single landing is cod, grade A, weighed on the quay weighbridge, and free of any dispute raised by the member?  
  `first_october_cod` = The earliest cod landing of the period; `haddock_landing` = The mid-month haddock landing; `night_discharge_landing` = The landing discharged overnight with the hold-open complaint; `final_landing` = The last landing of the period  
  gold: {"first_october_cod": 0.8975, "haddock_landing": 0.025, "night_discharge_landing": 0.045, "final_landing": 0.0325}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** What is the earliest course the manager can take that satisfies every stated constraint on paying the member?  
  `pay_on_schedule` = Pay on the stated date, as every query can be settled by then; `hold_for_weight_check` = Delay until the disputed weight is reconciled with the quay figure; `hold_for_sign_off` = Delay until the manager signs off under the quota clause  
  gold: {"pay_on_schedule": 0.4625, "hold_for_weight_check": 0.4, "hold_for_sign_off": 0.1375}  · agreement 2/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0193  ·  restaurant food safety  ·  system record  ·  decider: the area hygiene auditor  ·  target: mostly debatable

```json
{
 "record_id": "HYG-LK-0418",
 "schema_ver": "3.1",
 "Site": {
  "siteCode": "LK-HS-07",
  "site_name": "Larkspur Harbour Street",
  "district": "Eastbank",
  "AuditorArea": "EB-3"
 },
 "visit": {
  "visit_type": "routine_followup",
  "visitDate": "2026-10-26",
  "arrival_time": "09:20",
  "departure_time": "11:05",
  "auditor_ref": "EHO-2291",
  "prev_visit_ref": "HYG-LK-0307"
 },
 "walkInCooler": {
  "unit_id": "WIC-02",
  "setpoint_c": 3,
  "reading_initial_c": "6.1",
  "reading_corrected_c": "4.9",
  "correction_note": "re-probed after door seal check",
  "probe_ser": "PRB-88417"
 },
 "cold_holding_limit_c": 5,
 "cleaningShift": {
  "shift_ref": "CS-1024-B",
  "start_ts": "2026-10-24T22:40",
  "end_ts": "2026-10-25T06:15",
  "crew_size": "6",
  "supervisor": null
 },
 "staffCerts": {
  "certs_on_file": "31",
  "staff_headcount_required": 40,
  "last_cert_check": "2026-10-20"
 },
 "handWashSink": {
  "water_temp_c": 41,
  "soap_dispenser_ok": true,
  "paper_towel_stock": null
 },
 "reinspection_options": [
  {
   "opt": "A",
   "date": "2026-10-30",
   "window": "07:00-10:00",
   "notice_hours_min": 48,
   "capacity_visits": "1",
   "booked": null
  },
  {
   "opt": "B",
   "date": "2026-11-02",
   "window": "13:00-15:30",
   "notice_hours_min": 24,
   "capacity_visits": "2",
   "booked": "0"
  },
  {
   "opt": "C",
   "date": "2026-11-03",
   "window": "06:30-09:00",
   "lead_time_days": "4",
   "capacity_visits": "1",
   "booked": null
  },
  {
   "opt": "D",
   "date": "2026-11-07",
   "window": "10:00-12:00",
   "notice_hours_min": 72,
   "capacity_visits": "3",
   "booked": "1"
  },
  {
   "opt": "E",
   "date": "2026-11-09",
   "window": "14:00-16:00",
   "notice_hours_min": null,
   "capacity_visits": "2",
   "booked": null
  }
 ],
 "policy": {
  "policy_ref": "CF-7.2",
  "clauses": [
   {
    "no": "7.2.1",
    "text": "Chilled food stored at or below the cold holding limit at all times."
   },
   {
    "no": "7.2.2",
    "text": "Any reading above the limit requires product check and recorded disposition within the same visit."
   },
   {
    "no": "7.2.3",
    "text": "Exception: where unit is repaired and re-probed within 2 h of the reading and reading is at or below limit, clause 7.2.2 does not apply."
   },
   {
    "no": "7.2.4",
    "text": "Re-inspection scheduled where two or more clauses are not met at the time of visit."
   }
  ],
  "outcome_options": [
   "no_action",
   "written_advice",
   "re_inspection_due",
   "improvement_notice",
   "closure_recommended"
  ]
 },
 "enforcement_ref": null,
 "exportBatch": 88213,
 "ui_theme": "lt",
 "kiosk_print_qty": "1",
 "legacy_flag": null,
 "notes": "Walk-in cooler WIC-02 was reported at 6.1 C on the first probe and the door seal was checked before a second reading was taken. Cleaning crew CS-1024-B signed in across the night change and the staff certificate register was reviewed at the desk on the day of visit."
}
```

**q1 [score / compare]** Rate the length of the overnight cleaning shift, from the auditor's point of view, from clock-in to clock-out as recorded.  
  `0` = Very short: under 240 minutes; `1` = Short: at least 240 but under 360 minutes; `2` = Standard: at least 360 but under 540 minutes; `3` = Long: at least 540 but under 660 minutes; `4` = Very long: 660 minutes or more  
  gold: {"0": 0.0089, "1": 0.0133, "2": 0.92, "3": 0.0356, "4": 0.0222}  · agreement 4/4 · check: settled · time_gap value 455.0 minutes edges [240.0, 360.0, 540.0, 660.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / infer]** Rate how demanding the cold holding policy is for the walk-in cooler on the visit day, from the auditor's view, once its exception clause is checked against the facts.  
  `0` = Nothing_required: no reading above the limit stands, so no product action is needed; `1` = Waived: a reading above the limit occurred but the repair-and-re-probe exception clearly removes the product check; `2` = Product_check_required: the exception is not shown to apply, so a product check and recorded disposition are needed in the visit; `3` = Check_and_follow_up: product check is needed and a further inspection is triggered by multiple unmet clauses  
  gold: {"0": 0.0525, "1": 0.18, "2": 0.6, "3": 0.1675}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [score / compare]** Rate how stale the staff certificate register check was, from the auditor's point of view, measured from the last check to the visit date.  
  `0` = Very recent: under 2 days; `1` = Recent: at least 2 but under 5 days; `2` = Moderate: at least 5 but under 7 days; `3` = Dated: at least 7 but under 14 days; `4` = Stale: 14 days or more  
  gold: {"0": 0.008, "1": 0.016, "2": 0.92, "3": 0.04, "4": 0.016}  · agreement 4/4 · check: settled · time_gap value 6.0 days edges [2.0, 5.0, 7.0, 14.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Booking on 29 October 2026, which re-inspection option is the earliest that meets its notice or lead-time requirement and still has spare visit capacity?  
  `opt_a` = The first listed option; `opt_b` = The second listed option; `opt_c` = The third listed option; `opt_d` = The fourth listed option; `opt_e` = The fifth listed option  
  gold: {"opt_a": 0.0217, "opt_b": 0.92, "opt_c": 0.0333, "opt_d": 0.0133, "opt_e": 0.0117}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / judge]** Which outcome does the policy most plausibly give for this visit once the exception clause and the re-inspection clause are checked?  
  `no_action` = No clause is unmet, so nothing follows; `written_advice` = At most one clause is unmet, so advice is given; `re_inspection_due` = Two or more clauses are unmet, so a re-inspection is scheduled; `improvement_notice` = Breaches warrant a formal notice; `closure_recommended` = Breaches are severe enough to recommend closure  
  gold: {"no_action": 0.0575, "written_advice": 0.28, "re_inspection_due": 0.5525, "improvement_notice": 0.0825, "closure_recommended": 0.0275}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0811  ·  parcel locker network  ·  system record  ·  decider: the field technician  ·  target: mostly clear

```json
{
 "ticket_id": "LKR-2026-048812",
 "siteRef": "SITE-NE-0417",
 "site_name": "Harlow Road Retail Park, Bay 3",
 "status": "awaiting_tech_decision",
 "opened_at": "2026-10-19T14:32:08Z",
 "priority": "P2",
 "category": "lock_actuator_fault",
 "sla": {
  "policy_code": "SLA-STD-5WD",
  "resolve_within": "5 working days",
  "working_calendar": "UK-ENG-2026",
  "due_date": "2026-10-26",
  "clock_excludes": [
   "weekends",
   "bank_holidays"
  ]
 },
 "fault_readings": {
  "bat_v_readings": [
   "12.1 V",
   "11.6 V",
   "11.9 V"
  ],
  "bat_min_v_policy": "11.8 V",
  "door_cycles_since_service": "18214 cycles",
  "lock_retries_last_24h": "37",
  "ambient_temp_c": null
 },
 "shelf_load": {
  "shelf_id": "B3-S07",
  "rated_limit": {
   "value": 6,
   "unit": "kg"
  },
  "item_weight": {
   "value": "12.8",
   "unit": "lb"
  },
  "item_ref": "PAR-88219-Q"
 },
 "signatures": {
  "signatures_on_file": 31,
  "signatures_required": 40,
  "audit_pass": false
 },
 "repair_options": [
  {
   "opt": "A",
   "desc": "OEM actuator, fitted",
   "unit_price_gbp": "112.00",
   "qty": "1",
   "discount_pct": "10",
   "call_out_fee_gbp": "45.00",
   "minimum_charge_gbp": null
  },
  {
   "opt": "B",
   "desc": "Refurbished actuator, fitted",
   "unit_price_gbp": "78.00",
   "qty": "1",
   "discount_pct": null,
   "surcharge_gbp": "12.50",
   "call_out_fee_gbp": "0.00",
   "minimum_charge_gbp": null
  },
  {
   "opt": "C",
   "desc": "Full door assembly swap",
   "unit_price_gbp": "265.00",
   "qty": "1",
   "discount_pct": "15",
   "call_out_fee_gbp": "0.00",
   "minimum_charge_gbp": null
  },
  {
   "opt": "D",
   "desc": "Third-party engineer, part supplied",
   "unit_price_gbp": "64.00",
   "qty": "1",
   "discount_pct": null,
   "call_out_fee_gbp": "95.00",
   "minimum_charge_gbp": "120.00",
   "weekend_surcharge_pct": "20"
  }
 ],
 "visit_slots": [
  {
   "slot_id": "V1",
   "date": "2026-10-30",
   "window": "08:00-12:00",
   "lead_time_h_required": 24,
   "capacity_free": "1 of 2",
   "access": "keyholder_required"
  },
  {
   "slot_id": "V2",
   "date": "2026-11-02",
   "window": "13:00-17:00",
   "notice_days_required": 3,
   "capacity_free": "2 of 2",
   "access": "open"
  },
  {
   "slot_id": "V3",
   "date": "2026-11-03",
   "window": "09:00-16:00",
   "lead_time_h_required": 48,
   "capacity_free": "0 of 2",
   "access": "open"
  },
  {
   "slot_id": "V4",
   "date": "2026-11-05",
   "window": "07:00-10:00",
   "notice_days_required": 2,
   "capacity_free": "1 of 1",
   "access": "keyholder_required"
  },
  {
   "slot_id": "V5",
   "date": "2026-11-07",
   "window": "10:00-14:00",
   "lead_time_h_required": 72,
   "capacity_free": "2 of 3",
   "access": "open"
  }
 ],
 "parts_order_ref": null,
 "assigned_tech": null,
 "legacy_import_flag": false,
 "print_queue_id": "PQ-7",
 "colour_code": "teal",
 "tz_offset_mins": 0,
 "notes": "Keyholder for Bay 3 is off site until Thursday and the site manager has not confirmed access. Lock retries rose sharply after the 16 October firmware push, and the battery readings were taken under load. Customer has asked for the shelf to be cleared of items before any visit."
}
```

**q1 [score / compare]** Rate the average battery voltage across the recorded readings, from the field technician's point of view, as an indicator of battery health against the policy minimum.  
  `0` = Critical: average below 11.5 V; `1` = Low: average at least 11.5 V but below 11.8 V; `2` = Marginal: average at least 11.8 V but below 12.2 V; `3` = Healthy: average of 12.2 V or more  
  gold: {"0": 0.0149, "1": 0.0427, "2": 0.92, "3": 0.0224}  · agreement 4/4 · check: settled · adjusted · average value 11.87 V edges [11.5, 11.8, 12.2] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate how complete the signature collection is, from the field technician's point of view, as the share of required signatures already on file.  
  `0` = Very low: below 40% of required; `1` = Low: at least 40% but below 60%; `2` = Partial: at least 60% but below 70%; `3` = Mostly complete: at least 70% but below 90%; `4` = Complete: 90% or more  
  gold: {"0": 0.0059, "1": 0.0059, "2": 0.0385, "3": 0.9201, "4": 0.0296}  · agreement 4/4 · check: settled · share value 77.5 % edges [40.0, 60.0, 70.0, 90.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / judge]** The low battery readings are the most likely main cause of the lock retries.  
  `true` = The battery evidence is the most plausible main explanation for the retries.; `false` = Another factor is more plausible, or the battery evidence is too weak or unreliable to be the main explanation.  
  gold: {"true": 0.1075, "false": 0.8925}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Which repair option costs least once its own discount, surcharge, fee or minimum is applied?  
  `opt_a` = OEM actuator, fitted, with its discount and call-out fee; `opt_b` = Refurbished actuator, fitted, with its surcharge; `opt_c` = Full door assembly swap, with its discount; `opt_d` = Third-party engineer, with call-out fee and minimum charge; `undeterminable` = The costs cannot be separated from the information given  
  gold: {"opt_a": 0.0206, "opt_b": 0.92, "opt_c": 0.0181, "opt_d": 0.0232, "undeterminable": 0.0181}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** Which is the earliest visit slot that has free capacity, meets its notice requirement from today, and does not depend on unconfirmed access?  
  `v1` = The first slot, needing a keyholder; `v2` = The slot with open access and notice requirement in days; `v3` = The slot with open access and a lead-time requirement in hours; `v5` = The latest slot, with open access  
  gold: {"v1": 0.0275, "v2": 0.915, "v3": 0.02, "v5": 0.0375}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0022  ·  hotel front desk  ·  policy extract and case note  ·  decider: the front desk manager  ·  target: mostly clear

```
HARBOURVIEW HOTEL (120 rooms) — RECEPTION & RESERVATIONS
Policy extract: Group Blocks, Early Arrivals and Room Changes
Ref: RR-POL-07, Rev 3 (issued 14/09/2026). Owner: Front Office Manager.

7.1 Group blocks
(a) A group block of 10 rooms or more requires a signed rooming list no later than 5 working days before arrival. Working days exclude Saturdays, Sundays and bank holidays.
(b) Rooms held under a block are released at 16:00 on the cut-off date if no deposit has been received (deposit £180 per room, minimum).
(c) Changes to a block after cut-off are subject to availability and rate parity.

7.2 Early arrivals
(a) Requests for arrival before 14:00 are confirmed only where a room is clean and available at time of request.
(b) Early arrival fee: £45 per room, up to 12:00. Between 12:00 and 14:00, £25.
(c) EXCEPTION: Where the guest is a Platinum loyalty member or the booking was made through a corporate account with a signed agreement on file, the fee in (b) is waived. The waiver applies only if the agreement reference (CA-) is recorded on the booking before arrival.

7.3 Room changes
(a) Changes within the same room type are free before 18:00 on day of arrival.
(b) Upgrades are charged at the difference in published rate per night, quoted in writing.
(c) Downgrades are not permitted after check-in.

CASE NOTE — Booking HV-88214 (Pemberton Logistics, block of 14 rooms)
Received: 20/10/2026 09:12, from A. Okonedo (Sales).
Rooming list due date per 7.1(a) to be confirmed. Arrival requested 27/10 for 14 rooms, all rooms previously on hold at standard rate £189 (initially logged as £159, corrected 21/10). Deposit recorded: £2,520 (14 × £180). Rooming list received 23/10 for 11 rooms only; remaining 3 names to follow.
Guest requests early arrival 12:30 for 6 rooms. Corporate agreement CA-4471 referenced in email; not yet entered on booking.
Housekeeping reports 4 rooms ready by 12:00; remaining 2 by 13:15.
Room changes requested by Pemberton: 2 rooms, same type, swap 1204 and 1207 before 18:00 on arrival day.
Cut-off per block: 16:00 on the rooming list due date.
```

**q1 [score / compare]** Rate how complete the Pemberton rooming list is, from the front desk manager's view: the share of the block's rooms that already have guest names on the list received.  
  `0` = Minimal: below 40% of rooms named; `1` = Partial: at least 40% but below 60%; `2` = Substantial: at least 60% but below 80%; `3` = Nearly complete: at least 80% but below 95%; `4` = Complete: 95% or more  
  gold: {"0": 0.0123, "1": 0.0267, "2": 0.9199, "3": 0.0349, "4": 0.0062}  · agreement 4/4 · check: settled · share value 78.57 % edges [40.0, 60.0, 80.0, 95.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / judge]** Rate how high the corrected standard nightly rate for the Pemberton block sits, from the front desk manager's point of view, using the rate on the booking after correction.  
  `0` = Very low: under £118.50; `1` = Low: £118.50 to under £163.50; `2` = Middle: £163.50 to under £207.50; `3` = High: £207.50 to under £272; `4` = Very high: £272 or more  
  gold: {"0": 0.01, "1": 0.04, "2": 0.93, "3": 0.0125, "4": 0.0075}  · agreement 4/4 · check: not_checked · stated value 189.0 £ edges [118.5, 163.5, 207.5, 272.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / compare]** All six rooms requested for early arrival will be clean and available at the requested arrival time.  
  `true` = Housekeeping expects every one of the six rooms to be ready by the requested time.; `false` = At least one of the six rooms is not expected to be ready by the requested time.  
  gold: {"true": 0.08, "false": 0.92}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** What is the earliest time on arrival day at which all six early-arrival rooms can be confirmed under the early arrival rule?  
  `at_1200` = By midday; `at_1230` = At the requested time; `at_1315` = When the last room is reported ready; `at_1400` = At standard check-in time; `at_1600` = Late afternoon  
  gold: {"at_1200": 0.045, "at_1230": 0.075, "at_1315": 0.7625, "at_1400": 0.105, "at_1600": 0.0125}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** If the corporate agreement reference is still not recorded on the booking before arrival, what total early arrival fee applies to the six rooms?  
  `fee_0` = No fee, waiver applies; `fee_100` = A lower combined fee than the flat mid-band rate for all rooms; `fee_150` = The mid-band fee charged on every room; `fee_230` = A mix of the higher fee on some rooms and the mid-band fee on others; `fee_270` = The higher fee charged on every room  
  gold: {"fee_0": 0.0171, "fee_100": 0.0152, "fee_150": 0.9201, "fee_230": 0.0286, "fee_270": 0.019}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0446  ·  veterinary practice  ·  voicemail and CRM note  ·  decider: the duty vet  ·  target: mixed

```
VOICEMAIL TRANSCRIPT
Line: Oakfield Veterinary Surgery, main line
Received: Sat 24/10/2026 at 23:52 (auto-transcribed, unedited)
Caller: Mrs D. Pellow (owner, Biscuit, 7 yr old cocker spaniel)
Callback no.: 07700 900 418

"Hi, um, it's Debbie Pellow, I rang on Thursday about Biscuit? Sorry, it's quite late. So he's, erm, he's been sick about, I think it's four times since teatime, and he's not really wanting his food, he had maybe, sort of, a third of his normal breakfast this morning, and he's been, um, walking a bit funny at the back end, but he's still wagging when I come in the room so I don't know if that's... anyway. I gave him the anti-sick tablet from the box you gave me, the maropitant, half of one, about, because he was retching. Um. He was last at yours on the twelfth? For his booster. Not sure if that matters. Could someone ring me back, I'm up till maybe one, or I can bring him in first thing, I'd just rather not wait till Monday if he's... I don't know. Thanks. Bye."

---

CRM NOTE
Contact: Pellow, Deborah | Patient: Biscuit (cocker spaniel, M/N, 7y) | Ref: PT-20417
Created: 25/10/2026 00:21 by R. Okafor (out-of-hours handover log)

Voicemail received Sat 24/10 23:52. Owner reports vomiting approx 4 episodes since early evening, reduced appetite (roughly a third of usual breakfast Sat am), mild hindlimb unsteadiness per owner. Still bright, tail wagging on greeting per owner. Administered 1/2 tab maropitant (from practice supply) approx 23:30. Owner states last visit 12/10 (booster). Owner requests callback, available until approx 01:00 or can attend Sun am.

Weight on file 9.4 kg (last recorded 12/10). Vaccination record checked: booster 12/10 recorded, no other visits in last 6 months. No record of insurance excess query.

Owner rang Thu 22/10 re: "belly" per her voicemail; no note of that call on this record, see call log 22/10 14:07 (unanswered, no message left).

Callback attempted 00:19, no answer, left message on mobile. Duty vet notified via on-call handover, pending callback decision.
```

**q1 [score / compare]** Rate how frequent Biscuit's vomiting has been, from the duty vet's view, taking teatime as 18:00 and counting to the voicemail time. Quantity: vomiting episodes per hour.  
  `0` = Occasional: fewer than 0.3 episodes per hour; `1` = Frequent: at least 0.3 but fewer than 0.8 episodes per hour; `2` = Very frequent: at least 0.8 but fewer than 1.5 episodes per hour; `3` = Relentless: 1.5 or more episodes per hour  
  gold: {"0": 0.025, "1": 0.8625, "2": 0.0975, "3": 0.015}  · agreement 4/4 · check: open · rate value 0.68 episodes per hour edges [0.3, 0.8, 1.5] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate how long ago Biscuit was last seen at the practice, from the duty vet's view, measured from his last visit to the voicemail date.  
  `0` = Recent: fewer than 7 days; `1` = Intermediate: at least 7 but fewer than 21 days; `2` = Long ago: 21 days or more  
  gold: {"0": 0.0337, "1": 0.92, "2": 0.0463}  · agreement 4/4 · check: settled · time_gap value 12.0 days edges [7.0, 21.0] (far)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [score / infer]** Rate the urgency of response the duty vet should give Biscuit's case, applying the sensible triage rule that repeated vomiting plus new hindlimb signs raises urgency, unless the dog is bright and responsive.  
  `0` = Routine: no action beyond normal booking; `1` = Same day: review during normal daytime hours; `2` = Prompt: speak to owner and examine within hours; `3` = Emergency: immediate attendance  
  gold: {"0": 0.0225, "1": 0.22, "2": 0.5625, "3": 0.195}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Which approach costs the least in further delay before Biscuit is assessed, given the failed callback and the owner's stated availability?  
  `ring_again_before_late_cutoff` = Retry the owner by phone while she is still up, then arrange an exam; `await_owner_call` = Wait for the owner to ring again without further effort; `sunday_morning_walk_in` = Rely on the owner bringing him in first thing without contact; `defer_to_monday` = Leave everything until the next working weekday  
  gold: {"ring_again_before_late_cutoff": 0.92, "await_owner_call": 0.0273, "sunday_morning_walk_in": 0.0371, "defer_to_monday": 0.0156}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** Which single plan meets every condition: reaches the owner while she is awake, gets Biscuit examined before Monday, and takes account of the maropitant already given?  
  `ring_before_cutoff_book_sunday_exam` = Phone again within her available window and book a Sunday examination, noting the dose; `ring_after_cutoff` = Phone later than she said she would be available; `leave_note_for_monday` = Record the case and contact her on the next working weekday; `advise_more_tablets_by_text` = Advise further antiemetic without an examination  
  gold: {"ring_before_cutoff_book_sunday_exam": 0.9201, "ring_after_cutoff": 0.0315, "leave_note_for_monday": 0.0242, "advise_more_tablets_by_text": 0.0242}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0689  ·  wedding venue  ·  system record  ·  decider: the venue owner  ·  target: mixed

```json
{
 "rec_id": "EVT-2026-0417",
 "eventType": "wedding_reception",
 "client_ref": "CLI-88213",
 "Guest_Count": "118",
 "licensed_capacity_persons": 120,
 "booking": {
  "status": "provisional",
  "hold_expires": "2026-11-05",
  "deposit_paid_gbp": "500.00",
  "created_ts": "2026-10-27T16:42:10Z",
  "channel": null
 },
 "venue": {
  "room_code": "BARN-A",
  "venue_hours": "10:00-23:00",
  "noise_limit_dB_LAeq": "65 dB",
  "generator_kva": 45
 },
 "slot_options": [
  {
   "id": "S1",
   "date": "2027-05-22",
   "hours": "10:00-23:00",
   "min_lead_days": 210,
   "notice_days": null
  },
  {
   "id": "S2",
   "date": "2027-06-05",
   "hours": "10:00-22:00",
   "min_lead_days": 150,
   "notice_days": 30
  },
  {
   "id": "S3",
   "date": "2027-06-12",
   "hours": "11:00-23:30",
   "min_lead_days": 120,
   "notice_days": 45
  },
  {
   "id": "S4",
   "date": "2027-06-19",
   "hours": "10:00-23:00",
   "min_lead_days": 90,
   "notice_days": 14
  }
 ],
 "marquee_quotes": [
  {
   "supplier": "Hawthorn Tentage Ltd",
   "quote_gbp": "2840.00",
   "pli_cover_gbp": "5000000",
   "certified_persons": 150,
   "delivery_miles": 22
  },
  {
   "supplier": "Fenwick & Ryle Event Hire",
   "quote_gbp": "2615.50",
   "pli_cover_gbp": "2000000",
   "certified_persons": 200,
   "delivery_miles": 14
  },
  {
   "supplier": "Greystone Marquees",
   "quote_gbp": "3010.00",
   "pli_cover_gbp": "10000000",
   "certified_persons": 120,
   "delivery_miles": 41
  },
  {
   "supplier": "Oakfield Pavilions",
   "quote_gbp": "2470.00",
   "pli_cover_gbp": "5000000",
   "certified_persons": 100,
   "delivery_miles": 9
  },
  {
   "supplier": "Marrow & Leigh Tents",
   "quote_gbp": "2990.00",
   "pli_cover_gbp": "5000000",
   "certified_persons": 180,
   "delivery_miles": 27
  }
 ],
 "catering_lines": [
  {
   "desc": "Bar staff, 3 x 6.5h",
   "amount_gbp": "420.00"
  },
  {
   "desc": "Glassware hire",
   "amount_gbp": "135.00"
  },
  {
   "desc": "Corkage",
   "amount_gbp": "90.00"
  }
 ],
 "invoice": {
  "no": "INV-44019",
  "marquee_billed_gbp": "3115.50",
  "vat_rate": 0.2,
  "paid": null
 },
 "staff_notes": "Client asked whether the 23:30 finish on S3 is still possible if the generator is used for the band. Marquee supplier not yet confirmed; S2 hold was requested by phone on 2026-10-28 and not logged. Quotes valid 14 days from issue.",
 "updated_by": "mhale",
 "legacy_flag": null,
 "tz": "Europe/London"
}
```

**q1 [score / compare]** Rate how far the invoiced marquee charge exceeds the Fenwick & Ryle quote, in pounds, from the venue owner's point of view.  
  `0` = Negligible: less than £100; `1` = Small: at least £100 but below £250; `2` = Moderate: at least £250 but below £490; `3` = Large: at least £490 but below £1,000; `4` = Severe: £1,000 or more  
  gold: {"0": 0.0129, "1": 0.0155, "2": 0.031, "3": 0.92, "4": 0.0206}  · agreement 4/4 · check: settled · difference value 500.0 GBP edges [100.0, 250.0, 490.0, 1000.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the total of the listed catering charges (before VAT) from the venue owner's point of view.  
  `0` = Low: less than £400; `1` = Modest: at least £400 but below £550; `2` = Substantial: at least £550 but below £800; `3` = Heavy: £800 or more  
  gold: {"0": 0.0138, "1": 0.0276, "2": 0.92, "3": 0.0386}  · agreement 4/4 · check: settled · sum value 645.0 GBP edges [400.0, 550.0, 800.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / judge]** The venue owner can safely promise the client a 23:30 finish on the 12 June slot.  
  `true` = The finish can be safely promised, with no material doubt about licence, noise or generator limits.; `false` = The finish cannot safely be promised, because doubt remains about hours, noise, power or confirmation.  
  gold: {"true": 0.03, "false": 0.97}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Which is the earliest slot that has enough lead time today, and ends within venue hours but no earlier than 23:00?  
  `s1` = The first slot option; `s2` = The second slot option; `s3` = The third slot option; `s4` = The fourth slot option  
  gold: {"s1": 0.026, "s2": 0.024, "s3": 0.03, "s4": 0.92}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / compare]** Which single supplier is certified for all 118 guests, has at least £5m liability cover, delivers within 30 miles and quotes no more than £2,900?  
  `hawthorn` = Hawthorn Tentage Ltd; `fenwick` = Fenwick & Ryle Event Hire; `greystone` = Greystone Marquees; `oakfield` = Oakfield Pavilions; `marrow` = Marrow & Leigh Tents  
  gold: {"hawthorn": 0.9199, "fenwick": 0.0209, "greystone": 0.0209, "oakfield": 0.0174, "marrow": 0.0209}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0156  ·  HR absence  ·  form submission  ·  decider: the payroll officer  ·  target: mixed

```
ABSENCE & LEAVE REVIEW FORM — Submission Record
Form ref: ALR-2026-0417    Status: Submitted    Submitted: 27/10/2026 16:42

Section A — Employee
Employee name: Tomasz Wrzesniak          Employee no.: 40518
Site: Hartley Road Depot                 Line manager: Bronwen Eccles
Start of role: 03/03/2019                Contract hours/week: 37.5 hrs

Section B — Absence detail
Absence type: [ ] Annual leave  [X] Sickness  [ ] Unpaid  [ ] Other
First day of absence: 12/10/2026         Last day of absence: (blank)
Reported to manager by: Phone, 12/10/2026 07:10
Fit note received: Yes, dated 14/10/2026, 21 days
Rostered shift length: 7 hrs 45 mins    Shift pattern ref: SP-HR-11
Shifts missed (count, from manager's log): 9    Shifts missed (count, employee statement): 11
Lateness recorded on return (mins): 35 / 2 hrs 10 mins   (see note)

Section C — Parts received (goods handling, kg)
Batch 1 weight: 18.4 kg    Batch 2 weight: 1,130 lb    Batch 3 weight: (blank)

Section D — Return to work
Phased return proposed: Yes   Start date: 02/11/2026 (Monday)
Phased return days: 3 days per week for 2 weeks; capacity 60%
Occupational health referral: Requested 20/10/2026. Appointment: [blank]
Return interview held: No. Due within 5 working days of return.

Section E — Manager comments
Employee reported two calls to the sick line on 13/10/2026 and 15/10/2026. Sick line log shows one call only (13/10). Employee states call on 15/10 was made from the depot car park at 06:55 and not connected. Please confirm before any entry is made on the record.

Section F — Free text
Employee says the fit note was posted, not handed in, and arrived 16/10. Manager recalls it being handed to the site office on 14/10. Site office signing book not available at time of submission. Overpayment query raised for 10/10 to 12/10 pending. Notice period on phased return is 10 working days.
Bank holiday: 26/10/2026 (Monday) — excluded from count.

Submitted by: B. Eccles   Signature: [blank]
```

**q1 [score / infer]** Rate how overdue the employee's return interview is, from the payroll officer's view today, applying the document's deadline rule to the proposed return date and any excluded days.  
  `0` = Not yet due: the return has not started, so the deadline window has not begun; `1` = Due and in time: the return has started and the deadline has not yet passed; `2` = Overdue: the return has started and the deadline has passed without an interview  
  gold: {"0": 0.92, "1": 0.0507, "2": 0.0293}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the total lateness recorded on return, treating the two recorded figures as separate occasions, from the payroll officer's view of time to consider for pay adjustment.  
  `0` = Minimal: under 60 minutes; `1` = Small: at least 60 but under 120 minutes; `2` = Moderate: at least 120 but under 180 minutes; `3` = Large: at least 180 but under 240 minutes; `4` = Severe: 240 minutes or more  
  gold: {"0": 0.0119, "1": 0.0322, "2": 0.9201, "3": 0.0239, "4": 0.0119}  · agreement 4/4 · check: settled · adjusted · sum value 165.0 minutes edges [60.0, 120.0, 180.0, 240.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / compare]** The fit note's covered period ends before the proposed phased return start date.  
  `true` = The period the fit note covers finishes before the phased return is due to begin.; `false` = The period the fit note covers runs to or beyond the date the phased return is due to begin.  
  gold: {"true": 0.08, "false": 0.92}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** By which date must the return interview be held, if the phased return starts as proposed and the stated deadline rule is applied?  
  `fri_6_nov` = By the end of the first week back, counting the return day as day zero or shorter; `mon_9_nov` = Within five working days counting from the first day back, with no excluded days; `tue_10_nov` = Five working days after the first day back, counting from the day after; `no_fixed_date` = No deadline can be set because the return date is not firm  
  gold: {"fri_6_nov": 0.2175, "mon_9_nov": 0.6175, "tue_10_nov": 0.1225, "no_fixed_date": 0.0425}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** What is the earliest date the phased return could validly start if the 10 working days' notice runs from submission of the form?  
  `mon_2_nov` = The proposed date already satisfies the notice period; `mon_9_nov` = Start after eight working days of notice; `tue_10_nov` = Start on the tenth working day after submission; `wed_11_nov` = Start the working day after ten full working days have elapsed; `thu_12_nov` = Start two working days after the notice has elapsed  
  gold: {"mon_2_nov": 0.035, "mon_9_nov": 0.1975, "tue_10_nov": 0.1875, "wed_11_nov": 0.54, "thu_12_nov": 0.04}  · agreement 3/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0907  ·  bank branch  ·  chat log  ·  decider: the back-office checker  ·  target: mostly debatable

```
Chat log export: Account Servicing – Harbour Lane Branch
Queue: BO-Servicing / Case CS-44107
Exported 2026-10-30 09:12:44 by system

[2026-10-28 16:52:10] Priya Lindqvist (Servicing Adviser): Right, picking this one up before I log off. Customer Mr Tobiah Renwick rang at twenty to five, wants the £12,500 overdraft on the joint account (sort code 20-41-67, acc ending 8812) reviewed. Sorry, I know it's late, he's been bouncing between phone and the app all afternoon and I said I'd get it logged. Anyway, the agreed limit on the file is £4,000 and the current utilisation sheet shows the account sitting at £3,680 debit this morning.

[2026-10-28 16:54:31] Dev Okafor (Team Lead): No worries Priya. Don't need the whole story in here, just the bits the checker needs. Is there a breach notice already?

[2026-10-28 16:55:02] Priya Lindqvist: Not yet. Notice went out Friday 23rd, Royal Mail second class so he'll say he never got it. Ref CS-44107-A. Also he mentioned his mum's birthday on the weekend and I forgot to ask what he wanted me to do about it, lol.

[2026-10-28 17:03:18] Dev Okafor: Ok. Checker sits Thursday. Put the review slot in the diary, Thursday 29th, appointment window 0900 to 1pm. Ring him Friday first thing, he's not answering after 6pm apparently.

[2026-10-29 08:47:05] Priya Lindqvist: Morning. Had a look at the ledger. He paid in £1,100 at 4:15pm yesterday, so the debit is probably lower now but I have not checked whether it cleared before the cut-off at 2300 hrs. Balance query in progress.

[2026-10-29 09:01:40] Dev Okafor: Fine. Need it on the checker's desk by close of business Friday 30th, 17:00 at the latest.

[2026-10-29 11:24:09] Priya Lindqvist: Balance now showing 4.2k debit at eleven past eleven. Not sure how. Will leave a note.

```

**q1 [score / compare]** From the checker's point of view, rate the size of the increase the customer is asking for: the requested overdraft minus the limit currently agreed on the file.  
  `0` = Minimal: less than £2,000; `1` = Modest: at least £2,000 but below £4,500; `2` = Substantial: at least £4,500 but below £8,400; `3` = Large: at least £8,400 but below £12,000; `4` = Very large: £12,000 or more  
  gold: {"0": 0.0076, "1": 0.0102, "2": 0.0419, "3": 0.92, "4": 0.0203}  · agreement 4/4 · check: settled · adjusted · difference value 8500.0 GBP edges [2000.0, 4500.0, 8400.0, 12000.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** From the checker's point of view, rate how much time remains between the last chat entry and the checker's desk deadline.  
  `0` = Very short: under 12 hours; `1` = Short: at least 12 hours but under 24 hours; `2` = Moderate: at least 24 hours but under 30 hours; `3` = Ample: 30 hours or more  
  gold: {"0": 0.0127, "1": 0.0327, "2": 0.9201, "3": 0.0345}  · agreement 4/4 · check: settled · time_gap value 29.6 hours edges [12.0, 24.0, 30.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / compare]** At the latest balance shown, the account is overdrawn by more than the limit agreed on the file.  
  `true` = The most recent debit balance quoted is greater than the agreed limit on file.; `false` = The most recent debit balance quoted is equal to or lower than the agreed limit on file, or cannot be taken as exceeding it.  
  gold: {"true": 0.825, "false": 0.175}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Which is the earliest review slot that still falls inside the diary window, comes after the last logged entry, and leaves time to meet the checker's deadline?  
  `thu_1030` = Thursday morning slot, before the last logged entry.; `thu_1200` = Thursday slot inside the window, after the last logged entry.; `thu_1400` = Thursday afternoon slot, outside the appointment window.; `fri_0900` = Friday first-thing slot, inside the deadline.; `fri_1730` = Friday evening slot, after the checker's deadline.  
  gold: {"thu_1030": 0.0149, "thu_1200": 0.92, "thu_1400": 0.0136, "fri_0900": 0.042, "fri_1730": 0.0095}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0758  ·  ride-share support  ·  meeting notes  ·  decider: the refund rule  ·  target: mostly debatable

```
MEETING NOTES: Rider & Driver Support, Weekly Ops Sync
Date: Thursday 29 October 2026, 09:30–10:05
Location: Room 4B, Tanner Street office (video link also open)
Attendees: Mirela Okonkwo (chair), Dylan Forsyth, Priya Venkataraman, Sanjay Holt, Ruth Adebayo (notes)

Apologies: Connor Bell (on leave until 4 November)

1. Stranded-trip claims, September and October
Ruth reported that 31 of the 40 stranded-trip claims logged in the period had the driver's arrival photo attached. Dylan said the number of claims raised across all cities in September was 1,184 against roughly 96,000 completed trips, which he has been using as the base for the monthly report. Priya noted the October export is not final until Monday and the total will move.

2. Waiting-time disputes
Sanjay said the average waiting charge disputed in Leeds last month was just under 9 minutes per trip, up from 7 minutes 40 seconds in August. Dylan disagreed: he read the figure from the dashboard as 1 hour 12 minutes across the fortnight, which he says is the total, not the average, and asked for it to be checked before it goes into the board pack.

3. Refund threshold
Mirela confirmed the current threshold stays at £18.50 per trip until the revised refund rule is signed off. Priya asked whether the threshold applies to the fare before or after the 20% service adjustment. Nobody knew. Dylan's view is that it is before; Sanjay's view is that it is after. Not settled.

4. Driver messages
Ruth reported 212 messages sent to drivers about the pickup-point change in Q3, of which 9 were logged as complaints. Priya asked for the complaint count to be confirmed against the tagging in the helpdesk, as two tags were merged in July.

5. Vehicle accessibility requests
Mirela said requests for wheelchair-accessible vehicles in Birmingham rose from about 40 a week to 58 a week following the new pricing. No change proposed.

Actions
- Ruth: confirm October claims export and re-issue the stranded-trip figures by Monday 2 November.
- Dylan: check the 1 hour 12 minute figure against the raw dashboard export and reply on the thread.
- Priya: confirm the complaint tag merge and the 212-message base for Q3.
- Sanjay: write up the Leeds waiting-time analysis with the August comparison.
- Mirela: take the refund-threshold basis question (before or after the 20% adjustment) to the policy group on 5 November.

Next meeting: Thursday 5 November 2026, 09:30.
```

**q1 [score / compare]** Rate, from the support team's view, how complete the driver arrival-photo evidence is across the logged stranded-trip claims in the period.  
  `0` = Rare: fewer than 25% of claims have the photo; `1` = Minority: at least 25% but below 50%; `2` = Around_half: at least 50% but below 75%; `3` = Most: at least 75% but below 90%; `4` = Nearly_all: 90% or more  
  gold: {"0": 0.0175, "1": 0.025, "2": 0.0875, "3": 0.825, "4": 0.045}  · agreement 4/4 · check: open · share value 77.5 percent edges [25.0, 50.0, 75.0, 90.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / infer]** Rate how far the revised refund rule can be relied on when deciding a refund for a trip handled the day after this meeting, from the refund team's point of view.  
  `0` = None: revised rule not signed off, so only the current threshold applies; `1` = Limited: current threshold applies, with the unsettled basis flagged for later review; `2` = Partial: some revised parts apply because a decision on them has been made; `3` = Full: the revised rule has been signed off and applies entirely  
  gold: {"0": 0.65, "1": 0.3075, "2": 0.0275, "3": 0.015}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / infer]** The refund-threshold basis question will be put to the policy group no later than the start of the next weekly ops sync.  
  `true` = The policy group considers the basis question at or before the time the next ops sync begins.; `false` = The policy group considers it after the next ops sync begins, or not by then.  
  gold: {"true": 0.35, "false": 0.65}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** For a trip whose fare is just above the stated threshold before the service adjustment but below it after, what outcome does the current rule give?  
  `refund_applies` = The threshold is met, so the trip qualifies under the rule.; `refund_not_applies` = The threshold is not met, so the trip does not qualify under the rule.; `basis_unsettled` = The document does not settle which fare basis applies, so the outcome cannot be fixed.  
  gold: {"refund_applies": 0.0384, "refund_not_applies": 0.0416, "basis_unsettled": 0.92}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0436  ·  warehouse  ·  system record  ·  decider: the buyer  ·  target: mostly clear

```json
{
 "record_id": "SCR-REQ-20261029-0417",
 "export_ts": "2026-10-29T08:12:44Z",
 "source_system": "WMS-Kestrel v7.3.1",
 "site_code": "HLM-DC2",
 "site_name": "Holmfield Distribution Centre 2",
 "record_type": "replenishment_request",
 "status": "PENDING_BUYER_REVIEW",
 "sku": {
  "sku_id": "PKG-4471-B",
  "desc": "Corrugated mailer box 300x220x150mm, kraft",
  "uom_base": "EA",
  "pack_qty": "250",
  "hazmat_flag": false,
  "legacy_bin": "C-14-03"
 },
 "stock_position": {
  "on_hand_qty": "1840",
  "allocated_qty": "1265",
  "available_qty": 575,
  "reorder_point": "900",
  "safety_stock": null,
  "last_count_dt": "2026-10-24",
  "count_variance_flag": "Y"
 },
 "reorder_calc": {
  "avg_weekly_picks": [
   "1190",
   "1046",
   "1302"
  ],
  "lead_time_days": "9",
  "cover_days_target": 14,
  "suggested_qty": null,
  "rounding_rule": "ROUND_UP_PACK"
 },
 "pick_events": {
  "short_pick_count": "17",
  "pick_lines_total": "1984",
  "measure_basis": "lines_week_to_date"
 },
 "supplier_candidates": [
  {
   "opt_ref": "OPT-A",
   "supplier_name": "Brightwater Packaging Ltd",
   "unit_price_gbp": "0.84",
   "volume_disc_pct": null,
   "min_order_qty": "1000",
   "delivery_surcharge_gbp": "38.50",
   "promised_lead_days": "7",
   "fsc_cert": true,
   "payment_terms_days": 14
  },
  {
   "opt_ref": "OPT-B",
   "supplier_name": "Tallis & Hay Corrugated",
   "unit_price_gbp": "0.79",
   "volume_disc_pct": "4",
   "min_order_qty": "750",
   "delivery_surcharge_gbp": null,
   "promised_lead_days": "11",
   "fsc_cert": true,
   "payment_terms_days": 30
  },
  {
   "opt_ref": "OPT-C",
   "supplier_name": "Northgate Box Supply",
   "unit_price_gbp": "0.81",
   "volume_disc_pct": "2.5",
   "min_order_qty": "500",
   "delivery_surcharge_gbp": "22.00",
   "promised_lead_days": "6",
   "fsc_cert": true,
   "payment_terms_days": 30
  },
  {
   "opt_ref": "OPT-D",
   "supplier_name": "Pellow Industrial Cartons",
   "unit_price_gbp": "0.76",
   "volume_disc_pct": null,
   "min_order_qty": "2000",
   "delivery_surcharge_gbp": "0.00",
   "promised_lead_days": "10",
   "fsc_cert": true,
   "payment_terms_days": 45
  },
  {
   "opt_ref": "OPT-E",
   "supplier_name": "Ashby Fold Board Co",
   "unit_price_gbp": "0.78",
   "volume_disc_pct": "1",
   "min_order_qty": "800",
   "delivery_surcharge_gbp": "15.00",
   "promised_lead_days": "5",
   "fsc_cert": false,
   "payment_terms_days": 45
  }
 ],
 "buyer_conditions": {
  "max_lead_days": 8,
  "max_moq": 1000,
  "fsc_required": true,
  "min_payment_terms_days": 30
 },
 "notes": "Count on 24 Oct not reconciled to ledger, variance under review by stock control. Overnight replen run skipped 28/29 Oct due to dock closure; resumes 30 Oct 02:00. Brightwater quote dated 6 Oct, valid 30 days.",
 "audit": {
  "created_by": "svc_replen_batch",
  "created_ts": "2026-10-28T23:58:03Z",
  "updated_by": "j.okonedo",
  "updated_ts": "2026-10-29T07:40:17Z",
  "version": 4
 }
}
```

**q1 [score / infer]** Rate how far the buyer can rely on the recorded available stock figure as the basis for sizing this order, given the count status and the missing planning data.  
  `0` = Unusable: the figure is known to be wrong or absent and cannot guide the order; `1` = Weak: the figure is flagged as doubtful and key planning data is missing, so it needs checking first; `2` = Fair: the figure is mostly sound with a minor unresolved caveat; `3` = Sound: the figure is recent, reconciled and complete  
  gold: {"0": 0.07, "1": 0.8125, "2": 0.1025, "3": 0.015}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the week-to-date short-pick rate (short picks as a share of pick lines) from the stock control team's point of view.  
  `0` = Very low: below 0.3%; `1` = Low: at least 0.3% but below 0.6%; `2` = Moderate: at least 0.6% but below 1.2%; `3` = High: at least 1.2% but below 2.0%; `4` = Very high: 2.0% or more  
  gold: {"0": 0.0094, "1": 0.0361, "2": 0.92, "3": 0.0282, "4": 0.0063}  · agreement 4/4 · check: settled · rate value 0.857 percent edges [0.3, 0.6, 1.2, 2.0] (far)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / judge]** The recorded available stock figure can safely be used for this order without further checking by stock control.  
  `true` = The figure is reliable enough to order from as it stands.; `false` = The figure is doubtful or incomplete and should be checked or treated cautiously before ordering.  
  gold: {"true": 0.0325, "false": 0.9675}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Which single supplier option meets every one of the buyer's stated conditions?  
  `opt_a` = The first supplier option; `opt_b` = The second supplier option; `opt_c` = The third supplier option; `opt_d` = The fourth supplier option; `opt_e` = The fifth supplier option  
  gold: {"opt_a": 0.0229, "opt_b": 0.02, "opt_c": 0.92, "opt_d": 0.02, "opt_e": 0.0171}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / compare]** For an order of 2,000 units, which supplier option has the lowest total cost once its own discount and delivery surcharge are applied?  
  `opt_a` = The first supplier option; `opt_b` = The second supplier option; `opt_c` = The third supplier option; `opt_d` = The fourth supplier option; `opt_e` = The fifth supplier option  
  gold: {"opt_a": 0.0175, "opt_b": 0.865, "opt_c": 0.02, "opt_d": 0.075, "opt_e": 0.0225}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0581  ·  hotel front desk  ·  voicemail and CRM note  ·  decider: the night auditor  ·  target: mostly clear

```
VOICEMAIL TRANSCRIPT
Harcourt Bay Hotel, Reservations line
Received Thu 29/10/2026 16:52, duration 1 min 12 s

"Um, hi, it's Pauline Lindqvist, booking HB-448172. We're in the family suite, 412. We came in Wednesday the twenty-eighth, about half three, and we're meant to be out Saturday the thirty-first, ten o'clock. Only my husband's flight's been, sort of, moved, so we might need till Sunday, the first, maybe eleven? Also the little fridge in 412 is, I don't know, maybe six degrees? It's not cold enough. Call me back, it's oh-seven-seven-oh-oh, nine hundred, three one eight. Thanks."

CRM NOTE
Logged 29/10/2026 17:08 | Agent RA-07 | Ref HB-448172
Lindqvist, Family Suite 412. Arrived 28/10 15:30. Departure on file 31/10 10:00. Guest called, may extend to 01/11, latest 11:00, not confirmed. Minibar fridge approx 6 C, ticket ENG-20261029-033 raised, engineer due Fri AM. Callback not made.

Housekeeping Wed output (rooms / hours on floor): A 36 / 5.5; B 42 / 7; C 29 / 4; D 40 / 6.5; E 33 / 6.
Linen batch LB-14: 86 kg out, 9 lb rejected.
Group block BR-88: 31 of 40 registration cards signed (Sat arrivals).

LATE CHECKOUT RULE LC-3
1. Standard checkout 11:00.
2. Extension to 13:00 free if rooms available and rate is flexible.
3. Extension to 18:00 charged at 50% of room rate.
4. Extension beyond 18:00 charged one night.
5. Exception: where booking carries a non-refundable rate, extensions beyond 13:00 are refused unless approved by duty manager.

COMPENSATION CP-2
1. Fault reported and logged under 24 hours: no credit.
2. Fault logged 24 to 48 hours: GBP 15 credit.
3. Fault logged over 48 hours: one night credit.
4. Exception: where fault was not reported by guest at time of issue, credit is capped at GBP 15 regardless of duration.
```

**q1 [score / infer]** Rate how restrictive the late-checkout rule is for a guest on a non-refundable rate asking to leave at 15:00 on the day of departure, assuming rooms are available. Rate from the night auditor's point of view.  
  `0` = Free: the extension is granted at no charge; `1` = Half rate: the extension is granted for half the room rate; `2` = One night: the extension is charged as a full night; `3` = Refused: the extension is refused unless the duty manager approves it  
  gold: {"0": 0.0175, "1": 0.0275, "2": 0.035, "3": 0.92}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate how complete the group's registration paperwork is, judged by the share of cards signed, from the night auditor's point of view.  
  `0` = Poor: less than 50% of cards signed; `1` = Partial: at least 50% but below 75% signed; `2` = Good: at least 75% but below 90% signed; `3` = Complete: at least 90% signed  
  gold: {"0": 0.016, "1": 0.04, "2": 0.92, "3": 0.024}  · agreement 4/4 · check: settled · share value 77.5 % edges [50.0, 75.0, 90.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [score / judge]** Rate how warm the guest's room fridge is, from the guest's point of view, using the temperature reported in the note.  
  `0` = Cold: below 3.5 C; `1` = Cool: at least 3.5 C but below 5.8 C; `2` = Warm: at least 5.8 C but below 9.2 C; `3` = Very warm: 9.2 C or more  
  gold: {"0": 0.015, "1": 0.095, "2": 0.8575, "3": 0.0325}  · agreement 4/4 · check: not_checked · stated value 6.0 C edges [3.5, 5.8, 9.2] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Which housekeeping floor cleaned the most rooms per hour on the floor on Wednesday?  
  `floor_a` = Floor A has the highest rate; `floor_b` = Floor B has the highest rate; `floor_c` = Floor C has the highest rate; `floor_d` = Floor D has the highest rate; `floor_e` = Floor E has the highest rate  
  gold: {"floor_a": 0.0286, "floor_b": 0.0143, "floor_c": 0.9199, "floor_d": 0.0229, "floor_e": 0.0143}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** If the fridge fault dated from arrival and the guest reported it as soon as noticed, what compensation does the compensation rule give, using the time it was logged?  
  `no_credit` = No credit is due; `fixed_small_credit` = The fixed small-sum credit is due; `one_night_credit` = One night's credit is due; `half_night_credit` = Half a night's credit is due; `manager_decides` = The rule gives no outcome; a manager must decide  
  gold: {"no_credit": 0.0325, "fixed_small_credit": 0.87, "one_night_credit": 0.0375, "half_night_credit": 0.0175, "manager_decides": 0.0425}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q6 [choice / infer]** A guest on a flexible rate, with rooms available, asks to leave at 16:00 instead of standard checkout. What charge does the late-checkout rule give?  
  `free` = No charge; `half_rate` = Half the room rate; `one_night` = A full night's charge  
  gold: {"free": 0.0359, "half_rate": 0.92, "one_night": 0.0441}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-1068  ·  restaurant food safety  ·  form submission  ·  decider: the shift manager  ·  target: mostly clear

```
KITCHEN HYGIENE & SUPPLIER CHECK FORM
Site: Harbour Street Grill (Store 14)
Form ref: HSG-KH-2026-1027
Submitted: 27/10/2026 06:42
Submitted by: Lewis Partridge (Sous Chef)
Shift: Early (05:30–13:30)

Section A – Fridge and cold holding
Walk-in cooler 1 temp (°C):            3.8
Walk-in cooler 2 temp (°C):            [blank]
Prep fridge (pass) temp (°C):          6.1
Freezer temp (°C):                     -18.5
Probe calibration check (Y/N):         Y
Calibrated by:                         Priya Nandakumar

Section B – Delivery receipts
Delivery ref:          DL-88214   Supplier: Coastline Fresh   Lines checked: 14   Rejected lines: 1
Delivery ref:          DL-88219   Supplier: Northgate Dairy   Lines checked: 9    Rejected lines: 0
Delivery ref:          DL-88226   Supplier: Coastline Fresh   Lines checked: [blank]   Rejected lines: 0
Chilled goods received at (°C):        4.2 (Coastline) / 9.0 (Northgate)
Reception temp recorded by:            Ravi Okafor / Lewis Partridge

Section C – Allergen labelling
Items audited:          38
Labels correct:         35
Labels missing/incorrect (see comments)

Section D – Supplier pricing (week 44)
Quotes received for cling film, 30cm, 6 rolls per case:
  Option 1  Pack Supply Co    £18.40 per case   less 10% trade discount    delivery £4.50
  Option 2  Kestrel Catering  £19.10 per case   no discount   free delivery over 4 cases
  Option 3  Bayside Packaging £17.60 per case   delivery surcharge £6.00 under 3 cases
  Option 4  Fenwick & Lamb    £18.00 per case   minimum order 5 cases, delivery free
  Option 5  Tern Wholesale    £16.95 per case   5% discount, handling fee £3.25 per order
Cases required per week:  [blank]

Comments:
Ravi says the walk-in 2 probe read 4.2 at 06:10 but Lewis thinks it was 2.4 as he saw it on the display at 06:05. Neither reading was written down on the chart. Coastline line 3 (cream cheese) arrived warm, Ravi rejected it, Lewis has it logged as accepted for the 06:40 cook. Please check which applies before the Tuesday review. Allergen errors are mainly on the new sauce tubs, batch 7731, and the sesame flag on the brioche rolls. Walk-in 2 was emptied into the prep fridge at 05:50 to make room for the Northgate order.
```

**q1 [score / compare]** Rate the seriousness of the allergen labelling error rate in the audit, from the shift manager's point of view. The rate is labels missing or incorrect as a share of items audited.  
  `0` = Low: error rate below 5%; `1` = Moderate: error rate at least 5% but below 10%; `2` = High: error rate at least 10% but below 15%; `3` = Severe: error rate of 15% or more  
  gold: {"0": 0.0225, "1": 0.92, "2": 0.04, "3": 0.0175}  · agreement 4/4 · check: settled · rate value 7.89 % edges [5.0, 10.0, 15.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / infer]** Rate how much delivery inspection coverage is actually recorded this morning, from the shift manager's point of view, using the total lines checked across the deliveries where a count is given.  
  `0` = Minimal: fewer than 12 lines recorded; `1` = Partial: at least 12 but fewer than 22 lines recorded; `2` = Substantial: at least 22 but fewer than 40 lines recorded; `3` = Extensive: 40 or more lines recorded  
  gold: {"0": 0.0171, "1": 0.0486, "2": 0.92, "3": 0.0143}  · agreement 4/4 · check: settled · sum value 23.0 lines edges [12.0, 22.0, 40.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [score / compare]** Rate the seriousness of the rejection rate on the first Coastline Fresh delivery, from the shift manager's point of view. The rate is rejected lines as a share of lines checked on that delivery.  
  `0` = Negligible: rejection rate below 3%; `1` = Minor: rejection rate at least 3% but below 7%; `2` = Notable: rejection rate at least 7% but below 15%; `3` = Serious: rejection rate of 15% or more  
  gold: {"0": 0.0175, "1": 0.075, "2": 0.88, "3": 0.0275}  · agreement 4/4 · check: open · rate value 7.14 % edges [3.0, 7.0, 15.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** For a one-off order of 5 cases of cling film, which of these three quotes costs least once its own discount, surcharge, minimum or delivery charge is applied?  
  `pack_supply` = Pack Supply Co quote, with its trade discount and delivery charge; `bayside` = Bayside Packaging quote, with its under-minimum delivery surcharge rule; `fenwick` = Fenwick & Lamb quote, with its minimum order and free delivery  
  gold: {"pack_supply": 0.92, "bayside": 0.0554, "fenwick": 0.0246}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [noul / judge]** The 9.0°C chilled reading on the Northgate Dairy delivery is a food safety concern that needs action before the dairy goods are used.  
  `true` = The reading is high enough to be a food safety concern that calls for checking or action before the goods are used.; `false` = The reading is acceptable, or does not call for any check or action before the goods are used.  
  gold: {"true": 0.8825, "false": 0.1175}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0700  ·  venue hire  ·  meeting notes  ·  decider: the bookings coordinator  ·  target: mostly clear

```
Meeting notes: Bookings review, Marlow Street Events Centre
Date: 29/10/2026, 09:30 to 10:05
Location: Room 2
Attendees: Priya Dhillon (Bookings Coordinator, chair), Tomasz Wiercinski (Events Manager), Benedikt Osei (Finance), Lauren Fairbrother (Catering liaison)
Apologies: Mei Lin Hartley

1. Christmas Gala, Hall B (180 seated). Ardent Logistics asked for a provisional hold from 28/10 to 2/11 while they arrange the deposit. Priya is happy with this. Tomasz recalls the client giving 14/11 for the deposit, not 2/11, and wants the hold released on 6/11.

2. Deposit rule BK-4.3: deposit due 20 working days before the event. Exception under clause 7.2 of the terms: deposit may be waived for registered charities with Finance sign-off, for bookings made before 1/9 only. Ardent's booking was made 14/9. Benedikt to confirm.

3. Hall B air handling readings at walkthrough: 21.5°C, 23.0°C, 22.2°C. Lauren to attach to maintenance ticket MT-7731.

4. New Year party parking: Lauren to circulate rates for the four lots (see sheet).

Actions
- Priya: confirm hold with Ardent by Fri 30/10.
- Benedikt: confirm clause 7.2 position within 5 working days (by 5/11).
- Lauren: circulate Lot C (£4.20 per hour, £12.00 event fee, 6 hours), Lot D (£3.10 per hour, £18.50 event fee, 9 hours), Lot E (£2.75 per hour, no event fee, 11 hours), Lot F (£5.00 per hour, £9.00 event fee, 4 hours).
- Tomasz: check load-in slots for the gala: Mon 2/11 06:00 to 10:00 (48 hours' notice); Sat 7/11 08:00 to 14:00 (10 working days' notice); Tue 10/11 14:00 to 18:00 (staff max 4); Thu 19/11 16:00 to 20:00 (2 days' notice).
```

**q1 [score / compare]** Rate how warm the Hall B air was at the walkthrough, from the coordinator's point of view, using the average of the three air handling readings.  
  `0` = Cool: average below 21.0°C; `1` = Comfortable: average at least 21.0°C but below 22.0°C; `2` = Warm: average at least 22.0°C but below 23.5°C; `3` = Hot: average 23.5°C or above  
  gold: {"0": 0.0168, "1": 0.0337, "2": 0.92, "3": 0.0295}  · agreement 4/4 · check: settled · average value 22.23 °C edges [21.0, 22.0, 23.5] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate how long the requested provisional hold would expire before the deposit date the client reportedly gave, from the coordinator's point of view.  
  `0` = Negligible: gap under 3 days; `1` = Short: gap at least 3 days but under 7 days; `2` = Substantial: gap at least 7 days but under 21 days; `3` = Very long: gap 21 days or more  
  gold: {"0": 0.0175, "1": 0.0325, "2": 0.925, "3": 0.025}  · agreement 4/4 · check: open · time_gap value 0.0 days edges [3.0, 7.0, 21.0] (far)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [choice / infer]** If notice is given at the end of this meeting, which is the earliest gala load-in slot that meets its own notice requirement?  
  `mon_2_nov` = The Monday early-morning slot meets its notice requirement and is the earliest.; `sat_7_nov` = The Saturday slot is the earliest that meets its notice requirement.; `thu_19_nov` = Only the later Thursday afternoon slot is the earliest that meets its notice requirement.  
  gold: {"mon_2_nov": 0.92, "sat_7_nov": 0.0448, "thu_19_nov": 0.0352}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Which parking lot has the lowest total cost for its stated number of hours, including any event fee?  
  `lot_c` = Lot C has the lowest total cost.; `lot_d` = Lot D has the lowest total cost.; `lot_e` = Lot E has the lowest total cost.; `lot_f` = Lot F has the lowest total cost.  
  gold: {"lot_c": 0.021, "lot_d": 0.0171, "lot_e": 0.0419, "lot_f": 0.92}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0348  ·  warehouse  ·  system record  ·  decider: the stock controller  ·  target: mostly debatable

```json
{
 "record_id": "SCX-2026-104477",
 "type": "receipt_exception",
 "siteCode": "WH-E3",
 "Batch_Ref": "B26-10-0917",
 "sku": "FRZ-PRAWN-500G",
 "sku_desc": "Prawn tail-on 500g IQF",
 "supplier": {
  "supplierId": "SUP-0412",
  "name": "Harrowgate Seafoods Ltd",
  "acct_status": "active",
  "open_CAR_refs": [
   "CAR-7731"
  ],
  "last_audit_dt": "2026-08-14"
 },
 "receipt": {
  "trailer_no": "TR-88213",
  "dock_door": "D14",
  "received_at": "2026-10-27T22:40:00",
  "putaway_confirmed_at": "2026-10-28T06:15:00",
  "pallets_rcvd": 14,
  "units_rcvd": "5210",
  "units_inspected": "roughly 5,150",
  "defect_units_logged": 41,
  "defect_class": "carton_crush",
  "gross_wt_kg": "1184.6",
  "temp_probe_c": 3.8
 },
 "policy_ref": {
  "doc": "SC-QA-07 Rev D",
  "clauses": [
   "1. Receipts are released to available stock where defect units logged do not exceed 0.8% of units inspected.",
   "2. Where clause 1 is exceeded, the batch is placed on QA hold pending disposition by the stock controller.",
   "3. Disposition options are: release; release with carton note; hold for supplier claim; quarantine and re-inspect; return to supplier.",
   "4. Exception: where the supplier holds a CAR with status OPEN raised within 120 days, clause 2 applies to affected pallets only and not to the whole batch.",
   "5. Clause 4 does not apply where temp_probe_c is above -18."
  ]
 },
 "prior_batches": [
  {
   "batch": "B26-10-0903",
   "units_rcvd": "4980",
   "defect_units": 12,
   "closed_dt": "2026-10-05"
  },
  {
   "batch": "B26-09-0871",
   "units_rcvd": "5340",
   "defect_units": 29,
   "closed_dt": "2026-09-22"
  }
 ],
 "site_throughput": [
  {
   "site": "WH-E1",
   "units_rcvd": "4870",
   "defects": 19
  },
  {
   "site": "WH-E2",
   "units_rcvd": "6022",
   "defects": 27
  },
  {
   "site": "WH-E3",
   "units_rcvd": "5210",
   "defects": 41
  },
  {
   "site": "WH-N1",
   "units_rcvd": "3345",
   "defects": 11
  },
  {
   "site": "WH-N4",
   "units_rcvd": "7740",
   "defects": null
  }
 ],
 "legacy_bin_code": "R-14-B-03",
 "label_template_rev": "v7.2",
 "printer_queue_id": "PQ-DOCK-2",
 "erp_sync_ts": "2026-10-28T06:16:42Z",
 "notes": "Driver reported the seal intact on arrival but cartons on pallets 9 and 11 were crushed. Inspection began at about 23:30 and was split across the midnight handover, with the second count taken after 00:00. Disposition to be confirmed before the 08:00 wave release."
}
```

**q1 [score / infer]** Rate, from the stock controller's view, how extensive the QA hold on this receipt must be under the written policy once its exception and the exception's own limit are checked.  
  `0` = No_hold: the defect count does not exceed the release limit, so the batch is released to available stock.; `1` = Pallet_hold: the limit is exceeded but the exception confines the hold to the affected pallets only.; `2` = Batch_hold: the limit is exceeded and the exception does not apply, so the whole batch is held.; `3` = Batch_hold_escalated: the whole batch is held and the policy also requires removal of it from any release wave.  
  gold: {"0": 0.75, "1": 0.0575, "2": 0.1625, "3": 0.03}  · agreement 3/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [noul / compare]** Part of the inspection count was recorded on a later calendar date than the date the trailer was received.  
  `true` = The second inspection count falls on a calendar date after the receipt date.; `false` = All inspection counts fall on the same calendar date as the receipt, or the later count cannot be placed on a later date.  
  gold: {"true": 0.92, "false": 0.08}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [choice / infer]** Which outcome does the quality policy give for this receipt once the defect limit and the exception clause with its own condition are checked?  
  `release_whole_batch` = The defect limit is not exceeded, so the batch is released without a hold.; `hold_affected_pallets` = The limit is exceeded and the exception confines the hold to the damaged pallets.; `hold_whole_batch` = The limit is exceeded and the exception is disapplied, so the entire batch is held.; `return_to_supplier` = The policy directly requires the goods to be sent back.; `cannot_settle` = Missing or approximate facts prevent the policy from giving a single outcome.  
  gold: {"release_whole_batch": 0.6875, "hold_affected_pallets": 0.03, "hold_whole_batch": 0.0775, "return_to_supplier": 0.015, "cannot_settle": 0.19}  · agreement 3/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Which site has the highest defect rate as a share of units received, going by the throughput figures?  
  `wh_e1` = The first eastern site has the highest rate.; `wh_e2` = The second eastern site has the highest rate.; `wh_e3` = This site has the highest rate.; `wh_n4_unknown` = A site with no defect figure could be highest, so the answer cannot be fixed.  
  gold: {"wh_e1": 0.02, "wh_e2": 0.0225, "wh_e3": 0.6125, "wh_n4_unknown": 0.345}  · agreement 3/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0144  ·  pharmacy dispensing  ·  statement with cover note  ·  decider: the locum pharmacist reviewing the log  ·  target: mixed

```
HOLLINS ROAD PHARMACY
14 Hollins Road, Wakefield WF2 7QD | Tel 01924 556201 | Co. reg. 08817342

STATEMENT OF ACCOUNT (REVISED)
Account: CHG-0417 Brackley Court Care Home
Statement ref: ST-2026-10-0417 rev B
Statement date: 28/10/2026
Period: 01/10/2026 to 27/10/2026

Date      Ref          Description                        Qty   Unit £   Amount £
02/10     RX-88214     Dispensing fee, monitored bags      31     2.15      66.65
05/10     RX-88301     Compliance packs, weekly            24     9.40     225.60
09/10     DEL-1107     Courier drop, Brackley (urgent)      3    14.00      42.00
12/10     RX-88377     Controlled drugs, CD2 items         12     3.10      37.20
16/10     DEL-1131     Courier drop, Brackley (standard)   18     1.85      33.30
19/10     RX-88420     Dispensing fee, monitored bags      29     2.15      62.35
23/10     RX-88466     Compliance packs, weekly            22     9.40     206.80
27/10     DEL-1158     Courier drop, Brackley (standard)   16     1.85      29.60
27/10     ADJ-0041     Credit: packs returned unused       -2     9.40     -18.80

Subtotal                                                                 684.70
VAT at 0%                                                                  0.00
Total due (rev A, issued 28/10/2026, superseded)                         721.10
Total due (rev B)                                                        684.70

Balance brought forward                                                  112.40
Payments received 14/10/2026 (BACS)                                     -250.00
Balance outstanding                                                     547.10

Collection desk, October, by site
Site          Items dispensed   Returned uncollected   Complaints logged   Collection messages sent
Brackley      1,214             41                     6                   902
Ossett        968               17                     2                   1,146
Horbury       1,032             58                     9                   1,240
Ryhill        415               7                      1                   388

Brackley Court satisfaction scores, October (out of 10): 8, 6, 9
Fridge log, Brackley Court, 26/10/2026 06:00: 4.8 °C (action limit 8.0 °C)

Delivery service options quoted for November 2026 (per care home, excl. VAT)
A  £1.85 per drop; 10% discount on the month's total where drops exceed 40; £12.00 monthly admin fee
B  £2.40 per drop; minimum monthly charge £60.00 applies
C  £1.60 per drop; fuel surcharge of 6% on drops made Monday to Friday
D  £95.00 flat for up to 70 drops; £1.10 per drop above 70
E  £2.05 per drop; 15% discount on drops booked 48 hours in advance; no fee

Payment terms: 30 days from statement date. Please quote account and statement ref on remittance.

---

From: Joan Pulford, Manager, Brackley Court Care Home
To: accounts@hollinsroadpharmacy.example
Date: 29/10/2026 08:41
Subject: Re: Statement ST-2026-10-0417 rev B

Dear Accounts,

We received rev B this morning and rev A on the 28th. Rev A showed £721.10 due, which we had already paid into against last month's balance. Please confirm which figure we are being asked to settle, as the credit line ADJ-0041 appears on rev B but not on rev A.

Two drops on the 9th were marked urgent but the courier signed for them at 16:20, which is not urgent by any reading. We have been told the Brackley figures above are ours to query. Nine of our October complaints concern Horbury, not Brackley, so I'd be grateful for the site breakdown to be checked.

Regards,
Joan Pulford
```

**q1 [score / compare]** Rate the average October satisfaction score given by Brackley Court, from the care home's point of view, using the three scores listed.  
  `0` = Very low: average below 3; `1` = Low: average at least 3 but below 5; `2` = Mixed: average at least 5 but below 7; `3` = Good: average at least 7 but below 8.5; `4` = Excellent: average 8.5 or more  
  gold: {"0": 0.0, "1": 0.0, "2": 0.03, "3": 0.92, "4": 0.05}  · agreement 4/4 · check: settled · average value 7.67 points out of 10 edges [3.0, 5.0, 7.0, 8.5] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [noul / judge]** The care home has reasonable grounds to ask for the urgent courier charge on the 9th to be reviewed.  
  `true` = The document gives reasonable grounds to question the urgent charge, so a review request is justified.; `false` = The document does not give reasonable grounds to question the urgent charge, so a review request is not justified.  
  gold: {"true": 0.79, "false": 0.21}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [choice / compare]** Which site had the highest rate of items returned uncollected per items dispensed in October?  
  `brackley` = Brackley has the highest rate; `ossett` = Ossett has the highest rate; `horbury` = Horbury has the highest rate; `ryhill` = Ryhill has the highest rate; `tie` = Two or more sites share the highest rate  
  gold: {"brackley": 0.0333, "ossett": 0.0284, "horbury": 0.92, "ryhill": 0.0116, "tie": 0.0067}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Assuming November drops match October's total, which delivery option would cost Brackley Court least?  
  `option_a` = Option A is cheapest; `option_b` = Option B is cheapest; `option_c` = Option C is cheapest; `option_d` = Option D is cheapest; `option_e` = Option E is cheapest  
  gold: {"option_a": 0.0168, "option_b": 0.0105, "option_c": 0.9201, "option_d": 0.0168, "option_e": 0.0358}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0589  ·  gym membership  ·  handwritten log transcription  ·  decider: the club manager  ·  target: mostly clear

```
Riverside Fitness Club – Membership Desk Day Book (Hand-written, transcribed)
Site: Riverside (Mill Lane)  Manager's book, vol. 3

Tues 13/10
09:40  Spoke to Mr D. Okafor re freeze on 'Gold' card. Says leaving for Lagos 3 wks. Freeze form (MF-22) given, to return by Fri.
14:15  Cancelled direct debit for acct 40417, per Mrs Pryce. Refund of £18.99 owed (1 mo). Passed to finance, ref FIN/2026/0931.
17:50  Crèche full again. 11 children on list, cap 12 – [struck through: 14] 12 sess. Told Ms Ellery to ring Ashgrove site re spare places.

Wed 14/10
08:05  Staff rota: Jas off sick, covered by Tomasz. Pool closed 1100–1300 (chlorine dosing).
11:30  Corporate deal: Brackwell & Sons, 40 staff eligible. 31 signed up so far. Need [struck through: 35] 36 to unlock the £2,400 rate. Chase Thurs.

Thurs 15/10
10:20  Call from Ms Ellery. Ashgrove crèche spare places = 3. Ref AG/CR/0447.
16:45  Pt. complaint re [illegible] locker key, 2nd time this month. Replacement key £4.50, charged to acct 40417? No – acct 40712 (check).

Mon 19/10
09:10  Rang Brackwell HR. Sign-up deadline now 6 Nov. Will send reminder mail Mon 26th.
15:00  Freeze MF-22 back in. Dates 2 Nov – 23 Nov. Hold card reactivates Mon 23rd, 06:00 sharp.

Fri 23/10
12:30  Gym floor reconfig: Studio B closed for 4 days from Mon 26th. Reopens Thurs 29th 07:00. Class cap down to 14 (was 20).

Mon 26/10
10:00  Reminder sent to Brackwell staff. Replies so far: 33 signed, 7 outstanding (not yet ticked).
Note: Ashgrove crèche closes for half term Sat 31st – Sun 1 Nov, reopens Mon 2nd, 07:30.

Wed 28/10
16:20  Ms Ellery asks whether Brackwell group can book 'Thursday after half term' taster. Need answer by Fri 30th, 12:00.

```

**q1 [score / compare]** Rate how long Mr Okafor's membership freeze lasts, from reactivation-date planning by the club manager, counting from its start date to the date the card reactivates.  
  `0` = Brief: under 7 days; `1` = Short: at least 7 days but under 14 days; `2` = Long: at least 14 days but under 28 days; `3` = Extended: 28 days or more  
  gold: {"0": 0.0207, "1": 0.0356, "2": 0.92, "3": 0.0237}  · agreement 4/4 · check: settled · time_gap value 21.0 days edges [7.0, 14.0, 28.0] (far)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate, from the club manager's view, how far the Brackwell corporate sign-up has progressed as a share of eligible staff, using the latest count of signed-up staff.  
  `0` = Minimal: under 25% of eligible staff; `1` = Partial: at least 25% but under 50%; `2` = Substantial: at least 50% but under 80%; `3` = Near complete: 80% or more  
  gold: {"0": 0.0093, "1": 0.0133, "2": 0.0573, "3": 0.9201}  · agreement 4/4 · check: settled · share value 82.5 percent edges [25.0, 50.0, 80.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [choice / infer]** Which account should the replacement locker key charge go to, once the account that was cancelled is ruled out?  
  `acct_40712` = Charge the account confirmed in the correction, which is still active; `acct_40417` = Charge the account first named, which has since been cancelled; `split_both` = Share the charge between both accounts; `waive_charge` = Make no charge to any account  
  gold: {"acct_40712": 0.9175, "acct_40417": 0.03, "split_both": 0.025, "waive_charge": 0.0275}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** What is the earliest date for the Brackwell taster session on the 'Thursday after half term'?  
  `thu_29_oct` = The Thursday before half term begins; `mon_2_nov` = The first day after half term, which is not a Thursday; `thu_5_nov` = The first Thursday after half term ends; `thu_12_nov` = The second Thursday after half term ends; `thu_19_nov` = The third Thursday after half term ends  
  gold: {"thu_29_oct": 0.025, "mon_2_nov": 0.0275, "thu_5_nov": 0.9075, "thu_12_nov": 0.0275, "thu_19_nov": 0.0125}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [noul / judge]** The Brackwell group is likely to reach the sign-up number needed for the discounted rate before the deadline.  
  `true` = The remaining sign-ups needed look achievable by the deadline given outstanding staff and time left.; `false` = The remaining sign-ups needed look unlikely to be achieved by the deadline given outstanding staff and time left.  
  gold: {"true": 0.73, "false": 0.27}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0494  ·  parcel locker network  ·  policy extract and case note  ·  decider: the field technician  ·  target: mostly clear

```
LOCKWELL PARCEL NETWORK – OPERATIONS MANUAL
Section 7: Bay Fault Credits (rev. 4, effective 1 September 2026)

7.1 Where a parcel is uncollected after the 72-hour free window and the bay fault log shows a door or sensor fault at that bay, the site operator shall raise a credit under 7.2.
7.2 Outcome:
(a) full credit of storage charges where the fault was logged before deposit;
(b) 50% credit where the fault was logged after deposit;
(c) no credit where no fault is logged;
(d) refer to Finance (form FIN-RF-12) where disputed lines exceed £150.
7.3 Exception: where the courier scan is absent, 7.2(b) is replaced by 7.2(a) provided the fault was logged within 48 hours of deposit.

Case note – ticket LKW-44821, Ferriby Road (site LKW-NE-0417)

Hi Dev, sorry for the late write-up. I was on the Harrogate run most of Tuesday 27th and Bridlington before that, which is why the ticket shows the 21st for everything; that's just when I opened it. Anyway. Customer parcel deposited Bay 14 at 09:40 on 19 October. Door sensor reset logged 14:12 that same day. Courier scan never came through. Storage lines on the account are £2.40, £3.10 and £1.75 (the last was a re-scan on the 24th, not sure why). Door cycle readings on site were 38, 41 and 35 seconds. Bay 9 had its own reset on 22 October, unrelated I think.

Q3 fault figures, failed collections of deposits: Ferriby Road 9 of 188; Thornbury 22 of 410; Kelso Park 6 of 97; Marlow Yard 14 of 255; Quayside 3 of 61.
```

**q1 [score / compare]** Rate the total storage charges on the customer's account for this parcel, from the site operator's point of view, as a level of charge.  
  `0` = Low: total under £4.00; `1` = Moderate: total at least £4.00 but under £12.00; `2` = High: total £12.00 or more  
  gold: {"0": 0.0379, "1": 0.92, "2": 0.0421}  · agreement 4/4 · check: settled · sum value 7.25 GBP edges [4.0, 12.0] (far)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the average door cycle time measured on site at the bay, from the field technician's point of view, as a level of slowness.  
  `0` = Fast: average under 30 seconds; `1` = Normal: average at least 30 but under 38.5 seconds; `2` = Slow: average at least 38.5 but under 45 seconds; `3` = Very slow: average 45 seconds or more  
  gold: {"0": 0.0267, "1": 0.9199, "2": 0.0415, "3": 0.0119}  · agreement 4/4 · check: settled · average value 38.0 seconds edges [30.0, 38.5, 45.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / judge]** The late write-up of the ticket does not undermine the evidence that the fault was logged within the time limit the exception requires.  
  `true` = The fault log timing still shows the fault recorded within the exception's time limit after deposit, despite the late write-up.; `false` = The late write-up casts doubt on, or the timing falls outside, the exception's time limit for logging the fault.  
  gold: {"true": 0.9025, "false": 0.0975}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Which site has the highest rate of failed collections as a share of its deposits?  
  `ferriby_road` = Ferriby Road has the highest failure share; `thornbury` = Thornbury has the highest failure share; `kelso_park` = Kelso Park has the highest failure share; `marlow_yard` = Marlow Yard has the highest failure share; `quayside` = Quayside has the highest failure share  
  gold: {"ferriby_road": 0.0133, "thornbury": 0.0286, "kelso_park": 0.92, "marlow_yard": 0.0248, "quayside": 0.0133}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** Which outcome does the manual give for this parcel's storage charges once the exception clause is checked?  
  `full_credit` = Storage charges are credited in full; `half_credit` = Fifty per cent of storage charges is credited; `no_credit` = No credit is given; `refer_finance` = The case is referred to Finance  
  gold: {"full_credit": 0.92, "half_credit": 0.0419, "no_credit": 0.0171, "refer_finance": 0.021}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0665  ·  HR absence  ·  chat log  ·  decider: an HR adviser  ·  target: mostly debatable

```
Chat log: HR Absence Team – Case HR-ABS-2026-0417
Exported 2026-10-29

[09:02:14] Priya Lindqvist: Morning Tomasz. Can you pick up the Okafor sickness case? Rachel's off until the 10th.
[09:03:40] Tomasz Wierzbicki: Yes. Where are we on the fit note?
[09:04:55] Priya Lindqvist: Fit note covers 14 Oct to 30 Oct. Employee has submitted a return-to-work form dated 27 Oct.
[09:06:10] Tomasz Wierzbicki: Noted. The return-to-work interview has to happen within 3 working days of the return date, so it's due by 3 Nov (excl. 1 Nov, a bank holiday in our calendar). Correct?
[09:07:22] Priya Lindqvist: Correct. Policy AB-4.2(a).
[09:09:31] Tomasz Wierzbicki: Attendance report shows 6 absences in the rolling 12 months, total 17.5 days. Is that the figure you want on the file?
[09:11:08] Priya Lindqvist: Yes, 17.5 days. Ignore the 0.5 half day in May, it was reversed.
[09:12:45] Tomasz Wierzbicki: Understood. Also the manager's note mentions a grievance. Is that linked?
[09:14:02] Priya Lindqvist: Separate file, GR-2026-0093. Don't merge them.
[09:15:19] Tomasz Wierzbicki: Got it.
[09:16:37] Priya Lindqvist: Unrelated: the car park barrier on level B is stuck again. Can facilities be told?
[09:17:10] Tomasz Wierzbicki: Raised ticket FAC-88213 for you.
[09:18:44] Priya Lindqvist: Thanks. One more thing, the occupational health referral was sent 21 Oct. Reply is due within 10 working days of receipt.
[09:19:58] Tomasz Wierzbicki: Received 22 Oct. I'll diarise it.
[09:21:03] Priya Lindqvist: Good. Speak after the 3 Nov check-in.
```

**q1 [score / compare]** Rate the average length of each recorded sickness absence in the rolling year, from the HR adviser's point of view, using the total days and number of absences on the attendance report.  
  `0` = Brief: average below 2 days; `1` = Short: average at least 2 days but below 3.5 days; `2` = Extended: average at least 3.5 days but below 5 days; `3` = Prolonged: average 5 days or more  
  gold: {"0": 0.02, "1": 0.8975, "2": 0.0725, "3": 0.01}  · agreement 4/4 · check: open · average value 2.92 days per absence edges [2.0, 3.5, 5.0] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate how much of the fit note period has elapsed by the end of 29 October, from the HR adviser's point of view, counting both the first and last dates covered as full days.  
  `0` = Early: less than 50% elapsed; `1` = Half: at least 50% but below 75% elapsed; `2` = Most: at least 75% but below 95% elapsed; `3` = Nearly all: 95% or more elapsed  
  gold: {"0": 0.0046, "1": 0.0246, "2": 0.92, "3": 0.0508}  · agreement 4/4 · check: settled · share value 94.1 percent of fit note days edges [50.0, 75.0, 95.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / infer]** The occupational health reply is due on or before the date of the planned check-in between the two advisers.  
  `true` = Ten working days from receipt ends on or before the check-in date.; `false` = Ten working days from receipt ends after the check-in date.  
  gold: {"true": 0.08, "false": 0.92}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Given the fit note end date and the bank holiday exception, by which date must the return-to-work interview be held?  
  `deadline_30_oct` = Counted from the date on the employee's return form, so already due very soon.; `deadline_2_nov` = First working day after the fit note ends, with no extra days allowed.; `deadline_3_nov` = The adviser's stated deadline, which counts from a day before the actual return.; `deadline_4_nov` = Three working days counted from the last day of the fit note itself.; `deadline_5_nov` = Three working days counted from the first working day after the fit note ends, skipping non-working days.  
  gold: {"deadline_30_oct": 0.0175, "deadline_2_nov": 0.0325, "deadline_3_nov": 0.305, "deadline_4_nov": 0.29, "deadline_5_nov": 0.355}  · agreement 2/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0982  ·  translation agency  ·  email thread  ·  decider: the vendor manager  ·  target: mixed

```
From: Priya Vashist <priya.vashist@lindqvistlanguages.example>
To: Tomasz Okonedo <tomasz.okonedo@lindqvistlanguages.example>
Cc: Gwen Harrowby <gwen.harrowby@lindqvistlanguages.example>
Date: Tue, 27 Oct 2026 16:42
Subject: RE: PO-2026-0917 Hungarian legal batch – interpreter availability

Tomasz,

Hamid confirmed by phone this morning that the Leeds slot is still open, but he has not put it in writing. Can you check the freelancer's own calendar before we commit?

Thanks,
Priya

Priya Vashist | Vendor Manager | Lindqvist Languages Ltd
Tel: 0113 496 2280 | Ext. 214

---

From: Tomasz Okonedo
Sent: Tue, 27 Oct 2026 14:10
To: Priya Vashist
Subject: RE: PO-2026-0917 Hungarian legal batch – interpreter availability

Priya,

Hamid says he can take the 4 Nov session, but I have him down for the 6 Nov one in our tracker. The tracker was last updated 19 Oct, so one of us is out of date. The client's notice for changes is 5 working days, which takes us past 30 Oct, so I'd rather not move anything without confirming.

Tomasz

---

From: Gwen Harrowby
Sent: Mon, 26 Oct 2026 11:05
To: Priya Vashist; Tomasz Okonedo
Subject: RE: PO-2026-0917 Hungarian legal batch – interpreter availability

Options as I understand them, per the client portal:

1. Leeds Crown Court annex, 4 Nov, 09:30–13:00. Lead time for travel booking 3 working days. Capacity 2 interpreters.
2. Remote (Zoom), 5 Nov, 14:00–17:00. Requires platform licence form LL-7 returned 48 hours prior. Capacity 4.
3. Sheffield office, 9 Nov, 10:00–12:30. Building closed Fri afternoons. Capacity 3.
4. Remote, 12 Nov, 08:30–11:00. Interpreter must be on the approved list (ref AL-0442). Capacity unlimited.

PO value on the batch is £1,870.00, pending the 2 Nov approval of the revised rate card (£38.50 per hour, previously £36.00).

Gwen

---

From: Priya Vashist
Sent: Mon, 26 Oct 2026 09:15
To: Gwen Harrowby; Tomasz Okonedo
Subject: PO-2026-0917 Hungarian legal batch

Team, the client has 14 pages of Hungarian witness statements to be turned around. Please confirm the session mode and interpreter list by Thursday.

Priya
```

**q1 [score / compare]** Rate the size of the proposed rate card rise, as a share of the previous hourly rate, from the vendor manager's point of view.  
  `0` = Minimal: under 2%; `1` = Modest: at least 2% but below 4%; `2` = Notable: at least 4% but below 10%; `3` = Large: 10% or more  
  gold: {"0": 0.0165, "1": 0.0259, "2": 0.92, "3": 0.0376}  · agreement 4/4 · check: settled · share value 6.94 % edges [2.0, 4.0, 10.0] (far)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the batch's cost per page of witness statements, from the vendor manager's point of view, using the purchase order value and the page count.  
  `0` = Low: under £90 per page; `1` = Moderate: at least £90 but below £135 per page; `2` = High: at least £135 but below £180 per page; `3` = Very high: £180 or more per page  
  gold: {"0": 0.017, "1": 0.92, "2": 0.0528, "3": 0.0102}  · agreement 4/4 · check: settled · rate value 133.57 £ per page edges [90.0, 135.0, 180.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / infer]** A change requested today to the Leeds session would fall inside the client's notice period, so it could not be made in time.  
  `true` = Counting the notice period in working days from today, it would run past the session date, so the change is too late.; `false` = The notice period would end on or before the session date, so a change could still be made in time.  
  gold: {"true": 0.7375, "false": 0.2625}  · agreement 3/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / judge]** Taking the freelancer's latest statement as correct, which is the earliest session option whose own booking or lead-time requirement can still be met if arranged today?  
  `leeds_court` = The in-person court annex session; `remote_first` = The earlier remote session needing a licence form; `sheffield_office` = The office session in Sheffield; `remote_approved_list` = The later remote session needing approved-list status  
  gold: {"leeds_court": 0.8575, "remote_first": 0.0775, "sheffield_office": 0.04, "remote_approved_list": 0.025}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** For the earlier remote session, when must the platform licence form be returned under the stated requirement?  
  `same_day_morning` = On the morning of the session itself; `one_day_before` = One day before the session start time; `two_days_before` = Forty-eight hours before the session start time; `three_working_days` = Three working days before the session; `no_deadline` = No deadline is stated for the form  
  gold: {"same_day_morning": 0.0156, "one_day_before": 0.0222, "two_days_before": 0.9199, "three_working_days": 0.0267, "no_deadline": 0.0156}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0924  ·  cold-chain logistics  ·  incident report  ·  decider: the quality manager  ·  target: mostly debatable

```
INCIDENT REPORT CC-IR-2026-0419
Site: Wexcombe Park Cold Hub, Bay 6
Reported by: Tomasz Glowacki, Shift Supervisor
Date of report: 26/10/2026

1. Timeline (GMT)
23/10/2026 17:30 Bay 6 logger BL-06 last in-range reading: 3.6 °C.
23/10/2026 17:40 Dock door 6 left unsealed after afternoon load. Strip curtain tied back.
23/10/2026 18:15 Door closed by night crew. Seal found torn along left edge.
26/10/2026 07:50 Ayesha Lindqvist (QC) reads BL-06 at 9.4 °C during routine walk.
26/10/2026 08:05 Bay 6 cordoned. Product placed on hold tag H-0412.

2. Witness remarks
Ayesha Lindqvist: "The curtain was still tied back when I came in. The seal was hanging off, you could feel warm air at the threshold."
Dmitri Okafor (night crew): "Door was shut at quarter past six. I did not check the seal, I assumed it was fine."

3. Affected stock
Initial entry (23/10 log): 32 pallets, chilled dairy, Bay 6A and 6B.
Correction (26/10, recount): 23 pallets. Bay 6B was double-counted in the initial entry.
Product spec: SPEC-CH-07, product core temperature not to exceed 5.0 °C.
Door open time, estimated from CCTV: about 40 minutes.
Approximate stock weight on hold: just under 1.1 tonnes.

4. Rule extract, SPEC-CH-07
4.1 Chilled stock exceeding 5.0 °C in any logged reading must be placed on hold.
4.2 Stock held under 4.1 may be released only after QC sign-off and a core probe reading.
4.3 Exception: where the excursion is under 2 hours and the core probe reads within limit, release may be authorised by the Site Manager without a second probe.
4.4 Frozen stock is outside this clause and falls under SPEC-FR-03.

5. Transfer vehicle check (for stock on hold)
TR-11: capacity 26 pallets, serviced 14/08/2026, pre-cool 2.4 °C, calibration 03/03/2026.
TR-07: capacity 24 pallets, serviced 02/06/2026, pre-cool 1.8 °C, calibration 19/02/2026.
TR-14: capacity 22 pallets, serviced 21/08/2026, pre-cool 1.9 °C, calibration 11/05/2026.
TR-19: capacity 25 pallets, serviced 10/09/2026, pre-cool 1.6 °C, calibration 14/10/2025.
TR-22: capacity 24 pallets, serviced 21/08/2026, pre-cool 1.9 °C, calibration 06/03/2026.
Conditions: capacity 24 pallets or more; service within 90 days; pre-cool 2.0 °C or below; calibration within 12 months.
```

**q1 [score / compare]** Rate how far the logged Bay 6 temperature reading exceeded the product's core temperature limit, from the quality manager's point of view.  
  `0` = Slight: excess below 2.0 °C; `1` = Moderate: excess of at least 2.0 °C but below 4.5 °C; `2` = Severe: excess of 4.5 °C or more  
  gold: {"0": 0.0237, "1": 0.92, "2": 0.0563}  · agreement 4/4 · check: settled · difference value 4.4 °C edges [2.0, 4.5] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the length of the unmonitored-in-range period for Bay 6, from the last in-range logger reading to the out-of-range reading, from the quality manager's point of view.  
  `0` = Short: below 24 hours; `1` = Extended: at least 24 hours but below 48 hours; `2` = Long: at least 48 hours but below 60 hours; `3` = Very long: 60 hours or more  
  gold: {"0": 0.0175, "1": 0.02, "2": 0.0425, "3": 0.92}  · agreement 4/4 · check: settled · time_gap value 62.33 hours edges [24.0, 48.0, 60.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / judge]** The temperature excursion affecting the held stock can safely be treated as lasting under two hours.  
  `true` = The evidence supports an excursion duration within the short limit set by the exception clause.; `false` = The evidence does not support that, because the excursion may have lasted longer than the short limit or its duration cannot be established.  
  gold: {"true": 0.045, "false": 0.955}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / infer]** Once the exception clause is checked, what does the rule currently give for the held chilled stock?  
  `no_hold_needed` = No hold was required because no logged reading breached the limit.; `remain_on_hold` = Stock stays on hold until QC sign-off and a core probe reading are obtained, with no release yet.; `site_manager_release` = Site Manager may release now without a second probe under the exception.; `release_after_qc_and_probe` = Release is allowed straight away through QC sign-off and a probe, with the exception not needed.; `other_specification` = The stock falls outside this clause and under a different specification.  
  gold: {"no_hold_needed": 0.01, "remain_on_hold": 0.8875, "site_manager_release": 0.0325, "release_after_qc_and_probe": 0.0525, "other_specification": 0.0175}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** Which single transfer vehicle meets every stated condition, judged at the report date?  
  `tr_11` = The first listed vehicle with the largest capacity.; `tr_14` = The vehicle with the smallest capacity.; `tr_19` = The vehicle with the lowest pre-cool temperature.; `tr_22` = The vehicle serviced on the same date as the smallest-capacity vehicle.  
  gold: {"tr_11": 0.03, "tr_14": 0.0167, "tr_19": 0.0333, "tr_22": 0.92}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0976  ·  solar installation  ·  email thread  ·  decider: the sales administrator  ·  target: mixed

```
From: Priya Nandakumar <priya.nandakumar@brightroofsolar.co.uk>
To: Tomasz Wielgosz <tomasz.wielgosz@brightroofsolar.co.uk>
Cc: Helen Ashdown <helen.ashdown@brightroofsolar.co.uk>
Date: Tue 27 Oct 2026 16:42
Subject: RE: Harlow Road batch – install dates and battery add-ons

Tomasz,

Thanks. Before I put anything into the sales pack I need the battery options nailed down. Here is what the three quotes currently show as I have them:

Option A – 6.4 kWh battery, base £3,850 + VAT, 5% loyalty discount if the customer already has a Brightroof panel warranty (applies to 14 of the 22 Harlow Road homes)
Option B – 9.6 kWh battery, base £4,600 + VAT, £250 surveyor visit fee waived if booked before 31 Oct
Option C – 8.0 kWh battery, base £4,120 + VAT, minimum install charge £400 if the roof is over 2 storeys

Tomasz, you said on Friday that the Harlow Road surveys were all single-storey. Helen's note from Monday says four of them are two-storey. Which is right? It changes whether the £400 minimum applies.

Helen, can you confirm the fee waiver date? I have it as 31 Oct, the booking form says 30 Oct.

Priya

-----Original Message-----
From: Tomasz Wielgosz
Sent: Mon 26 Oct 2026 09:15
To: Priya Nandakumar
Subject: RE: Harlow Road batch – install dates and battery add-ons

Priya,

All 22 surveys on Harlow Road are single-storey, I checked the site sheets on Friday. The commissioning log shows 19 of 22 panels live so far, so we are on track for the 9 Nov cut-off.

Sites are dropping out fast, so Option B looks the most sensible for the homes that want a bigger battery.

Tomasz

From: Helen Ashdown
Sent: Mon 26 Oct 2026 17:03
To: Tomasz Wielgosz; Priya Nandakumar
Subject: Harlow Road surveys

Hi both,

Four of the Harlow Road sites (nos. 3, 9, 14, 20) are two-storey, I photographed the gutters on the 14th. Site 14 has a rear extension that might count as a third level depending on how the council reads it. Commissioning is at 19 live, but two of those (nos. 6 and 11) were re-tested after the inverter swap and are not yet signed off.

Helen

-----Original Message-----
From: Priya Nandakumar
Sent: Fri 23 Oct 2026 11:30
To: Tomasz Wielgosz
Subject: Harlow Road batch – install dates and battery add-ons

Tomasz,

Can you confirm the install schedule for the batch and whether the surveyors have checked storey count on each site? Sales need the battery pricing by Wednesday.

Priya
```

**q1 [score / compare]** Rate the size of the loyalty discount on the smaller battery, from the point of view of a customer who qualifies for it.  
  `0` = Small: less than 4.2%; `1` = Moderate: at least 4.2% but below 6.8%; `2` = Large: 6.8% or more  
  gold: {"0": 0.04, "1": 0.92, "2": 0.04}  · agreement 4/4 · check: settled · stated value 5.0 % edges [4.2, 6.8] (moderate)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [noul / judge]** The Harlow Road batch is likely to reach its commissioning cut-off with every panel live and signed off.  
  `true` = The evidence suggests all panels will be live and signed off by the cut-off date.; `false` = The evidence suggests some panels will probably not be live and signed off by the cut-off date, or it is too uncertain to expect it.  
  gold: {"true": 0.065, "false": 0.935}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [choice / compare]** For a Harlow Road home that already holds a Brightroof panel warranty, which battery arrangement costs least before VAT once its own discount or fee is applied?  
  `a_discounted` = Smaller battery with the loyalty discount applied; `a_full_price` = Smaller battery with no discount; `b_fee_waived` = Largest battery booked in time for the visit fee waiver; `b_with_fee` = Largest battery with the surveyor visit fee charged; `c_mid` = Mid-sized battery with no minimum charge  
  gold: {"a_discounted": 0.92, "a_full_price": 0.0192, "b_fee_waived": 0.0256, "b_with_fee": 0.0128, "c_mid": 0.0224}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Which battery has the lowest base price per kWh before VAT, discounts and fees?  
  `option_a` = The smaller battery; `option_b` = The largest battery; `option_c` = The mid-sized battery; `tie` = Two or more batteries have the same lowest price per kWh  
  gold: {"option_a": 0.032, "option_b": 0.92, "option_c": 0.032, "tie": 0.016}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0191  ·  college admissions  ·  chat log  ·  decider: the course leader  ·  target: mixed

```
Chat log export: Harrowgate Institute of Technical Skills, Admissions (Enrolment Queue)
Thread ref: ADM-CHAT-4471
Exported: 29/10/2026 16:12

[29/10/2026 09:04] Priya Dhillon (Admissions Officer): Morning Tomasz. Applicant for the Level 3 Diesel Mechanics cohort (ref APP-22method-0917) has sent in her medical form but the lifting test sheet is still blank. Can you check whether it came through to the portal?

[09:11] Tomasz Wierzbicki (Workshop Liaison): Checked, nothing in the portal. She was booked for the manual handling assessment on Thu 05/11 but that slot needs 48 hrs notice and the bay closes at 15:30 on Thursdays.

[09:14] Priya Dhillon: Ok. Her weigh-in was 71.4 kg at the clinic, she says about 157 lb on the home scale. Does the form need kg?

[09:19] Tomasz Wierzbicki: Kg only. Lift test is set at 20 kg floor-to-waist, 10 reps. Room 2B is free Fri 06/11 from 08:30 to 12:00, but it's a 2 hr minimum booking and the assessor is only in until 11:00 that day.

[10:02] Priya Dhillon: Unrelated, can you also confirm the Autumn induction fee? Finance sent £285.00 against the invoice of £340.00 for the same learner group.

[10:08] Tomasz Wierzbicki: Invoice is the one with the 55-minute transport surcharge line, finance may have dropped it. Not my area.

[10:15] Priya Dhillon: Noted. Two more options from the assessors list: Mon 09/11 at 13:00 in Bay 4, needs 5 working days' notice, and Wed 11/11 09:00 at the Eastfield site, which is roughly 40 min each way by minibus from Harrowgate.

[10:21] Tomasz Wierzbicki: Eastfield needs a signed site transfer form, and the coach leaves at 07:45. Bay 4 has a capacity of 6 and currently has 5 booked.

[10:24] Priya Dhillon: Medical form still outstanding for the applicant. I'll chase by email. Leaving this open.

[16:12] Export ends.
```

**q1 [score / compare]** Rate the applicant's body weight in kilograms, taking the average of the clinic reading and the home-scale reading converted to kilograms, as the course leader would use for the form.  
  `0` = Very low: below 65 kg; `1` = Low: at least 65 kg but below 68.5 kg; `2` = Moderate: at least 68.5 kg but below 72 kg; `3` = High: at least 72 kg but below 75 kg; `4` = Very high: 75 kg or more  
  gold: {"0": 0.0147, "1": 0.0295, "2": 0.92, "3": 0.0274, "4": 0.0084}  · agreement 4/4 · check: settled · average value 71.31 kg edges [65.0, 68.5, 72.0, 75.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / compare]** Rate the size of the shortfall between the invoiced induction fee and the fee finance sent, from the college's point of view.  
  `0` = Negligible: under £20; `1` = Small: at least £20 but under £40; `2` = Moderate: at least £40 but under £57; `3` = Large: at least £57 but under £90; `4` = Very large: £90 or more  
  gold: {"0": 0.0117, "1": 0.0367, "2": 0.92, "3": 0.0233, "4": 0.0083}  · agreement 4/4 · check: settled · difference value 55.0 GBP edges [20.0, 40.0, 57.0, 90.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [score / compare]** Rate how long the applicant would wait on average, from the export date, across the four offered assessment slot dates, from the course leader's point of view.  
  `0` = Short: under 7 days; `1` = Medium: at least 7 days but under 10 days; `2` = Long: 10 days or more  
  gold: {"0": 0.0176, "1": 0.92, "2": 0.0624}  · agreement 4/4 · check: settled · adjusted · average value 9.75 days edges [7.0, 10.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [noul / judge]** The 07:45 coach to Eastfield leaves enough time to reach the Wednesday session before it starts.  
  `true` = The journey from departure fits comfortably before the session start, allowing for the stated travel time.; `false` = The journey does not fit comfortably before the session start, or the travel details do not support arriving in time.  
  gold: {"true": 0.7125, "false": 0.2875}  · agreement 4/4 · check: not_checked  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** Which is the earliest slot that gives at least a two-hour session and meets its own notice rule from today?  
  `thu_05_nov` = The Thursday manual handling slot at the bay that closes in the afternoon.; `fri_06_nov` = The Friday morning booking in the room, limited by the assessor's departure.; `mon_09_nov` = The Monday afternoon slot in the bay with working-day notice.; `wed_11_nov` = The Wednesday morning slot at the other site, needing a transfer form.  
  gold: {"thu_05_nov": 0.2175, "fri_06_nov": 0.64, "mon_09_nov": 0.085, "wed_11_nov": 0.0575}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

## X-0231  ·  accounts payable  ·  voicemail and CRM note  ·  decider: a supplier relations manager  ·  target: mostly clear

```
VOICEMAIL TRANSCRIPT
Received: Tue 27 Oct 2026, 16:42
From: Gareth Mullins, Dispatch Supervisor, Holloway Pressings Ltd (ext. 4417)
Callback: 01632 960318
Duration: 0:51

"Hi, it's Gareth from Holloway, calling about the, um, the PO for the bracket run, 4500187... I think it's the one for the forty-two hundred pieces? Yeah. So we've had the delivery in, the second one, the Thursday one, and the tally says, erm, about thirty-eight hundred good, and the rest went back. I'm not sure if that's, sort of, all of them or whether there's more coming on the Friday truck. Accounts have sent us the invoice already, the one for the full forty-two, and I'm told it's, I think it's about nineteen thousand four hundred? Anyway, can you give me a ring back. The, the QA lot did three samples on the, I think it was three, and they were all, sort of, around, eh, point-eight of a millimetre out on the flange. So. Yeah. Ring me back. Thanks."

---

CRM NOTE
Account: Holloway Pressings Ltd (HPL-0442)
Contact: Gareth Mullins
Logged by: Priya Kolawole, AP Supplier Desk
Date: 28/10/2026 09:15
Ref: PO 4500187 / GRN 880214, 880231

Returned call to Gareth 28/10 at 09:02, no answer, left message. Spoke to Gareth's colleague Dawn in dispatch at 09:20. Dawn confirmed Friday truck (GRN 880231) did not arrive, delivery is short. Received quantity to date recorded at 3,640 pcs across GRN 880214 (accepted 3,200 + 440 on hold pending inspection). Remaining 560 pcs not yet delivered; Dawn unsure whether on order for 30/10.

Invoice INV-HP-77213 raised on full PO qty 4,200 at £4.62/pc = £19,404.00. Gareth's estimate of £19,400 is rounded. Payment run currently set for 11/11. Invoice not yet matched to GRN; three-way match will fail on quantity.

QA sample: 3 pcs, flange dimension out by 0.8 mm (tolerance per drawing DWG-BR-112 rev C is ±0.5 mm). Hold placed on 440 pcs under NCR-2026-0391.

Supplier terms (Clause 7.3 of Supplier Agreement SA-2024-19): payment terms net 60 from receipt of valid invoice. Clause 7.4: invoices may be disputed within 14 days of receipt; disputed value is withheld. Exception under 7.4(b): where non-conformance is confirmed by supplier-acknowledged NCR, the withheld amount is not subject to late payment interest. NCR not yet acknowledged by Holloway.

Next action: await Holloway acknowledgement of NCR-2026-0391. Follow up with Gareth on Friday delivery.
```

**q1 [score / compare]** Rate, from the AP supplier manager's view, how serious the quality hold is, judged by the share of pieces received to date that are on inspection hold.  
  `0` = Minor: below 5% of received pieces held; `1` = Moderate: at least 5% but below 12% held; `2` = High: at least 12% but below 20% held; `3` = Severe: 20% or more held  
  gold: {"0": 0.0074, "1": 0.0519, "2": 0.92, "3": 0.0207}  · agreement 4/4 · check: settled · rate value 12.09 percent edges [5.0, 12.0, 20.0] (close)  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q2 [score / infer]** Rate the late payment interest exposure for the company, from AP's view, if it withholds the disputed amount at the scheduled payment run under the supplier agreement's dispute clause and its exception.  
  `0` = Nil: nothing is withheld, so no interest question arises; `1` = Protected: withheld amount is covered by a supplier-acknowledged non-conformance report, so no interest; `2` = Contingent: withheld within the dispute window but non-conformance not yet acknowledged, so interest depends on the dispute outcome; `3` = Likely: withheld after the dispute window has closed without acknowledgement, so interest probably accrues; `4` = Certain: the whole invoice is withheld with no valid dispute, so interest accrues  
  gold: {"0": 0.025, "1": 0.04, "2": 0.7625, "3": 0.145, "4": 0.0275}  · agreement 4/4 · check: open  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q3 [noul / compare]** The value of the pieces received to date, at the invoiced unit price, is below £17,000.  
  `true` = The received quantity multiplied by the unit price is less than £17,000.; `false` = The received quantity multiplied by the unit price is £17,000 or more.  
  gold: {"true": 0.92, "false": 0.08}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q4 [choice / compare]** Which payment approach leaves the company paying the least now, once each approach's own withholding is applied at the invoiced unit price?  
  `pay_full_invoice` = Pay the whole invoice with nothing withheld.; `pay_accepted_only` = Withhold everything not yet delivered and everything on hold or unaccepted.; `pay_received` = Withhold only the pieces not yet delivered.; `pay_less_held` = Withhold only the pieces placed on inspection hold.  
  gold: {"pay_full_invoice": 0.015, "pay_accepted_only": 0.92, "pay_received": 0.035, "pay_less_held": 0.03}  · agreement 4/4 · check: settled  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

**q5 [choice / infer]** What is the earliest date on which the received quantity could match the full invoiced quantity for the three-way match?  
  `today_28_10` = The match can pass today on the current receipts.; `delivery_30_10` = The match could pass once the shortfall arrives on the possible next delivery date.; `payment_run_11_11` = The match can only pass by the scheduled payment run date.; `no_confirmed_date` = No date is confirmed because the remaining delivery is not firmly on order.  
  gold: {"today_28_10": 0.004, "delivery_30_10": 0.0657, "payment_run_11_11": 0.0103, "no_confirmed_date": 0.92}  · agreement 3/4 · check: settled · adjusted  
  - [ ] OK   - [ ] broken   - [ ] ambiguous in a way the gold does not reflect

---

