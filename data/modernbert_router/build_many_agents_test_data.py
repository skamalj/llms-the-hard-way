"""Many-agent routing test (fresh, written for exp/listwise-index): 12 businesses that appear in no training data, each with
9-15 agents, as large support desks have. Per business: 2 conversations of 5 user turns (routed live, with the assistant's
replies) and 6 first messages. Agents are distinct departments: no near-duplicate pairs, but each business has the usual
related ones (e.g. refunds vs payments), so the test is hard but every label can be read from the text.

    python build_many_agents_test_data.py      -> many_test/routing.json, many_test/first_turn.json
"""
import json
from pathlib import Path

OUT = Path(__file__).parent / "many_test"
STAY = {"answer", "follow", "aspect", "closing", "also_stay"}
SWITCH = {"switch", "short_switch", "return"}

# ---------------------------------------------------------------------------------------------------------------- businesses
B = {}

B["department_store"] = {
    "agents": {
        "Women's Fashion Agent": "Helps with women's clothing and shoes: sizes, styles, stock in other stores.",
        "Men's Fashion Agent": "Helps with men's clothing and shoes: sizes, styles, stock in other stores.",
        "Home & Furniture Agent": "Answers questions about sofas, beds, dining sets and home accessories.",
        "Electronics Agent": "Answers questions about TVs, laptops, headphones and small kitchen appliances.",
        "Beauty Counter Agent": "Books makeovers and answers questions about cosmetics, skincare and fragrances.",
        "Toys & Games Agent": "Helps with toys, board games and children's gifts.",
        "Personal Shopping Agent": "Books appointments with a personal stylist.",
        "Click & Collect Agent": "Handles online orders collected in store: collection points, times and ready notices.",
        "Home Delivery Agent": "Handles delivery of large items: delivery dates, missed deliveries and assembly on delivery.",
        "Returns & Refunds Agent": "Handles returns, exchanges and refunds for items bought in store or online.",
        "Store Card Agent": "Handles the store credit card: statements, payments, credit limits and card applications.",
        "Alterations Agent": "Books clothing alterations: hemming, taking in, and collection of altered items.",
        "Wedding List Agent": "Sets up and manages wedding gift lists.",
        "Gift Cards Agent": "Sells gift cards and checks gift card balances.",
        "Store Facilities Agent": "Answers questions about opening hours, parking, toilets, lifts and the cafe.",
    },
    "conversations": [
        [("I ordered a corner sofa online, when will it be delivered?", "Home Delivery Agent", "start",
          "It's due on Saturday between 8am and 1pm. Would you like the assembly service as well?"),
         ("yes please", "Home Delivery Agent", "answer", "Added. The team will assemble it in the room of your choice."),
         ("Also, the cushions in the photo look grey but mine are listed as stone, which is it?", "Home & Furniture Agent", "switch",
          "Stone is a warm light grey; it matches the photo closely."),
         ("ok and can I pay the delivery charge with my store card?", "Store Card Agent", "short_switch",
          "Yes, it will appear on next month's statement."),
         ("great, thanks", "Store Card Agent", "closing", None)],
        [("I want to return a dress I bought last week, it doesn't fit.", "Returns & Refunds Agent", "start",
          "No problem. Was it bought in store or online?"),
         ("online", "Returns & Refunds Agent", "answer", "You can return it to any store or by post with the free label in your account."),
         ("Could I just get the next size up in the same dress instead?", "Returns & Refunds Agent", "aspect",
          "Yes, choose exchange and we'll send the size up when we receive the return."),
         ("Is the size 14 actually in stock at the Leeds store? I'd rather try it on there.", "Women's Fashion Agent", "switch",
          "Leeds has two in size 14 on the second floor."),
         ("And is there parking near the Leeds store?", "Store Facilities Agent", "short_switch", None)],
    ],
    "first": [
        ("How much is left on the gift card my aunt gave me?", "Gift Cards Agent", "clear"),
        ("trousers too long, can you shorten them", "Alterations Agent", "short"),
        ("We're getting married in June and want guests to choose presents from your shop.", "Wedding List Agent", "indirect"),
        ("My online order says ready, which desk do I go to?", "Click & Collect Agent", "close"),
        ("noise cancelling hedphones under 200?", "Electronics Agent", "noisy"),
        ("I'd like someone to help me put together an outfit for an interview.", "Personal Shopping Agent", "clear"),
    ],
}

