"""Seed list for the score-only augmentation (independent_v5_score_aug): five flows, four score questions per case.

Domains, document kinds and complications are train_v2's: domain x decider x document kind x complications.

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

COMPUTATIONS.update({
    "ratio": "a ratio or percentage with an explicit denominator (for example passed items over items tested, or cost over budget), both parts stated separately, never the ratio itself",
    "change": "a change between two periods or readings (direction and size, absolute or percentage), both values stated, never the change itself",
    "aggregate": "an aggregate over 3 to 6 observations under a stated rule (for example the mean excluding a voided reading, or the count of days above a limit), never the result itself",
    "conversion": "a quantity that must be converted between units or time bases (per week to per month, minutes to hours, pounds to kilograms) before it can be compared, never the converted value",
})

FLOWS = {
    "F1": {
        "name": "Evidence-based scoring",
        "doc": "The document must contain several separate pieces of evidence bearing on at least four different properties of the situation (for example quality of work, risk to a person, completeness of a submission, customer impact, reliability of a supplier). Mix qualitative evidence (remarks, observations, complaints, praise) with structured observations (counts, readings, dates), and mix in plausible but irrelevant details. Some properties should come out clearly low, some in the middle, some high.",
        "q": "F1 EVIDENCE-BASED SCORING: each question names a property and its scale; the right level follows from identifying and combining the relevant pieces of evidence in the document and weighing them against the level descriptions, not from a single keyword. Include short inferences as well as direct reading.",
        "kinds": {"read": 0.45, "infer": 0.20, "compare": 0.05, "judge": 0.30},
        "complications": 1,
    },
    "F2": {
        "name": "Boundary and adjacent-level discrimination",
        "doc": "The document must contain several figures, counts, dates or facts that sit close to a limit or a natural boundary (just under, exactly at, or just over), and at least one stated rule or rubric with explicit inclusive or exclusive thresholds, plus qualitative facts that sit between two descriptions (for example 'partly resolved', 'one of three conditions not met').",
        "q": "F2 BOUNDARY DISCRIMINATION: each question is decided near a level boundary. For numeric scales write explicit, non-overlapping edges with inclusive/exclusive wording, units, rounding and time window; place the edges so the document's value is just below, exactly at, or just above an edge as planned. For non-numeric scales, write level descriptions that differ by one decisive condition. Middle levels should be correct as often as extremes.",
        "kinds": {"read": 0.10, "infer": 0.15, "compare": 0.45, "judge": 0.30},
        "complications": 1,
        "twins": True,
    },
    "F3": {
        "name": "Conflicting evidence",
        "doc": "The document must contain conflicting evidence: strong positive indicators alongside at least one material negative signal; a recent period that differs from the earlier history (better or worse); observations from two sources that disagree; and criteria that pull in different directions. If the organisation has a rule about which criterion takes priority or how criteria are weighted, state it explicitly in the document.",
        "q": "F3 CONFLICTING EVIDENCE: each question rates a property where different facts point to different levels. The instruction or the level descriptions must say how evidence is to be weighed whenever the answer depends on it (which period counts, which criterion takes priority, or that the overall balance is to be judged); never rely on an unstated weighting rule. It is right that some questions remain genuinely split between two neighbouring levels.",
        "kinds": {"read": 0.10, "infer": 0.20, "compare": 0.10, "judge": 0.60},
        "complications": 2,
    },
    "F4": {
        "name": "Missing, incomplete or uncertain evidence",
        "doc": "The document must have gaps of different kinds: at least one required field missing or blank while other evidence is present; a record that covers only part of the period in question; a small number of observations; one stale observation alongside fresher ones; and at least one statement whose confidence is explicitly limited ('provisional', 'estimated', 'not yet verified').",
        "q": "F4 MISSING OR UNCERTAIN EVIDENCE: each question rates a property for which some of the evidence is missing, partial, stale, small-sample or provisional. Every scale must say how missing or insufficient evidence is treated: either a level that explicitly means 'not enough evidence to rate higher' or 'cannot be confirmed', or a stated rule such as 'missing readings count as failures' or 'rate on the observations available if at least three exist'. Never leave missingness to assumption, and keep 'the quantity is low' distinct from 'there is not enough evidence'.",
        "kinds": {"read": 0.25, "infer": 0.25, "compare": 0.10, "judge": 0.40},
        "complications": 1,
    },
    "F5": {
        "name": "Numerical and quantitative reasoning",
        "doc": "The document must contain the raw inputs for several calculations, stated as separate facts in different places and never with the results: percentages and ratios with explicit denominators, comparisons across entities or periods, aggregation of several observations under a stated rule, a trend or change between periods, and at least one quantity in a different unit or time base from the one a decision would use.",
        "q": "F5 NUMERICAL REASONING: each question's level is decided by a value that must be worked out from the document's inputs, and at least two of the four need more than one step (for example a ratio of two sums, a change in a rate between periods, an average after excluding a voided reading, or a conversion followed by a comparison). Each scale states units, denominator, rounding rule, time window and inclusive/exclusive edges. Not every question may be a single threshold lookup.",
        "kinds": {"read": 0.10, "infer": 0.30, "compare": 0.55, "judge": 0.05},
        "complications": 1,
        "computations": ["rate", "share", "time_gap", "difference", "sum", "average", "ratio", "change", "aggregate", "conversion"],
    },
}

FLOW_COMPLICATIONS = {
    "F1": [COMPLICATIONS[i] for i in (0, 7, 11, 8, 6)],
    "F2": [COMPLICATIONS[i] for i in (10, 5, 9, 4, 0)],
    "F3": [COMPLICATIONS[i] for i in (8, 0, 1, 7, 11)],
    "F4": [COMPLICATIONS[i] for i in (3, 4, 7, 11, 5)],
    "F5": [COMPLICATIONS[i] for i in (2, 6, 5, 7, 9, 10)],
}

LEVELS = [3, 4, 5]
LEVEL_WEIGHTS = [0.40, 0.35, 0.25]
SEEDS_PER_FLOW = 130


def _target_level(rng: random.Random, n_levels: int) -> int:
    # every level, extremes and middle, gets credible examples
    return rng.randrange(n_levels)


def make_seed(rng: random.Random, flow: str, idx: int) -> dict:
    f = FLOWS[flow]
    domain = rng.choice(list(DOMAINS))
    d = DOMAINS[domain]
    kinds = list(DOC_KINDS)
    weights = [9.0 if k == "system record" else 1.0 for k in kinds]  # about 50% JSON records
    kind = rng.choices(kinds, weights)[0]
    comps = rng.sample(FLOW_COMPLICATIONS[flow], f["complications"])
    qplan = []
    kind_names, kind_w = list(f["kinds"]), list(f["kinds"].values())
    for _ in range(4):
        n = rng.choices(LEVELS, LEVEL_WEIGHTS)[0]
        qplan.append({"levels": n, "kind": rng.choices(kind_names, kind_w)[0], "target_level": _target_level(rng, n)})
    comp_plan = rng.sample(f["computations"], 3) if f.get("computations") else []
    return {
        "seed_id": f"{flow}-{idx:04d}",
        "flow": flow,
        "flow_name": f["name"],
        "question_plan": qplan,
        "computations": comp_plan,
        "computation_desc": [COMPUTATIONS[c] for c in comp_plan],
        "domain": domain,
        "domain_desc": d["desc"],
        "decider": rng.choice(d["deciders"]),
        "doc_kind": kind,
        "doc_desc": DOC_KINDS[kind]["desc"],
        "form": DOC_KINDS[kind]["fmt"],
        "complications": comps,
        "length_words": rng.choice([240, 280, 320, 380, 440]),
        # F2: odd-numbered seeds are bases, the next even seed is its twin (one decisive fact changed)
        "twin_of": f"{flow}-{idx - 1:04d}" if f.get("twins") and idx % 2 == 0 else None,
    }


def make_seeds(n_per_flow: int = SEEDS_PER_FLOW, seed: int = 20261030) -> List[dict]:
    out = []
    for fi, flow in enumerate(FLOWS):
        rng = random.Random(seed * 10 + fi)
        out.extend(make_seed(rng, flow, i + 1) for i in range(n_per_flow))
    return out


if __name__ == "__main__":
    import collections
    S = make_seeds()
    print(len(S), collections.Counter(s["form"] for s in S))
    print(collections.Counter(q["levels"] for s in S for q in s["question_plan"]))
    print(collections.Counter(q["kind"] for s in S for q in s["question_plan"]))
