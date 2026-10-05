"""Generic (non-banking) router training data for modernbert.ipynb.

Run from the repo root: python data/modernbert_router/build_generic_router_data.py

27 domains, each with its own five agents (one deliberately close pair + one general agent).
None of the domains or agents relate to the banking test agents (Payments, Card Support, Investment,
Insurance, General Customer Support). There is no fixed train/validation split: the notebook validates
by leaving whole domains out.
Every conversation ends with a user message; the label is the agent that should handle that message.
current_agent is the agent that spoke the last assistant message (None for a fresh conversation): it is the
agent "holding" the conversation when the router is called, and it is often NOT the right answer (handoffs,
topic changes), so the router must learn when to stay and when to switch.
context_change says whether the LAST user message moves the conversation to a different topic (True), or
continues the current one (False: follow-ups, short answers, "ok" after a handoff); None for a fresh conversation.
"""
import json
import random

rng = random.Random(42)

DOMAINS = {
"it_helpdesk": {
  "close_pair": ["Password & Access Agent", "Network & VPN Agent"],
  "agents": {
    "Password & Access Agent": ("Handles password resets, account lockouts, multi-factor authentication codes, sign-in errors and access permissions to systems and shared folders.",
      ["I forgot my password.", "My account is locked out.", "I need access to the finance shared folder.", "The two-factor code never arrives.", "pls reset my password", "I can't sign in, it says wrong password.", "I need admin rights on the CRM.", "My login keeps getting rejected."]),
    "Network & VPN Agent": ("Handles Wi-Fi and office network problems, VPN connections, slow or dropped internet and remote network access.",
      ["The VPN keeps disconnecting.", "Wi-Fi in the meeting room is not working.", "internet is super slow today", "I can't connect to the office network from home.", "The VPN client times out.", "There is no network on my desk port.", "my connection drops every few minutes", "The guest Wi-Fi password doesn't work."]),
    "Hardware Agent": ("Handles laptops, monitors, keyboards, printers, docking stations, broken devices and hardware replacements.",
      ["My laptop screen is cracked.", "The printer on floor 3 is jammed.", "I need a second monitor.", "my keyboard stopped working", "The docking station doesn't charge my laptop.", "My mouse is broken.", "The laptop fan is extremely loud.", "I spilled coffee on my laptop."]),
    "Software Installation Agent": ("Handles installing, updating and licensing software applications, and applications that crash or won't start.",
      ["I need Photoshop installed.", "Excel crashes when I open big files.", "Can you update Zoom on my laptop?", "my license for the design tool expired", "Please install Python on my machine.", "The reporting app won't start after the update.", "I need the latest version of Teams.", "The PDF editor shows a license error."]),
    "General IT Support Agent": ("Handles general IT questions, requests that do not clearly belong to a specialist, and routing people to the right IT team.",
      ["I have a general IT question.", "Who do I ask about IT stuff?", "I need help with something on my computer.", "Can someone from IT help me?", "I'm new here and have an IT question.", "not sure which IT team I need"]),
  },
  "topics": {"Password & Access Agent": "password", "Network & VPN Agent": "VPN", "Hardware Agent": "printer", "Software Installation Agent": "software", "General IT Support Agent": "IT question"},
  "ambiguous": {"opener": ["I can't get into the VPN.", "Remote login isn't working.", "I can't reach the system from home."],
                "clarify": ["Is it a password or access problem, or does the connection itself fail?", "Does it reject your login, or does the connection not come up at all?"],
                "resolve": {"Password & Access Agent": ["It says my password is wrong.", "My account is locked.", "it rejects my login"],
                            "Network & VPN Agent": ["The connection drops before I can even log in.", "It just times out.", "the connection never comes up"]}},
},
"hr": {
  "close_pair": ["Recruitment Agent", "Onboarding Agent"],
  "agents": {
    "Leave & Holidays Agent": ("Handles annual leave requests, sick leave, holiday balances, parental leave and time-off approvals.",
      ["I want to book two weeks of annual leave.", "How many holidays do I have left?", "I'm sick today and need to log sick leave.", "how do i apply for parental leave", "My leave request is still pending approval.", "Can I carry over unused leave?", "I need a day off on Friday.", "My holiday balance looks wrong."]),
    "Recruitment Agent": ("Handles job openings, job applications, interviews, candidate referrals and hiring status.",
      ["I want to apply for the data analyst opening.", "When is my second interview?", "I'd like to refer a friend for a job.", "status of my job application?", "Are there any open roles in marketing?", "I need to reschedule my interview.", "We need to hire two more engineers.", "Has the candidate accepted the interview slot?"]),
    "Onboarding Agent": ("Handles new joiner onboarding after an offer is accepted: first-day setup, welcome sessions, onboarding documents and start-date logistics.",
      ["I start next Monday, what happens on my first day?", "I haven't received my onboarding documents.", "When is the welcome session for new joiners?", "my new team member starts tomorrow, is everything ready?", "Who is my onboarding buddy?", "What should I bring on my first day?", "Can my start date move by a week?", "The new joiner checklist is missing."]),
    "Training & Learning Agent": ("Handles training courses, certifications, learning budgets and mandatory compliance trainings.",
      ["I want to enroll in the leadership course.", "How much is my learning budget?", "I need to finish the mandatory compliance training.", "can i get a certification covered", "Which courses are available this quarter?", "My training certificate is missing.", "Is there a course on public speaking?", "I failed the compliance quiz, can I retake it?"]),
    "General HR Support Agent": ("Handles general HR questions, policies that do not clearly belong to a specialist, and routing people to the right HR team.",
      ["I have a question about HR.", "Who can help me with a policy question?", "I need some HR help.", "Where do I find the employee handbook?", "general question about company policy", "not sure who in HR to ask"]),
  },
  "topics": {"Leave & Holidays Agent": "leave", "Recruitment Agent": "interview", "Onboarding Agent": "first day", "Training & Learning Agent": "training", "General HR Support Agent": "policy question"},
  "ambiguous": {"opener": ["It's about the new hire on my team.", "I have a question about our new person.", "This is about someone joining the team."],
                "clarify": ["Is the person still in the hiring process, or have they accepted and are about to start?", "Are we still hiring them, or are they already joining?"],
                "resolve": {"Recruitment Agent": ["Still interviewing, I need to schedule the final round.", "We haven't made an offer yet.", "still in interviews"],
                            "Onboarding Agent": ["They accepted, they start on Monday.", "She joins next week and her first day needs planning.", "already signed, starting soon"]}},
},
"airline": {
  "close_pair": ["Flight Booking Agent", "Check-in & Seating Agent"],
  "agents": {
    "Flight Booking Agent": ("Handles new flight bookings, date and route changes, cancellations and rebooking of flights.",
      ["I want to book a flight to Lisbon.", "Can I change my flight to Friday?", "Please cancel my booking.", "i need to move my flight a day earlier", "I missed my flight, can you rebook me?", "Is there a later flight to Rome?", "I want to fly via Paris instead.", "Book me a return trip to Berlin."]),
    "Check-in & Seating Agent": ("Handles online check-in, boarding passes, seat selection, upgrades at check-in and travel document checks at check-in.",
      ["I can't check in online.", "My boarding pass won't download.", "I want to change my seat to a window.", "can i get an upgrade at check in", "Check-in says my passport details are invalid.", "When does online check-in open?", "I want to sit next to my wife.", "My boarding pass shows the wrong name."]),
    "Baggage Agent": ("Handles checked and cabin baggage allowance, lost or delayed bags, damaged luggage and extra baggage.",
      ["My suitcase didn't arrive.", "How much luggage can I take?", "My bag was damaged on the flight.", "can i add an extra bag", "Is a guitar allowed as cabin baggage?", "My luggage is delayed, where is it?", "The handle of my suitcase broke.", "What is the weight limit for checked bags?"]),
    "Special Assistance Agent": ("Handles wheelchair assistance, travelling with infants, medical needs, pets on board and unaccompanied minors.",
      ["I need a wheelchair at the airport.", "I'm travelling with a newborn.", "Can I bring my dog on board?", "my son will fly alone, he is 10", "I need to carry insulin on the plane.", "My mother needs help boarding.", "Can I bring a car seat for my baby?", "I need oxygen during the flight."]),
    "General Travel Support Agent": ("Handles general travel questions, requests that do not clearly belong to a specialist, and routing people to the right team.",
      ["I have a travel question.", "Who can help me with my trip?", "I need some help with travel.", "Can someone answer a general question?", "general question about flying with you", "not sure who handles this"]),
  },
  "topics": {"Flight Booking Agent": "flight", "Check-in & Seating Agent": "seat", "Baggage Agent": "luggage", "Special Assistance Agent": "wheelchair", "General Travel Support Agent": "travel question"},
  "ambiguous": {"opener": ["I need to change something about my flight.", "There's a problem with my trip next week.", "Something about my flight is wrong."],
                "clarify": ["Do you want to change the flight itself, or your seat and check-in details?", "Is it the flight booking, or the seat and boarding pass?"],
                "resolve": {"Flight Booking Agent": ["The flight itself, I need a different date.", "The route, I want to fly via Paris.", "the booking, different day"],
                            "Check-in & Seating Agent": ["Just my seat, I want an aisle.", "The check-in details, my boarding pass is wrong.", "only the seat"]}},
},
"clinic": {
  "close_pair": ["Prescriptions Agent", "Pharmacy Delivery Agent"],
  "agents": {
    "Appointments Agent": ("Handles booking, rescheduling and cancelling doctor appointments and finding available doctors.",
      ["I need an appointment with a dermatologist.", "Can I move my appointment to next week?", "Please cancel my appointment tomorrow.", "is dr. mehta available on monday", "I want to see a doctor this week.", "I missed my appointment, can I rebook?", "I need a follow-up visit.", "Is there an evening slot with a GP?"]),
    "Prescriptions Agent": ("Handles prescription renewals, dosage questions, medication changes and repeat prescriptions.",
      ["I need to renew my prescription.", "Can my dosage be increased?", "My doctor wants to change my medication.", "repeat prescription for my inhaler pls", "Is it safe to take these two medicines together?", "My prescription ran out.", "The new tablets give me headaches.", "I need a prescription for my allergy pills."]),
    "Pharmacy Delivery Agent": ("Handles delivery of medicines: delivery status, missed deliveries, delivery addresses and damaged medicine parcels.",
      ["My medicine delivery hasn't arrived.", "Where is my medication parcel?", "Can you deliver my pills to my office instead?", "the delivery guy missed me", "When will my medicines be delivered?", "My medication package was left outside.", "The parcel arrived open.", "I want a delivery slot after 6pm."]),
    "Lab Results Agent": ("Handles blood test and lab results, explaining test values, scheduling lab tests and missing results.",
      ["Are my blood test results ready?", "What does a high cholesterol result mean?", "I need to book a blood test.", "my lab results are missing", "Can someone explain my thyroid results?", "When do I get my test results?", "Do I need to fast before the blood test?", "My results show a red flag."]),
    "General Patient Support Agent": ("Handles general patient questions, requests that do not clearly belong to a specialist, and routing patients to the right team.",
      ["I have a question for the clinic.", "Who can help me as a patient?", "I need some help please.", "Can someone answer a general question?", "general question about the clinic", "not sure who to ask here"]),
  },
  "topics": {"Appointments Agent": "appointment", "Prescriptions Agent": "prescription", "Pharmacy Delivery Agent": "delivery", "Lab Results Agent": "test results", "General Patient Support Agent": "general question"},
  "ambiguous": {"opener": ["It's about my medicine.", "There's a problem with my tablets.", "I have an issue with my medication."],
                "clarify": ["Is it about the prescription itself, or about the delivery of the medicine?", "Is this about what you were prescribed, or about getting it delivered?"],
                "resolve": {"Prescriptions Agent": ["The prescription, it has expired.", "The dosage, I think it's too low.", "the prescription itself"],
                            "Pharmacy Delivery Agent": ["The delivery, it never came.", "The parcel, it went to my old address.", "getting it delivered"]}},
},
"food_delivery": {
  "close_pair": ["Order Status Agent", "Delivery Address Agent"],
  "agents": {
    "Order Status Agent": ("Handles where an order is, delivery time estimates, late orders and order tracking.",
      ["Where is my order?", "My food is 40 minutes late.", "How long until my order arrives?", "the tracker hasn't moved", "Has the restaurant started my order?", "My order says delivered but I don't have it.", "Why is my order still preparing?", "Is my order on the way?"]),
    "Delivery Address Agent": ("Handles changing the delivery address, delivery instructions, wrong addresses and drop-off locations.",
      ["I need to change my delivery address.", "Please tell the rider to use the back door.", "I entered the wrong address.", "deliver to my office instead", "Can you add a gate code to my delivery?", "The rider can't find my building.", "Leave it with the reception please.", "My flat number is missing from the address."]),
    "Restaurant & Menu Agent": ("Handles menu items, ingredients and allergens, restaurant opening hours and dish availability.",
      ["Does the pad thai contain peanuts?", "Is the pizza place open now?", "Is the vegan burger still available?", "what's in the house salad", "Which dishes are gluten free?", "When does the sushi place close?", "Is the curry very spicy?", "Do they have a kids menu?"]),
    "App Settings Agent": ("Handles app login, profile details, notifications and saved preferences in the app.",
      ["I can't log into the app.", "How do I change my phone number in the app?", "Turn off the promo notifications.", "update my profile name", "My saved preferences disappeared.", "How do I switch the app to dark mode?", "The app keeps logging me out.", "Change the language of the app."]),
    "General Customer Help Agent": ("Handles general questions, requests that do not clearly belong to a specialist, and routing customers to the right team.",
      ["I have a general question.", "Who can help me?", "I need some help with the app.", "Can someone help me out?", "general question about your service", "not sure who handles this"]),
  },
  "topics": {"Order Status Agent": "order", "Delivery Address Agent": "address", "Restaurant & Menu Agent": "menu", "App Settings Agent": "app settings", "General Customer Help Agent": "general question"},
  "ambiguous": {"opener": ["There's a problem with my delivery.", "Something's wrong with my food delivery.", "My delivery isn't going well."],
                "clarify": ["Is your order late, or does the delivery address or drop-off need changing?", "Is it the timing of the order, or where it should be delivered?"],
                "resolve": {"Order Status Agent": ["It's late, the tracker hasn't moved.", "It's been an hour and nothing.", "the timing, it's late"],
                            "Delivery Address Agent": ["The address is wrong, I moved.", "The rider needs to come to the back entrance.", "where it goes, wrong address"]}},
},
"university": {
  "close_pair": ["Course Registration Agent", "Exams & Timetable Agent"],
  "agents": {
    "Admissions Agent": ("Handles applications, entry requirements, admission decisions and application documents.",
      ["I want to apply for the master's program.", "What are the entry requirements for medicine?", "Has my application been decided?", "do you need my transcripts", "Can I still submit my application?", "My admission letter has a typo.", "Is there an application deadline for spring?"]),
    "Course Registration Agent": ("Handles enrolling in courses, adding or dropping modules, waitlists and credit limits.",
      ["I want to add a statistics module.", "Can I drop the history course?", "I'm on the waitlist for biology.", "how many credits can i take", "Registration won't let me enroll in chemistry.", "I need to switch my elective.", "Can I take an extra course this term?"]),
    "Exams & Timetable Agent": ("Handles exam dates, timetables, lecture rooms, exam clashes and resits.",
      ["When is my calculus exam?", "Two of my exams are at the same time.", "Where is my timetable?", "can i resit the physics exam", "Which room is the final in?", "My timetable shows the wrong lecture time.", "Is the exam online or on campus?"]),
    "Student Housing Agent": ("Handles dormitory applications, room assignments, housing maintenance and moving in.",
      ["I need a dorm room for next semester.", "The heating in my room is broken.", "When can I move into my dorm?", "can i change roommates", "I haven't got a room assignment yet.", "My dorm key doesn't work.", "Is there housing for couples?"]),
    "General Student Support Agent": ("Handles general student questions, requests that do not clearly belong to a specialist, and routing students to the right office.",
      ["I have a general student question.", "Who can help me as a student?", "I need some help with university stuff.", "Can someone answer a quick question?", "not sure which office to ask"]),
  },
  "topics": {"Admissions Agent": "application", "Course Registration Agent": "course", "Exams & Timetable Agent": "exam", "Student Housing Agent": "dorm", "General Student Support Agent": "general question"},
  "ambiguous": {"opener": ["It's about one of my courses.", "I have a problem with my biology course.", "Something's off with my course."],
                "clarify": ["Is it about enrolling in the course, or about its exams and timetable?", "Do you mean registration, or the exam and lecture schedule?"],
                "resolve": {"Course Registration Agent": ["Enrolling, I can't get in.", "I want to drop it.", "registration"],
                            "Exams & Timetable Agent": ["The exam date clashes with another.", "I can't find when the lectures are.", "the exam schedule"]}},
},
"car_service": {
  "close_pair": ["Service Booking Agent", "Repairs & Diagnostics Agent"],
  "agents": {
    "Service Booking Agent": ("Handles booking, rescheduling and cancelling car service appointments and inspections.",
      ["I want to book my annual service.", "Can I move my service appointment to Thursday?", "Please cancel my inspection.", "book a service for next week", "When is my next service due?", "Is there a slot on Saturday?", "I need an oil change appointment."]),
    "Repairs & Diagnostics Agent": ("Handles warning lights, strange noises, fault diagnosis and the status of ongoing repairs.",
      ["The engine warning light is on.", "My brakes make a squealing noise.", "What's wrong with my gearbox?", "is my car repair done yet", "The car shakes at high speed.", "The mechanic found something, what does it mean?", "There's a burning smell from the engine."]),
    "Parts Agent": ("Handles spare parts availability, tyre orders, accessories and part delivery times.",
      ["Do you have winter tyres in stock?", "I need a new side mirror.", "When will my ordered part arrive?", "can i buy roof racks", "Is the brake pad for my model available?", "I want original wiper blades.", "Do you sell floor mats for my car?"]),
    "Roadside Assistance Agent": ("Handles breakdowns on the road, flat tyres, towing and emergency help.",
      ["My car broke down on the highway.", "I have a flat tyre and no spare.", "I need a tow truck.", "car wont start, im stuck", "I locked my keys in the car.", "My battery is dead in the parking lot.", "I ran out of fuel on the motorway."]),
    "General Customer Service Agent": ("Handles general customer questions, requests that do not clearly belong to a specialist, and routing customers to the right team.",
      ["I have a general question.", "Who can help me with my car?", "I need some help please.", "Can someone answer a quick question?", "not sure who handles this"]),
  },
  "topics": {"Service Booking Agent": "service appointment", "Repairs & Diagnostics Agent": "warning light", "Parts Agent": "parts", "Roadside Assistance Agent": "breakdown", "General Customer Service Agent": "general question"},
  "ambiguous": {"opener": ["Something is wrong with my car and I need it looked at.", "My car needs attention.", "I need you to look at my car."],
                "clarify": ["Do you want to book a workshop slot, or should we first diagnose the problem?", "Should I book it in, or do you want to know what's wrong first?"],
                "resolve": {"Service Booking Agent": ["Just book a slot, I know it needs a service.", "Book it in for Tuesday.", "book it"],
                            "Repairs & Diagnostics Agent": ["Diagnose it, there's a weird noise.", "Tell me what the warning light means first.", "figure out what's wrong"]}},
},
}


