# End-to-End Plan: Persona-Language Translation with a Stitched Encoder–Decoder Bridge

**Project goal:** Build and validate a custom stitched encoder–decoder Transformer that translates ordinary source meaning into one of six persona-specific “languages” (for example, Don lingo or Jai lingo). A bidirectional encoder represents the source sentence/context; a trainable projection bridge and cross-attention connect those representations to an autoregressive decoder. LoRA adapters are used at **both the encoder and decoder**.

**Task framing:** This is not open-ended reaction generation and is not merely making a sentence sound more dramatic. Treat each persona as a target linguistic system. The output may change vocabulary, syntax, framing, implication, and rhythm, but it should preserve the source’s intended meaning and relevant facts.

**Core scientific question:** Does the stitched encoder–decoder system use source representations from the encoder to preserve meaning while realizing that meaning in the requested persona language?

---

## 1. Task definition and example

### Input

- A source sentence or short passage in ordinary language.
- A target persona label and its consistent persona-language specification.
- Optional context needed to resolve references or preserve intent.

### Output

A translation of the same underlying message into the target persona’s linguistic system.

Illustrative example (original wording, not a film quote):

**Source:** “I know you are planning something, but I don't know what it is yet.”

**Target persona:** Don

**Possible target:** “Interesting. You have a plan. I just haven't decided how much of it you should be allowed to finish.”

This is illustrative rather than a fixed gold answer. Persona-language translation is not word-for-word translation: the surface expression can change substantially, but the intended idea must remain recognizable. Dataset reviewers must reject outputs that invent a materially different event or abandon the source intent merely to sound like the persona.

### Two separate requirements

1. **Semantic preservation:** retain the source’s core proposition, facts, intent, and sentiment where applicable.
2. **Persona-language realization:** express that meaning in a recognizable and consistent target persona language.

Do not collapse these into one score. A fluent persona-like output can still be a bad translation if it changes the meaning.

---

## 2. Target architecture

```text
Source sentence / context
          |
          v
Bidirectional encoder (pretrained base frozen initially)
+ encoder LoRA adapter
          |
          v
Contextual encoder hidden states H
          |
          v
Trainable projection bridge + normalization
          |
          v
Cross-attention inserted into selected decoder layers
          |
          v
Autoregressive decoder (pretrained base frozen initially)
+ decoder LoRA adapter
          |
          v
Translation in requested persona language
```

The target persona specification is supplied consistently to the decoder as a control instruction/target-language description. The source content must reach the decoder through the encoder–bridge path in the **primary bridge experiment**. Do not also give the full source sentence directly to the decoder in that condition, because the decoder could bypass the bridge and solve the task without using encoder states. A separate direct-source decoder baseline can be evaluated later.

### Component responsibilities

- **Bidirectional encoder:** builds contextual representations of the source. Use a pretrained encoder such as `microsoft/deberta-v3-base` or `answerdotai/ModernBERT-base`, subject to environment compatibility.
- **Encoder LoRA:** adapts encoder representations to the translation task while keeping the encoder’s pretrained base weights frozen initially.
- **Projection bridge:** maps encoder hidden states to the decoder hidden dimension and calibrates their scale.
- **Cross-attention:** allows decoder positions to retrieve source information while generating each next token.
- **Autoregressive decoder:** generates the target persona-language sequence. Use `Qwen/Qwen2.5-1.5B-Instruct` as the first bridge decoder, with the agreed Hinglish adapter merged into the base first if that remains the selected starting checkpoint.
- **Decoder LoRA:** adapts the decoder to the persona-language targets and the new encoder-conditioning pathway while the original decoder weights remain frozen initially.
- **Training objective:** teacher-forced next-token prediction over target translation tokens only. Mask source/control/prompt tokens out of the loss and supervise the correct EOS/end-of-turn token.

**Important implementation distinction:** Qwen2.5 is pretrained as a decoder-only model and has no native cross-attention path by default. The custom architecture must explicitly add cross-attention modules and route encoder hidden states into the decoder forward and generation paths. Concatenating source text into the decoder prompt is not a stitched encoder–decoder bridge experiment.

---

## 3. Fixed persona-language inventory

Use the same six fictionalized persona definitions throughout the pilot. Use **original dialogue only**; do not copy film dialogue or quotations.

