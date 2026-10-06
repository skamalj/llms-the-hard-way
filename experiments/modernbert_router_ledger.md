# ModernBERT Router: Experiment Ledger

One entry per Kaggle run, newest last. Each entry records what changed, the configuration, the results in absolute numbers on the fixed evaluation suite, and the decision taken.

## Fixed evaluation suite

These are the numbers recorded for every run. Some were not recorded in older runs; those cells show "—".

| ID | Measurement | Where |
|---|---|---|
| E1 | Router, leave-domains-out on generic data (every domain held out once) | Cell 45b |
| E2 | Router, banking benchmark (50) | Cell 47b |
| E3 | Router, all banking (225) | Cell 47b |
| E4 | Router, banking ding-dong live replay, per user turn (25) and full conversations (5) | Cells 51, 58 |
| E5 | Router, realistic conversations, 3 broad agents per company, live (40 turns) | Cell 59 |
| E6 | Context-change detector, leave-domains-out (all / short ≤ 3 words) | Cell 62 |
| E7 | Context-change detector, realistic conversations (35 turns) | Cell 63 |
| E8 | Context-change detector, banking ding-dong turns (18) | Cell 63 |
| E9 | Combined router (detector + router), live, on E4 and E5 | planned (Cell 64) |

The generic training data changed between runs (3,542 → 3,931 → 5,049 conversations), so E1 is only roughly comparable across data versions.

---

## Run 1 — 2026-10-05: frozen ModernBERT-base, dual + cross features

- **Model:** ModernBERT-base (22 layers, H = 768), frozen; our own forward pass.
- **Data:** generic v1, 27 domains, 3,542 conversations; no current agent.
- **Head selection:** listwise loss, lr 1e-3; winner `dual + cross`, MLP-64, best epoch 1–3.
- **Results:**

| E1 | E2 | E3 | E4 turn / conv | Payments vs Card |
|---|---|---|---|---|
| 2484 / 3542 (70.1%) | 40 / 50 | 187 / 225 | 13 / 25 · — | 97 / 117 |

- **Observation:** the head overfits within 1–3 epochs, a sign of domain shift. Short follow-ups are routed on surface words.
- **Decision:** lower lr, add logging, split the big cells. Run 2 accidentally re-ran this same code, and its numbers are identical.

## Run 3 — 2026-10-05: ModernBERT-large, PCA grid

- **Model:** ModernBERT-large (28 layers, H = 1,024), frozen; matches the reference to 2.8e-5.
- **Head selection:** 18 configs (2 feature sets × PCA none/256/64 × linear/MLP-64/MLP-256), lr 3e-4. Winner `dual + cross + sim`, PCA 256, MLP-64.
- **Results:**

| E1 | E2 | E3 | E4 turn / conv | Payments vs Card | Cell 59 (old, 5 overlapping agents, 39 turns) |
|---|---|---|---|---|---|
| 2691 / 3542 (76.0%) | **44 / 50** | **193 / 225** | 18 / 25 · 4 / 5 | **106 / 117** | combined 28 · cross 22 · dual 27 |

- **Observation:** large beats base everywhere, by about 6 points. Without PCA, the heads overfit in 1–5 epochs. Short replies such as "ok", "PS5" and "R-88213" fall back to the conversation's first topic.
- **Decision:** add the current agent as context; drop the separate last-message dual pass; add a cross + dual summed-probability option; remove PCA (user decision).

## Run 4 — 2026-10-05: current agent, no PCA, summed-probability option

- **Data:** generic v2, 3,931 conversations, with `current_agent` (the agent that spoke last) and a short-answer pattern.
- **Features:** `current agent: X` in the input text, plus an `is_current` flag. Dual = conversation vs candidate only.
- **Head selection:** 8 configs; winner `dual + cross + sim`, MLP-256.
- **Results:**

| E1 | E2 | E3 | E4 turn / conv | Payments vs Card |
|---|---|---|---|---|
| 3064 / 3931 (77.9%) | 39 / 50 | 189 / 225 | **21 / 25 · 5 / 5** | 102 / 117 |

