# Signpost-D: invoice cases (brief v2.1, one domain)

Read these two files first, and follow them for everything not said here:

- **`brief_v2.md`** sets the standard for cases: question kinds, clear-cut and mixed, wording rules, options and quotas.
- **`format_spec.md`** sets the exact output form, System One:
  - **true/false items are statements,** with `true` and `false` descriptions that between them cover every case;
  - **choice items** are labels, each with a description;
  - **score items** are a list of `"Name: description"` levels, lowest first, and the instruction names the quantity they rise in.

Where the two disagree on form, `format_spec.md` wins.

Invent everything yourself. Do not look anything up, and do not use the web.

## The domain: checking supplier invoices before payment

Each case is one moment in an accounts-payable team's work. A supplier's invoice has arrived, or is due to be paid, and someone must decide what to do with it. Draw on what a careful accounts-payable clerk or finance manager actually checks:

- **The invoice against what was ordered:** items, quantities, unit prices, agreed discounts, tax, delivery or freight charges, and whether the order was authorised.
- **The invoice against what was received:** quantities delivered, short or damaged deliveries, items not yet received, and services not yet performed.
- **The invoice itself:**
  - the supplier's identity and bank details, including changes to bank details;
  - the invoice number and date;
  - arithmetic: line totals, subtotal, tax, and the grand total;
  - currency;
  - whether it may already have been paid or entered.
- **Payment timing:** payment terms, due dates, early-payment discounts and late fees, cash available, and the order of priority in a payment run.
- **Approval:** spending limits, who must sign off, missing approvals, and approvers who are away.
- **The supplier relationship:** disputes, credit notes, previous issues, and new suppliers.

Vary the business behind each case widely: restaurants, building firms, schools, clinics, software companies, charities, shops, factories, a household paying a tradesperson, and so on. Vary the supplier, the amounts, the currency and the size of the problem. **Many invoices should be perfectly fine.** A clean invoice that should simply be paid is a valid, common case, so don't make every case a trap.

## Form

- **About half the states are JSON records,** written the way a finance system would store an invoice, an order, a delivery note or a payment schedule: nested objects and lists, short field names, numbers as numbers, dates as strings.
- **The other half are text:** an email from a supplier, a message thread inside the finance team, a clerk's note, a small table, or a log of a payment run.
- **Rules:** sometimes state the team's rule (an approval limit, a tolerance for price differences, a payment-run rule). Sometimes give no rule, and let the answer rest on what a careful professional would normally do.

## Batch shape

Write **50 cases** in your batch, each with **3–6 questions**, using the kind shares and option-count quotas of `brief_v2.md`.

Ask about what an invoice checker actually decides:
- whether to pay, hold or query;
- what is wrong, and how serious it is;
- how urgent it is to act;
- whether the arithmetic or a comparison holds;
- who must approve.

Never use the same question wording in two cases.

## Output

One JSON object per line, in System One form, **without gold**:

```json
{"id": "<batch>-001", "domain": "accounts payable", "form": "JSON record",
 "state": {"...": "..."},
 "questions": {"q1": {"type": "noul", "instructions": "<a statement>", "criteria": {"true": "…", "false": "…"}},
               "q2": {"type": "choice", "instructions": "…", "criteria": {"<label>": "<description>", "…": "…"}},
               "q3": {"type": "score", "instructions": "<names its quantity>", "criteria": ["Lowest: …", "…", "Highest: …"]}},
 "kinds": {"q1": "read", "q2": "judge", "q3": "compare"}}
```

`kind` is one of `read`, `infer`, `judge`, `compare`.

Work only in the private folder you are given. Before finishing, check your output by script:
- every line parses, and the ids run in order;
- every `noul` instruction is a statement (no "?"), and its criteria keys are exactly `true` and `false`;
- every choice has 2–6 labels, each with a description;
- every score has 3–5 levels;
- no question text repeats.
