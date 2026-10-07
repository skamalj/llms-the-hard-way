"""Realistic multi-turn TEST conversations for modernbert.ipynb (evaluation metric E10). Never used for training.

Run from the repo root: python data/modernbert_router/build_realistic_test_data.py

Written free-form, without templates, so the phrasing is varied the way real users write. 14 companies that appear
nowhere in the training data, the banking test or Cell 59, each with 3-4 broad agents as a real support desk would have.
Every user turn is labelled with the agent that should handle it and a turn type:
  start         first message of the conversation
  answer        short answer to the agent's own question ("Tuesday", "BA-2291")
  follow        follow-up on the same request
  aspect        same agent, a different aspect of its topic (our known weak spot)
  closing       "ok cheers", "great, thanks"
  also_stay     starts with "Also/And ..." but stays with the same agent
  switch        a clear move to another agent
  short_switch  a move to another agent in a few words ("and my fine?")
  return        back to an earlier topic / agent
  handoff_ok    "ok" right after the assistant handed the user to another agent
  branch        a message whose right agent depends on the history (its twin in another conversation goes elsewhere)
The assistant reply after a user turn is written as if the expected agent answered it.
"""
import json
from pathlib import Path

COMPANIES = {
    "pharmacy": {
        "Repeat Prescriptions Agent": "Handles prescriptions: refills, repeat prescriptions, transfers from other pharmacies and prescription status.",
        "Pharmacist Advice Agent": "Answers medicine questions: dosage, side effects, interactions and over-the-counter advice.",
        "Home Delivery Agent": "Handles home delivery of pharmacy orders: delivery slots, tracking and missed deliveries.",
    },
    "water utility": {
        "Water Billing Agent": "Explains water bills, meter charges and payment arrangements.",
        "Leaks & Repairs Agent": "Handles leaks, burst pipes, low pressure, discoloured water and repair visits.",
        "New Connections Agent": "Connects new properties and handles meter installation for new homes.",
    },
    "dating app": {
        "Profile & Account Agent": "Helps with profiles, photos, login problems and deleting or pausing an account.",
        "Subscriptions Agent": "Handles premium plans, renewals, cancellations and charges for the app.",
        "Safety & Reports Agent": "Handles reports about other users, harassment, fake profiles and blocking.",
    },
    "ride-hailing app": {
        "Trip Issues Agent": "Handles problems with a trip: route, driver behaviour, cancellations and wrong pickup points.",
        "Fares & Payments Agent": "Explains fares, surge pricing, refunds for overcharges and payment methods.",
        "Lost Items Agent": "Helps passengers recover items left in a car.",
    },
    "cruise line": {
        "Cruise Bookings Agent": "Books and changes cruises: cabins, dates, passengers and deposits.",
        "Onboard Services Agent": "Handles dining reservations, spa, drinks packages and special requests on board.",
        "Shore Excursions Agent": "Books and explains excursions at ports of call.",
    },
    "solar installer": {
        "Quotes & Survey Agent": "Prices solar systems and books site surveys.",
        "Installation Agent": "Schedules and manages installation days and the installation crew.",
        "Monitoring & Faults Agent": "Helps with the monitoring app, low output and inverter faults after installation.",
    },
    "pet food subscription": {
        "Orders & Deliveries Agent": "Handles pet food orders, delivery dates, missing boxes and changing the delivery address.",
        "Nutrition Advice Agent": "Advises on food choice, portions, allergies and switching recipes.",
        "Plan & Billing Agent": "Handles the subscription plan, pausing, skipping, cancelling and charges.",
    },
    "photo printing service": {
        "Print Orders Agent": "Handles print, photobook and canvas orders, delivery and order changes.",
        "Print Quality Agent": "Handles faded, cropped, blurry or damaged prints and reprints.",
        "Account & Storage Agent": "Helps with logins, uploads, albums and photo storage space.",
    },
    "car dealership": {
        "Sales & Test Drives Agent": "Helps choose a car, books test drives and handles new car orders.",
        "Service Appointments Agent": "Books servicing, MOTs and repairs at the workshop.",
        "Trade-In Agent": "Values part-exchange and trade-in vehicles.",
    },
    "driving school": {
        "Lesson Booking Agent": "Books, moves and cancels driving lessons and assigns instructors.",
        "Theory Test Agent": "Helps with the theory test: booking it, practice material and results.",
        "Fees & Packages Agent": "Explains lesson prices, packages, discounts and payments.",
    },
    "parking operator": {
        "Permits Agent": "Issues and renews residents' and business parking permits.",
        "Fines & Appeals Agent": "Handles parking fines, penalty notices and appeals.",
        "Parking Payments Agent": "Handles pay-by-phone parking, receipts and wrong charges.",
    },
    "electronics repair shop": {
        "Repair Requests Agent": "Takes new repair requests and quotes for broken devices.",
        "Repair Status Agent": "Gives updates on devices already in for repair and pickup times.",
        "Warranty Agent": "Handles warranty claims on repairs and repeat faults.",
    },
    "games console company": {
        "Online Account Agent": "Helps with console accounts, online subscriptions, sign-in and parental controls.",
        "Hardware Support Agent": "Fixes console and controller hardware faults, overheating and repairs.",
        "Digital Store Agent": "Handles game purchases, downloads, refunds and gift cards in the digital store.",
    },
}