B["ferry_operator"] = {
    "agents": {
        "Bookings Agent": "Makes, changes and cancels ferry bookings for foot passengers and vehicles.",
        "Vehicle Measurements Agent": "Advises on vehicle sizes, roof boxes, trailers and caravans for the car deck.",
        "Cabins Agent": "Books and changes cabins and reclining seats on overnight crossings.",
        "Pets on Board Agent": "Handles travelling with dogs and cats: kennels, pet cabins and pet passports.",
        "Check-in & Port Agent": "Answers questions about check-in times, port directions and boarding.",
        "Accessibility Agent": "Arranges help for passengers with reduced mobility: lifts, wheelchairs and parking near the lifts.",
        "Onboard Dining Agent": "Answers questions about restaurants, menus and pre-booking meals on board.",
        "Delays & Cancellations Agent": "Handles delayed or cancelled sailings, weather disruption and rebooking after cancellations.",
        "Refunds Agent": "Processes refunds for cancelled bookings and compensation claims.",
        "Freight Agent": "Handles bookings for lorries and commercial freight.",
    },
    "conversations": [
        [("We're taking the car across on Friday night, can we get a cabin?", "Cabins Agent", "start",
          "Yes, there are four-berth cabins left. How many of you are travelling?"),
         ("two adults and a baby", "Cabins Agent", "answer", "A two-berth cabin with a travel cot would suit you. Shall I add it?"),
         ("yes. The car has a roof box though, does that change anything?", "Vehicle Measurements Agent", "switch",
          "A roof box usually takes the car over 1.85 m high, so it needs a high vehicle ticket."),
         ("it's 2.1 metres with the box", "Vehicle Measurements Agent", "answer", "Then you need the high vehicle category; the difference is £24."),
         ("can we book breakfast for the morning too?", "Onboard Dining Agent", "switch", None)],
        [("Our sailing this morning was cancelled because of the storm. What happens now?", "Delays & Cancellations Agent", "start",
          "I'm sorry. We can move you to tomorrow's 7am sailing at no cost. Would that work?"),
         ("is there anything this evening?", "Delays & Cancellations Agent", "follow", "The 9pm sailing has space for cars, yes."),
         ("ok put us on the 9pm", "Delays & Cancellations Agent", "follow", "Done. Your new booking reference is FX-5521."),
         ("We had to pay for a hotel last night because of the cancellation, can we claim that back?", "Refunds Agent", "switch",
          "Yes, send the hotel receipt with your booking reference and we'll review the claim."),
         ("And my mum uses a wheelchair, can we park near the lift on the 9pm?", "Accessibility Agent", "switch", None)],
    ],
    "first": [
        ("Can my dog stay in the car during the crossing?", "Pets on Board Agent", "clear"),
        ("check in closes when?", "Check-in & Port Agent", "short"),
        ("I run a haulage firm and need space for three lorries every Tuesday.", "Freight Agent", "indirect"),
        ("I need to move my booking to the following weekend.", "Bookings Agent", "close"),
        ("refund for cancelld trip pls", "Refunds Agent", "noisy"),
        ("Is the restaurant open on the early morning crossing?", "Onboard Dining Agent", "clear"),
    ],
}

B["water_utility"] = {
    "agents": {
        "Billing Agent": "Explains water bills, charges and payment dates.",
        "Payment Plans Agent": "Sets up instalment plans and help for customers struggling to pay.",
        "Meter Readings Agent": "Takes meter readings and answers questions about estimated readings.",
        "Meter Installation Agent": "Arranges free water meter fitting and meter replacements.",
        "Leaks & Bursts Agent": "Handles leaks in the street, burst pipes and flooding from water mains.",
        "Water Quality Agent": "Handles discoloured, cloudy or bad-tasting water and water hardness questions.",
        "Low Pressure Agent": "Handles low water pressure and no water supply.",
        "Sewerage Agent": "Handles blocked drains, sewer smells and sewage overflows.",
        "Moving Home Agent": "Opens and closes accounts when customers move in or out.",
        "New Connections Agent": "Handles water connections for new buildings and extensions.",
        "Complaints Agent": "Takes formal complaints about our service.",
    },
    "conversations": [
        [("My water has been coming out brown since this morning.", "Water Quality Agent", "start",
          "Sorry about that. Is it from every tap or just the kitchen?"),
         ("every tap", "Water Quality Agent", "answer", "There's work on the main in your street; run the cold tap for 20 minutes and it should clear."),
         ("Also the pressure upstairs is really weak since the work started", "Low Pressure Agent", "switch",
          "That can happen while the main is being flushed. It should recover by this evening."),
         ("it was weak last week too, before the work", "Low Pressure Agent", "follow", "Then I'll book an engineer to check your supply pipe."),
         ("thanks, that's all", "Low Pressure Agent", "closing", None)],
        [("I'm moving into a flat on Ash Grove on the 1st, how do I set up my water account?", "Moving Home Agent", "start",
          "I can do that now. What's the full address?"),
         ("14 Ash Grove, flat 2", "Moving Home Agent", "answer", "Done, your account starts on the 1st."),
         ("Does the flat have a meter or will I pay a fixed rate?", "Meter Installation Agent", "switch",
          "There's no meter yet; you'll pay the fixed rate unless you ask us to fit one, which is free."),
         ("yes fit one please", "Meter Installation Agent", "answer", "Booked for the 9th."),
         ("And can I pay the bills monthly instead of twice a year?", "Billing Agent", "switch", None)],
    ],
    "first": [
        ("Water is gushing out of the pavement outside my house.", "Leaks & Bursts Agent", "clear"),
        ("drain blocked, smells awful", "Sewerage Agent", "short"),
        ("I lost my job and can't afford this quarter's bill all at once.", "Payment Plans Agent", "indirect"),
        ("My bill says estimated, here's my actual reading: 0482.", "Meter Readings Agent", "close"),
        ("we're bulding an extension and need a new water supply", "New Connections Agent", "noisy"),
        ("I want to make a formal complaint about how my last call was handled.", "Complaints Agent", "clear"),
    ],
}