def _domain(close, agents, opener, clarify, resolve_a, resolve_b):
    """Compact domain spec: agents = [(name, description, [intents], topic), ...]; close = (agent_a, agent_b)."""
    return {"close_pair": list(close),
            "agents": {n: (d, i) for n, d, i, _ in agents},
            "topics": {n: t for n, _, _, t in agents},
            "ambiguous": {"opener": opener, "clarify": clarify, "resolve": {close[0]: resolve_a, close[1]: resolve_b}}}


def _general(name, who):
    return (name, f"Handles general {who} questions, requests that do not clearly belong to a specialist, and routing people to the right team.",
            [f"I have a general {who} question.", "Who can help me with this?", "I need some help please.", "not sure who handles this"], "general question")


NEW_DOMAINS = {
"hotel": _domain(("Reservations Agent", "Front Desk & Check-in Agent"), [
    ("Reservations Agent", "Handles room bookings, date changes, cancellations, room types and group reservations.",
     ["I want to book a double room for three nights.", "Can I change my stay to next weekend?", "Please cancel my reservation.", "do you have a suite available in june", "I need five rooms for a team offsite."], "reservation"),
    ("Front Desk & Check-in Agent", "Handles check-in and check-out times, early arrival, late checkout, room keys and arrival details.",
     ["What time is check-in?", "Can I get a late checkout tomorrow?", "My room key stopped working.", "we arrive at 6am can we check in early", "I'll arrive after midnight, is the desk open?"], "check-in"),
    ("Housekeeping Agent", "Handles room cleaning, extra towels and pillows, toiletries and laundry service.",
     ["Can I get extra towels?", "Please clean my room now.", "We need another pillow.", "is there a laundry service", "The bathroom has no soap."], "towels"),
    ("Concierge Agent", "Handles restaurant recommendations, local tours, taxis, attraction tickets and city tips.",
     ["Can you recommend a seafood restaurant nearby?", "Book me a taxi to the airport.", "Are there any city tours tomorrow?", "whats worth seeing around here", "Can you get us museum tickets?"], "taxi"),
    _general("General Guest Support Agent", "guest")],
    ["I need to change something about my stay.", "Something about my room and arrival needs sorting."],
    ["Do you want to change the booking dates or room, or your arrival and check-in times?", "Is it the reservation itself, or your check-in or checkout?"],
    ["The booking, I need different dates.", "a bigger room type"], ["Just a late checkout.", "I'll arrive early and want to check in"]),
"mobile_network": _domain(("Network Coverage Agent", "SIM & eSIM Agent"), [
    ("Network Coverage Agent", "Handles no signal, slow mobile data, dropped calls, outages and coverage in an area.",
     ["I have no signal at home.", "Mobile data is really slow today.", "My calls keep dropping.", "is there an outage in my area", "No coverage in the new office."], "signal"),
    ("SIM & eSIM Agent", "Handles SIM activation, eSIM setup, lost SIMs, SIM swaps and PIN or PUK codes.",
     ["My new SIM isn't activated.", "How do I set up an eSIM on my phone?", "I lost my SIM and need a replacement.", "it asks for a puk code", "I want to move my number to an eSIM."], "sim"),
    ("Device Repair Agent", "Handles broken phones, screen repairs, battery problems and repair status.",
     ["My phone screen is cracked.", "The battery drains in two hours.", "When will my repaired phone be ready?", "phone wont turn on", "The charging port is loose."], "screen"),
    ("Roaming Agent", "Handles using the phone abroad, roaming activation and roaming data problems.",
     ["Will my phone work in Spain?", "Roaming data doesn't work abroad.", "How do I turn on roaming?", "no network since i landed in dubai", "Can I call home while travelling?"], "roaming"),
    _general("General Mobile Support Agent", "mobile")],
    ["My phone has no service.", "I can't use my phone network."],
    ["Is it a coverage problem in your area, or is your SIM or eSIM not working?", "Does the network fail everywhere, or does the phone say no SIM?"],
    ["Only at home, the signal is weak.", "everyone in my area has no signal"], ["It says no SIM detected.", "the esim never activated"]),
"rentals": _domain(("Viewings Agent", "Lease & Contracts Agent"), [
    ("Viewings Agent", "Handles booking and rescheduling property viewings, open houses and virtual tours.",
     ["I want to view the two-bedroom flat.", "Can I move my viewing to Saturday?", "Is there a virtual tour of the house?", "book a viewing tomorrow pls", "When is the next open house?"], "viewing"),
    ("Lease & Contracts Agent", "Handles rental agreements, lease renewals, contract terms, notice periods and move-in dates.",
     ["I want to renew my lease.", "What is the notice period in my contract?", "Can I add my partner to the lease?", "when does my contract end", "I need a copy of my rental agreement."], "lease"),
    ("Maintenance Requests Agent", "Handles repairs in rented homes: leaks, broken heating, appliances and repair visits.",
     ["The kitchen tap is leaking.", "Heating in the flat is broken.", "When is the repair person coming?", "mould in the bathroom", "The oven in the flat doesn't work."], "repair"),
    ("Neighbourhood Info Agent", "Handles questions about the area: schools, transport, parking and local amenities.",
     ["Are there good schools nearby?", "How far is the station from the flat?", "Is there parking on the street?", "whats the area like at night", "Are there supermarkets close by?"], "area"),
    _general("General Tenant Support Agent", "tenant")],
    ["I'm interested in the flat on Park Street.", "About the apartment I looked at."],
    ["Do you want to see the property, or are you ready to discuss the rental contract?", "Is this about a viewing, or about the lease terms?"],
    ["I'd like to see it first.", "a viewing this week"], ["I've seen it, I want to sign.", "the contract terms please"]),
"gym": _domain(("Class Booking Agent", "Personal Training Agent"), [
    ("Class Booking Agent", "Handles booking and cancelling group classes, class schedules and waitlists.",
     ["Book me into the 7pm yoga class.", "Can I cancel my spin class tomorrow?", "What classes are on Saturday?", "am i on the waitlist for pilates", "Is there a beginner HIIT class?"], "class"),
    ("Personal Training Agent", "Handles one-to-one trainer sessions, training plans, fitness assessments and choosing a trainer.",
     ["I want a personal trainer.", "Can I get a training plan for running?", "Move my session with Alex to Friday.", "need a fitness assessment", "Which trainer specialises in rehab?"], "trainer"),
    ("Membership Agent", "Handles membership freezes, upgrades, guest passes and membership status.",
     ["I want to freeze my membership for a month.", "Can I bring a guest?", "How do I upgrade to the premium membership?", "is my membership still active", "I'm moving away, how do I end my membership?"], "membership"),
    ("Facilities Agent", "Handles lockers, showers, opening hours, broken equipment and the pool.",
     ["The showers are cold.", "Is the pool open today?", "A treadmill is broken.", "what are the opening hours", "My locker won't open."], "locker"),
    _general("General Member Support Agent", "member")],
    ["I want some help with my workouts.", "I'd like to start training properly."],
    ["Do you want to join group classes, or work one-to-one with a trainer?", "Group sessions, or a personal trainer?"],
    ["Group classes are fine.", "book me into classes"], ["One-to-one with a trainer.", "a personal plan and coach"]),
"library": _domain(("Book Loans Agent", "Digital Resources Agent"), [
    ("Book Loans Agent", "Handles borrowing and returning printed books, renewals, holds and overdue items.",
     ["I want to renew my books.", "Can I reserve a copy of this novel?", "My book is overdue.", "how many books can i borrow", "I returned a book but it's still on my account."], "loan"),
    ("Digital Resources Agent", "Handles e-books, audiobooks, online databases and remote access to journals.",
     ["How do I borrow e-books?", "The audiobook app won't load.", "I can't access the journal database from home.", "ebook download fails", "Do you have online newspapers?"], "e-book"),
    ("Room Reservations Agent", "Handles booking study rooms, meeting rooms and quiet spaces.",
     ["I need a study room for four people.", "Book the meeting room on Friday.", "Can I extend my study room booking?", "quiet room available now?", "Cancel my room booking tomorrow."], "study room"),
    ("Events & Workshops Agent", "Handles author talks, children's story time, workshops and event sign-ups.",
     ["When is the next author talk?", "Sign my kids up for story time.", "Is there a coding workshop this month?", "any events this weekend", "I want to cancel my workshop spot."], "workshop"),
    _general("General Library Help Agent", "library")],
    ["I want to read this title.", "Can I get the new crime novel?"],
    ["Do you want the printed book, or the e-book or audiobook version?", "Physical copy or digital?"],
    ["The printed book please.", "a physical copy"], ["The e-book is fine.", "audiobook version"]),
"restaurant": _domain(("Table Booking Agent", "Private Events Agent"), [
    ("Table Booking Agent", "Handles table reservations, changing party size, cancellations and waitlists.",
     ["Table for two at 8pm tonight.", "Can I change my booking to six people?", "Please cancel our table on Friday.", "any tables free for lunch", "Put us on the waitlist."], "table"),
    ("Private Events Agent", "Handles private dining rooms, large parties, set menus for events and venue hire.",
     ["I want to host a birthday dinner for 30.", "Can we hire the private room?", "Do you do set menus for company events?", "book the whole terrace for a party", "We need a room for a wedding lunch."], "private room"),
    ("Menu & Allergies Agent", "Handles dishes, ingredients, allergies, dietary needs and the wine list.",
     ["Is the risotto gluten free?", "Do you have vegan options?", "Does the dessert contain nuts?", "whats on the tasting menu", "Can the chef make it dairy free?"], "menu"),
    ("Lost & Found Agent", "Handles items left behind at the restaurant.",
     ["I left my jacket last night.", "Did anyone find a phone at table 4?", "I forgot my umbrella.", "lost my sunglasses there yesterday", "My scarf is missing after dinner."], "lost item"),
    _general("General Guest Help Agent", "guest")],
    ["We're a big group coming next week.", "I need to book for a lot of people."],
    ["Do you want a normal table, or a private event?", "Is it a regular booking or a private party?"],
    ["Just eight of us, a normal table.", "a big table is enough"], ["Forty people, a private party.", "we want the room to ourselves"]),
"streaming": _domain(("Playback Issues Agent", "Device Pairing Agent"), [
    ("Playback Issues Agent", "Handles buffering, video quality, subtitles, audio problems and playback errors.",
     ["The video keeps buffering.", "Subtitles are out of sync.", "There's no sound on episode three.", "error code when i press play", "Picture quality is blurry."], "buffering"),
    ("Device Pairing Agent", "Handles signing in on TVs and consoles, pairing codes, device limits and casting.",
     ["How do I sign in on my smart TV?", "The pairing code doesn't work.", "It says too many devices.", "cant cast to my tv", "How do I log out of my old console?"], "tv sign-in"),
    ("Profiles & Parental Controls Agent", "Handles user profiles, kids profiles, maturity ratings and viewing PINs.",
     ["Set up a kids profile.", "Block mature content for my son.", "Delete an old profile.", "change the viewing pin", "Can I rename my profile?"], "profile"),
    ("Content Requests Agent", "Handles availability of shows and films, new releases and regional catalogues.",
     ["When is season two coming?", "Why was this movie removed?", "Can you add more documentaries?", "is the new series available here", "Is this film available in my country?"], "series"),
    _general("General Viewer Support Agent", "viewer")],
    ["Nothing works on my TV.", "The app on my TV is acting up."],
    ["Can you sign in on the TV, or does the video fail when it plays?", "Is it signing in, or playback?"],
    ["I'm signed in, but videos keep freezing.", "playback stops"], ["I can't even sign in on it.", "the tv code won't link"]),
"saas_product": _domain(("Bug Reports Agent", "Integrations & API Agent"), [
    ("Bug Reports Agent", "Handles errors, crashes, broken features and unexpected behaviour in the product.",
     ["The export button does nothing.", "The dashboard crashes when I filter.", "Charts show the wrong dates.", "getting a 500 error on save", "Search results are missing items."], "bug"),
    ("Integrations & API Agent", "Handles API keys, webhooks, rate limits and connecting the product to other tools.",
     ["How do I get an API key?", "Our webhook stopped firing.", "We hit the API rate limit.", "connect it to slack", "The CRM sync fails."], "api"),
    ("Feature Requests Agent", "Handles product suggestions, roadmap questions and feedback on features.",
     ["Can you add dark mode?", "Is SSO on the roadmap?", "I'd like bulk editing.", "feature idea for reports", "When will mobile support arrive?"], "feature"),
    ("Workspace Admin Agent", "Handles adding users, roles and permissions, workspace settings and seat management.",
     ["Add three new users to our workspace.", "Make Priya an admin.", "Remove a former employee's access.", "change workspace name", "How do I set read-only roles?"], "workspace"),
    _general("General Product Support Agent", "product")],
    ["Our data stopped syncing.", "Records aren't coming through anymore."],
    ["Is it the product showing an error, or an integration or API connection failing?", "Does the app itself break, or the connection to another tool?"],
    ["The app shows an error when it loads.", "the page itself breaks"], ["The API connection to our CRM fails.", "the webhook from our tool"]),
"shipping": _domain(("Shipment Tracking Agent", "Pickup Scheduling Agent"), [
    ("Shipment Tracking Agent", "Handles where a parcel is, delivery estimates, delays and delivery confirmations.",
     ["Where is my parcel?", "Tracking hasn't updated in three days.", "When will my shipment arrive?", "it says delivered but nothing here", "Why is my package delayed?"], "tracking"),
    ("Pickup Scheduling Agent", "Handles booking courier pickups, changing pickup times and missed pickups.",
     ["Schedule a pickup for tomorrow.", "The courier didn't come to collect.", "Can I move my pickup to the afternoon?", "book collection from my office", "Cancel the pickup on Friday."], "pickup"),
    ("Customs Documents Agent", "Handles customs forms, export paperwork, commercial invoices and held shipments.",
     ["Customs is holding my package.", "Which form do I need to send to Canada?", "Do I need a commercial invoice?", "export docs for electronics", "My shipment needs a customs code."], "customs"),
    ("Packaging Agent", "Handles packaging rules, size and weight limits, fragile items and labels.",
     ["How should I pack glassware?", "What is the maximum box size?", "Can I ship liquids?", "need labels printed", "Is bubble wrap enough for a laptop?"], "packaging"),
    _general("General Shipping Help Agent", "shipping")],
    ["The courier situation is a mess.", "There's a problem with my parcel and the courier."],
    ["Is your parcel already on its way, or is it about the courier collecting it?", "Is it tracking a sent parcel, or a pickup?"],
    ["It's on its way but stuck.", "already shipped, no updates"], ["They never came to collect it.", "the pickup was missed"]),
"government_services": _domain(("Passport Agent", "National ID Agent"), [
    ("Passport Agent", "Handles new passports, passport renewals, lost passports and application status.",
     ["I need to renew my passport.", "My passport was stolen.", "How long does a new passport take?", "status of my passport application", "Can I get an urgent passport?"], "passport"),
    ("National ID Agent", "Handles national identity documents, ID renewals, address changes on the ID and replacements.",
     ["My ID document expires next month.", "I need to update the address on my ID.", "I lost my national ID.", "replace my damaged id", "How do I get an ID for my child?"], "national id"),
    ("Driving Licence Agent", "Handles driving tests, licence renewals, licence points and international driving permits.",
     ["Book my driving test.", "My driving licence expired.", "I need an international driving permit.", "how many points on my licence", "I passed my test, when does my licence arrive?"], "licence"),
    ("Public Records Agent", "Handles birth and marriage certificates, records requests and certified copies.",
     ["I need a copy of my birth certificate.", "How do I register a marriage?", "Request certified copies of records.", "lost my marriage certificate", "Correct an error on a certificate."], "certificate"),
    _general("General Citizen Help Agent", "citizen")],
    ["I need a new identity document.", "My identity document situation needs sorting."],
    ["Is it a passport for travel, or your national ID?", "Passport or national identity document?"],
    ["A passport, I'm travelling abroad.", "the passport"], ["The national ID for use at home.", "my national id"]),
"school": _domain(("Homework & Grades Agent", "Parent Meetings Agent"), [
    ("Enrollment Agent", "Handles school admissions, enrolling new pupils, transfers between schools and waiting lists.",
     ["I want to enroll my daughter for next year.", "Can my son transfer to your school?", "Is there a waiting list for year 3?", "documents needed for enrollment", "When do admissions open?"], "enrollment"),
    ("School Transport Agent", "Handles school bus routes, pickup times, bus stops and transport changes.",
     ["Which bus goes to our street?", "The school bus was late again.", "Change my child's bus stop.", "bus pickup time tomorrow", "Is there transport for after-school clubs?"], "bus"),
    ("Homework & Grades Agent", "Handles the homework portal, grades, school reports, marks and assignment deadlines.",
     ["Where can I see my son's grades?", "The homework portal won't load.", "When are school reports out?", "missing marks for science", "What homework is due this week?"], "grades"),
    ("Parent Meetings Agent", "Handles booking parent-teacher meetings, talking to teachers and discussing a child's progress or behaviour.",
     ["Book a meeting with the maths teacher.", "I'd like to discuss my child's behaviour.", "When are parent evenings?", "need to talk to the class teacher", "Can we meet about her progress?"], "teacher meeting"),
    _general("General School Office Agent", "school")],
    ["I'm worried about my child's results.", "My son is struggling at school."],
    ["Do you want to check the grades and homework, or meet a teacher to discuss it?", "See the marks, or talk with the teacher?"],
    ["Just show me the grades.", "check his marks"], ["I want to meet the teacher.", "a meeting to discuss it"]),
"vet_clinic": _domain(("Vet Appointments Agent", "Vaccinations Agent"), [
    ("Vet Appointments Agent", "Handles booking vet visits for sick or injured pets, rescheduling and emergencies.",
     ["My dog is limping, can a vet see him?", "Book a check for my cat's eye infection.", "Move my vet visit to Monday.", "my rabbit stopped eating", "Is there an emergency vet tonight?"], "vet visit"),
    ("Vaccinations Agent", "Handles vaccination schedules, boosters, vaccination records and travel vaccines for pets.",
     ["Is my puppy due for vaccines?", "When is the rabies booster?", "I need my cat's vaccination record.", "jabs for travelling abroad with my dog", "Did my dog get the kennel cough vaccine?"], "vaccine"),
    ("Grooming Agent", "Handles grooming appointments, nail trims, baths and coat care.",
     ["Book a grooming session.", "Can you trim my dog's nails?", "My cat needs a bath.", "groom appointment saturday", "Do you do de-shedding?"], "grooming"),
    ("Pet Boarding Agent", "Handles overnight stays, boarding bookings, daycare and care instructions while owners are away.",
     ["Can my dog stay while I travel?", "Book boarding for two weeks.", "Is there doggy daycare?", "my cat needs boarding in july", "Can you give her medicine while boarding?"], "boarding"),
    _general("General Pet Care Agent", "pet care")],
    ["My dog needs to come in.", "I want to bring my puppy in."],
    ["Is your pet unwell, or is it for routine vaccinations?", "Sick visit or vaccines?"],
    ["He's sick, he's been vomiting.", "an injury, he's limping"], ["Just his routine vaccines.", "booster shots"]),
"home_services": _domain(("Plumbing Agent", "Electrical Agent"), [
    ("Plumbing Agent", "Handles leaks, blocked drains, toilets, water pressure and pipe repairs.",
     ["My kitchen sink is blocked.", "Water is leaking under the floor.", "The toilet keeps running.", "low water pressure upstairs", "A pipe burst in the garage."], "leak"),
    ("Electrical Agent", "Handles power problems in the home, sockets, lighting, fuse boxes and wiring.",
     ["Half the sockets have no power.", "The lights keep flickering.", "The fuse box trips every night.", "install a new light fitting", "Sparks came from a socket."], "socket"),
    ("Cleaning Agent", "Handles house cleaning, deep cleans, move-out cleans and window cleaning.",
     ["Book a deep clean for Friday.", "I need a cleaner every week.", "Can you clean the windows?", "move out clean next month", "The cleaner missed the kitchen."], "cleaning"),
    ("Pest Control Agent", "Handles mice, insects, wasp nests and pest inspections.",
     ["There are mice in the kitchen.", "Wasps are nesting in the roof.", "I found bed bugs.", "ants everywhere", "Can someone inspect for termites?"], "pests"),
    _general("General Home Help Agent", "home services")],
    ["My water heater stopped working.", "No hot water since this morning."],
    ["Is there a leak or a water problem, or has the heater lost power?", "Plumbing issue or electrical?"],
    ["Water is leaking from the tank.", "the pipe is dripping"], ["It has no power, the switch is dead.", "the fuse keeps tripping"]),
"event_tickets": _domain(("Ticket Transfers Agent", "Event Changes Agent"), [
    ("Ticket Transfers Agent", "Handles sending tickets to friends, name changes on tickets and resale listings.",
     ["I want to send my ticket to a friend.", "Can I change the name on my ticket?", "How do I resell my tickets?", "transfer 2 tickets to my brother", "My friend didn't get the transferred ticket."], "ticket transfer"),
    ("Event Changes Agent", "Handles postponed or cancelled events, new dates, venue changes and what happens to tickets.",
     ["The concert was postponed, what now?", "Is the show still on tonight?", "The venue changed, are my tickets valid?", "festival cancelled?", "What's the new date for the match?"], "postponed"),
    ("Seating & Venue Agent", "Handles seat locations, venue maps, entry gates and what you can bring.",
     ["Where is section C?", "Which gate should I use?", "Can I bring a bag into the arena?", "are my seats covered", "Is there parking at the venue?"], "seat"),
    ("Accessibility Agent", "Handles wheelchair spaces, companion tickets, hearing loops and accessible entrances.",
     ["I need a wheelchair space.", "Do you offer companion tickets?", "Is there step-free access?", "hearing loop at the theatre?", "Can I get seats near an accessible toilet?"], "wheelchair"),
    _general("General Fan Support Agent", "event")],
    ["I can't make the show anymore.", "Something changed with my concert tickets."],
    ["Do you want to pass your tickets to someone, or has the event itself changed?", "Transferring tickets, or an event change?"],
    ["I want to give them to a friend.", "transfer them"], ["They moved the date and I can't go.", "the event was rescheduled"]),
"car_rental": _domain(("Rental Reservations Agent", "Pickup & Return Agent"), [
    ("Rental Reservations Agent", "Handles booking rental cars, changing dates or car class, and cancelling reservations.",
     ["Book a car for next week in Madrid.", "Can I change to an SUV?", "Cancel my rental reservation.", "extend my rental dates", "Do you have automatics available?"], "rental booking"),
    ("Pickup & Return Agent", "Handles collecting and returning cars, branch opening hours, late returns and key drop.",
     ["Where do I pick up the car at the airport?", "I'll return the car late tonight.", "Is the branch open on Sunday?", "key drop after hours?", "Can I return it to a different city?"], "return"),
    ("Damage Reports Agent", "Handles scratches, dents, accidents with a rental car and damage report disputes.",
     ["I scratched the rental car.", "There was a dent before I took it.", "I had a small accident.", "the damage report is wrong", "A stone cracked the windscreen."], "scratch"),
    ("Rental Add-ons Agent", "Handles child seats, GPS units, extra drivers and snow chains.",
     ["I need a child seat.", "Add my husband as a driver.", "Can I get a GPS unit?", "snow chains for the trip", "Do you have roof boxes?"], "child seat"),
    _general("General Rental Help Agent", "car rental")],
    ["I need to change my car rental.", "My plans with the rental car changed."],
    ["Is it the booking itself, or how you pick up or return the car?", "Change the reservation, or the pickup and return?"],
    ["Different dates and a bigger car.", "the booking dates"], ["I'll return it at another branch.", "pickup at the station instead"]),
"coworking": _domain(("Desk Booking Agent", "Meeting Rooms Agent"), [
    ("Desk Booking Agent", "Handles hot desks, dedicated desks, desk availability and desk booking changes.",
     ["I need a desk tomorrow.", "Is there a dedicated desk free?", "Cancel my desk on Thursday.", "book a desk near the window", "Can I keep the same desk all week?"], "desk"),
    ("Meeting Rooms Agent", "Handles booking meeting rooms, room equipment and video-call setup.",
     ["Book a meeting room for 10 people.", "Does room B have a screen?", "Extend my room booking by an hour.", "need a room with video calls", "Cancel my meeting room at 3pm."], "meeting room"),
    ("Mail & Packages Agent", "Handles business mail, receiving packages and mail forwarding.",
     ["Did a package arrive for me?", "Forward my mail to my home.", "Can you receive a delivery for my company?", "any letters today", "My parcel went to the wrong floor."], "mail"),
    ("Workspace Facilities Agent", "Handles Wi-Fi, heating, cleaning, kitchen supplies and building access.",
     ["The office Wi-Fi is down.", "It's too cold on the second floor.", "The coffee machine is broken.", "door access not working", "The kitchen is out of milk."], "wifi"),
    _general("General Member Help Agent", "coworking")],
    ["I need a space for my team tomorrow.", "We need somewhere to work together tomorrow."],
    ["Do you need desks to work at, or a meeting room?", "Desks or a meeting room?"],
    ["Four desks next to each other.", "desks for the day"], ["A room for a two-hour meeting.", "a meeting room"]),
"museum": _domain(("Guided Tours Agent", "School Groups Agent"), [
    ("Guided Tours Agent", "Handles guided tours for visitors, tour languages, times and private tours.",
     ["Is there an English guided tour today?", "Book a private tour for six adults.", "How long is the guided tour?", "audio guide or live guide?", "Tour times on Sunday?"], "tour"),
    ("School Groups Agent", "Handles school visits, education programmes, teacher bookings and class workshops.",
     ["I'm a teacher and want to bring my class.", "Do you have workshops for 10-year-olds?", "Book a school visit for 30 pupils.", "education programme for history", "How many adults do we need per pupil?"], "school visit"),
    ("Exhibitions Agent", "Handles current and upcoming exhibitions, artworks on display and exhibition dates.",
     ["What's the new exhibition about?", "Is the Monet painting on display?", "When does the dinosaur exhibition end?", "upcoming shows next month", "Which floor has modern art?"], "exhibition"),
    ("Visitor Services Agent", "Handles opening hours, cloakroom, accessibility, the cafe and lost items.",
     ["What time do you open?", "Is there a cloakroom?", "Is the museum wheelchair accessible?", "where is the cafe", "I lost my scarf in the gallery."], "opening hours"),
    _general("General Museum Help Agent", "museum")],
    ["I want to bring a group of kids.", "We're planning a visit with children."],
    ["Is this a school class visit, or a family group wanting a guided tour?", "School trip or family tour?"],
    ["Just our family and cousins, we want a guide.", "a family tour"], ["It's my class from school.", "a school trip"]),
"cloud_hosting": _domain(("Server Outages Agent", "Scaling & Performance Agent"), [
    ("Server Outages Agent", "Handles servers that are down, unreachable sites, crashes and incident status.",
     ["Our server is down.", "The website is unreachable.", "Is there an incident in eu-west?", "vm crashed and won't boot", "Our database server stopped responding."], "outage"),
    ("Scaling & Performance Agent", "Handles slow response times, CPU and memory limits, autoscaling and load.",
     ["The site is very slow under load.", "CPU is at 100% all day.", "How do I set up autoscaling?", "need more memory on the vm", "Requests time out during peak hours."], "performance"),
    ("Domain & DNS Agent", "Handles domain names, DNS records, SSL certificates and email records.",
     ["My domain doesn't point to the server.", "Add an MX record.", "SSL certificate expired.", "dns not propagating", "Move my domain to your service."], "dns"),
    ("Backups & Restore Agent", "Handles backup schedules, restoring data and snapshots.",
     ["Restore yesterday's backup.", "Are my backups running?", "Create a snapshot before the upgrade.", "deleted a table need restore", "How long are backups kept?"], "backup"),
    _general("General Cloud Support Agent", "cloud")],
    ["Our app isn't responding properly.", "Users say the site isn't working."],
    ["Is it completely down, or up but very slow?", "Down, or just slow?"],
    ["Completely down, nothing loads.", "it's offline"], ["It loads, but takes 30 seconds.", "slow under traffic"]),
"public_transport": _domain(("Timetables Agent", "Service Disruptions Agent"), [
    ("Timetables Agent", "Handles route schedules, first and last departures, journey planning and connections.",
     ["When is the last train to the airport?", "How often does bus 42 run?", "Plan my journey to the stadium.", "first tram on sunday", "Which line connects to the university?"], "timetable"),
    ("Service Disruptions Agent", "Handles delays, cancellations, strikes, engineering works and replacement buses.",
     ["Why is my train cancelled?", "Is the metro delayed today?", "Are there replacement buses this weekend?", "strike tomorrow?", "Line 2 is stuck, what's happening?"], "delay"),
    ("Lost Property Agent", "Handles items lost on trains, buses and at stations.",
     ["I left my bag on the train.", "Lost my phone on bus 12.", "Has anyone found a laptop?", "forgot my umbrella on the tram", "Where is the lost property office?"], "lost property"),
    ("Accessible Travel Agent", "Handles step-free access, booking assistance, lifts and travelling with a wheelchair.",
     ["Is the station step-free?", "Book assistance for my trip.", "The lift at central is broken.", "travelling with a wheelchair tomorrow", "Are the buses low-floor?"], "step-free"),
    _general("General Travel Info Agent", "travel")],
    ["Is my train running tonight?", "Can I still get home by train tonight?"],
    ["Do you want the normal timetable, or are you asking about delays and cancellations?", "Schedule, or disruptions?"],
    ["The normal times, when is the last one?", "the schedule"], ["I heard there are cancellations.", "is it delayed"]),
"wedding_planning": _domain(("Venue Agent", "Catering Agent"), [
    ("Venue Agent", "Handles wedding venue booking, venue visits, capacity and decorations at the venue.",
     ["Is the garden venue free in May?", "Can we visit the hall?", "How many guests fit in the barn?", "venue decorations allowed?", "Book the venue for our date."], "venue"),
    ("Catering Agent", "Handles wedding menus, tastings, dietary needs and the cake.",
     ["Can we book a menu tasting?", "We need vegetarian options.", "How much food for 120 guests?", "wedding cake flavours", "Can the caterer handle allergies?"], "catering"),
    ("Photography Agent", "Handles photographers, videographers, photo packages and shot lists.",
     ["We need a photographer.", "Do you offer videography?", "When do we get our photos?", "drone shots possible?", "Add a second photographer."], "photos"),
    ("Guest Management Agent", "Handles invitations, RSVPs, seating plans and guest accommodation.",
     ["Send out the invitations.", "Track RSVPs for us.", "Help with the seating plan.", "hotel rooms for guests", "Who hasn't replied yet?"], "invitations"),
    _general("General Wedding Help Agent", "wedding")],
    ["We need to sort the reception.", "The reception planning needs work."],
    ["Is it about the reception venue, or the food and drinks?", "Venue or catering?"],
    ["Where it will be held.", "the venue for it"], ["What we'll serve the guests.", "the menu"]),
}

