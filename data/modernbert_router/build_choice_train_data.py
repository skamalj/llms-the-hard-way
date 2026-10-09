"""Grounded choice TRAINING questions for the choice head (runs 16-17). Never used for testing.

Run from the repo root: python data/modernbert_router/build_choice_train_data.py

Same three question types as E12 (yes / no, choice, score on an ordered scale) and the same rule: the answer is in the
text, no world knowledge. The texts are generated from phrase banks written for this file, so wording varies; most texts
are asked SEVERAL questions with different answers, which teaches the model to read the question, not only the text.
The builder checks that no training text or question shares a 5-word phrase with any E12 test text, and balances the
yes / no answers 50 / 50 within every family (run 16's yes / no head leaned to "no" after a 335 / 508 split).
"""
import json
import random
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "choice_train"
rng = random.Random(16)
YN = ["yes", "no"]
items = []


def add(family, typ, state, question, options, answer):
    assert answer in options, (state, question, answer)
    items.append({"id": f"ct{len(items):05d}", "domain": f"choice/{family}", "type": typ, "category": family,
                  "state": state, "question": question, "options": list(options), "answer": answer})


def ask_yn(family, state, question, truth):
    add(family, "noul", state, question, YN, "yes" if truth else "no")


# ---------------------------------------------------------------- tone / sentiment
POS = ["The staff were brilliant and the room was spotless.", "Quick delivery and the quality is excellent.",
       "Really pleased with the repair, it works like new.", "Lovely people, great coffee, we'll be back.",
       "Setup took two minutes and everything just worked.", "The tutor was patient and my son finally enjoys maths.",
       "Fantastic service from start to finish.", "The new menu is delicious, the dessert was a highlight.",
       "Exactly as described and it arrived a day early.", "Our guide was funny and knew everything about the castle."]
NEU = ["The parcel arrived on Tuesday.", "I received the invoice and will pass it to accounts.",
       "The room was as described.", "The course runs for six weeks.", "I've updated my address in the app.",
       "The meeting has been moved to the second floor.", "The bus was on time.", "Please find the form attached.",
       "The shop opens at nine on Saturdays.", "My order number is on the email you sent."]
NEG = ["The food was cold and we waited over an hour.", "Third time the app has crashed today, really fed up.",
       "The cleaner missed half the rooms and left a mess.", "Nobody called me back despite two promises.",
       "The jacket ripped the first time I wore it.", "Rude staff and a dirty table, very disappointing.",
       "The engineer never turned up and nobody told us.", "I was overcharged and the refund still hasn't come.",
       "The seats were broken and the film kept stopping.", "Worst hotel stay I've had, the heating never worked."]
for s in POS:
    ask_yn("tone", s, "Is the writer happy?", True)
    add("tone", "choice", s, "What is the tone of the message?", ["negative", "neutral", "positive"], "positive")
    add("tone", "score", s, "How satisfied is the customer?", ["unhappy", "neutral", "happy"], "happy")
for s in NEU:
    ask_yn("tone", s, "Is the writer complaining?", False)
    add("tone", "choice", s, "What is the tone of the message?", ["negative", "neutral", "positive"], "neutral")
    add("tone", "score", s, "How satisfied is the customer?", ["unhappy", "neutral", "happy"], "neutral")
for s in NEG:
    ask_yn("tone", s, "Is the writer happy?", False)
    ask_yn("tone", s, "Is the writer complaining?", True)
    add("tone", "choice", s, "What is the tone of the message?", ["negative", "neutral", "positive"], "negative")
    add("tone", "score", s, "How satisfied is the customer?", ["unhappy", "neutral", "happy"], "unhappy")

# ---------------------------------------------------------------- urgency
URG = {
    "high": ["The server room is flooding right now!", "Our shop's card machines are all down and customers are queueing.",
             "Gas smell in the kitchen, what do I do?", "The lift is stuck with my dad inside.",
             "We can't open the front door and the kids are inside alone.", "Payroll failed and staff get paid today."],
    "medium": ["The printer upstairs keeps jamming, could someone look this week?", "My laptop is getting slow, can IT check it soon?",
               "The heating in meeting room 3 isn't great, please look at it in the next few days.",
               "One of the delivery vans has a warning light on.", "A few customers say the website is slow at lunchtime."],
    "low": ["No rush, but the logo on the website could be a bit bigger.", "At some point could we order more pens?",
            "Whenever convenient, please update my job title in the directory.", "Not urgent: the coffee machine descaling light is on.",
            "Next month would be fine to repaint the fence."],
}
for level, texts in URG.items():
    for s in texts:
        add("urgency", "score", s, "How urgent is this?", ["low", "medium", "high"], level)
        ask_yn("urgency", s, "Does this need attention immediately?", level == "high")
        ask_yn("urgency", s, "Does the writer say there is no rush?", "rush" in s.lower() or "not urgent" in s.lower() or "whenever" in s.lower())

