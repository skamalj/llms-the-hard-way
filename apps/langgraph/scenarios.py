"""Test scenarios for the LangGraph app. Every user turn is labelled with the agent that should handle it.

Written for this app (Northwind Outdoor Gear is new to Signpost). Note: the same author (Claude) also wrote Signpost's
training data, so a shared writing style may favour Signpost a little; the independent test set in the repo is the
outside check.
"""
O, R, P, W, B = ("Orders & Delivery Agent", "Returns & Refunds Agent", "Product Advice Agent",
                 "Repairs & Warranty Agent", "Billing & Membership Agent")

# A. First messages: a new thread each, no history, no current agent.  (message, expected agent, kind)
FIRST_MESSAGES = [
    ("Where's my order? It was meant to arrive on Tuesday.", O, "clear"),
    ("parcel says delivered but nothing here", O, "short"),
    ("Can I change the delivery address on order NW-4471?", O, "clear"),
    ("tracking number pls", O, "short"),
    ("The boots don't fit, can I send them back?", R, "clear"),
    ("I returned a tent two weeks ago and still haven't had my money back.", R, "close"),
    ("how do I get a return label", R, "short"),
    ("I'd like to swap this jacket for a medium.", R, "clear"),
    ("Which sleeping bag is warm enough for minus 5?", P, "clear"),
    ("is the Ridgeline 2 tent any good on windy coasts", P, "indirect"),
    ("I'm usually a 9.5 in trainers, what size walking boots should I order?", P, "indirect"),
    ("Is this jacket actually waterproof or just water resistant?", P, "clear"),
    ("The zip on my tent broke on the second trip.", W, "indirect"),
    ("My stove won't light any more and it's not even a year old.", W, "close"),
    ("Can you fix a torn rucksack strap?", W, "clear"),
    ("warranty claim for a cracked trekking pole", W, "short"),
    ("I was charged twice for my last order.", B, "close"),
    ("How many loyalty points do I have?", B, "clear"),
    ("Can I pay with a gift card and my credit card together?", B, "clear"),
    ("I want to cancel my Northwind membership.", B, "clear"),
]

# B. Conversations: one thread each, routed live (Signpost sees the real history and the current agent).
#    (user message, expected agent, turn type)
CONVERSATIONS = {
    "order-then-product-then-billing": [
        ("Hi, my order NW-5521 hasn't arrived yet.", O, "start"),
        ("it was due on Monday", O, "answer"),
        ("ok thanks", O, "closing"),
        ("Also, the tent in that order, does it come with a footprint?", P, "switch"),
        ("and is the footprint the same size as the tent floor?", P, "follow"),
        ("Actually I've just noticed I was charged twice for this order.", B, "switch"),
        ("yes, two payments of £189", B, "answer"),
    ],
    "repair-then-return-then-advice": [
        ("My hiking boots are leaking after three walks.", W, "start"),
        ("bought them in March", W, "answer"),
        ("And can I just return them instead of getting them repaired?", R, "switch"),
        ("ok, send me the label", R, "follow"),
        ("while you're at it, which boots would you recommend instead for wet moors?", P, "switch"),
    ],
    "advice-points-and-back": [
        ("What's the warmest sleeping bag under 1.5 kg?", P, "start"),
        ("something for the Alps in October", P, "answer"),
        ("Do I get loyalty points if I buy it?", B, "switch"),
        ("nice. back to the bag, does it pack small enough for a 40 litre rucksack?", P, "return"),
        ("great, thanks", P, "closing"),
    ],
    "short-replies": [
        ("I need to send back a jacket, it's the wrong colour.", R, "start"),
        ("the green one", R, "answer"),
        ("yes", R, "answer"),
        ("refund please", R, "answer"),
        ("and my points?", B, "short_switch"),
    ],
    "repair-stays-then-delivery": [
        ("My stove stopped working on a trip.", W, "start"),
        ("It's the Pocket Flame 2, about 8 months old", W, "answer"),
        ("Also the igniter button feels loose", W, "also_stay"),
        ("How long will the repair take?", W, "follow"),
        ("Can you deliver it back to my office instead of home?", O, "switch"),
    ],
    "refund-question-then-card": [
        ("I returned two items last week", R, "start"),
        ("but only one refund has shown up on my card", R, "follow"),
        ("the second one was a £60 fleece", R, "answer"),
        ("separately, can I update the card saved on my account?", B, "switch"),
        ("thanks, that's all", B, "closing"),
    ],
}

# C. Persistence: the first PERSIST_SPLIT turns run, then a NEW checkpointer and graph are built (nothing kept in
#    memory) and the thread continues from what DynamoDB holds.
PERSIST_CONVERSATION = "order-then-product-then-billing"
PERSIST_SPLIT = 3

# D. Reducer: a long conversation with a small window (prune above 8 messages, down to 4), so Signpost routes from a
#    pruned history in DynamoDB. (user message, expected agent, turn type)
REDUCER_WINDOW = (8, 4)
LONG_CONVERSATION = [
    ("I ordered a tent and a stove last week, order NW-6002.", O, "start"),
    ("when will it get here?", O, "follow"),
    ("great. Is that tent OK for two people with big rucksacks?", P, "switch"),
    ("and how heavy is it packed?", P, "follow"),
    ("ok. The stove from my last order never lit properly though", W, "switch"),
    ("it's the Pocket Flame 2", W, "answer"),
    ("can you book the repair?", W, "follow"),
    ("Also, how many loyalty points did this order earn?", B, "switch"),
    ("can I use them on the repair?", B, "follow"),
    ("one more thing, the tent pegs were missing from the box", O, "switch"),
    ("yes please send them", O, "answer"),
    ("thanks, bye", O, "closing"),
]
