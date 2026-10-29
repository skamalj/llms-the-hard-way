"""Seed list for the independent set (train_v3, R19: weighted to 4-5 level score and 4-5 option choice questions): domain x decider x document kind x complications.

All organisations, people and places are invented. Nothing here refers to any
benchmark, dataset or real company.
"""
from __future__ import annotations

import random
from typing import Dict, List

# domain -> (short description, list of deciders, typical units of measure)
DOMAINS: Dict[str, Dict] = {
    "parcel depot": {"desc": "a regional parcel sorting depot and its courier drivers", "deciders": ["the depot duty manager", "a customer service agent handling a complaint", "the claims clerk", "an automated routing rule"]},
    "accounts payable": {"desc": "the accounts payable team of a mid-sized manufacturer", "deciders": ["the AP clerk", "the finance controller", "a supplier relations manager", "an auditor"]},
    "HR absence": {"desc": "an HR team handling leave, sickness and absence", "deciders": ["the line manager", "an HR adviser", "the payroll officer"]},
    "walk-in clinic": {"desc": "a community walk-in clinic reception and triage desk", "deciders": ["the triage nurse", "the practice manager", "the receptionist", "a locum doctor reviewing notes"]},
    "warehouse": {"desc": "a distribution warehouse and its stock control team", "deciders": ["the stock controller", "a shift supervisor", "the buyer", "an automated replenishment job"]},
    "home insurance": {"desc": "a home contents insurance claims department", "deciders": ["the claims handler", "a senior claims assessor", "the complaints officer"]},
    "IT service desk": {"desc": "an internal IT service desk for a 600-person company", "deciders": ["the service desk analyst", "the incident manager", "a team lead reviewing SLA breaches"]},
    "lab QC": {"desc": "a quality control laboratory for consumer products", "deciders": ["the QC analyst", "the release authority", "the production planner"]},
    "SaaS billing": {"desc": "the billing and account team of a software subscription company", "deciders": ["a billing specialist", "the account manager", "the dunning automation"]},
    "college admissions": {"desc": "the admissions office of a vocational college", "deciders": ["the admissions officer", "the course leader", "an appeals panel member"]},
    "car park enforcement": {"desc": "a company that manages private car parks and penalty notices", "deciders": ["the appeals clerk", "the site inspector", "a customer service agent"]},
    "residential lettings": {"desc": "a lettings agency managing rented flats and houses", "deciders": ["the property manager", "the deposit adjudicator", "the maintenance coordinator"]},
    "energy supplier": {"desc": "the customer billing team of a small energy supplier", "deciders": ["a billing agent", "the complaints handler", "a meter-reading validation routine"]},
    "retail loyalty": {"desc": "the loyalty programme team of a grocery chain", "deciders": ["a customer care agent", "the programme manager", "the fraud-prevention reviewer"]},
    "venue hire": {"desc": "an events venue taking bookings for conferences and parties", "deciders": ["the bookings coordinator", "the venue manager", "the catering lead"]},
    "corporate expenses": {"desc": "the expenses desk of a consulting firm", "deciders": ["the expenses approver", "the finance business partner", "the policy owner"]},
    "fleet maintenance": {"desc": "the fleet team of a delivery company running 60 vans", "deciders": ["the fleet supervisor", "the workshop foreman", "a driver's line manager"]},
    "restaurant food safety": {"desc": "a chain restaurant kitchen and its hygiene records", "deciders": ["the head chef", "the area hygiene auditor", "the shift manager"]},
    "school office": {"desc": "the administrative office of a secondary school", "deciders": ["the attendance officer", "the head of year", "the office manager"]},
    "public library": {"desc": "a city library service with branches and a reservations system", "deciders": ["the branch librarian", "the fines and fees desk", "the collections manager"]},
    "planning applications": {"desc": "a town council planning department", "deciders": ["the case officer", "the validation clerk", "a committee clerk"]},
    "charity grants": {"desc": "a grant-making foundation assessing applications", "deciders": ["the grants officer", "the programme committee", "the finance reviewer"]},
    "hotel front desk": {"desc": "a 120-room hotel's reception and reservations", "deciders": ["the front desk manager", "the reservations agent", "the night auditor"]},
    "gym membership": {"desc": "a chain of gyms and its membership administration", "deciders": ["the membership adviser", "the club manager", "the direct-debit retry process"]},
    "construction site": {"desc": "a building contractor's site office", "deciders": ["the site manager", "the health and safety adviser", "the quantity surveyor"]},
    "software release": {"desc": "the release management team of a software company", "deciders": ["the release manager", "the on-call engineer", "the change advisory board chair"]},
    "hospital beds": {"desc": "a hospital's bed management and discharge coordination office", "deciders": ["the bed manager", "the discharge coordinator", "the ward sister"]},
    "veterinary practice": {"desc": "a small-animal veterinary practice", "deciders": ["the duty vet", "the practice receptionist", "the insurance claims administrator"]},
    "farm produce": {"desc": "a fruit and vegetable packhouse grading deliveries from growers", "deciders": ["the intake grader", "the packhouse manager", "the grower liaison"]},
    "bus operations": {"desc": "a city bus operator's control room and depot", "deciders": ["the control room supervisor", "the depot allocator", "the customer complaints team"]},
    "bank branch": {"desc": "a retail bank branch's account servicing team", "deciders": ["the branch adviser", "the back-office checker", "the complaints handler"]},
    "e-commerce returns": {"desc": "the returns and refunds team of an online homeware retailer", "deciders": ["the returns agent", "the refunds supervisor", "the returns-eligibility rule"]},
    "recruitment": {"desc": "the recruitment team of a logistics company", "deciders": ["the recruiter", "the hiring manager", "the compliance checker"]},
    "property helpdesk": {"desc": "a facilities helpdesk for an office landlord", "deciders": ["the helpdesk coordinator", "the facilities manager", "the contractor scheduler"]},
    "water utility": {"desc": "a water company's billing and leak-allowance team", "deciders": ["the billing adviser", "the leak-allowance assessor", "the meter technician"]},
    "translation agency": {"desc": "a translation agency managing freelance assignments", "deciders": ["the project manager", "the quality reviewer", "the vendor manager"]},
    "nursery": {"desc": "a children's day nursery and its administration", "deciders": ["the nursery manager", "the room leader", "the finance administrator"]},
    "procurement": {"desc": "the procurement team of a university running small tenders", "deciders": ["the procurement officer", "the evaluation panel chair", "the contracts manager"]},
    "call centre QA": {"desc": "a call centre's quality team reviewing agent call records and complaint rates", "deciders": ["the QA analyst", "the team leader", "the complaints escalation reviewer"]},
    "pharmacy dispensing": {"desc": "a community pharmacy's dispensing and prescription-collection desk", "deciders": ["the responsible pharmacist", "the dispensing technician", "the locum pharmacist reviewing the log"]},
    "ride-share support": {"desc": "the rider and driver support team of a city ride-share operator", "deciders": ["the support agent", "the trust-and-safety reviewer", "the refund rule"]},
    "solar installation": {"desc": "a residential solar installer's survey and commissioning team", "deciders": ["the surveyor", "the commissioning engineer", "the sales administrator"]},
    "freight forwarding": {"desc": "a freight forwarder booking sea and road consignments", "deciders": ["the bookings clerk", "the operations manager", "the demurrage rule"]},
    "clinical trial site": {"desc": "the coordinator's office at a clinical trial site handling visit windows and samples", "deciders": ["the study coordinator", "the principal investigator", "the monitor on a site visit"]},
    "university timetabling": {"desc": "a university's timetabling and room-booking office", "deciders": ["the timetabler", "the department administrator", "the room-allocation rule"]},
    "wedding venue": {"desc": "a country wedding venue taking bookings and running events", "deciders": ["the events coordinator", "the venue owner", "the catering manager"]},
    "fishing fleet": {"desc": "a small fishing cooperative's landing office and quota records", "deciders": ["the landing clerk", "the cooperative manager", "the quota-compliance rule"]},
    "parcel locker network": {"desc": "the operations team of a parcel-locker network", "deciders": ["the network controller", "the field technician", "the overdue-collection rule"]},
    "theatre box office": {"desc": "a regional theatre's box office and front of house", "deciders": ["the box office manager", "the duty house manager", "the refund policy"]},
    "cold-chain logistics": {"desc": "a cold-chain distributor moving chilled and frozen goods", "deciders": ["the dispatcher", "the quality manager", "the temperature-excursion rule"]},
}