# ---------------------------------------------------------------- intent
INTENT = {
    "refund": ["Please return the cost of the headphones to my card.", "Please refund the £40 for the cancelled lesson.",
               "Can I get a refund on the train ticket?"],
    "exchange": ["Can I swap this shirt for a medium?", "I'd like to exchange the blue kettle for the red one.",
                 "The shoes pinch, can I change them for a half size up?"],
    "repair": ["Can someone fix my bike's gears?", "The dishwasher leaks, please send someone to repair it.",
               "My phone screen is cracked, can you mend it?"],
    "information": ["What are your opening hours on Sunday?", "Do you deliver to Cardiff?", "Is the hall wheelchair accessible?"],
    "cancel": ["Please cancel my gym membership.", "I'd like to cancel tomorrow's appointment.", "Cancel my newspaper subscription from May."],
    "complaint": ["Your driver blocked my drive for an hour.", "The toilets were filthy again today.", "I was kept on hold for 50 minutes."],
}
INTENT_OPTS = list(INTENT)
for intent, texts in INTENT.items():
    for s in texts:
        opts = [intent] + rng.sample([o for o in INTENT_OPTS if o != intent], 3)
        rng.shuffle(opts)
        add("intent", "choice", s, "What does the customer want?", opts, intent)
        ask_yn("intent", s, "Is the customer asking for a refund?", intent == "refund")
        ask_yn("intent", s, "Is this a complaint?", intent == "complaint")
        ask_yn("intent", s, "Does the customer want to cancel something?", intent == "cancel")

# ---------------------------------------------------------------- facts: is X stated?
NAMES = ["Priya", "Tomasz", "Grace", "Omar", "Elena", "Kofi", "Hannah", "Luis", "Mei", "Callum"]
ITEMS = ["printer", "sofa", "laptop", "fridge", "bicycle", "lamp", "mattress", "camera", "desk", "heater"]
for k in range(60):
    name, item = rng.choice(NAMES), rng.choice(ITEMS)
    num = rng.randint(10000, 99999)
    with_num = k % 2 == 0
    with_phone = k % 3 == 0
    with_date = k % 4 < 2
    parts = [f"Hi, it's {name}."]
    parts.append(f"My {item} (order {num}) stopped working." if with_num else f"My {item} stopped working.")
    if with_date:
        parts.append(f"It was delivered on the {rng.randint(2, 28)}th.")
    if with_phone:
        parts.append(f"Call me on 07{rng.randint(100, 999)} {rng.randint(100000, 999999)}.")
    s = " ".join(parts)
    ask_yn("fact", s, "Does the customer give an order number?", with_num)
    ask_yn("fact", s, "Does the customer give a phone number?", with_phone)
    ask_yn("fact", s, "Does the message say when the item was delivered?", with_date)
    add("fact", "choice", s, "Which item is the message about?", [item] + rng.sample([i for i in ITEMS if i != item], 2), item)
for k in range(30):
    food = rng.choice(["nuts", "gluten", "dairy", "shellfish", "eggs"])
    has = k % 2 == 0
    s = (f"Table for {rng.randint(2, 8)} on Friday. One guest can't eat {food}." if has
         else f"Table for {rng.randint(2, 8)} on Friday, it's a birthday so a candle would be lovely.")
    ask_yn("fact", s, "Does the booking mention a dietary need?", has)
    ask_yn("fact", s, "Is the booking for Friday?", True)
    ask_yn("fact", s, "Is the booking for Saturday?", False)

# ---------------------------------------------------------------- detail: the stated one among several mentioned
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
COLOURS = ["black", "white", "navy", "green", "red", "grey"]
CITIES = ["Bristol", "Leeds", "Glasgow", "Norwich", "Exeter", "York"]
for k in range(40):
    a, b, c = rng.sample(DAYS, 3)
    pattern = k % 3
    if pattern == 0:
        s, ans = f"{a} is no good for me any more, can we do {b} instead?", b
    elif pattern == 1:
        s, ans = f"Let's keep {a}. {b} and {c} are both busy for me.", a
    else:
        s, ans = f"I'd prefer {c}, but {a} would also work if {c} is full.", c
    opts = [a, b, c]
    rng.shuffle(opts)
    add("detail", "choice", s, "Which day does the writer want?", opts, ans)
    ask_yn("detail", s, f"Does the writer want {ans}?", True)
    other = next(d for d in opts if d != ans)
    ask_yn("detail", s, f"Does the writer want {other}?", False)
