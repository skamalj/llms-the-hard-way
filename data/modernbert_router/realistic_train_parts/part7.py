"""Realistic TRAINING conversations, part 7: email provider, home alarm company, car leasing, motorbike rental, boat hire."""

COMPANIES = {
    "email provider": {
        "Mailbox Access Agent": "Helps users who can't sign in, reset passwords and set up two-step verification.",
        "Email Delivery Agent": "Fixes emails not sending or arriving, bounces and spam folder issues.",
        "Mailbox Storage Agent": "Handles a full mailbox, storage limits and storage upgrades.",
        "Custom Domain Agent": "Sets up custom email domains and DNS records.",
        "Email Plan Billing Agent": "Handles premium plans, charges and refunds.",
    },
    "home alarm company": {
        "Alarm Installation Agent": "Books alarm and camera installations and survey visits.",
        "Alarm Faults Agent": "Fixes false alarms, beeping panels, low batteries and offline sensors.",
        "Alarm Monitoring Agent": "Handles 24/7 monitoring, keyholders and police response.",
        "Alarm App Agent": "Helps with the alarm app, arming remotely and notifications.",
        "Alarm Contract Agent": "Handles contracts, monthly fees, moving house and cancellation.",
    },
    "car leasing": {
        "Lease Quotes Agent": "Gives lease quotes for cars, terms and mileage.",
        "Lease Application Agent": "Handles lease applications, credit checks and documents.",
        "Lease Delivery Agent": "Arranges delivery of the new lease car.",
        "End of Lease Agent": "Handles returning the car, damage inspections and excess mileage charges.",
        "Lease Payments Agent": "Handles monthly lease payments and payment dates.",
    },
    "motorbike rental": {
        "Bike Hire Bookings Agent": "Books motorbike and scooter rentals and changes dates.",
        "Rider Licence Agent": "Checks licence categories and age requirements for each bike.",
        "Riding Gear Agent": "Rents helmets, jackets, gloves and luggage.",
        "Bike Breakdown Agent": "Helps riders whose bike breaks down or has a puncture during the rental.",
        "Hire Deposit Agent": "Handles deposits, damage charges and deposit refunds.",
    },
    "boat hire": {
        "Boat Bookings Agent": "Books day boats and holiday cruisers and changes dates.",
        "Skipper Training Agent": "Explains the handling lesson and who can drive the boat.",
        "Moorings & Route Agent": "Advises on routes, locks, moorings and journey times.",
        "On-Board Help Agent": "Helps with problems on the boat: engine, toilet, power and water.",
        "Boat Hire Payments Agent": "Handles balances, damage deposits and refunds.",
    },
}