DOC_KINDS: Dict[str, Dict] = {
    "email thread": {"fmt": "text", "desc": "an email thread of three to six messages between the people involved, with quoted replies, signatures and at least one message that corrects or contradicts an earlier one"},
    "chat log": {"fmt": "text", "desc": "a timestamped chat or ticket log with several short messages from two or three participants, including an unrelated aside"},
    "form submission": {"fmt": "text", "desc": "a submitted form rendered as field labels and values, with some fields blank, some values in the wrong field, and a free-text comments box"},
    "system record": {"fmt": "json", "desc": "a system export of one record as a JSON object with 15 to 40 fields, nested sub-objects, inconsistent key naming, a few null fields, some numbers stored as strings, and a few fields that are irrelevant"},
    "policy extract and case note": {"fmt": "text", "desc": "an extract from an internal policy (with numbered clauses, including at least one exception clause) followed by a short case note describing a specific situation to which it may apply"},
    "incident report": {"fmt": "text", "desc": "an incident or event report with a timeline of times and actions, witness remarks, and a figure that is corrected later in the report"},
    "meeting notes": {"fmt": "text", "desc": "notes of a short meeting with attendees, numbered points, actions, and at least one item where two people disagree on a figure or a date"},
    "statement with cover note": {"fmt": "text", "desc": "a statement, invoice or account summary with line items and totals, followed by a short cover note or complaint from the recipient"},
    "handwritten log transcription": {"fmt": "text", "desc": "a transcription of a handwritten log or diary with uneven entries, abbreviations, a crossed-out value marked [struck through] and a replacement, and one illegible word marked [illegible]"},
    "voicemail and CRM note": {"fmt": "text", "desc": "a voicemail transcript from a customer or colleague (with hesitations and approximate figures) followed by the CRM note the agent wrote afterwards, which does not perfectly match the voicemail"},
}