B["energy_supplier"] = {
    "agents": {
        "Tariffs Agent": "Explains tariffs and helps customers switch to a different energy tariff.",
        "Bills & Payments Agent": "Explains energy bills, direct debits and payment amounts.",
        "Meter Readings Agent": "Takes gas and electricity meter readings.",
        "Smart Meters Agent": "Books smart meter installations and fixes smart meters that stop sending readings.",
        "Prepayment Agent": "Helps prepayment customers with top-ups, keys, cards and emergency credit.",
        "Power Cuts Agent": "Reports power cuts and gives updates on restoring supply.",
        "Gas Safety Agent": "Handles gas leaks and the smell of gas; gives emergency safety advice.",
        "Solar Export Agent": "Handles payments for electricity exported from customers' solar panels.",
        "EV Charging Agent": "Helps with electric vehicle tariffs and home charger installations.",
        "Moving Home Agent": "Moves energy accounts when customers move house.",
        "Priority Services Agent": "Registers customers who need extra support, such as medical equipment users.",
        "Energy Saving Agent": "Gives advice and grants for insulation and lowering energy use.",
        "Complaints Agent": "Takes formal complaints about our service.",
    },
    "conversations": [
        [("I've just bought an electric car, is there a tariff for charging overnight?", "EV Charging Agent", "start",
          "Yes, our EV tariff has cheap rates from midnight to 5am. Do you have a home charger yet?"),
         ("not yet", "EV Charging Agent", "answer", "We can install one from £799, including the survey."),
         ("would that need a smart meter?", "EV Charging Agent", "follow", "Yes, the EV tariff needs a smart meter."),
         ("I don't have one, can you fit it first?", "Smart Meters Agent", "switch", "Sure, the earliest smart meter installation is next Wednesday."),
         ("Wednesday's fine. Also why did my direct debit go up last month?", "Bills & Payments Agent", "switch", None)],
        [("I can smell gas in the kitchen.", "Gas Safety Agent", "start",
          "Please open the windows, don't use switches or flames, and leave the house. An engineer is on the way."),
         ("ok we're outside now", "Gas Safety Agent", "answer", "Good. The engineer will be there within the hour."),
         ("Also my dad lives with us and uses an oxygen machine, can you note that on our account?", "Priority Services Agent", "switch",
          "I've added him to our priority services register."),
         ("does that mean you'd warn us before planned power cuts?", "Priority Services Agent", "follow", "Yes, we'll call you before any planned cut."),
         ("thanks for the help", "Priority Services Agent", "closing", None)],
    ],
    "first": [
        ("The power's out on our whole street.", "Power Cuts Agent", "clear"),
        ("emergency credit please", "Prepayment Agent", "short"),
        ("We had panels put on the roof in spring and haven't been paid anything for what we send back.", "Solar Export Agent", "indirect"),
        ("Is there a cheaper fixed deal than the one I'm on?", "Tariffs Agent", "close"),
        ("any grants for loft insulaton?", "Energy Saving Agent", "noisy"),
        ("We're moving out on Friday, here are the final readings.", "Moving Home Agent", "close"),
    ],
}

