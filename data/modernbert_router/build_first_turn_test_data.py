"""First-turn routing TEST set for modernbert.ipynb (evaluation metric E11). Never used for training.

Run from the repo root: python data/modernbert_router/build_first_turn_test_data.py

One incoming user message, no history, no current agent: pick the right agent among 5 candidates.
10 companies that appear nowhere in the training data, the banking test, Cell 59 or E10. Each has 5 agents,
including deliberately close pairs. Messages are written free-form (no templates). Each has a type:
  clear     names the need directly
  short     1-4 words
  indirect  describes the situation without the obvious keyword
  close     sits between two similar agents of the same company
  noisy     typos / lower case / missing punctuation, as real users type
"""
import json
from collections import Counter
from pathlib import Path

COMPANIES = {
    "online grocery": {
        "Online Orders Agent": "Places, changes and cancels online grocery orders and delivery slots.",
        "Missing & Substituted Items Agent": "Handles items missing from a delivery, wrong substitutions and damaged goods, with refunds for them.",
        "Loyalty Card Agent": "Handles loyalty card points, vouchers and linking a card to an account.",
        "Click & Collect Agent": "Handles collecting online orders from a store: collection times, lockers and collection problems.",
        "Store Feedback Agent": "Takes feedback and complaints about physical stores, staff and opening hours.",
    },
    "smartwatch maker": {
        "Device Setup Agent": "Helps set up a new watch: pairing with a phone, first start and language.",
        "Sync & App Agent": "Fixes the companion app: data not syncing, notifications and app crashes.",
        "Battery & Hardware Agent": "Handles battery drain, charging problems, cracked screens and broken straps.",
        "Health Features Agent": "Explains heart-rate, sleep, step and workout tracking.",
        "Returns Agent": "Handles returning a watch within the return period and refunds for returns.",
    },
    "council waste services": {
        "Bin Collections Agent": "Handles regular household bin collection days and missed collections.",
        "Bulky Waste Agent": "Books collection of large items such as sofas, fridges and mattresses.",
        "Recycling Agent": "Explains what goes in which recycling bin and orders new recycling boxes.",
        "Garden Waste Agent": "Handles the paid garden waste subscription and its collections.",
        "Fly-Tipping Agent": "Takes reports of rubbish dumped illegally in public places.",
    },
    "online marketplace for sellers": {
        "Seller Payouts Agent": "Handles when and how sellers are paid for their sales.",
        "Listings Agent": "Helps create and edit product listings, photos and prices.",
        "Disputes Agent": "Handles buyer complaints, returns opened by buyers and item-not-received claims.",
        "Shipping Labels Agent": "Creates postage labels and fixes label and courier pickup problems.",
        "Account Verification Agent": "Verifies seller identity and business documents and lifts account holds.",
    },
    "home appliance maker": {
        "Engineer Visits Agent": "Books an engineer to repair a broken appliance at home.",
        "Spare Parts Agent": "Sells replacement parts such as filters, shelves, seals and hoses.",
        "Warranty Registration Agent": "Registers new appliances and extends warranties.",
        "Product Manuals Agent": "Explains how to use appliance settings and programmes, and sends manuals.",
        "Safety Recalls Agent": "Handles safety recalls and checks whether a model is affected.",
    },
    "cinema chain": {
        "Ticket Booking Agent": "Books cinema tickets and seats, and handles booking errors.",
        "Refunds & Exchanges Agent": "Refunds or exchanges tickets for cancelled or missed showings.",
        "Cinema Membership Agent": "Handles the monthly cinema membership: joining, cancelling and member benefits.",
        "Cinema Accessibility Agent": "Arranges wheelchair spaces, subtitled and audio-described screenings and carer tickets.",
        "Food & Drink Agent": "Handles snack orders, pre-ordered food and food allergen information.",
    },
    "bike share scheme": {
        "Rider Account Agent": "Handles sign-up, login, payment cards and ride history.",
        "Bike Faults Agent": "Takes reports of broken bikes: brakes, flat tyres, gears and lights.",
        "Docking Stations Agent": "Handles full or empty docks and bikes that will not lock or release.",
        "Ride Charges Agent": "Explains ride prices and fixes wrong or extra charges.",
        "Passes & Plans Agent": "Sells and manages day passes, annual passes and student plans.",
    },
    "accounting software": {
        "Invoicing Agent": "Helps create, send and chase invoices and quotes.",
        "Payroll Agent": "Helps run payroll, payslips and employee pay settings.",
        "Bank Feeds Agent": "Connects bank accounts and fixes transactions that do not import.",
        "Tax Returns Agent": "Helps prepare and file VAT and tax returns from the software.",
        "Users & Login Agent": "Manages user logins, passwords and permissions for the team.",
    },
    "hair salon chain": {
        "Salon Bookings Agent": "Books, moves and cancels hair appointments.",
        "Prices & Services Agent": "Explains treatments, prices and how long services take.",
        "Complaints Agent": "Handles complaints about a cut, colour or treatment and arranges fixes.",
        "Gift Vouchers Agent": "Sells gift vouchers and checks voucher balances.",
        "Hair Products Agent": "Advises on and sells shampoos, conditioners and styling products.",
    },
    "charity": {
        "Donations Agent": "Handles one-off and monthly donations, changing or stopping them, and tax relief on donations.",
        "Fundraising Events Agent": "Handles sign-ups and questions for runs, walks and sponsored events.",
        "Volunteering Agent": "Matches people to volunteering roles and handles volunteer questions.",
        "Charity Shops Agent": "Handles donating goods to charity shops and shop opening times.",
        "Data & Privacy Agent": "Handles mailing preferences, unsubscribing and personal data requests.",
    },
}