COMPLICATIONS: List[str] = [
    "a key figure appears twice, once as an initial value and once as a correction, and only the correction is right",
    "a rule with an exception clause whose precondition is stated far from the facts it applies to",
    "a figure that is not stated directly and must be worked out from two others (a difference, a ratio, a percentage, or a time gap)",
    "one important field is missing or left blank, so some decisions cannot be made with certainty",
    "an important figure is given only approximately ('about', 'roughly', 'just under')",
    "a time gap that crosses midnight, a weekend, or a month end",
    "mixed units (for example kilograms and pounds, or minutes and hours) within the same document",
    "several irrelevant numbers of the same kind as the deciding one (other dates, other amounts, other references)",
    "two people state different versions of the same fact and neither is clearly authoritative",
    "a deadline counted in working days rather than calendar days",
    "a policy threshold that the facts land very close to",
    "a long-winded, chatty style with the important detail buried in the middle",
]

COMPUTATIONS: Dict[str, str] = {
    "rate": "a rate: a count of events and a count of opportunities (for example complaints and messages sent, or defects and units inspected) stated separately, never the rate itself",
    "share": "a share of a count: a part and a whole (for example 31 signatures of 40 required) stated separately, never the percentage",
    "time_gap": "a gap between two times or dates, both stated (ideally across midnight, a weekend or a month end), never the duration itself",
    "difference": "a difference between two stated amounts or readings (for example a reading and a limit, or a quote and an invoice), never the difference itself",
    "sum": "a total that must be added up from 2 to 4 stated parts (line amounts, shifts, deliveries), never the total itself",
    "average": "an average of 2 to 4 stated readings or scores, never the average itself",
}

# R19 (train_v3): date and time gaps come in several flavours; one is named per seed that uses a time gap.
TIME_GAP_VARIANTS: List[str] = [
    "a deadline counted in working days, skipping a weekend (and a stated public holiday if natural)",
    "dates given partly by weekday or relative phrase ('the Tuesday after', 'ten days before the 14th', 'next Friday') that must be turned into calendar dates",
    "a time gap that crosses midnight (for example a shift or an event running from late evening into the next morning)",
    "a deadline to the minute or second (for example a cut-off of 17:00 and an event logged at 17:01:47)",
    "times written in mixed formats within the same document (24-hour clock, am/pm, and written-out times)",
    "a gap that crosses a month end or a weekend in calendar days",
]

# R19: choice questions mostly need a calculation across the options or a rule with an exception.
CHOICE_PATTERNS: Dict[str, str] = {
    "cheapest_after_adjustment": "several (4 to 5) alternatives, each with a price or cost and its own discount, surcharge, minimum or fee, so that the cheapest only shows after working each one out",
    "only_one_meets_all": "several (4 to 5) candidates (suppliers, applicants, vehicles, rooms, contractors) each checked against 3 or 4 stated conditions, where only one meets every condition and the others each fail on a different one",
    "earliest_feasible": "several (4 to 5) possible slots, dates or routes, each with its own constraint (lead time, opening hours, capacity, notice period), so that the earliest feasible one needs each constraint checked",
    "largest_or_smallest_computed": "several (4 to 5) items (sites, shifts, batches, accounts) for each of which a rate, total or average must be worked out from stated parts before they can be ranked",
    "rule_with_exception": "a stated rule with numbered clauses and at least one exception clause, where the right outcome among 4 to 5 possible outcomes depends on whether the exception's precondition holds",
}