B["airport"] = {
    "agents": {
        "Parking Agent": "Books and changes airport car parking and answers parking questions.",
        "Drop-off & Pick-up Agent": "Explains drop-off zones, pick-up areas and their charges.",
        "Security Agent": "Answers questions about security screening, liquids and items allowed in hand luggage.",
        "Lost Property Agent": "Handles items lost in the terminal or at security.",
        "Special Assistance Agent": "Arranges help for passengers with reduced mobility or hidden disabilities.",
        "Lounges Agent": "Books airport lounges and fast track security.",
        "Shops & Dining Agent": "Answers questions about shops, restaurants and click-and-collect duty free.",
        "Flight Information Agent": "Gives arrival and departure times, gates and terminal information.",
        "Public Transport Agent": "Gives train, bus and taxi connections to and from the airport.",
        "Hotels Agent": "Books airport hotels.",
        "Currency Exchange Agent": "Orders travel money for collection at the airport.",
        "Noise Complaints Agent": "Takes complaints about aircraft noise from local residents.",
        "Jobs Agent": "Answers questions about jobs and security passes for airport staff.",
        "Feedback Agent": "Takes compliments and complaints about the terminal and staff.",
    },
    "conversations": [
        [("I'm flying out on the 12th, can I book parking for a week?", "Parking Agent", "start",
          "Yes. Would you like the short stay or the long stay car park with a shuttle?"),
         ("long stay", "Parking Agent", "answer", "Booked: 12th to 19th, long stay, £62."),
         ("Can I take my insulin pens through security?", "Security Agent", "switch",
          "Yes, medicines are allowed; keep them with a prescription or doctor's letter."),
         ("my mother is travelling with me and can't walk far, can someone help her to the gate?", "Special Assistance Agent", "switch",
          "Yes, we'll meet her at the assistance desk in departures."),
         ("And can we book the lounge for both of us?", "Lounges Agent", "short_switch", None)],
        [("I left my laptop at security this morning.", "Lost Property Agent", "start",
          "Sorry to hear that. What time did you go through, and what does it look like?"),
         ("about 7.30, a silver laptop in a black sleeve", "Lost Property Agent", "answer",
          "A silver laptop in a black sleeve was handed in. You can collect it from the info desk."),
         ("I've already flown, can someone collect it for me?", "Lost Property Agent", "follow",
          "Yes, with a signed note from you and their ID."),
         ("Is there a train from the city that gets to the airport before 6am?", "Public Transport Agent", "switch",
          "The first train arrives at 5:12am."),
         ("ok thanks", "Public Transport Agent", "closing", None)],
    ],
    "first": [
        ("Is flight AB204 from Rome still on time?", "Flight Information Agent", "clear"),
        ("pick up charge?", "Drop-off & Pick-up Agent", "short"),
        ("The planes have been flying over my house at 4am all week.", "Noise Complaints Agent", "indirect"),
        ("Where can I collect the duty free I ordered online?", "Shops & Dining Agent", "close"),
        ("need euros to colect at terminal 2", "Currency Exchange Agent", "noisy"),
        ("Can I book a room for the night before my early flight?", "Hotels Agent", "clear"),
    ],
}

B["online_marketplace"] = {
    "agents": {
        "Buyer Orders Agent": "Helps buyers with their orders: order status, tracking and changing orders.",
        "Buyer Refunds Agent": "Handles refunds and the money-back guarantee for buyers.",
        "Item Not Received Agent": "Opens cases for items that never arrived.",
        "Seller Accounts Agent": "Helps sellers set up and verify their seller accounts.",
        "Listings Agent": "Helps sellers create, edit and promote listings.",
        "Seller Payouts Agent": "Explains when and how sellers get paid, and payout holds.",
        "Fees Agent": "Explains selling fees and fee invoices.",
        "Shipping Labels Agent": "Helps sellers buy and print shipping labels.",
        "Trust & Safety Agent": "Handles scams, fake listings and suspicious messages.",
        "Account Security Agent": "Handles hacked accounts, password resets and two-step verification.",
        "Disputes Agent": "Steps in when a buyer and seller can't agree.",
        "Feedback Agent": "Handles feedback and reviews left by buyers and sellers.",
    },
    "conversations": [
        [("I sold a camera last week but the money still isn't in my bank.", "Seller Payouts Agent", "start",
          "New sellers' payouts are held for 7 days after delivery. When was it delivered?"),
         ("Tuesday", "Seller Payouts Agent", "answer", "Then it will be released next Tuesday."),
         ("Why was I charged £18 on that sale?", "Fees Agent", "switch", "That's the 12% final value fee on £150."),
         ("The buyer left me one star saying it was scratched, which isn't true. Can that be removed?", "Feedback Agent", "switch",
          "I'll review it; reviews that break our rules can be removed."),
         ("Also how do I promote my other listings?", "Listings Agent", "switch", None)],
        [("My parcel shows delivered but I never got it.", "Item Not Received Agent", "start",
          "I can open a case for you. What's the order number?"),
         ("ORD-77120", "Item Not Received Agent", "answer", "Case opened; the seller has 3 days to respond."),
         ("The seller is now asking me to pay him outside the site for a replacement, is that ok?", "Trust & Safety Agent", "switch",
          "No, please don't. Payments outside the site aren't protected. I'll look into the seller."),
         ("ok I won't", "Trust & Safety Agent", "closing", "Thank you. Your case stays open."),
         ("if he doesn't reply in 3 days, do I get my money back?", "Buyer Refunds Agent", "switch", None)],
    ],
    "first": [
        ("I want to start selling my handmade candles here.", "Seller Accounts Agent", "clear"),
        ("print postage label", "Shipping Labels Agent", "short"),
        ("Someone logged into my account from another country and changed my email.", "Account Security Agent", "indirect"),
        ("The seller and I disagree about whether the jacket was described properly.", "Disputes Agent", "close"),
        ("wheres my order its been 2 weeks", "Buyer Orders Agent", "noisy"),
        ("Can I change the size on an order I placed an hour ago?", "Buyer Orders Agent", "close"),
    ],
}

