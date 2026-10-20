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

## Runs

*(to be filled)*
