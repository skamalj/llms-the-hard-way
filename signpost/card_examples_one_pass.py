"""The one-pass model card's code examples, run exactly as written in the card; their printed output is recorded in the card.

    python card_examples_one_pass.py <path to the signpost-one-pass folder>
"""
import sys
import time

sys.path.insert(0, sys.argv[1])
from signpost_one_pass import SignpostOnePass  # noqa: E402

t0 = time.perf_counter()
sp = SignpostOnePass(sys.argv[1])
print(f"[loaded on {sp.device} in {time.perf_counter() - t0:.1f}s]\n")

# ---- 1. Routing a first message
agents = {
    "Orders Agent": "Handles order status, delivery dates, tracking and changing a delivery address.",
    "Returns Agent": "Handles returns, exchanges, return labels and refunds for returned items.",
    "Billing Agent": "Handles payments, invoices, double charges and saved cards.",
    "Tech Support Agent": "Fixes problems with the app, logins and devices.",
}
messages = [{"role": "user", "content": "I was charged twice for my last order."}]
agent, probs = sp.route(messages, agents)
print("1.", agent, {a: round(p, 3) for a, p in probs.items()})

# ---- 2. Routing inside a conversation (history + the agent that answered last)
messages = [
    {"role": "user", "content": "I need to send back a jacket, it's the wrong colour."},
    {"role": "assistant", "content": "Sorry about that! Which colour did you receive?"},
    {"role": "user", "content": "the green one"},
]
agent, probs = sp.route(messages, agents, current_agent="Returns Agent")
print("2a.", agent, round(probs[agent], 3))                    # a short answer stays with the current agent

messages += [
    {"role": "assistant", "content": "Thanks, I've emailed you a free return label for the green jacket."},
    {"role": "user", "content": "and my app keeps logging me out, can someone look at that?"},
]
agent, probs = sp.route(messages, agents, current_agent="Returns Agent")
print("2b.", agent, round(probs[agent], 3))                    # a new topic moves to another agent

# ---- 3. A choice question about a text
pick, probs = sp.choice("Help! My payouts have been failing for 3 days!",
                        "Which team should handle this?", ["billing", "sales", "retail"])
print("3.", pick, {o: round(p, 3) for o, p in probs.items()})

# ---- 4. A yes / no question
p_yes = sp.yes_no("Help! My payouts have been failing for 3 days!", "Does this convey urgency?")
print("4.", round(p_yes, 3))

# ---- 5. A score on an ordered scale (levels from low to high)
level, expected, probs = sp.score("Help! My payouts have been failing for 3 days!",
                                  "How frustrated is the writer?", ["calm", "frustrated", "furious"])
print("5.", level, round(expected, 2), {l: round(p, 3) for l, p in probs.items()})

# ---- 6. More choice / yes-no / score examples
print("6a.", sp.choice("The blue sofa is £899 and the grey one is £749.", "Which sofa is cheaper?", ["blue", "grey"])[0])
print("6b.", round(sp.yes_no("I'll pay by bank transfer this time instead of card.", "Will the customer pay by card?"), 3))
print("6c.", sp.score("No rush, whenever you get a moment.", "How urgent is this?", ["low", "medium", "high"])[0])

# ---- 7. Many agents: one pass, however many there are
store = {
    "Orders Agent": "Tracks orders, delivery dates and changes to a delivery address.",
    "Returns Agent": "Handles returns, exchanges and return labels.",
    "Refunds Agent": "Handles refunds for returned or cancelled items.",
    "Billing Agent": "Handles invoices, payment failures and double charges.",
    "Gift Cards Agent": "Sells and redeems gift cards and checks their balance.",
    "Loyalty Agent": "Handles reward points and membership tiers.",
    "Product Advice Agent": "Helps choose products: sizes, materials and compatibility.",
    "Repairs Agent": "Books repairs and handles warranty claims for broken products.",
    "Store Locations Agent": "Gives store addresses, opening hours and stock at a store.",
    "Account Agent": "Handles logins, passwords, email changes and closing an account.",
    "Business Sales Agent": "Handles bulk orders and quotes for companies.",
    "Complaints Agent": "Takes formal complaints about staff or service.",
}
t0 = time.perf_counter()
agent, probs = sp.route([{"role": "user", "content": "The zip on my backpack broke after two weeks, can you fix it under warranty?"}], store)
print(f"7. {agent} {round(probs[agent], 3)} ({len(store)} agents, {(time.perf_counter() - t0) * 1000:.0f} ms on {sp.device})")

# ---- 8. A question with many options
cities = ["Lisbon", "Oslo", "Prague", "Dublin", "Vienna", "Krakow", "Seville", "Bergen", "Porto", "Zagreb",
          "Tallinn", "Ghent", "Lyon", "Turin", "Malmo", "Riga", "Bilbao", "Bruges", "Graz", "Split"]
pick, probs = sp.choice("We flew into Oslo on Friday, then took the train west to Bergen, where the conference was.",
                        "In which city was the conference?", cities)
print(f"8. {pick} {round(probs[pick], 3)} ({len(cities)} options)")