B["cinema_chain"] = {
    "agents": {
        "Tickets Agent": "Books and changes cinema tickets.",
        "Membership Agent": "Handles cinema memberships, free tickets and member pricing.",
        "Private Hire Agent": "Books private screenings and birthday parties.",
        "Accessibility Agent": "Answers questions about subtitled and audio described screenings, wheelchair spaces and carer tickets.",
        "Food & Drink Agent": "Answers questions about snacks, the bar and pre-ordering food.",
        "Gift Vouchers Agent": "Sells gift vouchers and checks voucher balances.",
        "Refunds Agent": "Refunds tickets for cancelled screenings and booking mistakes.",
        "Lost Property Agent": "Handles items left in our cinemas.",
        "Screen Times Agent": "Gives film times, ratings and running times.",
        "Feedback Agent": "Takes compliments and complaints about visits.",
    },
    "conversations": [
        [("Are there any subtitled screenings of the new Bond film this week?", "Accessibility Agent", "start",
          "Yes, Wednesday at 6pm and Sunday at 2pm, both with subtitles."),
         ("Wednesday please, and I bring a carer", "Accessibility Agent", "answer", "Your carer goes free; I've noted it for Wednesday."),
         ("how long is the film?", "Screen Times Agent", "switch", "It runs for 2 hours 43 minutes plus 20 minutes of trailers."),
         ("Can I book the tickets now?", "Tickets Agent", "switch", "Done: two tickets, Wednesday 6pm, screen 4."),
         ("and could we pre-order popcorn for the interval?", "Food & Drink Agent", "switch", None)],
        [("I'd like to book a screen for my son's 10th birthday party.", "Private Hire Agent", "start",
          "Lovely. How many children, and which date?"),
         ("12 kids, Saturday the 18th", "Private Hire Agent", "answer", "The 11am slot is free on the 18th, with party food included."),
         ("Can we bring our own cake?", "Private Hire Agent", "follow", "Yes, we'll store it and bring it out after the film."),
         ("Also I left a blue scarf in screen 2 last night, did anyone find it?", "Lost Property Agent", "switch",
          "A blue scarf was handed in last night, yes."),
         ("brilliant, back to the party, can parents stay and watch?", "Private Hire Agent", "return", None)],
    ],
    "first": [
        ("How much is a membership for two people?", "Membership Agent", "clear"),
        ("voucher balance", "Gift Vouchers Agent", "short"),
        ("The screening stopped halfway because the projector failed and we went home.", "Refunds Agent", "indirect"),
        ("What time is the last showing of the animated film on Friday?", "Screen Times Agent", "close"),
        ("the staff at the bar were really rude last nite", "Feedback Agent", "noisy"),
        ("Can I swap my tickets to the 8pm showing?", "Tickets Agent", "clear"),
    ],
}

B["bookshop_chain"] = {
    "agents": {
        "Book Orders Agent": "Orders books that are out of stock and tracks customer orders.",
        "Recommendations Agent": "Recommends books by genre, age or interests.",
        "Events Agent": "Handles author events, signings and book club evenings.",
        "School & Library Supply Agent": "Handles bulk orders for schools and libraries.",
        "Loyalty Card Agent": "Handles loyalty points and the loyalty card.",
        "E-books Agent": "Helps with e-books, the reading app and downloads.",
        "Returns Agent": "Handles returns and exchanges of books and gifts.",
        "Gift Wrapping Agent": "Arranges gift wrapping and gift messages.",
        "Second-hand Books Agent": "Buys and values second-hand and rare books.",
    },
    "conversations": [
        [("Do you have the new Ishiguro novel in stock?", "Book Orders Agent", "start",
          "It's sold out in store, but I can order it in; it would arrive in three days."),
         ("yes order it please", "Book Orders Agent", "answer", "Ordered. We'll text you when it's in."),
         ("Can you suggest something similar for my dad? He loved Remains of the Day.", "Recommendations Agent", "switch",
          "He might enjoy 'A Gentleman in Moscow' or 'Stoner'."),
         ("I'll take Stoner. Could you wrap it as a present?", "Gift Wrapping Agent", "switch", "Of course; would you like a gift message?"),
         ("yes, 'Happy 70th, Dad'", "Gift Wrapping Agent", "answer", None)],
        [("Is the crime writer's signing on Thursday still happening?", "Events Agent", "start",
          "Yes, Thursday at 7pm. Tickets are £5 and include £5 off the book."),
         ("I'll book two", "Events Agent", "answer", "Two tickets booked for Thursday."),
         ("Do I get loyalty points on the event tickets?", "Loyalty Card Agent", "switch", "Yes, 10 points per pound."),
         ("my card number ends 4410, how many points do I have?", "Loyalty Card Agent", "follow", "You have 1,240 points."),
         ("Also my book club wants to read the same book, can I order 8 copies?", "Book Orders Agent", "switch", None)],
    ],
    "first": [
        ("My grandad left a box of old first editions, would you buy them?", "Second-hand Books Agent", "indirect"),
        ("ebook won't download", "E-books Agent", "short"),
        ("Our primary school needs 30 copies of a reading scheme book for September.", "School & Library Supply Agent", "clear"),
        ("I got two copies of the same book as presents, can I swap one?", "Returns Agent", "close"),
        ("good books for a 9 yr old who likes dinosaurs?", "Recommendations Agent", "noisy"),
        ("When is the next book club evening?", "Events Agent", "clear"),
    ],
}

