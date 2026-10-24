# Labelling decision cases

Each case is a situation (`state`) with several questions. For **every question**, give a probability for **every option** (or every score level), summing to 1. Answer from the situation alone, as a careful professional in that field would. Do not look anything up, and do not use the web or any other model.

## How to set the probabilities

- **Clear-cut:** if a careful reader would pick one option without hesitation, give it most of the weight (0.85–0.97) and spread the rest over plausible near-misses.
- **Genuinely mixed:** if the situation has conflicting signals, missing information, or two reasonable readings, spread the weight over the options a careful professional would hesitate between, in proportion to how strongly you lean (for example 0.55 / 0.35 / 0.10).
- **Implausible options:** never put exactly 0 on an option unless it is impossible given the facts; use small values (0.01–0.03).
- **Score scales:** probability usually sits on one level and its neighbours, not on distant levels.
- **Yes/no:** the options are `yes` and `no` as described in the question.
- **Defined options call for confident labels:** when the options or levels define the answer precisely (a number range, a stated rule), a careful reader is sure; do not spread weight there.
- **Judge each question on its own merits.** Do not try to make the answers of one case consistent with a story you invent.

## Your stance

You are one of three independent labellers. The facts and the rules above are the same for all three; your **stance** only affects how you lean when the situation is genuinely mixed:

{STANCE}

On clear-cut questions, the stance should make no difference.

## Working rules

Work only in the private folder you are given. Never read or write any other folder except your output file.

## Output

One JSON object per case, one per line (JSON Lines), in the same order as the input:

```json
{"id": "A-001", "answers": {"q1": {"yes": 0.9, "no": 0.1},
                            "q2": {"<option name>": 0.6, "<option name>": 0.3, "<option name>": 0.1},
                            "q3": {"<level name>": 0.05, "<level name>": 0.7, "<level name>": 0.25}}}
```

Use the option and level names **exactly** as written in the case. Include every question and every option. Each question's probabilities sum to 1 (round to two decimals; make the last one absorb rounding).
