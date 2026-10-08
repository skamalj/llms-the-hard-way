"""E12: grounded choice TEST questions (phase 8), for our model and the Strands decider side by side. Never used for training.

Run from the repo root: python data/modernbert_router/build_choice_test_data.py

Every item is (state, question, options, answer) and the answer can be read from the STATE alone: no world knowledge,
as with the decider ("pick between sets of options and rate things on a scale" from the given text). Three types, the
decider's three primitives:
  noul    yes / no question                          options ["yes", "no"]
  choice  one of N unordered options
  score   one position on an ORDERED scale (options listed from low to high)
Categories say what the question needs: tone, intent, urgency, routing, detail (pick the stated detail), compare
(compare things stated in the text), fact (is something stated / true in the text).
Pairs: the same state asked two different questions with different answers (pair id in "pair"), to check that a model
reads the question and not only the text.
"""
import json
from collections import Counter
from pathlib import Path

OUT = Path(__file__).parent / "choice_test"
YN = ["yes", "no"]

# (id, category, state, question, answer)
NOUL = [
    ("n01", "urgency", "Help! My payouts have been failing for 3 days!", "Does this convey urgency?", "yes"),
    ("n02", "urgency", "No rush at all, but when you get a moment could you update my postal address?", "Does this convey urgency?", "no"),
    ("n03", "fact", "Hi, my order 88123 arrived without the charger.", "Does the customer give an order number?", "yes"),
    ("n04", "fact", "Hi, my order arrived without the charger, can you help?", "Does the customer give an order number?", "no"),
    ("n05", "intent", "I'd like my money back for the jacket, it fell apart after one wash.", "Is the customer asking for a refund?", "yes"),
    ("n06", "intent", "The jacket fell apart after one wash. Can you send me the same one in a new piece instead?", "Is the customer asking for a refund?", "no"),
    ("n07", "tone", "Absolutely love the new update, the app is so much faster now!", "Is the writer happy?", "yes"),
    ("n08", "tone", "Since the update the app crashes every time I open it. Useless.", "Is the writer happy?", "no"),
    ("n09", "fact", "I've already restarted the router twice and it's still not working.", "Has the user already restarted the router?", "yes"),
    ("n10", "fact", "The internet is down. What should I try first?", "Has the user already restarted the router?", "no"),
    ("n11", "intent", "Please cancel my membership from next month.", "Does the customer want to cancel?", "yes"),
    ("n12", "intent", "I was thinking of cancelling, but the new classes look great, so I'll stay. Can I book Tuesday yoga?", "Does the customer want to cancel?", "no"),
    ("n13", "fact", "Meeting moved to Thursday 3pm, same room.", "Did the meeting room change?", "no"),
    ("n14", "fact", "Meeting stays on Thursday 3pm but we're now in room 4B instead of 2A.", "Did the meeting room change?", "yes"),
    ("n15", "urgency", "There's water pouring through the ceiling light in the kitchen right now.", "Is this an emergency?", "yes"),
    ("n16", "urgency", "The kitchen tap drips a little at night. Could someone look at it next month?", "Is this an emergency?", "no"),
    ("n17", "fact", "Dear team, attached is my invoice for March. Kind regards, Lena", "Does the message mention an attachment?", "yes"),
    ("n18", "fact", "Dear team, could you tell me when my March invoice will be paid? Kind regards, Lena", "Does the message mention an attachment?", "no"),
    ("n19", "tone", "I've called four times and nobody has called me back. This is ridiculous.", "Is the customer frustrated?", "yes"),
    ("n20", "tone", "Thanks for calling me back so quickly yesterday, all sorted now.", "Is the customer frustrated?", "no"),
    ("n21", "intent", "Can I change my delivery to Saturday instead of Friday?", "Is the customer asking to change the delivery day?", "yes"),
    ("n22", "intent", "Can I change the delivery address to my office? Friday is still fine.", "Is the customer asking to change the delivery day?", "no"),
    ("n23", "fact", "The parcel was left with my neighbour at number 12.", "Was the parcel delivered?", "yes"),
    ("n24", "fact", "The tracking says delivered but there's nothing here and the neighbours don't have it.", "Did the customer receive the parcel?", "no"),
    ("n25", "fact", "I paid by card at the counter but forgot to take the receipt.", "Did the customer pay?", "yes"),
    ("n26", "fact", "I wanted to pay by card but the machine was broken, so I left without paying.", "Did the customer pay?", "no"),
    ("n27", "intent", "Could you send me a quote for painting three bedrooms?", "Is the customer asking for a price?", "yes"),
    ("n28", "intent", "The painters did a great job on the bedrooms, thank you.", "Is the customer asking for a price?", "no"),
    ("n29", "fact", "Our flight lands at 22:40, so we'll check in late, around midnight.", "Will the guests arrive after 11pm?", "yes"),
    ("n30", "fact", "Our flight lands at 14:10, so we'll be at the hotel around four.", "Will the guests arrive after 11pm?", "no"),
    ("n31", "fact", "I'm allergic to peanuts, please make sure the cake has none.", "Does the customer mention an allergy?", "yes"),
    ("n32", "fact", "Please write 'Happy 40th Sam' on the cake, chocolate sponge.", "Does the customer mention an allergy?", "no"),
    ("n33", "urgency", "My flight is in two hours and the booking says cancelled!", "Does the customer need an answer quickly?", "yes"),
    ("n34", "urgency", "For my trip next spring, is it possible to add a bag later?", "Does the customer need an answer quickly?", "no"),
    ("n35", "fact", "The washing machine is 3 years old and the warranty was 2 years.", "Is the washing machine still under warranty?", "no"),
    ("n36", "fact", "The washing machine is 8 months old and came with a 2-year warranty.", "Is the washing machine still under warranty?", "yes"),
    ("n37", "intent", "I'm writing to complain about the rude driver on the number 9 bus this morning.", "Is this a complaint?", "yes"),
    ("n38", "intent", "What time does the first number 9 bus leave on Sundays?", "Is this a complaint?", "no"),
    ("n39", "fact", "Both tickets are for the 7:30pm show on Friday.", "Are the tickets for an evening show?", "yes"),
    ("n40", "fact", "Both tickets are for the 2pm matinee on Saturday.", "Are the tickets for an evening show?", "no"),
    ("n41", "tone", "Honestly the best meal we've had all year, the staff were lovely.", "Is the review positive?", "yes"),
    ("n42", "tone", "Cold food, an hour's wait and a waiter who ignored us. Never again.", "Is the review positive?", "no"),
    ("n43", "fact", "I'm a student at Leeds and I have my student card with me.", "Does the customer say they are a student?", "yes"),
    ("n44", "fact", "I'm a teacher at a school in Leeds.", "Does the customer say they are a student?", "no"),
    ("n45", "intent", "Can someone call me back on 07700 900123 after 5pm?", "Does the customer want a call back?", "yes"),
    ("n46", "intent", "Please don't call me, email is better for me.", "Does the customer want a call back?", "no"),
    ("n47", "fact", "We ordered 4 chairs but only 3 were in the delivery.", "Is something missing from the delivery?", "yes"),
    ("n48", "fact", "All 4 chairs arrived today, thanks, but one has a scratch.", "Is something missing from the delivery?", "no"),
    ("n49", "fact", "The 4 chairs arrived today, but one has a scratch on the leg.", "Is any item damaged?", "yes"),
    ("n50", "fact", "We ordered 4 chairs but only 3 were in the delivery; those are perfect.", "Is any item damaged?", "no"),
    ("n51", "compare", "The blue sofa is £899 and the grey one is £749.", "Is the grey sofa cheaper than the blue one?", "yes"),
    ("n52", "compare", "The blue sofa is £699 and the grey one is £749.", "Is the grey sofa cheaper than the blue one?", "no"),
    ("n53", "fact", "Please leave the parcel in the green bin by the side door if I'm out.", "Did the customer give a safe place for the parcel?", "yes"),
    ("n55", "detail", "Can we move the call from Tuesday to Thursday? Friday doesn't work for me.", "Does Friday work for the writer?", "no"),
    ("n56", "compare", "Quote 1: £1,200, done in 2 weeks. Quote 2: £950, done in 6 weeks. We need it finished before the party in 3 weeks.", "Is Quote 2 cheaper than Quote 1?", "yes"),
    ("n57", "compare", "The bill this month is £312; it's usually about £90.", "Is the bill higher than usual?", "yes"),
    ("n58", "compare", "Two adults and three children, the youngest is 2.", "Are there more children than adults?", "yes"),
    ("n54", "fact", "Please don't leave the parcel outside; take it back to the depot if I'm out.", "Did the customer give a safe place for the parcel?", "no"),
]