B["solar_installer"] = {
    "agents": {
        "Quotes Agent": "Gives quotes and surveys for new solar panel systems.",
        "Battery Storage Agent": "Advises on and quotes for home battery storage.",
        "Installation Scheduling Agent": "Books and moves installation dates.",
        "Planning & Permits Agent": "Advises on planning permission and listed building rules.",
        "Finance Agent": "Explains finance plans and monthly payments for systems.",
        "Monitoring App Agent": "Helps with the monitoring app and missing generation data.",
        "Repairs Agent": "Handles faults with panels, inverters and wiring after installation.",
        "Warranty Agent": "Handles warranty claims for panels and inverters.",
        "Grid Export Agent": "Helps register systems with the electricity network and export payments.",
    },
    "conversations": [
        [("How much would panels cost for a three-bed semi?", "Quotes Agent", "start",
          "Typically £6,000 to £8,000. Can we book a free survey to measure the roof?"),
         ("yes, any weekday", "Quotes Agent", "answer", "Booked for Tuesday at 10am."),
         ("Can I spread the cost monthly?", "Finance Agent", "switch", "Yes, over 5 or 10 years; I'll send the options after the survey."),
         ("Our house is in a conservation area, is that a problem?", "Planning & Permits Agent", "switch",
          "Panels facing the street may need planning permission there; we'll check during the survey."),
         ("ok, and would a battery be worth adding?", "Battery Storage Agent", "switch", None)],
        [("Since Monday the app shows zero generation even though it's sunny.", "Monitoring App Agent", "start",
          "Let's check the app first. Has your Wi-Fi password changed recently?"),
         ("no", "Monitoring App Agent", "answer", "Then the problem is probably the inverter, not the app."),
         ("The inverter screen is showing a red light and an error E07.", "Repairs Agent", "switch",
          "E07 is an isolation fault; an engineer needs to visit. I've booked Thursday."),
         ("Is the visit covered? The system is only two years old.", "Warranty Agent", "switch", "Yes, inverters are covered for 10 years."),
         ("good, thank you", "Warranty Agent", "closing", None)],
    ],
    "first": [
        ("Can I move my installation from the 3rd to the 10th?", "Installation Scheduling Agent", "clear"),
        ("export payments", "Grid Export Agent", "short"),
        ("We get loads of power at midday but nothing in the evening when we need it.", "Battery Storage Agent", "indirect"),
        ("My panels were fitted last year; one has a crack. Is that covered?", "Warranty Agent", "close"),
        ("inverter beeping all nite", "Repairs Agent", "noisy"),
        ("Do you offer 0% finance on a full system?", "Finance Agent", "clear"),
    ],
}