1. **Vijay (Deewar):** self-made, proud, bitter about injustice, quietly defiant, never backs down.
2. **Don:** cool and calculating, faintly amused, a step ahead; short controlled lines with a hint of threat.
3. **Shahenshah:** larger-than-life champion of justice; royal manner and grand Urdu-tinged language about honour and truth.
4. **Anthony Gonsalves:** cheerful and comic, playful exaggeration, freely mixes English.
5. **Vijay Dinanath Chauhan (Agneepath):** intense and terse, controlled anger, short blunt lines and long-held resolve.
6. **Jai (Sholay):** calm and laconic, dry humour, loyal and practical; says little.

The persona specification is the target-language control, not the source meaning. Keep its format stable across training, validation, and testing. Do not rely on a character name alone to convey the intended language; include the agreed description.

---

## 4. Dataset design: parallel persona-language translations

### Recommended first controlled pilot

Handcraft and review **60 distinct source statements**. For each source, create one translation for each of the six personas:

- 60 source statements × 6 target personas = **360 source–persona pairs**.
- Split by **source statement**, not by individual pair, so translations of the same source cannot leak across splits.
- A practical starting split is 40 source statements for training (240 pairs), 10 for validation (60 pairs), and 10 for blind testing (60 pairs).
- Keep the blind test unavailable for checkpoint selection and training decisions.

This is a pilot dataset, not a claim that 360 pairs are enough for production-quality persona translation. Quality and coverage matter more than volume at this stage.

### Source coverage

Include varied:
- communicative intents (assertion, refusal, uncertainty, warning, reassurance, apology, congratulations, negotiation, disagreement);
- sentiments and levels of intensity;
- sentence lengths and syntactic structures;
- concrete facts, relationships, and references that must survive translation;
- simple and context-dependent statements.

Avoid source statements that force every persona to invent a new reaction or event. The task is to translate a given message, not to answer a scenario with a newly invented response.

### Annotation rules

For every source:
1. Write the source in neutral, ordinary language.
2. Record its meaning in a short, persona-neutral semantic note (core proposition, facts, intent, sentiment).
3. Write six original translations, one per persona.
4. Check each translation against the semantic note.
5. Check that the six outputs differ in persona-language realization without needlessly changing the underlying message.
6. Mark ambiguous sources and revise or remove them rather than using them as noisy supervision.

Store at least: `example_id`, `source_id`, `source_text`, `semantic_note`, `target_persona`, `persona_spec_version`, `target_text`, `split`, and `review_status`. Preserve provenance and avoid near-duplicate sources across splits.

### Evaluation rubric

Rate these dimensions independently:
1. **Meaning preservation:** core proposition, facts, intent, and sentiment retained.
2. **Persona-language recognition:** a blind rater can identify the intended persona from the expression.
3. **Fluency/naturalness:** the output reads naturally in its intended language/register.
4. **Unsupported additions/deletions:** invented facts or dropped meaning.
5. **Repetition and termination:** repeated phrases, malformed output, and correct EOS/end-of-turn behavior.

Use blind, shuffled outputs for human persona recognition. Automated lexical/style metrics may be diagnostic, but must not substitute for semantic review.

---

## 5. Implementation and experiment sequence

### Phase 0 — Freeze the task contract and dataset

**Build**
- Freeze the persona-language definitions, prompt format, data schema, split IDs, generation settings, and evaluation rubric.
- Handcraft and review the parallel source/translation examples.
- Split by source ID, ensuring all six translations of a source stay in the same split.
- Record model/tokenizer versions and reproducible seeds.

**Gate**
- No source-level leakage across splits.
- Every target preserves the semantic note, is original, and is recognizably appropriate for its persona.
- All target sequences have correct termination supervision.

### Phase 1 — Validate the decoder baseline and training format

**Build**
- Load the selected decoder checkpoint and tokenizer.
- If using the existing Hinglish adapter, verify and document exactly how it is merged into the base.
- Confirm the chat/template format, target formatting, EOS handling, truncation, and generation behavior.
- Run a prompt-only baseline in which the decoder sees the source and target persona instruction directly. This is a useful task baseline, but **not** evidence that the bridge works.

**Record**
- Generated samples, target-token loss if available, stop reasons, and human rubric scores.

**Gate**
- The decoder can train and generate sensible, terminated target text with the chosen serialization. Fix template and data issues before adding bridge complexity.

### Phase 2 — Build the stitched bridge and verify the forward path

**Build**
- Run the bidirectional encoder and capture contextual hidden states.
- Add a trainable projection from encoder dimension to decoder dimension.
- Insert cross-attention into selected decoder layers; decoder self-attention remains causal.
- Route encoder states through the projection into each intended cross-attention layer.
- Unit-test tensor shapes, attention masks, padding, gradients, device/dtype behavior, and autoregressive generation.
- Verify pretrained decoder weights load as expected; missing keys should be explained by newly introduced modules.

