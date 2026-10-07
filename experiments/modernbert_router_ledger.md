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

Later phase branches are created when each phase starts, from the branch of the best result so far.

## Roadmap (agreed plan; update as phases finish)

| Phase | What | Pass criteria | Status |
|---|---|---|---|
| 0 | Ledger and fixed evaluation suite | this file exists; every run is logged | done |
| 1 | Cascade: detector N → stay with the current agent; Y → router picks among the other agents. Plus the detector data-gap fixes | E5 combined ≥ 36/40; E4 per turn ≥ 21/25; E7 ≥ 34/35; E8 ≥ 16/18; E6 no worse than 4300/4347 | **failed (run 6)**: the hard gate is worse than the router alone |
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
| branch phase6 | Realistic free-form TRAINING data: 40 businesses × 4 conversations, 744 user turns, merged with the templates | E10 test / E11 / banking above run 10 | **running** |
| decision 2026-10-07 | **Final architecture has one detector: context change (pooled features + feed-forward head).** The switch detector is dropped from the next run on. Decision rule for any challenger: settings chosen on dev companies, must beat the default by ≥ 2 / 83 on E10 test; on a tie the simpler option wins | — | agreed |
| next (after phase6) | **Q-K-V rewrite, proper test:** explicit `x_current` (Q) / `x_hist` (K, V) inputs instead of `attn(x, x, x)` + masks, plus a variant where the current message is encoded alone (the bidirectional encoder no longer leaks the history into Q). Context-change label only. Then decide Q-K-V vs pooled and freeze the design | Q-K-V gate ≥ pooled + 2 on E10 test | **next** |
| 7 | Optional: a **small generative router** (e.g. Qwen2.5-0.5B-Instruct + LoRA, outputs the agent name) as a different-paradigm comparison (System 1 guide, strategy C) | vs the best encoder router on E2–E5, E10 | optional |
| — | Rejected for now: target-only second pass / TTA (it removes exactly the history that short replies need; "router x2" already hurt); scaling the attention α inside the frozen encoder (a distribution shift for a frozen backbone); history KV caching for the encoder (only an approximation, because history tokens attend to the new turn); ONNX / Triton / CUDA graphs (latency work, not accuracy) | — | — |
| 5 | Optional: partial fine-tuning of the top 2–4 ModernBERT layers with differential learning rates (fp16 on the T4) | E1/E2/E3 clearly above the frozen best | optional |