# (company, conversation id, [(user message, expected agent, turn type, assistant reply or None)])
CONVERSATIONS = [
    ("pharmacy", "pharm-1", [
        ("Hi, I need a refill on my blood pressure tablets.", "Repeat Prescriptions Agent", "start", "Of course. Is it the amlodipine from Dr Shah?"),
        ("yes that one", "Repeat Prescriptions Agent", "answer", "Done, it'll be ready tomorrow after 2pm."),
        ("Can I take it with ibuprofen? I've got a bad back.", "Pharmacist Advice Agent", "switch", "It's best to avoid ibuprofen with your blood pressure; paracetamol is safer."),
        ("how many paracetamol a day max?", "Pharmacist Advice Agent", "follow", "Up to 8 tablets of 500mg in 24 hours, at least 4 hours apart."),
        ("ok thanks", "Pharmacist Advice Agent", "closing", "You're welcome."),
        ("Actually could you deliver the tablets instead of me collecting them?", "Home Delivery Agent", "switch", "Sure, morning or afternoon tomorrow?"),
        ("afternoon", "Home Delivery Agent", "answer", "Booked between 1 and 5pm."),
    ]),
    ("pharmacy", "pharm-2", [
        ("My delivery was supposed to come yesterday and nothing arrived.", "Home Delivery Agent", "start", "Sorry about that. What's your postcode?"),
        ("LS6 2AB", "Home Delivery Agent", "answer", "The driver missed you; I can resend it today."),
        ("please do", "Home Delivery Agent", "closing", "It's on its way this afternoon."),
        ("And is my inhaler prescription in that bag too?", "Repeat Prescriptions Agent", "switch", "Your inhaler is still waiting on the GP's approval."),
        ("how long does that usually take", "Repeat Prescriptions Agent", "follow", "Normally two working days."),
        ("Also, is it fine to use the inhaler more than twice a day?", "Pharmacist Advice Agent", "switch", "If you need it more often, speak to your GP; it may mean your asthma isn't controlled."),
        ("back to the delivery, will the driver ring the bell this time?", "Home Delivery Agent", "return", "Yes, I've added a note to ring and wait."),
    ]),
    ("water utility", "water-1", [
        ("There's water bubbling up from the pavement outside my house.", "Leaks & Repairs Agent", "start", "Thanks for reporting it. Is it a steady flow or a small trickle?"),
        ("steady, quite a lot", "Leaks & Repairs Agent", "answer", "We'll send a crew within 4 hours."),
        ("Will my water be cut off while they fix it?", "Leaks & Repairs Agent", "aspect", "Possibly for an hour or two; we'll text you before."),
        ("And my bill jumped this quarter, is that from the leak?", "Water Billing Agent", "switch", "A leak on the public side isn't charged to you. Your bill rose because of an estimated reading."),
        ("I can send a real reading", "Water Billing Agent", "follow", "Great, what does the meter show?"),
        ("00412", "Water Billing Agent", "answer", "Thanks, I've recalculated it; it's £31 lower."),
        ("ok great", "Water Billing Agent", "closing", None),
    ]),
    ("water utility", "water-2", [
        ("We're building a new house and need a water connection.", "New Connections Agent", "start", "Congratulations! Do you have the site address and planning reference?"),
        ("yes, PL/2291 at 4 Orchard Way", "New Connections Agent", "answer", "Thanks. A survey can be done next week. Which day suits?"),
        ("Thursday", "New Connections Agent", "answer", "Booked for Thursday."),
        ("how much is it going to cost?", "New Connections Agent", "aspect", "A standard connection is about £1,800; the survey confirms the price."),
        ("Separately, my current flat has brown water from the taps since this morning.", "Leaks & Repairs Agent", "switch", "That's usually sediment after mains work. Run the cold tap for 20 minutes."),
        ("still brown after 20 mins", "Leaks & Repairs Agent", "follow", "Then I'll send a technician today."),
        ("thanks", "Leaks & Repairs Agent", "closing", None),
    ]),
    ("dating app", "date-1", [
        ("I can't upload a new photo, it keeps failing.", "Profile & Account Agent", "start", "Is the photo larger than 10MB?"),
        ("it's 14MB", "Profile & Account Agent", "answer", "That's the problem; please resize it under 10MB."),
        ("worked, thanks", "Profile & Account Agent", "closing", "Great."),
        ("Someone keeps messaging me even after I said stop.", "Safety & Reports Agent", "switch", "I'm sorry. Can you share their profile name?"),
        ("Dave_88", "Safety & Reports Agent", "answer", "I've blocked them for you and our team will review the account."),
        ("Also why was I charged twice this month?", "Subscriptions Agent", "switch", "I see a duplicate renewal; the extra charge will be refunded within 5 days."),
        ("ok and can I cancel premium after that?", "Subscriptions Agent", "follow", "Yes, you can cancel any time; it stays active until the end of the month."),
    ]),
    ("dating app", "date-2", [
        ("I want to pause my account for a few months.", "Profile & Account Agent", "start", "You can hide your profile in settings. Do you also want to stop your subscription?"),
        ("yes stop that too", "Subscriptions Agent", "short_switch", "Done, your premium won't renew."),
        ("will I lose my matches if I pause?", "Profile & Account Agent", "return", "No, your matches stay saved while you're hidden."),
        ("good", "Profile & Account Agent", "closing", None),
    ]),
    ("ride-hailing app", "ride-1", [
        ("My driver took a really long route and I was charged £38 instead of £20.", "Fares & Payments Agent", "start", "Sorry about that. Can you share the trip date?"),
        ("last night around 11", "Fares & Payments Agent", "answer", "I can see the detour; I've refunded £18."),
        ("thanks. the driver was also really rude", "Trip Issues Agent", "switch", "I'm sorry to hear that. I've logged a complaint about the driver."),
        ("I think I left my scarf in the car too", "Lost Items Agent", "switch", "I'll contact the driver. What colour is it?"),
        ("grey wool", "Lost Items Agent", "answer", "Thanks, I'll update you once the driver replies."),
        ("and the refund goes back to my card?", "Fares & Payments Agent", "return", "Yes, to the card you paid with, within 3 days."),
    ]),
    ("ride-hailing app", "ride-2", [
        ("The driver cancelled on me twice and I missed my train.", "Trip Issues Agent", "start", "I'm really sorry. Was it this morning's trips from Kings Road?"),
        ("yeah", "Trip Issues Agent", "answer", "I can see both cancellations; I've reported the drivers."),
        ("I was charged a cancellation fee though", "Fares & Payments Agent", "switch", "That shouldn't happen when the driver cancels; I've removed the £5 fee."),
        ("ok cheers", "Fares & Payments Agent", "closing", None),
    ]),
    ("cruise line", "cruise-1", [
        ("I'd like to book the 7-night Norway cruise in June for two.", "Cruise Bookings Agent", "start", "Lovely. Inside, ocean view or balcony cabin?"),
        ("balcony", "Cruise Bookings Agent", "answer", "A balcony cabin is £2,450 per person. Shall I hold it?"),
        ("yes hold it", "Cruise Bookings Agent", "follow", "Held for 48 hours; a £200 deposit secures it."),
        ("What excursions are there in Bergen?", "Shore Excursions Agent", "switch", "There's a funicular and city walk, or a fjord boat trip."),
        ("the fjord one sounds good, how long is it", "Shore Excursions Agent", "follow", "About 4 hours, back an hour before departure."),
        ("Also my wife is vegan, can dinners be arranged?", "Onboard Services Agent", "switch", "Yes, I'll note vegan meals for every dinner."),
        ("perfect", "Onboard Services Agent", "closing", None),
        ("one more thing on the booking, can we add my mum to the cabin?", "Cruise Bookings Agent", "return", None),
    ]),
    ("cruise line", "cruise-2", [
        ("We're on board now and want to book the spa for tomorrow.", "Onboard Services Agent", "start", "Of course. Morning or afternoon?"),
        ("morning please", "Onboard Services Agent", "answer", "Booked for 10am."),
        ("how much is the drinks package per day?", "Onboard Services Agent", "aspect", "£59 per person per day."),
        ("and is the snorkelling trip in Santorini still available?", "Shore Excursions Agent", "switch", "Two places left. Shall I book them?"),
        ("yes both", "Shore Excursions Agent", "answer", "Booked."),
    ]),
    ("solar installer", "solar-1", [
        ("How much would solar panels cost for a 3-bed semi?", "Quotes & Survey Agent", "start", "Usually £6,000 to £8,000. A survey gives an exact price. Shall I book one?"),
        ("yes please, weekends only", "Quotes & Survey Agent", "answer", "Saturday the 12th at 10am?"),
        ("works", "Quotes & Survey Agent", "answer", "Booked."),
        ("If I go ahead, how long does installation take?", "Installation Agent", "switch", "Normally one to two days on site."),
        ("do I need to be home both days", "Installation Agent", "follow", "Only at the start and the end of each day."),
    ]),
    ("solar installer", "solar-2", [
        ("My panels were installed last month but the app shows almost no output.", "Monitoring & Faults Agent", "start", "Is the inverter showing a red or green light?"),
        ("red", "Monitoring & Faults Agent", "answer", "That's an inverter fault. Try switching it off for 5 minutes."),
        ("still red", "Monitoring & Faults Agent", "follow", "I'll book an engineer visit."),
        ("Also the installers left scaffolding poles in my garden", "Installation Agent", "switch", "Apologies, I'll arrange collection this week."),
        ("and when is the engineer coming for the inverter?", "Monitoring & Faults Agent", "return", "Wednesday morning."),
    ]),
    ("pet food subscription", "pet-1", [
        ("My dog's box didn't arrive this week.", "Orders & Deliveries Agent", "start", "Sorry! The courier shows it was left with a neighbour at number 14."),
        ("ah found it, thanks", "Orders & Deliveries Agent", "closing", "Great."),
        ("He's been scratching a lot, could it be the chicken recipe?", "Nutrition Advice Agent", "switch", "It could be a chicken allergy. Our salmon recipe is a good alternative."),
        ("how should I switch him over", "Nutrition Advice Agent", "follow", "Mix the new food in gradually over 7 days."),
        ("can you change next week's box to salmon then", "Orders & Deliveries Agent", "switch", "Done, next week's box is salmon."),
        ("and will the price change?", "Plan & Billing Agent", "short_switch", "Salmon is £2 more per box."),
    ]),
    ("pet food subscription", "pet-2", [
        ("We're going on holiday, can I skip two deliveries?", "Plan & Billing Agent", "start", "Yes. Which dates?"),
        ("the 3rd and the 17th", "Plan & Billing Agent", "answer", "Both skipped; you won't be charged for them."),
        ("Also can I pause the plan entirely after that?", "Plan & Billing Agent", "also_stay", "Yes, pausing is free for up to 3 months."),
        ("How much food should a 20kg dog actually eat per day?", "Nutrition Advice Agent", "switch", "About 280g of our dry food a day."),
    ]),
    ("photo printing service", "photo-1", [
        ("My photobook arrived and the pictures are all cropped at the edges.", "Print Quality Agent", "start", "Sorry. Did you see a warning about the safe zone when you ordered?"),
        ("no warning at all", "Print Quality Agent", "answer", "Then I'll reprint it for free."),
        ("thank you", "Print Quality Agent", "closing", None),
        ("When will the reprint arrive?", "Print Orders Agent", "switch", "It ships in 3 days and arrives 2 days later."),
        ("can it go to my office address instead", "Print Orders Agent", "follow", "Yes, what's the address?"),
        ("Unit 4, Brook Park, M15 6JJ", "Print Orders Agent", "answer", "Updated."),
        ("And my storage says full, can I free space without losing photos?", "Account & Storage Agent", "switch", "Yes, download an album then delete it, or upgrade to 100GB."),
    ]),
    ("photo printing service", "photo-2", [
        ("I can't log into my account, it says email not found.", "Account & Storage Agent", "start", "Did you sign up with Google?"),
        ("oh yes I did", "Account & Storage Agent", "answer", "Then use 'Sign in with Google' and you'll be in."),
        ("in now. I want to order 30 prints from my Italy album", "Print Orders Agent", "switch", "Gloss or matte?"),
        ("matte", "Print Orders Agent", "answer", "Added to your basket."),
        ("will they be faded like last time?", "Print Quality Agent", "switch", "We've changed printers since then, and we'll reprint free if anything is faded."),
    ]),
    ("car dealership", "car-1", [
        ("I'd like to test drive the new Corolla hybrid.", "Sales & Test Drives Agent", "start", "Happy to. This Saturday or next week?"),
        ("saturday", "Sales & Test Drives Agent", "answer", "Saturday at 11am is booked."),
        ("What would you give me for my 2017 Golf?", "Trade-In Agent", "switch", "Roughly £8,500 depending on mileage. How many miles?"),
        ("about 62k", "Trade-In Agent", "answer", "Then around £8,200; we'll confirm on the day."),
        ("Also it needs its MOT next month, can you do that?", "Service Appointments Agent", "switch", "Yes, which date?"),
        ("the 14th", "Service Appointments Agent", "answer", "Booked for the 14th at 9am."),
        ("back to the Corolla, does it come in blue?", "Sales & Test Drives Agent", "return", None),
    ]),
    ("car dealership", "car-2", [
        ("My car is due a service, can I book it in?", "Service Appointments Agent", "start", "Sure. What's the registration?"),
        ("YK19 ABC", "Service Appointments Agent", "answer", "Thanks. Next Tuesday at 8:30?"),
        ("fine. how long will it take?", "Service Appointments Agent", "aspect", "About 3 hours; a courtesy car is available."),
        ("While it's in, can someone value it? I might trade it in.", "Trade-In Agent", "switch", "Yes, we'll value it during the service."),
    ]),
    ("driving school", "drive-1", [
        ("I want to book my first driving lesson.", "Lesson Booking Agent", "start", "Great! Weekdays or weekends?"),
        ("weekdays after 5", "Lesson Booking Agent", "answer", "Tuesday at 5:30pm with Sarah?"),
        ("ok", "Lesson Booking Agent", "closing", "Booked."),
        ("how much is it?", "Fees & Packages Agent", "branch", "£38 per hour, or £340 for a 10-hour package."),
        ("I'll take the package", "Fees & Packages Agent", "follow", "Great, I'll send the payment link."),
        ("Also do I need to pass the theory test first?", "Theory Test Agent", "switch", "No, but you need it before booking your practical test."),
    ]),
    ("driving school", "drive-2", [
        ("I failed my theory test by two points.", "Theory Test Agent", "start", "So close! Do you want to rebook it?"),
        ("yes as soon as possible", "Theory Test Agent", "answer", "The earliest is in 10 days. Shall I book it?"),
        ("yes", "Theory Test Agent", "answer", "Booked."),
        ("how much is it?", "Theory Test Agent", "branch", "The test fee is £23."),
        ("and can I move my Thursday lesson to Friday?", "Lesson Booking Agent", "short_switch", "Done, Friday at the same time."),
    ]),
    ("parking operator", "park-1", [
        ("I got a parking fine but I had a valid permit on display.", "Fines & Appeals Agent", "start", "You can appeal. What's the fine reference?"),
        ("PCN44821", "Fines & Appeals Agent", "answer", "Thanks. Please upload a photo of the permit."),
        ("uploaded", "Fines & Appeals Agent", "follow", "Received; the appeal is under review."),
        ("My permit expires next week, can I renew it now?", "Permits Agent", "switch", "Yes, the renewal is £60 for a year. Shall I start it?"),
        ("go ahead", "Permits Agent", "answer", "Renewed until next October."),
        ("and the fine, how long will the appeal take?", "Fines & Appeals Agent", "return", "Up to 14 days."),
    ]),
    ("parking operator", "park-2", [
        ("The parking app charged me for 3 hours but I only stayed 1.", "Parking Payments Agent", "start", "Did you end the session in the app when you left?"),
        ("no I forgot", "Parking Payments Agent", "answer", "I can refund the extra 2 hours this once."),
        ("thanks. can I get a receipt for my expenses?", "Parking Payments Agent", "aspect", "Sent to your email."),
        ("Also I'd like a business permit for my van", "Permits Agent", "switch", "You'll need the van's V5 document. Shall I send the form?"),
    ]),
    ("electronics repair shop", "repair-1", [
        ("My laptop screen is cracked, can you fix it?", "Repair Requests Agent", "start", "Yes. What model is it?"),
        ("Dell XPS 13", "Repair Requests Agent", "answer", "The screen replacement is £180 and takes 3 days."),
        ("ok book it in", "Repair Requests Agent", "follow", "Bring it in any time; your reference is R-5531."),
        ("I also dropped my phone in for a battery last week, is it ready?", "Repair Status Agent", "switch", "Your phone is ready to collect."),
        ("what time do you close", "Repair Status Agent", "follow", "6pm today."),
    ]),
    ("electronics repair shop", "repair-2", [
        ("You replaced my phone battery 2 months ago and it's draining fast again.", "Warranty Agent", "start", "Repairs have a 6-month warranty. What's the repair reference?"),
        ("R-4410", "Warranty Agent", "answer", "Found it. We'll replace the battery again for free."),
        ("great, when can I bring it", "Warranty Agent", "follow", "Any day this week."),
        ("and my tablet that's in for the charging port, any news?", "Repair Status Agent", "switch", "The part arrives tomorrow; it'll be ready Friday."),
        ("ok", "Repair Status Agent", "closing", None),
    ]),
    ("games console company", "game-1", [
        ("My controller keeps drifting to the left.", "Hardware Support Agent", "start", "Have you tried recalibrating it in settings?"),
        ("yes didn't help", "Hardware Support Agent", "answer", "Then it's a hardware fault; it's under warranty, so we'll replace it."),
        ("how do I send it", "Hardware Support Agent", "follow", "I'll email a prepaid label."),
        ("Also I bought a game twice by mistake", "Digital Store Agent", "switch", "I can refund the duplicate. Which game?"),
        ("Racer X", "Digital Store Agent", "answer", "Refunded to your wallet."),
        ("and how do I stop my kid buying stuff?", "Online Account Agent", "switch", "Set a spending limit in parental controls."),
    ]),
    ("games console company", "game-2", [
        ("I can't sign in to my account on the console.", "Online Account Agent", "start", "Do you get an error code?"),
        ("E-102", "Online Account Agent", "answer", "That's a password issue; I've sent a reset link."),
        ("done, I'm in", "Online Account Agent", "closing", "Great."),
        ("My console is also getting really hot and loud", "Hardware Support Agent", "switch", "Make sure the vents have space; is it in a cabinet?"),
        ("yeah it's in a cabinet", "Hardware Support Agent", "answer", "Move it out so air can flow, and it should cool down."),
        ("ok. my gift card isn't working in the store either", "Digital Store Agent", "short_switch", "What's the card's first four characters?"),
    ]),
    ("water utility", "water-3", [
        ("Can I pay my water bill in monthly instalments?", "Water Billing Agent", "start", "Yes, £42 a month would clear it by March. Shall I set that up?"),
        ("yes", "Water Billing Agent", "answer", "Done."),
        ("Also can I get paper bills instead of email?", "Water Billing Agent", "also_stay", "Sure, paper bills from next quarter."),
        ("and why is there a sewerage charge on it?", "Water Billing Agent", "aspect", "Sewerage is charged for the waste water you return to the network."),
        ("and the low pressure in my shower?", "Leaks & Repairs Agent", "short_switch", "Does it affect all taps or only the shower?"),
        ("all taps", "Leaks & Repairs Agent", "answer", "Then it's on our side; I'll check the mains in your street."),
    ]),
    ("dating app", "date-3", [
        ("A profile I matched with is clearly fake, it's using a celebrity's photos.", "Safety & Reports Agent", "start", "Thanks for telling us. What's the profile name?"),
        ("Jessie_xo", "Safety & Reports Agent", "answer", "I've removed it."),
        ("Also, can I stop people seeing my distance?", "Profile & Account Agent", "switch", "Yes, switch off 'Show distance' in your profile settings."),
        ("And is the premium plan cheaper if I pay yearly?", "Subscriptions Agent", "switch", "Yearly works out at 40% less."),
        ("ok and can I switch to yearly mid-month?", "Subscriptions Agent", "aspect", "Yes, the unused part of this month is credited."),
    ]),
    ("ride-hailing app", "ride-3", [
        ("I left my phone in the car this morning!", "Lost Items Agent", "start", "Let's get it back. Which trip was it?"),
        ("the 8:15 to the station", "Lost Items Agent", "answer", "I've contacted the driver; he has it."),
        ("how do I get it back?", "Lost Items Agent", "follow", "He can drop it off for a £15 return fee, or you can collect it."),
        ("drop it off", "Lost Items Agent", "answer", "He'll bring it at 6pm."),
        ("will the £15 go on my card?", "Fares & Payments Agent", "branch", "Yes, it's charged to your card on file."),
    ]),
    ("cruise line", "cruise-3", [
        ("We need to change our cruise dates from May to July.", "Cruise Bookings Agent", "start", "The July sailing has cabins. There's a £100 change fee. Go ahead?"),
        ("go ahead", "Cruise Bookings Agent", "answer", "Changed to July 14th."),
        ("Also can we upgrade to a balcony?", "Cruise Bookings Agent", "also_stay", "Yes, for £340 more per person."),
        ("and the excursions we booked for May?", "Shore Excursions Agent", "short_switch", "I'll move them to the July ports; the times will change slightly."),
        ("thanks. Is there a kids' club on board?", "Onboard Services Agent", "switch", "Yes, for ages 3 to 12, free of charge."),
    ]),
    ("electronics repair shop", "repair-3", [
        ("Is my laptop ready yet? Reference R-5531.", "Repair Status Agent", "start", "It's being tested now; ready after 3pm."),
        ("will the screen be covered if it cracks again?", "Warranty Agent", "switch", "The new screen has a 6-month warranty against defects, not accidental damage."),
        ("ok. and could you also look at my speaker that won't charge?", "Repair Requests Agent", "switch", "Yes, bring it in with the laptop pickup."),
        ("great", "Repair Requests Agent", "closing", None),
    ]),
    ("photo printing service", "photo-3", [
        ("Can I add another canvas to the order I placed yesterday?", "Print Orders Agent", "start", "Yes, if it hasn't printed yet. What size?"),
        ("40 by 60", "Print Orders Agent", "answer", "Added; the order total is now £78."),
        ("Also could it ship with the rest?", "Print Orders Agent", "also_stay", "Yes, both ship together on Friday."),
        ("one of my photos looked blurry in the preview", "Print Quality Agent", "switch", "It's low resolution; it'll print soft at that size. Want a smaller size?"),
        ("yes make it 20 by 30", "Print Quality Agent", "answer", None),
    ]),
    ("parking operator", "park-3", [
        ("I want to appeal a fine, the sign was hidden behind a tree.", "Fines & Appeals Agent", "start", "Please send a photo of the sign and the fine reference."),
        ("PCN50213, photo attached", "Fines & Appeals Agent", "answer", "Received. Payments for this fine are on hold during the appeal; the Parking Payments team can confirm that."),
        ("Can you pass me to them?", "Fines & Appeals Agent", "follow", "Sure, I'll pass you to the Parking Payments Agent."),
        ("ok", "Parking Payments Agent", "handoff_ok", "Hi, yes, nothing will be charged while the appeal is open."),
        ("great, thanks", "Parking Payments Agent", "closing", None),
    ]),
    ("games console company", "game-3", [
        ("A game I bought won't download, it's stuck at 0%.", "Digital Store Agent", "start", "Try clearing the download queue and restarting."),
        ("didn't work", "Digital Store Agent", "follow", "I'll refund it so you can buy it again cleanly."),
        ("ok. how much storage does the console have left though?", "Hardware Support Agent", "switch", "Settings > Storage shows it; the game needs 85GB."),
        ("72GB free", "Hardware Support Agent", "answer", "Then that's the problem. Delete something or add an external drive."),
        ("and my online subscription renews tomorrow, can I stop that?", "Online Account Agent", "switch", "Yes, I've turned off auto-renew."),
    ]),
    ("pharmacy", "pharm-3", [
        ("Can you transfer my prescriptions from Boots to you?", "Repeat Prescriptions Agent", "start", "Yes. What's your date of birth?"),
        ("12 March 1980", "Repeat Prescriptions Agent", "answer", "Thanks, the transfer will take 2 days."),
        ("One of them is new and I'm not sure how to take it.", "Repeat Prescriptions Agent", "follow",
         "Our pharmacist can explain that; I'll pass you to the Pharmacist Advice Agent."),
        ("ok", "Pharmacist Advice Agent", "handoff_ok", "Hi, which medicine is it?"),
        ("sertraline", "Pharmacist Advice Agent", "answer", "Take it once a day, same time, with or without food."),
    ]),
]