for k in range(30):
    a, b = rng.sample(COLOURS, 2)
    s = rng.choice([f"Since {a} has run out, {b} will do.", f"Not the {a}, please send the {b} version.",
                    f"I ordered {b} but you sent {a}."])
    want = b
    opts = [a, b, rng.choice([c for c in COLOURS if c not in (a, b)])]
    rng.shuffle(opts)
    add("detail", "choice", s, "Which colour does the customer want?", opts, want)
for k in range(30):
    a, b = rng.sample(CITIES, 2)
    s = rng.choice([f"I live in {a} now, so please send it to {b}, where I work.", f"Ship it to {b}, not to my old address in {a}.",
                    f"I moved from {a} to {b} last month; please deliver to the new address."])
    opts = [a, b, rng.choice([c for c in CITIES if c not in (a, b)])]
    rng.shuffle(opts)
    add("detail", "choice", s, "Which city should it be delivered to?", opts, b)
    ask_yn("detail", s, f"Should it be delivered to {a}?", False)

# ---------------------------------------------------------------- compare numbers in the text
PEOPLE = ["Ade", "Bea", "Cai", "Dev", "Eli", "Fay", "Gus", "Ida"]
for k in range(50):
    who = rng.sample(PEOPLE, 3)
    vals = rng.sample(range(40, 99), 3)
    unit = rng.choice([("scored", ""), ("ran", " km"), ("sold", " tickets")])
    s = ", ".join(f"{p} {unit[0]} {v}{unit[1]}" for p, v in zip(who, vals)) + "."
    hi, lo = who[vals.index(max(vals))], who[vals.index(min(vals))]
    add("compare", "choice", s, "Who has the highest number?", who, hi)
    add("compare", "choice", s, "Who has the lowest number?", who, lo)
    ask_yn("compare", s, f"Did {who[0]} get more than {who[1]}?", vals[0] > vals[1])
for k in range(40):
    p1, p2 = rng.sample(range(15, 120), 2)
    thing = rng.choice(["The basic plan", "The small box", "The standard room", "The morning class"])
    other = rng.choice(["the premium plan", "the large box", "the deluxe room", "the evening class"])
    s = f"{thing} costs £{p1} and {other} costs £{p2}."
    ask_yn("compare", s, f"Is {thing.lower()} cheaper?", p1 < p2)
    add("compare", "choice", s, "Which option is cheaper?", [thing.lower(), other], thing.lower() if p1 < p2 else other)
for k in range(30):
    t1, t2 = rng.sample(range(5, 55), 2)
    s = f"Route A takes {t1} minutes and route B takes {t2} minutes."
    add("compare", "choice", s, "Which route is faster?", ["route A", "route B"], "route A" if t1 < t2 else "route B")
    ask_yn("compare", s, "Does route B take longer than route A?", t2 > t1)

# ---------------------------------------------------------------- counting
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
for k in range(40):
    adults, kids = rng.randint(1, 3), rng.randint(0, 3)
    if (adults, kids) == (2, 3):                       # E12 has "Two adults and three children"
        kids = 2
    s = f"Booking for {WORDS[adults]} adult{'s' if adults > 1 else ''}" + (f" and {WORDS[kids]} child{'ren' if kids > 1 else ''}." if kids else ", no children.")
    total = adults + kids
    opts = sorted({total, max(1, total - 1), total + 1})
    add("count", "choice", s, "How many people are in the booking?", [WORDS[o] for o in opts], WORDS[total])
    ask_yn("count", s, "Are there children in the booking?", kids > 0)
    ask_yn("count", s, "Are there more children than adults?", kids > adults)

# ---------------------------------------------------------------- topic and language
TOPIC = {
    "sport": ["The striker scored twice in the second half.", "She won the 400 metres in a new club record."],
    "weather": ["Frost is likely overnight with clear skies.", "Thunderstorms will move east during the afternoon."],
    "cooking": ["Fold the egg whites gently into the batter.", "Roast the peppers until the skins blister."],
    "politics": ["The minister resigned after the vote.", "Parliament will debate the bill next week."],
    "health": ["Drink plenty of water and rest for two days.", "The clinic offers flu jabs on Wednesdays."],
    "travel": ["The ferry to the island leaves every hour.", "Our flight was diverted to Manchester."],
}
TOPICS = list(TOPIC)
for t, texts in TOPIC.items():
    for s in texts:
        opts = [t] + rng.sample([o for o in TOPICS if o != t], 3)
        rng.shuffle(opts)
        add("topic", "choice", s, "What is the text about?", opts, t)