B["electronics_retailer"] = {
    "agents": {
        "Phones Agent": "Helps choose mobile phones and phone accessories.",
        "Laptops & PCs Agent": "Helps choose laptops, desktops and monitors.",
        "TV & Audio Agent": "Helps choose TVs, soundbars and speakers.",
        "Gaming Agent": "Helps with consoles, games and gaming accessories.",
        "Kitchen Appliances Agent": "Helps choose fridges, ovens, dishwashers and coffee machines.",
        "Delivery & Installation Agent": "Arranges delivery and installation of large appliances and TV wall mounting.",
        "Repairs Agent": "Books repairs for broken devices.",
        "Care Plans Agent": "Sells and explains extended warranties and care plans.",
        "Trade-in Agent": "Values old devices for trade-in.",
        "Order Tracking Agent": "Tracks online orders and changes delivery details.",
        "Returns Agent": "Handles returns and refunds within 30 days.",
        "Business Sales Agent": "Handles bulk orders for businesses.",
        "Price Match Agent": "Checks and applies price matching against other retailers.",
    },
    "conversations": [
        [("I'm looking for a 65 inch TV for gaming.", "TV & Audio Agent", "start",
          "For gaming, look for 120Hz and HDMI 2.1. What's your budget?"),
         ("around 1200", "TV & Audio Agent", "answer", "The LG C-series 65 is £1,199 and ideal for gaming."),
         ("Another shop has it for £1,099, can you match that?", "Price Match Agent", "switch",
          "Yes, send me the link and we'll match it."),
         ("Can you mount it on the wall when you deliver it?", "Delivery & Installation Agent", "switch",
          "Yes, wall mounting is £79 with delivery."),
         ("And will my PS5 work with it at 120?", "Gaming Agent", "switch", None)],
        [("My laptop screen cracked, can you fix it?", "Repairs Agent", "start",
          "We can. What model is it?"),
         ("ZenBook 14, bought here last year", "Repairs Agent", "answer", "Screen repairs for that model are £189, about 7 days."),
         ("Would my care plan cover it?", "Care Plans Agent", "switch", "Accidental damage is covered on the Gold plan; you have Silver."),
         ("ok so I pay for it", "Care Plans Agent", "follow", "Yes, but you could upgrade to Gold for future cover."),
         ("How much would you give me for it as a trade-in instead?", "Trade-in Agent", "switch", None)],
    ],
    "first": [
        ("Which fridge freezer has an ice maker and fits a 60 cm gap?", "Kitchen Appliances Agent", "clear"),
        ("where's my order", "Order Tracking Agent", "short"),
        ("We're kitting out a new office and need 25 laptops with an invoice.", "Business Sales Agent", "indirect"),
        ("I bought headphones last week and changed my mind, can I bring them back?", "Returns Agent", "close"),
        ("best phone under 400 with good camra", "Phones Agent", "noisy"),
        ("I need a monitor for video editing.", "Laptops & PCs Agent", "clear"),
    ],
}

B["car_dealership"] = {
    "agents": {
        "New Cars Agent": "Helps choose new cars and arranges test drives of new models.",
        "Used Cars Agent": "Helps with used cars in stock and test drives of used cars.",
        "Part Exchange Agent": "Values customers' current cars for part exchange.",
        "Car Finance Agent": "Explains finance deals, PCP and HP agreements.",
        "Servicing Agent": "Books services and MOTs.",
        "Repairs & Bodywork Agent": "Books repairs and bodywork after accidents.",
        "Parts & Accessories Agent": "Sells parts, roof bars, mats and accessories.",
        "Warranty Agent": "Handles manufacturer and extended warranty claims.",
        "Electric Vehicles Agent": "Advises on electric cars, range and charging.",
        "Fleet Sales Agent": "Handles company car and fleet orders.",
        "Courtesy Cars Agent": "Books courtesy cars while customers' cars are in the workshop.",
        "Delivery & Handover Agent": "Arranges collection and handover of new cars.",
    },
    "conversations": [
        [("I'd like to test drive the new electric SUV.", "New Cars Agent", "start",
          "Of course. Would Saturday morning suit you?"),
         ("Saturday 10am", "New Cars Agent", "answer", "Booked for Saturday at 10am."),
         ("What's the real range in winter?", "Electric Vehicles Agent", "switch",
          "Around 230 miles in cold weather, about 290 in summer."),
         ("And how much would you give me for my 2018 Golf?", "Part Exchange Agent", "switch",
          "With 60,000 miles, roughly £9,500, subject to inspection."),
         ("what would the monthly payment be then?", "Car Finance Agent", "switch", None)],
        [("My car is due its service next month, can I book it?", "Servicing Agent", "start",
          "Yes. What's the registration?"),
         ("KX19 ABC", "Servicing Agent", "answer", "It's due a major service; I have the 14th free."),
         ("Can I have a courtesy car that day?", "Courtesy Cars Agent", "switch", "Yes, one is reserved for you on the 14th."),
         ("Also the gearbox has been making a whine, is that covered under warranty?", "Warranty Agent", "switch",
          "Gearbox faults are covered until year 5; the technician will check it at the service."),
         ("thanks, see you on the 14th", "Warranty Agent", "closing", None)],
    ],
    "first": [
        ("Do you have any used estates under £15k?", "Used Cars Agent", "clear"),
        ("roof bars", "Parts & Accessories Agent", "short"),
        ("Someone reversed into my rear bumper in the car park.", "Repairs & Bodywork Agent", "indirect"),
        ("When can I pick up my new car? The order was confirmed in May.", "Delivery & Handover Agent", "close"),
        ("we need 12 company cars for our sales tem", "Fleet Sales Agent", "noisy"),
        ("Can I settle my PCP agreement early?", "Car Finance Agent", "clear"),
    ],
}