for _k, _v in NEW_DOMAINS.items():
    assert _k not in DOMAINS, _k
    assert len(_v["agents"]) == 5 and all(a in _v["agents"] for a in _v["close_pair"]), _k
DOMAINS.update(NEW_DOMAINS)


OK_WORDS = ["OK", "ok", "Okay.", "okay", "Sure.", "sure", "k", "Alright.", "fine", "yes"]
FOLLOWUPS = ["How long will that take?", "Can you check again?", "same issue still", "what about that?", "ok and then?",
             "Is there anything I need to do?", "any update?", "no it's still not working", "Can you explain that?",
             "what does that mean for me?", "and when will I hear back?", "thanks, what's next?"]
ACKS = ["I can help you with that.", "Sure, let me look into that.", "Okay, I'm checking that now.", "I'll take care of that.", "Let me help you with that."]
INFO_REPLIES = ["Let me check the details.", "I've looked into it.", "Here is what I found.", "That's being processed.", "I've noted that."]
GENERAL_PROMPTS = ["Sure, what do you need help with?", "Tell me what happened.", "Of course, what's it about?"]
HANDOFF = ["This is for the {a}. Please continue with the {a}.", "The {a} handles this. Please continue with that agent.",
           "Please continue with the {a}, they can help.", "I'll pass you to the {a}."]