TRAINING_DOMAINS = json.load(open("data/modernbert_router/generic/domains.json"))
training_agents = {a for d in TRAINING_DOMAINS.values() for a in d["agents"]}

records = []
for company, cid, turns in CONVERSATIONS:
    agents = COMPANIES[company]
    assert not set(agents) & training_agents, (cid, set(agents) & training_agents)
    messages, user_turns = [], []
    for user_msg, expected, kind, reply in turns:
        assert expected in agents, (cid, expected)
        user_turns.append({"message_index": len(messages), "expected_agent": expected, "turn_type": kind})
        messages.append({"role": "user", "content": user_msg})
        if reply:
            messages.append({"role": "assistant", "content": reply})
    assert len(messages) <= 15 and messages[0]["role"] == "user", cid
    records.append({"id": cid, "company": company, "agents": agents, "messages": messages, "user_turns": user_turns})

out = Path("data/modernbert_router/realistic/conversations.json")
out.parent.mkdir(parents=True, exist_ok=True)
json.dump(records, open(out, "w"), indent=1, ensure_ascii=False)
n_turns = sum(len(r["user_turns"]) for r in records)
from collections import Counter
print(f"{len(records)} conversations, {len(COMPANIES)} companies, {n_turns} user turns")
print(dict(Counter(u["turn_type"] for r in records for u in r["user_turns"])))