LANG = {
    "French": ["Pouvez-vous m'envoyer la facture, s'il vous plaît ?", "Le colis n'est pas encore arrivé."],
    "Spanish": ["¿A qué hora abre la tienda mañana?", "Necesito cancelar mi cita del jueves."],
    "German": ["Mein Paket ist leider beschädigt angekommen.", "Können Sie mich morgen zurückrufen?"],
    "Italian": ["Vorrei prenotare un tavolo per due persone.", "Il treno è in ritardo di venti minuti."],
    "Portuguese": ["Gostaria de mudar o meu endereço de entrega.", "A encomenda chegou ontem à noite."],
}
LANGS = list(LANG) + ["English"]
for lang, texts in LANG.items():
    for s in texts:
        opts = [lang] + rng.sample([o for o in LANGS if o != lang], 3)
        rng.shuffle(opts)
        add("language", "choice", s, "Which language is the message in?", opts, lang)
        ask_yn("language", s, "Is the message written in English?", False)

# ---------------------------------------------------------------- team routing (non-agent wording)
TEAMS = {
    "billing": ["There are two identical charges for March on my statement.", "Why is my invoice higher this month?", "My direct debit failed."],
    "technical support": ["The app freezes when I upload a photo.", "I can't connect the printer to Wi-Fi.", "Error 504 when I log in."],
    "sales": ["Can I get a quote for 50 licences?", "Do you offer a discount for charities?", "I'd like to upgrade to the business plan."],
    "deliveries": ["My parcel says delivered but it isn't here.", "Can you deliver on Saturday instead?", "The courier left it in the rain."],
}
TEAMS_L = list(TEAMS)
for team, texts in TEAMS.items():
    for s in texts:
        add("routing", "choice", s, "Which team should handle this?", TEAMS_L, team)
        ask_yn("routing", s, "Is this about money or payments?", team == "billing")

# ---------------------------------------------------------------- scales from stated numbers
for k in range(40):
    days = rng.choice([0, 1, 2, 3, 5, 9, 14, 21, 30, 45])
    s = rng.choice(["Fixing it should take roughly {} days.", "Delivery is expected in {} days.", "The visa takes around {} days to process."]).format(days) \
        if days else "We can do it today while you wait."
    level = "same day" if days == 0 else "within a week" if days <= 7 else "more than a week"
    add("scale", "score", s, "How long will it take?", ["same day", "within a week", "more than a week"], level)
for k in range(40):
    n = rng.choice([4, 8, 15, 30, 45, 60, 90, 120, 200, 350])
    s = rng.choice(["We expect about {} people at the launch.", "The class has {} students.", "Around {} guests are coming to the party."]).format(n)
    level = "under 20" if n < 20 else "20 to 100" if n <= 100 else "over 100"
    add("scale", "score", s, "How big is the group?", ["under 20", "20 to 100", "over 100"], level)
    ask_yn("scale", s, "Are more than 100 people expected?", n > 100)
FREQ = {"rarely": ["It happened once last spring.", "Maybe twice a year at most."],
        "sometimes": ["It happens every couple of weeks.", "Now and then, perhaps once a week."],
        "constantly": ["It happens every time I use it.", "Non-stop, all day, every day."]}
for level, texts in FREQ.items():
    for s in texts:
        add("scale", "score", s, "How often does it happen?", ["rarely", "sometimes", "constantly"], level)
INTENS = {"calm": ["No problem at all, whenever suits you.", "Thanks, happy to wait for the update."],
          "annoyed": ["This is the second time, a bit annoying to be honest.", "I'd appreciate a faster reply next time."],
          "furious": ["This is a disgrace. I want a manager NOW.", "Absolutely unacceptable, I'm reporting you."]}
for level, texts in INTENS.items():
    for s in texts:
        add("scale", "score", s, "How angry is the writer?", ["calm", "annoyed", "furious"], level)
        ask_yn("scale", s, "Is the writer angry?", level != "calm")