# (company, message, correct agent, type)
MESSAGES = [
    # online grocery
    ("online grocery", "I need to change my delivery slot to Saturday morning.", "Online Orders Agent", "clear"),
    ("online grocery", "My order arrived without the eggs and the milk.", "Missing & Substituted Items Agent", "clear"),
    ("online grocery", "points not showing", "Loyalty Card Agent", "short"),
    ("online grocery", "I'm outside the store and the locker won't open with my code.", "Click & Collect Agent", "indirect"),
    ("online grocery", "The staff at the Hill Street branch were really rude to my mum.", "Store Feedback Agent", "clear"),
    ("online grocery", "They swapped my oat milk for cow's milk, I'm lactose intolerant.", "Missing & Substituted Items Agent", "indirect"),
    ("online grocery", "can i add bananas to tomorrows order", "Online Orders Agent", "noisy"),
    ("online grocery", "Where do I pick up my order at the Riverside store, and until what time?", "Click & Collect Agent", "close"),
    ("online grocery", "cancel my order", "Online Orders Agent", "short"),
    ("online grocery", "Half the eggs in my delivery were smashed.", "Missing & Substituted Items Agent", "close"),
    # smartwatch maker
    ("smartwatch maker", "My new watch won't pair with my iPhone.", "Device Setup Agent", "clear"),
    ("smartwatch maker", "Steps from yesterday never showed up in the app.", "Sync & App Agent", "indirect"),
    ("smartwatch maker", "battery dies by lunchtime", "Battery & Hardware Agent", "short"),
    ("smartwatch maker", "How does it work out my sleep score?", "Health Features Agent", "clear"),
    ("smartwatch maker", "I'd like to send it back, it's only been a week.", "Returns Agent", "indirect"),
    ("smartwatch maker", "the screen got a crack after i bumped it on a door", "Battery & Hardware Agent", "noisy"),
    ("smartwatch maker", "I don't get message notifications on the watch any more.", "Sync & App Agent", "close"),
    ("smartwatch maker", "Is the heart rate reading accurate during swimming?", "Health Features Agent", "close"),
    ("smartwatch maker", "first time turning it on, how do i change the language", "Device Setup Agent", "noisy"),
    ("smartwatch maker", "refund for return", "Returns Agent", "short"),
    # council waste services
    ("council waste services", "My bin wasn't emptied on Tuesday.", "Bin Collections Agent", "clear"),
    ("council waste services", "I need an old fridge freezer taken away.", "Bulky Waste Agent", "clear"),
    ("council waste services", "Can pizza boxes go in the blue bin?", "Recycling Agent", "indirect"),
    ("council waste services", "I want to sign up for the brown bin for grass cuttings.", "Garden Waste Agent", "close"),
    ("council waste services", "Someone dumped a mattress and bin bags in the alley behind our road.", "Fly-Tipping Agent", "indirect"),
    ("council waste services", "bin not emptied", "Bin Collections Agent", "short"),
    ("council waste services", "my garden waste bin was skipped this week", "Garden Waste Agent", "close"),
    ("council waste services", "how much to collect a sofa", "Bulky Waste Agent", "noisy"),
    ("council waste services", "need a new recycling box, mine got blown away", "Recycling Agent", "noisy"),
    ("council waste services", "what day is collection", "Bin Collections Agent", "short"),
    # online marketplace for sellers
    ("online marketplace for sellers", "When will I get paid for the sales I made last week?", "Seller Payouts Agent", "clear"),
    ("online marketplace for sellers", "I can't add more than 5 photos to my item.", "Listings Agent", "indirect"),
    ("online marketplace for sellers", "A buyer says the parcel never arrived and opened a case against me.", "Disputes Agent", "clear"),
    ("online marketplace for sellers", "The courier didn't turn up for the pickup I booked.", "Shipping Labels Agent", "indirect"),
    ("online marketplace for sellers", "My account is on hold and asks for ID.", "Account Verification Agent", "clear"),
    ("online marketplace for sellers", "payout delayed", "Seller Payouts Agent", "short"),
    ("online marketplace for sellers", "buyer wants to return the jacket, says it's the wrong size", "Disputes Agent", "noisy"),
    ("online marketplace for sellers", "how do i change the price on my listing", "Listings Agent", "noisy"),
    ("online marketplace for sellers", "The label printed with the wrong weight so the post office refused it.", "Shipping Labels Agent", "close"),
    ("online marketplace for sellers", "My money is stuck because they want my business registration documents.", "Account Verification Agent", "close"),
    # home appliance maker
    ("home appliance maker", "My washing machine stopped mid-cycle and shows error E21.", "Engineer Visits Agent", "indirect"),
    ("home appliance maker", "I need a new water filter for my fridge.", "Spare Parts Agent", "clear"),
    ("home appliance maker", "I just bought a dishwasher and want to register it.", "Warranty Registration Agent", "clear"),
    ("home appliance maker", "Which programme should I use for wool jumpers?", "Product Manuals Agent", "indirect"),
    ("home appliance maker", "Is my tumble dryer one of the recalled ones?", "Safety Recalls Agent", "clear"),
    ("home appliance maker", "oven not heating", "Engineer Visits Agent", "short"),
    ("home appliance maker", "the door seal on my washer is torn, can i buy just the seal", "Spare Parts Agent", "noisy"),
    ("home appliance maker", "Can I extend the guarantee on my fridge for another two years?", "Warranty Registration Agent", "close"),
    ("home appliance maker", "I got a letter saying my model might be a fire risk.", "Safety Recalls Agent", "indirect"),
    ("home appliance maker", "lost the manual", "Product Manuals Agent", "short"),
    # cinema chain
    ("cinema chain", "I want two tickets for the 8pm showing of Dune tonight.", "Ticket Booking Agent", "clear"),
    ("cinema chain", "The film was cancelled because the projector broke, can I get my money back?", "Refunds & Exchanges Agent", "clear"),
    ("cinema chain", "How do I cancel my monthly membership?", "Cinema Membership Agent", "clear"),
    ("cinema chain", "Do you have subtitled screenings for deaf viewers this week?", "Cinema Accessibility Agent", "clear"),
    ("cinema chain", "Do the nachos contain gluten?", "Food & Drink Agent", "indirect"),
    ("cinema chain", "I booked the wrong day by mistake, can I swap to Friday?", "Refunds & Exchanges Agent", "close"),
    ("cinema chain", "my booking confirmation never came through but i was charged", "Ticket Booking Agent", "noisy"),
    ("cinema chain", "wheelchair space", "Cinema Accessibility Agent", "short"),
    ("cinema chain", "Do members get discounts on popcorn?", "Cinema Membership Agent", "close"),
    ("cinema chain", "pre-order snacks", "Food & Drink Agent", "short"),
    # bike share scheme
    ("bike share scheme", "The brakes on bike 4471 barely work.", "Bike Faults Agent", "clear"),
    ("bike share scheme", "The dock on Market Street is full and I can't return my bike.", "Docking Stations Agent", "clear"),
    ("bike share scheme", "I was charged £12 for a 10 minute ride.", "Ride Charges Agent", "clear"),
    ("bike share scheme", "Is there a student discount on the annual pass?", "Passes & Plans Agent", "clear"),
    ("bike share scheme", "I can't log in to the app after changing phones.", "Rider Account Agent", "indirect"),
    ("bike share scheme", "flat tyre", "Bike Faults Agent", "short"),
    ("bike share scheme", "the bike wont release from the dock even though the app says unlocked", "Docking Stations Agent", "noisy"),
    ("bike share scheme", "I returned it but the ride is still running and I'm being charged.", "Ride Charges Agent", "close"),
    ("bike share scheme", "need to update my payment card", "Rider Account Agent", "close"),
    ("bike share scheme", "day pass price", "Passes & Plans Agent", "short"),
    # accounting software
    ("accounting software", "How do I send a reminder for an unpaid invoice?", "Invoicing Agent", "clear"),
    ("accounting software", "Payslips this month show the wrong tax code for two staff.", "Payroll Agent", "indirect"),
    ("accounting software", "My bank transactions stopped importing on Monday.", "Bank Feeds Agent", "clear"),
    ("accounting software", "I need to file my VAT return by Friday.", "Tax Returns Agent", "clear"),
    ("accounting software", "How do I give my accountant access without seeing payroll?", "Users & Login Agent", "close"),
    ("accounting software", "reset password", "Users & Login Agent", "short"),
    ("accounting software", "can i put my logo on quotes", "Invoicing Agent", "noisy"),
    ("accounting software", "new starter joins next week, how do i add them to the pay run", "Payroll Agent", "noisy"),
    ("accounting software", "Some transactions from my business account show up twice.", "Bank Feeds Agent", "close"),
    ("accounting software", "VAT figure looks wrong on the return preview", "Tax Returns Agent", "close"),
    # hair salon chain
    ("hair salon chain", "Can I book a cut and blow-dry for Thursday afternoon?", "Salon Bookings Agent", "clear"),
    ("hair salon chain", "How much is a full head of highlights?", "Prices & Services Agent", "clear"),
    ("hair salon chain", "My colour came out orange instead of ash blonde.", "Complaints Agent", "indirect"),
    ("hair salon chain", "I'd like to buy a £50 voucher for my sister's birthday.", "Gift Vouchers Agent", "clear"),
    ("hair salon chain", "What shampoo would you recommend for curly frizzy hair?", "Hair Products Agent", "clear"),
    ("hair salon chain", "move my appointment", "Salon Bookings Agent", "short"),
    ("hair salon chain", "how long does a keratin treatment take", "Prices & Services Agent", "noisy"),
    ("hair salon chain", "How much is left on my voucher?", "Gift Vouchers Agent", "close"),
    ("hair salon chain", "The stylist cut way more off than I asked, I want it sorted.", "Complaints Agent", "close"),
    ("hair salon chain", "do you sell the serum you used on me", "Hair Products Agent", "noisy"),
    # charity
    ("charity", "I'd like to set up a monthly donation of £10.", "Donations Agent", "clear"),
    ("charity", "How do I sign up for the half marathon in your team?", "Fundraising Events Agent", "clear"),
    ("charity", "I'm retired and would love to help out a couple of days a week.", "Volunteering Agent", "indirect"),
    ("charity", "Can I drop off two bags of clothes at the Main Street shop?", "Charity Shops Agent", "clear"),
    ("charity", "Please stop sending me letters.", "Data & Privacy Agent", "indirect"),
    ("charity", "stop my direct debit", "Donations Agent", "short"),
    ("charity", "can you claim gift aid on what i gave last year", "Donations Agent", "noisy"),
    ("charity", "What information do you hold about me?", "Data & Privacy Agent", "close"),
    ("charity", "I'm doing a sponsored walk, where do I send the money I raised?", "Fundraising Events Agent", "close"),
    ("charity", "shop opening hours", "Charity Shops Agent", "short"),
]

