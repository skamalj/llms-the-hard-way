# Signpost-D: instructions for writing decision cases (v2)

You are writing training data for a small model that makes decisions about situations. Each **case** is one situation plus several questions about it. The model will read the situation and each question, and give a probability for every answer option.

Invent everything yourself. Do not copy, adapt or look up any existing dataset, benchmark, website or document, and do not use the web. Write as a careful professional in each field would.

## 1. What a case contains

1. **A domain**, from the list in section 4.
2. **A situation** ("state"): the information someone would have in front of them when deciding. Vary the form from case to case:
   - a short prose note or report;
   - an email or a message thread (2–6 messages, with who said what);
   - a JSON record (nested fields, lists, numbers, dates, flags; use field names a real system in that domain would plausibly use);
   - a small table (rows and columns, as plain text);
   - a log excerpt (timestamped lines);
   - a form or checklist (field: value lines).

   Length: 40–350 words, or an equivalent amount of data. Include concrete details: names, amounts, dates, quantities, durations, statuses.
3. **3 to 6 questions** about the situation, mixing the three types below. Every question must be answerable from the situation, by reading carefully and judging sensibly as a professional would. Never require outside facts.

## 2. The three question types

| Type | What the question is | Options |
|---|---|---|
| **yes/no** | a statement or question that is either true or false of the situation | exactly `yes` and `no`; give a one-line description of what each means here |
| **choice** | pick one of several named options | 2–6 short option names (1–3 words), each with a one-line description; the options must not overlap |
| **score** | place the situation on an ordered scale | 3–5 levels ordered from low to high, each a short name with a one-line description of what puts a situation at that level |

Mix question **kinds** across cases, roughly in these shares:
- **Read off (about 20%):** the answer is stated or nearly stated ("Has the payment been received?", "Who has the highest score?").
- **Infer (about 20%):** the answer follows from combining details ("Is the order likely to arrive before the event?" when the dates are given separately).
- **Judge / decide (about 40%):** what should happen next, or how serious or urgent something is, weighing several signals ("What should the clinic do with this referral?", "How urgent is this repair?").
- **Compare numbers (about 20%):** amounts against a limit, quantities against an order, dates against a deadline, a total against the sum of its parts, the largest or smallest of several values.

Make about 70% of situations **clear-cut** and about 30% **genuinely mixed**: conflicting signals, missing information, or two reasonable answers. A mixed case is valuable only if a careful reader would still lean one way, or would honestly split between two options.

Vary everything:
- the wording of the questions (do not reuse one phrasing across cases);
- the number of options, by quota (section 3);
- which option is correct. Do not let the first option, the most dramatic option or the "sensible middle" option ("hold and check", "fix then release") usually win; in clear-cut cases the extreme options should win about as often as the middle ones;
- the domain mix within your batch.

## 2a. Wording rules (each one prevents an ambiguity found in the pilot)

- **Boundaries:** every limit says whether it is inclusive: "at least", "more than", "on or before", "within 28 days counting the day after". Never put a value exactly on a threshold unless the wording settles it.
- **Counting:** say how days, hours or items are counted, when it matters ("business days, not counting today").
- **One reading:** every rule, policy or term in the situation has a single meaning. Define terms like "full pallet" or "par level" where they decide an answer.
- **Stated practice:** if an answer depends on how an organisation works (oldest stock first, what counts as a usable device), state it in the situation.
- **Criteria for "first", "main" and "most":** questions like "what should be done first" or "what was the main cause" name the criterion: earliest deadline, most severe harm, or what the outcome depended on.
- **Data, not estimates:** do not write questions whose answer depends on choosing between the literal data and an estimate between data points.
- **Dates:** if you give a weekday with a date, give the year, and make sure they match. Otherwise give dates without weekdays, or weekdays without dates.

## 3. Writing the options well

- Every option must be a real possibility in that situation, not a filler.
- A description says what the option *means* ("Pause the shipment until the address is confirmed"), not whether it applies here.
- Score levels must be in order and evenly spread. A situation should be placeable at exactly one level by a careful reader. Neighbouring levels must differ in **what they mean for the decision**, ideally with thresholds ("under 2 hours", "2–24 hours", "more than a day"); never two levels that both mean "no real effect".
- Choice options must be mutually exclusive: never two options that could both be done.
- **Option-count quotas** across your batch:
  - choice questions: about 15% with 2 options, 30% with 3, 25% with 4, 20% with 5, 10% with 6;
  - score questions: about 40% with 3 levels, 35% with 4, 25% with 5.
- Do not reveal the answer in the question.

## 4. Domains

Spread each batch roughly evenly over these:

- **Work and business:** retail store operations · restaurant and catering · hotel and hospitality · event planning · real estate and property management · construction site work · manufacturing line · warehouse and inventory · procurement and purchasing · accounts and bookkeeping · payroll and HR requests · recruiting and hiring · IT helpdesk · software releases and bugs · facilities and building maintenance · fleet and vehicle management · logistics and courier delivery · insurance claims · banking and lending · legal intake at a small firm · marketing campaigns · online marketplace sellers · customer support for an online service · subscription and membership management · grant and funding applications
- **Public and care:** clinic appointments and referrals · pharmacy · school administration · university admissions · library services · city services and permits · utilities (power, water, internet) · emergency preparedness at a workplace · nonprofit volunteer coordination
- **Everyday life:** household budgeting · home repairs · travel bookings · moving house · pet care · personal fitness and health tracking · neighbourhood and housing association

## 4a. Working rules

- Work only in the private folder you are given. Never read or write any other folder except your output file.

## 5. Output format

One JSON object per line (JSON Lines). For each case:

```json
{"id": "<batch>-001", "domain": "pharmacy", "form": "message thread",
 "state": "<the situation: a string, or a JSON object for record-style situations>",
 "questions": [
   {"qid": "q1", "type": "yes_no", "kind": "infer",
    "question": "…", "options": {"yes": "…", "no": "…"}},
   {"qid": "q2", "type": "choice", "kind": "judge",
    "question": "…", "options": {"<name>": "<description>", "…": "…"}},
   {"qid": "q3", "type": "score", "kind": "judge",
    "question": "…", "levels": [{"name": "…", "description": "…"}, "… low to high …"]}
 ]}
```

`kind` is one of `read`, `infer`, `judge`, `compare`. **Do not include answers.** Separate labellers will answer every question independently.

## 6. Labellers (a separate step)

Each labeller sees the situation and the questions, never the other labellers' answers, and gives for every question a probability for each option or level, summing to 1. They reflect genuine uncertainty:
- a clear-cut answer gets most of the weight;
- a mixed case is spread across the options a careful professional would hesitate between.

Three labellers per case; their distributions are averaged.

## 7. Validators (a separate step)

For every case, check:
- the state is realistic and complete enough;
- every question is answerable from it;
- the options are distinct and meaningful;
- the score levels are ordered and placeable;
- no question gives its answer away;
- the averaged labels agree with a careful reading. Where the labellers disagree strongly, decide whether the case is genuinely mixed (keep it) or badly written (fix the question or drop the case).