# (id, category, state, question, options, answer)
CHOICE = [
    ("c01", "routing", "Help! My payouts have been failing for 3 days!", "Which team should handle this?", ["billing", "sales", "retail"], "billing"),
    ("c02", "routing", "I'd like a demo of your software for my team of 40.", "Which team should handle this?", ["billing", "sales", "support"], "sales"),
    ("c03", "routing", "The app logs me out every time I switch screens.", "Which team should handle this?", ["billing", "sales", "support"], "support"),
    ("c04", "intent", "The shoes are too small, can I swap them for a size 9?", "What does the customer want?", ["refund", "exchange", "repair", "information"], "exchange"),
    ("c05", "intent", "The kettle stopped working after a week. Can you fix it?", "What does the customer want?", ["refund", "exchange", "repair", "information"], "repair"),
    ("c06", "intent", "I'd just like my money back for the lamp please.", "What does the customer want?", ["refund", "exchange", "repair", "information"], "refund"),
    ("c07", "intent", "Does the lamp work with a dimmer switch?", "What does the customer want?", ["refund", "exchange", "repair", "information"], "information"),
    ("c08", "detail", "Can we move the call from Tuesday to Thursday? Friday doesn't work for me.", "Which day does the writer want?", ["Tuesday", "Thursday", "Friday"], "Thursday"),
    ("c09", "detail", "I can't do Thursday any more; let's keep Tuesday, or Friday at a push.", "Which day does the writer prefer?", ["Tuesday", "Thursday", "Friday"], "Tuesday"),
    ("c10", "detail", "I'll pay by bank transfer this time instead of card.", "How will the customer pay?", ["card", "bank transfer", "cash"], "bank transfer"),
    ("c11", "detail", "I usually pay by card, but today I'll pay cash at the door.", "How will the customer pay?", ["card", "bank transfer", "cash"], "cash"),
    ("c12", "tone", "Thanks so much, the team went above and beyond!", "What is the tone of the message?", ["angry", "neutral", "grateful"], "grateful"),
    ("c13", "tone", "Please confirm receipt of the documents.", "What is the tone of the message?", ["angry", "neutral", "grateful"], "neutral"),
    ("c14", "tone", "Third time I'm writing. Fix this NOW or I'm leaving.", "What is the tone of the message?", ["angry", "neutral", "grateful"], "angry"),
    ("c15", "routing", "My dog has been limping since yesterday.", "Which department should take this?", ["grooming", "veterinary", "boarding"], "veterinary"),
    ("c16", "routing", "Can Max stay with you for the week we're in Spain?", "Which department should take this?", ["grooming", "veterinary", "boarding"], "boarding"),
    ("c17", "routing", "Max needs a wash and his nails clipped.", "Which department should take this?", ["grooming", "veterinary", "boarding"], "grooming"),
    ("c18", "detail", "Room 214 has no hot water; room 215 is fine.", "Which room has the problem?", ["room 214", "room 215", "room 216"], "room 214"),
    ("c19", "compare", "Plan A costs £20 a month for 10GB; Plan B costs £25 for unlimited data. I use about 30GB.", "Which plan fits this user?", ["Plan A", "Plan B"], "Plan B"),
    ("c20", "compare", "Plan A costs £20 a month for 10GB; Plan B costs £25 for unlimited data. I use about 3GB.", "Which plan is cheaper for this user?", ["Plan A", "Plan B"], "Plan A"),
    ("c21", "compare", "The 8:05 train arrives at 9:40 and the 8:20 train arrives at 9:35.", "Which train arrives first?", ["the 8:05", "the 8:20"], "the 8:20"),
    ("c22", "compare", "Store A is 2 miles away and closes at 6; Store B is 5 miles away and closes at 9. It's 7pm now.", "Which store can the customer still visit today?", ["Store A", "Store B"], "Store B"),
    ("c23", "detail", "Please send it to my work address, not home: 4 King Street.", "Where should it be sent?", ["home", "work", "collection point"], "work"),
    ("c24", "detail", "I'll pick it up myself from the collection point at the station.", "Where should it be sent?", ["home", "work", "collection point"], "collection point"),
    ("c25", "routing", "I was charged twice for my last order.", "Which agent should handle this?", ["Orders Agent", "Payments Agent", "Returns Agent"], "Payments Agent"),
    ("c26", "routing", "Where is my order? It's three days late.", "Which agent should handle this?", ["Orders Agent", "Payments Agent", "Returns Agent"], "Orders Agent"),
    ("c27", "routing", "The dress doesn't fit, how do I send it back?", "Which agent should handle this?", ["Orders Agent", "Payments Agent", "Returns Agent"], "Returns Agent"),
    ("c28", "intent", "Could you tell me what time you open on bank holidays?", "What kind of message is this?", ["question", "complaint", "compliment", "request for action"], "question"),
    ("c29", "intent", "Your cashier was wonderful with my elderly mum today.", "What kind of message is this?", ["question", "complaint", "compliment", "request for action"], "compliment"),
    ("c30", "intent", "The floor was filthy and the bins were overflowing.", "What kind of message is this?", ["question", "complaint", "compliment", "request for action"], "complaint"),
    ("c31", "intent", "Please close my account and delete my data.", "What kind of message is this?", ["question", "complaint", "compliment", "request for action"], "request for action"),
    ("c32", "detail", "I'd like the large pizza, but with the thin base, not the stuffed crust.", "Which base did the customer choose?", ["thin", "classic", "stuffed crust"], "thin"),
    ("c33", "detail", "Two adults and three children, the youngest is 2.", "How many people are in the group?", ["three", "four", "five"], "five"),
    ("c34", "detail", "Flight BA117 is delayed; my connecting flight BA92 leaves at 18:00.", "Which flight is delayed?", ["BA117", "BA92"], "BA117"),
    ("c35", "routing", "My boiler is making a banging noise and there's no hot water.", "Who should be sent?", ["plumber", "electrician", "roofer"], "plumber"),
    ("c36", "routing", "Half the sockets in the house stopped working after the storm.", "Who should be sent?", ["plumber", "electrician", "roofer"], "electrician"),
    ("c37", "routing", "Tiles blew off in the storm and now the attic is wet.", "Who should be sent?", ["plumber", "electrician", "roofer"], "roofer"),
    ("c38", "detail", "Blue is sold out, so I'll take the green one, not the red.", "Which colour will the customer take?", ["blue", "green", "red"], "green"),
    ("c39", "topic", "The match went to penalties and the keeper saved two.", "What is the text about?", ["sport", "politics", "cooking", "weather"], "sport"),
    ("c40", "topic", "Simmer the onions for ten minutes before adding the stock.", "What is the text about?", ["sport", "politics", "cooking", "weather"], "cooking"),
    ("c41", "topic", "Heavy rain and strong winds are expected along the coast tonight.", "What is the text about?", ["sport", "politics", "cooking", "weather"], "weather"),
    ("c42", "topic", "The council voted to approve the new budget by 32 votes to 19.", "What is the text about?", ["sport", "politics", "cooking", "weather"], "politics"),
    ("c43", "compare", "Quote 1: £1,200, done in 2 weeks. Quote 2: £950, done in 6 weeks. We need it finished before the party in 3 weeks.", "Which quote meets the deadline?", ["Quote 1", "Quote 2"], "Quote 1"),
    ("c44", "detail", "My son Tom is 7 and my daughter Ava is 10; it's Ava's birthday party.", "Whose party is it?", ["Tom", "Ava"], "Ava"),
    ("c45", "language", "Bonjour, je voudrais réserver une table pour deux ce soir.", "Which language is the message written in?", ["English", "French", "Spanish", "German"], "French"),
    ("c46", "language", "Hola, quiero cambiar la fecha de mi reserva.", "Which language is the message written in?", ["English", "French", "Spanish", "German"], "Spanish"),
    ("c47", "intent", "I'm locked out of my account after too many wrong passwords.", "What is the problem?", ["login", "payment", "delivery"], "login"),
    ("c48", "intent", "My card keeps getting declined at checkout.", "What is the problem?", ["login", "payment", "delivery"], "payment"),
    ("c49", "detail", "Table for six at 8pm please; if 8 is full, 7:30 is fine but not 9.", "What time did the customer ask for first?", ["7:30pm", "8pm", "9pm"], "8pm"),
    ("c50", "routing", "Help! My payouts have been failing for 3 days!", "Which topic is this about?", ["payments", "account access", "shipping"], "payments"),
    ("c51", "compare", "Ana scored 72, Ben scored 85 and Cara scored 79.", "Who scored highest?", ["Ana", "Ben", "Cara"], "Ben"),
    ("c52", "compare", "Ana scored 72, Ben scored 85 and Cara scored 79.", "Who scored lowest?", ["Ana", "Ben", "Cara"], "Ana"),
    ("c53", "detail", "Starter: soup. Main: the fish, not the steak. Dessert: none, thanks.", "Which main did the customer order?", ["soup", "fish", "steak"], "fish"),
    ("c55", "detail", "Hi, my order 88123 arrived without the charger.", "What is missing?", ["charger", "cable", "manual"], "charger"),
    ("c56", "detail", "Flight BA117 is delayed; my connecting flight BA92 leaves at 18:00.", "Which flight leaves at 18:00?", ["BA117", "BA92"], "BA92"),
    ("c57", "detail", "Our flight lands at 22:40, so we'll check in late, around midnight.", "When will the guests check in?", ["around four", "around midnight"], "around midnight"),
    ("c58", "detail", "Starter: soup. Main: the fish, not the steak. Dessert: none, thanks.", "What did the customer choose for dessert?", ["soup", "fish", "none"], "none"),
    ("c59", "detail", "Our whole office has been offline since 8am and we can't take orders.", "What can the office not do?", ["take orders", "run payroll", "print"], "take orders"),
    ("c54", "routing", "I want to upgrade to the premium plan.", "Which team should handle this?", ["billing", "sales", "support"], "sales"),
]

