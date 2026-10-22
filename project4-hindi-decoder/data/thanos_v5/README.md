# thanos_v5 — English → Thanos-voice English, with a stricter hand-written set

`thanos_v4` plus **100 pairs written by hand** (`raw/handwritten_pairs.jsonl`, ids h001–h100, origin `handwritten`).

| Split | Rows | From |
|---|---|---|
| train | 598 | thanos_v4 train (498) + 100 handwritten |
| validation | 25 | thanos_v4, unchanged |
| test | 25 | thanos_v4, unchanged |

**Why.** In run R12 (v4) the model kept the meaning but the voice stayed light: polite rewordings ("Should…", "yet") rather than Thanos. The handwritten pairs push the voice harder while staying **strict**:

- statements with weight (cost, resolve, loss, warning, duty), plus everyday ones with names, numbers and conditions;
- restructured into short, heavy clauses, often two sentences ("Three months of study, and I fell two marks short.");
- every fact, name, number (as words), negation, condition and hedge kept; a question stays a question;
- **no interpretive additions**: a second sentence only restates what the input says. (The curated validation set does add interpretive second sentences; chrF will not reward their absence.)

h013–h018 are the six sentences of the notebook's earlier final cell (R12), now training data; the notebook's final cell has six new sentences (`DEMO` in `build_v5.py`), kept out of training.

**Checks** (`build_v5.py`, all pass): no target equals its input or contains a digit; no handwritten input resembles a validation, test or demo sentence (word overlap < 0.5) or repeats a v4 training input (< 0.6); no demo sentence resembles any training input (< 0.5).

Rebuild: `python build_v5.py` (reads `../thanos_v4/`).
