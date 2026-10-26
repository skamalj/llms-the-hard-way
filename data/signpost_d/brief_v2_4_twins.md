# Signpost-D: twin cases (brief v2.4)

Read these two files first, and follow them for everything not said here:

- **`brief_v2.md`** sets the standard for cases: situations, forms, question kinds, wording rules, options and domains.
- **`format_spec.md`** sets the exact output form, System One: true/false items are statements with `true`/`false` descriptions; choice items are labels with descriptions; score items are `"Name: description"` levels, lowest first, and the instruction names its quantity.

Where the two disagree on form, `format_spec.md` wins. Invent everything yourself. Do not look anything up, and do not use the web.

## Why twins

A model can often guess an answer from the words around the deciding detail ("leaks", "late", "compromised") without reading the detail itself: the number, the date, or the rule clause that actually settles it. A **twin** is a copy of a case in which **exactly one deciding detail is changed**, so that the answer to at least one question changes, while everything else stays the same. Seeing both versions, a model can only tell them apart by reading that detail.

## What a twin must be

1. **One change only.** Change exactly one of these, and nothing else in the state:
   - **a number** (about half of all twins): an amount, a count, a percentage, a duration, a time or a date, so that a comparison or a calculation comes out the other way (for example 7 returns out of 252 sold becomes 14 out of 252, against a 5% limit);
   - **one clause of a stated rule** (about a third): add or remove an exception, change "at least" to "more than", change a limit, change which condition applies (for example "faulty items get a full refund whatever their state" is removed from the policy);
   - **one fact or status** (the rest): a flag, an approval, a signature, a yes/no field, which person did something.
2. **The questions stay word for word the same**, with the same options or levels in the same order, and the same `kinds`.
3. **The change must flip at least one question:** for a clear-cut question, its correct answer becomes a different option (for a score question, a different level; for true/false, the opposite). Where the case allows, **at least one other question keeps its answer**, so a model also learns what the change does not affect.
4. **The new value never sits exactly on a threshold** unless the wording settles it. Work out every answer yourself, before and after the change.
5. **The changed case must still be realistic and consistent:** if a total depends on the changed number, either change only something no total depends on, or keep every dependent figure consistent (and count that as the one change).
6. **Do not signal the change:** no "(updated)", no comment, no extra emphasis. The twin must read as an ordinary case.

## Output

One JSON object per line, in System One form, **without gold**. Each twin carries `twin_of` (the id of the case it was made from) and `change`: one sentence saying what changed, which questions flip and to what, and which keep their answer. `change` is for the validators only; it is never shown to the model or the labellers.

```json
{"id": "<batch>-001", "twin_of": "<base id>", "domain": "...", "form": "...",
 "state": "...", "questions": {"q1": {"...": "..."}}, "kinds": {"q1": "compare"},
 "change": "returns_last_28_days 7 -> 14: q2 flips (2.8% -> 5.6%, now above the 5.0% limit); q1, q3 keep their answer"}
```

## Two kinds of batch

- **Twins of existing cases (batches TB):** you are given base cases (state, questions, kinds, no answers). Write one twin of each, with id `<batch>-001` … in the order given, `twin_of` set to the base's id, and the same `domain` and `form`.
- **New pairs (batches TA):** write a new base case to `brief_v2.md`'s standard (3–5 questions of mixed types, at least one compare question), then its twin. The base gets id `<batch>-NNa` and the twin `<batch>-NNb`, with `twin_of` set to the base's id; the base has no `twin_of` and its `change` is an empty string. Spread your pairs over the domains you are given; about half the states JSON records.

Work only in the private folder you are given. Before finishing, check your output by script:
- every line parses; ids run in order; every twin's `twin_of` names its base;
- a twin's questions and kinds are identical to its base's (same keys, same instructions, same criteria);
- a twin's state differs from its base's (and, by your own reading, in one detail only);
- every `change` names at least one question that flips.