MARGIN_BANDS: List[str] = ["close", "moderate", "far"]
# R19: at least a third of computed score questions within 5% of a level edge. The writer lands the requested
# band only about a third of the time (train_v2), so the request is weighted towards "close".
MARGIN_WEIGHTS = [0.55, 0.25, 0.20]

CLARITY: List[str] = ["mostly clear", "mixed", "mostly debatable"]
CLARITY_WEIGHTS = [0.45, 0.35, 0.20]

NON_TIME_COMPUTATIONS = [c for c in COMPUTATIONS if c != "time_gap"]


def make_seed(rng: random.Random, idx: int) -> dict:
    domain = rng.choice(list(DOMAINS))
    d = DOMAINS[domain]
    kinds = list(DOC_KINDS)
    weights = [3.9 if k == "system record" else 1.0 for k in kinds]  # roughly 30% JSON records
    kind = rng.choices(kinds, weights)[0]
    comps = rng.sample(COMPLICATIONS, rng.randint(1, 3))
    clarity = rng.choices(CLARITY, CLARITY_WEIGHTS)[0]
    n_q = rng.choice([4, 4, 5, 5, 5, 6])
    # R19 type composition: about 45% score, 40% choice, 15% noul
    n_noul = 1 if rng.random() < 0.72 else 0
    rest = n_q - n_noul
    n_score = int(rest * 0.53 + rng.random())
    n_score = min(max(n_score, 1), rest - 1)
    n_choice = rest - n_score
    # R19: date or time gaps in about a third of computed questions
    if rng.random() < 0.62:
        comps_plan = ["time_gap", rng.choice(NON_TIME_COMPUTATIONS)]
        rng.shuffle(comps_plan)
        time_variant = rng.choice(TIME_GAP_VARIANTS)
    else:
        comps_plan = rng.sample(NON_TIME_COMPUTATIONS, 2)
        time_variant = None
    stated_band = rng.random() < 0.08  # R19: bands are nearly solved, so stated-value band questions are rare
    # R19: mostly 4-5 levels; each score question is computed, or (about one in six) decided by a stated rule with its exception
    score_plan = []
    for i in range(n_score):
        levels = rng.choice([3, 4, 4, 5, 5])
        if stated_band and i == n_score - 1:
            score_plan.append({"decider": "stated", "levels": levels, "margin": rng.choices(MARGIN_BANDS, MARGIN_WEIGHTS)[0]})
        elif rng.random() < 0.17:
            score_plan.append({"decider": "rule", "levels": levels, "margin": None})
        else:
            score_plan.append({"decider": comps_plan[i % 2], "levels": levels, "margin": rng.choices(MARGIN_BANDS, MARGIN_WEIGHTS)[0]})
    # R19: choice mostly 4-5 options, picking the answer needs a calculation across options or a rule with an exception
    choice_plan = [{"pattern": rng.choice(list(CHOICE_PATTERNS)), "options": rng.choice([3, 4, 4, 5, 5])} for _ in range(n_choice)]
    if len(choice_plan) == 2 and choice_plan[0]["pattern"] == choice_plan[1]["pattern"]:
        choice_plan[1]["pattern"] = rng.choice([p for p in CHOICE_PATTERNS if p != choice_plan[0]["pattern"]])
    return {
        "seed_id": f"X{idx:04d}",
        "n_score": n_score, "n_noul": n_noul, "n_choice": n_choice,
        "computations": comps_plan,
        "computation_desc": [COMPUTATIONS[c] for c in comps_plan],
        "time_gap_variant": time_variant,
        "stated_band": stated_band,
        "margins": [sp["margin"] for sp in score_plan],
        "score_plan": score_plan,
        "choice_plan": choice_plan,
        "choice_desc": [CHOICE_PATTERNS[c["pattern"]] for c in choice_plan],
        "domain": domain,
        "domain_desc": d["desc"],
        "decider": rng.choice(d["deciders"]),
        "doc_kind": kind,
        "doc_desc": DOC_KINDS[kind]["desc"],
        "form": DOC_KINDS[kind]["fmt"],
        "complications": comps,
        "clarity": clarity,
        "length_words": rng.choice([220, 260, 300, 360, 420]),
        "n_questions": n_q,
    }


def make_seeds(n: int, seed: int = 20261029) -> List[dict]:
    rng = random.Random(seed)
    return [make_seed(rng, i + 1) for i in range(n)]


if __name__ == "__main__":
    import json
    for s in make_seeds(5):
        print(json.dumps(s, indent=1))