| Cell 59 variant | router | router x2 | cross | dual | cross+dual |
|---|---|---|---|---|---|
| 5 distinct agents per company (40 turns) | 27 | — | 27 | 15 | 28 |
| **E5: 3 broad agents per company (40 turns)** | **35** | 29 | 29 | 16 | 27 |

- **Observation:** the current agent helps the live multi-turn replay but hurts some single decisions (Payments → Investment). The `is_current` stay signal is not learned for short answers after a switch. Repeating the last statement ("router x2") hurts. Dual alone is weak.
- **Decision:** add a separate yes/no context-change detector; add many more short-reply examples.

## Run 5 — 2026-10-06: context-change detector + more short replies

- **Data:** generic v3, 5,049 conversations, with `context_change` labels (Y 1,851 / N 2,496; 2,402 short last messages).
- **Router winner:** `dual + cross + sim`, MLP-256 (55 epochs).
- **Router results:**

| E1 | E2 | E3 | E4 turn / conv | E5 router · x2 · cross · dual · cross+dual |
|---|---|---|---|---|
| 4085 / 5049 (80.9%) | 40 / 50 | 184 / 225 | 20 / 25 · 3 / 5 | 31 · 28 · 31 · 18 · 31 |

- **Detector:** one joint pass; spans = last message, history, previous assistant message; 7H features. A linear head won.

| E6 all | E6 short | E7 realistic | E8 banking ding-dong |
|---|---|---|---|
| **4330 / 4347 (99.6%)** | **2393 / 2402** | 32 / 35 | 14 / 18 |

- **Observation:** the detector solves short replies ("55102", "Chrome", "ok thanks" → N with p ≈ 0.00). Its real-world misses come from gaps in the training data:
  - "Also …" always means a switch in training;
  - returns to an earlier topic with "again" are missed;
  - short switches with unseen words are missed;
  - the first real request after the General agent is missed.

  The router alone has plateaued at about 80% and fails short replies even with the current agent known.
- **Decision:** see the roadmap below. Phase 1 (detector + router cascade, detector data gaps) comes next.

## Run 6 — 2026-10-07: Phase 1, hard cascade (branch `exp/phase1-cascade`)

- **Data:** generic v4, 5,914 conversations. The detector fixes were added:
  - "Also/And …" same-topic follow-ups = N;
  - "… again" returns = Y;
  - first request after the General agent = Y;
  - more short-switch wording.
- **New:** an agent-switch label (right agent ≠ current agent), trained with the same detector features. Cell 64 cascade: no current agent → router; p(switch) < 0.5 → stay with the current agent; otherwise the router picks among the *other* agents (the current one is excluded).
- **Router winner:** `dual + cross + sim`, MLP-256, 30 epochs.

**Router alone**

| E1 | E2 | E3 | E4 turn / conv | E5 router · x2 · cross · dual · cross+dual |
|---|---|---|---|---|
| 4771 / 5914 (80.7%) | 41 / 50 | 176 / 225 | 17 / 25 · 3 / 5 | **34** · 30 · 33 · 18 · 32 |

**Detectors** (held-out generic domains / realistic / banking ding-dong)

| Label | E6 all | E6 short | E7 | E8 |
|---|---|---|---|---|
| context change (MLP-256) | 5073 / 5212 (97.3%) | 2601 / 2625 | 30 / 35 | 11 / 18 |
| agent switch (MLP-256) | 5014 / 5212 (96.2%) | 2580 / 2625 | — | banking static with a current agent: 132 / 180 (Y 127/153, **N 5/27**) |

**E9: cascade vs router alone**

| Test | Router alone | Cascade |
|---|---|---|
| Realistic conversations, live | **34 / 40** | 30 / 40 |
| Banking ding-dong, live, per turn | **17 / 25** | 14 / 25 |
| Banking benchmark | **41 / 50** | 31 / 50 |
| All banking | **176 / 225** | 143 / 225 |