# ---------------------------------------------------------------- more ordered scales
for k in range(60):
    before = rng.randint(40, 200)
    ratio = rng.choice([0.4, 0.6, 0.97, 1.0, 1.03, 1.8, 2.5, 3.2])
    now = round(before * ratio)
    level = "lower" if ratio < 0.9 else "about the same" if ratio <= 1.1 else "much higher"
    s = rng.choice(["This quarter's gas bill is £{n}; last quarter it was £{b}.", "I paid £{n} this month against £{b} the month before.",
                    "The water bill came to £{n}. Normally it's around £{b}."]).format(n=now, b=before)
    add("scale", "score", s, "How does the new amount compare with before?", ["lower", "about the same", "much higher"], level)
    ask_yn("scale", s, "Is the new amount higher than before?", now > before)
CERT = {"unsure": ["I honestly can't remember which branch it was.", "Not sure, it could have been any of them.",
                   "No idea if I locked it, sorry.", "I might be wrong, I really don't know."],
        "fairly sure": ["I think it was the Leeds branch, probably.", "Pretty sure it was last Thursday.",
                        "It was most likely the blue form.", "I believe I paid, but I'd have to check."],
        "certain": ["It was the Leeds branch, I have the receipt in my hand.", "Definitely Thursday, it's in my calendar.",
                    "I'm completely sure, I watched it happen.", "Absolutely certain, the bank confirmed it."]}
for level, texts in CERT.items():
    for s in texts:
        add("scale", "score", s, "How sure is the writer?", ["unsure", "fairly sure", "certain"], level)
POLITE = {"rude": ["Sort it out, I'm not asking again.", "Are you people incapable of reading?", "Stop wasting my time and fix it."],
          "neutral": ["The form is attached.", "Please update the address.", "Order 4471, status please."],
          "very polite": ["Huge thanks for bearing with me, it means a lot.", "Sorry to trouble you, would you kindly check this?",
                          "Many thanks for your help, it's very kind of you."]}
for level, texts in POLITE.items():
    for s in texts:
        add("scale", "score", s, "How polite is the writer?", ["rude", "neutral", "very polite"], level)
        ask_yn("scale", s, "Is the writer polite?", level == "very polite")
SAT5 = {"very unhappy": ["Dreadful from start to end, I want a full refund.", "The worst service I have ever had."],
        "unhappy": ["A bit disappointing, the room was smaller than shown.", "Not great, it took ages to arrive."],
        "neutral": ["It was fine, nothing special either way.", "Average experience, did the job."],
        "happy": ["Good value and friendly staff.", "Nice place, we enjoyed it."],
        "very happy": ["Absolutely wonderful, could not have been better!", "Perfect in every way, thank you so much!"]}
for level, texts in SAT5.items():
    for s in texts:
        add("scale", "score", s, "How satisfied is the customer?", list(SAT5), level)

# ================================================================ run 17: more families, more texts (built in pairs of
# questions with opposite answers wherever possible, so yes / no stays balanced and the question has to be read)
FIRST = ["Asha", "Ben", "Chloe", "Dan", "Ewa", "Femi", "Gita", "Harry", "Iris", "Jon", "Kemi", "Liam", "Maya", "Nico", "Ola", "Pete",
         "Rosa", "Sam", "Tara", "Umar", "Vera", "Wes", "Yara", "Zak"]
PRODUCTS = ["kettle", "router", "blender", "jacket", "tablet", "toaster", "rucksack", "monitor", "speaker", "watch", "drill", "pram",
            "headset", "vacuum", "chair", "keyboard"]
PLACES = ["Bath", "Cardiff", "Derby", "Durham", "Hull", "Inverness", "Lincoln", "Oxford", "Perth", "Preston", "Stirling", "Truro"]
TIMES = ["8am", "9:30am", "11am", "12:30pm", "2pm", "3:15pm", "4pm", "5:30pm", "7pm", "8:45pm"]
CHANNELS = ["email", "phone", "text message", "post"]
STATUS = {"delivered": ["Your {p} was handed to you at the door.", "We left your {p} in the porch as asked."],
          "in transit": ["Your {p} is on its way and arrives tomorrow.", "The {p} has left our warehouse and is with the courier."],
          "delayed": ["Sorry, your {p} is held up and will be three days late.", "The courier missed today's run, so your {p} is late."],
          "cancelled": ["As requested, the {p} order has been cancelled.", "We could not supply the {p}, so the order is cancelled."]}
ST = list(STATUS)