**Trainable during smoke tests**
- Projection bridge and new cross-attention modules.
- Keep encoder base and decoder base weights frozen.
- LoRA adapters may be instantiated but do not begin full adapter training until the forward path and loss are verified.

**Gate**
- End-to-end forward and generation work.
- Cross-attention receives encoder states and padding is masked correctly.
- Gradients reach the bridge/cross-attention parameters.
- The code is not silently falling back to ordinary decoder-only inference.

### Phase 3 — Train the first end-to-end bridge with LoRA at both ends

This is the first actual task-training stage. Both encoder and decoder LoRA are part of the intended architecture.

**Trainable**
- Encoder LoRA adapter.
- Projection bridge.
- Added cross-attention modules.
- Decoder LoRA adapter.

**Frozen**
- Pretrained encoder base weights.
- Original pretrained decoder base weights.

**Training**
- Use teacher forcing.
- Compute loss only over target translation tokens; mask source/control/prompt tokens.
- Use a small smoke subset first, then train on the full training split.
- Track trainable parameter counts and gradient norms separately for encoder LoRA, bridge, cross-attention, and decoder LoRA.
- Save checkpoints and evaluate every epoch; do not assume the final epoch is best.

**Gate**
- Training loss decreases without degenerate outputs.
- Held-out meaning preservation and persona-language recognition show improvement over the initial baseline.
- No single module has zero gradients or is unintentionally excluded from optimization.

### Phase 4 — Prove the encoder–bridge contribution with controlled interventions

Run the same held-out sources, target personas, decoder settings, and checkpoint under these conditions:

- **A. Full system:** correct source encoder states, bridge, cross-attention, encoder LoRA, and decoder LoRA.
- **B. Encoder ablation:** replace the source representation with a defined null/learned-null representation while keeping dimensions and the rest of the model unchanged.
- **C. Mismatched source:** feed encoder representations from a different source statement with the same shape. Keep the requested target persona fixed.
- **D. Direct-source decoder baseline:** give source text directly to the decoder with the target persona instruction, without using the encoder bridge. This is a task baseline, not the main bridge condition.
- **E. Optional frozen-adapter comparison:** compare with encoder LoRA disabled or with a frozen pretrained encoder, to measure the value of encoder adaptation separately.

**Measure**
- Held-out target-token negative log-likelihood/log-probability under controlled conditions.
- Human meaning-preservation scores and unsupported additions/deletions.
- Persona-language recognition and fluency.
- Changes caused by null and mismatched source representations.

**Interpretation**
- If A and B are indistinguishable, the encoder path may be ignored, bypassed, or insufficiently trained.
- If A differs from B but is not better, the encoder has influence but useful influence has not been demonstrated.
- If C causes source-specific facts or intent to shift toward the mismatched source, that is evidence that the model uses encoder information.
- The full system must improve semantic preservation over ablations; output changes alone do not prove success.
- Compare A with D fairly. The bridge need not beat every strong direct-source baseline on every metric, but the experiment must report the result honestly.

**Gate**
- Show both causal sensitivity to encoder interventions and a measurable held-out benefit from correct source representations.

### Phase 5 — Diagnose and tune the two LoRA adapters separately

Only after Phase 4 establishes a working, useful bridge, run controlled adapter comparisons:

1. Both encoder and decoder LoRA enabled.
2. Encoder LoRA disabled; decoder LoRA enabled.
3. Encoder LoRA enabled; decoder LoRA disabled.
4. Both LoRA adapters disabled, with trained bridge/cross-attention retained where the comparison is meaningful.

Keep base weights, data, prompts, generation settings, and checkpoint-selection rules controlled. Treat these as diagnostic ablations, not necessarily the best deployment configuration.

Tune one factor at a time: LoRA rank, target modules, learning rates, and adapter dropout. Begin conservatively (for example, rank 8 or 16) and do not increase rank and target modules simultaneously in the first comparison. Re-run encoder-intervention tests after changes to ensure the decoder has not learned to ignore the bridge.

**Gate**
- Understand whether each adapter contributes and select the simplest configuration that improves held-out translation quality without erasing encoder dependence.

### Phase 6 — End-to-end blind evaluation

Evaluate the best checkpoint against:
- direct-source decoder baseline;
- full stitched system;
- encoder ablation;
- mismatched-source intervention;
- encoder-LoRA and decoder-LoRA ablations.

Use the same held-out and blind test sources and fixed decoding settings. Have raters judge shuffled outputs without knowing the system condition.