- **Verdict: Phase 1 FAILS its pass criteria.** The hard cascade is worse than the router alone on every test.
- **Why:**
  1. **A false "switch" is unrecoverable.** Excluding the current agent guarantees an error whenever the detector wrongly says Y. That happened on same-topic follow-ups that aren't tiny, such as "yes twice" (0.82), "can I spread it out?" (0.99) and "send the link" (0.89).
  2. **Errors compound live:** a wrong pick becomes the current agent, and then "ok thanks" correctly *stays*, with the wrong agent.
  3. **On banking, the switch detector almost always says Y** (it kept only 5 of 27 N cases).
  4. **The data fixes over-corrected:** "Also I was charged twice" (a real switch) is now N.
- **What did improve:** the router alone on realistic conversations, 31 → 34/40, probably from the extra short-reply data. Banking went down (184 → 176).
- **Decision:** don't use a hard gate. Move to Phase 2 (soft fusion: combine the router's and the detector's probabilities, with no exclusion), with the fusion weight tuned on the generic held-out folds, not on the test sets. Also add same-topic follow-up data without a prefix (another request for the same agent) so the detector learns longer same-topic follow-ups.

---

## Branches

Every experiment lives on its own branch, and nothing is merged into `master` until a path is chosen. Experiment branches are pushed to GitHub. The notebook's `DATA_BRANCH` (Cell 34) must name the branch whose data Kaggle should clone.

| Branch | Content | Based on |
|---|---|---|
| `exp/baseline-run5` | Run 5 state: router + context-change detector, with outputs | `master` (b7c1808) |
| `exp/phase1-cascade` | Phase 1: detector + router cascade, detector data fixes | `exp/baseline-run5` |

Later phase branches are created when each phase starts, from the branch of the best result so far.

## Roadmap (agreed plan; update as phases finish)

| Phase | What | Pass criteria | Status |
|---|---|---|---|
| 0 | Ledger and fixed evaluation suite | this file exists; every run is logged | done |
| 1 | Cascade: detector N → stay with the current agent; Y → router picks among the other agents. Plus the detector data-gap fixes | E5 combined ≥ 36/40; E4 per turn ≥ 21/25; E7 ≥ 34/35; E8 ≥ 16/18; E6 no worse than 4300/4347 | **failed (run 6)**: the hard gate is worse than the router alone |
| 2 | Soft fusion instead of a hard cascade: p(change) as a router feature or a logit bias toward the current agent | beats Phase 1 on E4 + E5 without hurting E2/E3 | planned |
| 2b | Learned Q-K-V cross-attention head (from `gemini-suggestions/ModernBERT Cross-Attention Router Model.py`), built on our own forward pass, not AutoModel. Token-level states are cached in fp16. First on the detector: the last-message tokens query the history tokens. Then on the router, as candidate-as-query over the conversation tokens, because a fixed `intent_head` cannot handle dynamic agents | detector: E7/E8 above Phase 1 at the same E6; router: E5 above the best | planned |
| 3 | Representation and head: layer-wise scalar mix (a few layers), residual bottleneck / gated heads, label smoothing; one axis per run | E1 and E5 improve over the best previous run | planned |
| 4 | Calibration: temperature scaling fitted on the validation folds, and the cascade threshold chosen there instead of a fixed 0.5. Confidence gate (entropy or top-1/top-2 margin) with coverage vs accuracy reporting; the fallback action decided with the user | a threshold that keeps ≥ 90% coverage at ≥ 95% accuracy | planned |
| 4b | k-NN memory for the detector (its Y/N labels do not depend on the domain): blend p_model with p_kNN from generic examples | E7/E8 improve | optional |
| — | Rejected for now: target-only second pass / TTA (it removes exactly the history that short replies need; "router x2" already hurt); scaling the attention α inside the frozen encoder (a distribution shift for a frozen backbone); history KV caching for the encoder (only an approximation, because history tokens attend to the new turn); ONNX / Triton / CUDA graphs (latency work, not accuracy) | — | — |
| 5 | Optional: partial fine-tuning of the top 2–4 ModernBERT layers with differential learning rates (fp16 on the T4) | E1/E2/E3 clearly above the frozen best | optional |