CONVERSATIONS = [
    ("email provider", "mail-1", [
        ("I can't log into my email, it says my password is wrong.", "Mailbox Access Agent", "start", "I can send a reset link to your recovery phone. Shall I?"),
        ("yes please", "Mailbox Access Agent", "answer", "Sent. Choose a new password with the link."),
        ("ok I'm in", "Mailbox Access Agent", "closing", "Great."),
        ("Now it says my mailbox is full", "Mailbox Storage Agent", "switch", "You're using 15 of 15GB. Delete large attachments or upgrade to 100GB."),
        ("how much is the upgrade", "Email Plan Billing Agent", "switch", "£1.99 a month."),
        ("go ahead", "Email Plan Billing Agent", "answer", "Done; you now have 100GB."),
    ]),
    ("email provider", "mail-2", [
        ("My emails to a client keep bouncing back.", "Email Delivery Agent", "start", "What does the bounce message say?"),
        ("mailbox unavailable", "Email Delivery Agent", "answer", "That means their address is wrong or closed; please check it with them."),
        ("ah, typo. thanks", "Email Delivery Agent", "closing", None),
        ("Can I use my own domain, smithdesign.co.uk?", "Custom Domain Agent", "switch", "Yes, on a premium plan. You'll need to add MX records at your registrar."),
        ("which records exactly", "Custom Domain Agent", "follow", "Two MX records and one TXT; I'll email you the exact values."),
    ]),
    ("email provider", "mail-3", [
        ("I was charged for premium but I cancelled.", "Email Plan Billing Agent", "start", "When did you cancel?"),
        ("last week", "Email Plan Billing Agent", "answer", "The charge went through before the cancellation; I've refunded it."),
        ("thanks. Also how do I set up two-step verification", "Mailbox Access Agent", "switch", "Go to Security, 2-step verification, and add your phone."),
    ]),
    ("email provider", "mail-4", [
        ("Emails from my school are going to spam.", "Email Delivery Agent", "start", "Open one and click 'Not spam'; future ones will go to your inbox."),
        ("done", "Email Delivery Agent", "closing", None),
        ("how much storage do I have left", "Mailbox Storage Agent", "switch", "You have 9GB free."),
    ]),
    ("home alarm company", "alarm-1", [
        ("Our alarm went off at 3am for no reason.", "Alarm Faults Agent", "start", "The log shows the hallway sensor. Is there a pet or a heater near it?"),
        ("we have a new radiator there", "Alarm Faults Agent", "answer", "That could do it. We can move the sensor; I'll book an engineer."),
        ("ok", "Alarm Faults Agent", "answer", "Booked for Thursday morning."),
        ("Did the police get called?", "Alarm Monitoring Agent", "switch", "No, the monitoring team called you first and you cancelled it."),
        ("and can I add my neighbour as a keyholder", "Alarm Monitoring Agent", "follow", "Yes, send me her name and number."),
    ]),
    ("home alarm company", "alarm-2", [
        ("I'd like an alarm fitted in my new house.", "Alarm Installation Agent", "start", "We start with a free survey. When suits you?"),
        ("next Monday", "Alarm Installation Agent", "answer", "Monday 10am is booked."),
        ("what does monitoring cost each month", "Alarm Contract Agent", "switch", "£24.99 a month on a 2-year contract."),
        ("can I arm it from my phone", "Alarm App Agent", "switch", "Yes, the app lets you arm and disarm and get alerts."),
    ]),
    ("home alarm company", "alarm-3", [
        ("We're moving house, can we take the alarm contract with us?", "Alarm Contract Agent", "start", "Yes, we move the system for a £99 fee."),
        ("fine, when can you do it", "Alarm Installation Agent", "switch", "We can fit it at the new address on the 14th."),
        ("great", "Alarm Installation Agent", "closing", None),
    ]),
    ("home alarm company", "alarm-4", [
        ("The panel keeps beeping.", "Alarm Faults Agent", "start", "That's usually a low battery in a sensor. Does the panel show which one?"),
        ("back door", "Alarm Faults Agent", "answer", "Replace the CR2032 battery in that sensor and the beeping will stop."),
        ("I'm not getting notifications on the app either", "Alarm App Agent", "switch", "Check notifications are allowed for the app in your phone settings."),
        ("they were off. fixed", "Alarm App Agent", "closing", None),
    ]),
    ("car leasing", "lease-1", [
        ("How much to lease a VW Golf for 3 years?", "Lease Quotes Agent", "start", "With 10,000 miles a year it's £289 a month."),
        ("and with 8,000", "Lease Quotes Agent", "follow", "£274 a month."),
        ("ok I'd like to apply", "Lease Application Agent", "switch", "I'll need your driving licence and 3 months of bank statements."),
        ("will it do a hard credit check?", "Lease Application Agent", "follow", "Yes, at the final stage only."),
        ("how quick is delivery", "Lease Delivery Agent", "switch", "About 6 weeks for that model."),
    ]),
    ("car leasing", "lease-2", [
        ("My lease ends next month, how do I give the car back?", "End of Lease Agent", "start", "We'll book a collection and an inspection at your home."),
        ("I'm a bit over on mileage", "End of Lease Agent", "follow", "It's 8p a mile over the limit, billed after collection."),
        ("can I move my last payment date", "Lease Payments Agent", "switch", "Yes, to which date?"),
        ("the 28th", "Lease Payments Agent", "answer", "Changed."),
    ]),
    ("car leasing", "lease-3", [
        ("Has my application been approved?", "Lease Application Agent", "start", "Yes, approved this morning."),
        ("great! when will the car come", "Lease Delivery Agent", "switch", "The 22nd, between 8am and 1pm."),
        ("and the first payment?", "Lease Payments Agent", "switch", "The initial payment is taken 7 days before delivery."),
    ]),
    ("car leasing", "lease-4", [
        ("Why was my payment £40 more this month?", "Lease Payments Agent", "start", "That's a one-off admin fee for the change of registered address."),
        ("ok", "Lease Payments Agent", "closing", None),
        ("Also, what if there's a scratch when I hand it back", "End of Lease Agent", "switch", "Small scratches under 25mm are fair wear and tear."),
    ]),
    ("motorbike rental", "moto-1", [
        ("I'd like to rent a bike for 3 days next week.", "Bike Hire Bookings Agent", "start", "Which bike? We have a Honda CB500 and a BMW R1250GS."),
        ("the BMW", "Bike Hire Bookings Agent", "answer", "Available Tuesday to Thursday."),
        ("do I need a full licence for that", "Rider Licence Agent", "switch", "Yes, a full A licence and age 25 or over."),
        ("I'm 31 with an A licence", "Rider Licence Agent", "answer", "Then you're fine."),
        ("can I rent panniers", "Riding Gear Agent", "switch", "Yes, £10 a day."),
        ("ok and the deposit?", "Hire Deposit Agent", "switch", "£1,000 held on a card."),
    ]),
    ("motorbike rental", "moto-2", [
        ("I've got a puncture on the rental bike.", "Bike Breakdown Agent", "start", "Are you safe? Where are you?"),
        ("lay-by on the A82 near Fort William", "Bike Breakdown Agent", "answer", "Recovery is on the way, about 60 minutes."),
        ("will I be charged for this", "Hire Deposit Agent", "switch", "No, punctures aren't charged."),
    ]),
    ("motorbike rental", "moto-3", [
        ("Do you rent helmets?", "Riding Gear Agent", "start", "Yes, in sizes S to XL, with a new liner for each rider."),
        ("and jackets", "Riding Gear Agent", "follow", "Yes, textile jackets and trousers."),
        ("I need to move my booking from Friday to Saturday", "Bike Hire Bookings Agent", "switch", "Done, Saturday to Monday."),
    ]),
    ("motorbike rental", "moto-4", [
        ("When do I get my deposit back?", "Hire Deposit Agent", "start", "It's released within 7 days of return."),
        ("it's been 10", "Hire Deposit Agent", "follow", "Sorry, I've released it now."),
        ("thanks. can I ride a 125 on a car licence", "Rider Licence Agent", "switch", "Only with a valid CBT certificate."),
    ]),
    ("boat hire", "boat-1", [
        ("I'd like to hire a boat for a week on the Broads in July.", "Boat Bookings Agent", "start", "For how many people?"),
        ("4", "Boat Bookings Agent", "answer", "The Kingfisher sleeps 4, from the 12th to the 19th."),
        ("none of us have driven a boat", "Skipper Training Agent", "switch", "No problem; everyone gets a free 30-minute handling lesson before leaving."),
        ("how far can we get in a day", "Moorings & Route Agent", "switch", "About 15 to 20 miles at the 5mph speed limit."),
        ("ok how much is the deposit", "Boat Hire Payments Agent", "switch", "£150 damage deposit, refunded after the trip."),
    ]),
    ("boat hire", "boat-2", [
        ("The engine on our boat won't start.", "On-Board Help Agent", "start", "Is the gear lever in neutral?"),
        ("oh, no it wasn't", "On-Board Help Agent", "answer", "Put it in neutral and try again."),
        ("started", "On-Board Help Agent", "closing", "Great."),
        ("where can we moor for tonight near Wroxham", "Moorings & Route Agent", "switch", "There are free moorings at Salhouse Broad, 20 minutes away."),
    ]),
    ("boat hire", "boat-3", [
        ("Can I change my boat booking to August?", "Boat Bookings Agent", "start", "Yes, the 2nd to 9th of August is free."),
        ("yes do that", "Boat Bookings Agent", "answer", "Moved."),
        ("is there a fee for moving", "Boat Hire Payments Agent", "switch", "£25 change fee."),
        ("fine", "Boat Hire Payments Agent", "closing", None),
    ]),
    ("boat hire", "boat-4", [
        ("Can my 16 year old steer the boat?", "Skipper Training Agent", "start", "Yes, if an adult who had the lesson is beside them."),
        ("great. we've run out of water on board", "On-Board Help Agent", "switch", "There's a free water point at the next boatyard."),
        ("how long to get there", "Moorings & Route Agent", "switch", "About 40 minutes."),
    ]),
]