SWITCH_PREFIX = ["Actually, ", "lol no, ", "just kidding, ", "Also, ", "Different thing: ", "Wait, ", "One more thing, ", ""]
AGENT_QUESTIONS = ["Can you share the reference number?", "Which day works best for you?", "When did this start?",
                   "Which device are you using?", "What's the address?", "Could you confirm the date?",
                   "Morning or afternoon?", "What's the name on the account?", "How many items is it?"]
SHORT_ANSWERS = ["Sunday", "the 14th", "PS5", "12 Harbour Road", "R-88213", "mornings", "yes", "no", "last Tuesday",
                 "about three days ago", "my phone", "two", "Jordan Lee", "afternoon please", "48211", "the blue one"]
CLOSINGS = ["thanks", "got it", "great, thanks", "perfect", "cool", "ok thank you", "that works", "noted"]
SHORT_SWITCH = ["and the {t}?", "what about my {t}?", "{t} please", "now the {t}", "also {t}", "{t} next", "and {t}?"]
RETURN_PREFIX = ["ok back to the first thing: ", "Anyway, back to my earlier question: ", "Forget that. ", "Never mind that, ", "seriously now, "]


def noisy(text):
    """Light user-style noise: lower-casing, dropped punctuation, a swapped-letter typo."""
    r = rng.random()
    if r < 0.15:
        text = text.lower().rstrip(".?!")
    elif r < 0.25 and len(text) > 8:
        i = rng.randrange(1, len(text) - 2)
        if text[i].isalpha() and text[i + 1].isalpha():
            text = text[:i] + text[i + 1] + text[i] + text[i + 2:]
    return text