# (id, category, state, question, options low -> high, answer)
FRUST = ["calm", "frustrated", "furious"]
URG = ["low", "medium", "high"]
SAT = ["very unhappy", "unhappy", "neutral", "happy", "very happy"]
SCORE = [
    ("s01", "tone", "Help! My payouts have been failing for 3 days!", "How frustrated is the writer?", FRUST, "frustrated"),
    ("s02", "tone", "Just checking when the payout will land, no problem either way.", "How frustrated is the writer?", FRUST, "calm"),
    ("s03", "tone", "SIX weeks and still no payout. I am DONE with you people. Lawyers next.", "How frustrated is the writer?", FRUST, "furious"),
    ("s04", "urgency", "Our whole office has been offline since 8am and we can't take orders.", "How urgent is this?", URG, "high"),
    ("s05", "urgency", "One of the meeting room screens flickers sometimes; please check it this week.", "How urgent is this?", URG, "medium"),
    ("s06", "urgency", "Whenever you have time, could you add a new font to the template?", "How urgent is this?", URG, "low"),
    ("s07", "tone", "Food was cold, the waiter was rude and we waited an hour. Worst night out ever.", "How satisfied is the customer?", SAT, "very unhappy"),
    ("s08", "tone", "The food was a bit bland and slow to arrive.", "How satisfied is the customer?", SAT, "unhappy"),
    ("s09", "tone", "Food was fine, service was fine, nothing special.", "How satisfied is the customer?", SAT, "neutral"),
    ("s10", "tone", "Nice food and friendly staff, we'd come back.", "How satisfied is the customer?", SAT, "happy"),
    ("s11", "tone", "Absolutely perfect evening, the best meal we've ever had. Thank you all!", "How satisfied is the customer?", SAT, "very happy"),
    ("s12", "detail", "The sofa is 1.4 metres wide.", "How wide is the sofa?", ["under 1 m", "1 to 2 m", "over 2 m"], "1 to 2 m"),
    ("s13", "detail", "The van is 2.6 metres wide.", "How wide is the van?", ["under 1 m", "1 to 2 m", "over 2 m"], "over 2 m"),
    ("s14", "detail", "The bedside table is 45 cm wide.", "How wide is the table?", ["under 1 m", "1 to 2 m", "over 2 m"], "under 1 m"),
    ("s15", "detail", "We expect around 140 guests.", "How large is the event?", ["under 50", "50 to 100", "over 100"], "over 100"),
    ("s16", "detail", "It's a small dinner for 12 people.", "How large is the event?", ["under 50", "50 to 100", "over 100"], "under 50"),
    ("s17", "detail", "We've invited 75 people to the reception.", "How large is the event?", ["under 50", "50 to 100", "over 100"], "50 to 100"),
    ("s18", "detail", "The repair will take about 3 days.", "How long will the repair take?", ["same day", "within a week", "more than a week"], "within a week"),
    ("s19", "detail", "We can fix it while you wait, about an hour.", "How long will the repair take?", ["same day", "within a week", "more than a week"], "same day"),
    ("s20", "detail", "The part has to come from Japan, so it'll be about a month.", "How long will the repair take?", ["same day", "within a week", "more than a week"], "more than a week"),
    ("s21", "tone", "Noted. I'll check it tomorrow.", "How polite is the message?", ["rude", "neutral", "very polite"], "neutral"),
    ("s22", "tone", "Thank you so much for your kind help, I really appreciate your patience.", "How polite is the message?", ["rude", "neutral", "very polite"], "very polite"),
    ("s23", "tone", "Just do your job and stop wasting my time.", "How polite is the message?", ["rude", "neutral", "very polite"], "rude"),
    ("s24", "fact", "I've tried everything in the guide, restarted twice and reinstalled the app.", "How much has the user already tried?", ["nothing", "a little", "a lot"], "a lot"),
    ("s25", "fact", "It doesn't work. What do I do?", "How much has the user already tried?", ["nothing", "a little", "a lot"], "nothing"),
    ("s26", "fact", "I restarted it once but it's still slow.", "How much has the user already tried?", ["nothing", "a little", "a lot"], "a little"),
    ("s27", "detail", "The bill this month is £312; it's usually about £90.", "How does this bill compare with usual?", ["lower", "about the same", "much higher"], "much higher"),
    ("s28", "detail", "The bill this month is £88; it's usually about £90.", "How does this bill compare with usual?", ["lower", "about the same", "much higher"], "about the same"),
    ("s29", "detail", "The bill this month is £40; it's usually about £90.", "How does this bill compare with usual?", ["lower", "about the same", "much higher"], "lower"),
    ("s30", "fact", "I'm fairly sure it was Tuesday, but it might have been Wednesday.", "How certain is the writer?", ["unsure", "fairly sure", "certain"], "fairly sure"),
    ("s31", "fact", "It was definitely Tuesday, I have the receipt.", "How certain is the writer?", ["unsure", "fairly sure", "certain"], "certain"),
    ("s32", "fact", "I have no idea which day it was, sorry.", "How certain is the writer?", ["unsure", "fairly sure", "certain"], "unsure"),
    ("s33", "urgency", "Smoke is coming out of the fuse box!", "How urgent is this?", URG, "high"),
    ("s34", "urgency", "The hallway bulb has gone; can you replace it on your next visit?", "How urgent is this?", URG, "low"),
    ("s35", "urgency", "The fridge is getting warm; it needs looking at in the next day or two.", "How urgent is this?", URG, "medium"),
    ("s36", "tone", "The delivery was a day late again, which is annoying because I took the day off for it.", "How frustrated is the writer?", FRUST, "frustrated"),
    ("s37", "tone", "Delivery was a day late, no worries at all.", "How frustrated is the writer?", FRUST, "calm"),
    ("s38", "tone", "A WEEK late and nobody answers the phone. Absolutely unacceptable. Cancel everything.", "How frustrated is the writer?", FRUST, "furious"),
    ("s39", "detail", "The flat is on the 14th floor.", "How high up is the flat?", ["ground floor", "floors 1 to 5", "above floor 5"], "above floor 5"),
    ("s40", "detail", "The flat is on the ground floor with a small garden.", "How high up is the flat?", ["ground floor", "floors 1 to 5", "above floor 5"], "ground floor"),
    ("s41", "detail", "The flat is on the third floor; there's no lift.", "How high up is the flat?", ["ground floor", "floors 1 to 5", "above floor 5"], "floors 1 to 5"),
    ("s42", "tone", "The hotel was okay. Clean room, but the breakfast was poor.", "How satisfied is the guest?", SAT, "neutral"),
    ("s43", "tone", "Lovely stay, comfy bed and a great breakfast.", "How satisfied is the guest?", SAT, "happy"),
    ("s44", "tone", "Dirty room, broken shower and no apology. Avoid.", "How satisfied is the guest?", SAT, "very unhappy"),
    ("s45", "detail", "We need it by tomorrow morning at the latest.", "How soon is it needed?", ["within a day", "within a week", "within a month"], "within a day"),
    ("s46", "detail", "Any time before the end of next week is fine.", "How soon is it needed?", ["within a day", "within a week", "within a month"], "within a week"),
    ("s47", "detail", "No hurry, as long as it's here before the wedding in four weeks.", "How soon is it needed?", ["within a day", "within a week", "within a month"], "within a month"),
    ("s48", "fact", "The printer jams now and then, maybe once a week.", "How often does the problem happen?", ["rarely", "sometimes", "constantly"], "sometimes"),
    ("s49", "fact", "The printer jams on every single page.", "How often does the problem happen?", ["rarely", "sometimes", "constantly"], "constantly"),
    ("s50", "fact", "The printer jammed once last year, otherwise it's been fine.", "How often does the problem happen?", ["rarely", "sometimes", "constantly"], "rarely"),
    ("s51", "urgency", "Help! My payouts have been failing for 3 days!", "How urgent is this?", URG, "high"),
    ("s52", "tone", "The new app is slightly better than the old one, I suppose.", "How satisfied is the customer?", SAT, "neutral"),
    ("s53", "tone", "The new app is a huge improvement, I love it!", "How satisfied is the customer?", SAT, "very happy"),
]

