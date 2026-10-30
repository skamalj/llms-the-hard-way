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
| E10 | Realistic multi-turn test, 35 conversations / 193 typed turns, live | Cell 69 |
| E11 | First-turn only, 100 single messages, 10 companies × 5 agents, typed | Cell 71 |
| E12 | Grounded choice questions (phase 8): at least 50 each of yes / no, choice and score (ordered scale), plus same-text / different-question pairs. Every answer is in the given text; no world knowledge. `data/modernbert_router/choice_test/` | phase 8 cells |

## Scorecard S1: ours vs the Strands decider (filled per run from phase 8 on; routing rows from run 13)

**Rules.** (1) **The exact same questions for both models** (same items, texts, questions, options and option order, from the same files); only the *presentation* may differ, each model in its own native format. A comparison on different questions is not a benchmark. Before any E12 row is reported, the two result files are checked item by item for identical item ids. (2) Nothing tuned on reported test data: our τ is chosen on the E10 dev companies only; the decider is used zero-shot in its documented format. (3) The decider's best setting is shown too (E10: 3-turn window). (4) Absolute pass / total; known contamination flagged. (5) The routing rows are the regression check for every later phase.

**Headline line:** routing on unseen companies (E10 test) ours vs decider; grounded choice (E12) ours vs decider; latency ours vs decider.

**Latest filled scorecard: run 21** (LoRA ModernBERT-large, ordinal score loss, one model for routing + choice: E10 test 81 / 83, E10 all 180, E11 95, banking 50 · 220, E12 **161 / 170** (yes / no 58, choice 56, score 47), ~50 ms p50. Decider: 62 / 69 · 151 / 163 · 96 · 48 / 214 · E12 160 (56 / 56 / 48), p50 185–439 ms. One seed each; differences of about ±4 are within run-to-run noise). Full tables in the run 19 and run 21 entries (routing on the E10 test companies: ours 70 (71 with confident switch) vs decider 62 / 69; E12: ours 96 / 170 zero-shot vs decider 160 / 170; E12 time per question: 63 ms vs 200 ms). Full tables in the run 14 entry.

**Table 1: accuracy**

| Suite | Items | What it tests | Ours | Decider | Note |
|---|---|---|---|---|---|
| E10 routing, test companies | 83 turns | multi-turn chat, unseen companies | gate | full / window 3 | headline routing number |
| E10 routing, all | 193 turns | same, all companies | | | dev turns were used to choose τ |
| E10 by turn type | 83 | stay vs switch behaviour | | | answer, closing, switch, short_switch, … |
| E11 first turn | 100 | single message, 5 agents | | | |
| Banking | 50 / 225 | banking routing | | | decider trained on banking77 / CLINC: not unseen for it |
| E12 yes / no | ≥ 50 | "Does this convey urgency?" | | | accuracy at 0.5 |
| E12 choice | ≥ 50 | "Which team should handle this?" | | | |
| E12 score | ≥ 50 | "How frustrated? calm / frustrated / depressed" | | | exact position, and mean distance in positions |
| E12 question pairs | pairs | same text, two questions | | | both answers right |

**Table 2: cost** (same T4, batch 1, warm, tokenization included)

| Measure | Ours | Decider |
|---|---|---|
| Latency p50 / p95 per routing turn (E10) | stay path / route path / blended | full / window 3 |
| Latency per E12 question | | |
| ms at 3 / 5 / 10 options | | |
| Peak GPU memory | | |
| Parameters | ModernBERT-large 395M + Nemotron-1B + heads | 2B + LoRA + head |
| Training needed for a new company / agent / question | none (descriptions only) | none |

The generic training data changed between runs (3,542 → 3,931 → 5,049 conversations), so E1 is only roughly comparable across data versions.

---

## How we got here: the evolution in 22 runs (summary for the blog, 2026-10-11)

*Written to be read on its own. Every number is pass / total on test items no model was trained on. Run numbers point to the full entries below; each phase has its own git branch (see "Branches").*

### The result

**Model name: Signpost** (user decision, 2026-10-11): one model that points each message to the right agent and each question to the right answer. The base model is credited in the model card ("fine-tuned from ModernBERT-large", Apache 2.0).

A **ModernBERT-large encoder (395 M parameters, frozen) with 7.2 M trainable LoRA parameters and a 0.26 M scoring head** is one model for two jobs:
- **agent routing**, with chat history and the current agent;
- **general grounded choice questions** about a text: yes / no, pick one of N, or rate on a scale.

It is about **one-fifth the size of the Strands decider** (Qwen3.5-2B + LoRA + head, about 2 B parameters), **trains in 33 minutes on one T4**, and answers in about **50 ms**. On the same test items:

| Test (same items for both) | **Ours: ModernBERT-large + LoRA (run 21)** | Strands decider 2B |
|---|---|---|
| Routing with chat history, unseen companies (E10 test, 83) | **81** | 62 (full history) / 69 (3-turn window) |
| Routing with chat history, all turns (E10, 193) | **180** | 151 / 163 |
| Routing a first message (E11, 100) | 95 | 96 |
| Banking routing (50 / 225) | **50 / 220** | 48 / 214 (banking77 was in its training) |
| General choice questions (E12, 170) | **161** | 160 |
| … yes / no (58) · choice (59) · score (53) | 58 · 56 · 47 | 56 · 56 · 48 |
| Latency p50, ms (E10 · E11 · banking · E12), T4 | **50 · 50 · 70 · 48** | 342 · 278 · 439 · 185 |

So we are **level with the decider on general choice questions, ahead on every routing test, and 4–7× faster** on our own tests.

**On the independent test set** (written outside the project; run 22b), the picture is:
- routing in conversations 131 vs 113 / 121 (**ahead**, mostly on switches);
- first messages 181 vs 178 (level);
- yes / no 74 vs 77 and choice 104 vs 106 (close);
- **score 53 vs 70 (behind)**, at 4–5.5× the speed.

The E12 score parity did not generalize. Our model also switches agents too readily on stay-type turns there (37 vs 48–49 of 55). That is with one seed per model, so differences of about ±4 are within the measured noise. "Level" is the honest word for E12, and "ahead" is safe only where the gap is far larger than that, as on routing.

### The path, phase by phase

