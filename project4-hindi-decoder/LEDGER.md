# Project 4 — Ledger

Two kinds of entries, newest last in each section:

- **Integration notes**: problems met while wiring the pieces together, why they happen, and the fix. Written to be lifted into the blog.
- **Runs**: one entry per Kaggle run (to be filled from the notebooks' saved outputs).

## Integration notes

### I1 — Generating from a prefix of embeddings with Gemma 3 (2026-10-20, `9-prefix-bridge/`, commit `57793db`)

**Setting.** The prefix bridge feeds the encoder's output to Gemma 3 4B IT as input vectors: `[<bos>] + prefix vectors + target`, passed as `inputs_embeds`. Training works: a plain forward pass of `Gemma3ForConditionalGeneration` accepts `inputs_embeds`.

**Problem.** Generation does not:

```
ValueError: You passed `inputs_embeds` to `.generate()`, but the model class Gemma3ForConditionalGeneration
doesn't have its forwarding implemented.
```

**Why.** `generate()` only accepts embeddings as the starting point for model classes whose generation-input preparation supports it (GPT-2 and most text-only decoders do). Gemma 3's multimodal class (`transformers` 5.17) does not, because it builds its own inputs from token ids (it looks for image tokens in them).

**Fix.** Give `generate()` token ids it can work with and swap in the vectors underneath:

1. Build the prompt as ordinary ids: `<bos>` followed by one **placeholder token** per prefix vector (any fixed token; we use `" ."`).
2. Register a **forward hook on Gemma's input-embedding layer**. When a prefix is waiting and the embedding output has the prompt's length (`1 + number of prefix vectors`), the hook replaces positions `1 …` with the prefix vectors and clears the waiting prefix.
3. That happens on the first (full-prompt) forward pass only; every later step embeds a single new token, so the hook leaves it alone, and `generate()` runs normally with its KV cache.

```python
def write_prefix(module, args, output):
    if SLOT.vectors is not None and output.dim() == 3 and output.shape[1] == 1 + len(SLOT.vectors):
        output = output.clone()
        output[:, 1:] = SLOT.vectors.to(output.dtype)
        SLOT.vectors = None
    return output

EMBED.register_forward_hook(write_prefix)          # EMBED = dec_model.get_input_embeddings()
```

**Guard.** `translate()` asserts the prefix was consumed, so a silent failure (the hook not firing, wrong length) stops with an error instead of producing text from placeholder tokens. Training is unaffected: it passes `inputs_embeds` and never calls the embedding layer with a waiting prefix.

**Why it is a correct substitute.** Gemma's embedding layer applies its own scaling (`× √hidden`); the hook replaces the *output* of that layer, so the prefix vectors enter at the same point and scale as in training, where they were concatenated with already-scaled token embeddings.

### I2 — Long runs on Kaggle: a silent kernel death, and pinned versions that did not install (2026-10-20, `9-prefix-bridge/`)

**What happened.** Stage 1 of the prefix bridge died after step 1000 of 1500, about 70 minutes in, with no Python error: the kernel simply restarted. GPU memory was not the cause (peak 8.1 GB of 15; a GPU shortage raises `OutOfMemoryError` instead). A kernel death without an error is almost always the machine's RAM. All progress was lost, because nothing was saved until the end of the stage.

The same run also printed `transformers 5.16.1, peft 0.20.0` although Cell 1 installs `5.17.0` and `0.21.2`, with warnings `Ignoring invalid distribution ~ransformers`. An earlier interrupted install had left a half-removed package in the environment, and the pinned install silently did not take.

**Fixes.**

- **Checkpoint and resume.** Every 500 steps, Cell 6 saves weights, optimizer state, scheduler state, step and log to `/kaggle/working/stage1_ckpt.pt`. On a restarted kernel, running all cells again rebuilds the same corpus (fixed seed) and the cell resumes from the checkpoint. It checks that the checkpoint belongs to a corpus of the same size.
- **Less RAM.** The full corpus tables (≈ 190k rows) are deleted once the 12,000 pairs are sampled, and `gc.collect()` plus `torch.cuda.empty_cache()` run at every checkpoint.
- **Pinned versions enforced.** `pip install --force-reinstall --no-deps` for the two pinned packages, and an assertion that stops the notebook if the versions in use are not the pinned ones.

**Lesson for the blog.** On a shared notebook service, a multi-hour training loop needs checkpoints as much as a cluster job does. Also, *check* the versions you pinned; don't assume the install worked.

## Runs

*Earlier runs (Phases 1–3, notebook 7) are summarised in the README's stage table and in their commit messages; full entries to be backfilled.*

### R8 — Cross-attention bridge, pre-trained (2026-10-20, `8-bridge-pretraining/`, commit `52f21f7`)

- **Setup:** ModernBERT-base + LoRA → bridge (Linear 768→2560) → 8 gated cross-attention blocks (≈ 210 M, from scratch) in Gemma 3 4B IT (4-bit) + LoRA; the decoder's only input is `<bos>`. Stage 1: 24,000 public English → Hinglish pairs (Hinglish-TOP + PHINC), one pass (3,000 steps of 8). Stage 2: v4 persona data (768 pairs), kept epoch 1 of 3.
- **Stage 1:** held-out loss 9.43 → 3.08; on 120 held-out corpus pairs chrF **27.6**, 119 distinct. Output keeps the kind of sentence and its grammar but swaps specifics ("weather in Kingston" → "New York me mausam kaisa hai").
- **Stage 2 (v4):** chrF validation **18.4** / test 17.8 / out-of-domain 18.4; 71 of 75 distinct (no collapse, against 5 of 75 without pre-training). Meaning mostly not preserved ("Kabir lands in Delhi at 9 tonight" → "Aaj raat 11 baje Mumbai ka traffic kharaab hoga").
- **Decision:** the cross-attention design needs far more data to carry details; try the prefix design (R9).

### R9 — Prefix bridge, pre-trained (2026-10-20, `9-prefix-bridge/`)

- **Setup:** ModernBERT-base + LoRA → bridge (MLP 768→2560→2560 + RMSNorm at Gemma's embedding scale, ≈ 8.5 M) → one input vector per English token, placed after `<bos>`; Gemma 3 4B IT (4-bit) + LoRA reads them with its own attention. No cross-attention blocks. Stage 1: **12,000** public pairs (6,000 Hinglish-TOP + 6,000 PHINC), 1,500 steps of 8 (one kernel death at ≈ step 1000; resumed from checkpoint, see I2). Stage 2: v4, kept epoch 2 of 4. Integration fix for generation: I1.
- **Stage 1:** held-out loss 9.57 → **2.28** (3.36 at step 1000); chrF **41.9**, 120 of 120 distinct. Specifics now carried ("weather in Kingston" → "Kingston me mausam kaisa hai"; "Berry Hill" → "Bar Hill"; "tomorrow" → "kal").
- **Stage 2 (v4):** chrF validation **31.9** / test **29.6** / out-of-domain **33.3**; 75 of 75 distinct; stopping 99–100 %. Meaning largely preserved, persona voices present: "Kabir lands in Delhi at 9 tonight" → "Kabir aaj raat Delhi pahunch jaayega" (the time dropped); "The plumber charged 4,000 for 2 hours…" → "Plumber ne 4,000 paise 2 ghante mein lete hain. Kya woh rate hai jo usne di?"; Anthony: "AC phir se band ho gaya—yeh bhi reboot karna hoga!".
- **Comparison:** with half the stage-1 data and ≈ 4 % of the new parameters, the prefix design beats the cross-attention design on every measure (stage-1 chrF 41.9 vs 27.6; v4 validation 31.9 vs 18.4).
- **Open:** the direct-source baseline on v4 (Gemma reading the English in its prompt) to judge how much the bridge still loses; occasional dropped numbers or details.