# --- delivery status (choice + yes / no pairs)
for k in range(160):
    st = ST[k % 4]
    prod = rng.choice(PRODUCTS)
    s = rng.choice(STATUS[st]).format(p=prod)
    opts = ST[:]
    rng.shuffle(opts)
    add("status", "choice", s, "What is the status of the order?", opts, st)
    ask_yn("status", s, "Has the customer received the item?", st == "delivered")
    ask_yn("status", s, f"Is the order {rng.choice([o for o in ST if o != st])}?", False)
    ask_yn("status", s, f"Is the order {st}?", True)

# --- who did what (names and roles)
for k in range(200):
    a, b = rng.sample(FIRST, 2)
    act = rng.choice([("booked the room", "paid the deposit"), ("wrote the report", "checked the figures"),
                      ("called the plumber", "let him in"), ("ordered the cake", "collected it"), ("found the keys", "returned them")])
    s = f"{a} {act[0]} and {b} {act[1]}."
    add("who", "choice", s, f"Who {act[0]}?", sorted([a, b, rng.choice([n for n in FIRST if n not in (a, b)])]), a)
    add("who", "choice", s, f"Who {act[1]}?", sorted([a, b, rng.choice([n for n in FIRST if n not in (a, b)])]), b)
    ask_yn("who", s, f"Did {a} {act[0].split(' ', 1)[0].rstrip('ed') if False else act[0].replace('booked', 'book').replace('wrote', 'write').replace('called', 'call').replace('ordered', 'order').replace('found', 'find')}?", True)
    ask_yn("who", s, f"Did {b} {act[0].replace('booked', 'book').replace('wrote', 'write').replace('called', 'call').replace('ordered', 'order').replace('found', 'find')}?", False)

# --- appointment times and parts of the day
def part_of_day(t):
    h = int(t.split(":")[0].rstrip("apm"))
    pm = t.endswith("pm")
    h24 = h + 12 if pm and h != 12 else h
    return "morning" if h24 < 12 else "afternoon" if h24 < 17 else "evening"
for k in range(200):
    t = rng.choice(TIMES)
    who_ = rng.choice(["the dentist", "the optician", "your mechanic", "the vet", "the hairdresser", "the bank adviser"])
    day = rng.choice(DAYS)
    s = rng.choice(["Reminder: you're booked with {w} on {d} at {t}.", "{d} at {t} is confirmed with {w}.",
                    "Your slot with {w} is {t} this {d}."]).format(w=who_, d=day, t=t)
    pod = part_of_day(t)
    add("time", "choice", s, "When is the appointment?", ["morning", "afternoon", "evening"], pod)
    ask_yn("time", s, "Is the appointment in the morning?", pod == "morning")
    ask_yn("time", s, f"Is the appointment on {day}?", True)
    ask_yn("time", s, f"Is the appointment on {rng.choice([d for d in DAYS if d != day])}?", False)

# --- contact preferences
for k in range(160):
    want, avoid = rng.sample(CHANNELS, 2)
    s = rng.choice(["Please contact me by {w}, not by {a}.", "{W} is best for me; I'd rather you didn't use {a}.",
                    "Don't use {a} please. {W} only."]).format(w=want, a=avoid, W=want.capitalize())
    opts = CHANNELS[:]
    rng.shuffle(opts)
    add("preference", "choice", s, "How does the customer want to be contacted?", opts, want)
    ask_yn("preference", s, f"Does the customer want to be contacted by {want}?", True)
    ask_yn("preference", s, f"Does the customer want to be contacted by {avoid}?", False)

# --- policy / rule reading (eligibility from stated numbers)
for k in range(220):
    limit = rng.choice([14, 28, 30, 60, 90])
    days_ago = rng.choice([3, 10, 20, 29, 31, 45, 75, 100])
    item = rng.choice(PRODUCTS)
    s = (f"Our policy: returns are accepted within {limit} days of purchase. "
         f"I bought the {item} {days_ago} days ago and want to send it back.")
    ok_ = days_ago <= limit
    ask_yn("policy", s, "Can the customer still return the item under the policy?", ok_)
    ask_yn("policy", s, "Is the purchase outside the return period?", not ok_)
    add("policy", "choice", s, "What should happen to the return request?", ["accept it", "refuse it"], "accept it" if ok_ else "refuse it")
for k in range(160):
    min_age = rng.choice([12, 16, 18, 21])
    age = rng.choice([9, 13, 15, 17, 19, 22, 30])
    act = rng.choice(["the climbing course", "the go-kart session", "the wine tasting", "the night tour"])
    s = f"{act.capitalize()} is open to people aged {min_age} and over. My son is {age}; can he join?"
    ask_yn("policy", s, "Is the son old enough to join?", age >= min_age)
    ask_yn("policy", s, "Is the son too young to join?", age < min_age)

