# thanos_v6 — thanos_v5 + 100 more handwritten pairs

| Split | Rows | From |
|---|---|---|
| train | 698 | thanos_v5 train (598) + 100 handwritten (`raw/handwritten_pairs_2.jsonl`, h101–h200) |
| validation | 25 | unchanged |
| test | 25 | unchanged |

The new pairs follow the same rules as v5's h001–h100 (see `../thanos_v5/README.md`): weighty statements (cost, resolve, loss, warning, duty) plus everyday ones with names, numbers and conditions; restructured into short, heavy clauses; every fact, name, number (as words), negation, condition and hedge kept; questions stay questions; no interpretive additions.

Handwritten pairs in train: 200 of 698 (29 %).

**Checks** (`build_v6.py`, all pass): no target equals its input or contains a digit; no new input resembles a validation, test or demo sentence (word overlap < 0.5) or repeats a v5 training input (< 0.6; h104 was replaced for this); no demo sentence resembles any training input.

Rebuild: `python build_v6.py` (reads `../thanos_v5/`). Used by `10-prefix-bridge-split/`.
