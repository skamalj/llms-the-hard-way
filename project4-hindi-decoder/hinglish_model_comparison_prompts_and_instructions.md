# Hinglish Model Comparison: Prompts and Instructions

## Goal

Validate the text-generation pipeline before training the six character
personas. The immediate target is **natural, readable Roman-script
Hinglish**. Voice and TTS are out of scope for this stage.

Compare only these two candidates first:

1.  `Qwen/Qwen2.5-1.5B` with the Hinglish adapter
    `sarthaksenapati/qwen1.5b-hinglish-sft-v2` --- first verify that the
    adapter is compatible with the exact base-model revision.
2.  `google/gemma-3-1b-it`

Do not train the persona model yet. First determine whether the
inference setup produces usable text.

------------------------------------------------------------------------

## 1. System instruction

Use this instruction for both models, adapting only the wrapper to each
model's required chat template:

``` text
You write natural, conversational Hinglish using the Roman/Latin alphabet.

Follow these rules:
- Write Hindi words in Roman script, mixed naturally with English where appropriate.
- Do not use Devanagari.
- Do not explain your process or repeat the instructions.
- Respond directly to the scenario in 1–3 short sentences.
- Keep the wording natural and readable, like something a person would actually say.
- Do not repeat phrases or sentences.
- Do not add labels, headings, quotation marks, or a character name unless the scenario asks for them.
- Do not copy dialogue from films or other copyrighted sources.
```

### Important formatting rule

Use each model's **official tokenizer/chat template**. Do not assume the
two models share the same prompt format. For chat models, apply the
model's chat template with an assistant-generation prompt as documented
for that model.

When measuring generated output, decode **only the newly generated
tokens**, not the original prompt plus generated continuation. Check the
model's EOS/stop-token handling. Prompt leakage, malformed special
tokens, and repeated output may indicate a pipeline/configuration issue
rather than only a model-quality issue.

------------------------------------------------------------------------

## 2. Five fixed comparison prompts

Use the exact same prompts for both models. Keep the system instruction
above unchanged.

### Prompt 1 --- Casual everyday Hinglish

``` text
Scenario: Abhee chai ka mood hai, but kaam bhi pending hai.
Write a short, natural response that a person might say in this situation.
```

### Prompt 2 --- Company celebration

``` text
Scenario: Aaj Lumiq company ke 13th anniversary ki party hai, and the whole team is excited.
Write a short, natural Hinglish response that fits this moment.
```

### Prompt 3 --- Boring day

``` text
Scenario: Today was so boring that I counted the ceiling fan's rotations.
Write a witty but natural Hinglish response. Do not translate the scenario literally.
```

### Prompt 4 --- Credit score

``` text
Scenario: My friend is worried because their credit score dropped.
Write a short, empathetic Hinglish response that sounds conversational, not like a formal article.
```

### Prompt 5 --- Something happened again

``` text
Scenario: It happened again, and this time I am really fed up.
Write a short, natural Hinglish response that conveys frustration without over-explaining.
```

------------------------------------------------------------------------

## 3. Generation settings for the first pass

Use comparable settings across models where the models support them:

-   Maximum new tokens: **80**
-   Sampling: start with **greedy decoding** (`do_sample=False`) for
    reproducibility.
-   Do not add repetition penalties or other decoding tricks in the
    first pass; first establish a clean baseline.
-   Use the correct model-specific EOS/stop-token configuration.
-   Record the exact model ID, adapter ID/revision, tokenizer, chat
    template, generation parameters, and library versions.
-   If a model requires a model-specific recommended inference path,
    follow its official instructions and document the difference.

If greedy decoding is consistently too stiff, run a second pass with
sampling. Keep that separate from the baseline so the results remain
interpretable.

------------------------------------------------------------------------

## 4. Manual evaluation rubric

Rate every output from **1 to 5**. Do not treat automatic script checks
or clean stopping as proof of language quality.

  ---------------------------------------------------------------------------
  Criterion             1 --- Poor        3 --- Acceptable  5 --- Strong
  --------------------- ----------------- ----------------- -----------------
  Naturalness           Broken or         Understandable,   Sounds like
                        unnatural         somewhat awkward  natural
                                                            conversation

  Scenario relevance    Misses the        Generally         Directly and
                        situation         on-topic          appropriately
                                                            responds

  Grammar/readability   Hard to           Readable with     Clear, fluent and
                        understand        noticeable issues easy to read

  Roman-script          Mostly Devanagari Mixed script or   Hindi/Hinglish
  compliance            or wrong script   inconsistent      consistently in
                                                            Roman script

  Code-switching        Awkward language  Understandable    Hindi and English
                        mixing            mixing            mix naturally

  Repetition            Loops or repeats  Some unnecessary  No noticeable
                        phrases           repetition        repetition

  Instruction following Leaks prompt or   Follows most      Follows all
                        ignores           constraints       constraints
                        constraints                         cleanly
  ---------------------------------------------------------------------------

For each result, record: - Model/variant - Prompt ID - Generated
output - Scores for all seven criteria - Notes on prompt leakage,
malformed tokens, repetition, or premature stopping

A short human review is required before selecting a winner. The
automatic checks in the earlier comparison are diagnostic signals only;
they are not human quality scores.

------------------------------------------------------------------------

## 5. Troubleshooting checklist

If outputs are broken, do these checks before concluding that the model
itself is unsuitable:

1.  **Chat template:** Confirm that the model's official chat template
    is being applied correctly.
2.  **Assistant prefix:** Confirm the prompt ends at the correct
    assistant-generation point.
3.  **Output slicing:** Decode only tokens generated after the input
    prompt.
4.  **Stop handling:** Confirm EOS and any model-specific stop tokens
    are recognized.
5.  **Token inspection:** If the text contains visible special-token
    fragments or malformed output, inspect generated token IDs and
    decoding.
6.  **Prompt leakage:** Check whether the model is continuing or
    reproducing the instruction instead of answering the scenario.
7.  **Repetition:** First reproduce the issue with greedy decoding and
    the 80-token limit before trying penalties.
8.  **Adapter compatibility:** For Qwen, verify the adapter's intended
    base model and tokenizer, and confirm it is loaded or merged as
    intended.

Do not start persona fine-tuning while these checks are unresolved.

------------------------------------------------------------------------

## 6. Decision rule

Choose a base candidate only if it repeatedly produces readable,
relevant Roman-script Hinglish across the five prompts, without severe
repetition, prompt leakage, or broken stopping.

-   If one model is clearly better under a correctly configured
    pipeline, use it for the next small persona-training pilot.
-   If both are poor, fix the inference pipeline and rerun before
    expanding the dataset.
-   Do not infer that a model is best based only on Roman-script
    compliance or clean stopping.

------------------------------------------------------------------------

## 7. What happens after this comparison

Once the text-generation baseline is reliable:

1.  Use the existing 60-example pilot: 10 examples for each of the six
    personas.
2.  Train a small LoRA/SFT persona pilot rather than immediately
    training the full decoder.
3.  Hold out scenarios for evaluation.
4.  Test whether the same scenario produces meaningfully different
    dialogue for each persona.
5.  Expand toward 360 examples (60 per persona) only if the pilot shows
    a measurable improvement.
6.  Keep voice/TTS work deferred until text generation is reliable.

The six personas are Vijay (*Deewar*), Don, Shahenshah, Anthony
Gonsalves, Vijay Dinanath Chauhan (*Agneepath*), and Jai (*Sholay*).
Generate original dialogue inspired by broad character traits; do not
reproduce recognizable film dialogue.