# --- aspect sentiment (mixed reviews: the question decides the answer)
ASPECTS = [("the food", ["delicious", "excellent", "superb"], ["cold", "bland", "greasy"]),
           ("the staff", ["friendly", "helpful", "kind"], ["rude", "slow", "unhelpful"]),
           ("the room", ["spotless", "spacious", "quiet"], ["dirty", "tiny", "noisy"]),
           ("the price", ["fair", "reasonable", "great value"], ["steep", "too high", "a rip-off"]),
           ("the delivery", ["quick", "on time", "careful"], ["late", "careless", "slow"])]
for k in range(260):
    (a1, g1, b1), (a2, g2, b2) = rng.sample(ASPECTS, 2)
    good1 = k % 2 == 0
    w1 = rng.choice(g1 if good1 else b1)
    w2 = rng.choice(b2 if good1 else g2)
    s = rng.choice(["{A1} was {w1}, but {a2} was {w2}.", "{A1}: {w1}. {A2}: {w2}.", "Honestly {a1} was {w1}; {a2}, on the other hand, was {w2}."]
                   ).format(A1=a1.capitalize(), a1=a1, w1=w1, A2=a2.capitalize(), a2=a2, w2=w2)
    ask_yn("aspect", s, f"Was the writer happy with {a1}?", good1)
    ask_yn("aspect", s, f"Was the writer happy with {a2}?", not good1)
    add("aspect", "choice", s, "What did the writer like?", sorted([a1, a2]), a1 if good1 else a2)
    add("aspect", "choice", s, "What did the writer dislike?", sorted([a1, a2]), a2 if good1 else a1)

# --- negation and changes of mind
for k in range(200):
    a, b = rng.sample(PLACES, 2)
    s = rng.choice(["I was going to fly to {a}, but now I'm going to {b} instead.", "Not {a} any more, the meeting moved to {b}.",
                    "Scrap {a}; we're meeting in {b}."]).format(a=a, b=b)
    opts = sorted([a, b, rng.choice([x for x in PLACES if x not in (a, b)])])
    add("negation", "choice", s, "Where is the writer going now?", opts, b)
    ask_yn("negation", s, f"Is the writer still going to {a}?", False)
    ask_yn("negation", s, f"Is the writer going to {b}?", True)

# --- thresholds on stated numbers
for k in range(220):
    n = rng.randint(2, 400)
    th = rng.choice([10, 25, 50, 100, 200])
    thing = rng.choice([("parcels", "We shipped {n} parcels today."), ("tickets", "So far {n} tickets have been sold."),
                        ("complaints", "The shop logged {n} complaints this month."), ("pages", "The report runs to {n} pages.")])
    s = thing[1].format(n=n)
    if n == th:
        continue
    ask_yn("threshold", s, f"Is the number of {thing[0]} more than {th}?", n > th)
    ask_yn("threshold", s, f"Is the number of {thing[0]} fewer than {th}?", n < th)

# --- sequence: what happened first / last
EVENTS = ["the alarm went off", "the lights went out", "the doorbell rang", "the phone rang", "the dog barked", "the kettle boiled"]
for k in range(160):
    e1, e2, e3 = rng.sample(EVENTS, 3)
    s = rng.choice(["First {a}, then {b}, and finally {c}.", "{A}. A minute later {b}. After that {c}."]).format(
        a=e1, b=e2, c=e3, A=e1.capitalize())
    opts = sorted([e1, e2, e3])
    add("sequence", "choice", s, "What happened first?", opts, e1)
    add("sequence", "choice", s, "What happened last?", opts, e3)
    ask_yn("sequence", s, f"Did this come before \"{e1}\": {e2}?", False)
    ask_yn("sequence", s, f"Did this come before \"{e3}\": {e1}?", True)

# --- product spec reading
for k in range(180):
    prod = rng.choice(PRODUCTS)
    w = rng.randint(1, 30)
    bat = rng.choice([0, 6, 10, 24, 48])
    col = rng.choice(COLOURS)
    s = f"Spec sheet — {prod}: weight {w} kg, colour {col}, " + (f"battery life {bat} hours." if bat else "mains powered, no battery.")
    ask_yn("spec", s, f"Does the {prod} have a battery?", bat > 0)
    ask_yn("spec", s, f"Is the {prod} {col}?", True)
    ask_yn("spec", s, f"Is the {prod} {rng.choice([c for c in COLOURS if c != col])}?", False)
    add("spec", "score", s, f"How heavy is the {prod}?", ["under 5 kg", "5 to 15 kg", "over 15 kg"],
        "under 5 kg" if w < 5 else "5 to 15 kg" if w <= 15 else "over 15 kg")