B["football_club"] = {
    "agents": {
        "Match Tickets Agent": "Sells and transfers tickets for home and away matches.",
        "Season Tickets Agent": "Handles season ticket renewals, seat moves and season ticket cards.",
        "Membership Agent": "Handles club membership and priority booking.",
        "Hospitality Agent": "Sells match-day hospitality packages and boxes.",
        "Stadium Tours Agent": "Books stadium tours and museum visits.",
        "Club Shop Agent": "Helps with shirts, kits and online shop orders.",
        "Kit Printing Agent": "Handles name and number printing on shirts.",
        "Disabled Supporters Agent": "Arranges accessible seating, carer tickets and parking for disabled supporters.",
        "Academy Agent": "Answers questions about the youth academy and trials.",
        "Community Trust Agent": "Handles community programmes, school visits and charity requests.",
        "Stadium Events Agent": "Books conferences, weddings and events at the stadium on non-match days.",
        "Away Travel Agent": "Books supporters' coaches to away matches.",
        "Lost Property Agent": "Handles items lost at the stadium.",
        "Supporter Liaison Agent": "Handles supporter concerns, safety and stadium behaviour reports.",
        "Media & Press Agent": "Handles press accreditation and media requests.",
    },
    "conversations": [
        [("Can I buy two tickets for the derby on the 20th?", "Match Tickets Agent", "start",
          "The derby is members-only priority this week. Are you a member?"),
         ("no", "Match Tickets Agent", "answer", "Then general sale opens on Monday at 10am."),
         ("How much is membership, and would it let me buy now?", "Membership Agent", "switch",
          "It's £35 a year and gives you access to priority sales straight away."),
         ("ok sign me up", "Membership Agent", "follow", "Done, your membership number is 778120."),
         ("Can I get my son's new shirt printed with his name before the game?", "Kit Printing Agent", "switch", None)],
        [("My dad uses a wheelchair, can we get seats together for Saturday?", "Disabled Supporters Agent", "start",
          "Yes, there are wheelchair bays with a carer seat in the east stand. Shall I book them?"),
         ("yes please", "Disabled Supporters Agent", "answer", "Booked, and the carer ticket is free."),
         ("is there accessible parking near the east stand?", "Disabled Supporters Agent", "aspect", "Yes, I've added a blue badge space."),
         ("We'd also love to do the stadium tour on Sunday morning.", "Stadium Tours Agent", "switch", "The 10am tour has space, it's fully accessible."),
         ("Last time some fans were throwing things near the bays, who can I tell?", "Supporter Liaison Agent", "switch", None)],
    ],
    "first": [
        ("My season ticket card isn't working at the turnstile.", "Season Tickets Agent", "clear"),
        ("coach to the away game", "Away Travel Agent", "short"),
        ("My nephew is 11 and his coach thinks he's good enough to try out for you.", "Academy Agent", "indirect"),
        ("We want a box for 10 people at the Boxing Day game.", "Hospitality Agent", "close"),
        ("left my jacket in the north stand on saturdy", "Lost Property Agent", "noisy"),
        ("Could the club send a player to visit our school?", "Community Trust Agent", "clear"),
    ],
}


def build():
    routing, first = [], []
    for company, b in B.items():
        agents = b["agents"]
        assert 9 <= len(agents) <= 15, (company, len(agents))
        for k, conv in enumerate(b["conversations"]):
            messages, user_turns, prev = [], [], None
            for user, expected, turn_type, assistant in conv:
                assert expected in agents, (company, expected)
                if prev and turn_type in STAY:
                    assert expected == prev, (company, user)
                if prev and turn_type in SWITCH:
                    assert expected != prev, (company, user)
                messages.append({"role": "user", "content": user})
                user_turns.append({"message_index": len(messages) - 1, "expected_agent": expected, "turn_type": turn_type})
                if assistant:
                    messages.append({"role": "assistant", "content": assistant})
                prev = expected
            routing.append({"id": f"{company}-{k + 1}", "company": company, "agents": agents, "messages": messages,
                            "user_turns": user_turns, "n_agents": len(agents)})
        for k, (message, target, kind) in enumerate(b["first"]):
            assert target in agents, (company, target)
            first.append({"id": f"{company}-f{k + 1}", "company": company, "agents": agents, "message": message,
                          "target_agent": target, "type": kind, "n_agents": len(agents)})
    users = [u for c in routing for u in [m["content"] for m in c["messages"] if m["role"] == "user"]] + [f["message"] for f in first]
    long = [u for u in users if len(u.split()) > 3]              # short replies ("yes please", "no") naturally repeat
    assert len(long) == len(set(long)), "every user message longer than 3 words is unique"
    OUT.mkdir(exist_ok=True)
    json.dump(routing, open(OUT / "routing.json", "w"), indent=1)
    json.dump({"messages": first}, open(OUT / "first_turn.json", "w"), indent=1)
    n_turns = sum(len(c["user_turns"]) for c in routing)
    print(f"{len(B)} businesses ({min(len(b['agents']) for b in B.values())}-{max(len(b['agents']) for b in B.values())} agents) | "
          f"{len(routing)} conversations, {n_turns} turns | {len(first)} first messages")


if __name__ == "__main__":
    build()
