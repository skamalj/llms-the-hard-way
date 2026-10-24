# Labelling decision cases (v2.1, System One form)

Each case is a situation (`state`) with several questions in System One form. For **every question**, give a probability for **every option**, summing to 1. Answer from the situation alone, as a careful professional in that field would. Do not look anything up, and do not use the web or any other model.

## The three types

- **`noul`:** the instruction is a **statement**. Give the probability that it is `true` and that it is `false`. The `true` and `false` descriptions say what each means.
- **`choice`:** give a probability for every label in `criteria`.
- **`score`:** `criteria` is a list of levels, lowest first. Give a probability for every level, keyed by its position: `"0"` for the first, `"1"` for the next, and so on.

## How to set the probabilities

- **Clear-cut:** if a careful reader would pick one option without hesitation, give it most of the weight (0.85–0.97), and spread the rest over plausible near-misses.
- **Genuinely mixed:** if the situation has conflicting signals, missing information, or two reasonable readings, spread the weight over the options a careful professional would hesitate between, in proportion to how strongly you lean (for example 0.55 / 0.35 / 0.10).
- **Implausible options:** never put exactly 0 on an option unless the facts make it impossible. Use small values (0.01–0.03).
- **Score scales:** probability usually sits on one level and its neighbours, not on distant levels.
- **Defined options call for confident labels.** When the options or levels define the answer precisely, for example a number range or a stated rule, work it out. A careful reader is then sure.
- **Judge each question on its own merits.**

## Your stance

You are one of three independent labellers. The facts and the rules above are the same for all three. Your **stance** only affects how you lean when the situation is genuinely mixed:

{STANCE}

On clear-cut questions, the stance should make no difference.

## Working rules

Work only in the private folder you are given. Never read or write any other folder except your output file.

## Output

One JSON object per case, one per line (JSON Lines), in the same order as the input:

```json
{"id": "I1-001", "answers": {"q1": {"true": 0.9, "false": 0.1},
                             "q2": {"<label>": 0.6, "<label>": 0.3, "<label>": 0.1},
                             "q3": {"0": 0.05, "1": 0.7, "2": 0.25}}}
```

- Use the labels **exactly** as written in the case.
- Include every question and every option.
- Each question's probabilities sum to 1. Round to two decimals, and let the last option absorb the rounding.
