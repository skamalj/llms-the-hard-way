# Signpost-D: validating twin cases (addendum to `validator_instructions_v2_1.md`)

Follow `validator_instructions_v2_1.md` for every question, with its verdicts and output format. This addendum adds the checks for **twins** (`brief_v2_4_twins.md`): a twin is a copy of a base case with exactly one deciding detail changed.

Each twin line in your input also has:
- `twin_of`: the base case's id;
- `change`: the generator's note on what changed and which questions should flip;
- `base`: the base case's state and its gold.

A base line (new pairs, ids ending in `a`) is an ordinary case: check it as usual.

## For every twin, check

1. **One change only.** Compare `state` with `base.state`. Exactly one deciding detail differs (a dependent figure kept consistent with it counts as part of the same change). If anything else differs, or the change is signalled ("updated", a comment), fix the question side only if the question is at fault; otherwise `drop` the whole twin (`"qid": "*"`). Never edit the state.
2. **The flip is real.** Work out each question on the twin yourself. Where the change says a question flips, the twin's gold must put its top on the new answer; where it says a question keeps its answer, the gold must agree with the base's. `look_closely` flags each place where the labellers' average does not match the change note: decide who is right (the labellers or the note) by your own working, and `relabel` the twin's gold if needed.
3. **No threshold ties.** The changed value must not sit exactly on a threshold unless the wording settles it.
4. **The questions still fit.** Option texts or level descriptions that quote a figure from the base must still be true, or not misleading, on the twin. If they no longer fit, `fix` the twin's question (it then differs from the base, which is allowed) or `drop` the twin.

Report, as well as the usual counts: how many twins have a real one-detail change, how many questions really flip, and every twin you dropped and why.