def intent(dom, agent):
    return noisy(rng.choice(DOMAINS[dom]["agents"][agent][1]))


def other_agent(dom, agent, exclude_general=False):
    names = [a for a in DOMAINS[dom]["agents"] if a != agent]
    if exclude_general:
        names = [a for a in names if "General" not in a]
    return rng.choice(names)


def general_agent(dom):
    return next(a for a in DOMAINS[dom]["agents"] if "General" in a)


def lower_first(t):
    return t[:1].lower() + t[1:] if t else t


def build(dom):
    d, ex = DOMAINS[dom], []
    agents = list(d["agents"])
    specialists = [a for a in agents if "General" not in a]
    gen = general_agent(dom)
    def add(msgs, target, tags, current, change):
        ex.append({"msgs": msgs, "target": target, "tags": tags, "current": current, "change": change})

    for a in agents:                                      # A. obvious single request
        for _ in range(4):
            add([intent(dom, a)], a, ["obvious"], None, None)
    for a in d["close_pair"]:                             # G/I. close-pair clarification (context decides)
        for _ in range(4):
            add([rng.choice(d["ambiguous"]["opener"]), rng.choice(d["ambiguous"]["clarify"]),
                 noisy(rng.choice(d["ambiguous"]["resolve"][a]))], a, ["close_pair", "context"], gen, False)
    for a in specialists:                                 # F. handoff + OK
        for _ in range(2):
            add([intent(dom, a), rng.choice(HANDOFF).format(a=a), rng.choice(OK_WORDS)], a, ["handoff", "ok_after_handoff"],
                rng.choice([gen, other_agent(dom, a)]), False)   # the agent that handed over
    for a in d["close_pair"]:                             # F + G. clarification, handoff, OK
        for _ in range(2):
            add([rng.choice(d["ambiguous"]["opener"]), rng.choice(d["ambiguous"]["clarify"]),
                 noisy(rng.choice(d["ambiguous"]["resolve"][a])), rng.choice(HANDOFF).format(a=a), rng.choice(OK_WORDS)],
                a, ["handoff", "ok_after_handoff", "close_pair", "context"], gen, False)
    for a in specialists:                                 # L. handoff chain via the general agent
        add([noisy(rng.choice(d["agents"][gen][1])), rng.choice(GENERAL_PROMPTS), intent(dom, a),
             rng.choice(HANDOFF).format(a=a), rng.choice(OK_WORDS)], a, ["handoff", "handoff_chain", "ok_after_handoff"], gen, False)
    for a in specialists:                                 # E/K. meaningless final message / follow-up -> same agent
        for _ in range(2):
            add([intent(dom, a), rng.choice(ACKS), rng.choice(OK_WORDS + FOLLOWUPS)], a, ["context", "follow_up"], a, False)
    for a in specialists:                                 # N. the agent asks, the user answers in a few words -> same agent
        for _ in range(4):
            add([intent(dom, a), rng.choice(AGENT_QUESTIONS), rng.choice(SHORT_ANSWERS)], a, ["context", "short_answer"], a, False)
    for a in specialists:                                 # N. the agent answers, the user closes briefly -> same agent
        for _ in range(2):
            add([intent(dom, a), rng.choice(INFO_REPLIES), rng.choice(CLOSINGS)], a, ["context", "short_answer", "closing"], a, False)
    for _ in range(16):                                   # N. same after a topic change: the new agent asks, short answer
        a = rng.choice(specialists); b = other_agent(dom, a, exclude_general=True)
        add([intent(dom, a), rng.choice(ACKS), rng.choice(SWITCH_PREFIX) + lower_first(intent(dom, b)), rng.choice(AGENT_QUESTIONS),
             rng.choice(SHORT_ANSWERS)], b, ["context", "short_answer", "after_switch"], b, False)
    for _ in range(14):                                   # M. legitimate topic change: latest request wins
        a = rng.choice(specialists); b = other_agent(dom, a, exclude_general=True)
        add([intent(dom, a), rng.choice(ACKS), rng.choice(SWITCH_PREFIX) + lower_first(intent(dom, b))], b, ["topic_change"], a, True)
    for _ in range(8):                                    # M. topic change after a follow-up exchange
        a = rng.choice(specialists); b = other_agent(dom, a, exclude_general=True)
        add([intent(dom, a), rng.choice(ACKS), rng.choice(FOLLOWUPS), rng.choice(INFO_REPLIES),
             rng.choice(SWITCH_PREFIX) + lower_first(intent(dom, b))], b, ["topic_change"], a, True)
    for _ in range(16):                                   # S. SHORT topic change: "and the bill?" -> the other agent
        a = rng.choice(specialists); b = other_agent(dom, a, exclude_general=True)
        add([intent(dom, a), rng.choice(AGENT_QUESTIONS + INFO_REPLIES), rng.choice(SHORT_SWITCH).format(t=d["topics"][b].lower())],
            b, ["topic_change", "short_switch"], a, True)
    for _ in range(8):                                    # H. bounce away and come back
        a = rng.choice(specialists); b = other_agent(dom, a, exclude_general=True)
        add([intent(dom, a), rng.choice(HANDOFF).format(a=a), intent(dom, b), rng.choice(HANDOFF).format(a=b),
             rng.choice(RETURN_PREFIX) + lower_first(intent(dom, a))], a, ["ding_dong", "topic_change"], a, True)   # a handed over to b
    for _ in range(8):                                    # J. distractor keyword: "forget the <other topic>"
        a = rng.choice(specialists); b = other_agent(dom, a, exclude_general=True)
        add([intent(dom, b), rng.choice(ACKS), f"Forget the {d['topics'][b]}. " + intent(dom, a)], a, ["distractor", "topic_change"], b, True)
    for _ in range(8):                                    # D. long conversations (9-15 messages), one topic throughout
        a = rng.choice(specialists)
        msgs = [intent(dom, a), rng.choice(ACKS)]
        for _ in range(rng.randint(3, 6)):
            msgs += [rng.choice(FOLLOWUPS), rng.choice(INFO_REPLIES)]
        msgs = msgs[:14] + [rng.choice(OK_WORDS + FOLLOWUPS)]
        add(msgs, a, ["long", "context", "follow_up"], a, False)
    for _ in range(6):                                    # H. ding-dong walks: one example per user turn (prefix)
        msgs, cur = [], rng.choice(specialists)
        msgs.append(intent(dom, cur))
        add(list(msgs), cur, ["ding_dong", "turn_prefix"], None, None)
        for _ in range(rng.randint(3, 6)):
            msgs.append(rng.choice(HANDOFF + ACKS).format(a=cur))
            speaker = cur                                  # the agent that just replied holds the conversation
            r = rng.random()
            changed = r < 0.55
            if r < 0.55:                                   # bounce to another agent's topic
                cur = other_agent(dom, cur, exclude_general=True)
                msgs.append(rng.choice(SWITCH_PREFIX) + lower_first(intent(dom, cur)))
            elif r < 0.8:                                  # follow-up on the current topic
                msgs.append(rng.choice(FOLLOWUPS))
            else:                                          # just acknowledges
                msgs.append(rng.choice(OK_WORDS))
            if len(msgs) > 15:
                break
            add(list(msgs), cur, ["ding_dong", "turn_prefix"], speaker, changed)
    return ex