| Phase (branch) | Runs | What we tried | What happened | What we learned |
|---|---|---|---|---|
| **Foundations** (`master`, `exp/baseline-run5`) | 1–5 | Our own ModernBERT forward pass (matches the reference to 2.8e-5); a frozen encoder plus a small head that scores (conversation, agent description) pairs from a joint (cross) pass and separate (dual) passes; base → large; PCA (removed); current agent as input; a yes / no context-change detector | Held-out routing 70% → 81%; banking 40 → 44 / 50; the detector solved short replies (99.6% held-out) | Large beats base; the current agent is needed for short replies; a frozen router plateaus around 80% |
| **Combining router and detector** (`exp/phase1-cascade`, `exp/phase2b-qkv-attention`) | 6–7 | A hard cascade (the detector decides stay / switch); a learned Q-K-V attention head for the detector | The cascade hurt (every wrong "switch" became a routing error); Q-K-V gave no robust gain | A detector should only act where it is very sure |
| **Encoders and realistic tests** (`exp/phase3a-modernbert`, `exp/phase3b-nemotron`) | 8–9 | A pluggable encoder: ModernBERT-large vs Nemotron-1B (a bidirectional Llama embedding model); new realistic tests E10 (chat history) and E11 (first turn) | Nemotron routed better (E10 +16, banking +20); ModernBERT was the better detector | Different pretraining, different strengths: this held to the end |
| **Benchmark** (`exp/benchmark-strands-decider`) | B1 | The Strands decider (2 B, zero-shot) on the same tests | E10 151 / 163, E11 96, banking 48 / 214 | A strong general model, weaker on long chat histories |
| **Hybrid + gate** (`exp/phase4-encoder-combos`, `exp/phase5-windowing`) | 10, 10b | Nemotron router + ModernBERT detector; a one-sided "confident stay" gate with τ chosen on dev companies; windowing the history | **74 / 83** on unseen companies vs the decider's 62 / 69; windowing gave nothing | The best frozen-encoder design |
| **Data and simplification** (`exp/phase6-realistic-train`, `exp/phase7-simplify`, `exp/phase7b-qkv-switch`) | 11–13 | Free-form realistic training conversations; removing everything that never won (cascade, soft fusion, switch detector, extra configs); switch-heavy data; a Q-K-V rewrite | Selection 5× faster; switch data lifted banking to 47 / 205; Q-K-V attention stayed uniform; the remaining errors were the router staying with the current agent on related switches | Simpler is better; measure one change at a time |
| **General choice, frozen** (`exp/phase8-general-choice`, `exp/phase8b-unified-choice`, `exp/phase8c-separate-heads`) | 14–17 | A new test E12 (170 yes / no, choice, score questions, the decider's job); one question format (`question:` + `candidate:`); shared vs separate heads; 6× more choice data | Zero-shot 96 → 113 → **114 / 170** (decider 160); identical runs differed by 4 on banking | **Frozen features plateau**: no head or amount of data teaches the encoder to read; and run-to-run noise is real |
| **Fine-tuning with LoRA** (`exp/phase9-choice-lora`, `exp/phase9b-lora-combined`) | 18–19 | Hand-written LoRA adapters on every attention and MLP layer + the same scoring head; one pass per option; then **one model for routing and choice**, on ModernBERT-large and Nemotron-1B | E12 114 → **153**; routing E10 test 75 (ModernBERT) / **79** (Nemotron) without any gate or detector; banking 212 / 217 | **The step change of the project.** The plateau was the frozen encoder. Nemotron still routes better, ModernBERT reads better |
| **Closing the score gap** (`exp/phase9c-score-data`, `exp/phase9d-score-loss`) | 20–21 | More score data (no gain; it taught a "deadline word = urgent" shortcut); a near-paraphrase guard against teaching the test; severity-based urgency data; an order-aware score loss | Score 43 → 46 → **47 / 53** (decider 48); E12 **161 / 170**; E10 test **81 / 83**; banking **50 / 220** | Data can teach shortcuts; guard against near-copies of test items; ordered scales need an ordered loss |
| **Independent review** (`exp/phase9e-independent`) | 22 | Test cases written outside the project, from a brief | First delivery largely template-made (20 texts for 300 questions; contradictory routing labels); flagged, run as delivered, revision requested | An outside test is needed for the final claim; it needs a precise brief and a self-check |

### The decisions that mattered most

1. **Fine-tune the encoder (LoRA), not just the head** (run 18). This one change moved general choice from 114 to 153 and routing from 74 to 75–81, with only 7.2 M trained parameters.
2. **One question format for everything** (run 16): `<text or conversation> | current agent | question | candidate`. Routing became one question among many, which let one model learn both jobs (run 19) at no cost to either.
3. **Remove what doesn't win** (Phase 7). The gate, cascade, switch detector, Q-K-V head and windowing all went. After fine-tuning, routing needs no detector at all.
4. **Treat measurement as part of the work:**
   - companies held out for testing, with dev companies for every choice of threshold;
   - the same items for both models;
   - absolute numbers;
   - a noise estimate (±4);
   - a guard that stops near-paraphrases of test items entering training;
   - an independent test set.
5. **Match the loss to the question.** Scales are ordered, so near-misses should cost less (the ordinal loss, run 21).

### What remains open

- **Error bars:** 2 more seeds of the final model.
- **The revised independent test set.** All our other tests were written by the same author as the training data, so a shared style may favour our model.
- **The decider's latency is an upper bound.** It ran in bfloat16 on a T4 without its optimized kernels. Our ModernBERT ran fp32 weights under autocast.
- **Banking is not unseen for the decider**, which was trained on banking77 / CLINC.
- ~~Nemotron-1B with the ordinal loss~~ **done (run 23):** a routing tie with ModernBERT-large, clearly worse on choice questions, at 3× the size. ModernBERT-large stays the final model.

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

## Run 7 — 2026-10-07: Phase 2b, learned Q-K-V attention head (branch `exp/phase2b-qkv-attention`)

- **Same data and router as run 6** (identical router numbers: E1 4771/5914, E2 41/50, E3 176/225, E4 17/25, E5 router 34/40).
- **New:** token-level states from one pass over `history [SEP] current agent` (5,212 × up to 193 tokens × 1,024, fp16, 2.06 GB). A trainable head: LayerNorm → 8-head attention (Q = last-message tokens, K/V = context tokens) → residual + LayerNorm → MLP on [mean of target x, mean of attended target h]. Trained for both labels, same folds, lr 1e-4, early stopping (best epoch ≈ 12).

**Held-out generic domains (in distribution): no gain**

| | Pooled detector | Q-K-V head |
|---|---|---|
| Context change, all / short | **5073** / 2601 | 5050 / 2595 |
| Agent switch, all / short | **5014** / 2580 | 4958 / 2571 |

**Unseen real-world tests: Q-K-V generalizes better**

| Test | Pooled | Q-K-V |
|---|---|---|
| E7 context change, realistic (35) | 30 (Y 13/15) | **32 (Y 15/15)** |
| E8 context change, banking ding-dong (18) | 11 | **14** |
| Agent switch, banking with a current agent (180) | 132 (N kept 5/27) | **144 (N kept 12/27)** |

**Cascade (hard gate), live**

| Test | Router alone | Cascade, pooled | Cascade, Q-K-V |
|---|---|---|---|
| Realistic conversations (40) | **34** | 30 | 32 |
| Banking ding-dong per turn (25) | 17 | 14 | **18** |
| All banking (225) | **176** | 143 | 156 |

- **Attention maps:** the attention is diffuse (top weights 0.01–0.05). There's a little signal: "afternoon" looks most at "or" in "Morning or afternoon?". The frozen encoder has already mixed the context into the target tokens, so the extra attention layer is not acting as a sharp pointer.
- **Verdict:** Q-K-V is a real improvement in **out-of-domain** detection (+2 realistic, +3 banking turns, +12 banking switch) at the same in-domain score. It's the first cascade to beat the router alone on the ding-dong replay (18 vs 17). But a hard gate still loses to the router alone overall. The remaining false "switch" calls are same-agent follow-ups about a *different aspect* of the same topic:
  - "how long until I get my money back?" (Returns & Refunds): 0.98;
  - "ah right, can I pay it in two parts?" (Billing): 0.88;
  - "Does the new plan come with a phone upgrade?": 0.97;
  - "what documents were missing?": 1.00.
- **Decision:** use the **Q-K-V** detectors from now on. Next is Phase 2 soft fusion (router probabilities × detector probability, no exclusion, weight tuned on generic held-out folds). Add generic data for "same agent, different aspect" follow-ups.

---

## Run 8 — 2026-10-07: Phase 3a, ModernBERT-large, pluggable encoder + layer mix + residual head + soft fusion (branch `exp/phase3a-modernbert`)

- **Same data as runs 6–7.** New: spans found by character offsets (encoder-agnostic); layer option last / mix (mean of the last 4 layers); a `resid-ls` head (residual bottleneck + label smoothing 0.1); soft fusion (router + w × Q-K-V switch, w chosen on generic held-out folds). Memory-lean handling: RAM steady at 4.6 GB (the first attempt died at the layer switch).
- **Regression check passed:** the detectors reproduce run 7 within 0.3% (context change pooled 5069 vs 5073, Q-K-V 5059 vs 5050; switch pooled 5007 vs 5014, Q-K-V 4968 vs 4958).

**Selection (E1, generic held-out):** winner `dual + cross + sim / last / resid-ls` = **4828 / 5914 (81.6%)**, the best so far (run 7: 4771). **"mix" is worse than "last" for every feature set and head** (by 1–2 points), so drop it. `resid-ls` wins with `dual + cross + sim`, but not with `cross` alone.

**Tests**

| Test | Run 7 router | **3a router** | 3a hard cascade (Q-K-V) | 3a soft fusion (w = 1) |
|---|---|---|---|---|
| E2 banking benchmark | 41 / 50 | 39 / 50 | — | 35 / 50 |
| E3 all banking | 176 / 225 | 173 / 225 | 154 / 225 | 160 / 225 |
| E4 ding-dong per turn (live) | 17 / 25 | **21 / 25** (5/5 full) | 14 / 25 | 15 / 25 |
| E5 realistic (live) | 34 / 40 | 29 / 40 | 28 / 40 | 30 / 40 |
| E5, cross-only head | 33 / 40 | **35 / 40** | | |

| Detector (unseen tests) | Pooled | Q-K-V |
|---|---|---|
| E7 context change, realistic | 32 / 35 | 32 / 35 |
| E8 context change, banking turns | 14 / 18 | 14 / 18 |
| Agent switch, banking (180) | 141 (N kept 5/27) | 138 (N kept 9/27) |

**Soft fusion on generic held-out:** w = 0 → 4828, w = 0.5 → 5245, **w = 1 → 5251 (+7.1 points)**, w = 8 → 5199.

**E10 — realistic test set (193 live turns, 13 companies), added after the run in the same kernel**

| Turn type | Turns | Router | Cross only | Hard cascade | Soft fusion |
|---|---|---|---|---|---|
| start | 35 | 28 | 26 | 28 | 28 |
| answer | 51 | 37 | 35 | 30 | 37 |
| follow | 21 | 14 | 14 | 12 | 13 |
| aspect | 7 | 6 | 6 | 6 | 6 |
| closing | 15 | 9 | 8 | 8 | 8 |
| also_stay | 4 | 4 | 2 | 3 | 3 |
| switch | 42 | 30 | 30 | 21 | 25 |
| short_switch | 6 | 5 | 4 | 1 | 3 |
| return | 7 | 3 | 3 | 4 | 5 |
| handoff_ok | 2 | 0 | 0 | 0 | 0 |
| branch | 3 | 2 | 3 | 1 | 2 |
| **all** | **193** | **138 (71.5%)** | 131 | 114 | 130 |

- **The router alone is best on E10.** Both detector combinations lose, mostly on **switches**: the hard cascade gets 21 of 42 switches, soft fusion 25, the router 30.
- **Live errors compound.** One missed switch makes every following short answer and closing go to the wrong agent. In water-1, one miss led to 4 wrong turns in a row.
- **Even first messages miss 7 of 35.** Example: "book the spa on board" → Cruise Bookings. So the basic conversation-to-description match is the weak link, more than turn handling.

- **Key finding: better generic held-out scores do NOT transfer to the real-world tests.**
  - The winning head scored +57 on generic held-out but went down on banking and on the realistic conversations.
  - Soft fusion added +423 correct on generic held-out but lost on banking (−13) and on ding-dong (−6), and only +1 on realistic.
  - The template-based generic data rewards cues that real conversations don't have. On banking, the switch detector keeps only 5–9 of 27 "stay" cases.
  - Choosing models and weights on generic held-out data is therefore misleading, and the real test sets are too small to choose on without overfitting to them.
- **Q-K-V's out-of-domain edge from run 7 didn't hold this time:** it ties pooled on E7/E8 and is slightly worse on banking switch. Its run-7 advantage was within run-to-run noise.
- **Decision (proposed):**
  1. Drop the "mix" layer option.
  2. Add the realistic E10 set (193 turns, 13 companies) to every run.
  3. Split realistic data into a **dev** part (for choosing configurations and the fusion weight) and a **held-out test** part.
  4. Prioritise **roadmap D (free-form realistic training data)** over further head tweaks, because the bottleneck is the training data's realism, not the head.
  5. Run 3b (Nemotron) to see whether a retrieval-trained encoder transfers better.

---

## Run 9 — 2026-10-07: Phase 3b, Nemotron-1B router encoder (branch `exp/phase3b-nemotron`)

- **Encoder:** `nvidia/llama-nemotron-embed-1b-v2` (bidirectional Llama-3.2-1B, H = 2,048), library forward pass in fp16, `query:` / `passage:` prefixes, newline separators. Layer option "last" only (mix dropped after 3a). Same data as run 8.
- **Fix during the run:** the tokenizer also needs `trust_remote_code=True`. Without it, transformers silently waits for a confirmation (VS Code hid the prompt), then errors.
- **Speed:** 34,435 feature passes in 352 s (fp16 is faster than our fp32 ModernBERT-large: 761 s). Cell 45b took 330 s. RAM 6.6 GB, GPU 5.5 GB. The Q-K-V token-state training was slow, about 37 min for both labels (H = 2,048).

**Router: Nemotron vs ModernBERT-large (3a)**

| Test | 3a ModernBERT | **3b Nemotron** |
|---|---|---|
| E1 generic held-out (winner) | 4828 / 5914 (81.6%) | **5068 (85.7%)**, `dual + cross + sim / mlp-256` |
| E1, dual-only head | 3353 (56.7%) | **3916 (66.2%)** |
| E2 banking benchmark | 39 / 50 | **43 / 50** |
| E3 all banking | 173 / 225 | **193 / 225** (ties the best, run 3) |
| E4 ding-dong per turn / full | **21 / 25 · 5/5** | 16 / 25 · 3/5 |
| E5 realistic (Cell 59): router / cross / dual | 29 / 35 / 19 | **34 / 35 / 26** |
| **E10 realistic test (193 turns), router** | 138 (71.5%) | **154 (79.8%)** |
| **E10, cross-only head** | 131 | **158 (81.9%)**, best on E10 so far |
| E10, soft fusion / hard cascade | 130 / 114 | 155 / 135 |

E10 by turn type (3b: router · cross only · soft fusion): start 32·32·32/35; answer 39·**43**·41/51; follow 14·15·13/21; switch 33·32·**34**/42; closing 9·9·**12**/15; return **7**·6·6/7; short_switch **6**·6·5/6; handoff_ok 2·2·2/2.

**Y/N detectors: Nemotron is much worse than ModernBERT**

| Test | 3a ModernBERT (pooled) | 3b Nemotron (pooled / Q-K-V) |
|---|---|---|
| Context change, generic held-out | **5069 / 5212** | 4825 / 4799 |
| Context change, realistic (35) | **32** (Y 15/15) | 24 / 24 (Y only 4–5 of 15) |
| Context change, banking turns (18) | **14** | 7 / 11 |
| Agent switch, banking (180) | 141 (N kept 5/27) | **153** (N 14/27) / 146 |

- **Soft fusion:** generic held-out w = 1 → 5475 (+407 over the router). On real tests: realistic **37 / 40** (+3), ding-dong 17 (+1), banking 183 (−10), E10 155 (+1). Mixed again; it helps closings and switches but hurts banking.
- **Verdict:**
  - **Nemotron is the better ROUTER encoder:** +16 on E10, +20 on banking, +5 on realistic. Its retrieval training makes standalone (dual) embeddings useful (+10 points), and E10's first messages go from 28 to 32 of 35.
  - **ModernBERT is the better DETECTOR encoder.** Nemotron's topical embeddings miss dialogue structure: it found only 4 of 15 real switches on the realistic set. The ding-dong replay is also worse with Nemotron.
**Cell 70: one-sided "confident stay" gate** (stay only if p < τ, otherwise the router chooses among ALL agents). τ was chosen on 7 E10 companies (dev, 110 turns) and is reported on the other 6 (test, 83 turns). Run in the same 3b kernel.

| Detector | Dev, router alone 86/110 → best τ | **Test, router alone 68 / 83** |
|---|---|---|
| switch / pooled | 90 @ 0.1 | **70** |
| switch / Q-K-V | 89 @ 0.02 | 69 |
| change / pooled | 79 @ 0.02 (worse at every τ) | 68 |
| change / Q-K-V | **91** @ 0.02 | **70** |

On test, the gate gains on closings (3 → 5 of 5) and follow-ups (8 → 9 of 9), keeps switches at 15/20, and loses at most 1 short switch.

- **This is the first way of using the Y/N detector that does not hurt the router:** +2 of 83 on test (+4–5 on dev). The gain is small and within noise at this test size, but it is consistently in the right direction.
- **Why the gain is limited:** the router alone already handles most continuations. The remaining errors are missed switches (5 of 20) and short answers made wrong by an earlier mistake. A gate can only keep a correct current agent; it cannot repair a wrong one.

**E11: first-turn routing only (Cell 71, same 3b kernel)**: 100 single messages, 10 new companies × 5 agents (with close pairs), no history and no current agent.

| Type | Messages | Router top-1 | Router top-2 | Cross only |
|---|---|---|---|---|
| clear | 31 | 29 | 31 | 30 |
| short | 17 | 16 | 16 | 16 |
| indirect | 17 | 15 | 16 | 13 |
| close | 20 | 18 | 19 | 16 |
| noisy | 15 | 15 | 15 | 13 |
| **all** | **100** | **93** | **97** | 88 |

- **Matching a single message to agent descriptions is strong:** 93% top-1, 97% top-2, consistent with E10's first turns (32 of 35). Ranges per company: 8–10 of 10.
- **The 7 mistakes:** 2 indirect (fly-tipping → bulky waste, "error E21" → safety recalls), 1 short ("oven not heating", p = 0.40), 2 clear ("two tickets for 8pm" → refunds at p = 0.97; "brakes barely work" → docking stations), 2 close pairs (swap the booking day; accountant access → payroll at p = 0.99). Some errors are **confidently wrong**, so a confidence threshold alone will not catch them; top-2 at 97% favours "shortlist and confirm" designs.
- **Implication:** the router's weakness is the multi-turn dynamics (missed switches, errors propagating live), not the conversation-to-description matching. Design direction: route the first message with the router, keep the agent on later turns unless a reliable detector says the topic changed, and only then re-route (possibly as a top-2 shortlist).

- **Next:**
  1. Cell 70: a one-sided "confident stay" gate (stay only if p < τ, otherwise the router chooses among all agents), with τ chosen on an E10 dev split (7 companies) and reported on the other 6. Evaluation only, in the same kernel.
  2. A **hybrid run**: Nemotron router + ModernBERT detectors (both encoders already load in every run).
  3. Roadmap D: realistic training data.

---

**Collapse test (Cell 72, 3b kernel):** the conversation up to a turn joined into ONE continuous statement (no roles, no newlines, no separators) and routed as a first message. On 10 E10 turns the live router got wrong: **1 / 10** (all text) and **1 / 10** (user text only). Collapsing throws away order and recency. Example, water-1: three leak messages outweigh the later billing exchange, so "ok great" (thanking the bill recalculation) goes to Leaks at 0.99–1.00. Conclusion: recency matters, so test a **window**, not a collapse.

---

## Benchmark B1 — 2026-10-07: Strands decider 2B, zero-shot (branch `exp/benchmark-strands-decider`, `decider_benchmark.ipynb`)

- **Model:** `StrandsAgents/strands-decider-2B-hobson-v19`: Qwen3.5-2B-Base + LoRA + readout head, trained as a general "decision model" (choice / yes-no / score with calibrated confidence) on about 30 public classification datasets. Used **as published, no training on our data**. A `choice` question: "Which agent should handle the user's latest message?"; options = agent name → description; state = transcript + "Latest user message: …". No current-agent input: every turn is routed independently.
- **Kaggle notes:** remove Kaggle's preinstalled `torchao` 0.10 (the new peft rejects it); the main notebook's kernel held GPU 0, so the decider ran on **`cuda:1`** (second T4). It ran in bf16 (torch reports bf16 support on the T4), without the optional fast kernels (flash-linear-attention, causal-conv1d). About 0.28 s per decision.

| Test | Our router (run 9, Nemotron-1B + head) | **Strands decider 2B** |
|---|---|---|
| E11 first turn, top-1 (100) | 93 | **96** |
| E11 first turn, top-2 (100) | 97 | **100** |
| E10 chat history (193), full history | 154 (cross-only head: 158) | 151 |
| E10 chat history, **window of the last 3 user turns** | — (not tried) | **163** |
| Banking benchmark (50) | 43 | **48** |
| All banking (225) | 193 | **214** |

E10 by turn type (decider, full / window 3): answer 41 / 47 of 51; follow 18 / 21 of 21; switch 26 / 30 of 42; short_switch 2 / 3 of 6; return **6** / 3 of 7; closing 11 / 12 of 15.

- **Reading:**
  - The decider is ahead everywhere except E10 with full history, where it is level with our router (151 vs 154).
  - **Windowing helps it a lot** (+12 on E10), mainly on answers (+6), switches (+4) and follow-ups (+3). Returns get worse (6 → 3) because the earlier topic falls out of the window. This supports trying the same window on our router (roadmap 3.5).
  - **Caveat on banking:** the decider's training data includes **banking77** and **CLINC-OOS**, both banking/intent datasets. Its banking lead is not a clean zero-shot comparison. E10 and E11 are new to both models.
- **Scale context:** a 2B decoder-LLM backbone fine-tuned on many classification tasks, vs our frozen encoder (ModernBERT-large 0.4B / Nemotron 1.2B) plus a small head trained only on template data. On E10/E11, the new domains, the gap is 3 points top-1 on first turns and +9 on chat history (with its best window vs our unwindowed router).

---

## Run 10 — 2026-10-07: Phase 4, hybrid encoders: Nemotron router + ModernBERT detectors (branch `exp/phase4-encoder-combos`)

- **New:** `ROUTER_ENCODER` and `DETECTOR_ENCODER` are chosen independently in Cell 34b (any of the 4 ModernBERT / Nemotron combinations; caches are kept per encoder). This run used router = `nemotron-1b`, detectors and Q-K-V = `modernbert` (ModernBERT-large, our forward pass). Same data as runs 6–9.
- **Each half reproduces its source run exactly:**
  - router (5068 / 5914; banking 43 / 193; Cell 59 34 / 40; E10 154; E11 93 / 97) = run 9;
  - context-change detector (held-out 5069; realistic 32 / 35 with 15 / 15 switches found; banking turns 14 / 18) and agent-switch detector (5007) = run 8.
- **The hard cascade still hurts** (realistic 28 vs 34, banking 162 vs 193). ModernBERT's agent-switch detector keeps only 5 / 27 banking "stays". E10 (router / cross only / hard cascade / soft fusion): 154 / 158 / 117 / 155.

**One-sided "confident stay" gate (Cell 70), now with ModernBERT detectors.** τ was chosen on 7 dev companies (110 turns; router alone 86) and reported on 6 test companies (83 turns).

| Detector | Dev, best (τ) | **Test (router alone 68 / 83)** |
|---|---|---|
| switch / pooled | 91 (0.2) | 73 |
| switch / Q-K-V | 92 (0.02) | 73 |
| **change / pooled** | **88 at every τ** | **74** |
| change / Q-K-V | 88 (0.02) | 74 |

Test by turn type (router → change / pooled gate): answer 17 → 20 of 22; follow 8 → 9 of 9; closing 3 → 5 of 5; switch 15 → 15 of 20; short_switch 4 → 4 of 4; return 2 → 2 of 2.

- **Best result so far for chat history:** **+6 / 83 on unseen test companies** with no loss on switches (run 9's Nemotron-detector gate: +2). The pooled context-change detector gives the same dev score at every τ, so its test gain does not come from a lucky τ choice.
- **E10 total with the gate (dev 88 + test 74): 162 / 193**, against the Strands decider's best 163 (3-turn window) and its 151 with full history. The dev part is the set τ was chosen on, but for this detector τ makes no difference there.
- **Versus the decider:** level on realistic chat history; behind on first messages (E11 93 / 97 vs 96 / 100) and on banking (193 vs 214; the decider was trained on banking77 / CLINC).

**Like-for-like on the 6 E10 test companies (83 turns, the same turns in every column).** The decider was split the same way in `decider_benchmark.ipynb`, section 9.

| Turn type | Turns | Router alone | **Hybrid + gate** (change / pooled) | Decider, full | Decider, window 3 |
|---|---|---|---|---|---|
| start | 15 | 15 | 15 | 14 | 14 |
| answer | 22 | 17 | **20** | 17 | **20** |
| follow | 9 | 8 | **9** | 8 | **9** |
| aspect | 1 | 1 | 1 | 1 | 1 |
| closing | 5 | 3 | **5** | 4 | **5** |
| also_stay | 3 | 2 | 2 | **3** | **3** |
| switch | 20 | **15** | **15** | 10 | 13 |
| short_switch | 4 | **4** | **4** | 1 | 2 |
| return | 2 | 2 | 2 | 2 | 1 |
| branch | 2 | 1 | 1 | **2** | 1 |
| **all** | **83** | 68 | **74** | 62 | 69 |

- **On unseen test companies, our hybrid + gate beats the Strands decider: 74 vs 69** (62 with full history). The gate now matches the decider's best on staying put (answers 20, follow-ups 9, closings 5), and we keep our lead on topic changes (switches 15 vs 13, short switches 4 vs 2).
- **Q-K-V head, clarified:** it does compute Q = current-message tokens and K/V = history tokens. The keys are restricted by `key_padding_mask`, and only the current-message rows are pooled. But it is written as `attn(x, x, x)` and should be rewritten with explicit `x_current` / `x_hist`. Its limited gain is expected: `x_current` comes from a bidirectional encoder that has already read the history. A cleaner test encodes the current message alone.
- **Next:** (1) windowing on our router (the decider gained +12 from it); (2) rewrite the Q-K-V head explicitly, plus a "current message encoded alone" variant; (3) realistic training data.

---

## Run 10b — 2026-10-07: windowing test (Cell 73, branch `exp/phase5-windowing`, same hybrid kernel)

The router and the detector read only the last N user turns (plus the assistant reply before the first of them); the current agent is still passed. Windows were chosen on the 7 dev companies and reported on the 6 test companies (83 turns).

| Setup | Dev (110) | **Test (83)** |
|---|---|---|
| Router alone, full history | 86 | 68 |
| Router alone, N = 3 (best on dev; N = 1 / 2 / 5 → 83 / 86 / 86) | 88 | 68 |
| **Gate, no window** (run 10) | 88 | **74** |
| Gate, router all + detector N = 1 (best on dev of 20 pairs) | 89 | 71 |

- **Windowing does not help our system:** every difference is 1–3 turns, which is noise. The best dev choices do not carry over to test.
- **Why it helped the decider (+7 on the same turns) but not us:**
  1. We pass the current agent and an is-current flag, while the decider routes every turn blind.
  2. The gate already fixes the turns the window fixed for the decider: answers, follow-ups and closings.
  3. Our training conversations are short.
- **Decision:** no window. The best system stays Nemotron router + ModernBERT confident-stay gate on full history (74 / 83 vs decider 69). **Next: better and more training data (roadmap D).**
- **Bug note:** the first version of Cell 73 used `for d in …` and overwrote ModernBERT's global head size `d`. The loop now uses `dw`.

---

## Run 11 — 2026-10-07: Phase 6, realistic training data (branch `exp/phase6-realistic-train`, hybrid kernel)

- **New:** 744 free-form realistic training turns (40 businesses × 4 conversations, 5 agents each) added once to the 5,914 template conversations → 6,658 conversations, 67 domains. Same hybrid as run 10 (Nemotron router, ModernBERT detectors), same tests. E1 is now over 6,658 and is **not comparable** with earlier runs.
- **Confounder:** the router head chosen on held-out folds changed from `mlp-256` (run 10) to `resid-ls` (5722 vs 5688 for mlp-256 on held-out). The detectors also picked `mlp-256`.

| Test | Run 10 | **Run 11** | Decider (B1) |
|---|---|---|---|
| E1 generic held-out | 5068 / 5914 | 5722 / 6658 (not comparable) | — |
| Banking benchmark / all | 43 / 50 · 193 / 225 | 41 / 50 · 188 / 225 | 48 · 214 |
| Ding-dong per turn | 16 / 25 | 16 / 25 | — |
| Cell 59 (40 turns), router | 34 / 40 | 35 / 40 | — |
| E10 router alone (193) | 154 | **160** | 151 full / 163 window 3 |
| E10 cross only / hard cascade / soft fusion | 158 / 117 / 155 | 156 / 146 / **163** | — |
| E10 dev router alone (110) | 86 | **91** | — |
| E10 **test** router alone (83) | 68 | 69 | 62 / 69 |
| E10 **test, gate** change / pooled @ 0.02 | **74** | 70 | — |
| E10 test, gate (all four detectors) | 73 / 73 / 74 / 74 | 70 / 70 / 70 / 70 | — |
| E11 first turn: router / top-2 | 93 / 97 | 92 / 97 | 96 |
| Context-change detector: Cell 59 / banking turns | 32 / 35 · 14 / 18 | 31 / 35 · 12 / 18 | — |

E10 test by turn type, router alone → gate (run 10 in brackets): answer 19 → 19 (17 → 20); follow 8 → 8 (8 → 9); closing 4 → 5 (3 → 5); also_stay 3 → 3 (2 → 2); **switch 12 → 12 (15 → 15)**; short_switch 4 → 4; return 2 → 2; branch 1 → 1.

- **The router got better at staying put but worse at switching.** On the test companies, stay-type turns went up (answer +2, closing +1, also_stay +1), but real switches fell from 15 to 12 of 20. With fewer stay errors left to fix, the gate adds only +1 instead of +6.
- **The gain is on the dev companies, not on test:** router alone dev 86 → 91, test 68 → 69. Soft fusion now reaches 163 / 193 over all of E10, level with the decider's best, but that total includes the dev companies.
- **Small losses elsewhere:** banking −2 / −5, E11 −1, context-change detector −1 / −2.
- **Verdict by the agreed rule (≥ 2 / 83 on E10 test): not adopted.** The best E10 test result is still run 10's 74 / 83. Likely cause: the realistic data is heavy on same-agent turns (answers, closings: 348 N vs 236 Y) where the current agent is the answer, so the head leans more on "stay"; the head change (resid-ls) may add to it. These two causes are not separated by this run.
- **Decision:** the default stays run 10's (templates only, `REALISTIC_TRAIN=0`). The realistic data stays on this branch as an option; a later retry would add more switch-heavy realistic conversations and fix the router head to `mlp-256` to remove the confounder.

---

## Phase 7 — simplifying the architecture: what we removed and why (2026-10-08, branch `exp/phase7-simplify`)

*Written so it can be read on its own (for the blog). Numbers are absolute pass / total; the run numbers refer to entries above.*

**Why simplify now.** Over runs 1–11 the notebook grew one idea at a time: a second detector, three ways to combine detector and router, three feature sets, three head types, windowing. Every idea was tested honestly, but most of them never beat the simpler alternative, and keeping them had real costs:
- each Kaggle run trained 45 router heads and 6 detector heads (about 12 minutes) just to choose among options that always lost;
- letting the run choose its own head made runs hard to compare. In run 11 we changed the training data, and the selection also switched the router head (MLP-256 → residual head), so we could not tell which change caused the result;
- the notebook was harder to read and explain.

**The rule we use to decide.** Every option is tuned on the 7 *dev* companies of the realistic test set (E10) and judged on the 6 *test* companies (83 turns) it never saw. A component must beat the simpler alternative by at least 2 of those 83 turns to stay; on a tie the simpler or cheaper option wins.

**What we removed**

| Component | What it did | Evidence | Why removed |
|---|---|---|---|
| **Agent-switch detector** | A second yes/no model: "should a different agent answer this?" (target ≠ current). Added in Phase 1 because, after a handoff ("I'll pass you to billing" → "ok"), the topic does not change but the agent does | As the gate's detector: run 10, 73 / 83 vs 74 for the context-change detector; run 11, 70 vs 70 | Never better than the context-change detector, doubles detector training, and partly repeats the router's job |
| **Hard cascade** | The detector decides stay / switch; on "switch" the current agent is *excluded* and the router picks among the others | Run 6: below the router alone; run 10: realistic 28 vs 34, banking 162 vs 193, E10 117 vs 154; run 11: E10 146 vs 160 | Every wrong "switch" became a guaranteed routing error. The detector is only reliable in one direction (when it is sure nothing changed), and the cascade trusted it in both |
| **Soft fusion** | Router probabilities + w × detector evidence, w chosen on held-out training domains | Run 9: realistic +3 and E10 +1, but banking −10; run 11: best E10 total (163 / 193) | Mixed across test sets, and built on the switch detector. The one-sided "confident stay" gate does the useful part (fixing short replies) more simply: it can only *keep* the current agent, never exclude one |
| **Windowing** | Router and detector read only the last N user turns | Run 10b: router with N = 3 scored 68 / 83, the same as full history; the gate with windows scored 71 vs 74 without | No gain. (The Strands decider *did* gain from a window, +7 on the same turns; our router already weights the latest message through its last-message span) |
| **Collapse test** | Rewrite a conversation as one statement and route it as a first message | 1 / 10 of the router's E10 failures fixed | A one-off diagnostic, answered |
| **Cross-only, dual-only and summed-probability routers** | Heads that read only one of the two encoder passes, or average the two | Held-out (run 11): 5,280 / 4,349 / 5,498 vs 5,722 of 6,658 for the combined head; never selected in any run. Cross-only was +4 on E10 in run 10 but −4 in run 11, and −5 on first turns | The combined head (both passes + similarities) is better or equal everywhere that is stable |
| **"Router x2"** | Repeat the last user message in the input at test time | Earlier runs: hurt | Rejected before; the code was still there |
| **Per-run head selection** | Each run chose among MLP-64, MLP-256 and a residual head (and linear / MLP-64 / MLP-256 for the detector) | The choices differed by less than 1% held-out, but the switch in run 11 confounded the data comparison | Heads are now fixed: router MLP-256 (the run 10 head), detector MLP-256 (the run 11 winner). The other head types stay in the code for deliberate experiments |

**What we kept, and why**

| Component | Evidence |
|---|---|
| Nemotron-1B as the router encoder | +16 on E10 and +20 on banking over ModernBERT-large (run 9) |
| ModernBERT-large as the detector encoder | Nemotron's retrieval embeddings found only 4 of 15 real topic switches (run 9) |
| Router features: cross pass + dual pass + 3 similarities + is_current flag, MLP-256 head | Best on held-out data in every run |
| Context-change detector (pooled spans + feed-forward head) | Best gate detector on the test companies (run 10) |
| One-sided "confident stay" gate (stay only if p(change) < τ, τ chosen on dev) | The only combination that beat the router alone on unseen companies: 74 vs 68 (run 10) |
| Realistic training data (744 turns, 40 businesses) | User decision: more variety in phrasing than the templates; its measured effect is in run 12 below |

**Decisions still open (tested later, same rule)**
- **Q-K-V attention head for the detector.** Kept with the context-change label only, until it is rewritten with explicit inputs (current message = Q, history = K / V) and a version where the current message is encoded on its own.
- **Dual pass.** Kept for now (held-out +442, first turns +5, E10 mixed). The planned plain baseline (ModernBERT + pooling + feed-forward head only) will show its real value.

**The resulting system**
```text
ModernBERT-large → pooled spans → MLP-256 → p(change)
   p < τ  → keep the current agent (router not run)
   p ≥ τ  → Nemotron-1B (cross + dual passes) → matching features → MLP-256 → one agent
```

**Effect on cost (run 12):** router selection 78 s instead of 422 s; detector training 61 s instead of 278 s. The Q-K-V head (13 minutes) is now the largest training cost.

---

## Run 12 — 2026-10-08: Phase 7, simplified notebook + realistic training data (branch `exp/phase7-simplify`)

- **Setup:** the simplified notebook above; same data as run 11 (templates + 744 realistic turns, 6,658 conversations, 67 domains); router head fixed to MLP-256 (run 10's head), detector MLP-256. So run 12 differs from **run 10 only in the data**, and from **run 11 only in the router head**.
- **Reproducible:** the router's held-out score (5,688 / 6,658) and the pooled detector (5,570 / 5,796; realistic 31 / 35; banking turns 12 / 18) match run 11's MLP-256 rows exactly.

| Test | Run 10 (templates, MLP-256) | Run 11 (+ realistic, resid-ls) | **Run 12 (+ realistic, MLP-256)** | Decider (B1) |
|---|---|---|---|---|
| E1 generic held-out | 5068 / 5914 | 5722 / 6658 | 5688 / 6658 | — |
| Banking benchmark / all | 43 / 50 · 193 / 225 | 41 · 188 | 41 · 188 | 48 · 214 |
| Ding-dong per turn | 16 / 25 | 16 / 25 | 16 / 25 | — |
| Cell 59 (40 turns), live | 34 / 40 | 35 / 40 | **37 / 40** | — |
| E10 router alone, all (193) | 154 | **160** | 152 | 151 full / 163 window 3 |
| E10 dev router alone (110) | 86 | 91 | 86 | — |
| E10 **test** router alone (83) | 68 | 69 | 66 | 62 / 69 |
| E10 **test, gate** change / pooled | **74** | 70 | 70 | — |
| E10 test, gate change / Q-K-V | 74 | 70 | 70 | — |
| E11 first turn: top-1 / top-2 | 93 / 97 | 92 / 97 | 93 / 97 | 96 |
| Detector, pooled vs Q-K-V: Cell 59 turns | 32 / 35 | 31 · — | 31 vs **32** / 35 | — |
| Detector, pooled vs Q-K-V: banking turns | 14 / 18 | 12 · — | 12 vs **14** / 18 | — |
| Detector held-out, pooled vs Q-K-V | 5069 / 5914 | 5570 / 5796 | 5570 vs 5539 / 5796 | — |

E10 test by turn type, router alone → gate (run 10 in brackets): answer 17 → 19 (17 → 20); follow 8 → 8 (8 → 9); closing 3 → 5 (3 → 5); also_stay 3 → 3 (2 → 2); **switch 12 → 12 (15 → 15)**; short_switch 4 → 4; return 2 → 2; branch 1 → 1.

**What run 12 tells us**
- **The switch loss comes from the data, not the head.** With run 10's head back, real switches on the test companies are still 12 / 20 (run 10: 15). Banking (41 · 188) is also the same as run 11, so that loss is the data too.
- **The data helps on Cell 59** (37 / 40, the best so far) and leaves first turns unchanged (93).
- **The residual head suited the new data better on E10** (run 11: 160 vs 152 over all 193 turns, 69 vs 66 on the test companies), but the gate result is the same (70) with either head.
- **Q-K-V vs pooled:** a tie in the gate (70 = 70) and on dev (85 vs 86); slightly better on the two small detector tests (+1, +2), slightly worse on held-out (−31 of 5,796). Not enough to decide; the explicit rewrite is the proper test.
- **Against the decider on the 83 test turns:** gate 70 vs decider 62 (full history) / 69 (window 3). Still ahead, but the margin over its best fell from 5 to 1.
- **Decision:** keep the simplified notebook (same quality, much faster, and every run now changes one thing). Keep the realistic data (user decision, for variety), with the open issue that it costs about 3 test switches; the next data step is more realistic *switch* examples, especially switches that sound like follow-ups. Next experiment as planned: the Q-K-V rewrite.

---

## Run 13 — 2026-10-08: Q-K-V rewrite (joint vs separate) + switch-heavy realistic data (branch `exp/phase7b-qkv-switch`)

- **Setup:** run 12's simplified notebook; realistic data grown from 744 to 936 turns (50 businesses; +192 switch-heavy turns, many phrased like follow-ups, with "Also …" stay twins) → 6,850 conversations, 77 domains. Router and detector heads fixed (MLP-256), so the only router change from run 12 is the data. Q-K-V head rewritten with explicit inputs: x_current (Q) = the current message's tokens, x_hist (K, V) = history + current-agent tokens; two modes: **joint** (one pass over the whole conversation, equivalent to the old head) and **separate** (the current message encoded alone).
- **Leakage check (asked because the early results looked "too good"):** every test user message compared with the realistic training data (exact match, and any shared 5-word phrase). Banking, ding-dong and E11: no overlap beyond one-word replies ("ok", "yes"). E10: only short replies and loose shared wording. **Cell 59: one verbatim sentence**, "Can I get an invoice for my company?", written in part 6 (password manager, a different agent) and in training since run 11; reworded after this run. Caveat: the same author (Claude) wrote the training conversations and the E10 / E11 / Cell 59 tests, so a shared writing style may favour our model a little on those (not on banking, which improved the most).

| Test | Run 10 | Run 12 | **Run 13** | Decider (B1) |
|---|---|---|---|---|
| E1 generic held-out | 5068 / 5914 | 5688 / 6658 | 5884 / 6850 (not comparable) | — |
| Banking benchmark / all | 43 · 193 | 41 · 188 | **47 / 50 · 205 / 225** (best ever) | 48 · 214 |
| Ding-dong per turn | 16 / 25 | 16 / 25 | **19 / 25** | — |
| Cell 59 (40 turns), live | 34 | 37 | **38 / 40** | — |
| E10 router alone, all (193) | 154 | 152 | 156 | 151 / 163 |
| E10 dev router alone (110) | 86 | 86 | 88 | — |
| E10 **test** router alone (83) | 68 | 66 | 68 | 62 / 69 |
| E10 **test, gate** pooled / QKV joint / QKV separate | 74 / — / — | 70 / — / — | **70 / 70 / 70** | — |
| E10 test switches (router → gate) | 15 → 15 | 12 → 12 | 12 → 12 | 10 / 13 |
| E11 first turn top-1 / top-2 | 93 / 97 | 93 / 97 | 93 / **98** | 96 |
| Detector held-out: pooled / QKV joint / QKV separate | — | — | 5728 / 5677 / 5677 of 5948 | — |
| Detector, Cell 59 turns (35) | 32 | 31 | 31 / **33** / 31 | — |
| Detector, banking turns (18) | 14 | 12 | **13** / 10 / **13** | — |

**Findings**
1. **The switch data paid off on banking, not on E10.** Banking went from 41 / 188 to 47 / 205, now 1 / 9 behind the decider, which was trained on banking77 / CLINC. Handoff turns are 12 / 12 and hard negatives 26 / 26 on the benchmark. Ding-dong is 19 / 25 and Cell 59 38 / 40. But the E10 test companies are unchanged: gate 70 / 83, with switches still 12 / 20.
2. **Why E10 test switches fail: the router stays with the current agent.** Every failed switch we inspected went back to the agent that answered the previous turn:
   - snorkelling trip → Onboard Services (current), not Shore Excursions;
   - scaffolding left in the garden → Monitoring & Faults (current), not Installation;
   - "could it be the chicken recipe?" → Orders (current), not Nutrition;
   - "change next week's box to salmon" → Nutrition (current), not Orders;
   - "And my bill jumped …" → Leaks (current), not Billing.

   These are switches *into a closely related agent* in which the message still mentions the current topic (the leak, the trip, the dog food). The one-sided gate cannot fix them, because it can only *keep* the current agent.
3. **Q-K-V verdict: no gain in either mode.** All three detectors give 70 / 83 in the gate (dev 87 / 87 / 87). Held-out, pooled is best (5728 vs 5677 / 5677). On the small tests, joint wins Cell 59 (+2) but loses banking (−3), and separate ties pooled. **The attention weights are almost uniform**: for "55102", "afternoon" and "ok thanks", the top history tokens each get ≈ 1 / (number of history tokens), e.g. 0.04 over ~25 tokens, on function words. The head does not learn *where* to look; it behaves like average pooling with extra parameters. Encoding the current message alone (separate) did not change this. By the agreed rule (≥ 2 / 83 over pooled), **Q-K-V does not earn its place.** It also costs about 17 minutes per run (token passes + 2 × 5 folds).
4. **Against the decider on the 83 test turns:** 70 vs 62 / 69. Banking is now close (47 vs 48, 205 vs 214), and first turns 93 vs 96 (top-2 98).

**Recommended decisions (for the user to confirm)**
- **Drop the Q-K-V head** (both modes); pooled + feed-forward is the detector. This closes the last open detector question.
- **Keep the switch-heavy data** (big banking / ding-dong / Cell 59 gains, no loss elsewhere).
- **Next experiment: a "confident switch" rule, the mirror of the confident-stay gate.** If p(change) ≥ τ_high (chosen on dev), exclude the current agent and let the router choose among the others. The run 6 hard cascade failed because it acted at p ≥ 0.5 with the weaker switch detector; at a high threshold, and only on the side where the router is now wrong (sticky on real switches), it may fix the 8 failed test switches without new training. It can be tested in Cell 70 on the same kernel.

---

## Run 14 — 2026-10-08: confident switch, Q-K-V dropped, E12 zero-shot vs the decider (branch `exp/phase8-general-choice`)

- **Setup:** run 13's data and heads (one training sentence reworded, see run 13); Q-K-V cells removed; Cell 70 is now a two-sided gate on the pooled context-change detector; Cell 72 runs E12 zero-shot. `decider_benchmark.ipynb` was rerun from the top on the same branch, with section 10 (E12) added. Its routing numbers reproduce B1 exactly (E11 96, E10 163, banking 48 · 214).

**Routing**

| Test | Run 13 | **Run 14** | Decider |
|---|---|---|---|
| E1 held-out (6,850) | 5884 | 5845 | — |
| Banking benchmark / all | 47 · 205 | **43 · 198** | 48 · 214 |
| Ding-dong per turn | 19 / 25 | 20 / 25 | — |
| E10 router alone, all (193) | 156 | 157 | 151 full / 163 window 3 |
| E10 test, router alone (83) | 68 | 68 | 62 / 69 |
| E10 test, confident-stay gate | 70 | 70 | — |
| **E10 test, stay + confident switch** | — | **71** | — |
| E11 top-1 / top-2 | 93 / 98 | 93 / 97 | 96 / 100 |

- **Run-to-run variance is larger than our decision margin.** Runs 13 and 14 train the same router on the same data with the same settings, yet banking moved from 47 · 205 to 43 · 198. The cause is the final head's epoch count, which is the median of the five folds' best epochs: [38, 23, 2, 2, 8] → 8 epochs in run 13, and [32, 2, 2, 2, 8] → 2 epochs in run 14. The features are recomputed on the GPU each session, so small numeric differences change early stopping, and one fold flips. **Differences of a few banking conversations, or of 1–2 E10 test turns, between runs are within this noise.** This needs fixing before further comparisons (see decisions).
- **Confident switch:** dev chose τ_high = 0.99 (dev 91 vs 88 for stay only), and test went from 70 to **71** (fixed 4, broke 3). Real switches went from 11 / 20 to **15 / 20**, the first recovery since run 10. But it broke an "aspect" turn ("how much is the drinks package per day?" moved away from Onboard Services), a follow-up and a branch turn, each at p ≥ 0.99. The dev curve is jagged (τ_high 0.95: 86, 0.98: 90, 0.99: 91, 0.995: 85), which is another sign of noise. **+1 < the agreed +2: not adopted.**

**E12: grounded choice questions, the exact same 170 items for both models** (same file and commit; each model in its native presentation)

| E12 | Items | Ours, zero-shot | Decider |
|---|---|---|---|
| yes / no | 58 | 29 (chance level; answered "yes" 25 times vs 30 true) | **56** |
| choice | 59 | 39 | **56** |
| score: exact level / within 1 / mean error | 53 | 28 / 45 / 0.63 levels | **48 / 53 / 0.47** |
| **all** | 170 | **96** | **160** |
| question groups, all answers right | 11 | 4 | 10 |
| time per question (T4, warm) | | **63 ms** | 200 ms |

Per category, ours vs the decider: topic 4 vs 4 and routing 10 vs 13, close; tone 17 vs 28, detail 25 vs 33, fact 20 vs 36, intent 9 vs 21, urgency 5 vs 11 and compare 5 vs 12, far behind.

- **Our router does not read the question yet.** On the decider's own example ("Help! My payouts have been failing for 3 days!") it picks billing and payments correctly, but answers urgency "no", frustration "calm" and urgency level "low". Yes / no is at chance: the candidates "yes. <question>" and "no. <question>" differ by one word, and a head trained only to match messages with agent descriptions has nothing to tell them apart. Choice works where the options are topics or teams (topic, routing), and fails where the answer depends on reading a detail, comparing numbers or judging intensity.
- **This was expected for zero-shot.** The decider was trained on exactly these question types, and our model never saw one. It is the baseline for phase 8 steps 3–4 (a `question:` segment + choice training). The decider sets a high bar: 160 / 170.
- **Speed:** ours is about 3× faster per question (63 vs 200 ms). The decider ran in bfloat16 on the T4, which has no fast bfloat16 path, so its time may improve in float16.

**Recommended decisions**
1. **Stabilize training before any more comparisons.** Train the final router head for a fixed number of epochs, or average 3–5 seeds, so that the same data gives the same numbers. Then rerun once to measure the remaining noise. Our ≥ 2 / 83 rule only means something if a rerun moves by less than that.
2. **Confident switch: not adopted** (+1 on test, below the agreed +2). The code stays in Cell 70, so it gets one more fair try once training is stable.
3. **Phase 8 steps 3–4 are the real question for general choice:** add a `question:` segment and train on mixed grounded-choice data, keeping all routing data. The no-regression routing bar must be set **after** step 1 (a stable baseline).

---

## Run 16 — 2026-10-09: unified choice model (branch `exp/phase8b-unified-choice`)

- **Setup:** one model answers any choice question. The input is `query: <text or conversation> | current agent: X | question: <q> | candidate: <option>`. Training mixes routing (6,850, question "Which agent should handle the user's latest message?"), context change as a yes / no question (5,948) and 1,524 general grounded questions (repeated ×3): 14,322 examples, 49,872 pairs. The cross pass gains a question span, and the loss is masked listwise over 2–5 options. Router head fixed (MLP-256). Encoding: 62,766 Nemotron passes in 754 s.

**Routing (the no-regression check)**

| Test | Run 13 | Run 14 | **Run 16 (unified)** | Decider |
|---|---|---|---|---|
| E1 routing held-out (6,850) | 5884 | 5845 | **5900** | — |
| Banking benchmark / all | 47 · 205 | 43 · 198 | 44 · 195 | 48 · 214 |
| Ding-dong per turn | 19 | 20 | 18 / 25 | — |
| Cell 59 (40) | 38 | — | **39 / 40** | — |
| E10 router alone, all (193) | 156 | 157 | 157 | 151 / 163 |
| E10 test, router alone (83) | 68 | 68 | **71** (switches 16 / 20) | 62 / 69 |
| **E10 test, gate (pooled detector, stay)** | 70 | 70 | **73** | — |
| E10 test, gate (unified yes / no detector, stay) | — | — | 72 | — |
| E11 top-1 / top-2 | 93 / 98 | 93 / 97 | 92 / 97 | 96 / 100 |

- **Routing did not regress.** Every routing number is inside the run 13–14 noise band or above it. The test-company gate is 73 / 83, the best since run 10's 74, and the router alone gets 16 / 20 real switches without any confident-switch rule. Given the noise found in run 14 (banking 47 → 43 with identical settings), we can claim "no loss", not "a gain".
- **Unified context-change detector (the yes / no question to the same model):** test 72 vs 73 for the separate ModernBERT detector, dev 89 vs 91, held-out 5,324 vs 5,733 / 5,948. Close in the gate, clearly weaker on held-out data. Keeping one model would cost about 1 test turn.
- **Confident switch: drop it.** With the pooled detector it broke 5 turns and fixed 1 (73 → 69). With the unified detector it changed nothing. Over runs 14 and 16 it never cleared +2.

**E12: the exact same 170 questions**

| E12 | Items | Run 14 (zero-shot) | **Run 16 (trained)** | Decider |
|---|---|---|---|---|
| yes / no | 58 | 29 | 35 | 56 |
| choice | 59 | 39 | 44 | 56 |
| score: exact / within 1 / mean error | 53 | 28 / 45 / 0.63 | 34 / 48 / 0.54 | 48 / 53 / 0.47 |
| **all** | 170 | 96 | **113** | **160** |
| question groups all right | 11 | 4 | 3 | 10 |
| ms per question | | 63 | 59 | 200 |

- **+17 on E12, but still 47 behind the decider.** The model-card example now comes out right (billing 0.78; urgency yes 0.70; frustrated 0.69), and routing-style, urgency and tone questions improved.
- **Yes / no is biased to "no":** it answered "yes" 15 times out of 58, against 30 true. The training yes / no items were 335 yes / 508 no, and its mistakes are confident "no"s on clear yeses ("Is the customer asking for a price?" for a quote request: no, 0.96).
- **Compare and detail stay weak** (compare 6 / 12, detail 25 / 38, question groups 3 / 11). These questions need the options weighed *against each other* ("who scored highest?", "which day does the writer want?"), and our model scores each option on its own. The general questions held out by family scored only 45–53%, so the skill does not transfer to question families the model has not trained on. 1,524 items from 11 families is a small base next to the decider's training.

**Decisions to take**
1. **Keep the unified format.** Routing is not hurt, and it adds general questions at 59 ms each.
2. **Context-change detector:** the separate ModernBERT detector is still the better one (73 vs 72 in the gate; held-out 96% vs 90%). Simplicity (one model) against about 1 test turn: the user's call.
3. **Drop the confident switch.**
4. **Next for E12:** balance yes / no in the training data; widen the question families and add more items per family, especially compare / detail; then consider a listwise option-interaction layer (options attending to each other) for the comparison questions, which per-option scoring cannot express.

---

## Run 17 — 2026-10-10: two separate heads (route / choice), 9,113 balanced choice items (branch `exp/phase8c-separate-heads`)

- **Setup:** the same input format and frozen encoder for every question, but two heads that share no training data, folds, standardization or tests. The **route head** has 6,850 routing conversations; the **choice head** has 9,113 general questions (5,572 yes / no balanced 50 / 50, 2,832 choice, 709 score; 24 families). The context-change labels go to neither head; the gate keeps the ModernBERT detector. One fix was made during the run: Cell 60 used `FOLDS` as a list after it became one fold list per head (`FOLDS["route"]` now).

**Route head vs run 16's single shared head**

| Test | Run 16 (shared) | **Run 17 (route head)** | Decider |
|---|---|---|---|
| E1 routing held-out (6,850) | 5900 | **5960** (best so far) | — |
| Banking benchmark / all | 44 · 195 | 43 · 194 | 48 · 214 |
| Ding-dong per turn | 18 | 17 / 25 | — |
| Cell 59 (40) | 39 | 38 | — |
| E10 router alone, all (193) | 157 | 158 | 151 / 163 |
| E10 test, router alone (83) | 71 | 69 | 62 / 69 |
| **E10 test, gate (stay, pooled detector)** | 73 | **72** | — |
| E11 top-1 / top-2 | 92 / 97 | **94** / 97 | 96 / 100 |

Every difference is within the run-to-run noise found in run 14. **A separate route head neither helps nor hurts routing.**

**Choice head vs run 16 on E12 (the exact same 170 questions)**

| E12 | Run 14 (zero-shot) | Run 16 (shared head, 1,524 items) | **Run 17 (choice head, 9,113 items)** | Decider |
|---|---|---|---|---|
| yes / no (58) | 29 | 35 | **38** | 56 |
| choice (59) | 39 | 44 | 44 | 56 |
| score: exact / within 1 (53) | 28 / 45 | 34 / 48 | 32 / 49 | 48 / 53 |
| **all (170)** | 96 | 113 | **114** | **160** |
| question groups all right (11) | 4 | 3 | 4 | 10 |
| ms per question | 63 | 59 | 57 | 200 |

- **Six times the training data gave +1.** The yes / no bias is fixed: 24 "yes" answers against 30 true, where run 16 gave 15. But overall E12 is flat, and so is the held-out score on question families the head never saw: 54% yes / no, 54% choice, 44% score.
- **The limit is the frozen features, not the data or the head.** The questions the model misses need *reading*: which detail the text states ("Which main did the customer order?" → soup instead of fish), comparing numbers ("Who scored highest?" → Ana, the lowest), and noticing that the same text gets a different question (question groups 4 / 11). The encoder's pooled span vectors do not carry these answers, and a head on top of frozen vectors cannot create them. The decider is a 2B generative model trained on these question types.
- **Confident switch** again lost on test (72 → 69, broke 4, fixed 1). It is recorded as dropped.

**Conclusions**
1. **Separate heads are fine and cleaner**: the same quality as one shared head, and the two jobs stay independent. Keep them.
2. **Routing is the product:** E10 test 72 / 83 vs the decider's 62 / 69, E11 94 vs 96, about 3.5× faster per question.
3. **General choice with frozen features has plateaued at about 114 / 170.** Closing the gap to 160 needs the encoder to learn: fine-tune its top layers on the choice data (roadmap item 5), or use a model trained for reading (the decider itself, or a small generative model, item 7) for general questions.

---

## Run 18 — 2026-10-10: choice questions with LoRA fine-tuning + a scoring head (`choice_lora.ipynb`, branch `exp/phase9-choice-lora`)

- **Setup:** ModernBERT-large, with the original weights frozen and hand-written LoRA adapters (r 16, alpha 32) on all 112 attention and MLP linear layers: 7.2 M trainable parameters + a 0.26 M head, against 395 M frozen. One encoder pass per option (`user: <text> [SEP] question: <q> [SEP] candidate: <option>`), mean pooling, MLP head, listwise loss. Trained on 8,197 choice questions; dev = 916 questions on texts never used in training; 3 epochs. **Training took 9.0 minutes on one T4** (2.9 steps/s, peak 6.1 GB). Chat history and agent routing are not part of this notebook.
- **Dev:** 399 / 916 before training → 904 after epoch 1 → **912 / 916** (epoch 3, kept). The dev questions come from the same 24 families as training, so this mostly shows the model learns the families. E12 is the real test.

**E12: the exact same 170 questions as every earlier run and the decider**

| E12 | Run 14 (frozen, zero-shot) | Run 17 (frozen + choice head) | **Run 18 (LoRA + head)** | Decider 2B |
|---|---|---|---|---|
| yes / no (58) | 29 | 38 | **52** | 56 |
| choice (59) | 39 | 44 | **55** | 56 |
| score, exact level (53) | 28 | 32 | **46** | 48 |
| score within 1 level / mean error | 45 / 0.63 | 49 / 0.57 | **53 / 0.13** | 53 / 0.47 |
| **all (170)** | 96 | 114 | **153** | **160** |
| question groups all right (11) | 4 | 4 | **9** | 10 |
| ms per question (T4) | 63 | 57 | **49** | 200 |

- **Fine-tuning closes most of the gap: 114 → 153, within 7 of the decider, at about a quarter of its time per question.** The model now reads the text against the question. Comparisons 10 / 12 (was 5), details 37 / 38 (was 25), facts 34 / 37 (was 25), and 9 of 11 same-text question groups fully right (was 4). Yes / no is balanced: 30 "yes" answers against 30 true.
- **Score answers are never more than one level off** (53 / 53), with a mean error of 0.13 levels, better than the decider's 0.47.
- **What it still misses (17):**
  - intensity at the extremes of a scale: "furious" read as "frustrated" (3×), "very unhappy" as "unhappy";
  - counting: "two adults and three children" → four;
  - two routing-style choices: the decider's own model-card example "payouts failing" → sales instead of billing, and boiler → electrician;
  - a few confident yes / no slips, e.g. "Are the tickets for an evening show?" for 7:30pm → no (1.00).
- **Caveats.**
  - One seed and one run. The run-to-run noise of fine-tuning is not measured yet.
  - The same author (Claude) wrote the training generators and E12, so a shared style may favour our model a little. The decider saw neither.
  - The decider is general-purpose and was used zero-shot; ours was trained for exactly these three question types.

**Conclusion.** The plateau of runs 16–17 was the **frozen encoder**. With LoRA (7 M trainable parameters, 9 minutes of training) the same ModernBERT-large reaches 153 / 170 on general grounded choice questions, near a 2B generative decider, and about 4× faster.

**Next options:** a second seed to measure noise; statement-style options for yes / no; the same LoRA recipe for agent routing (E10 / E11 / banking) to see whether fine-tuning also lifts routing; latency at batch 1 against the decider (the planned benchmark).

---

## Run 19 — 2026-10-11: one LoRA model for routing + choice, ModernBERT-large vs Nemotron-1B (`lora_combined.ipynb`, branch `exp/phase9b-lora-combined`)

- **Setup:** one encoder with hand-written LoRA (r 16) + one scoring head, trained on routing (6,319 conversations with history, current agent and 5 described agents) and choice questions (8,176) together, in one question format, one pass per option. Dev: 7 unseen routing domains (531) + held-out choice texts (937). 2 epochs. The same data, settings and tests for both encoders.
- **Training:** ModernBERT-large 31.6 min (peak 9.8 GB; fp32 weights + fp16 autocast, no checkpointing); Nemotron-1B 67.8 min (peak 4.1 GB; fp16 weights, gradient checkpointing). Dev routing / choice: ModernBERT 525 / 531 and 934 / 937; Nemotron 526 / 531 and 932 / 937.

**Accuracy: the exact same test items as every earlier run and the decider**

| Test | **LoRA ModernBERT-large** | **LoRA Nemotron-1B** | Frozen system (run 17) | Choice-only LoRA (run 18) | Strands decider 2B |
|---|---|---|---|---|---|
| **E10 test companies, live (83)** | **75** | **79** | 69 router / 72 gate | — | 62 full / 69 window 3 |
| E10 all, live (193) | 174 | **180** | 158 | — | 151 / 163 |
| E10 real switches, test (20) | 16 | **19** | 14 | — | 10 / 13 |
| E11 first turn top-1 / top-2 (100) | 96 / 100 | **97** / 99 | 94 / 97 | — | 96 / 100 |
| Banking benchmark (50) | **49** | 48 | 43 | — | 48 |
| Banking all (225) | 212 | **217** | 194 | — | 214 |
| **E12 choice (170)** | **153** | 141 | 114 | 153 | **160** |
| E12 yes / no · choice · score | 55 · 55 · 43 | 51 · 54 · 36 | 38 · 44 · 32 | 52 · 55 · 46 | 56 · 56 · 48 |

**Latency per question** (T4, one question at a time, warm, tokenization included; ms)

| Test | LoRA ModernBERT-large p50 / p95 | LoRA Nemotron-1B p50 / p95 | Decider |
|---|---|---|---|
| E10 (3–4 agents, chat history) | 51 / 70 | 55 / 92 | 342 / 427 full · 277 / 349 window 3 |
| E11 (5 agents, one message) | 51 / 52 | 54 / 58 | 278 / 347 |
| Banking (5 agents, history) | 70 / 90 | 92 / 136 | 439 / 528 |
| E12 (2–5 options, short text) | 48 / 51 | 42 / 46 | 185 / 190 |

**Findings**
1. **Fine-tuning the encoder transforms routing.** Both LoRA models beat the frozen system everywhere, and they beat the decider on every routing test, without any gate or detector:
   - E10 test companies: **79 / 83** (Nemotron) and **75 / 83** (ModernBERT), against the decider's best of 69 and our previous best of 74;
   - real switches: 19 / 20 (Nemotron), the failure mode that runs 11–17 could not fix;
   - E10 all: 180 / 193 against 163;
   - banking: 217 / 225 against 214, though the decider was trained on banking data;
   - E11: 97 against 96.
2. **One model can do both jobs.** ModernBERT-large keeps its choice-only E12 score (153, the same as run 18) while also routing. So training routing and choice together cost nothing on choice.
3. **The two encoders have different strengths.** Nemotron is better at routing (+4 E10 test, +6 all, +5 banking), ModernBERT at choice questions (+12 E12, mainly score: 43 vs 36). Nemotron's choice mistakes are often confident misreadings of numbers ("45 cm" → over 2 m, 0.99), consistent with an embedding model pretrained for topical retrieval, not for detail.
4. **Speed:** about 50 ms per question on both, at least 4× faster than the decider (its E12 mean was 200 ms; section 11 will give its p50 / p95 on every test). Nemotron is faster on E12 because it runs in fp16, while ModernBERT ran fp32 weights under autocast. ModernBERT in fp16 should be faster still.
5. **Against the decider overall:** ahead on all routing tests; behind on general choice by 7 (ModernBERT) or 19 (Nemotron).

**Caveats**
- One seed per encoder; fine-tuning noise not yet measured.
- The same author (Claude) wrote the training data and the E10 / E11 / E12 / banking tests, so a shared style may favour our models. The decider saw none of it, and it was used zero-shot.
- The live E10 numbers use no confident-stay gate. The model's own previous pick is the current agent.

**E12 breakdown: where the fine-tuned models still trail the decider** (the exact same 170 questions; run 19 models vs the decider's section 10 run)

E12 has 170 short-text questions in three types: **yes / no** (58), **choice** among 2–5 unordered options (59) and **score**, a level on an ordered scale (53). Every answer can be read from the text.

| E12 type | LoRA ModernBERT-large | LoRA Nemotron-1B | Decider 2B | ModernBERT gap |
|---|---|---|---|---|
| yes / no (58) | 55 | 51 | 56 | −1 |
| choice (59) | 55 | 54 | 56 | −1 |
| **score (53)**, exact level | **43** | 36 | **48** | **−5** |
| score within 1 level | 53 | 50 | 53 | 0 |
| **all (170)** | **153** | 141 | **160** | **−7** |
| same-text question groups fully right (11) | 8 | 7 | 10 | −2 |
| "yes" answers given (30 true) | 31 | 29 | 30 | — |

| Category (all types) | LoRA ModernBERT-large | LoRA Nemotron-1B | Decider 2B | ModernBERT gap |
|---|---|---|---|---|
| **tone** (frustration, satisfaction) | 24 / 28 | 22 / 28 | 28 / 28 | **−4** |
| **compare** (numbers stated in the text) | 10 / 12 | 8 / 12 | 12 / 12 | −2 |
| routing-style ("which team / trade") | 12 / 14 | 11 / 14 | 13 / 14 | −1 |
| urgency | 10 / 13 | 8 / 13 | 11 / 13 | −1 |
| detail | 34 / 38 | 33 / 38 | 33 / 38 | +1 |
| fact | 36 / 37 | 32 / 37 | 36 / 37 | 0 |
| intent | 21 / 22 | 21 / 22 | 21 / 22 | 0 |
| topic · language | 4 / 4 · 2 / 2 | 4 / 4 · 2 / 2 | 4 / 4 · 2 / 2 | 0 |

**ModernBERT's 17 mistakes, by cause**
- **Score one level off (10).** Every score miss is an adjacent level. Two kinds:
  - **Scale ends (7):**
    - "SIX weeks and still no payout. I am DONE…" and "A WEEK late and nobody answers…" → frustrated (truth: furious);
    - "Dirty room, broken shower and no apology" → unhappy (very unhappy);
    - "Lovely stay, comfy bed and a great breakfast" → very happy (happy);
    - "Help! My payouts have been failing for 3 days!" → urgency medium (high);
    - "meeting room screens flicker sometimes; please check it this week" → low (medium);
    - "The hallway bulb has gone; replace it on your next visit" → medium (low).
  - **Stated facts into ranges (3):**
    - "We can fix it while you wait, about an hour" → within a week (same day);
    - "third floor" → above floor 5 (floors 1 to 5);
    - "jammed once last year" → sometimes (rarely).
- **Comparisons (2):**
  - "blue sofa £699, grey £749 — is the grey cheaper?" → yes (no);
  - "two adults and three children — more children than adults?" → no (yes).
- **Negated or absent details (2):**
  - "Main: the fish, **not** the steak" → main = soup (fish);
  - "Dessert: none" → soup (none).
- **Team / trade choice (2):**
  - "a demo of your software for my team of 40" → support (sales);
  - "boiler banging, no hot water" → electrician (plumber).
- **Yes / no (1):** changing the delivery **address** read as changing the delivery **day** → yes (no).

**The decider's 10 mistakes**
- yes / no: delivery address read as delivery day (the same item ours missed); "parcel left with my neighbour" → not delivered;
- choice: "can't do Thursday, keep Tuesday, or Friday at a push" → Friday; "charged twice for my last order" → Orders Agent; "two adults and three children" → four people;
- score: "whenever you have time… new font" → urgency medium (low); "small dinner for 12" → 50 to 100 (under 50); "£88 vs usually £90" → lower (about the same); "hallway bulb" → medium (low); "third floor" → ground floor.

**Nemotron's 29 mistakes** follow the same pattern, with more score misses (17), and several of them confident misreadings of numbers and units:
- "The bedside table is 45 cm wide" → over 2 m (0.99);
- "The van is 2.6 metres wide" → 1 to 2 m (0.98);
- "while you wait, about an hour" → more than a week;
- "The 8:20 arrives at 9:35, the 8:05 at 9:40 — which arrives first?" → the 8:05 (0.98).

This fits an embedding model pretrained for topical retrieval rather than for reading details. It is the better router (E10 test 79 vs 75) and the weaker reader of numbers.

**What this tells us.** The remaining gap to the decider is narrow and specific: **score precision** (5 of 7 points), mostly scale ends and turning stated numbers into ranges, plus a few comparisons and negations. Run 20 targets the score part with more ordered-scale training data. Comparisons and negated details are only 4 items, which one seed can move by noise alone.

**Next**
- ~~Decider latency~~ **measured 2026-10-11** (`decider_benchmark.ipynb` section 11; table above). Our LoRA models are **4–7× faster** at p50 and p95 on every test: E10 6.7×, banking 6.3×, E11 5.5×, E12 3.9× (ModernBERT vs the decider's full-history setting). Caveat: the decider ran in bfloat16 on a T4 (no native bfloat16) and without its optimized kernels (`causal_conv1d`, `flash-linear-attention` fell back to plain PyTorch), so its times are an upper bound. Our ModernBERT also ran fp32 weights under fp16 autocast. Cost scales differently: ours with the number of options (one pass each, batched), the decider's with prompt length (history + all options in one prompt). Its E12 accuracy reproduced exactly (160 / 170).
- A second seed for both encoders.
- ModernBERT in fp16 for speed.
- Choose the production pair: one model (ModernBERT: best balance), or Nemotron for routing and ModernBERT for choice.

---

## Run 20 — 2026-10-11: more score training data (709 → 2,004), ModernBERT-large only (branch `exp/phase9c-score-data`)

- **Setup:** identical to run 19's ModernBERT-large (same notebook, model, loss and settings). The only change is the choice training data: score items 709 → 2,004 (ranges with mixed units, graded intensity scales, 5-level ratings, frequency, deadline urgency, effort, size of a change), 10,408 choice items in total. Training 32.8 min; dev routing 525 / 531, dev choice 1,064 / 1,080.

| Test | Run 19 ModernBERT | **Run 20 ModernBERT (+ score data)** | Decider |
|---|---|---|---|
| E10 test companies (83) | 75 | **76** | 62 / 69 |
| E10 all (193) | 174 | 174 | 151 / 163 |
| E11 top-1 / top-2 | 96 / 100 | 96 / 100 | 96 / 100 |
| Banking 50 / 225 | 49 / 212 | 49 / 211 | 48 / 214 |
| **E12 all (170)** | 153 | **154** | 160 |
| E12 yes / no (58) | 55 | 54 | 56 |
| E12 choice (59) | 55 | **57** | 56 |
| **E12 score exact (53)** | **43** | **43** | **48** |
| E12 score within 1 level | 53 | 51 | 53 |
| E12 question groups (11) | 8 | 9 | 10 |
| Latency p50 E10 / E11 / banking / E12 (ms) | 51 / 51 / 70 / 48 | 50 / 50 / 71 / 48 | 342 / 278 / 439 / 185 |

- **More score data did not raise the score.** It stayed at 43 / 53, and within-one-level went *down* from 53 to 51. Every other number moved by 0–2, within the noise of a single seed. Choice rose to 57 / 59, one above the decider.
- **The mistakes moved around.**
  - **Fixed:** both "furious" items (scale ends), "happy / very happy" for one item, the boiler / plumber stays wrong, and "fish, not the steak" is now right.
  - **New mistakes:**
    - "The bedside table is 45 cm wide" → over 2 m (0.95);
    - "Noted. I'll check it tomorrow" → rude;
    - "The fridge is getting warm…" → high (truth medium);
    - "Help! My payouts have been failing for 3 days!" → urgency **low** (0.79, two levels off) and "Does this convey urgency?" → no (0.90).
- **Urgency got worse** (category 8 / 13, was 10 / 13). The likely cause is the new **deadline-urgency** training family: it teaches urgency from explicit deadline words ("within the next hour", "by Friday", "next month"). E12's urgency questions carry no deadline words; urgency there comes from severity ("payouts failing", "smoke from the fuse box", "fridge getting warm"). The model seems to have learned "no deadline word → low urgency". This is a shortcut that our own data introduced.
- **Some E12 score items are judgment calls between neighbours** (a flickering screen "this week" = medium; a hallway bulb "next visit" = low), and the decider misses some of the same ones (bulb, third floor). So part of the remaining gap is ambiguity, not reading.

**Note added before run 21.** A content-word check found generated training texts that were near-paraphrases of about 10 E12 items (see run 21's roadmap row), so E12 numbers from runs 16–20 may be slightly inflated. They were reworded for run 21.

**Conclusions**
1. More generated score data, on its own, is not the lever. It also showed how a template family can teach a shortcut (deadline words → urgency).
2. **Next (run 21):**
   - fix the urgency shortcut by adding severity-based urgency examples with no deadline words, so both cues are taught;
   - add the **order-aware score loss**: a small share of each target spread onto the neighbouring levels, plus a penalty on the distance between the predicted average level and the true one. Near-misses then cost less than far misses, and two-level errors like "payouts failing → low" are punished.
   - A second seed of run 20 would also show how much of the ±2 movement is noise.

---

## Run 21 — 2026-10-11: clean data + severity urgency; plain vs order-aware score loss (branch `exp/phase9d-score-loss`)

- **Setup:** ModernBERT-large, trained **twice on the same data and seed** (same notebook), once per score loss.
  - **Data (new for both):** training texts that were near-paraphrases of E12 items were reworded, and a content-word guard now blocks any such text. 192 severity-based urgency items were added. Choice training items: 9,586 (score 1,920).
  - **plain:** cross-entropy on the true level, as in runs 19–20.
  - **ordinal:** for score questions, 10% of the target goes to the neighbouring levels, plus 0.5 × \|expected level − true level\| / (levels − 1). Yes / no, choice and routing keep the plain loss.
  - Training 33 min each; dev routing 524 / 526 of 531, dev choice 994 / 995 of 1,014.

| Test | Run 19 | Run 20 | **Run 21 plain** (clean baseline) | **Run 21 ordinal** | Decider 2B |
|---|---|---|---|---|---|
| E10 test companies (83) | 75 | 76 | 77 | **81** | 62 / 69 |
| E10 real switches, test (20) | 16 | 17 | 17 | **20** | 10 / 13 |
| E10 all (193) | 174 | 174 | 175 | **180** | 151 / 163 |
| E11 top-1 / top-2 | 96 / 100 | 96 / 100 | 96 / 100 | 95 / 100 | 96 / 100 |
| Banking 50 / 225 | 49 / 212 | 49 / 211 | **50** / 216 | **50 / 220** | 48 / 214 |
| **E12 all (170)** | 153 | 154 | 155 | **161** | 160 |
| E12 yes / no (58) | 55 | 54 | 55 | **58** | 56 |
| E12 choice (59) | 55 | 57 | 54 | 56 | 56 |
| **E12 score exact (53)** | 43 | 43 | **46** | **47** | 48 |
| E12 score within 1 level | 53 | 51 | 53 | 53 | 53 |
| E12 question groups (11) | 8 | 9 | 10 | 10 | 10 |
| Latency p50 E10 / E11 / banking / E12 (ms) | 51 / 51 / 70 / 48 | 50 / 50 / 71 / 48 | 51 / 50 / 70 / 48 | 50 / 50 / 70 / 48 | 342 / 278 / 439 / 185 |

**Findings**
1. **The score gap is closed: 43 → 46 → 47, against the decider's 48.**
   - Most of the gain came with the **data change** (plain, 46). Clean data removed the E12 near-paraphrases, which can only remove help, so the severity-based urgency examples are the likely cause. Urgency rose to 10–11 / 13 from run 20's 8, and "Help! My payouts…" is no longer "low".
   - The **ordinal loss** added only +1 on score. Its main visible effect is that score answers keep within one level (53 / 53).
   - The rounded-expected-level rule gives 46 for both variants, so it is no better than taking the top level.
2. **Best results so far, all from the ordinal variant:** E12 **161 / 170** (decider 160); E10 test companies **81 / 83** with **all 20 real switches**; banking **50 / 50** and **220 / 225** (decider 48 / 214, and banking77 was in its training). All at ~50 ms per question.
3. **But part of the gap between the two variants is noise, and this run measures it.** The ordinal loss only changes score questions, yet routing moved too: E10 test 77 → 81, banking 216 → 220. It also lifted yes / no from 55 to 58, which the loss does not touch. The shared LoRA adapters see different gradients from the score batches, which changes the whole training path. So with one seed per variant, **differences of about ±4 on these tests are within run-to-run noise.** The run-to-run variance found in run 14 applies to fine-tuning too.
4. **Remaining mistakes (ordinal, 9):**
   - **score (6):**
     - "about an hour" → within a week;
     - "It doesn't work. What do I do?" → tried "a little";
     - hallway bulb → medium urgency;
     - "dirty room…" → unhappy (truth very unhappy);
     - "jammed once last year" → sometimes;
     - "payouts failing" → medium urgency;
   - **choice (3):** "charged twice for my last order" → Orders Agent (the decider makes the same mistake); "what time you open on bank holidays" → request for action; boiler → electrician (wrong in every run).

**Conclusions**
- On the same 170 E12 questions, our fine-tuned ModernBERT-large (7.2 M LoRA parameters, one model for routing + choice) **matches the decider on general choice questions** (161 vs 160; score 47 vs 48). It **leads on every routing test**, at about a quarter to a seventh of the decider's time per question.
- The headline claim must be "level with the decider on E12" rather than "better": +1 is far inside the measured noise.
- **Adopt the ordinal loss:** it is never worse on score, keeps every score answer within one level, and costs nothing. Keep the clean data and the guard.
- **Next:**
  - repeat both variants with 2 more seeds, to put error bars on every number before the blog's final table;
  - optionally, Nemotron with the ordinal loss (the stronger router).

---

## Run 22 — 2026-10-11: independent test set V1; our training collapsed, the decider's results stand (branch `exp/phase9e-independent`)

- **Setup:** the writer's V1 files, corrected in the converter (3 scales reordered, 8 non-scales retyped as choice; no answer changed; 22 claim checks flagged), giving 100 yes / no, 108 choice, 92 score, 40 conversations / 172 turns and 200 first messages. Ours: `lora_combined.ipynb`, ModernBERT-large, ordinal loss, the exact run 21 recipe. Decider: `decider_benchmark.ipynb` sections 1–3, 10, 12.

**Our training collapsed. These results are invalid and not used.**

| | Run 21 ordinal (healthy) | Run 22 (collapsed, same data and seed) |
|---|---|---|
| Dev routing / dev choice after epoch 2 | 526 / 995 | 497 / 599 |
| E12 | 161 | 88 |
| E10 test / E11 / banking 225 | 81 / 95 / 220 | 63 / 80 / 197 |

- **What happened:** the training code is unchanged from run 21 (only test blocks were added, and they run after training).
  - The **routing loss rose** from 1.49 to about 1.64 at steps 300–600, just after the warm-up ends and the learning rate peaks (step 262).
  - The **choice loss never fell below ~0.8** (about chance for 2–3 options); in healthy runs it reaches ~0.00x.

  The training became unstable at peak learning rate and never recovered on choice questions. GPU nondeterminism makes identical runs differ, and this time it tipped into collapse. It is **1 failure in 6 LoRA trainings** (runs 18–21 were all healthy).
- **Fix (for the rerun):** a collapse guard. After epoch 1, if dev routing < 95% or dev choice < 85% (healthy runs: ≥ 97.7% / ≥ 94.9%), training restarts from scratch with the next seed, up to 3 attempts, and every attempt is recorded in the results. The recipe itself is unchanged. *(The collapsed run's notebook printout was cleared by mistake while adding the guard; its numbers are recorded here.)*

**The decider on the independent set (valid):**

| Independent test | Decider 2B | Notes |
|---|---|---|
| Questions, all (300) | 253 | |
| … yes / no (100) | 77 | truth yes 28 / 50, truth no 49 / 50 |
| … claim checks (22, all truth "yes") | **0 / 22** | it answered "no" to every "does the text contradict the claim …" item |
| … yes / no without claim checks (78) | 77 | |
| … choice (108) | 106 | |
| … score (92) | 70 (within 1 level 90) | |
| Questions without flagged items (278) | 253 | |
| Routing, full history (172) | 113 | switch 18 / 46, short_switch 2 / 20 |
| Routing, 3-turn window (172) | 121 | switch 21 / 46, short_switch 6 / 20 |
| First turn top-1 / top-2 (200) | 178 / 193 | |
| Latency p50: questions · routing · first turn (ms) | 197 · 375 · 284 | |

- **Even on outside-written cases, the decider is weak at switches inside a conversation:** 2–6 of 20 short switches and 18–21 of 46 switches. That is the same pattern as on E10, so it was not an artefact of our own test writing.
- **The claim checks are hard for the decider** (0 / 22). Double-negation questions ("does the text contradict the claim 'Is X?'") are answered as if they asked "Is X?".

**Next:** rerun our side with the collapse guard (decider results are kept); then compare on the independent set.

---

## Run 22b — 2026-10-11: rerun with the collapse guard; the independent comparison (branch `exp/phase9e-independent`)

- **Training:** healthy on the first attempt (seed 42; dev after epoch 1: routing 97.6%, choice 95.0%), 32.6 min. **It reproduces run 21** closely: E10 test 80 (run 21: 81), E10 all 183 (180), E11 96 (95), banking 50 / 218 (50 / 220), E12 161 (161; yes / no 58, choice 56, score 47). This supports the ±4 noise estimate. Run 22's collapse was a random training failure.

**Independent test set (V1, corrected), the same cases for both models**

| Test | **Ours: ModernBERT-large + LoRA** | **Decider 2B** | Difference |
|---|---|---|---|
| Routing in conversations, live (172) | **131** | 113 full / 121 window 3 | **+10 to +18** |
| … correct previous agent given (172) | 140 | — (no current-agent input) | |
| … switches (46) · short switches (20) | **36 · 18** | 18 · 2 (full) / 21 · 6 (window 3) | |
| … stay-type turns live: answer, also_stay, aspect, return (55) | 37 | 48 / 49 | −11 to −12 |
| First message top-1 / top-2 (200) | **181** / 193 | 178 / 193 | +3 |
| Questions, all (300) | 231 | **253** | −22 |
| … yes / no (100) · without the 22 claim checks (78) | 74 · 74 | 77 · 77 | −3 (both 0 / 22 on claim checks) |
| … choice (108) | 104 | 106 | −2 |
| … **score (92)**: exact · within 1 level | **53** · 89 | **70** · 90 | **−17** · −1 |
| Latency p50, ms: questions · routing · first message | **49 · 68 · 51** | 197 · 375 · 284 | 4–5.5× faster |

**Findings**
1. **The routing advantage holds on outside-written conversations,** above all on switches: 18 / 20 short switches against 2–6, and 36 / 46 switches against 18–21. First-message routing is level.
2. **A weakness our own tests did not show:** on these conversations our model **switches too readily**. It gets 37 / 55 stay-type turns right live, against 48–49 for the decider. Given the correct previous agent, `answer` turns are 40 / 40, so part of the live loss is one wrong pick carrying over.
3. **Yes / no and choice are close to the decider** (−3, −2). Both models fail every claim-check item (double negation).
4. **Score parity on E12 does not hold independently: 53 vs 70 / 92**, although 89 / 92 are within one level (decider 90). E12's score items and our score training data share an author. On outside-written scales, our model's level precision is clearly lower. **This is the main remaining gap.**

**Overall (the claim for the blog):** at about one-fifth of the decider's size (395 M + 7.5 M trained vs about 2 B) and 4–5.5× faster per question, our model is **ahead on conversational routing, level on first-message routing, close on yes / no and choice, and behind on score questions.**

**Next options:**
- **Score precision on outside data:** more varied scale data written by a different author, or the independent writer's style as a template, with the guard against copying test items.
- **Over-switching:** more stay-type examples (answers, aspects, also-stay) in realistic conversations.
- **Error bars:** 2 more seeds.

*(Superseded on 2026-10-11 by the user's independence rule: the independent set is a final check only, and no training data is added or changed because of it. The first two options are therefore not pursued as described.)*

---

## Run 23 — 2026-10-11: Nemotron-1B with the final recipe, 3 epochs (branch `exp/phase9e-independent`)

- **Setup:** Nemotron-1B (`llama-nemotron-embed-1b-v2`) with LoRA (112 layers, 11.3 M) + head (0.52 M), ordinal score loss, collapse guard, the same training data as runs 21–22b (nothing from or inspired by the independent set), **3 epochs** (best epoch chosen on dev). Healthy on the first attempt: dev after epoch 1 was routing 97.9% / choice 92.0%; after epoch 3, 98.9% / 98.4% (best). Training 103.2 min, peak GPU 4.1 GB.

| Test (the same items for all) | **Nemotron-1B (run 23)** | **ModernBERT-large (run 22b)** | Decider 2B |
|---|---|---|---|
| E10 test companies (83) · all (193) | 79 · 182 | **80 · 183** | 62 / 69 · 151 / 163 |
| E11 first message (100) | **97** | 96 | 96 |
| Banking 50 / 225 | 47 / 207 | **50 / 218** | 48 / 214 |
| E12 (170): yes / no · choice · score | 149: 53 · 53 · 43 | **161: 58 · 56 · 47** | 160: 56 · 56 · 48 |
| **Independent** routing live · given previous agent (172) | **134** · **142** | 131 · 140 | 113 / 121 · — |
| Independent first message (200) | 181 (top-2 194) | 181 (top-2 193) | 178 (top-2 193) |
| Independent questions (300) | 200 | 231 | **253** |
| … yes / no (100) · choice (108) · score (92) | 69 · 97 · 34 | 74 · 104 · 53 | **77 · 106 · 70** |
| Parameters, frozen + trained | 1.2 B + 11.8 M | **395 M + 7.5 M** | ~2 B |
| Training time (T4) | 103 min | **33 min** | — |
| Latency p50: E10 · banking · IND routing · E12 · IND questions (ms) | 54 · 89 · 87 · 43 · 42 | 52 · 70 · 68 · 50 · 49 | 342 · 439 · 375 · 185 · 197 |

**Findings**
1. **Nemotron did not do better, even with 3 epochs.** Routing is a tie: independent +3 / +2 and E10 −1 are within noise, and banking −11 favours ModernBERT. Choice questions are clearly worse: independent −31, of which score −19 (34 vs 53); E12 −12.
2. **The pattern from run 19 holds:** Nemotron's retrieval pretraining handles topics well but is weaker at reading details and numbers (score 34 / 92 independent, though 91 / 92 are within one level).
3. **It costs 3× the parameters and 3× the training time,** and routing is slower (87 vs 68 ms p50 on independent conversations).

**Decision (recommended): ModernBERT-large + LoRA + head (run 22b) is the final model.** It ties Nemotron on routing, is clearly better on choice questions, and is about one-fifth the decider's size (Nemotron-1B would be more than half of it).

---

## Run 24 — 2026-10-11: two separate specialists vs one combined model (branch `exp/phase9e-independent`)

- **Setup:** `TRAIN_MODE = "separate"`, ModernBERT-large. Two models were trained independently from scratch, each with its own LoRA adapters and head, under the same recipe as the combined run 22b (ordinal loss, 2 epochs, seed 42, collapse guard, the same data). Both trained healthily on the first attempt:
  - **routing model:** 6,319 routing conversations only; 25.4 min; dev routing 98.3%, best epoch 1;
  - **questions model:** 9,586 questions only; 7.2 min; dev choice 97.6%, best epoch 2.

  Each was scored only on its own tests.

| Routing test | Routing only | **Combined (run 22b)** | Δ | Decider |
|---|---|---|---|---|
| E10 test companies (83) · all (193) | 77 · 179 | **80 · 183** | −3 · −4 | 62 / 69 · 151 / 163 |
| E11 first message (100) | **97** | 96 | +1 | 96 |
| Banking 50 / 225 | 48 / 210 | **50 / 218** | −2 / −8 | 48 / 214 |
| Independent routing live · given previous agent (172) | 131 · **143** | 131 · 140 | 0 · +3 | 113 / 121 · — |
| Independent first message (200) | 180 | **181** | −1 | 178 |

| Question test | Questions only | **Combined (run 22b)** | Δ | Decider |
|---|---|---|---|---|
| E12 (170) | 155 | **161** | −6 | 160 |
| … yes / no · choice · score | 57 · 53 · 45 | 58 · 56 · 47 | −1 · −3 · −2 | 56 · 56 · 48 |
| Independent questions (300) | 228 | **231** | −3 | 253 |
| … yes / no · choice · score | 74 · **105** · 49 | 74 · 104 · **53** | 0 · +1 · −4 | 77 · 106 · 70 |

Latency was the same as the combined model (49–71 ms p50).

**Findings**
1. **No interference.** Neither specialist beats the combined model by more than the ±4 noise on any test.
2. **A hint of mutual help:** the two largest differences, banking −8 and E12 −6, both favour the combined model. With one seed each this is not proven, but it points to the jobs helping each other: the routing data teaches the model about customer messages, and the question data teaches it to read details.
3. **The cost is the same:** two specialists take 25 + 7 = 32 min against 33 min for the combined model, and deploying them would mean two models instead of one.

**Decision: one model for both jobs (name: **Signpost**, chosen by the user on 2026-10-11).** Joint training does not pollute either job, and the combined model is at least as good as two specialists. Run 22b's combined ModernBERT-large stays the final model.

---

## Run 25 — 2026-10-11: train and export Signpost (branch `exp/phase9e-independent`)

- **Training:** the final recipe, combined. Healthy on the first attempt (dev after epoch 1: routing 98.1% / choice 95.8%; after epoch 2: 99.1% / 98.3%), 32.7 min.
- **Export:** 112 LoRA layers merged into the encoder. `signpost/` is 0.79 GB (fp16 safetensors, head, config, `signpost.py`); `signpost.zip` is 0.73 GB. **The reload check with `signpost.py` matched the trained model exactly**: E11 97 / 100 and E12 161 / 170, in fp16 and in fp32 (the CPU path).
- **Local copy:** `models/signpost/` (downloaded and extracted by the user; its `signpost_config.json` shows this run's scores, and its `signpost.py` matches the repo). `models/` is git-ignored, so the weights are never committed.

| Test | Run 25 (exported Signpost) | Run 22b | Run 21 | Decider |
|---|---|---|---|---|
| E10 test (83) · all (193) | 78 · 181 | 80 · 183 | 81 · 180 | 62 / 69 · 151 / 163 |
| E11 top-1 (100) | 97 | 96 | 95 | 96 |
| Banking 50 / 225 | 48 / 210 | 50 / 218 | 50 / 220 | 48 / 214 |
| E12 (170): yes / no · choice · score | 161: 58 · 58 · 45 | 161: 58 · 56 · 47 | 161: 58 · 56 · 47 | 160: 56 · 56 · 48 |
| Independent questions (300): yes / no · choice · score | 221: 75 · 103 · 43 | 231: 74 · 104 · 53 | — | 253: 77 · 106 · 70 |
| Independent routing live (172) · first message (200) | 133 · 180 | 131 · 181 | — | 113 / 121 · 178 |

- **Three runs of the same recipe** (21, 22b, 25) now give an error bar. Routing and E12 are steady within about ±4. Banking (210–220) and **independent score (43–53)** vary more. So the independent score gap to the decider (70) is 17–27 points, real whichever seed is used.
- **The exported model is the one used in Part 2** (LangGraph app). Its own numbers are the run 25 column.

---

## Signpost in LangGraph — 2026-10-11: real-setting test (branch `exp/signpost-langgraph`, `signpost_app/`)

- **App:** Northwind Outdoor Gear, a fictional outdoor retailer new to Signpost, with 5 agents (Orders & Delivery, Returns & Refunds, Product Advice, Repairs & Warranty, Billing & Membership).
  - **Graph:** START → `signpost` node (the exported Signpost from `models/signpost/`, CPU) → `Command(goto=agent)` → the agent answers with Claude Opus 5.5 (effort low, server-side refusal fallback) → END.
  - **State:** messages, current_agent, route.
  - **Memory:** `DynamoDBSaver` (table `signpost-checkpoints`, on-demand billing, 1-day expiry, created on first use, AWS SSO profile in ap-south-1), with the `agentstate-reducer` pruning the stored history inside every save (default above 12 messages, down to 6).
  - **Where it ran:** locally in Windows PowerShell with uv (inference only, user-approved).
- **Tests:** written for the app by the same author as the training data; Northwind and its agents are new to Signpost.

| Test | Routing-only run (stub replies) | **Full run (Claude agents)** |
|---|---|---|
| A. First messages (20, a new thread each) | 19 / 20 | **19 / 20** |
| B. Conversations (6, 32 turns, routed live) | 32 / 32 | **31 / 32** |
| C. Persistence (a new checkpointer resumes from DynamoDB) | 7 / 7, restore OK | **7 / 7, restore OK** (6 messages + current agent) |
| D. Long conversation, reducer window 8 / 4 (12 turns) | 9 / 12 | **10 / 12** (stored per turn 2,4,6,8,4,6,8,4,6,8,4,6) |
| Routing latency on CPU, p50 (first message / with history) | 0.9 s / 2–3 s | **1.3 s / ~4 s** (GPU: ~50–70 ms) |

**Findings**
- **Signpost routes correctly in a live LangGraph app:** 67 / 71 turns with real LLM replies in the history, across persistence and pruned history.
- **Misroutes recover by themselves.** The wrongly chosen agent answers "I'll pass you to …", and Signpost (trained on hand-offs) routes the next turn correctly. Example in D: "tent pegs missing" went to Repairs; Repairs handed over; "yes please send them" went to Orders.
- **The misses match the independent test's weak spot:**
  - a short answer with a product word pulls away from the current agent ("the second one was a £60 fleece", during a return → Product Advice, p 0.88);
  - "swap this jacket for a medium" → Product Advice;
  - two debatable labels ("can I use [points] on the repair?" → Repairs; "tent pegs missing from the box" → Repairs).
- **The stub-reply run was slightly flattering** (the stubs named the agent): 32 / 32 vs 31 / 32 on B. The real-reply run is the number to quote.
- **CPU latency (1–4 s) is the practical cost locally;** options are a shorter history window, fp16 on a small GPU, or tighter batching.

---

## Infrastructure notes

- **Kaggle gives 2 × T4, and the notebook uses only `cuda:0`** (noted 2026-10-07). Options to use the second GPU, in order of payoff vs effort:
  1. **Feature extraction across both GPUs** (the longest step: ~15 min for ModernBERT-large, more for Nemotron-1B). Split the texts in two, give each GPU its own copy of the encoder (ModernBERT-large ≈ 1.6 GB; Nemotron fp16 ≈ 2.5 GB), and run the halves in two threads. Expected ≈ 2× faster extraction.
  2. **Memory split for Nemotron-1B**: encoder on `cuda:1`, router heads, Q-K-V head and cached features on `cuda:0`.
  3. **Head selection in parallel**: train the leave-domains-out folds on both GPUs (two worker processes). Expected ≈ 2× faster for Cell 45b, at the cost of more complex code.

  Not started. Revisit when the extraction or selection time becomes the bottleneck (likely in 3b).

## Branches

Every experiment lives on its own branch, and nothing is merged into `master` until a path is chosen. Experiment branches are pushed to GitHub. The notebook's `DATA_BRANCH` (Cell 34) must name the branch whose data Kaggle should clone.

| Branch | Content | Based on |
|---|---|---|
| `exp/baseline-run5` | Run 5 state: router + context-change detector, with outputs | `master` (b7c1808) |
| `exp/phase1-cascade` | Phase 1: detector + router cascade, detector data fixes (run 6) | `exp/baseline-run5` |
| `exp/phase2b-qkv-attention` | Phase 2b: Q-K-V attention head for the detectors, cascade with it (run 7) | `exp/phase1-cascade` |
| `exp/phase3a-modernbert` | Phase 3a: pluggable encoder, layer mix, residual head, soft fusion; ModernBERT-large | `exp/phase2b-qkv-attention` |
| `exp/phase3b-nemotron` | Phase 3b: the same code with `ROUTER_ENCODER = "nemotron-1b"` | `exp/phase3a-modernbert` |
| `exp/phase4-encoder-combos` | Router and detector encoders chosen independently (`ROUTER_ENCODER`, `DETECTOR_ENCODER`): any of the 4 ModernBERT / Nemotron combinations; default = hybrid (Nemotron router + ModernBERT detectors) | `exp/phase3b-nemotron` |
| `exp/phase5-windowing` | Cell 73: windowing test (router / detector windows on dev, report on test). Result: no gain | `exp/phase4-encoder-combos` |
| `exp/phase6-realistic-train` | Realistic free-form training data (744 turns, 40 businesses), `REALISTIC_TRAIN` switch in Cell 34 (run 11). Result: not adopted (E10 test gate 70 vs 74) | `exp/phase5-windowing` |
| `exp/signpost-langgraph` | `signpost_app/`: LangGraph app with Signpost as the router, 5 Claude agents, DynamoDB checkpointer + agentstate-reducer; tests A–D (67 / 71 with Claude agents) | `exp/phase9e-independent` |
| `exp/phase9e-independent` | Run 22: independent test set (as delivered + flags), test blocks in `lora_combined.ipynb` and decider section 12 | `exp/phase9d-score-loss` |
| `exp/phase9d-score-loss` | Run 21: E12 near-paraphrase guard + reworded training texts, severity urgency, ordinal score loss (plain and ordinal variants in one notebook run) | `exp/phase9c-score-data` |
| `exp/phase9c-score-data` | Run 20: 2,004 score training items (from 709); `lora_combined.ipynb` with ModernBERT-large only | `exp/phase9b-lora-combined` |
| `exp/phase9b-lora-combined` | Run 19: `lora_combined.ipynb` (one LoRA model for routing + choice, ModernBERT-large and Nemotron-1B, accuracy + latency); decider latency section 11 | `exp/phase9-choice-lora` |
| `exp/phase9-choice-lora` | Phase 9: `choice_lora.ipynb`, choice questions only, LoRA fine-tuning of the encoder + scoring head | `exp/phase8c-separate-heads` |
| `exp/phase8c-separate-heads` | Run 17: separate route and choice heads (no shared data, folds, statistics or tests); 9,113 balanced general-choice training items | `exp/phase8b-unified-choice` |
| `exp/phase8b-unified-choice` | Run 16: one choice model (question segment, routing + context change + general questions, 2–5 options with masking); unified yes / no detector in the gate | `exp/phase8-general-choice` |
| `exp/phase8-general-choice` | Run 14: Q-K-V removed; two-sided gate (confident stay + confident switch) in Cell 70; E12 zero-shot cells (Cell 72 ours, decider section 10) | `exp/phase7b-qkv-switch` |
| `exp/phase7b-qkv-switch` | Run 13: Q-K-V head rewritten with explicit x_current (Q) / x_hist (K, V), two modes (joint = one pass, separate = current message encoded alone); gate compares pooled / joint / separate. Realistic data + 192 switch-heavy turns (936 total, 50 businesses). E12 test set (170 items) added | `exp/phase7-simplify` |
| `exp/phase7-simplify` | Simplified notebook (136 cells): one router config (`dual + cross + sim`, MLP-256), one detector label (context change, MLP-256; pooled + Q-K-V); cascade, soft fusion, switch detector, windowing and collapse test removed. Realistic training data on | `exp/phase6-realistic-train` |

Later phase branches are created when each phase starts, from the branch of the best result so far.

## Roadmap (agreed plan; update as phases finish)

| Phase | What | Pass criteria | Status |
|---|---|---|---|
| 0 | Ledger and fixed evaluation suite | this file exists; every run is logged | done |
| 1 | Cascade: detector N → stay with the current agent; Y → router picks among the other agents. Plus the detector data-gap fixes | E5 combined ≥ 36/40; E4 per turn ≥ 21/25; E7 ≥ 34/35; E8 ≥ 16/18; E6 no worse than 4300/4347 | **failed (run 6); closed**: the hard gate is worse than the router alone; removed in Phase 7 |
| 2 | Soft fusion instead of a hard cascade | — | **folded into Phase 3 (step 3.4)** |
| 2b | Learned Q-K-V cross-attention head (from `gemini-suggestions/ModernBERT Cross-Attention Router Model.py`), built on our own forward pass, not AutoModel. Token-level states are cached in fp16. First on the detector: the last-message tokens query the history tokens. Then on the router, as candidate-as-query over the conversation tokens, because a fixed `intent_head` cannot handle dynamic agents | detector: E7/E8 above Phase 1 at the same E6; router: E5 above the best | **done (run 7)**: better out-of-domain detection, the hard cascade is still below the router alone |
| 3 | **Same experiments, two encoders: 3a = ModernBERT-large (our forward pass), 3b = Nemotron-1B (library forward, user decision 2026-10-07).** 3.1 pluggable encoder (`ROUTER_ENCODER`, character-offset spans instead of `[SEP]` counting); 3.3 layer option last / mix (mean of the last 4 layers) and a residual head with label smoothing in the selection grid; 3.4 soft fusion (router + w × Q-K-V switch detector, w chosen on generic held-out folds). Local tests: ModernBERT-base and SmolLM2-135M (library code path) | 3a reproduces run 7 within noise; 3b vs 3a side by side on E1–E10 | **done (runs 8, 9)**: Nemotron is the better router, ModernBERT the better detector |
| 3.5 | **From `system_1_multi_agent_router_strategy_guide.md`, the next feature/data round (after 3a/3b):** (1) a **recent-window span** (the last 2 exchanges) next to the whole-conversation mean, aimed at the measured failure where the average is dominated by the first topic; (2) **agent-tagged history**: `assistant (Billing Agent): …`, so the input carries the conversation's agent trail; the builder records each speaker | E5 short-reply turns and E4 improve over the best run | proposed |
| 3c | **Pretrained reranker `BAAI/bge-reranker-v2-m3`**: (a) a zero-shot baseline that scores (conversation, agent description) with no training; (b) another encoder option behind `ROUTER_ENCODER` | E2/E3/E5 vs the trained routers | proposed |
| D | **Free-form, LLM-written conversations (written by Claude, not from templates)**: varied phrasing, realistic shifts, branching trajectories (the same last message needs different agents depending on history). First a **larger realistic TEST set** (≈150–200 conversations over several new companies with 3–5 broad agents), because 40 turns cannot separate close results; then training data, to replace the template phrasing that taught surface cues | the test set exists and is used as E10 in every run | proposed |
| 4 | Calibration: temperature scaling fitted on the validation folds, and the cascade threshold chosen there instead of a fixed 0.5. Confidence gate (entropy or top-1/top-2 margin) with coverage vs accuracy reporting; the fallback action decided with the user. Also a **Fallback / \"none of these\" candidate** for out-of-scope or ambiguous turns (from the System 1 guide) | a threshold that keeps ≥ 90% coverage at ≥ 95% accuracy | planned |
| 4b | k-NN memory for the detector (its Y/N labels do not depend on the domain): blend p_model with p_kNN from generic examples | E7/E8 improve | optional |
| 6 | Nemotron encoder swap | — | **moved into Phase 3 as 3b** |
| branch phase4 | Hybrid encoders: Nemotron router + ModernBERT detectors, confident-stay gate (τ on dev companies, reported on test companies) | gate beats router alone on E10 test | **done (run 10)**: 74 / 83 vs 68; beats the decider (62 / 69) |
| branch phase5 | Windowing (last N user turns) for the router and the detector | E10 test above 74 / 83 | **done (run 10b)**: no gain, no window |
| branch phase6 | Realistic free-form TRAINING data: 40 businesses × 4 conversations, 744 user turns, merged with the templates | E10 test / E11 / banking above run 10 | **done (run 11): not adopted** — E10 test gate 70 vs 74; router stays better, switches worse |
| decision 2026-10-07 | **Final architecture has one detector: context change (pooled features + feed-forward head).** The switch detector is dropped from the next run on. Decision rule for any challenger: settings chosen on dev companies, must beat the default by ≥ 2 / 83 on E10 test; on a tie the simpler option wins | — | agreed |
| branch phase7 | **Simplify** (user decision 2026-10-07): keep the realistic training data; remove the agent-switch detector, hard cascade (Cell 64), soft fusion (Cell 68), collapse test (Cell 72), windowing (Cell 73), the cross-only / dual-only / summed-probability configs and per-run head selection. Router fixed to `dual + cross + sim` + MLP-256; detector fixed to MLP-256. Kept for later decisions: Q-K-V (context change only) and the dual pass | E10 test gate vs run 10 (74) and run 11 (70); also separates run 11's head change (resid-ls) from the data change | **done (run 12)**: same gate result as run 11 (70 / 83), 5× faster selection; the switch loss is from the data, not the head |
| run 13 (next; user 2026-10-08) | **Q-K-V rewrite, proper test:** explicit `x_current` (Q) / `x_hist` (K, V) inputs instead of `attn(x, x, x)` + masks, plus a variant where the current message is encoded alone (the bidirectional encoder no longer leaks the history into Q). Context-change label only. Then decide Q-K-V vs pooled and freeze the design | Q-K-V gate ≥ pooled + 2 on E10 test | **done (run 13)**: no gain in either mode; attention ≈ uniform; recommended to drop |
| run 13, same branch (user 2026-10-08) | **More realistic SWITCH training data.** Run 12 showed the realistic data costs about 3 real switches on the E10 test companies (12 / 20 vs 15). Add realistic conversations rich in switches, especially switches that sound like follow-ups ("And is my inhaler prescription in that bag too?", "Also the installers left …"), returns and short switches, in new businesses (none from any test set). Runs together with the Q-K-V rewrite: the rewrite only changes the detector and is compared side by side with pooled in the same run, so the two effects stay separable | E10 test switches back to ≥ 15 / 20 with the gate ≥ 74 / 83; no loss on E11 / banking / Cell 59 | **done (run 13)**: banking 47 · 205, ding-dong 19, Cell 59 38; E10 test switches unchanged (12 / 20): failures are the router staying with the current agent |
| run 14 (user 2026-10-08) | **Phase 8 step 1–2 + confident switch, Q-K-V dropped** (branch `exp/phase8-general-choice`). (a) Q-K-V cells removed (user decision after run 13). (b) Cell 70: two-sided gate on the pooled context-change detector: p < τ_low → keep the current agent; p > τ_high → router among the OTHER agents (new "confident switch", aimed at the run 13 failures where the router stays with the current agent on a switch to a related agent); τ_low then τ_high chosen on dev companies, ties to "off". (c) Cell 72: E12 zero-shot with our router (text = user message, options = candidates described by the question); `decider_benchmark.ipynb` section 10: E12 with the decider in its native noul / choice / score questions. Same data as run 13 | test gate ≥ 72 / 83 with the confident switch (≥ 2 over the stay-only gate, 70); E12 per type vs the decider | **done (run 14)**: confident switch +1 (71 vs 70, not adopted); E12 zero-shot ours 96 / 170 vs decider 160 / 170; run-to-run variance found (banking 47 → 43 with identical settings) |
| run 16 (user 2026-10-08) | **Unified choice model** (branch `exp/phase8b-unified-choice`; stability work postponed by the user). Every example is (text, question, options): input `query: … current agent: … question: … candidate: …`. Training mixes routing (6,850, "Which agent should handle the user's latest message?"), the context-change label as a yes / no question (5,948) and 1,524 general grounded questions (`choice_train/items.json`: 843 yes / no, 452 choice, 229 score; 541 texts, 469 asked several questions; no 5-word phrase shared with E12), repeated ×3. Cross pass gains a question span; masked listwise loss over 2–5 options. Cell 70 compares the ModernBERT pooled detector with the unified model's own yes / no answer (each with dev-chosen confident stay / switch). Training code checked on CPU with random features (runs end to end; a planted label signal is learned) | routing within noise of run 14 (E10 test gate ~70, banking ~43–47 · 198–205, E11 ~93); E12 well above 96 / 170, towards the decider's 160 | **done (run 16)**: routing no loss (E10 test gate 73, held-out 5,900); E12 96 → 113 / 170 (decider 160); unified detector 72 vs pooled 73 |
| run 25 (user 2026-10-11) | **Train and export Signpost** (`lora_combined.ipynb`, `TRAIN_MODE = "combined"`, `EXPORT = 1`, same branch). The final recipe (ModernBERT-large, LoRA r 16, ordinal loss, 2 epochs, seed 42, collapse guard), retrained because earlier runs saved results but no weights; it doubles as a third seed of the final recipe. Export: the LoRA updates are merged into the encoder (W ← W + scale · B·A); `signpost/` = `encoder/` (fp16 safetensors + tokenizer), `head.pt`, `signpost_config.json`, `signpost.py` (standalone loader: `route`, `yes_no`, `choice`, `score`; the source is `signpost/signpost.py` in the repo); zipped to `signpost.zip`. The folder is reloaded with `signpost.py` and E11 / E12 are rescored in fp16 and fp32, which must match the trained model. Then part 2: a LangGraph app with 5 agents, Signpost as the router and the DynamoDB checkpointer + reducer, run locally (new branch) | export check matches; E-tests within noise of runs 21 / 22b | **done (run 25)**: exported, reload check exact (E11 97, E12 161 in fp16 and fp32); local copy in `models/signpost/` |
| run 24 (user 2026-10-11) | **Two separate specialists vs one combined model** (`lora_combined.ipynb`, `TRAIN_MODE = "separate"`, same branch `exp/phase9e-independent`). Question: does training routing and questions together in one LoRA model make either job worse (shared adapters pulling against each other)? Two ModernBERT-large models trained **independently from scratch**, each with its own adapters and head: a **routing model** (6,319 routing conversations only), scored on E10, E11, banking, independent routing and first messages; and a **questions model** (9,586 yes / no, choice, score questions only), scored on E12 and independent questions. Everything else matches the combined run 22b (LoRA r 16, ordinal loss, 2 epochs, seed 42, collapse guard, same data); each is compared with run 22b and the decider. If the specialists win by more than ~±4, the product becomes two models (user: "then we will need two names") | specialist vs combined run 22b on its own tests | **done (run 24)**: no interference — specialists are not better (routing E10 test 77 vs 80, banking 210 vs 218; questions E12 155 vs 161, independent 228 vs 231) → **one combined model stays** |
| run 23 (user 2026-10-11) | **Nemotron-1B with the final recipe** (`lora_combined.ipynb`, same branch `exp/phase9e-independent`): LoRA + head, ordinal score loss, collapse guard, the same training data as runs 21–22b, **3 epochs** (was 2; best epoch chosen on dev). Run 19 showed Nemotron is the stronger router (E10 test 79 vs 75) but weaker on choice (E12 141 vs 153); this run tests it with the final recipe on all tests including the independent set. **Independence rule (user, 2026-10-11): the independent test set is a final check only — no training data may be added, changed or modelled on anything learned from it** (the score / over-switching ideas noted after run 22b are therefore not pursued with data from or inspired by it) | vs ModernBERT-large run 22b and the decider on every test, independent set included | **done (run 23)**: routing tie with ModernBERT (IND 134 vs 131, E10 test 79 vs 80), choice clearly worse (IND questions 200 vs 231, score 34 vs 53), 3× size and training time → **ModernBERT-large stays the final model** |
| run 22 (user 2026-10-11) | **Independent test set** (branch `exp/phase9e-independent`): 3 files written outside the project from `experiments/independent_test_brief.md`, stored unchanged in `data/modernbert_router/independent/` and converted by `build_independent_test_data.py`. **Validation of the first delivery:** all lines valid, every answer among its options, no excluded business. But the cases are largely template-made. `questions.jsonl`: only 20 distinct texts for 300 questions; 81 / 100 choice questions are one wording ("Which exact number is explicitly stated…"); yes / no is 26 yes / 74 no. `routing.jsonl`: 26 distinct user messages in 160 turns; all 40 first messages are "I need help with a … at your <company>" (no need stated → flagged `vague_start`); 20 turns contradict their type, e.g. `also_stay` but the agent changes (flagged `label_conflict`). `first_turn.jsonl`: good (200 distinct). **Nothing is dropped:** flagged turns are reported separately; routing is scored live and with the correct previous agent given; yes / no is split by truth. Our side: `lora_combined.ipynb` (ModernBERT-large, ordinal loss), evaluated in the same run. Decider: `decider_benchmark.ipynb` section 12. A revision request (template limits, label rules and a self-check script) was added to the brief for the test writer | an outside check of runs 19–21; the revised files will replace these when they arrive **V1 (2026-10-11, used from now on):** passes the brief's self-check. 150 distinct texts (each ≤ 2 uses), 290 question wordings (max 6), yes / no 50 / 50; routing 172 unique messages, informative first messages, 0 type contradictions (1 `handoff_ok` turn mis-tagged, flagged), 123 distinct assistant replies; first turn unchanged; only generic 5-word overlaps with our training data (3) and E12 (1). **New question flags:** `claim_check` (22 yes / no "does the text contradict the claim …" items, **all** answering "yes", so passable by pattern) and `unordered_scale` (11 "score" items whose options are not one low → high scale, e.g. ["copper", "brass", "same amount"] or reversed ["matches", "partly matches", "does not match"]). Reported with and without flagged items. **Corrections applied in the converter (user-approved, 2026-10-11; the delivered files are unchanged and no answer was changed):** the 11 `unordered_scale` items were fixed instead of flagged, 3 reversed scales reordered low → high (q208, q230, q270) and 8 non-scales retyped `score` → `choice` (q218, q242, q260, q262, q280, q286, q292, q294), so the types are now 100 yes / no, 108 choice, 92 score. The 22 claim checks were **not** edited (user agreed): balancing them would mean rewriting claims (new content by the training-data author), so they stay flagged and are reported separately. First delivery kept as `*_v0.jsonl` | an outside check of runs 19–21 | **done (runs 22 + 22b)**: ours vs decider on independent V1: routing 131 vs 113 / 121, first turn 181 vs 178, questions 231 vs 253 (score 53 vs 70) |
| run 21 (user 2026-10-11) | **Order-aware score loss, plain vs ordinal on the same clean data** (`lora_combined.ipynb`, branch `exp/phase9d-score-loss`, ModernBERT-large trained twice, same seed). (1) **Data clean-up (user: "ensure the training cases are not teaching the specific test cases").** A new content-word check found generated training texts that were near-paraphrases of E12 items, e.g. "The food was cold and we waited over an hour" vs E12 "Food was cold … we waited an hour"; "Stop wasting my time and fix it" vs "… stop wasting my time"; the day template "Let's keep Friday. Tuesday and Thursday are both busy" vs "… let's keep Tuesday, or Friday at a push"; the effort steps "followed the online guide … reinstalled the app"; "About the printer" frequency texts. All were reworded or re-themed, and the builder now **fails** if any training text shares ≥ 3 content words and ≥ 60% of the smaller text's content words with an E12 text (on top of the 5-word-phrase check). These overlaps touched about 10 E12 items, so **E12 scores of runs 16–20 may be slightly inflated**; run 21's plain variant is the clean baseline. (2) **Urgency from severity** (192 items, no deadline words, scenarios unlike E12's) against run 20's deadline-word shortcut. (3) **Ordinal loss** for score questions: 10% of the target on the neighbouring levels + 0.5 × \|expected − true level\| / (levels − 1); E12 also reports score with the rounded expected level. Choice items 10,600 (score 2,148) | ordinal > plain on E12 score (plain is the clean reference); routing and yes / no unchanged within noise | **done (run 21)**: plain (clean baseline) E12 155, score 46; **ordinal E12 161** (decider 160), score 47 (48), E10 test 81 / 83, banking 50 · 220; ±4 between variants is within noise |
| run 20 (user 2026-10-11) | **More score training data, ModernBERT-large only** (`lora_combined.ipynb`, branch `exp/phase9c-score-data`). Run 19's score answers were always within one level but often one level off (ModernBERT 43 / 53 exact; decider 48): scale ends ("furious" read as "frustrated") and stated numbers into ranges ("about an hour" → "within a week"). Score items 709 → **2,004**: ranges with mixed units (length, weight, distance, duration, price, temperature, age, speed, headcount, fullness), graded intensity scales (worry, excitement, anger, confidence, difficulty, severity), 5-level ratings, frequency, deadline urgency, effort tried, size of a change; most dimensions are not in E12, and no text shares a 5-word phrase with E12. Total choice items 10,408. The only change from run 19 is the data (same model, loss, settings); an order-aware loss is kept for a later run | E12 score above 43 / 53 (run 19) towards the decider's 48, with E12 yes / no, choice and all routing tests unchanged within noise | **done (run 20)**: score unchanged (43 / 53; within 1 level 53 → 51); E12 154, choice 57; urgency worse (deadline-word shortcut); routing unchanged |
| run 19 (user 2026-10-10) | **One LoRA model for routing AND choice questions, ModernBERT-large then Nemotron-1B in one notebook** (`lora_combined.ipynb`, branch `exp/phase9b-lora-combined`). One encoder with hand-written LoRA + one scoring head, trained on routing (6,850 conversations with history and current agent, 5 agents with descriptions) and the 9,113 choice questions together, in the same question format; dev = 10% of routing domains + 10% of choice texts; 2 epochs. Tests: E10 live (all / 83 test-company turns), E11, banking, E12. **Latency** p50 / p95 / mean per question for every test, on both models; `decider_benchmark.ipynb` section 11 measures the decider the same way | routing ≥ the frozen system (E10 test 69 router alone, E11 94, banking 43 / 194); E12 ≈ run 18 (153); latency below the decider's | **done (run 19)**: E10 test 75 (ModernBERT) / **79** (Nemotron) vs decider 69; banking 212 / 217 vs 214; E11 96 / 97 vs 96; E12 153 / 141 vs 160; ~50 ms / question |
| phase 9 / run 18 (user 2026-10-10) | **Choice only: encoder fine-tuned with LoRA + a scoring head** (new notebook `choice_lora.ipynb`, branch `exp/phase9-choice-lora`; chat history and agent routing set aside for now). Run 17 showed that frozen features plateau on E12 (114 / 170 with 6× data). Here ModernBERT-large (default; `CHOICE_ENCODER` can pick Nemotron-1B) gets hand-written LoRA adapters (r 16) on every attention and MLP linear layer; one encoder pass per option (cross-encoder), mean pooling, MLP head, listwise loss over 2–5 options. Trained on the 9,113 choice questions with 10% of the *texts* held back as dev for early stopping; E12 only at the end | E12 well above 114 / 170, towards the decider's 160; ms per question reported | **done (run 18)**: E12 **153 / 170** (run 17: 114; decider: 160), 49 ms / question, 9 min training |
| run 17 (user 2026-10-09) | **Two separate heads, never mixed** (branch `exp/phase8c-separate-heads`). Same input format and frozen encoder for every question, but a **route head** trained, folded, standardized and tested only on routing (6,850 conversations; E10 + gate, E11, banking, Cell 59) and a **choice head** trained, folded, standardized and tested only on general questions (E12). Context-change labels go to neither head (the gate keeps the ModernBERT detector). **More choice training data:** 9,113 items (5,572 yes / no, 2,832 choice, 709 score) from 24 question families and 2,330 texts (2,192 asked several questions); yes / no balanced 50 / 50 within every family; no 5-word phrase shared with E12. Compared with run 16's single shared head | route head vs run 16 on routing (within noise or better); choice head vs run 16's 113 / 170 and the decider's 160 / 170 on E12 | **done (run 17)**: route head = shared head on routing (gate 72, held-out 5,960, E11 94); choice head E12 114 / 170 (run 16: 113) — frozen features plateau |
| phase8 (user 2026-10-08) | **General choice model, as an AUGMENTATION of the router: can the same model keep its agent-routing performance while also answering grounded choice questions, and how does it compare with the Strands decider?** Nothing learned so far is dropped: all routing data stays in training. (1) **E12 test set:** about 100 grounded items (the answer is in the given text; no world knowledge, as with the decider), covering the decider's three question types: yes / no ("Does this convey urgency?"), choice ("Which team should handle this?") and score on an ordered scale ("How frustrated is the writer? calm / frustrated / depressed"), including pairs where the same text gets two questions with different answers (does the model read the question?). (2) Both models zero-shot on E12 first. (3) Input format: `question:` segment added, `candidate agent:` → `candidate:`; routing becomes one task among several. (4) Train on routing + mixed grounded-choice data (task types and wording disjoint from E12). (5) Side-by-side vs the decider on E12 per type, then latency | **Routing must not regress** vs run 13 (E10 test gate within 1 turn, E11 within 1, banking within 2 / 5, Cell 59 within 1); E12 reported per type next to the decider | **in progress**: E12 built; zero-shot (run 14: 96 / 170), one shared head (run 16: 113 / 170), separate heads (run 17) |
| base (user request 2026-10-07) | **Absolute baseline: plain ModernBERT-large + pooling + feed-forward head, nothing else.** One cross pass over (conversation + candidate agent), mean-pooled over the whole input, one MLP head scoring each candidate; the highest score wins. No Nemotron, no dual pass, no span features, no similarities, no current-agent flag, no detector, no gate, no windowing. Same training data as the run it is compared with; same tests as the decider (E10 dev / test, E11, banking 50 / 225). Two rows: **base-0** exactly as above; **base-0 + current agent** = the same model with the current-agent flag added as one extra input, so its effect is measured on its own. Every extra component (hybrid encoders, detector, gate, Q-K-V) must justify itself against this baseline AND the decider | report side by side with B1 (decider) and the current best | **to do** |
| latency (user request 2026-10-07; after the architecture is frozen) | **Latency benchmark vs the decider.** Same T4, one GPU each, batch size 1, warm-up excluded, timing includes tokenization; p50 / p95 / mean ms per user turn over the E10 turns (realistic chat lengths) and E11 first turns. Ours timed per path: **stay** (detector only, router skipped) and **route** (detector + router over every candidate agent), plus the blended per-turn cost at the real stay rate on E10. Also: time vs number of agents (3 / 5 / 10) and vs conversation length, peak GPU memory, and the decider with full history vs window 3 | reported side by side with accuracy, so the trade-off is visible | **after freeze** |
| 7 | Optional: a **small generative router** (e.g. Qwen2.5-0.5B-Instruct + LoRA, outputs the agent name) as a different-paradigm comparison (System 1 guide, strategy C) | vs the best encoder router on E2–E5, E10 | optional |
| — | Rejected for now: target-only second pass / TTA (it removes exactly the history that short replies need; "router x2" already hurt); scaling the attention α inside the frozen encoder (a distribution shift for a frozen backbone); history KV caching for the encoder (only an approximation, because history tokens attend to the new turn); ONNX / Triton / CUDA graphs (latency work, not accuracy) | — | — |
| 5 | Optional: partial fine-tuning of the top 2–4 ModernBERT layers with differential learning rates (fp16 on the T4) | E1/E2/E3 clearly above the frozen best | optional |

## Signpost published on Hugging Face — 2026-10-11

- **Repo:** [huggingface.co/skamalj/signpost](https://huggingface.co/skamalj/signpost), public, Apache-2.0. Files: `encoder/` (merged ModernBERT-large, fp16), `head.pt`, `signpost_config.json`, `signpost.py`, `README.md` (model card), `card_examples.py`.
- **Source:** the run 25 export (`models/signpost/`). The training state is preserved as git tag `signpost-v1.0` (148608a, branch `exp/phase9e-independent`). The card is `signpost/README.md` on `exp/signpost-langgraph`.
- **Card examples verified twice:** run on the local export, then again on a fresh `snapshot_download` from the Hub (CPU, fp32). The outputs were identical, and they are the ones recorded in the card: routing (first message; a stay and a switch with history), choice, yes / no, score.
- **The card's evaluation** gives correct / total for both models on identical items, with the decider on full history. Its 3-turn-window results are given as a note.

## 03 restructure — 2026-10-17: `03_lora_signpost.ipynb` rebuilt, LoRA via `peft`, rerun with the Signpost recipe (branch `signpost`)

- **Notebook changes:**
  - 17 → 22 cells, numbered from 1; 576 → 393 code lines; longest cell 398 → 75 lines.
  - LoRA comes from `peft==0.21.2` (`get_peft_model` on `Wqkv`, `Wo`, `Wi`; `merge_and_unload()` at save). The hand-written `LoRALinear` is gone, since a separate LoRA-by-hand notebook will cover the mechanism.
  - Only the final recipe remains: the Nemotron, two-specialist and multi-loss paths are removed (each run is reproducible from its own commit).
  - The ordinal loss is built as tensors, and `scores()` handles any number of options.
  - Four test functions instead of seven, using the `table` helper.
  - Independent set 2 was added (data copied from `exp/listwise-index`).
  - The export is now "save and verify" (`SAVE_MODEL`), and it also writes the LoRA adapter on its own.
  - Kaggle needs `pip uninstall torchao` (version 0.10 makes `peft` refuse to load).
- **Training:** healthy on the first attempt, 38.5 min on a T4, best epoch 2 (dev routing 98.9%, dev questions 98.0%). `peft` reports 7,196,672 trainable parameters (the same 112 layers).
- **Save and verify:** `encoder/` 793 MB, `adapter/` 29 MB (fp32), `signpost.zip` 0.76 GB. Reloaded with the published `signpost.py`, the saved model reproduces the trained one exactly: E11 96 and E12 162, in both fp16 and fp32.

| Test | This run | Run 25 (published) | Decider |
|---|---|---|---|
| E10 all · test companies | 178 · 77 | 181 · 78 | 151 · 62 |
| Independent routing live · given | 131 · 140 | 133 · — | 113 |
| Independent 2 routing live · given | 59 · 62 | 62 · 65 | 55 |
| E11 · independent first messages · independent 2 first messages | 96 · 180 · 49 | 97 · 180 · 47 | 96 · 178 · 50 |
| Banking 50 · 225 | 50 · 216 | 48 · 210 | 48 · 214 |
| E12: yes/no · choice · score | 162: 57 · 57 · 48 | 161: 58 · 58 · 45 | 160 |
| Independent questions: yes/no · choice · score | 232: 80 · 106 · 46 | 221: 75 · 103 · 43 | 253: 77 · 106 · 70 |
| Independent 2 questions: yes/no · choice · score · many-option | 195: 49 · 48 · 49 · 49 | 188: 47 · 47 · 45 · 49 | 185 |
| Latency p50: E10 · E12 · independent-2 routing (up to 11 agents) | 59 · 55 · 212 ms | | |

**Findings**
1. **`peft` reproduces the hand-written LoRA:** the same parameter count, results within noise, and a merged model that the existing loader reproduces exactly.
2. **Routing is level with run 25** (all within −3 … +6). **Questions are better on both outside sets** (independent +11, independent 2 +7). Part of that is seed variation: run 22b had independent questions at 231.
3. **Score on independent set 1 is still the gap:** 46 / 92 against the decider's 70, with 85 / 92 within one level.

**Decision:** keep run 25 as the published model; this run would only be used if the Hub moves to an adapter layout.

**Score diagnosis (from the training data):** 2,148 score items use only **34 distinct scales**; 93% are three-level and there are no four-level scales. The model learns those scales' words, not ordered scales in general. **Plan:** a fresh independent set 3 of score questions, written by a subagent first; then about 1,500 hand-written score items on 300+ scales (3–6 levels, every answer position); one run of the unchanged recipe, judged on set 3 (branch `exp/score-data`).

## Score attempt — 2026-10-17: hand-written score data, tried and dropped (branch `exp/score-data`, deleted)

- **Tried:** the 2,148 templated score training items (34 scales) were replaced by 1,425 hand-written items on 279 scales (3–6 levels). Independent set 3 (150 score questions, 75 scales) was written first by a subagent from a neutral brief.
- **Result (one Kaggle run, Signpost recipe):**
  - Independent set 3: 135 / 150, against **133 for the published Signpost** on the same items. No gain; the pre-set bar of 120 had been set without a baseline.
  - Independent set 1 score: 54 / 92 (seeds before: 43–53).
  - Independent first messages fell to 171 (180–181 in every earlier run), and independent-2 routing to 56. Not adopted.
- **Blind relabelling** of the 92 set-1 and 150 set-3 score items (text, question and scale only):
  - Opus labeller: matched set 1 on 78%, set 3 on 100%.
  - Haiku labeller: matched set 1 on 88%, set 3 on 97%.
  - Every label is within one level.
- **Conclusion:**
  - Set 1's labels are sound.
  - Signpost trails careful readers by about 30 points on that outside-written set (47–59% against 78–88%; the decider gets 76%), and by about 10 points on clear-cue scales (set 3: 89–90% against 97–100%). It is nearly always within one level, and often one level too low on strongly worded texts.
  - The cause was not scale variety.
  - Test sets written by Claude subagents understate the gap, because every Claude reader finds them easy.
- **Decision:** dropped. The branch, with its data, set 3 and brief, was deleted at the user's request. The published Signpost stays, and the score limitation is stated. A real fix would need score data and a test written outside our model family.

## 03 final run — 2026-10-17: the restructured notebook, saved with results (branch `signpost`)

- **Training:** healthy on the first attempt, 35.2 min, best epoch 2 (dev routing 98.7%, dev questions 97.5%), 7,196,672 trainable parameters (`peft`). **Save and verify:** reloading in fp32 is exact (E11 96, E12 159); in fp16, E12 gives 160 (one item flips between precisions).

| Test | This run | Run 25 (published) | Decider |
|---|---|---|---|
| E10 all · test companies · given previous agent | 181 · 80 · 183 | 181 · 78 · — | 151 · 62 |
| Independent routing live · given | 135 · 144 | 133 · — | 113 |
| Independent 2 routing live · given | 63 · 64 | 62 · 65 | 55 |
| E11 · independent first messages · independent 2 first messages | 96 · 178 · 50 | 97 · 180 · 47 | 96 · 178 · 50 |
| Banking 50 · 225 | 49 · 216 | 48 · 210 | 48 · 214 |
| E12: yes/no · choice · score | 159: 55 · 56 · 48 | 161: 58 · 58 · 45 | 160 |
| Independent questions: yes/no · choice · score | 219: 73 · 104 · 42 | 221: 75 · 103 · 43 | 253: 77 · 106 · 70 |
| Independent 2 questions | 190 | 188 | 185 |

- **Everything is within noise of the published model.** Latency p50 is 55–58 ms for questions and E10, and 187 ms for independent-2 routing (up to 11 agents).
- **Same seed, same code, different result:** the previous rerun got independent questions 232 (score 46); this one gets 219 (42). GPU training is not bit-for-bit repeatable, so a single run moves by about ±10 on that set.
- **This is the notebook's saved state.**

## 04 restructure — 2026-10-18: `04_decider_benchmark.ipynb` rebuilt and rerun (branch `signpost`)

- **Notebook changes:**
  - 25 → 20 cells, numbered from 1.
  - Every test runs once and is timed as it runs; the old latency section reran E10, E11, banking and E12.
  - Helpers are defined once, up front.
  - One function each for conversations (full history and window 3), first messages and questions (native types; many-option as a choice question).
  - Independent set 2 was added.
  - A full side-by-side table against Signpost run 25 and 03's final run.
  - The decider stays in bfloat16 (the contradictory float32 text was removed); stale references were fixed.
- **Reproducibility:** the decider is deterministic. Every number on E10, E11, banking, E12 and independent set 1 matches benchmark B1 exactly.

| Test | Decider: full history · window 3 | Signpost run 25 · 03 final run |
|---|---|---|
| E10 all · test companies | 151 · 163 / 193; 62 · 69 / 83 | 181 · 181; 78 · 80 |
| Independent routing | 113 · 121 / 172 | 133 · 135 |
| **Independent 2 routing** | **55 · 59 / 70** | 62 · 63 |
| E11 · independent first messages · **independent 2 first messages** | 96 · 178 · **50** | 97 · 180 · 47; 96 · 178 · 50 |
| Banking 50 · 225 | 48 · 214 | 48 · 210; 49 · 216 |
| E12: yes/no · choice · score | 160: 56 · 56 · 48 | 161 · 159 |
| Independent questions: yes/no · choice · score | 253: 77 · 106 · 70 | 221 · 219 (score 43 · 42) |
| **Independent 2 questions: yes/no · choice · score · many-option** | **185: 49 · 46 · 43 · 47** | 188 · 190 (score 45 · 47) |
| Latency p50 | questions ~200 ms; routing 290–650 ms | questions 55 ms; routing 58–187 ms |

**Findings:** the conclusions of benchmark B1 hold, and independent set 2 adds one point: there the decider's score (43 / 50) is not better than Signpost's (45–47). Its score advantage shows on independent set 1 only. Cell 10 of 04 and Cell 9 of 03 were updated to match these outputs (03 also gains a row for the dropped score-data attempt).

---

# Runs 26–29: one pass per question (moved from branch `exp/listwise-index` with notebook 05, unchanged)

## Run 26 setup — 2026-10-13: one pass per question, all options in one input (branch `exp/listwise-index`, `05_listwise_signpost.ipynb`)

- **Question:** can one encoder pass per question replace Signpost's one pass per option, and scale to many options (up to 50) and many agents (up to 15)?
- **Model:** Signpost's encoder, LoRA (r 16) and head. All options go into one input (`… question: Q [SEP] option: A. … [SEP] option: B. …`), each option's tokens are mean-pooled, and the same head scores every option. The softmax over the options gives the answer, 1…N.
  - `MAX_LEN` 1,536; the oldest history is dropped first, options never.
  - `MAX_OPTIONS` 50 as a safety check.
  - Training batches are formed by token budget.
- **Training data, about 10.5K questions (user decision):**
  - all of Signpost's yes/no questions;
  - 30% of its routing conversations and 30% of its choice and score questions, stratified by business and family;
  - **2,500 hand-written many-option questions:** 957 individually written texts across 13 topics (no sentence templates), each used 2–3 times with different option lists of 2–50 options, drawn from same-topic value lists.
  - Routing questions get 0–10 extra **distractor agents** from other businesses each time they're used, up to 15 agents. Agents with generic names (general, support, billing, …) or names sharing a word with the business's own agents are excluded.
- **Fresh tests (hand-written, never used for training):**
  - **many-agent routing:** 12 businesses that appear in no training data, each with 9–15 agents; 24 conversations (120 turns, routed live) and 72 first messages;
  - **many-option questions:** 162 questions with 10–50 options. Their value lists share nothing with training (numbers aside), and the guard checks there's no shared 5-word sequence;
  - **option order:** the many-agent first messages with the agents reversed.
- **In the same notebook:** the old suites for comparison with Signpost run 25, then the published Signpost (from the Hub) and the Strands decider on the fresh tests, with latency.
- **Why the user rejected template data:** templates produce near-identical sentences, which narrows coverage and lets the model learn patterns instead of reading. The first, template-based many-option set was replaced by hand-written texts.

## Run 26 results — 2026-10-13: one pass per question (branch `exp/listwise-index`)

- **Training:** healthy on the first attempt, **12.5 min** (Signpost: 33). 10,508 training questions:
  - routing 1,894 (30%);
  - yes/no 5,000 (all);
  - choice and score 1,335 (30%);
  - many-option 2,279 (after the dev split).

  Dev after epoch 2: routing 98.9%, routing with 15 agents 97.4%, questions 95.9%. Peak GPU 13.1 GB.

| Old tests (same items) | **One pass (run 26)** | Signpost (run 25) | Decider |
|---|---|---|---|
| Conversations, unseen companies (83) · all (193) | 78 · **172** | 78 · **181** | 62 · 151 |
| First message E11 (100) | **99** | 97 | 96 |
| Banking 50 · 225 | 46 · 207 | 48 · 210 | 48 · 214 |
| E12 (170): yes/no · choice · score | **154**: 56 · 55 · 43 | **161**: 58 · 58 · 45 | 160 |
| Independent questions (300): yes/no · choice · score | **227**: 72 · 105 · **50** | 221: 75 · 103 · 43 | 253: 77 · 106 · 70 |
| Independent routing live (172) · first message (200) | 133 · 177 | 133 · 180 | 113 · 178 |

| Fresh tests (hand-written) | **One pass** | Signpost (Hub) | Decider |
|---|---|---|---|
| Many-option questions (162, 10–50 options) | 151 · 51 ms | 150 · 62 ms | **160** · 395 ms |
| Many-agent routing, live (120 turns, 9–15 agents) | **104** · 55 ms | 103 · 96 ms (p95 186) | 83 · 655 ms (99 with the last 3 turns) |
| … previous agent given | 107 | 109 | — |
| Many-agent first messages (72) | 62 · 51 ms | 62 · 50 ms | **70** · 526 ms |
| Option order: same pick with the agents reversed | 67 / 72 | — | — |

**Findings**
1. **One pass per question works.** It's level with Signpost on most tests, trained on two-thirds of the data in a third of the time. Its latency stays **flat at about 51–55 ms** for 10 to 50 options, while Signpost's grows with the agent count (96 ms p50, 186 ms p95 for 9–15 agents, batched on a GPU).
2. **Two drops are beyond the ±4 noise: conversations, all companies (−9) and E12 (−7).** Run 26 used only 30% of the routing and choice/score data, so the likely cause is less data rather than the design. Run 27 tests that with all of it.
3. **Accuracy holds as options grow:** many-option results are 26/27 at 10 or fewer options and 13/14 at 41–50. Routing dips a little at 13–15 agents (41/50 vs 37/40 at 10 or fewer).
4. **Against the decider:**
   - **we're far ahead in many-agent conversations** (104 vs 83, or 99 with its last-3-turns setting);
   - **it leads on many-agent first messages** (70 vs 62; ours miss mostly "close" messages, 10/14);
   - **it leads on many-option questions** (160 vs 151). Ours lose almost entirely on the departments family (21/30), the one family with no exact training counterpart.
5. **A small position effect:** reversing the agents changed 5 of 72 picks.

**Next (run 27, user decisions):**
- all of Signpost's data;
- the same 2,500 many-option questions;
- about 2,500 routing questions trained with 10–15 agents each time;
- a second independent test set, written by a subagent from a neutral brief (50 of each question type).

## Run 27 setup — 2026-10-13: all of Signpost's data + multi-option cases; a second independent set (branch `exp/listwise-index`)

- **Training (user decisions):**
  - all of Signpost's routing, yes/no, choice and score questions (`ROUTE_FRACTION` = `QUESTION_FRACTION` = 1.0);
  - the same 2,500 hand-written many-option questions;
  - about **2,500 routing questions trained with 10–15 agents** every time they're used (`MANY_AGENT_ROUTES`); the other routing questions get 5–9.

  This keeps the multi-option cases from being drowned out by the larger data. It also tests whether run 26's drops on E10 (all companies) and E12 came from using 30% of the data.
- **Second independent set (`independent2/`):**
  - **How it was written:** by a subagent (another Claude instance). It received only a neutral brief: formats, rules, a list of businesses to avoid, and a self-check. It was told not to open any repository file.
  - **Questions:** 50 yes/no (27 yes), 50 choice (2–5 options), 50 score (3–5 ordered levels, mostly 3) and 50 many-option (10–50 options, 13 kinds).
  - **Routing:** 50 first messages (10 businesses, 8–11 agents, 10 of each kind) and 12 conversations (70 turns, 7 businesses).
  - **Self-check:** OK.
  - **Kept for reference:** the raw files are in `independent2/raw/`; `build_independent2_test_data.py` converts and re-checks them.
  - **What it reported as borderline:**
    - few middle-level score answers (9 of 45);
    - a jobs list containing "manager" as a distractor;
    - four routing labels it flagged as debatable but kept.
  - **Caveat:** it's independent of our data and code, but not of the model family.
- **The notebook** runs it for our model, the published Signpost and the decider, and shows run 27 next to run 26.

## Run 27 results — 2026-10-14: all of Signpost's data + multi-option cases (branch `exp/listwise-index`)

- **Training:** healthy on the first attempt, 26.4 min, 18,049 questions:
  - routing 6,319, of which 2,500 were trained with 10–15 agents;
  - yes/no 5,000;
  - choice and score 6,730;
  - many-option 2,279.

  Dev after epoch 2: routing 99.4%, routing with 15 agents 98.3%, questions 97.6% (run 26: 98.9 / 97.4 / 95.9).

| Old tests | **Run 27** | Run 26 | Signpost (run 25) | Decider |
|---|---|---|---|---|
| Conversations, unseen companies · all | 78 · **177** | 78 · 172 | 78 · 181 | 62 · 151 |
| E11 · banking 50 · 225 | 99 · **49 · 211** | 99 · 46 · 207 | 97 · 48 · 210 | 96 · 48 · 214 |
| E12 (170): yes/no · choice · score | 153: 54 · 53 · 46 | 154: 56 · 55 · 43 | **161** | 160 |
| Independent questions (300): yes/no · choice · score | 211: 71 · 105 · **35** | 227: 72 · 105 · 50 | 221: 75 · 103 · 43 | **253**: 77 · 106 · 70 |
| Independent routing (172) · first message (200) | **136 · 181** | 133 · 177 | 133 · 180 | 113 · 178 |

| Fresh tests and the second independent set | **Run 27** | Signpost (Hub) | Decider |
|---|---|---|---|
| Many-option questions (162) | 152 · 58 ms | 150 · 66 ms | **160** · 422 ms |
| Many-agent routing live (120) · first messages (72) | **104** · 63 | 103 · 62 | 83 (99 with the last 3 turns) · **70** |
| Independent 2, questions (200): yes/no · choice · score · many-option | **188**: 46 · 46 · 47 · 49 | **188**: 47 · 47 · 45 · 49 | 185: 49 · 46 · 43 · 47 |
| Independent 2, routing live (70) · first messages (50) | 58 · 49 | **62** · 47 | 55 (59 with the last 3 turns) · **50** |
| Latency on independent 2 routing, p50 / p95 | **60 / 64 ms** | 124 / 220 ms | 768 ms |
| Option order: same pick with the agents reversed | 69 / 72 (run 26: 67) | — | — |

**Findings**
1. **Full data fixed routing:** every routing test rose from run 26 (E10 all +5, banking +3 / +4, independent routing +3, independent first message +4). The one-pass model now matches or beats Signpost on routing, at a flat ~55–60 ms for any number of agents.
2. **It didn't fix the question side, and independent score fell:**
   - E12 stayed at 153 (Signpost 161);
   - **independent score dropped 50 → 35**, although 90 / 92 answers are within one level.

   This run used all the template-generated score items (1,942, vs 581 in run 26). As in run 20, more generated score data didn't transfer to outside-written scales. That's consistent with the user's concern about template data. With one seed it isn't proven.
3. **On the second independent set the three models are close:** questions 188 / 188 / 185, routing live 58 / 62 / 55, first messages 49 / 47 / 50. The one-pass model is fastest, and its latency stays flat.
4. **E12 comparison questions fell 10 → 7 / 12.** That's within one-seed noise on 12 items.

**Suggested next (run 28):** template score questions capped at about 30%, plus hand-written score questions with varied scales. Alternatively, a second seed of run 27, to separate the data effect from noise.

## Run 28 setup — 2026-10-14: score questions trained as plain choice questions (branch `exp/listwise-index`)

- **Why:** with the ordinal score loss, the published Signpost gets 43 / 92 on independent score. Run 27 got 35 / 92.
  - A local test on Signpost (CPU, all 92 items) showed that **presentation isn't the issue.** Asked as a plain choice with the levels shuffled, the answers were identical (43, with 0 items changing). Using the rounded expected level gave 41.
  - **The misses are systematic: 41 of 49 are one level too low.** "Very clear" is read as "partly clear" (about 17 items), "very satisfied" as "satisfied" (5), and high or major urgency and seriousness as medium or moderate (about 12). The model hedges towards the middle.
  - Possible causes: the ordinal loss's neighbour smoothing and distance penalty, and / or template score data with few extreme answers and no clarity-type scales.
- **Change (user decision):** `SCORE_LOSSES=plain`, so score questions are trained like any choice question (plain cross-entropy on the right level). Everything else is as in run 27: all of Signpost's data, the 2,500 many-option questions, and 2,500 routing questions with 10–15 agents. The summary shows run 28 next to run 27, with E12 and independent score broken out.

## Run 28 results — 2026-10-14: score questions trained as plain choice questions (branch `exp/listwise-index`)

- **Training:** healthy on the first attempt, 26.4 min. Same data and seed as run 27; only the score loss changed (plain). Dev after epoch 2: routing 99.1%, routing with 15 agents 98.1%, questions 97.4%.

| Test (same items) | **Run 28 (plain)** | Run 27 (ordinal) | Signpost (run 25) | Decider |
|---|---|---|---|---|
| **Independent score (92)** | **46** | 35 | 43 | 70 |
| **Independent questions (300)**: yes/no · choice · score | **221**: 70 · 105 · 46 | 211: 71 · 105 · 35 | 221 | 253 |
| **E12 (170)**: yes/no · choice · score · comparison (12) | **158**: 57 · 56 · 45 · 11 | 153: 54 · 53 · 46 · 7 | 161 | 160 |
| Conversations, unseen companies · all | 76 · 179 | 78 · 177 | 78 · 181 | 62 · 151 |
| E11 · banking 50 · 225 | 97 · 49 · 212 | 99 · 49 · 211 | 97 · 48 · 210 | 96 · 48 · 214 |
| Independent routing · first message | 134 · 180 | 136 · 181 | 133 · 180 | 113 · 178 |
| Many-option (162) · many-agent routing live (120) · first messages (72) | 147 · 100 · 63 | 152 · 104 · 63 | 150 · 103 · 62 | 160 · 83 · 70 |
| Independent 2: questions · routing live · first messages | 185 · 55 · 49 | 188 · 58 · 49 | 188 · 62 · 47 | 185 · 55 · 50 |
| Option order: same pick with the agents reversed | 68 / 72 | 69 / 72 | — | — |

**Findings**
1. **The ordinal loss hurt outside-written scales.**
   - Training score questions as plain choices lifted independent score **35 → 46** and the independent total **211 → 221** (level with Signpost).
   - E12 rose to **158**, within noise of Signpost's 161, and comparison questions recovered (7 → 11 / 12).
   - E12's own score count didn't change (45 vs 46): its scales were written in the same style as our training data.
2. **Routing moved within noise:** most tests shifted by 1–2, the many-agent and independent-2 tests by up to 4. Many-option questions dropped 152 → 147, mostly in the departments family (19 vs 23 / 30). As run 21 showed, changing the loss shifts the whole training path by about ±4.
3. **The one-pass model is now level with Signpost on every old test** (all within ±3) at a flat ~55–60 ms. The remaining gap is independent score against the decider: 46 vs 70.

**Decision (recommended):** adopt the plain loss. **Next:**
- a second seed of this setup, to separate the gains from noise;
- hand-written score questions with varied scales and more answers at the extremes (the last template-made part of the data).

## Run 29 setup — 2026-10-14: no score questions in training or testing (branch `exp/listwise-index`)

- **Why:** across runs 21–28, score questions (pick a level on an ordered scale) never transferred to outside-written scales: independent score 35–50 / 92, against the decider's 70. Changing their loss also moved the other results around. **Decision: the model is not meant for score questions.** They are left out of training and of every test, so the model is judged only on what it is meant to do.
- **Change:** `INCLUDE_SCORE=0` (new setting). This drops score items from training and dev, and from the score items in E12 (now 117: 58 yes/no + 59 choice), the independent questions (208) and independent set 2 (150 questions). Everything else is exactly as in run 28: plain loss, all data, 2,500 many-option questions, 2,500 many-agent routing items, seed, MAX_LEN 1536.
- **Reference, the same items without score:**

| Test | Run 28 | Run 27 | Signpost (run 25 / hub) | Decider |
|---|---|---|---|---|
| E12 (117) | 113 | 107 | 116 | 112 |
| Independent questions (208) | 175 | 176 | 178 | 183 |
| Independent 2 questions (150) | 139 | — | 143 | 142 |

- Routing, first-message and many-option tests are unchanged and are compared against run 28 directly. The published Signpost and the decider run in the notebook on the same reduced sets.

## Run 29 results — 2026-10-14: no score questions in training or testing (branch `exp/listwise-index`)

- **Training:** healthy on the first attempt, 25.5 min. 2,148 score questions left out (training + dev). Dev after epoch 2: routing 99.1%, routing with 15 agents 98.1%, questions 98.4% (score-free dev).

| Test (same items, no score) | **Run 29 (no score)** | Run 28 | Run 27 | Signpost (run 25 / hub) | Decider |
|---|---|---|---|---|---|
| E12 (117): yes/no · choice | **107**: 54 · 53 | 113: 57 · 56 | 107 | 116: 58 · 58 | 112: 56 · 56 |
| Independent questions (208): yes/no · choice | **174**: 71 · 103 | 175: 70 · 105 | 176 | 178: 75 · 103 | 183: 77 · 106 |
| Conversations, unseen companies · all | 75 · 176 | 76 · 179 | 78 · 177 | 78 · 181 | 62 · 151 |
| E11 · banking 50 · 225 | 98 · 47 · 208 | 97 · 49 · 212 | 99 · 49 · 211 | 97 · 48 · 210 | 96 · 48 · 214 |
| Independent routing · first message | 128 · 179 | 134 · 180 | 136 · 181 | 133 · 180 | 113 · 178 |
| Many-option (162) · many-agent routing live (120) · first messages (72) | 149 · 101 · 63 | 147 · 100 · 63 | 152 · 104 · 63 | 150 · 103 · 62 | 160 · 83 · 70 |
| Independent 2 (score-free): questions (150) · routing live · first messages | 138 · 58 · 48 | 139 · 55 · 49 | — | 143 · 62 · 47 | 142 · 55 · 50 |
| Option order: same pick with the agents reversed | 69 / 72 | 68 / 72 | 69 / 72 | — | — |

**Findings**
1. **Leaving score out fixed nothing.** No test improved beyond noise. The yes/no and choice questions that remain didn't get better: E12 113 → 107 (yes/no 57 → 54, choice 56 → 53), independent questions 175 → 174, independent 2 questions 139 → 138.
2. **Some results fell beyond the usual ±4 noise:** E12 −6 and independent routing live −6 (switch turns 30/46). Banking 225 fell −4 and E10 all −3. Many-agent and independent-2 routing went up by 1–3, which is noise.
3. **The score questions weren't hurting the rest; if anything they helped a little**, as extra question data that keeps the shared head general. The independent yes/no weakness is unchanged: claim-check items are still 0/22, and truth "yes" is 27/50.
4. **Latency is unchanged:** a flat ~50–55 ms.

**Decision (recommended):** keep the run 28 setup (score included, plain loss) as the best one-pass model. In the notes, state that score questions on outside-written scales are weak (46/92 against the decider's 70). Don't drop the data.

## 05 — 2026-10-18: `05_one_pass_signpost.ipynb`, the one-pass model on the run-28 recipe (branch `signpost`)

- **Notebook:** Part 4b, structured like 03. It uses run 28's recipe only: all of Signpost's data + 2,500 many-option questions, 2,500 routing items trained with 10–15 agents, plain loss, `MAX_LEN` 1536, up to 50 options. LoRA comes from `peft`, and option pooling is built as one tensor mask. Signpost's and the decider's results are fixed reference numbers from 03, 04 and run 28's notebook. A save-and-verify step uses the new standalone loader `signpost/signpost_one_pass.py`.
- **Training:** healthy on the first attempt, 28.5 min, best epoch 2. Dev routing 98.1% (98.3% with 15 agents), dev questions 97.6%. Trainable parameters: 7,196,672.
- **Save and verify:** `signpost-one-pass/` holds `encoder/` (793 MB), `adapter/` (29 MB) and `signpost-one-pass.zip` (0.76 GB). Reloaded with `signpost_one_pass.py`, it is **exact in both fp16 and fp32**: E11 98, E12 152, many-option 152.

| Test | 05 | Run 28 | Signpost (published) | Decider |
|---|---|---|---|---|
| E10 all · test companies | 175 · 76 | 179 · 76 | 181 · 78 | 151 · 62 |
| Independent routing · independent 2 routing · many-agent routing (live) | 134 · 56 · 102 | 134 · 55 · 100 | 133 · 62 · 103 | 113 · 55 · 83 |
| E11 · independent first messages · independent 2 first messages · many-agent first messages | 98 · 178 · 50 · 62 | 97 · 180 · 49 · 63 | 97 · 180 · 47 · 62 | 96 · 178 · 50 · 70 |
| Option order: same pick with the agents reversed | 71 / 72 | 68 | — | — |
| Banking 50 · 225 | 47 · 210 | 49 · 212 | 48 · 210 | 48 · 214 |
| E12: yes/no · choice · score | **152**: 54 · 53 · 45 | 158 | 161 | 160 |
| Independent questions: yes/no · choice · score | 226: 80 · 106 · 40 | 221: 70 · 105 · 46 | 221 | 253 |
| Independent 2 questions · many-option questions | 184 · **152** | 185 · 147 | 188 · 150 | 185 · 160 |
| Latency p50: questions · routing with 5 agents · routing with 8–11 agents · 10–50 options | 56 · 60 · 62 · 61 ms | | 55 · 58 · 187 · 63 ms | 200 · 316 · 654 · 382 ms |

**Findings**
1. **The notebook reproduces the one-pass result within noise**, and its saved model and loader are verified exactly. The exception is E12, at 152 (−6 against run 28; runs 27–28 gave 153–158). This run's training path differs (`peft`, data order, dev sampling), and a shift of this size is in line with that.
2. **Latency stays flat at 56–62 ms on every test**, while Signpost's routing cost triples with 8–11 agents (187 ms).
3. Option order is very stable (71 / 72). The model gets 12 of the 22 claim-check yes/no items (every other model gets 0). Independent score is 40 / 92 (this model's range is 35–46).

## Signpost one-pass published — 2026-10-18: [huggingface.co/skamalj/signpost-one-pass](https://huggingface.co/skamalj/signpost-one-pass)

- **What:** the model from 05's run (`signpost-one-pass.zip`, downloaded and kept locally in `models/signpost-one-pass/`, which is git-ignored). It is a separate repo (option A), so the published Signpost is unchanged.
- **Files:** `encoder/` (merged ModernBERT-large, fp16), `head.pt`, `signpost_config.json` (`"format": "one-pass"`), the loader `signpost_one_pass.py`, the card (`signpost/README_one_pass.md` in the repo) and `card_examples_one_pass.py`. The LoRA adapter on its own is not published. Public, Apache-2.0; Hub commit 0cb2271.
- **Card examples:** run on the local export on CPU (fp32). All answers are correct, including routing among 12 agents in one pass (833 ms on a laptop CPU) and a 20-option question.
- **Signpost's card** now links to the one-pass model (Hub commit e76e5c6).
- **Verified from the Hub:** a fresh `snapshot_download` into a new folder has encoder weights byte-identical to the local export, and the card examples give exactly the recorded outputs (only the CPU timing of the 12-agent example varies: 833 and 1,018 ms).

## 06 — 2026-10-24: `06_typed_decisions_benchmark.ipynb`, Signpost on the Typed Decisions benchmark (branch `signpost-typed-decisions`)

- **What:** [LocalLLaMA/typed-decisions](https://huggingface.co/datasets/LocalLLaMA/typed-decisions) (dataset revision 4772cfe): 400 test cases, each a JSON state with five typed questions (yes/no 600, choice 600, score 800 decisions) in four workflows (agent-trace review, customer service, invoice processing, security alerts). Gold answers are soft distributions from a ~4B teacher. Scored with the benchmark's own code. Measurement only: no training, no upload, nothing submitted.
- **Reference points (accuracy):** uniform 0.308 · always-majority ~0.47 · teacher self-agreement 0.735 · public leaderboard 0.61 (fitted MiniLM) to 0.81.
- **Input format:** five formats compared on 200 train-split cases (1,000 decisions): raw JSON (as published), readable `key: value` lines, yes/no statements asked as questions, yes/no option descriptions, 512 tokens. **As published was best for both models**, 0.388 vs 0.377–0.379 (Signpost) and 0.410 vs 0.381–0.392 (one-pass), so the test split was scored as published only.
- **Calibration:** a temperature fitted on Signpost's own E12 + independent questions (470; never the benchmark): T = 2 for Signpost (own accuracy 0.813, NLL 0.641 → 0.500), T = 4 for one-pass (0.804, NLL 0.838 → 0.422).

**Test split, general mode (2,000 decisions):**

| | Signpost | one-pass |
|---|---|---|
| Accuracy | **0.4175** | 0.415 |
| — yes/no · choice · score | 0.590 · **0.320** · 0.361 | 0.550 · 0.322 · 0.384 |
| — agent trace · customer service · invoices · security | 0.424 · 0.436 · 0.448 · 0.362 | 0.334 · 0.538 · 0.338 · 0.450 |
| KL · Brier · ECE at T = 1 | 0.519 · 0.271 · 0.130 | 1.993 · 0.537 · 0.403 |
| KL · Brier · ECE at the fitted T | **0.409 · 0.223 · 0.038** (T = 2) | 0.525 · 0.282 · 0.147 (T = 4) |
| Latency per case (5 questions), T4 p50 · p95 | 343 · 438 ms | 143 · 189 ms |

**Findings**
1. **Below the always-majority baseline (0.42 vs ~0.47), above uniform.** Both models are far below the leaderboard. Not worth submitting as is.
2. **Choice questions are the weakest (0.32)**, although choice is Signpost's strength on its own tests. Here the choices are *policy* decisions (continue / human review / stop; approve / hold / reject; contain / investigate / monitor) to be inferred from structured fields, not answers stated in the text; the teacher's policy has strong priors the model doesn't share. Yes/no is best (0.59 / 0.55). Score is 0.36 / 0.38 (4–5-level rubrics, the known weak spot).
3. **Readable formatting did not help**; the gap is in what the model knows, not in how the input looks.
4. **Calibration from our own data transfers:** Signpost's ECE drops from 0.130 to 0.038 and KL from 0.52 to 0.41 at T = 2, with accuracy unchanged. One-pass is far more overconfident (KL 1.99 at T = 1) and needs T = 4.
5. **Next:** a specialist fine-tune on the benchmark's train split shows how far this architecture can go on these decisions; the general route needs new training data with structured states and policy decisions (Phase C, neutral brief).

## 07 run 1 — 2026-10-24: `07_signpost_d.ipynb`, Signpost-D on the pilot data only (`DATA_MIX = "new"`, branch `signpost-typed-decisions`)

- **Data:** Signpost-D pilot (`data/signpost_d/pilot/final.jsonl`). 300 cases / 1,392 questions:
  - written by six Opus 5.5 generator subagents from our own brief (`data/signpost_d/brief.md`, no benchmark content);
  - soft-labelled by three independent stances (cautious, pragmatic, neutral; averaged). They agree on the top answer for 94% of questions;
  - checked by two validators: 12 fixes, 5 relabels, 1 drop.
  - Split by case: 240 train (1,113 questions), 60 dev (279).
  - Overlap with the benchmark (my script only): no 8-word overlaps; only generic field names and labels shared.
- **Setup:**
  - start from Signpost's published weights (merged encoder + head), new LoRA r 16, 7.2 M trainable;
  - soft-label cross-entropy, plus an expected-level term for score questions;
  - MAX_LEN 512, gradient checkpointing (batches of 8 ran out of memory on a T4), BATCH_NEW 4;
  - 6 epochs, best epoch by dev KL; 37 min on a T4, peak 3.6 GB.
- **Before training**, Signpost as published on our dev cases: accuracy **0.398** (KL 0.745, ECE 0.174). This is almost its benchmark score (0.4175), so our independently written cases test the same missing skill.

**Our dev cases by epoch:**

| | before | 1 | 2 | 3 | 4 | 5 | 6 (kept) |
|---|---|---|---|---|---|---|---|
| accuracy | 0.398 | 0.427 | 0.466 | 0.527 | 0.606 | 0.602 | **0.634** |
| KL | 0.745 | 0.637 | 0.638 | 0.637 | 0.520 | 0.486 | **0.474** |

Still improving at epoch 6. Temperature fitted on dev: 1.25.

**Benchmark test (general mode, scored once):**

| | Signpost (06) | run 1 |
|---|---|---|
| accuracy | 0.4175 | **0.3965** |
| yes/no · choice · score | 0.590 · 0.320 · 0.361 | 0.570 · 0.303 · 0.336 |
| agent trace · customer service · invoices · security | 0.424 · 0.436 · 0.448 · 0.362 | 0.280 · 0.466 · 0.398 · 0.442 |
| KL · Brier · ECE (T=1) | 0.519 · 0.271 · 0.130 | 0.783 · 0.333 · 0.147 |
| KL · Brier · ECE (fitted T) | 0.409 · 0.223 · 0.038 (T 2, own data) | 0.667 · 0.308 · 0.115 (T 1.25, dev) |

**Signpost's original tests (forgetting):**

| | Signpost | run 1 |
|---|---|---|
| E10 routing live | 181/193 | 114 |
| independent routing | 133/172 | 80 |
| independent 2 routing | 62/70 | 34 |
| E11 first messages | 97/100 | 82 |
| E12 questions | 161/170 | 131 |
| independent questions | 221/300 | 187 |
| independent 2 questions | 188/200 | 147 |

Latency is unchanged (~55 ms per question).

**Findings**
1. **Our data teaches our cases:** dev accuracy rose from 0.398 to 0.634 (+24 points) and dev KL from 0.745 to 0.474.
2. **It did not transfer to the benchmark:** 0.3965 against 0.4175. Security (+8) and customer service (+3) improved; agent trace (−14) and invoices (−5) fell; KL is worse.
3. **Heavy forgetting:** training on the new cases alone damaged the general reading skill, routing most of all. Even simple items fail, such as "who scored highest?". This likely cancels any benchmark gain.
4. **Some of what was learned is our labellers' conventions.** The benchmark's gold comes from a different ~4B teacher with its own policy priors, so neutral data can close only part of that gap.
5. **Next:** run 2 (`new+old`) to test whether keeping the general skill restores Signpost's tests and helps the benchmark. Then decide on the full data run, with brief v2 and three different labeller models.

## 07 run 2 — 2026-10-24: `07_signpost_d.ipynb`, from plain ModernBERT-large on v1 data (abandoned)

- **Setup:**
  - start from `answerdotai/ModernBERT-large`, with a new LoRA (r 16) and a new head (HEAD_LR 1e-3);
  - data: D_SET v1, 1,500 cases (6,071 train / 1,056 dev questions);
  - 4 epochs, batch 8.
- **Stopped by a network failure** during epoch 2. At epoch 1, dev accuracy was 0.4375, KL 0.744 and ECE 0.057; the loss fell slowly, 1.23 → 1.19.
- **Not repeated.** Two faults were found, and both are fixed for run 3:
  - **Score loss:** the expected-level term weighted options by their position after shuffling, not by their level.
  - **Score scales:** some ran highest first. The data was then put in System One form (`data/signpost_d/format_spec.md`, commit ace7a5a). 510 format fixes, of which 110 were scales written the wrong way round and 396 were score instructions reworded to name their quantity.
- **Notebook changes for run 3:**
  - one `render()` for our cases and the benchmark: `noul` as true/false with their descriptions, `choice` by its labels, `score` by its criteria lowest first;
  - one temperature per question type, fitted on dev;
  - a calibration check: top-probability histograms, entropy, and over-certain options and their share of the KL.

## 07 run 3 — 2026-10-24: v1 in System One form, from plain ModernBERT-large (collapsed, stopped)

- **Setup:** as run 2, with the score-loss fix, `render()` and per-type temperatures. Seed 42.
- **Collapsed:** epoch 1 gave dev KL **0.7542**, against **0.7544** for a uniform guess on the same dev questions. The model gave every option the same probability.
  - The loss stayed at about 1.2 throughout: the uniform guess's cross-entropy (1.08) plus the score term. The floor set by the soft labels is 0.33.
  - Dev accuracy was 0.430. The prior (average label by type and position) reaches 0.462.
- **Same failure as Signpost's run 22** (notebook 03): a start from plain ModernBERT-large stayed at chance. Runs 2 and 3 both used seed 42.
- **Fix for run 4:** a collapse guard.
  - At step 400, dev KL on 300 questions must be at least 0.02 below the uniform guess's.
  - If it isn't, training restarts with seed + 1000, up to 3 attempts.

## 07 run 4 — 2026-10-24: as run 3, with the collapse guard (stopped)

- **Setup:** plain ModernBERT-large, with the collapse guard at step 400 and seeds 42 / 1042 / 2042.
- **Stopped by the user:** the loss stayed at about 1.18–1.19, the same uniform-guess level as runs 2 and 3. The saved outputs were overwritten locally by a notebook edit, so the exact log is only in the Kaggle copy.
- **Conclusion:** a start from plain ModernBERT-large has not trained on this data in three runs. Next:
  - **Run 5:** 07 from Signpost's weights, as in run 1, with all the run-3 fixes.
  - **Then:** `08_signpost_d_onepass.ipynb` (option B).

## 07 run 5 — 2026-10-24: v1 in System One form, from Signpost's weights

- **Setup:** `07_signpost_d.ipynb` (commit e10df5c).
  - Start from `skamalj/signpost` (merged encoder and head), with a new LoRA (r 16), HEAD_LR 5e-4, 4 epochs and batch 8.
  - Data: v1 in System One form (6,071 train / 1,056 dev questions). Includes the score-loss fix, `render()` and the collapse guard.
  - 153 minutes on a T4.
- **Collapse check at step 400:** dev KL 0.506, against 0.664 for a uniform guess. Passed.
- **Dev by epoch.** Epoch 2 was kept: the skill is learned within 1–2 epochs, and later epochs only memorise (training loss 0.53 by epoch 4).

| | 1 | **2 (kept)** | 3 | 4 |
|---|---|---|---|---|
| accuracy | 0.689 | 0.689 | 0.698 | 0.703 |
| KL | 0.486 | **0.485** | 0.490 | 0.518 |
| ECE | 0.051 | 0.035 | 0.041 | 0.051 |

- **Dev by type, at epoch 2:**

| Type | Accuracy | KL | Fitted temperature |
|---|---|---|---|
| true/false | 0.771 | 0.370 | 1.5 |
| choice | 0.676 | 0.507 | 1 |
| score | 0.612 | 0.591 | 1.25 |

  With the fitted temperatures, overall dev KL is 0.470.
- **Grounded-question tests** (Signpost / run 1 / run 5). The reading skill is mostly kept, unlike run 1:

| Test | Signpost | Run 1 | Run 5 |
|---|---|---|---|
| E12 | 161 | 131 | 146 |
| independent | 221 | 187 | 226 |
| independent 2 | 188 | 147 | 185 |

  Independent score questions are weak: 46 / 92.
- **Benchmark test split** (scored once):

| | Accuracy | KL | Brier | ECE |
|---|---|---|---|---|
| T = 1 | 0.4155 | 0.678 | 0.358 | 0.248 |
| T per type | 0.4155 | 0.563 | 0.314 | 0.207 |

  - Signpost scored 0.4175 / KL 0.519. The prior scores 0.470 / KL 0.347.
  - By type: true/false 0.502 (Signpost 0.590), choice 0.393 (0.320), score 0.367 (0.361).
  - By workflow: customer service 0.630 (+0.19), security 0.472 (+0.11), agent trace 0.346 (−0.08), invoices 0.214 (−0.23, below uniform).
- **Calibration:** the head does **not** push towards 0 and 1.
  - On the benchmark, predicted entropy is 0.65 against 0.64 for the gold, and only 4.5% of the KL comes from over-certain options.
  - The KL comes from putting weight on the wrong option.
- **Reading:**
  1. Every type drops by about the same amount from dev to the benchmark (0.25–0.28), so this is a transfer gap, not one type's format.
  2. All 2,442 of our true/false items were yes/no questions, while the card defines `noul` as "the probability that the **statement** is true".
  3. Next: all true/false items rewritten as statements (gold unchanged), then `08_signpost_d_onepass.ipynb`. One pass means score levels see the whole rubric.

## 08 run 6 — 2026-10-25: Signpost-D one-pass, from Signpost one-pass's weights

- **Setup:** `08_signpost_d_onepass.ipynb`.
  - Start from `skamalj/signpost-one-pass` (merged encoder and head), with a new LoRA (r 16), HEAD_LR 5e-4, 3 epochs and batch 8.
  - One pass per question: every option goes into one input, and each option is pooled over its own tokens.
  - Data: v1 at commit 9cc3e7c. All true/false items are statements with exact true/false descriptions, score instructions name their quantity, and 48% of states are JSON.
  - **46.5 minutes on a T4,** against 153 for run 5. Peak GPU 2.8 GB.
- **Collapse check at step 400:** dev KL 0.442, against 0.664 for a uniform guess.
- **Dev by epoch.** Epoch 2 was kept: epoch 3 raised accuracy but made the model overconfident.

| | 1 | **2 (kept)** | 3 |
|---|---|---|---|
| accuracy | 0.675 | **0.712** | 0.725 |
| KL | 0.461 | **0.4605** | 0.492 |
| Brier | 0.297 | **0.292** | 0.294 |
| ECE | 0.033 | **0.029** | 0.040 |

- **Dev by type:**

| Type | Accuracy | KL |
|---|---|---|
| true/false | 0.760 | 0.373 |
| choice | 0.718 | 0.480 |
| score | 0.651 | 0.537 |

  Fitted temperatures: true/false 1.5, score 1.25, choice 1.
- **Grounded-question tests** (Signpost / run 5 / run 6):

| Test | Signpost | Run 5 | Run 6 |
|---|---|---|---|
| E12 | 161 | 146 | 148 |
| independent | 221 | 226 | **236** |
| independent 2 | 188 | 185 | **188** |

- **Benchmark test split** (scored once):

| | Accuracy | KL | Brier | ECE |
|---|---|---|---|---|
| T = 1 | **0.4365** | 0.685 | 0.376 | 0.242 |
| T per type | **0.4365** | **0.551** | 0.324 | 0.195 |

  - **The first model above Signpost's 0.4175.** It is still below the prior (0.470 / KL 0.347).
  - By type: true/false 0.557, choice 0.390, score 0.381.
  - By workflow:

| Workflow | Accuracy | Change from run 5 |
|---|---|---|
| agent trace | 0.432 | +0.09 |
| customer service | 0.598 | |
| security | 0.504 | |
| **invoices** | **0.212** | below uniform; KL 1.03, ECE 0.50, so confidently wrong |

  - Without invoices, accuracy on the other three workflows is about 0.51.
- **Calibration:** on the benchmark, predicted entropy is 0.655 against 0.639 for the gold. Only 1.7% of the KL comes from over-certain options at T = 1, and none with the per-type temperatures.
- **Reading:**
  1. One pass is better than one pass per option on dev and on the benchmark, and 3× faster.
  2. The format corrections coincide with gains where the format had differed most (agent traces, true/false).
  3. Invoices are the remaining large gap.
- **Next:** run 7 is 08 with a bigger LoRA (r 64) and a deeper head. The head gets zero-initialised residual blocks on the published head, so it starts identical to it.

## Data v1_1 — 2026-10-25: v1 + 150 invoice cases

- **Why:** after run 6 the user chose to add the invoice domain. The domain is public on the dataset card; no benchmark question, case or field was seen by anyone writing the data.
- **Disclosure:** the invoice cases were added *after* a benchmark result showed invoices as the weak workflow. Any submission must say so.
- **Brief:** `data/signpost_d/brief_v2_1_invoices.md`. It describes accounts-payable checks from general practice, and cases are written directly in System One form.
- **Production:**
  - 3 Opus generators (I1–I3, 50 cases each, on different businesses);
  - 3 labellers (Opus cautious, Sonnet pragmatic, Fable neutral). All three agree on the top answer for 98% of questions; mean top 0.93;
  - 3 validators: 32 keep, 11 fix, 6 relabel, 0 drop. Five relabels corrected a labeller's arithmetic.
- **Overlap with the benchmark (my script only, on a temporary copy):** no 8-word overlap. The shared JSON keys are generic invoice words (24 of 697).
- **v1_1 in numbers:** 1,650 cases and 7,824 questions.
  - Of the invoice cases' 697 questions: 323 true/false, 245 choice, 129 score. Half of their states are JSON.
  - Dev: run 6's 225 v1 cases are kept unchanged, plus 22 invoice cases.

## Signpost-D: the plan of options, to explore one at a time (2026-10-25)

This was agreed with the user while run 7 was training. Each step is one notebook run, compared on the same dev split (run 6's v1 dev cases, plus invoice dev cases) and on the benchmark test split, scored once. The zero-shot rule holds throughout: train only on our own data, never on benchmark cases, questions, fields or factors. The invoice cases were added after a benchmark result, and that must be disclosed.

**Run 7 is training now** (08 on v1_1): LoRA r 64, 2 zero-initialised residual head blocks, and the 150 invoice cases. Then:

1. **Read run 7.**
   - Compare dev on the v1 cases with run 6 (0.712 / KL 0.4605).
   - Compare our invoice dev with the benchmark's invoice row (0.212). Weak on both points to capacity or data; good on ours but weak on theirs points to the teacher's conventions.
2. **Separate run 7's three changes.** One run each, against run 6:
   - invoice data only (r 16, plain head);
   - LoRA r 64 only;
   - deeper head only.
3. **Average models.** Average the probabilities of runs 6, 7 and later runs. Choose the combination on our own dev set only.
4. **Score questions,** our weakest type (dev 0.65, benchmark 0.38, and 800 of the 2,000 benchmark questions):
   - **4a:** more score data, written with brief v2.1;
   - **4b:** an ordinal score head, with levels treated as positions on one scale.
5. **A deeper or wider head,** if step 2 shows the head helps: e.g. 4 blocks, or 512 units. The blocks start at zero, so the warm start is kept.
6. **A bigger encoder.**
   - **6a:** 08 from plain ModernBERT-large, to test whether one pass removes the stall at a uniform guess seen in runs 2–4.
   - **6b:** if 6a trains, 08 with Ettin-encoder-1B.
7. **More and broader data:** about 500 cases with brief v2.1, written in System One form from the start. In runs 5 and 6, dev stopped improving after epoch 2.
8. **An encoder–decoder under 0.8B parameters** (notebook 09, Thanos-style).
   - **Shape:**
     - The encoder reads the state.
     - An MLP bridge maps **every** state token to a soft token in the decoder's embedding space; nothing is pooled, so the numbers stay reachable.
     - The decoder reads `<bos> Case: [soft tokens] \n` followed by the question and the options lettered A, B, …
     - Each option's probability is read from its label token at the last position, as `/v1/systemone` reads a decoder. One forward pass is enough; nothing is generated.
   - **Configurations:**
     - **A:** ModernBERT-base (about 150M) + Gemma 3 270M, about 0.42B in total.
     - **B (recommended):** Signpost-D one-pass encoder (about 395M, already trained on our decisions) + Gemma 3 270M, about 0.67B.
     - **C:** ModernBERT-base + Qwen3-0.6B, about 0.75B.
   - **Training:**
     - stage 1 aligns the bridge: the decoder reconstructs the state text from the soft prefix (Thanos stage 1, with a guard for its sudden "click");
     - stage 2 trains decisions on v1_1, with soft-label cross-entropy on the label tokens and the decoder's LoRA reset (Thanos run 16: reset beat carry).
   - **Control:** the same decoder alone, reading the state as plain text. The encoder–decoder must beat it, or the bridge adds nothing.
   - **Risks:**
     - small decoders are weak at arithmetic (d3-edge, 0.6B: 0.425);
     - Gemma 270M may add little reasoning;
     - two stages take about 1.5–2 hours on a T4.
9. **A small decoder deciding directly** (Gemma 3 1B + LoRA, labels A–Z read from logprobs). This can be served by vLLM `/v1/systemone` and scored by the official `score_with_jobs.py`. It is outside the 0.8B limit, so it is kept for comparison.

**Not to do:**
- fitting the benchmark's own fixed questions (per-question priors);
- its domains beyond invoices;
- its teacher's habits.

That is where the gap to the Prior (0.470 / KL 0.347) lies, but closing it that way would make Signpost-D a fitted, not a zero-shot, model.

### Options 8 and 9 set up for an unattended run (2026-10-25)

- **`09_signpost_d_encdec.ipynb`:** the encoder–decoder, about 0.75B in total.
  - **Model:** ModernBERT-base (+LoRA), an MLP bridge (one soft token per state token, nothing pooled), and Qwen3-0.6B (+LoRA). Qwen3-0.6B is ungated, so no token is needed.
  - **Prompt:** `Case:` [soft tokens], then the question and lettered options. Each option's probability is read from its label token at `Answer:`.
  - **Stage 1:** reconstruct each training case's text (its first 256 tokens) from its soft tokens, for 3 epochs, training the encoder LoRA, the bridge and the decoder LoRA.
  - **Stage 2:** the decoder LoRA is reset, the encoder and bridge are frozen, and decisions are trained for 2 epochs. The best epoch is chosen by dev KL, with the collapse check at step 400.
  - **`MODE = "decoder"`:** the control run, the same decoder and LoRA reading the case as text.
  - **Settings:** a papermill `parameters` cell. Results go to `<run>_results.json`, which includes per-question probabilities for averaging later.
- **`11_runner.ipynb`:** runs the queue `09_encdec`, then `09_decoder`, with papermill, each in its own kernel.
  - A run that fails is logged, and the next still runs.
  - A summary table is printed after each run, against run 6.
  - An optional Kaggle secret `HF_TOKEN` is passed through the environment, never written down.

## 08 run 7 — 2026-10-25: one-pass on v1_1 (invoice cases), LoRA r 64, deeper head

- **Setup:** `08_signpost_d_onepass.ipynb` (commit 23b9fcb).
  - Start from `skamalj/signpost-one-pass`, with LoRA r 64 / alpha 128 (28.8M trainable) and `HEAD_EXTRA` 2 (zero-initialised residual blocks).
  - Data: D_SET v1_1 (6,669 train / 1,155 dev questions). 3 epochs, 53 minutes, peak GPU 3.2 GB.
- **Collapse check at step 400:** dev KL 0.423, against 0.664 for a uniform guess (run 6: 0.442).
- **Dev by epoch.** Epoch 2 was kept; epoch 3 became overconfident.

| | 1 | **2 (kept)** | 3 |
|---|---|---|---|
| accuracy | 0.669 | **0.713** | 0.724 |
| KL | 0.495 | **0.440** | 0.504 |
| ECE | 0.052 | **0.012** | 0.064 |

- **Dev split, per-type temperatures:**

| Part | Run 6 | Run 7 |
|---|---|---|
| v1 cases (same 1,056 questions) | 0.712 / KL 0.446 | 0.713 / KL **0.430** |
| invoice cases (99 questions) | – | **0.707** / KL 0.445 |

  By type (dev, T = 1): true/false 0.778, choice 0.690, score 0.661.
- **Grounded-question tests:** E12 146, independent 233 (score 54/92, against 47 in run 6), independent 2 183.
- **Benchmark test split** (scored once):

| | Accuracy | KL | Brier | ECE |
|---|---|---|---|---|
| T = 1 | **0.471** | 0.663 | 0.345 | 0.230 |
| T per type | **0.471** | **0.548** | 0.300 | 0.182 |

  - Level with the prior's 0.470 on accuracy; the prior's KL is 0.347.
  - By type: true/false 0.628, choice 0.430, score 0.384.
  - By workflow:

| Workflow | Run 6 | Run 7 |
|---|---|---|
| **invoices** | 0.212 | **0.478** |
| agent trace | 0.432 | 0.374 |
| customer service | 0.598 | 0.564 |
| security | 0.504 | 0.468 |

- **Calibration:** no option is over-certain, either on dev or on the benchmark. Predicted entropy on the benchmark is 0.626, against 0.639 for the gold.
- **Reading:**
  1. The invoice data closed the invoice gap. That gap was missing data, not the teacher's conventions; our own invoice dev is 0.707.
  2. The other three workflows fell 3–6 points while our v1 dev held. The cause is either the data mix or the r 64 capacity; plan step 2 (invoices only, r 16, plain head) separates them.
  3. Score questions are still the weakest type.
- **Disclosure:** the invoice cases were added after a benchmark result.

### Run 7 analysis — why choice questions fail (benchmark train split, reading only; no data changed)

- **Per question,** the model gives nearly one answer to every case:

| Question | Model's top answer | Gold's top answers | Accuracy |
|---|---|---|---|
| agent / action | observe 299/300 | human_review 142, observe 114 | 0.377 |
| invoice / disposition | approve 300/300 | approve 120, manual_review 110, hold 57 | 0.400 |
| security / disposition | close_benign 260 | investigate 214 | 0.113 |
| customer service / category (answered from the text) | spread | spread | 0.793 |

- **Field-flip test:** the same case, with its deciding fields set safe or risky, 60 cases each.

| Question | Fields changed | Mean change (TV) | Top answer changed |
|---|---|---|---|
| agent / outcome | violation counts | 0.758 | 60/60 |
| agent / action | the same fields | 0.163 | 0/60 |
| invoice / disposition | invoice price 15% over the order | 0.005 | 0/60 |
| security / disposition | MFA, allowlist, change window, criticality | 0.022 | 1/60 |

- **Reading:** the encoder reads values whose meaning an option's text names; the "harmful" description says "violated a constraint", which is why outcome moves. It cannot compare two numbers, combine several weak signals, or turn a finding into an action. That points to a decoder: the 09 encoder–decoder and its decoder-only control. Run the same field-flip test on them.
- **Runner dropped (2026-10-25):** `11_runner.ipynb` was removed. Its Kaggle session disconnected partway, and the user now runs the notebooks one at a time:
  - `09` with `MODE = "encdec"`;
  - then `09` with `MODE = "decoder"`, `RUN_NAME = "09_decoder"`, in a fresh kernel.

  The papermill `parameters` cell in 09 stays; it's harmless.
- **`09b_signpost_d_encdec_joint.ipynb` (user's idea):** the encoder–decoder trained in one stage. The encoder LoRA, bridge and decoder LoRA learn together on the decisions; there is no reconstruction stage, and `LR_BRIDGE` is 1e-3. The best-epoch snapshot covers all three parts.
  - Why: in `09`, stage 1 reached only 0.51 held-out token accuracy (0.38 before) after 2 of 3 epochs, a loss of 1.97 per token. It did not click; the case texts are long and full of numbers.
  - `09` keeps running, to see what a half-aligned bridge gives.

## 09 run 8 — 2026-10-25: encoder–decoder, two stages (copy, then decide)

- **Setup:** ModernBERT-base + bridge + Qwen3-0.6B, 760M in total, on v1_1.
  - Stage 1: 3 epochs, 528 steps, 34 minutes.
  - Stage 2: decoder LoRA only (10.1M), with the encoder and bridge frozen; 2 epochs, 70 minutes.
- **Stage 1 never clicked.** Held-out reconstruction token accuracy went 0.377 → 0.496 → 0.508 → 0.509, with the loss about 1.85 per token.
- **Stage 2:** collapse check 0.517 (uniform guess 0.664). Dev epoch 1: 0.550 / KL 0.623 (kept). Epoch 2: 0.572 / KL 0.633.
- **Dev, per-type temperatures:** 0.550 / KL 0.612. The v1 part is 0.548; the invoice part 0.566.
- **Grounded tests:** E12 63/170, independent 133/300, independent 2 74/171.
- **Benchmark:** **0.3355** / KL 0.572 (per-type temperatures). The uniform guess scores 0.308.
- **Field-flip test:** mean change 0.001–0.004 and **0 of 60** on every question. The decoder ignores the case entirely; its answers depend only on the question and options. It is never confident: no top probability above 0.9.
- **Reading:** a frozen, poorly aligned bridge is a dead end. Stage 2 learned to answer from the question wording; training loss fell to 0.83 while dev did not improve. Next is `09b` (joint training: the decision loss trains the bridge), then the decoder-only control.

## 09b run 8b — 2026-10-25: encoder–decoder trained jointly (collapsed)

- **Setup:** `JOINT = True`, bridge LR 1e-3, 15.3M trainable.
- **Collapsed:** the loss went 1.33 → 1.17 → 1.21 → 1.21 over steps 100–400, the uniform level; the collapse check gave 0.6650 against 0.6641.
- **Reading:** a random, fast-changing bridge swamped the decoder's input, so it could not even use the question wording (which run 8 did). Fix: a gate on the soft tokens, starting at 0, and a bridge LR of 3e-4 (09c).

## 09 run 9 — 2026-10-25: decoder only (the control)

- **Setup:** Qwen3-0.6B + LoRA (10.1M trainable, 606M in total), reading the case as plain text, on v1_1. 61 minutes; peak GPU 4.1 GB.
- **Collapse check:** **0.399**, the best start of any run (run 7: 0.423).
- **Dev:** epoch 1 0.696 / KL **0.453** (kept); epoch 2 0.708 / 0.489 (memorising). The fitted temperatures were 1 for every type.
  - v1 part 0.696 / 0.448; invoice part 0.697 / 0.511. Run 7 was 0.713 / 0.430 and 0.707 / 0.445.
  - By type: true/false 0.759, choice 0.692, score 0.624.
- **Grounded tests:** E12 119/170; independent 235/300 (score 61/92, the best yet); independent 2 142/171.
- **Benchmark:**

| | Accuracy | KL | Brier | ECE |
|---|---|---|---|---|
| Run 7 (08, encoder) | **0.471** | 0.548 | 0.300 | 0.182 |
| **Run 9 (decoder)** | 0.461 | **0.491** | **0.277** | **0.153** |

  The best KL, Brier and ECE of any run. By type and workflow (run 9 against run 7):

| | Run 9 | Run 7 |
|---|---|---|
| choice | **0.452** | 0.430 |
| score | **0.420** | 0.384 |
| true/false | 0.525 | **0.628** |
| agent trace | **0.432** | 0.374 |
| customer service | 0.588 | 0.564 |
| security | 0.450 | 0.468 |
| invoices | 0.374 | **0.478** |

- **Field-flip test** (run 9 against run 7):

| Question | Run 9 | Run 7 |
|---|---|---|
| agent action | 0.168 / 4 of 60 | 0.163 / 0 |
| agent outcome | 0.669 / 60 | 0.758 / 60 |
| invoice | **0.025** / 2 | 0.005 / 0 |
| security | **0.053** / 0 | 0.022 / 1 |

- **Reading:**
  1. The decoder notices the deciding fields slightly more than the encoder, but still almost never changes its answer for them. Comparing numbers and combining signals is weak at both 0.4B and 0.6B.
  2. The two models are complementary. The encoder is better at reading, true/false and invoices. The decoder is better at judgement (score, choice, agent trace) and much better calibrated.
- **Next options:**
  - average runs 7 and 9, weighted on dev;
  - 09c, a gated joint encoder–decoder;
  - generic comparison and signal-combination training data (motivated by the benchmark analysis, so it needs disclosure if done);
  - a bigger decoder, which is over the 0.8B limit.
- **`09c_signpost_d_gated.ipynb`** (`MODE = "gated"`): the decoder reads the case as raw text, as run 9 does, plus a gated encoder reading.
  - **The reading:** 32 summary tokens (ModernBERT states averaged over 32 consecutive stretches, through the bridge) × tanh(g). The gate g starts at 0, so step 1 is exactly run 9's decoder.
  - **Training:** joint (decoder LoRA, encoder LoRA, bridge at 3e-4, gate at 5e-3); the gate's value is logged every 100 steps.
  - **Why:** run 9 (text) has the best calibration and judgement; run 7 (encoder) reads better and is stronger on true/false and invoices. The gate avoids 09b's collapse.

## 09c run 10 — 2026-10-25: gated encoder–decoder (raw text + gated encoder reading)

- **Setup:** `09c_signpost_d_gated.ipynb`, `MODE = "gated"`, v1_1, Qwen3-0.6B + ModernBERT-base, joint training, 2 epochs (80.5 min on a T4), 15.3 M trainable.
- **The gate never opened:** tanh(g) rose to about 0.04–0.05 in epoch 1 and fell back to 0.028 by the end. The decoder takes almost nothing from the encoder when it can read the text itself.
- **Dev:** epoch 1 0.689 / KL 0.457 (best, kept); epoch 2 0.690 / KL 0.521 (over-fitting: the loss fell 0.90 → 0.70 while dev KL rose). Run 9 had epoch 1 at 0.696 / 0.453. Dev predictions are *less* certain than the gold (entropy 0.70 against 0.29) at epoch 1.
- **Benchmark (T = 1; all fitted temperatures were 1):**

| | Accuracy | KL | Brier | ECE |
|---|---|---|---|---|
| Run 7 (08, encoder) | **0.471** | 0.548 | 0.300 | 0.182 |
| Run 9 (09, decoder) | 0.461 | **0.491** | **0.277** | **0.153** |
| **Run 10 (09c, gated)** | 0.453 | 0.510 | 0.281 | 0.177 |

| | Run 10 | Run 9 | Run 7 |
|---|---|---|---|
| choice | 0.452 | 0.452 | 0.430 |
| score | 0.393 | **0.420** | 0.384 |
| true/false | 0.535 | 0.525 | **0.628** |
| agent trace | 0.434 | 0.432 | 0.374 |
| customer service | 0.588 | 0.588 | 0.564 |
| security | 0.464 | 0.450 | 0.468 |
| invoices | 0.326 | 0.374 | **0.478** |

- **Field-flip test (mean change / top changed of 60):**

| Question | Run 10 | Run 9 | Run 7 |
|---|---|---|---|
| agent action | **0.225 / 34** | 0.168 / 4 | 0.163 / 0 |
| agent outcome | 0.652 / 60 | 0.669 / 60 | 0.758 / 60 |
| invoice | 0.011 / 0 | 0.025 / 2 | 0.005 / 0 |
| security | **0.098 / 5** | 0.053 / 0 | 0.022 / 1 |

- **Reading:**
  1. On the benchmark, 09c is run 9 within noise, slightly worse overall (0.453 against 0.461), worse on score and invoices. The encoder adds nothing measurable when the decoder reads the text.
  2. The field-flip test moved: the agent-action answer now changes in 34 of 60 cases (run 9: 4) and security in 5 (run 9: 0). The model reacts more to the deciding fields, but that did not turn into accuracy. Invoices still do not react at all.
  3. Two epochs are too many for the decoder at this learning rate: epoch 2 over-fits in every decoder run so far.
- **Decision:** the gated encoder–decoder is not worth pursuing at this size. Next: the choice-only test (`08b`, run 7's encoder settings on choice questions only, with the new choice data `v1_2` and two losses).

## Data v1_2 — 2026-10-25: v1_1 + 150 choice-only cases (K1–K3)

- **Why:** choice is run 7's weakest type on the benchmark (0.430). The choice-only test (`08b`) needs more choice questions. **Disclosure:** added after the benchmark showed choice is weak, as the invoice cases were; the cases are general (no benchmark content, workflow, field or wording was used).
- **Brief:** `data/signpost_d/brief_v2_2_choice.md`, built on `brief_v2.md` and `format_spec.md`. Every question is a `choice` question, 4–5 per case. Kind shares weighted towards the thin kinds: read ~20%, infer ~20%, compare ~25%, judge ~35%. Half the states JSON records. Domains: brief v2's list, split over the three batches.
- **Pipeline (as the invoices):** three Opus generators (50 cases each) → three labellers per batch (Opus cautious, Sonnet pragmatic, Fable neutral; averaged) → an Opus validator per batch, with the labellers' notes and the disagreement checks as "look closely" items.
- **Result:** 150 cases, 667 choice questions (read 134, infer 141, compare 178, judge 214); 75 JSON states; verdicts: 24 keep, 9 relabel, 7 fix, 0 drop; all three labellers agree on the top answer in 98.4% of questions; mean gold top 0.913; 0 format errors.
- **Notable validator fixes:** options that overlapped (K1-003, K2-002, K3-033), an impossible option (K1-002), an ambiguous day count (K2-025), a labeller who missed a fridge over its limit (K2-039), and splits the facts settle (K1-035, K1-044, K3-018, K3-043).
- **D_SET `v1_2`** = v1_1 (unchanged, first 1,650 lines) + these 150 cases: 1,800 cases, 3,367 choice questions in all. In `08b`, 15% of the K cases (22) join dev, split on their own, so the earlier dev cases stay as they were.
- **Build:** `data/signpost_d/v1_choice/build.py` (from the invoice build, plus a check that every question is a choice).

## Data v1_3 — 2026-10-25: v1_2 + 300 score-only cases (L1–L6)

- **Why:** for a score-only run after the choice-only test (`08b`), to see whether score questions also gain from training alone and from more data. **Disclosure:** added after the benchmark results by type, as the invoice and choice cases were; the cases are general (no benchmark content, workflow, field or wording was used).
- **Brief:** `data/signpost_d/brief_v2_3_score.md`, built on `brief_v2.md` and `format_spec.md`. Every question is a `score` question, exactly 4 per case, each on a different scale. Every instruction names its quantity and level 0 is the least of it (the score-consistency rule); levels are `"Name: description"` with thresholds between neighbours; 3/4/5 levels about 40/35/25%; the lowest and highest levels should win about as often as the middle ones. Kinds about read 20%, infer 20%, compare 25%, judge 35%; half the states JSON. Domains: brief v2's list, split over six batches.
- **Pipeline (as the choice cases):** six Opus generators (50 cases each) → three labellers per batch (Opus cautious, Sonnet pragmatic, Fable neutral; averaged) → an Opus validator per batch with `validator_score_consistency.md` as well, and the labellers' notes plus the disagreement checks as "look closely" items.
- **Result:** 300 cases, 1,200 score questions (read 244, infer 233, compare 316, judge 407); 150 JSON states; verdicts: 49 keep, 49 fix, 24 relabel, 0 drop; all three labellers agree on the top level in 96.4% of questions; mean gold top 0.874 (the choice cases: 0.913); 19.8% of questions have a gold top under 0.85; 0 format errors.
- **What the validators fixed:** mostly values on or beside a level boundary that the wording did not settle (which log row, which reading, which base for a percentage, how days are counted), neighbouring levels that overlapped, and levels that left a gap. Score-consistency fixes: one reversed scale (L6-047 q3) and five instructions reworded to name the quantity the levels follow (L2-031, L3-019, L3-038 ×2, L4-001, L4-040, L6-009). One state error (L3-028: a weekday count that does not match the dates) was handled by rewording the instruction; the case may be worth regenerating.
- **D_SET `v1_3`** = v1_2 (unchanged, first 1,800 lines) + these 300 cases: 2,100 cases; 3,559 score, 3,367 choice and 2,765 true/false questions. A score-only run must split the L cases on their own (as `08b` does for I and K) so the earlier dev cases stay as they were.
- **Build:** `data/signpost_d/v1_score/build.py` (from the choice build; checks every question is a score).

## 08b run 11 — 2026-10-25: run 7's encoder on choice questions only (v1_2)

- **Setup:** `08b_signpost_d_choice.ipynb`. Run 7's settings (start `skamalj/signpost-one-pass`, LoRA r 64, `HEAD_EXTRA` 2, seed 42), trained, checked and selected on **choice questions only**: 2,846 training questions (1,428 cases), 521 dev questions (v1 386, invoices 33, new K cases 102). 6 epochs, cross-entropy (variant `BRIER_W = 0`).
- **Dev by epoch (choice):** 0.680 / KL 0.553 → **0.678 / 0.523 (best, epoch 2)** → 0.706 / 0.532 → 0.699 / 0.584 → 0.695 / 0.618 → 0.703 / 0.572. Epochs 3–6 only memorised (the loss kept falling, dev KL rose).
- **Dev parts at the best epoch:** v1 choice 0.684 / KL 0.496, invoices 0.667 / 0.661, K cases 0.657 / 0.580. v1 + invoices together (419 questions) ≈ 0.683 / 0.51, level with run 7's choice dev (0.690 / 0.488).
- **Benchmark (T = 1; the fitted choice temperature was 1):**

| `type=choice` | Accuracy | KL | Brier | ECE |
|---|---|---|---|---|
| Run 7 (all types, 6,669 questions) | **0.430** | **0.601** | **0.281** | **0.140** |
| **Run 11 (choice only, 2,846)** | 0.375 | 0.811 | 0.361 | 0.251 |

  Overall 0.3775 / KL 0.657 (true/false 0.490 and score 0.295, never trained). Grounded tests: E12 127/170, IND 205/300, IND2 164/200.
- **Variant 2 (`BRIER_W = 1`) stopped by hand** after epoch 1 (dev 0.633 / KL 0.610, behind variant 1's epoch 1): the choice-only setup had already lost 5.5 points, so the GPU went to the comparison below.
- **Reading:** level with run 7 on our own choice questions, 5.5 points worse on the benchmark's. The run changed two things at once, the question types and the amount of data (57% fewer questions), so it cannot say which caused the drop. **`08c`** separates them: all three types cut to the same 2,846 questions (1,379 cases; 1,081 choice, 926 true/false, 839 score).

## 08c run 12 — 2026-10-26: all three types, cut to 08b's 2,846 questions (type mix or amount?)

- **Setup:** `08c_signpost_d_mix_vs_amount.ipynb`, `TRAIN_MODE = "all_subsampled"`. As run 11 (run 7's settings, v1_2, 6 epochs, cross-entropy), but the 2,846 training questions are drawn from all three types (seed 42): 1,081 choice, 926 true/false, 839 score, from 1,379 cases (run 11: 2,846 choice from 1,428 cases). Dev: the same dev cases, all three types (1,257 questions).
- **Dev:** best epoch 2 again (0.674 / KL 0.506); later epochs gained accuracy (0.695 at 6) but lost KL. Choice dev 0.668 / KL 0.551 (run 11: 0.678 / 0.523).
- **Benchmark, `type=choice` (T per type; choice temperature 1):**

| | Training questions | Choice questions | Accuracy | KL | Brier | ECE |
|---|---|---|---|---|---|---|
| Run 7 (all types, v1_1) | 6,669 | 2,281 | **0.430** | 0.601 | 0.281 | 0.140 |
| Run 11 (choice only) | 2,846 | 2,846 | 0.375 | 0.811 | 0.361 | 0.251 |
| **Run 12 (all types, cut)** | 2,846 | 1,081 | 0.353 | **0.482** | **0.244** | **0.114** |

- **Benchmark overall:** 0.441 / KL 0.510 / Brier 0.280 / ECE 0.163 (run 7: 0.471 / 0.548 / 0.300 / 0.182). By type: true/false **0.633** / KL 0.292 (the best of any run; run 7 0.628), score 0.362, choice 0.353. Workflows: agent trace 0.314, customer service 0.556, invoices 0.410, security 0.484. Grounded tests: E12 135/170, IND 236/300, IND2 178/200 (all better than run 11).
- **Reading:**
  1. **Choice accuracy follows the amount of data**, not the type mix: with 2,846 questions both runs sit at 0.35–0.38 (one standard error on 600 questions is about 0.02); run 7, with 6,669, reaches 0.43. Run 12 got there with only 1,081 choice questions, so questions of the other types count for choice accuracy almost as much as choice questions do.
  2. **The type mix makes the probabilities much better:** choice KL 0.482 against 0.811 for choice only, and better than run 7's 0.601 with less than half the data; the best choice Brier and ECE of any run. Training on one type makes the model over-confident on it.
  3. **So experts per type are not supported:** separating the types loses calibration and gains nothing in accuracy. More data across all types is the lever.
- **Next:** run 7's setup on all of v1_3 (2,100 cases, about 8,000 training questions), with the L cases split into dev on their own, and 3 epochs (the best epoch has been 2 in every run with this start).

## 08d run 13 — 2026-10-26: all three types on v1_3 (the new choice and score data)

- **Setup:** `08d_signpost_d_all.ipynb`, defaults (`TRAIN_MODE = "all"`, `ORDINAL_HEAD` and `LEVEL_POSITIONS` off). Run 7's settings on **v1_3** (v1_3 now 2,099 cases: L3-028 dropped for a date error in its state, `v1_score/validation/validation_Lzz_manual.jsonl`): 8,254 training questions (score 3,049, choice 2,846, true/false 2,359), 3 epochs, cross-entropy. Dev 1,433 questions from 313 cases (all 269 earlier dev cases kept, 44 L cases added). 67.8 min on a T4.
- **Training:** per-type loss at the end of epoch 3: true/false 0.31, choice 0.59, score 0.67. Dev: 0.671 / KL 0.513 → **0.707 / 0.456 (best, epoch 2)** → 0.718 / 0.514.
- **Dev at the best epoch:** choice 0.708 / KL 0.485, true/false 0.793 / 0.311, score 0.636 / 0.538. v1 part **0.724 / KL 0.417** (run 7: 0.713 / 0.430, the best v1 dev so far); invoices 0.657, K 0.775, L 0.591 / 0.653.
- **Benchmark (T per type; temperatures choice 1, true/false 1.25, score 1):**

| | Accuracy | KL | Brier | ECE | choice | true/false | score |
|---|---|---|---|---|---|---|---|
| Prior | 0.470 | **0.347** | | | | | |
| Run 7 (v1_1) | 0.471 | 0.548 | 0.300 | 0.182 | 0.430 | 0.628 | 0.384 |
| Run 9 (decoder) | 0.461 | **0.491** | **0.277** | **0.153** | **0.452** | 0.525 | 0.420 |
| Run 12 (v1_2, cut) | 0.441 | 0.510 | 0.280 | 0.163 | 0.353 | **0.633** | 0.362 |
| **Run 13 (v1_3, all)** | **0.481** | 0.551 | 0.299 | 0.186 | 0.412 | 0.605 | **0.440** |

  Workflows: agent trace **0.464** (best; run 9 0.432), customer service 0.538, invoices 0.418 (KL 0.914), security **0.504** (best). Grounded tests: E12 141/170, IND 242/300, IND2 186/200 (best of runs 11–13).
- **Reading:**
  1. **The best accuracy so far, and the first run above the prior** (0.481 against 0.470; one standard error on 2,000 questions is about 0.011, so it is a small step).
  2. **The score data worked:** score 0.440 against run 7's 0.384 (+5.6 points), the best of any run including the decoder.
  3. Choice (0.412) and true/false (0.605) sit slightly under run 7, within about one standard error.
  4. **Calibration slipped:** KL 0.551 against run 12's 0.510; the predictions are sharper (535 benchmark tops in 0.8–0.9). Invoices are the worst case: KL 0.914, confident and wrong.
- **Next:** run 14 = the same with `ORDINAL_HEAD = True` (score questions only), compared with this run's score numbers.

## 08d run 14 — 2026-10-26: `ORDINAL_HEAD = True` (stopped at step ~800)

- **Setup:** as run 13 with `ORDINAL_HEAD = True`: for score questions, s = the published head's expected level over the levels, σ = softplus(a new linear layer on the mean level vector) + 0.1 (starting at 1.0 level), probabilities = logistic shares between k ± 0.5; `ORD_LR` 1e-3.
- **Stopped by hand in epoch 1:** every type's loss rose after step 400, not only score's (run 13 at the same steps in brackets): step 800, choice 1.30 (0.97), true/false 0.70 (0.61), score 1.32 (1.09); collapse check at step 400, dev KL 0.531 (0.468).
- **Diagnosis:**
  1. **A design flaw:** s was computed from the shared published head, which also scores every choice and true/false option. Score questions then trained that head only on the average of its level scores, which allows extreme scores, and the change hurt the other types. The spread layer also fed gradient into the encoder through the mean level vector.
  2. **Too slow a start:** σ began at 1.0 level, where even a perfect position gives flat answers with extra weight on the end levels (the logistic tails); Adam at 1e-3 needs about 1,900 steps to bring σ down to 0.3.
- **If retried:** a separate small layer for s on the level vectors (the shared head untouched), σ starting near 0.5, a faster learning rate for both. **Next instead:** run 15, `LEVEL_POSITIONS = True` alone (input text only; no change to the heads or the gradients).

## 08d run 15 — 2026-10-26: `LEVEL_POSITIONS = True` (best run so far)

- **Setup:** as run 13 (v1_3, all types, 8,254 training questions, 3 epochs, cross-entropy) with `LEVEL_POSITIONS = True`: every score level is shown as "level i of n (lowest/highest): <level text>", on our data, the grounded tests and the benchmark. Nothing else changed. 67.3 min.
- **Training:** per-type losses tracked run 13 within about ±0.03 at every logged step. Dev: 0.650 / KL 0.525 → **0.703 / 0.474 (best, epoch 2)** → 0.706 / 0.537. Temperatures fitted on dev: 1.25 for all three types (run 13: choice 1, true/false 1.25, score 1).
- **Dev at the best epoch (T per type):** all 0.703 / KL 0.467; choice 0.712 / 0.498, true/false 0.769 / 0.332, score 0.640 / 0.544. Parts: v1 0.717 / 0.434, invoices 0.717 / 0.463, K 0.745 / 0.504, L 0.585 / 0.645. **On dev, level with run 13.**
- **Benchmark:**

| | Accuracy | KL | Brier | ECE | choice | true/false | score |
|---|---|---|---|---|---|---|---|
| Prior | 0.470 | 0.347 | | | | | |
| Run 9 (decoder) | 0.461 | 0.491 | 0.277 | 0.153 | 0.452 | 0.525 | 0.420 |
| Run 13 (v1_3) | 0.481 | 0.551 | 0.299 | 0.186 | 0.412 | 0.605 | 0.440 |
| **Run 15, T = 1** | **0.5165** | 0.458 | 0.240 | 0.110 | 0.453 | 0.645 | 0.468 |
| **Run 15, T per type** | **0.5165** | **0.402** | **0.216** | **0.065** | 0.453 | 0.645 | 0.468 |

  By type (T per type): choice 0.453 / KL 0.574, true/false **0.645** / 0.272, score **0.468 / 0.372** (run 13: 0.440 / 0.607). Workflows: agent trace 0.474, customer service **0.618**, invoices **0.482** (KL 0.632; run 13 0.914), security 0.492. Grounded tests: E12 135/170, IND 218/300, IND2 174/200 (score items lower than run 13).
- **Reading:**
  1. **The best run by a wide margin:** accuracy 0.5165 (+3.5 points on run 13, +4.6 on the prior), KL 0.402 (the best of any run; the decoder had 0.491), Brier 0.216, ECE 0.065. Close to the leaderboard's d3-lite 0.8B (0.531).
  2. **Score improved most, as intended:** 0.440 → 0.468, KL 0.607 → 0.372.
  3. **But choice (+4.1) and true/false (+4.0) improved too,** although their input did not change, and dev did not move. Part of the gain is probably run-to-run variation (one standard error is about 0.02 per type), so **a repeat with another seed is needed** before treating the whole jump as the effect of level positions. The positions may also help the shared encoder by making score questions less confusing; a repeat would show it.
  4. KL gains also come from the fitted temperature (1.25 everywhere): at T = 1 the KL is 0.458.
- **Dev predictions saved** for the failure analysis: `experiments/analysis/run15_dev_preds.json` (1,433 questions: id, qid, type, probabilities in option order).

## Dev failure analysis — 2026-10-26 (run 15's dev predictions; our own data only)

Script: scratchpad `ana/fail.py` on `experiments/analysis/run15_dev_preds.json` joined with v1_3.

- **Misses are real errors, not unclear labels:** true/false 94 wrong (0 with a split gold, 66 confident and wrong), choice 150 (13 split, 48 confident), score 182 (14 split, 33 confident). About 95% of misses sit on a clear gold.
- **Compare is the weakest kind in every type:** true/false read 0.924 / judge 0.842 / infer 0.712 / **compare 0.650**; choice read 0.817 / judge 0.742 / infer 0.653 / **compare 0.560**; score judge 0.687 / infer 0.637 / read 0.620 / **compare 0.520**.
- **Two failure patterns (read case by case):**
  1. **No calculation:** 7 of 252 returns (2.8%) read as above a 5% limit (G09-009); 70% of 46 against 40 pickers (G19-013); 17:01:47 against a 17:00 deadline read as 30–60 minutes late (D-041); the average of 79 and 76 (G01-026); 14:15 to 14:58 read as 16–30 minutes (G02-032); an amount exactly on an inclusive band (I1-019); disk growth against a backup time (G16-027).
  2. **Surface cues over the stated rule:** "leaks" → half refund though faulty items get a full refund in any state (K2-034); the cheaper hotel though the rule requires the same star rating or higher (G17-044); "escalate" though no signature means no protection (G14-017); "compromised" though the log shows the user's own device (G06-039); noise that returned → full night rather than the rule's 50% (G02-042). True/false leans to "true" on alarming statements: 54 of 94 errors are "true" for a false gold; gold-false accuracy 0.714 against gold-true 0.816.
- **Smaller patterns:** score misses are mostly one level (140 of 182), more often too high (113) than too low (69), and pulled off the end levels (78); 5-level scales 0.514 against 3-level 0.723. Choice falls with more options (2: 0.808 … 6: 0.595) and when the answer is the last option (0.639). No difference by form (JSON 0.643–0.775 against text 0.638–0.762) or state length.
- **Matches the benchmark's field-flip test:** the model reacts to signal words, not to the numbers and rule clauses that decide the answer.
- **Next options:** (1) contrastive twin cases (the same case with one number or one rule condition changed so the answer flips), our own data, motivated by this dev analysis; (2) a decoder that writes a short working-out before answering, for the calculations an encoder cannot learn; (3) a seed repeat of run 15 to confirm its jump.

## Data v1_4 — 2026-10-26: v1_3 + 200 twin cases (training only)

- **Why:** the dev failure analysis of run 15 (our own dev data) showed the model follows signal words instead of the deciding number or rule clause. **Twins** make that shortcut useless: a copy of a case with exactly one deciding detail changed (a number, one rule clause, or one fact), so at least one answer flips while the questions stay word for word the same.
- **Brief:** `data/signpost_d/brief_v2_4_twins.md`; validator addendum `validator_twins.md` (one change only, the flip is real, no threshold ties, the questions still fit the twin).
- **Batches:** TB1, TB2 = twins of 100 v1_3 **training** cases with compare questions (55 v1, 20 L, 15 K, 10 invoices; 36 domains); TA1, TA2 = 50 new base cases and their twins. Labellers saw the new pairs in shuffled order (no base next to its twin). `prep_val_twins.py` gave validators each twin's base and gold and flagged every question whose labelled answer did or did not flip against the generator's change note.
- **Result:** 200 cases (150 twins), 867 questions (true/false 364, choice 290, score 213; compare 401, judge 207, infer 160, read 99); 99 JSON states; verdicts 19 keep, 23 fix, 7 relabel, 0 drop; all three labellers agree on the top in 98.6%; mean gold top 0.921. Every twin has a real one-detail change; about 265 questions flip against their base. Validators fixed twins whose options quoted a base figure or premise that no longer held (TB1-019, 020, 021, 050; TB2-011, 019, 027, 031, 035, 046, 039, 033) and one labeller miscalculation (TB2-044).
- **D_SET `v1_4`** = v1_3 (unchanged, first 2,099 lines) + these: 2,299 cases. **The T cases are training only** (`TRAIN_ONLY = ("T",)` in 08d), so the dev set is exactly runs 13 and 15's (313 cases; checked), and no TB base is in dev. Training questions: 9,121 (score 3,262, choice 3,136, true/false 2,723).
- **Build:** `data/signpost_d/v1_twins/build.py`.
- **08d regenerated for run 16:** `D_SET = "v1_4"`, `LEVEL_POSITIONS = True` (run 15's setting), the `TRAIN_ONLY` group; everything else as run 15. Compare with run 15 (0.5165 / KL 0.402), and on dev the compare questions (run 15: true/false 0.650, choice 0.560, score 0.520).

## Decoder plan, 2026-10-26: training-time working-outs dropped; Qwen3.5-0.8B chosen

- **Working-outs (option 1, "distilling step by step"): dropped.** The plan was to train the decoder on a second, training-only task (write a short working-out) while answering stays one pass. The working-out texts were to be written by Opus agents from our gold (`brief_working.md`, 40 batches prepared under `v1_4_working/`). Every writer that started was stopped by Anthropic's safeguards (`reasoning_extraction`: model-written reasoning traces for training another model). The approach is not pursued in any rewording; no working-out was written, and neither the brief nor the batches are committed. What stays open: working-outs written by people, and reading tasks built by code from the states (field values, which of two numbers is larger), which contain no model reasoning.
- **Small decoders on Hugging Face (API survey, open text models 0.2–1.6 B, recent):** Qwen/Qwen3.5-0.8B (0.87 B incl. a 12-layer vision tower, Apache-2.0, Feb 2026, 3.4 M downloads; a hybrid of 18 linear-attention and 6 full-attention layers); Qwen/Qwen3-0.6B (run 9); openbmb/MiniCPM5-1B (1.08 B, Apache-2.0); LiquidAI LFM2.5-350M / 1.2B (own licence); tiiuae Falcon-H1-Tiny-R-0.6B; ibm-granite granite-4.0-350m / h-1b; Gemma 3 270M / 1B (gated). No Qwen3.6–3.8 or Gemma 4 model under 1 B (the "Qwen3.8" entries are speculative-decoding draft heads). **Chosen: Qwen3.5-0.8B**, supported by the pinned transformers 5.17.0 (`Qwen3_5ForCausalLM`, which `AutoModelForCausalLM` maps for this checkpoint).
- **`10_signpost_d_qwen35.ipynb`:** 09's decoder mode (run 9's prompt and label-token readout, LoRA r 16, 2 epochs) with Qwen3.5-0.8B on v1_4, 08d's dev split (same 313 dev cases as runs 13–16; twins training only), level positions on score questions, LoRA on attention, MLP and linear-attention projections (never the vision tower), a fallback to the full multimodal model if the text-only load misses any language weight, and the dev predictions dumped.

## Data v1_numq — 2026-10-26: number questions built by code (training only)

- **Why:** the dev failure analysis (run 15) showed the model does not read or compare the deciding number. These questions train exactly that, with exact golds and no model-written text.
- **How:** `data/signpost_d/v1_numq/build.py` reads the JSON states of v1_4's **training** cases (never a dev case) and writes up to 3 questions per case from templates: a value above a threshold (true/false), which of two comparable values is larger (same-unit siblings, or the same field in two list entries), date order and day gaps, the highest entry in a list of records (choice), and a size band (score, 4 levels, lowest first). Thresholds never sit on the value; ids, codes, phone numbers and years are skipped. Golds about 0.95 on the computed answer. Sums were dropped (too often meaningless), and pairs restricted to comparable values, after reading samples.
- **Result:** 928 cases (ids `N-<source id>`), 2,529 questions: true/false 1,635 (760 true, 875 false), score 816, choice 78; all System One form.
- **`08f_signpost_d_numq.ipynb`** (from 08d, run 16's settings): `NUMQ_MODE = "warmup"` (one pass over the number questions, then 2 real epochs; collapse check on real data after the warm-up; only real epochs kept), `"mix"` (20% of every epoch), `"off"` (control). Dev unchanged (313 cases); dev predictions dumped. Run 17 = warm-up; run 18 = mix.

## 08d run 16 — 2026-10-26: run 15 + the twins (v1_4) — benchmark down, dev unchanged

- **Setup:** as run 15 (level positions, 3 epochs) on v1_4 (9,121 training questions incl. the 200 twin cases, training only). Seed 42 collapsed at step 400 (losses rose after the learning rate peaked at step ~200; dev KL 0.6640 = uniform); the automatic retry with **seed 1042** trained normally (collapse check KL 0.467). 72.2 min.
- **Dev (best epoch 2):** 0.708 / KL 0.467 (run 15: 0.703 / 0.467); choice 0.726, true/false 0.759, score about 0.64; v1 0.722 / 0.437, invoices **0.737** / 0.428, K 0.716, L 0.602. Level with or better than run 15 everywhere.
- **Benchmark (T per type):** **0.445 / KL 0.534 / Brier 0.293 / ECE 0.174** (run 15: 0.5165 / 0.402 / 0.216 / 0.065); choice 0.395, true/false 0.517, score 0.429; invoices 0.340 (KL 0.906). Down 7 points across every type and workflow.
- **Reading:** run 16 differs from run 15 in two things, the twins and the seed. Dev did not move while the benchmark dropped 7 points; runs 13 → 15 showed the same pattern on a smaller scale (choice and true/false +4 points with unchanged inputs and dev). **Transfer to the benchmark is unstable across training paths,** so single-run differences of several points cannot be attributed, and run 15's 0.5165 may be partly a lucky draw (a selection effect if chosen by benchmark score). The dev dump was not run, so no compare-question breakdown.
- **Next (isolating the twins):** run 15's setup again on v1_3 (no twins) with seed 1042. Near 0.45 → the seed did it; near 0.51 → the twins hurt transfer. Then weight averaging across seeds or epochs, and interpolation towards the start weights (WiSE-FT), as ways to make transfer stable. Run 17 (number questions) waits until the noise level is known.

## 08d run 15b — 2026-10-26: run 15's configuration, seed 1042 (incomplete; split not pinned)

- **Setup:** run 15's configuration (v1_3, level positions, 3 epochs) with `SEED = 1042`. **Flaw found:** `dev_split` shuffled with `SEED`, so changing the seed also changed the dev cases (1,438 dev questions against 1,433; train 8,249 against 8,254). Its dev numbers are therefore not comparable with run 15's.
- **Training finished** (70.9 min; best epoch 2, dev 0.708 / KL 0.467 on its own dev cases); **the Kaggle session died** (network) during the measurements, so there is no benchmark score.
- **Fix:** the dev split now uses a fixed `SPLIT_SEED = 42` (08f, 10; 08d next). Runs 15c and 15d (seeds 1042 and 2042, split pinned) replace this run as the seed test.

## 08d run 15c — 2026-10-26: run 15's configuration, seed 1042, split pinned — collapsed after the check

- **Setup:** run 15's configuration exactly (v1_3, no twins, level positions, 3 epochs), dev split pinned (train 8,254 / dev 1,433, as run 15), training seed 1042 (the first of `SEED_VARIANTS = [1042, 2042]`).
- **Collapsed after passing the step-400 check** (dev KL 0.531): at step 600 every type's loss jumped (true/false 0.57 → 0.65 → 0.69 = ln 2, choice 1.04 → 1.26, score 1.15 → 1.33) and stayed at the uniform level; epoch 1 dev 0.380 / KL 0.782. Stopped by hand in epoch 2.
- **Reading:** with run 16's first attempt (seed 42 on v1_4), that is two collapses near the learning-rate peak, one with no twins at all. **The configuration itself is fragile; the twins did not cause the collapse.** A run that nears collapse and recovers can pass dev yet transfer differently, which may explain the benchmark swings (runs 13–16).
- **Next:** stabilise training (LoRA LR 2e-4 → 1e-4, head 5e-4 → 2.5e-4, warm-up 6% → 15%, a second collapse check at the end of epoch 1), then the seed test (42, 1042, 2042) on that setup.

## 08d stable seeds — 2026-10-26: run 15's configuration with stabilised training, 3 seeds

- **Setup:** run 15's configuration (v1_3, level positions, 3 epochs, cross-entropy) with **LoRA LR 1e-4, head LR 2.5e-4, warm-up 15%** and a second collapse check after epoch 1; dev split pinned (313 cases / 1,433 questions); seeds 42, 1042, 2042 in one session with per-epoch checkpoints in /kaggle/working (seed 42 resumed after a lost session, from its epoch-1 checkpoint, as designed). About 72 min per seed; no collapse; best epoch 2 for every seed.

| Seed | Dev acc / KL | Bench acc | Bench KL | Brier | ECE | choice | true/false | score |
|---|---|---|---|---|---|---|---|---|
| 42 | 0.705 / 0.464 | 0.4455 | 0.503 | 0.274 | 0.176 | 0.387 | 0.600 | 0.374 |
| 1042 | 0.700 / 0.462 | 0.461 | 0.558 | 0.314 | 0.176 | 0.410 | 0.552 | 0.431 |
| 2042 | 0.708 / 0.454 | 0.4565 | 0.521 | 0.296 | 0.170 | 0.420 | 0.543 | 0.419 |
| **Mean** | **0.704 / 0.460** | **0.454** | **0.527** | **0.295** | **0.174** | 0.406 | 0.565 | 0.408 |

- **Reading:**
  1. **The stable configuration is consistent:** benchmark accuracy 0.4455–0.461 (range 1.6 points), dev 0.700–0.708. Our reliable level is **0.454 ± ~0.01**, below the prior (0.470 / KL 0.347).
  2. **The types trade places between seeds** (true/false 0.543–0.600, score 0.374–0.431), while the total stays flat: a case for averaging the seeds' weights.
  3. **Run 15's 0.5165 was an outlier.** One caution: the completed old-learning-rate runs scored 0.481 (13), 0.5165 (15) and 0.445 (16), mean 0.481, above the stable mean; the higher rate may transfer better when it does not collapse. Not established; two runs collapsed at that rate.
- **Saved:** the three seeds' weights (LoRA, head, config) in Kaggle's /kaggle/working/checkpoints/all-pos-v1_3-lr0.0001-head0.00025-warm0.15-ep3/seed*/; dev predictions in `experiments/analysis/stable_seed*_dev_preds.json`.
- **Next:** a weight-averaged model of the three seeds (and WiSE-FT towards the start weights), chosen on dev.

## 08g — 2026-10-26: weight-averaged model of the three stable seeds (no training)

- **Method:** each seed's full LoRA weight change (B @ A × α/r) averaged over seeds 42, 1042, 2042 (112 adapted modules) and added to the start weights; heads averaged. WiSE-FT α ∈ {1.0, 0.75, 0.5} chosen on dev KL → **α = 1.0**. The seeds' weight changes are nearly orthogonal (cosine 0.06 between seeds 42 and 1042), yet their average is better than each.
- **Dev:** α 1.0 **0.712 / KL 0.438** (single seeds 0.700–0.708 / 0.454–0.464; the best dev KL so far); α 0.75 0.695 / 0.464; α 0.5 0.646 / 0.524. Parts: v1 0.728 / 0.404, invoices 0.737, K 0.696, L 0.608. Grounded tests **E12 149/170, IND 248/300, IND2 184/200** (best of any run).
- **Benchmark (T per type), scored once for the chosen α:**

| | Accuracy | KL | Brier | ECE | choice | true/false | score |
|---|---|---|---|---|---|---|---|
| Seeds, mean | 0.454 | 0.527 | 0.295 | 0.174 | 0.406 | 0.565 | 0.408 |
| Seeds, best of three on each measure | 0.461 | 0.503 | 0.274 | 0.170 | | | |
| **Average of the three (soup)** | **0.462** | **0.497** | 0.280 | **0.158** | 0.418 | 0.585 | 0.403 |
| Prior | 0.470 | 0.347 | 0.189 | 0.088 | | | |

  Workflows: agent trace 0.452, customer service 0.586, invoices 0.352 (KL 0.843), security 0.458.
- **Reading:** a small, consistent gain with no extra latency: accuracy at the top of the seed range (+0.8 over the mean, within noise), KL and ECE better than every seed. Still below the prior on both. Saved as `checkpoints/soup/…/soup.pt` (0.69 GB, in Kaggle's persistent folder) for continued training; dev predictions in `experiments/analysis/soup3_dev_preds.json`.

## Decoder line (path A) — 2026-10-26: notebook 11

- **`11_signpost_d_decoder.ipynb`:** one notebook for A1–A5. `MODE = "zeroshot"` scores untrained models; `"train"` fine-tunes each model for each seed. Prompt: each model's chat template (thinking off), a short system line, the case and the question with lettered options (score levels with positions); probabilities from the next-token logits of the letters. Training: LoRA α = r (attention, MLP, linear-attention projections), LoRA weights fp32, fp16 autocast, clipping with the gradient norm logged, warm-up 15%, collapse checks at a step and after epoch 1, best epoch on dev KL, per-epoch checkpoints with resume; 1.7 B and 4 B in 4 bit (QLoRA). Measurement: dev by type and by kind, benchmark with case-level 95% bootstrap intervals, each test scoring counted in `checkpoints/test_touches.json`.
- **First session (A1), zero-shot:** `skamalj/signpost-one-pass` as published (reference: our encoders' start), Qwen3-0.6B, Qwen3.5-0.8B, Qwen3-1.7B (4-bit), Qwen3-4B (4-bit); v1_3 dev split.
- **Working rules adopted from the review:** three seeds or no claim; test split only at decision points (counted); report by question kind. The style audit of the benchmark and 4B-model relabelling were declined (zero-shot kept strict).

## 11 A1 — 2026-10-27: zero-shot baselines (no training)

- **Setup:** notebook 11, `MODE = "zeroshot"`, v1_3 dev split (313 cases / 1,433 questions), level positions on; per-type temperature fitted on dev; benchmark with case-level 95% intervals (test touches counted). One T4 session, 15:21–16:07 (Qwen3-4B alone about 20 minutes for dev + benchmark). Qwen3.5-0.8B ran on the slow reference kernels (no `causal_conv1d` / `flash-linear-attention` on the T4 image).

| Model (untrained) | Dev acc / KL | Bench acc [95% CI] | Bench KL [95% CI] | Brier | ECE | choice | true/false | score |
|---|---|---|---|---|---|---|---|---|
| signpost-one-pass (published) | 0.460 / 0.745 | 0.4295 [0.407, 0.451] | 0.433 [0.417, 0.449] | 0.239 | 0.076 | 0.322 | 0.577 | 0.400 |
| Qwen3-0.6B | 0.453 / 0.740 | 0.314 [0.296, 0.332] | 0.514 [0.497, 0.531] | 0.266 | 0.139 | 0.302 | 0.535 | 0.158 |
| Qwen3.5-0.8B | 0.452 / 0.745 | 0.3845 [0.367, 0.403] | 0.470 [0.452, 0.487] | 0.247 | 0.078 | 0.302 | 0.557 | 0.318 |
| Qwen3-1.7B (4-bit) | 0.426 / 0.803 | 0.3975 [0.378, 0.418] | 0.529 [0.510, 0.547] | 0.282 | 0.163 | 0.285 | 0.587 | 0.340 |
| **Qwen3-4B (4-bit)** | **0.628 / 0.619** | **0.499 [0.476, 0.525]** | 0.557 [0.531, 0.582] | 0.296 | 0.200 | **0.582** | 0.505 | 0.433 |

- **Reading:**
  1. **Untrained Qwen3-4B beats every model we have trained on accuracy** (0.499 against the encoder seeds' 0.454 and the soup's 0.462; intervals do not overlap the seeds' mean) and is the only zero-shot model above the prior's accuracy (0.470). Its strength is choice (0.582, against our best 0.453); its true/false is at chance (0.505) and it is over-confident (ECE 0.20, many probabilities at 1.0), so KL is poor.
  2. **Below 4B, untrained decoders are poor** (0.31–0.40), below the untrained Signpost encoder (0.4295). Fine-tuning carried Qwen3-0.6B from 0.314 to 0.461 in run 9 (+15 points), so training is worth a lot at these sizes.
  3. **A jump between 1.7B and 4B** on dev (0.43 → 0.63) and the benchmark (0.40 → 0.50): reading ability arrives with size, matching the leaderboard's 2–4B band.
- **Next (A2):** fine-tune Qwen3-4B (4-bit + LoRA) on v1_3, then Qwen3-1.7B, same dev split and settings, so the comparison with the encoder and run 9 changes only the model.

## 11 A2 attempt 1 — 2026-10-27: Qwen3-4B fine-tune, stopped at step 400 for speed

- **Setup:** Qwen3-4B 4-bit (nf4, fp16 compute) + LoRA r 16, LR 1e-4, batch 2 × accumulation 4, v1_3, 2 epochs planned (2,064 optimizer steps), one T4.
- **Speed:** ~10.2 s per optimizer step (8 questions): ~6 h for two epochs. Too slow; stopped by choice after the collapse check, no checkpoint kept.
- **Training signal:** loss 1.49 (step 100) → 0.88 → 0.87 → 0.82 (step 400); gradient norm mean 8.3 (max 34) in the first 100 steps, then 2.7–3.2 (max ~7.6). **Collapse check at step 400: dev KL 0.361 on 300 dev questions (uniform 0.664)**, no temperature. For reference, untrained 4B dev KL 0.619 (full dev, with temperature); best encoder dev KL 0.438 (soup). Not a like-for-like number, but a strong early sign.
- **Next:** rebuild notebook 11 for speed: 1 epoch (decoders over-fitted in epoch 2 in runs 9 and 10), one pass per case (all of a case's questions after one copy of the state, letters read before a fixed placeholder; ~2.6× fewer tokens), fp16 weights instead of 4-bit (no dequantisation; ~11–12 GB peak), and both T4s (one seed per GPU via accelerate's notebook_launcher).

## 11 A2 — 2026-10-27: Qwen3-4B fine-tuned (fp16, one pass per case, 2 GPUs, 1 epoch), seed 42

- **Setup:** notebook 11 (commit 2164468): Qwen3-4B in fp16 + LoRA r 16 (α = r, fp32 LoRA weights, fp16 autocast), LR 1e-4, warm-up 15%, **1 epoch**, v1_3, level positions; **one pass per case** (state once, questions numbered, answers read after "n:" with fixed "_" placeholders; question order and choice/true-false options shuffled per case); **data-parallel on 2 × T4** (1 case per GPU per step, LoRA gradients averaged; 893 steps). Peak 9.5 GB per GPU. **38.9 min of training** (~2.5 s per step of ~9 questions; ~4.5× faster per question than attempt 1), about 45 min for the whole run.
- **Training:** loss 1.28 (step 100) → 0.86 → 0.78 → 0.81 → 0.76 → 0.84 → 0.74 → 0.79 → 0.70 (step 893); gradient norm mean 5.8 then 2.5–3.2 (max 21.5 in the first 100 steps, otherwise ≤ 15.8). Collapse check at step 400: dev KL 0.289 (uniform 0.664).
- **Dev (T per type):** **0.780 / KL 0.326** / Brier 0.209 / ECE 0.044; choice 0.806, true/false 0.825, score 0.717. By kind: read 0.928, judge 0.814, infer 0.725, **compare 0.639**.
- **Benchmark (T per type), test touch 6:**

| | Accuracy [95% CI] | KL [95% CI] | Brier | ECE | choice | true/false | score |
|---|---|---|---|---|---|---|---|
| **Qwen3-4B fine-tuned, seed 42** | **0.5655 [0.541, 0.591]** | **0.330 [0.310, 0.350]** | 0.188 | 0.093 | 0.598 | 0.618 | 0.501 |
| Qwen3-4B untrained (A1) | 0.499 | 0.557 | 0.296 | 0.200 | 0.582 | 0.505 | 0.433 |
| Encoder soup (08g) | 0.462 | 0.497 | 0.280 | 0.158 | 0.418 | 0.585 | 0.403 |
| Prior | 0.470 | 0.347 | 0.189 | 0.088 | | | |

  Workflows: agent trace 0.538, customer service 0.662, **invoices 0.434 (KL 0.442, ECE 0.260)**, security 0.628.
- **Reading:**
  1. **First model above the prior on both accuracy and KL**, and above d3-lite (0.8B, 0.531); below d3-nano (2B, 0.629). Fine-tuning added 6.6 points over the untrained 4B and fixed its calibration (ECE 0.20 → 0.09, KL 0.557 → 0.330).
  2. **Dev and benchmark moved together** for the first time (dev 0.70 → 0.78 against the encoders; benchmark 0.46 → 0.57).
  3. One seed only: not yet a claim under the two-seed rule.
  4. Compare questions remain the weak kind; invoices the weak workflow.
- **Next:** 2 epochs from scratch on seed 42 (best epoch by dev KL; loss still falling at the end of epoch 1), then a second seed with the winning epoch count.

## Data v1_5 — 2026-10-27: harder general cases and unhinted number questions

- **v1_numq_u** (code-built, training only, ids U-…): questions that never name a field's path or quote the deciding value. Kinds: threshold, two-hop lookup (row named by another of its fields), ratio, difference and date gap (each with a graded margin 0.5×–2× of the limit, recorded in meta), highest / lowest / latest entry (choice), size band (score). Reworded by 8 Opus agents (wording only; golds stay code-built; 2,762 of 2,763 rewrites passed the checks: same limits, same labels, no path, no deciding value). Builder faults found by the rewording and filtered (189 questions): date ranges read as dates, unrelated pairs > 10× apart, years as quantities, identifier fields, impossible percentage / age limits, mixed-unit or phrase-label extremes. **727 training cases / 2,329 questions; 129 held-out cases / 434 questions** (15% of source cases plus two phrasings only in held-out cases) for a number-reading metric.
- **v1_more** (ids M01–M10, brief_v2_5_general.md): 500 cases written to need careful reading: every case has at least two of several numbers of one kind, a rule with its exception stated apart, a small calculation, misleading tone, the deciding fact in a second place, irrelevant details. Compare questions about 33%. Three labellers per batch (Opus cautious, Sonnet pragmatic, Fable neutral), an Opus validator per batch that redid every calculation: 36 fixes (reversed score scales in M09/M01/M02, gaps in true/false descriptions, overlapping levels, a missing fact), 18 relabels (mostly one labeller's misreading or arithmetic), 2 drops. **500 cases / 2,139 questions**, 98.3% three-way top agreement, mean gold top 0.907 (the brief's 40% mixed was not reached; generators wrote mostly clear-cut cases).
- **v1_5 = v1_3 + v1_more + v1_numq_u: 3,326 cases.** For the notebooks: M cases split 15% to dev as their own group; U cases training only; dev reported both on the old 313 cases (comparable with every earlier run) and on all dev cases.

## 11 A2b — 2026-10-27: Qwen3-4B, 2 epochs (seed 42), same setup as A2

- **Setup:** as A2 (fp16, one pass per case, 2 GPUs, LR 1e-4 with warm-up 15% and linear decay) but `EPOCHS = 2` (1,786 steps), best epoch by dev KL. 77.7 min of training, about 82 min in all.
- **Training:** loss 1.44 (step 100) → 0.75–0.84 through epoch 1 → 0.57–0.71 in epoch 2; gradient norm mean 2.7–3.7 (one spike of 38 at step 400, no effect). Collapse check at step 400: dev KL 0.321.
- **Dev:** epoch 1 **0.777 / KL 0.340** / ECE 0.033; epoch 2 **0.793 / KL 0.342** / ECE 0.013. Kept epoch 1 (lower KL by 0.002), so the scored model is epoch 1 of a 2-epoch schedule, i.e. stopped at half the learning-rate decay.
- **Benchmark (T per type), test touch 7:** **0.542 [0.516, 0.571] / KL 0.406** / Brier 0.232 / ECE 0.143; choice 0.597, true/false 0.598, score 0.459. Invoices 0.396 (ECE 0.286).
- **Reading:**
  1. **The 1-epoch run (A2: 0.5655 / KL 0.330 / ECE 0.093) is better on every benchmark measure.** The model kept here is an un-decayed epoch-1 checkpoint, which explains the worse calibration (ECE 0.143). Accuracy difference (2.4 points) is inside the two runs' intervals.
  2. **Epoch 2 raised dev accuracy (+1.7) and lowered ECE, at the same dev KL**, so a second epoch is not clearly harmful, but on dev KL it buys nothing. Dev compare questions stayed at 0.615–0.639.
  3. Decision: **1 epoch with the full decay** stays the setting; the next lever is data (v1_5).

## 11 A3 — 2026-10-27: Qwen3-4B on v1_5 (1 epoch, seed 42)

- **Setup:** as A2 (fp16, one pass per case, 2 GPUs, LR 1e-4, 1 epoch) on **v1_5**: 12,400 training questions (A2: 8,254), 1,469 steps, 64.9 min of training. Dev 388 cases / 1,755 questions (the earlier 313 plus 75 M cases).
- **Training:** loss 1.62 (step 100) → 0.64–0.81; gradient norm mean 3.1–4.5 with isolated spikes (87 at step 1000), no effect. Collapse check at step 400: dev KL 0.315.
- **Dev:** all 0.774 / KL 0.345; **earlier 313 cases 0.791 / KL 0.322** (A2: 0.780 / 0.326). By kind: read 0.937, judge 0.829, infer 0.711, **compare 0.618** (A2 0.639).
- **Held-out number questions (never trained on; 434):** 0.859 overall; threshold 0.920, two-hop 0.929, band 0.911, extreme 0.848, dates 0.722; ratio 0.333 (n 9) and difference 0.625 (n 8) too few to read; held-out phrasings 0.917 against 0.840 for trained phrasings (different question mix); margin within 5% 0.892, 5–25% 0.788, over 25% 0.876.
- **Benchmark (T per type), test touch 8:**

| | Accuracy [95% CI] | KL [95% CI] | Brier | ECE | choice | true/false | score |
|---|---|---|---|---|---|---|---|
| **A3, v1_5** | **0.5675 [0.538, 0.596]** | 0.393 [0.365, 0.421] | 0.219 | 0.103 | 0.595 | 0.588 | **0.531** |
| A2, v1_3 | 0.5655 [0.541, 0.591] | **0.330 [0.310, 0.350]** | 0.188 | 0.093 | 0.598 | 0.618 | 0.501 |

  Workflows: agent trace 0.508 (A2 0.538), customer service 0.670 (0.662), **invoices 0.518 (0.434)**, security 0.574 (0.628).
- **Reading:**
  1. **Accuracy unchanged** (0.5675 against 0.5655); score questions +3 and invoices +8.4, offset by true/false and security. One seed, all inside the noise.
  2. **KL clearly worse** (0.393 against 0.330; the intervals do not overlap); true/false ECE 0.176. Likely cause: the code-built number questions carry sharp 0.95 golds (and the new cases are sharp too), so the model became more confident, which costs KL where it is wrong.
  3. **The number skill learned does not transfer to our own compare questions** (dev compare 0.618, unchanged): the model reads code-style number questions well (0.86 held out) but the gap on real compare questions is elsewhere.
  4. Decision: v1_3 stays the reference data for the model comparisons; a v1_3 + M (without U) run would separate the two additions later.

## 11 A4 — 2026-10-27: model comparison on v1_3 (1 epoch, seed 42): Qwen3-4B-Instruct-2507 and Qwen3-1.7B

- **Setup:** exactly A2 (v1_3, fp16, one pass per case, 2 GPUs, LoRA r 16 α 16, LR 1e-4, warm-up 15%, 1 epoch, 893 steps); only the model changes. Instruct-2507: 38.9 min of training; 1.7B: 17.2 min (about 1.1 s per step).
- **Training:** Instruct-2507 loss 1.39 → 0.70, collapse check dev KL 0.277 (A2 0.289). 1.7B loss 1.60 → 0.84, collapse check 0.407.

| Model | Dev acc / KL | Dev compare | Held-out number q. | Bench acc [95% CI] | Bench KL [95% CI] | Brier | ECE | choice | true/false | score |
|---|---|---|---|---|---|---|---|---|---|---|
| **Qwen3-4B-Instruct-2507** | 0.784 / 0.324 | 0.636 | 0.664 | **0.644 [0.620, 0.667]** | 0.341 [0.314, 0.369] | **0.176** | **0.056** | **0.642** | **0.753** | **0.564** |
| Qwen3-4B (A2) | 0.780 / 0.326 | 0.639 | – | 0.5655 [0.541, 0.591] | **0.330** [0.310, 0.350] | 0.188 | 0.093 | 0.598 | 0.618 | 0.501 |
| Qwen3-1.7B | 0.701 / 0.444 | 0.569 | 0.544 | 0.532 [0.506, 0.560] | 0.421 [0.392, 0.450] | 0.247 | 0.108 | 0.485 | 0.543 | 0.559 |

  Workflows, Instruct-2507: agent trace 0.596, customer service 0.716, invoices 0.622 (A2 0.434), security 0.642. 1.7B: 0.502 / 0.682 / 0.414 / 0.530.
- **Reading:**
  1. **Qwen3-4B-Instruct-2507 is the new best: 0.644**, +7.9 over Qwen3-4B on the same data and recipe (intervals do not overlap), with every type and workflow up (true/false +13.5, invoices +18.8) and the best calibration so far (ECE 0.056). Above d3-nano (2B, 0.629), below d3-mini (4B, 0.743). KL about the same as A2.
  2. **Dev did not see it** (0.784 against 0.780): the gain is in transfer, from the stronger instruction-tuned start, not in fitting our data.
  3. **Qwen3-1.7B: 0.532 / KL 0.421**, level with d3-lite (0.8B, 0.531) and 11 points below the 4B-Instruct; fine-tuning added 13.5 points over its zero-shot 0.3975. Score questions hold up (0.559) while choice and true/false fall.
  4. Held-out number questions (not trained on here): 0.664 for Instruct-2507, 0.544 for 1.7B; A3 (trained on them) 0.859.
- **Next:** a second seed for Qwen3-4B-Instruct-2507 (two-seed rule), then its seed average; variants on that model (learning rate, LoRA rank, v1_3 + M).

## 11 A4b — 2026-10-27: Qwen3-4B-Instruct-2507, second seed (1042), v1_3, 1 epoch

- Same setup as A4 (seed 42). The session was interrupted by a laptop restart and resumed from the step-800 checkpoint (as designed); 5.7 min of training after the resume.
- **Dev:** 0.793 / KL 0.321 (seed 42: 0.784 / 0.324); compare 0.662.
- **Benchmark (T per type), test touch 11:** **0.632 [0.606, 0.657] / KL 0.341** / Brier 0.182 / ECE 0.062; choice 0.665, true/false 0.698, score 0.557. Workflows: agent trace 0.588, customer service 0.712, invoices 0.588, security 0.640.
- **Two seeds: mean 0.638 (0.644, 0.632), KL 0.341, ECE 0.059.** The jump over Qwen3-4B (0.5655) is confirmed under the two-seed rule. Seed spread 1.2 points.
- Adapters of both seeds are in Kaggle's checkpoints folder for a weight average.

## 11 A5 — 2026-10-27: Qwen3-4B-Instruct-2507 on v1_6 (v1_3 + 1,000 harder cases), 2 epochs, seed 42

- **Setup:** as A4 but `D_SET = "v1_6"` (2,636 training cases / 11,855 questions; dev 463 cases = the earlier 313 + 150 M cases) and `EPOCHS = 2` (2,636 steps, 111 min of training).
- **Training:** loss 1.75 (step 100) → 0.70–0.89 in epoch 1 → 0.60–0.67 in epoch 2; gradient norm mean 2.9–4.2 (one isolated spike of 58 at step 2000, no effect). Collapse check at step 400: dev KL 0.294.
- **Dev (T = 1):** epoch 1 0.778 / KL 0.345; **epoch 2 0.795 / KL 0.330 / ECE 0.010**, kept. With T per type: all 0.795 / 0.321; **earlier 313 cases 0.808 / KL 0.313** (A4: 0.784 / 0.324; A4b 0.793 / 0.321). By kind: read 0.947, judge 0.840, infer 0.738, **compare 0.676** (A4 0.636, A4b 0.662). Held-out number questions 0.671.
- **Benchmark (T per type), test touch 12:** **0.630 [0.606, 0.655] / KL 0.318 [0.290, 0.347]** / Brier 0.175 / ECE 0.057; choice 0.632, true/false 0.712, score 0.568. Workflows: agent trace 0.572, customer service 0.686, invoices 0.606, security 0.656.
- **Reading:**
  1. **Accuracy unchanged** against v1_3 / 1 epoch (A4 seeds 0.644 and 0.632, mean 0.638): 0.630 is inside both intervals.
  2. **Best KL and Brier so far** (0.318 / 0.175 against 0.341 / 0.176-0.182), and below the prior on every measure (0.470 / 0.347 / 0.189 / 0.088). Score questions 0.568 (A4: 0.564 / 0.557).
  3. **Dev rose again where the benchmark did not:** old-dev +1.5 to +2.4 points and compare +1.4 to +4 over A4, benchmark accuracy flat. The harder cases teach our own compare questions but not, so far, the benchmark's.
  4. One seed; a second seed is needed before claiming the KL gain.

## 11 A6 — 2026-10-27: weight average ("soup") of Qwen3-4B-Instruct-2507 seeds 42 and 1042 (v1_3, 1 epoch), no training

- **Method:** notebook 11 `MODE = "soup"`: each seed's LoRA weight change (B @ A × α / r, 252 modules) added at half weight to the fp16 base weights, so the result is one plain model (no LoRA at inference). About 5 min for the whole run on 2 GPUs.
- **Dev (v1_3, T per type):** 0.795 / KL 0.318 (seeds: 0.784 / 0.324, 0.793 / 0.321); compare 0.669. Held-out number questions 0.661.
- **Benchmark (T per type), test touch 13:** **0.649 [0.626, 0.672] / KL 0.340** / Brier 0.177 / ECE 0.054; choice 0.668, true/false 0.742, score 0.565. Workflows: agent trace 0.614, customer service 0.714, invoices 0.612, security 0.656.
- **Reading:** +1.1 points over the two seeds' mean (0.638) and +0.5 over the better seed (0.644), with the same KL (0.340 against 0.341) and the best ECE of the three. Choice gains the most (0.668 against 0.642 / 0.665). As with the encoder (08g), averaging seeds is a small, consistent gain at no inference cost. **Best benchmark accuracy so far.**

## 11 A7 — 2026-10-27: Qwen3-4B-Instruct-2507, LoRA rank 64 (α 64), v1_6, 2 epochs, seed 42

- **Setup:** as A5 with `r = 64` (132.1 M trainable against 33.0 M); peak 11.3 GB per GPU; ~2.7 s per step, about 2 h. The session was restarted at step 2,200 and resumed from that checkpoint as designed.
- **Training:** loss 1.43 (step 100) → 0.69–0.89 in epoch 1 → 0.59–0.63 in epoch 2 (A5: 0.60–0.67); gradient norm mean 3.3–4.3. Collapse check at step 400: dev KL 0.319 (A5 0.294).
- **Dev (T = 1):** epoch 1 0.762 / KL 0.348 (A5 0.778 / 0.345); **epoch 2 0.801 / KL 0.322** (A5 0.795 / 0.330), kept. With T per type: all 0.801 / 0.314; **earlier 313 cases 0.813 / KL 0.301** (A5 0.808 / 0.313); compare 0.674. Held-out number questions 0.675.
- **Benchmark (T per type), test touch 14:** **0.6275 [0.601, 0.653] / KL 0.337** / Brier 0.182 / ECE 0.076; choice 0.582, true/false 0.720, score 0.593. Workflows: agent trace 0.598, customer service 0.672, invoices 0.630, security 0.610.
- **Reading:** best dev so far on every view, but on the benchmark accuracy is level with A5 (0.630) and KL and ECE are worse (0.337 / 0.076 against 0.318 / 0.057). Choice fell 5 points while score rose 2.5. The extra capacity fits our data more closely without transferring: the same dev-up / benchmark-flat pattern as A5. **Rank 16 stays.** One seed.

## 11 E1 — 2026-10-27: acceptance test of the independent shift_dev (R3), 9 saved runs, no training, no benchmark touch

- **Method:** notebook 11 `MODE = "evaluate"`: each saved adapter (the soup: seeds 42 + 1042 averaged) merged into its base model, scored on our dev (v1_3's 313 cases; temperatures fitted there) and on `independent_v1/shift_dev` (408 cases, 1,833 questions) with the same temperatures; Spearman rank correlation of each with the benchmark results already in hand.

| Run | Our dev acc / KL | shift_dev acc / KL | Benchmark acc / KL |
|---|---|---|---|
| A6 Instruct soup (v1_3) | 0.795 / 0.318 | **0.727** / 0.283 | **0.649** / 0.340 |
| A5 Instruct v1_6 ep2 r16 | 0.807 / 0.313 | 0.726 / 0.279 | 0.630 / 0.318 |
| A7 Instruct v1_6 ep2 r64 | 0.812 / 0.301 | 0.725 / 0.278 | 0.6275 / 0.337 |
| A4 Instruct seed 42 | 0.784 / 0.324 | 0.723 / 0.276 | 0.644 / 0.341 |
| A4b Instruct seed 1042 | 0.792 / 0.321 | 0.714 / 0.291 | 0.632 / 0.341 |
| A2b Qwen3-4B v1_3 ep2 (epoch 1 kept) | 0.775 / 0.333 | 0.710 / 0.297 | 0.542 / 0.406 |
| A2 Qwen3-4B v1_3 ep1 | 0.781 / 0.326 | 0.703 / 0.292 | 0.5655 / 0.330 |
| A3 Qwen3-4B v1_5 | 0.791 / 0.322 | 0.700 / 0.307 | 0.5675 / 0.393 |
| A4 Qwen3-1.7B | 0.701 / 0.444 | 0.677 / 0.321 | 0.532 / 0.421 |

- **Rank correlation with the benchmark (9 runs):** accuracy: our dev 0.65, **shift_dev 0.80**; KL: our dev 0.69, shift_dev 0.64.
- **Reading:**
  1. **shift_dev is the better accuracy referee.** It separates the families in the benchmark's order (Instruct 0.714–0.727 > Qwen3-4B 0.700–0.710 > 1.7B 0.677), puts the soup first, and orders the two Instruct seeds as the benchmark does. Our dev ranks A7 and A5 first and the soup only fourth.
  2. **It does not resolve differences under ~1.5 points** (the Instruct runs span 1.3 points; standard error on 1,833 questions is about 1 point) and it missed A2b's benchmark weakness (an un-decayed epoch-1 checkpoint).
  3. **Neither set ranks KL well** (0.64 / 0.69): calibration choices still need the benchmark or a better-calibrated referee.
  4. Absolute levels differ (shift_dev 0.68–0.73, benchmark 0.53–0.65); only the ordering is used.
- **Use from now on:** shift_dev decides between candidates that differ by more than ~1.5 points on it (model choice, big data changes); the benchmark is touched only to confirm a final candidate or to settle a close call, and each touch is counted.

## 12 P1 — 2026-10-28: compute probe (notebook 12): does the decoder fail to compute, or to map a value to an option? No training, no benchmark touch

- **Method:** Qwen3-4B-Instruct-2507 untrained (`base`) and with A5's adapter merged (`tuned`). Arm **A**: notebook 11's one pass (letters after `n:`). Arm **B**: A plus one line with the computed value, made by code from the code-built inputs (all 96 checked against the gold). Arm **C**: the model writes its working, then `Answers:` (greedy, up to 1,536 tokens per case). Each case timed alone at batch 1 on a T4. Sets: held-out code-built true/false questions needing a date gap, ratio or difference (`numq_computed`, 96, never trained on by A5: v1_6 has no code-built questions); held-out code-built score questions placing a stated value in bands (`numq_band`, 101); our dev's score questions of kind compare/infer (291) and judge/read (399).

| Set | base A | base B (value given) | base C (working) | tuned A | tuned B |
|---|---|---|---|---|---|
| numq_computed (96) | 0.521 | 0.698 | **0.969** | 0.625 | 0.729 |
| numq_band (101) | 0.554 | — | — | **0.426** | — |
| dev score, compare / infer (291) | 0.378 | — | — | 0.577 (0.545 / 0.626) | — |
| dev score, judge / read (399) | 0.526 | — | — | 0.774 (0.773 / 0.786) | — |

- **Latency (T4, batch 1):** one pass 180–350 ms per question (case p50 about 300–370 ms); arm C 21.6 s per question (case p50 33.5 s, p95 94 s; 599 tokens per case, 2 answers unparsed, 1 truncated).
- **Reading:**
  1. **The model can compute:** with working allowed it gets 0.969 on the computed questions; in one pass 0.52 (untrained) / 0.63 (tuned).
  2. **Two one-pass gaps:** computing the value (tuned A → B: +10 points) and comparing a given value with the limit (tuned B 0.73 against C 0.97: +24). The second is the larger.
  3. **Training helps only a little and partly hurts:** A5's training (almost no computing data) raised computed questions +10 and dev compare/infer +20, but compare/infer stays 20 points under judge/read (0.58 against 0.77), and **band questions fell 0.55 → 0.43** (the trained model answers score levels from impression instead of the band edges).
  4. Differences (8 questions) are 0.375 in every one-pass arm, even with the value given: too few to read.
  5. Working-out costs about 100× latency; ruled out by the milliseconds-per-question requirement. Open question for a training run: whether many computed and band questions (v1_numq_u has them) raise one-pass A towards B and beyond.

## 11 A8 — 2026-10-28: queue item 1, LR 2e-4 (A5 settings otherwise: Qwen3-4B-Instruct-2507, v1_6, r16, 2 epochs, seed 42); judged on shift_dev, no benchmark touch

- **Training:** 2,636 steps, 121 min; loss 1.53 (step 100) → 0.70–0.90; gradient norm mean 2.7–3.4 after step 200 (max 31.7 in the first 100 steps); collapse check at step 400: dev KL 0.341. No instability at the doubled rate.
- **Dev (T = 1):** epoch 1 0.777 / KL 0.377 (A5 0.778 / 0.345); **epoch 2 0.800 / KL 0.322** (A5 0.795 / 0.330), kept. T per type: 0.800 / 0.311 (A5 0.795 / 0.321); earlier 313 cases 0.814 / KL 0.299 (A5 0.808 / 0.313). By type: choice 0.825, true/false 0.867, score 0.712. By kind: read 0.941, judge 0.845, infer 0.742, compare 0.688 (A5 0.676).
- **shift_dev (T per type): 0.722 / KL 0.265** (A5 0.726 / 0.279). By kind: read 0.911, compare 0.776, infer 0.712, judge 0.640.
- **Held-out number questions:** 0.638 (A5 0.671); bands 0.386, dates 0.646, threshold 0.796.
- **Reading:** accuracy is level with A5 on the referee (−0.4 points, inside shift_dev's ~1.5-point resolution); KL is a little better on both dev (−0.010) and shift_dev (−0.014), but shift_dev ranks KL poorly (ρ 0.64). Under the rule agreed before the run (level → keep 1e-4), **LR 1e-4 stays** for item 2; 2e-4 is a safe alternative if KL becomes the deciding measure. One seed.

## 12 P2 — 2026-10-28: item 1a, shift_dev misses by gold certainty and full-case latency (notebook 12 `shift_full`), no training, no benchmark

- **Method:** all 408 shift_dev cases (1,833 questions, 4.49 per case), every question of a case in one pass (arm A), untrained Qwen3-4B-Instruct-2507 and A5 merged; each case timed alone on a T4. Misses grouped by the reviewers' gold top probability: clear ≥ 0.85, leaning 0.6–0.85, split < 0.6.

| A5 (accuracy 0.727, 501 misses) | Questions | Accuracy | Misses | Share of misses | Misses where the gold gives our pick ≥ 0.25 |
|---|---|---|---|---|---|
| clear | 1,126 | 0.800 | 225 | 45% | 0 |
| leaning | 329 | 0.708 | 96 | 19% | 33 |
| split | 378 | 0.524 | 180 | 36% | 112 |

- **By kind (accuracy clear / leaning / split):** compare 0.792 / 0.652 / 0.500; infer 0.791 / 0.625 / 0.491; judge 0.900 / 0.793 / 0.531; read 0.932 / 1.0 / –. Untrained: 0.422 overall (clear 0.564, leaning 0.289, split 0.114).
- **Latency (A5, T4, batch 1):** per case p50 970 ms / p95 1,460 ms; **per question p50 221 ms / p95 353 ms**, inside the 500 ms budget.
- **Reading:**
  1. **55% of misses sit on uncertain gold** (leaning or split), 145 of them on questions where the gold gives our pick at least a quarter. By the rule agreed before the check, **teacher relabelling (3a) qualifies for a run.**
  2. **45% are clear-gold misses (12% of all questions):** a skill gap, concentrated in compare and infer (0.79 on clear against judge 0.90); that is what the R15 data targets.
  3. Caveat for 3a: on uncertain questions the "right" answer is the labeller's habit. shift_dev's labellers (Haiku personas + Opus) are not the benchmark's ~4B teacher, so shift_dev can show whether teacher labels change these answers, but only the final benchmark scoring shows whether they match the benchmark's teacher better.

## 11 A9 — 2026-10-28: queue item 2, Qwen3-4B-Instruct-2507 on v1_7 (v1_6 + independent_v1/train 418 + independent_v2/train_v2 2,085), LR 1e-4, r16, 2 epochs, seed 42; no benchmark touch

- **Data:** 5,602 cases, 23,765 training questions (A5: 11,855); dev unchanged (463 cases; R- and V- cases training only). Training 345 min (5,138 steps); loss 2.02 → 0.73–0.78 (epoch 1) → 0.60 at the end, against a label-entropy floor of 0.388 (ours 0.342, the reviewers' 0.434).
- **Dev (T = 1):** epoch 1 0.781 / KL 0.328 (A5 0.778 / 0.345); epoch 2 0.800 / KL 0.326, kept. T per type 0.800 / 0.312 (A5 0.795 / 0.321); earlier 313 cases 0.811 / 0.298. Score 0.715; compare 0.688, infer 0.747, judge 0.838, read 0.953.
- **Held-out number questions: 0.758** (A5 0.671, A8 0.638): bands **0.703** (0.39–0.43), threshold 0.864, two-hop 0.762, ratio 0.778 (n 9), dates 0.633 (unchanged).
- **shift_dev (T per type): 0.784 / KL 0.202 / ECE 0.111** (A5 0.726 / 0.279); compare 0.801, infer 0.789, **judge 0.735** (A8 0.640), read 0.978.
- **Reading:**
  1. **shift_dev is no longer independent of training for data decisions:** v1_7 contains 2,503 cases from the same reviewer pipeline (writers, labellers, checking pass) as shift_dev and the sealed test. Part of +5.8 is likely learning that pipeline's style and its labellers' habits; the largest gain is on judge questions (+9.5), where gold is the labellers' habit, and ECE rose (temperatures fitted on our dev no longer fit).
  2. **Part of the gain is real transfer:** the held-out code-built number questions (outside both pipelines, never trained on) rose 0.67 → 0.76, bands 0.43 → 0.70: the R15 computed and band questions taught a skill, not a template (unlike A3's code-built data). Date gaps did not move.
  3. shift_dev still ranks models trained on the same v1_7 (item 3) fairly. The data decision (v1_7 vs v1_6) needs the benchmark: proposed touch 15 for this model after the three runs finish.

## 11 A10 — 2026-10-28: queue item 3, Granite 4.2 3B on v1_7 (A9's recipe: LoRA r16, LR 1e-4, 2 epochs, seed 42); no benchmark touch

- **Training:** 5,138 steps over three Kaggle sessions (resumed at step 2,200 and again late in epoch 2; both resumes clean); about 6.0 min per 100 steps (10% faster than Qwen3-4B); loss 1.03 at step 100 (Qwen3-4B 2.02); gradient norm mean 6–15, about three times Qwen's (Granite's fixed activation multipliers), clipped at 1.0; no non-finite loss; largest untrained fp16 activation 12,384.
- **Dev (T = 1):** epoch 1 0.764 / KL 0.361 (A9 0.781 / 0.328); epoch 2 0.793 / KL 0.344, kept. T per type 0.793 / 0.328 (A9 0.800 / 0.312); earlier 313 cases 0.799 / 0.319. By kind: compare 0.684, infer 0.754, judge 0.830, read 0.927.
- **Held-out number questions: 0.615** (A9 0.758): bands 0.525 (A9 0.703), dates 0.506 (0.633), threshold 0.716 (0.864), two-hop 0.548 (0.762).
- **shift_dev (T per type): 0.782 / KL 0.205** (A9 0.784 / 0.202); compare 0.797, infer 0.790, judge 0.739, read 0.911 (A9 0.978).
- **Reading:** level with Qwen3-4B-Instruct-2507 on shift_dev (fair here: same training data), slightly behind on our dev, and clearly behind on the held-out number questions (−14 points; bands −18, dates −13) and on read questions (−7). The untrained lead (0.544 against 0.419 on 30 cases) did not survive training, and the deeper stack (40 layers against 36) did not help one-pass computing. **Granite does not replace Qwen3-4B-Instruct-2507.** shift_dev_v2 (notebook 14) will score it too.

## 11 A11 — 2026-10-29: queue item 3, Qwen3.5-4B on v1_7 (A9's recipe), trained on Colab Pro (one A100); no benchmark touch

- **Setup:** text model only (4.21 B, vision tower not loaded); LoRA r16 on 200 modules including the linear-attention projections; fp16; one GPU with two cases accumulated per step (`CASES_PER_STEP = 2`: same cases, order and 5,138-step schedule as the two-T4 Kaggle runs); fast linear-attention kernels from `fla-core` (`causal_conv1d` on its PyTorch fallback). Checkpoints fetched from and pushed to the private repo `skamalj/signpost-d-checkpoints` after each epoch. Training 124 min (about 2.3 min per 100 steps).
- **Training:** loss 0.97 at step 100 (Qwen3-4B 2.02, Granite 1.03), 0.67 at step 2,500; collapse check at step 400: dev KL 0.243 (Qwen3-4B 0.332, Granite 0.325).
- **Dev (T = 1):** epoch 1 0.820 / KL 0.285; **epoch 2 0.845 / KL 0.253**, kept. T per type **0.845 / 0.247** (A9 0.800 / 0.312); earlier 313 cases 0.858 / 0.232. By type: choice 0.847, true/false 0.914, **score 0.778** (A9 0.715). By kind: **compare 0.773** (A9 0.688), infer 0.797, judge 0.866, read 0.965.
- **Held-out number questions: 0.880** (A9 0.758, Granite 0.615): bands 0.941, threshold 0.938, two-hop 0.905, extreme 0.879, dates 0.684 (A9 0.633); within-5% margins 0.757.
- **shift_dev (T per type): 0.807 / KL 0.175** (A9 0.784 / 0.202, Granite 0.782 / 0.205): compare 0.830, infer 0.815, judge 0.750, read 0.978. Fair between the three (same training data).
- **Reading:** Qwen3.5-4B leads on every measure: +2.3 on shift_dev (above its ~1.5-point resolution), +4.5 on our dev, +12 on held-out number questions, with the lowest KL everywhere. The linear-attention concern (exact lookups) did not show: read 0.978 and two-hop 0.905. Date gaps remain the weakest skill. **Qwen3.5-4B becomes the base model**, subject to shift_dev_v2 (notebook 14) and one benchmark confirmation (touch 15).

## 14 E2 — 2026-10-29: acceptance test of shift_dev_v2 (R17, third pipeline), 13 saved runs, no benchmark touch

- **Method:** notebook 14 (notebook 11's evaluate mode) on Colab A100: each saved adapter (or seed average) merged, scored on our dev (v1_3's 313 cases, temperatures fitted there) and on shift_dev_v2 (440 cases, 1,938 questions); Spearman rank correlation with the benchmark over the nine runs that have a benchmark result.
- **Rank correlation (9 runs):** accuracy: our dev 0.65, **shift_dev_v2 0.53** (shift_dev before its contamination: 0.80); KL: our dev 0.69, shift_dev_v2 0.74.
- **shift_dev_v2 accuracy / KL:** Qwen3.5 v1_7 **0.800 / 0.267**; A9 (Qwen3-4B v1_7) 0.766 / 0.326; Granite v1_7 0.763 / 0.347; A5 0.751 / 0.353; A8 0.748 / 0.351; A7 0.742 / 0.369; A4 0.728 / 0.366; A6 (soup) 0.723 / 0.373; A2 0.719; A2b 0.717; A4b 0.716; A3 0.711; Qwen3-1.7B 0.648.
- **Reading:**
  1. **The acceptance test fails for accuracy:** shift_dev_v2 orders runs no better than our own dev. It repeats our dev's error, preferring the v1_6 runs (A5, A7; benchmark 0.627–0.630) to the v1_3 Instruct runs (A4, A6; 0.644–0.649). Likely cause: its documents are written by Opus, like all our cases, so it rewards what our data teaches. The benchmark gaps among these runs (~2 points) are within the benchmark's own noise, so nine runs order them weakly; large gaps (model families, 1.7B last) agree.
  2. It cannot settle v1_7 against v1_6 (A9 +1.5 over A5 on it). It ranks KL best of the three sets.
  3. **Model choice confirmed:** Qwen3.5 leads Qwen3-4B on the same data by +3.4 here, +2.3 on shift_dev, +4.5 on our dev and +12 on held-out number questions.
  4. Next: benchmark touch 15 for Qwen3.5 v1_7 (`BENCH_LABELS`), the only clean referee left.

## 14 B1 — 2026-10-29: benchmark touch 15, Qwen3.5-4B on v1_7 (A11), one seed

- **Benchmark (T per type, temperatures fitted on v1_3's 313 dev cases): 0.6555 [0.6305, 0.6805] / KL 0.311 [0.281, 0.343] / Brier 0.172 / ECE 0.052**; choice 0.623, true/false 0.758, score 0.603.
- **Against earlier runs:** A5 (Qwen3-4B, v1_6) 0.630 / 0.318 (choice 0.632, true/false 0.712, score 0.568); A6 soup (v1_3) 0.649 / 0.340; A4 0.644 / 0.341. Best single run and best KL so far.
- **Reading:** +2.6 over A5 (one seed each, inside each other's intervals): score +3.5, true/false +4.6, choice −0.9. The referees' leads (dev +4.5, shift_dev +2.3, shift_dev_v2 +3.4, number questions +12 over A9) shrink again on the benchmark; far less than the +8 of the earlier switch to Instruct-2507. On the 26 Oct zero-shot table this ties d1-3B (0.656), behind d3-mini (0.743, also Qwen3.5-4B). Choice is now the weakest type.

## 14 Q1 — 2026-10-29: one pass per case against one pass per question, Qwen3.5 v1_7 (A11), no training, no benchmark touch

- **Method:** notebook 14 (`QPASS_LABELS`): the saved model scored twice, each question either packed with its case's other questions (as trained) or alone in the same prompt; temperatures per type fitted per mode on our dev (v1_3's 313 cases); referee shift_dev_v2.

| Mode | Our dev | shift_dev_v2 | choice / true-false / score | compare / infer / judge / read |
|---|---|---|---|---|
| per case | **0.858** / KL 0.231 | **0.800** / KL 0.267 | 0.772 / 0.854 / 0.748 | 0.705 / 0.842 / 0.783 / 0.982 |
| per question | 0.835 / KL 0.253 | 0.792 / KL 0.272 | 0.784 / 0.832 / 0.734 | 0.692 / 0.853 / 0.772 / 0.972 |

- **Reading:** one pass per question is worse (dev −2.2, shift_dev_v2 −0.8, KL worse on both); only choice gains a little (+1.2). The comparison favours per case, since the model was trained that way, but nothing suggests the other questions of a case hurt. **One pass per case stays**; it is also about 4.5 times cheaper per question.

## 11 A12 — 2026-10-29: queue item 4, two more seeds of A11 (Qwen3.5-4B on v1_7), Colab A100; no benchmark touch

| Seed | Dev T per type (acc / KL) | score | Number questions (dates) | shift_dev (acc / KL) | Training |
|---|---|---|---|---|---|
| 42 (A11) | 0.845 / 0.247 | 0.778 | 0.880 (0.684) | 0.807 / 0.175 | 124 min |
| 1042 | 0.842 / 0.249 | 0.774 | 0.885 (0.646) | 0.804 / 0.182 | 121 min |
| 2042 | 0.835 / 0.262 | 0.761 | 0.816 (0.544) | 0.801 / 0.189 | 118 min |
| mean | 0.841 / 0.253 | 0.771 | 0.860 | 0.804 / 0.182 | |

- **Reading:** the recipe is stable on the referees (shift_dev spread 0.6 points, dev 1.0); seed 2042 is the weakest, mainly on number questions (dates 0.54, bands 0.88) and compare (0.730 on dev). Collapse checks at step 400: 0.243 / 0.235 / 0.226. Next: the three-seed soup (notebook 11, `MODE = "soup"`).

## 11 A13 — 2026-10-29: soup of the three Qwen3.5 v1_7 seeds (42, 1042, 2042), no training, no benchmark touch

- **Method:** notebook 11 `MODE = "soup"`: each seed's LoRA weight change merged into the fp16 base at one third (200 adapted modules).
- **Dev (T per type): 0.855 / KL 0.234** (best seed 0.845 / 0.247; seed mean 0.841 / 0.253); choice 0.863, true/false 0.917, score 0.790; compare 0.781, infer 0.813, judge 0.879, read 0.968; earlier 313 cases 0.863 / 0.222.
- **Held-out number questions:** 0.871 (seeds 0.880 / 0.885 / 0.816): bands 0.941, threshold 0.951, two-hop 0.976, dates 0.608; within-5% margins 0.838.
- **shift_dev: 0.801 / KL 0.178** (seeds 0.807 / 0.804 / 0.801; KL 0.175 / 0.182 / 0.189).
- **Reading:** +1.0 over the best seed on our dev with the lowest dev KL so far; level with the seeds on shift_dev (which is contaminated for data decisions but fair between these runs). On the old base the soup (A6) was likewise level-to-slightly-up on shift_dev and +0.5 to +1.7 over its seeds on the benchmark. The soup is the natural final candidate for this recipe.

## 14 B2 — 2026-10-29: benchmark touch 16, the Qwen3.5 v1_7 three-seed soup (A13)

- **Benchmark (T per type, temperatures fitted on v1_3's 313 dev cases): 0.6535 [0.630, 0.6795] / KL 0.283 [0.255, 0.311] / Brier 0.156 / ECE 0.027**; choice 0.615, true/false 0.748, score 0.611.
- **shift_dev_v2:** 0.815 / KL 0.267 (seed 42: 0.800 / 0.267); compare 0.722, infer 0.860, judge 0.805, read 0.982. Our dev (v1_3 313): 0.863 / 0.222.
- **Against seed 42 alone (touch 15: 0.6555 / KL 0.311 / Brier 0.172 / ECE 0.052):** accuracy level (−0.2, well inside the intervals), but **KL −0.028, Brier −0.016, ECE halved**: the best calibration we have recorded. Score +0.9, choice −0.8, true/false −1.0.
- **Leaderboard context (26 Oct table):** accuracy level with d1-3B (0.656), behind d3-mini (0.743); KL 0.283 is below d3-mini's 0.319 and d1-3B's 0.286, Brier 0.156 against 0.123 / 0.144, ECE 0.027 against 0.047 / 0.037.
- **Reading:** on this base the soup buys calibration, not accuracy (on the old base it bought both, +0.5 to +1.7). Accuracy has settled at about 0.655 for Qwen3.5 on v1_7; further accuracy needs new data (v1_8) or recipe changes. Sealed test still unused.

## 11 P3 — 2026-10-29: does packing hurt later questions? (Qwen3.5 v1_7 seed 42, our dev, no new run)

- **Position mix (dev):** early questions are mostly true/false and compare (position 1: compare 52%), later ones mostly score and judge (positions 3+: judge 50–61%). Training shuffles question order in every case and epoch.
- **Accuracy by position:** 0.847 / 0.838 / 0.851 / 0.827 / 0.877 (positions 1–5+), which looks flat only because late positions hold easier judge questions.
- **Within each kind, positions 1–2 against 3+:** read 0.972 / 0.956, compare 0.777 / 0.764, infer 0.812 / 0.782, judge 0.882 / 0.861: a small late-position penalty of about 1.5–3 points, in all four kinds (each alone within noise).
- **Decision (user, 2026-10-29): training runs must stay within 5–6 hours** (Colab A100). Packed training on v1_7 takes about 2.1 h and on v1_8 about 2.6 h; per-question training costs about 4.6 times as much (v1_7 about 9–10 h), so it would need roughly half the data. Its likely gain (about +1 point overall, later questions only) does not justify that: **per-question training dropped**. Cheaper ideas kept for later: a prompt format that puts the case nearer the later questions (e.g. questions before the case).

## 11 A14 — 2026-10-29: Qwen3.5-4B on v1_8 (v1_7 + R19's train_v3, 1,008 X- cases) with LoRA rank 32 (α 32), seed 42; Colab (about 3× faster GPU, likely an H100); no benchmark touch

- **Setup:** 6,610 cases, 28,610 training questions, dev unchanged (463 cases); 60.9 M trainable; 6,146 steps in 49 min. Loss 1.03 → 0.55; collapse check at step 400: dev KL 0.230.
- **Dev (T = 1):** epoch 1 0.806 / KL 0.308 (v1_7 seeds 0.811–0.831 / 0.275–0.285); epoch 2 0.839 / 0.268, kept. T per type **0.839 / 0.256** (v1_7 seeds 0.835–0.845 / 0.247–0.262); score 0.768; compare 0.747, infer 0.783, judge 0.874, read 0.971; earlier 313 cases 0.852 / 0.244.
- **Held-out number questions: 0.843** (v1_7 seeds 0.816–0.885): bands 0.941, threshold 0.920, dates **0.570** (0.544–0.684), within-5% margins 0.811.
- **shift_dev: 0.802 / KL 0.180** (v1_7 seeds 0.801–0.807 / 0.175–0.189).
- **Reading:** inside the v1_7 seeds' range on every measure, at its lower half on score, compare and date gaps, exactly what R19 targeted. shift_dev shares train_v3's pipeline and should, if anything, favour v1_8, yet it is flat. Two changes at once (data and rank), so neither is attributed; no sign that either helped. The v1_7 soup (touch 16: 0.6535 / KL 0.283) stays the candidate.

## 16/14 E3 — 2026-10-29: quick-teacher labels for shift_dev_v2 (Qwen3.5-4B, thinking off), acceptance test; no training, no benchmark touch

- **Labels (notebook 16, `TEACHER_MODE = "quick"`):** three samples per case at temperatures 0.7 / 1.0 / 1.3. Pairwise self-agreement 0.707 / 0.647 / 0.597 against the benchmark teacher's 0.735, so **0.7 chosen before any ranking**. At 0.7, mean top 0.846; the teacher's top answer equals the reviewers' on 66.8% of questions (clear gold 0.697, leaning 0.632, split 0.408; compare 0.555, score 0.535, read 0.937). The earlier thinking teacher was far too consistent (0.953).
- **Acceptance test (notebook 14, `LABELS = "teacher_quick"`, 9 runs with benchmark results):** rank correlation with benchmark accuracy **0.47** (reviewers' labels 0.53); Instruct runs only −0.60 for both. Scores compress to 0.68–0.70 for every Instruct and Qwen3-4B run (1.7B 0.632).
- **Reading:** teacher-style labels from a calibrated quick 4B teacher do not track the benchmark better, so **teacher relabelling stays off** (the rule fixed before the test). The test's power is limited: the five Instruct runs sit within about 2 benchmark points.
- **Pattern across all runs:** less fitting transfers better to the benchmark (A2 1 epoch 0.5655 against A2b 2 epochs 0.542; A4 v1_3 1 epoch 0.644 against A5 v1_6 2 epochs 0.630; soups best), while every referee rewards more fitting. Candidate next step: **WiSE-FT** (blend the soup's weight change at α < 1 towards the untrained base), chosen only by benchmark touches.

## 14 B3 — 2026-10-29: WiSE-FT blends of the Qwen3.5 v1_7 soup, benchmark touches 17 and 18

- **Method:** notebook 14; the three-seed soup's weight change merged at alpha 0.5 and 0.75 (alpha = share of the fine-tune kept; 1.0 is the plain soup, touch 16). Temperatures per type fitted on v1_3's 313 dev cases.

| alpha | Benchmark acc [95% CI] | KL | Brier | ECE | choice / true-false / score | shift_dev_v2 | our dev |
|---|---|---|---|---|---|---|---|
| 1.0 (touch 16) | 0.6535 [0.630, 0.680] | 0.283 | 0.156 | 0.027 | 0.615 / 0.748 / 0.611 | 0.815 | 0.863 |
| **0.75 (touch 18)** | **0.6655 [0.641, 0.690]** | **0.279** | **0.153** | 0.035 | 0.628 / 0.748 / **0.631** | 0.811 | 0.855 |
| 0.5 (touch 17) | 0.6525 [0.629, 0.678] | 0.284 | 0.154 | 0.044 | 0.623 / 0.750 / 0.601 | 0.796 | 0.845 |

- **Reading:** alpha 0.75 is our best benchmark result on every measure but ECE (+1.2 accuracy over the plain soup, score +2.0), but +1.2 is below the +2 rule fixed before the run and well inside the intervals. It was also picked from three tries on the benchmark itself, which flatters it by up to about a point. So the "less fitting" pattern is at most weak. The curve is flat-topped around 0.65–0.67 for alpha 0.5–1.0. On the 26 Oct zero-shot table, 0.6655 would sit just above d1-3B (0.656), below clef-flash (0.710) and d3-mini (0.743).

## 11 A15 / 14 B4 — 2026-10-30: Qwen3.5-4B on v1_7s (v1_7 + R21's score-only augmentation: 409 cases / 1,636 score questions), rank 16, seed 42; benchmark touch 19

- **Setup:** A11's recipe with the score set added (6,011 cases, 25,401 training questions, dev unchanged); 5,548 steps in 133 min on the Colab GPU; collapse check at step 400: dev KL 0.259.
- **Referees:** dev T per type 0.843 / KL 0.257 (A11 0.845 / 0.247); score 0.773 (0.778); number questions 0.850 (0.880), dates 0.582 (0.684); shift_dev 0.801 / 0.185 (0.807 / 0.175); shift_dev_v2 0.806 / 0.275 (A11 0.800 / 0.267).
- **Benchmark (touch 19): 0.6555 [0.6325, 0.6795] / KL 0.250 [0.228, 0.272] / Brier 0.1395 / ECE 0.018**; choice 0.618, true/false 0.762, score 0.604. A11: 0.6555 / 0.311 / 0.172 / 0.052; score 0.603.
- **Decision rule (fixed beforehand: score +3 and overall +1.5): failed.** Accuracy is identical to A11, overall and on score.
- **But calibration improved sharply:** KL −0.061, Brier −0.033, ECE about a third, the best calibration of any run (soup at α 0.75: KL 0.279 / Brier 0.153). On the 26 Oct table, KL 0.250 is below d3-mini (0.319) and d1-3B (0.286), behind only clef-flash (0.209), and Brier 0.140 is below d1-3B (0.144). The strictly validated, non-overlapping scales with honest spread gold seem to teach the model how sure to be, not which level to pick.