# Pairs (question sensitivity): every state asked more than one question, each with its own answer. Built automatically.


def items():
    out = []
    for i, cat, state, q, a in NOUL:
        out.append({"id": i, "type": "noul", "category": cat, "state": state, "question": q, "options": YN, "answer": a})
    for i, cat, state, q, opts, a in CHOICE:
        out.append({"id": i, "type": "choice", "category": cat, "state": state, "question": q, "options": opts, "answer": a})
    for i, cat, state, q, opts, a in SCORE:
        out.append({"id": i, "type": "score", "category": cat, "state": state, "question": q, "options": opts, "answer": a,
                    "answer_index": opts.index(a)})
    groups = {}
    for x in out:
        groups.setdefault(x["state"], []).append(x)
    pairs = {}
    for state, xs in groups.items():
        if len(xs) > 1:
            pid = f"p{len(pairs) + 1:02d}"
            pairs[pid] = [x["id"] for x in xs]
            for x in xs:
                x["pair"] = pid
    return out, pairs


data, PAIRS = items()
ids = Counter(x["id"] for x in data)
assert all(n == 1 for n in ids.values())
for x in data:
    assert x["answer"] in x["options"], x["id"]
    assert len(set(x["options"])) == len(x["options"]), x["id"]
types = Counter(x["type"] for x in data)
assert all(types[t] >= 50 for t in ["noul", "choice", "score"]), types
yes = sum(x["answer"] == "yes" for x in data if x["type"] == "noul")

OUT.mkdir(exist_ok=True)
json.dump({"pairs": PAIRS, "items": data}, open(OUT / "items.json", "w"), indent=2, ensure_ascii=False)
print(f"E12: {len(data)} items | " + " | ".join(f"{t} {n}" for t, n in types.items()) + f" | yes/no balance {yes} yes / {types['noul'] - yes} no")
print("categories:", dict(Counter(x["category"] for x in data).most_common()))
print(f"question-sensitivity groups (same state, different questions): {len(PAIRS)}, {sum(len(v) for v in PAIRS.values())} items")
print("wrote", OUT / "items.json")
