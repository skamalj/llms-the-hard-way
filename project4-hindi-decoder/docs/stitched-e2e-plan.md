# Project 4 — Implementation plan for the persona-language translation bridge

**Status:** draft for review, 2026-10-19 · **Branch:** `hindi-decoder-compare`

**Specification:** [`encoder_decoder_bridge_e2e_plan_v2.md`](encoder_decoder_bridge_e2e_plan_v2.md) (plan v2, kept verbatim). This document does not restate it. It records how v2 is carried out here: what changes from the earlier work, what the v3 data does and does not yet provide, what we already know from the pilots, and the decisions still open.

**Data:** [`data/persona_translation_v3/`](../data/persona_translation_v3/) (v3, copied unchanged from the authors' release).

## 1. What changed

| | Before (persona pilots, runs 1–4) | Now (plan v2, data v3) |
|---|---|---|
| Task | given a *scenario*, invent a persona's reaction line | **translate** an English source sentence into a persona's Roman-script Hinglish, preserving its meaning |
| Data | 60 → 168 scenario/line examples | 60 English sources × 6 personas = 360 parallel pairs |
| Splits | train / held-out (held-out also used to pick the checkpoint) | **train 40 sources (240) / validation 10 (60) / blind test 10 (60)**, split by source; test never used for selection |
| Main quality question | coherent and in character | **meaning preserved** *and* persona recognisable, scored separately |
| Encoder input | persona + scenario | the English **source** |
| Decoder input (bridge condition) | — | persona specification only; the source reaches it only through the encoder |
| LoRA | decoder only | **encoder and decoder** from the first full training stage |
| First bridge decoder | Gemma 3 4B IT (pilots) | `Qwen/Qwen2.5-1.5B-Instruct` (v2) |

`Project 4 Requirements.md` stays as the original brief; where it differs (decoder family, FP16, scenario wording), plan v2 governs.

**What carries over from the pilots:** the training loop (answer-only loss including the stop token, early stopping, per-epoch probe outputs), the automatic signals (stop reason, repetition, Devanagari share, persona overlap, copying), the blind persona-matching sheet, and these findings:

- **Stopping is learned from the target's stop token,** when that token's embedding is trained: Gemma 3 IT went from never stopping to 84/84.
- **Qwen2.5-1.5B *base* + Hinglish adapter never stopped, even after persona LoRA (0/84).** Most likely cause: the base model's chat tokens (`<|im_end|>`) are untrained, and LoRA cannot train embeddings. The Instruct model's chat tokens are trained, so this should not recur with v2's choice (to be checked, §4).
- **Gemma 3 4B in 4-bit** is the strongest decoder tried so far on fluency (about 1 in 3 coherent lines on the old task); Gemma 3 1B and Qwen base + adapter were weaker.

## 2. Data v3: what it provides, and two gaps

**Provides (checked):** 360 pairs, 6 per source; train `s001–s040`, validation `s041–s050`, test `s051–s060`; no source or target duplicated; Roman script only (no Devanagari); manifest, `.json` and `.jsonl` files agree. The six personas' lines differ (mean word overlap between personas 0.095, range 0.035–0.183), with distinct lengths (median words: Agneepath 6, Don and Jai 10, Vijay 11, Shahenshah 13, Anthony 14).

**Gap 1 — semantic notes.** v2 asks for a per-source note of the core proposition, facts, intent and sentiment, used to judge meaning preservation. In v3 every pair carries the same generic sentence ("Preserve the source proposition; …"). **Needed before Phase 4 / Phase 6 human scoring** (60 short notes, one per source); not needed for Phase 1 training.

**Gap 2 — persona description in the input.** v2: "do not rely on a character name alone; include the agreed description." v3's ready-made `input` names the persona only; the descriptions are in the manifest (`personas`). The notebooks will build the input from the manifest's name **and** description (§5).

**Review notes (not blocking):**
- Some comic lines add small details (s003, Anthony: "Main yahan full reception lekar baitha tha!"). v2's rubric counts unsupported additions; reviewers should decide whether such persona colour is acceptable or should be trimmed.
- The README asks for review by fluent Hinglish speakers before training; the test split must stay untouched during model selection.

## 3. Phases, mapped to this project

| v2 phase | Deliverable here | Status / notes |
|---|---|---|
| 0 Task contract and data | v3 data + this plan; semantic notes (gap 1) | data in; notes to write |
| 1 Decoder baseline (direct source in the prompt) | `persona-translation-baseline` notebook, run for **Gemma 3 4B IT and Qwen2.5-1.5B-Instruct** (§5) | next |
| 2 Bridge skeleton, no training | `stitched-bridge` notebook: modules + plumbing tests | after Phase 1 |
| 3 First end-to-end training (encoder LoRA + bridge + cross-attention + decoder LoRA) | same notebook | — |
| 4 Encoder interventions (full / null encoder / mismatched source / direct-source / encoder LoRA off) | same notebook, fixed checkpoint | needs semantic notes for human scoring |
| 5 Adapter ablations, one factor at a time | — | — |
| 6 Blind end-to-end evaluation | blind sheets on the test split | — |
| 7 Joint fine-tuning, scaling | — | only after Phase 6 |

**Bridge details carried from the earlier draft** (implementation choices within v2):

- **Encoder:** `answerdotai/ModernBERT-base` (768), English source only — the v3 sources are English, so an English encoder fits.
- **Bridge:** `Linear(768 → 1536)` + RMSNorm, to match Qwen-Instruct's hidden size and scale.
- **Cross-attention:** pre-norm `nn.MultiheadAttention(1536)` in every 4th decoder layer to start (7 of Qwen's 28), each behind a **tanh gate initialised to 0**, so the untrained system is exactly the pretrained decoder.
- **Decoder prompt in the bridge condition:** persona name + description + a fixed translation instruction; **no source text** (v2 §2).

**Plumbing tests for Phase 2** (in addition to v2's checks): gate-0 equivalence (logits equal the plain decoder's), padding-mask invariance, cached vs uncached generation match, gradient audit per module, and memory on 2 × T4.

## 4. Decoder choice: one conflict to settle

v2 names `Qwen/Qwen2.5-1.5B-Instruct` "with the agreed Hinglish adapter merged into the base first". The adapter `sarthaksenapati/qwen1.5b-hinglish-sft-v2` was trained on **`Qwen/Qwen2.5-1.5B` (base)**, not Instruct. Merging it into Instruct applies weight changes learned against different weights: the shapes match, so it runs, but nothing guarantees it helps, and our adapter check (configured base = loaded base) fails by design.

**Decided:** Phase 1 runs all three as a controlled baseline comparison, not as three equally valid configurations — Gemma 3 4B IT (compare with the pilots), Qwen2.5-1.5B-Instruct (the clean Qwen baseline and preferred bridge candidate), and Qwen-Instruct + the base-trained adapter (**diagnostic only**: does the adapter help despite the mismatch?):

| Variant | Stop token trained? | Hinglish | Risk |
|---|---|---|---|
| Gemma 3 4B IT, 4-bit | yes | best so far | heavier (needs 4-bit on a T4); hidden 2560 |
| Qwen2.5-1.5B-Instruct | yes (to confirm: embedding check) | unknown on this task | may be weak in Roman Hinglish |
| Qwen2.5-1.5B-Instruct + Hinglish adapter (merged) | yes | adapter's strength | adapter trained on a different base |

The bridge decoder (Phase 2 onwards) is then the Phase 1 winner. v2's default is Qwen-Instruct; switching to Gemma would change the bridge widths (2560) and memory, not the method.

## 5. Phase 1 notebook: what changes from the persona pilot

One notebook, one switch at the top selecting the decoder (`gemma-4b`, `qwen-instruct`, `qwen-instruct+hinglish`), so all three runs share every other line of code.

**Data and prompt**
- Load `train_v3.json`, `validation_v3.json`, `test_v3.json` from the repository.
- Input built from the manifest: the v3 instruction ("Translate the English sentence into natural Roman-script Hinglish in the voice of …; preserve the original meaning; do not add new events or facts"), **plus the persona's description**, plus `English: <source>`.
- Target: the v3 `target` followed by the model's own end-of-turn token (taken from its chat template, as in the Qwen notebook).
- The old scenario sets (held-out scenarios, six fixed new scenarios, trait lines) are removed.
- Small out-of-domain set of English sources without references, including the requirements' two ("I am going to eat fruit today", "My Wi-Fi is disconnected").

**Training and selection**
- Train on 240, **select the checkpoint by validation loss** (60), early stopping as before; probes each epoch from validation sources only.
- **Test (60) is generated once, after selection**, and reported, never used for a decision.

**Evaluation added for translation**
- **Reference similarity:** chrF against the v3 reference (diagnostic; one reference per pair).
- **Untranslated content:** share of the output that is copied English from the source.
- **Meaning-preservation sheet** for human scoring: source, persona, output, reference, side by side (1–5 meaning, 1–5 fluency, unsupported additions yes/no).
- Kept: stop reason, repetition, Devanagari share, persona overlap (yardstick 0.095), blind persona sheet, records as JSON lines.

**Model-specific**
- **Gemma:** unchanged loading (4-bit QLoRA, token in Cell 0, image encoder excluded from LoRA).
- **Qwen-Instruct:** fp32, no token. Its chat template adds a default system message when none is given; kept as is and identical in training and generation. **Before training, print the embedding norms of `<|im_end|>`, `<|im_start|>`, `<|endoftext|>` against the median token**, to confirm the stop token is trained (the base-model failure).
- **Qwen-Instruct + adapter:** the adapter check becomes a warning, not an assertion (base mismatch is expected and recorded).

**Fixes carried in:** the settings JSON (`target_modules` is a set → write it as a sorted list); probe and blind-sheet seeds per run.

**Phase 1 gates** (decided 2026-10-19; engineering gates for choosing the decoder, not evidence that the bridge works):

| Metric | Gate | Definition |
|---|---|---|
| Correct stopping | ≥ 95 % | the last generated token is the model's end-of-turn / end-of-text token, before the 80-token limit |
| Repetition failures | ≤ 5 % | an output in which any word 4-gram occurs twice; generation is plain greedy with no repetition guard, so this is measured, not suppressed |
| Meaning preservation | mean ≥ 4 / 5 | human score against the **English source** (not the reference wording), on a fixed validation sample |
| Fluency | reported | human, 1–5, same sample |
| Unsupported additions | rate reported | human: none / harmless comic framing / material (invented fact or event) |
| Persona recognition | reported; 50 % stretch gate | blind 6-way identification: for each sample source the six outputs are shuffled A–F and the reviewer assigns each letter one persona (a permutation); accuracy = correct / pairs; chance is 1 in 6 (17 %) |

- **Fixed human-scoring sample:** 5 of the 10 validation sources (every other one) × 6 personas = **30 pairs**, the same pairs for every decoder.
- **Decoder selection rule:** validation performance (the gates above, plus chrF and persona overlap as diagnostics), stopping reliability, translation quality and resource use — never training loss alone. The adapter-merged Qwen run is a separate, diagnostic condition.
- One run per decoder for this screening; three seeds are for the final comparisons (P3).

## 5a. Phase 1 results (2026-10-19) and the decoder decision

Three runs, identical except the decoder (`4-translation-baseline/`). LoRA outputs; validation unless stated.

| | Gemma 3 4B IT (4-bit) | Qwen2.5-1.5B-Instruct | Qwen-Instruct + Hinglish adapter (diagnostic) |
|---|---|---|---|
| Stopping (gate ≥ 95 %) | 98 % ✓ | 100 % ✓ | 100 % ✓ |
| Repetition (gate ≤ 5 %) | 3 % ✓ | 0 % ✓ | 0 % ✓ |
| chrF validation / test | **22.8 / 23.8** | 20.0 / 21.4 | 22.8 / 20.8 |
| Persona overlap (references 0.095) | 0.179 | 0.180 | 0.162 |
| Kept epoch (validation loss) | 1 (2.62) | 2 (3.04) | 2 (2.88) |
| Meaning, 30-pair sample — *rough reading, not the human score* | ≈ 3.2 / 5 | ≈ 1.8 / 5 | ≈ 2 / 5 |
| Stock words not in the data ("khatam": outputs vs train targets) | 3 % vs 2 % | 37 % vs 2 % | 45 % vs 2 % |
| Time per epoch / per output | ≈ 5 min / 2.5 s | ≈ 2 min / 1.6 s | ≈ 2 min / 1.9 s |

- **Both Qwen variants collapse onto a few stock words** ("khatam", "aaj", "dhamki", "daleel") far more often than the training targets use them, and most outputs lose the source meaning. The adapter is not the cause (the clean Instruct run shows the same); Qwen 1.5B's Roman Hinglish is the limit. Qwen-Instruct's `<|im_end|>` is trained (it stops 97–98 % even without LoRA), so the base model's stopping failure does not recur.
- **Gemma's habits match the data's** (stock-word rates close to the training targets) and its meaning preservation is clearly the best.
- **Decision (proposed): Gemma 3 4B IT is the bridge decoder.** This departs from v2's default (Qwen-Instruct) on v2's own selection rule: validation performance, stopping and translation quality, at the cost of about 2.5× the training time. Bridge widths change to Gemma's hidden size (2560, to confirm from its config in Phase 2); the method does not.
- Human scoring of Sheets A and B for Gemma is still needed to confirm the meaning gate (≥ 4 / 5); the rough reading suggests it is **not yet met**.

### Per-persona scores and the three personas kept (2026-10-19)

Gemma's LoRA outputs, all 10 validation sources + 6 out-of-domain sources per persona (16 each; test not used), scored by Claude: meaning 1–5 against the English source, fluency 1–5, persona fit 1–5, additions (none / harmless / material). File: [`4-translation-baseline/gemma-4b-scores-claude.csv`](../4-translation-baseline/gemma-4b-scores-claude.csv), one reason per score. **Not independent:** an AI scorer, not a native speaker; and blind recognition was not possible (the scorer had seen the labels), so persona fit stands in for it.

| Persona | Meaning, validation | Meaning, all 16 | Meaning ≥ 4 | Fluency | Persona fit | Material additions | Stopped |
|---|---|---|---|---|---|---|---|
| **Don** | **3.6** | **4.00** | **12/16** | **3.56** | **4.06** | 1 | 16/16 |
| **Anthony Gonsalves** | 3.2 | 3.62 | 10/16 | 3.06 | 3.75 | 1 | 14/16 (two loops) |
| **Jai (Sholay)** | 3.4 | 3.56 | 8/16 | 3.44 | 3.19 | 2 | 16/16 |
| Vijay (Deewar) | 3.2 | 3.50 | 9/16 | 3.25 | 2.25 | 1 | 16/16 |
| Shahenshah | 2.5 | 3.12 | 7/16 | 2.75 | 2.62 | 5 | 16/16 |
| Vijay Dinanath Chauhan (Agneepath) | 2.2 | 2.50 | 4/16 | 3.19 | 4.00 | 0 | 16/16 |

**Decision: continue with three personas — Don, Anthony Gonsalves, Jai; drop the other three.** The project needs three.

- **Don:** best on every measure, and the only persona at the meaning gate (4.00).
- **Anthony:** second-best meaning, strongly recognisable; his failures (two loops, one meaning reversal, the "boss" tic in 30 of 40 training targets) are in the decoder-LoRA and data buckets, i.e. fixable.
- **Jai:** third-best meaning, few errors of the unfixable kind.
- **Dropped:** Vijay (meaning similar to Jai's but the weakest persona fit, and his lines duplicate Jai's); Shahenshah (invented words in the Urdu-tinged register — bucket D, not fixable here — and 5 material additions); Agneepath (most recognisable, but his compression loses the meaning in 12 of 16).
- The three are well spread: cool and controlled (Don), comic and code-switching (Anthony), calm and practical (Jai). One risk to watch: Don and Jai both write short lines (median 10 words each in the data); their contrast needs to stay sharp in the refined data.
- **Effect on the plan:** the data becomes 60 sources × 3 personas = 180 pairs (train 120 / validation 30 / test 30) unless sources are added; blind recognition becomes 3-way (chance 1 in 3, so its gate must be raised accordingly); everything else is unchanged.

### Gaps for Gemma 3 4B IT, by what can fix them

**A. The encoder (+ LoRA) may handle** — to be proven in Phase 4, not assumed:
- A1. Logical structure lost or weakened: contrast and negation ("celebrate *without ignoring* the remaining work" → "Aage badh rahe hain, par poori tarah nahi"; "fix the cause *instead of* treating symptoms" → "treating symptoms is good, the cause is better"; Anthony reversing "busy ≠ progress"). A bidirectional encoder re-read through cross-attention at every step is the bridge's case for better source grounding.
- A2. Robustness to unseen phrasing: untranslated English rises from 3 % (validation) to 8 % (out-of-domain).
- Limit: the encoder adds no Hinglish vocabulary, persona voice or stopping; and the Phase 1 decoder already sees the source directly, so the bridge must at least match it (Phase 4 arm D, with the capacity-matched control P2).

**B. Decoder LoRA training can fix:**
- B1. Checkpoint choice: validation loss keeps epoch 1, while epoch 2's probe lines read better. Save every epoch's adapter and score the fixed sample per epoch; choose on quality as well as loss (v2: inspect every checkpoint).
- B2. Fast over-fitting (training loss 3.0 → 1.0 in three epochs while validation rises): lower learning rate (5e-5), higher dropout, possibly rank 8.
- B3. Persona tics amplified into templates (Shahenshah appending "Insaaf ka faisla hona chahiye"; two cases of identical lines for different personas): less over-fitting, together with C2–C3.
- B4. The single loop ("boss boss boss…", 1 of 96): fewer-epoch training and C2; a repetition guard is available later if needed.

**C. Refined training data can fix:**
- C1. Agneepath compression beyond meaning ("Progress. Abhi nahi."): his targets are about half the source length (0.55 words per source word), terse but complete; add or revise lines so terse still keeps every clause, guided by the semantic notes.
- C2. Anthony: "boss" in 30 of 40 targets, and jokes that add details ("popcorn", "full reception") → the model copies the tic and adds material content ("…like pizza"). Make "boss" occasional; keep comedy in framing, not in facts.
- C3. Shahenshah: justice words in 9 of 40 targets → vary the register markers so they are not a formula.
- C4. Don's near-English outputs ("Customer confused. We gave two different answers."): set an expected English share per persona in the writing guidelines.
- C5. Vijay vs Jai too close (identical lines): sharpen the contrast (moral weight and defiance vs practical, dry calm).
- C6. Size and evaluation: 240 training pairs over-fit within two epochs; 60 validation pairs give a noisy selection signal. Expand after refining; add the semantic notes (P4) and, ideally, a second reference per validation pair, so chrF counts more than one acceptable phrasing.
- C7. Independent native review of all targets (already decided).

**D. Cannot fix within this setup:**
- D1. Invented or malformed words, mostly in the Urdu-tinged register ("progah", "aazm-e-khatam", "dohte"): the vocabulary limit of a 4B model in 4-bit. LoRA on a few hundred pairs does not add vocabulary; only a larger or full-precision decoder would, which the T4 budget and the closed selection rule out.
- D2. Romanised Hinglish has no standard spelling (phal / fal, khaunga / khauunga), so one-reference chrF has a low ceiling; only human scoring measures quality.
- D3. Pilot-scale statistics: a 30-pair human sample detects only large differences (three seeds for the final comparisons, P3, narrow this but do not remove it).
- D4. Fluency and persona voice are the decoder's job by design; the bridge can change them only indirectly.

## 6. Proposals beyond v2 — decisions

| # | Proposal | Decision |
|---|---|---|
| P1 | Warm the bridge up on a public English → Hinglish corpus | **Conditional.** First establish whether the bridge learns on the 240 pairs (gradient flow, loss curves, ablations). Only if it stays ineffective, run the warm-up as its own phase, documenting corpus, licence, split hygiene and contamination risk. |
| P2 | Parameter-matched direct-source control in Phase 4 | **Adopted.** Match trainable parameters as closely as practical and report the remaining difference; also keep the direct-source baseline without extra capacity. |
| P3 | Three training seeds | **Adopted for the final comparisons** (mean and spread); one run per decoder for Phase 1 screening. |
| P4 | Semantic notes and target review | **Adopted, before Phase 4;** does not block the first training runs. |

## 7. Responsibilities and open items

- **Semantic notes:** 60 drafted by the reviewer's assistant, one per source, persona-neutral, with three parts: *core meaning* (the proposition that must stay true), *facts and intent* (what it asserts, requests or commits to), *allowed variation* (what a persona may change in wording, rhythm or framing). These are not independent linguistic validation.
- **Target review:** a fluent Hinglish speaker, independent of the model and data authoring, checks all 360 targets for natural Roman-script Hinglish, meaning preservation, persona distinctiveness, and unsupported additions, omissions or changed implications. Borderline comic framing (e.g. s003 Anthony, "full reception") is flagged for the reviewer's decision, not rejected automatically. Judgements on the test split are recorded before any result is used to choose a checkpoint.
- **Sequencing:** the Phase 1 winner only selects the decoder for the bridge. The bridge's success still has to be shown causally in Phase 4: changing or removing the encoder's source representation must change the output in the expected way.