domains_out = {dom: {"close_pair": d["close_pair"],
                     "agents": {a: v[0] for a, v in d["agents"].items()},
                     "keywords": {a: [d["topics"][a].lower()] for a in d["agents"]}} for dom, d in DOMAINS.items()}
conversations = []
for dom in DOMAINS:
    for k, e in enumerate(build(dom)):
        roles = ["user", "assistant"]
        rec = {"id": f"{dom}-{k:03d}", "domain": dom,
               "messages": [{"role": roles[i % 2], "content": t} for i, t in enumerate(e["msgs"])],
               "target_agent": e["target"], "current_agent": e["current"], "context_change": e["change"], "tags": e["tags"]}
        assert 1 <= len(rec["messages"]) <= 15 and rec["messages"][-1]["role"] == "user", rec["id"]
        assert (rec["current_agent"] is None) == (len(rec["messages"]) == 1), rec["id"]   # an agent holds it once one has replied
        assert (rec["context_change"] is None) == (len(rec["messages"]) == 1), rec["id"]
        conversations.append(rec)

banking_words = ["payments agent", "card support", "investment agent", "insurance agent", "general customer support"]
for rec in conversations:
    text = " ".join(m["content"].lower() for m in rec["messages"])
    assert not any(w in text for w in banking_words), f"banking agent leaked into {rec['id']}"

json.dump(domains_out, open("data/modernbert_router/generic/domains.json", "w"), indent=1, ensure_ascii=False)
json.dump(conversations, open("data/modernbert_router/generic/conversations.json", "w"), indent=1, ensure_ascii=False)
print(f"domains: {len(DOMAINS)} | conversations: {len(conversations)} ({len(conversations) * 5} candidate pairs)")
stay = sum(c["current_agent"] == c["target_agent"] for c in conversations)
fresh = sum(c["current_agent"] is None for c in conversations)
print(f"current agent: none (fresh) {fresh} | stays with current {stay} | switches away {len(conversations) - stay - fresh}")
yes = sum(c["context_change"] is True for c in conversations)
no = sum(c["context_change"] is False for c in conversations)
short = [c for c in conversations if c["context_change"] is not None and len(c["messages"][-1]["content"].split()) <= 3]
print(f"context change: Y {yes} | N {no} | short last message (<= 3 words): {len(short)} "
      f"(Y {sum(c['context_change'] for c in short)}, N {sum(not c['context_change'] for c in short)})")