training_agents = {a for d in json.load(open("data/modernbert_router/generic/domains.json")).values() for a in d["agents"]}
realistic = json.load(open("data/modernbert_router/realistic/conversations.json"))
e10_agents = {a for c in realistic for a in c["agents"]}
all_agents = {a for ag in COMPANIES.values() for a in ag}
assert not all_agents & training_agents, all_agents & training_agents
assert not all_agents & e10_agents, all_agents & e10_agents
assert all(len(ag) == 5 for ag in COMPANIES.values())

records = []
for k, (company, msg, agent, kind) in enumerate(MESSAGES):
    assert agent in COMPANIES[company], (company, agent)
    assert kind in {"clear", "short", "indirect", "close", "noisy"}, kind
    records.append({"id": f"ft-{k:03d}", "company": company, "message": msg, "target_agent": agent, "type": kind})

out = Path("data/modernbert_router/first_turn/messages.json")
out.parent.mkdir(parents=True, exist_ok=True)
json.dump({"companies": COMPANIES, "messages": records}, open(out, "w"), indent=1, ensure_ascii=False)
print(f"{len(records)} first-turn messages, {len(COMPANIES)} companies x 5 agents")
print(dict(Counter(r["type"] for r in records)))
print("messages per agent:", sorted(Counter(r["target_agent"] for r in records).values()))