# --- request type and asked-for action
REQ = {"price": ["How much would it cost to {x}?", "Could you quote me to {x}?"],
       "booking": ["Can I book someone to {x} next week?", "I'd like to arrange for you to {x}."],
       "status": ["Have you managed to {x} yet?", "Any update on whether you can {x}?"],
       "cancellation": ["Please don't {x} after all, cancel it.", "I no longer need you to {x}."]}
XS = ["service the boiler", "clean the carpets", "fit a new lock", "trim the hedge", "repaint the hallway", "fix the gutter"]
for k in range(200):
    rt = list(REQ)[k % 4]
    s = rng.choice(REQ[rt]).format(x=rng.choice(XS))
    opts = list(REQ)
    rng.shuffle(opts)
    add("request", "choice", s, "What is the customer asking for?", opts, rt)
    ask_yn("request", s, "Is the customer asking for a price?", rt == "price")
    ask_yn("request", s, "Is the customer cancelling something?", rt == "cancellation")

# --- more scales: amount of damage, size of a delay, satisfaction from mixed wording
for k in range(160):
    lvl = ["minor", "moderate", "severe"][k % 3]
    s = rng.choice({"minor": ["There's a tiny scratch on the {p}, barely visible.", "Just a small mark on the {p}, nothing serious."],
                    "moderate": ["The {p} has a dent and one button is loose.", "A crack along the side of the {p}, but it still works."],
                    "severe": ["The {p} arrived smashed and can't be used at all.", "The {p} is in pieces, completely destroyed."]}[lvl]).format(
        p=rng.choice(PRODUCTS))
    add("damage", "score", s, "How bad is the damage?", ["minor", "moderate", "severe"], lvl)
    ask_yn("damage", s, "Does the item still work?", lvl != "severe")
for k in range(140):
    mins = rng.choice([2, 5, 10, 25, 40, 70, 120, 240])
    s = rng.choice(["The train is running {m} minutes late.", "Your table will be ready in about {m} minutes.", "Expect a wait of roughly {m} minutes."]).format(m=mins)
    lvl = "short" if mins <= 10 else "medium" if mins <= 45 else "long"
    add("delay", "score", s, "How long is the wait?", ["short", "medium", "long"], lvl)
    ask_yn("delay", s, "Is the wait over an hour?", mins > 60)

# ---------------------------------------------------------------- checks against E12 (no shared text)
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).split()


def shingles(s, n=5):
    w = norm(s)
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


e12 = json.load(open(HERE / "choice_test" / "items.json"))["items"]
e12_states = {x["state"] for x in e12}
e12_sh = set().union(*(shingles(s) for s in e12_states))
clash = [x["state"] for x in items if x["state"] in e12_states or shingles(x["state"]) & e12_sh]
assert not clash, sorted(set(clash))
ids = Counter(x["id"] for x in items)
assert all(n == 1 for n in ids.values())

# balance yes / no within every family: drop surplus answers of the majority side at random
by_fam = {}
for x in items:
    if x["type"] == "noul":
        by_fam.setdefault((x["category"], x["answer"]), []).append(x)
drop = set()
for fam in {f for f, _ in by_fam}:
    y, n = by_fam.get((fam, "yes"), []), by_fam.get((fam, "no"), [])
    big, small = (y, n) if len(y) > len(n) else (n, y)
    drop |= {x["id"] for x in rng.sample(big, len(big) - len(small))}
items = [x for x in items if x["id"] not in drop]

OUT.mkdir(exist_ok=True)
json.dump({"items": items}, open(OUT / "items.json", "w"), indent=1, ensure_ascii=False)
types = Counter(x["type"] for x in items)
texts = Counter(x["state"] for x in items)
yes = sum(x["answer"] == "yes" for x in items if x["type"] == "noul")
print(f"choice training items: {len(items)} | " + " | ".join(f"{t} {n}" for t, n in types.items())
      + f" | yes/no balance {yes} yes / {types['noul'] - yes} no")
print("families:", dict(Counter(x["category"] for x in items).most_common()))
print(f"distinct texts: {len(texts)} | texts asked more than one question: {sum(n > 1 for n in texts.values())}")
print("no text shares a 5-word phrase with E12; wrote", OUT / "items.json")