Report:
- meaning preservation;
- persona-language recognition;
- fluency/naturalness;
- unsupported additions/deletions;
- held-out target-token loss;
- repetition and termination behavior;
- encoder intervention effects;
- representative successes and failures for every persona.

**Gate**
- The full system demonstrates a credible benefit on the intended translation task and beats its own encoder ablations on semantic preservation. Do not claim success from training loss or persona resemblance alone.

### Phase 7 — Joint fine-tuning and scaling

Only after the controlled evaluation:
1. Start from the best Phase 6 checkpoint.
2. Jointly fine-tune encoder LoRA, bridge, cross-attention, and decoder LoRA using conservative learning rates.
3. Keep both pretrained base models frozen initially; only LoRA and bridge-side trainable modules are updated.
4. Consider selectively unfreezing top encoder layers only if controlled evidence identifies the encoder representation as a bottleneck. This is a separate experiment.
5. Expand the manually reviewed parallel dataset only after the pilot pipeline is reproducible.
6. Compare every major change against the same blind evaluation protocol and rerun encoder ablations.

Stop or roll back if training loss improves while meaning preservation, persona recognition, or encoder dependence worsens.

---

## 6. Training schedule at a glance

| Stage | Encoder base | Encoder LoRA | Bridge + cross-attention | Decoder base | Decoder LoRA |
|---|---|---|---|---|---|
| Decoder/task baseline | Not used in direct-source baseline | N/A | None | Frozen pretrained | None initially |
| Bridge smoke test | Frozen | Off/not trained | Train | Frozen | Off/not trained |
| First end-to-end training | Frozen | Train | Train | Frozen | Train |
| Encoder causal tests | Frozen | Fixed per checkpoint | Fixed per checkpoint | Frozen | Fixed per checkpoint |
| Adapter ablations | Frozen | Toggle per condition | Fixed per checkpoint | Frozen | Toggle per condition |
| Joint fine-tuning | Frozen initially | Train | Train | Frozen | Train |
| Optional encoder unfreezing | Selective only if justified | Train | Train | Frozen | Train |

The smoke test verifies the bridge plumbing before adapter training. The first full task-training phase then trains **both LoRA adapters**, bridge, and cross-attention together while keeping the pretrained base weights frozen. Controlled interventions determine whether this learned system actually uses the encoder signal.

---

## 7. Critical implementation checks

- **No accidental bypass:** in the primary bridge condition, source content reaches the decoder through encoder states, not by also copying the full source into the decoder prompt.
- **Cross-attention:** implement explicitly; the chosen decoder has no native cross-attention by default.
- **Causal mask:** decoder self-attention remains causal; cross-attention masks encoder padding correctly.
- **Loss mask:** only target translation tokens contribute to supervised loss.
- **EOS:** include and supervise the correct end-of-turn/EOS token.
- **Gradient audit:** report trainable parameter counts and gradient norms separately for encoder LoRA, bridge, cross-attention, and decoder LoRA.
- **Weight loading:** verify expected missing/unexpected keys when adapting the pretrained decoder.
- **Generation path:** prove encoder states are passed during every generation step, including cached decoding if a cache is implemented.
- **Fair ablation:** hold prompts, target persona instruction, model checkpoint, decoding settings, and evaluation sources constant.
- **Data leakage:** split by source statement, not by translation pair.
- **Reproducibility:** save configs, source IDs, split IDs, checkpoints, metrics, and generated samples.
- **Original content:** use original persona-language examples, not copied film dialogue.

---

## 8. Decision checklist

- [ ] Task is framed as meaning-preserving persona-language translation.
- [ ] Parallel source/target examples are reviewed and split by source ID.
- [ ] Decoder direct-source baseline is valid and reproducible.
- [ ] Custom encoder–bridge–cross-attention–decoder forward/generation path works.
- [ ] Bridge/cross-attention gradients are nonzero.
- [ ] Both encoder and decoder LoRA adapters are trained in the first full end-to-end task stage.
- [ ] Correct encoder representations improve held-out semantic preservation over encoder ablation.
- [ ] Mismatched source representations cause measurable, interpretable source-specific changes.
- [ ] Encoder-LoRA and decoder-LoRA contributions are tested separately.
- [ ] Full system is evaluated blindly against the direct-source baseline and bridge ablations.
- [ ] Only then begin joint fine-tuning or scale the dataset.

**Success criterion:** With controlled interventions, demonstrate that the encoder representations pass through the trainable bridge, influence the decoder's next-token distribution, and improve meaning-preserving translation into the requested persona language. The final claim must be supported by held-out and blind evaluation—not merely lower training loss or a more recognizable persona voice.
