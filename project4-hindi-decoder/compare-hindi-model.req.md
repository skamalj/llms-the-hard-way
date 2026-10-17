# Requirement: Hindi/Hinglish Decoder Model Comparison

**File:** `compare-hindi-model.req.md`  
**Project:** Project 4 — Character Personality Classifier & Dialogue Style Transfer  
**Status:** Draft requirements for implementation  
**Primary objective:** Compare small Hugging Face decoder models for Hindi and Romanized Hinglish generation before selecting a decoder for the custom stitched encoder-decoder architecture.

---

## 1. Background

Project 4 builds a custom stitched encoder-decoder Transformer:

1. A bidirectional encoder reads an input scenario and persona tag.
2. A projection bridge maps encoder hidden states to the decoder's hidden dimension.
3. Custom cross-attention layers allow decoder queries to attend to encoder representations.
4. An autoregressive decoder generates a persona-conditioned response.

The decoder should produce natural Hindi or Hinglish. Before integrating a decoder into the custom architecture, we need a small, reproducible comparison of candidate pretrained checkpoints and, where applicable, existing language-specific adapters.

This comparison is a **model-selection experiment**, not the implementation of the stitched architecture itself.

## 2. Goals

- Identify a small decoder with credible documented Hindi and/or Romanized Hinglish capability.
- Compare generated responses on identical inputs.
- Separate documented model-card claims from capabilities observed in our own tests.
- Check whether outputs are fluent, coherent, appropriately code-switched, and consistently written in the requested script.
- Assess integration risks for a custom decoder with added cross-attention.
- Produce a recommendation backed by saved prompts, outputs, configuration, and evaluation results.

## 3. Non-goals

This experiment does not:

- Train the six cinematic personas.
- Implement or train the encoder, projection bridge, or custom cross-attention.
- Claim that a model supports Hinglish merely because its model card says it supports Hindi or multiple languages.
- Treat illustrative outputs, model-card descriptions, or unexecuted code as actual benchmark results.
- Automatically merge or modify any model or adapter weights.
- Establish production readiness or prove generalization from a small phrase set.

## 4. Candidate models

Start by verifying each model's current Hugging Face model card, license, architecture, tokenizer, loading instructions, and available weights. Repository identifiers below are candidate identifiers and must be checked before execution.

| Candidate | Hugging Face repository | Why include it | Key question |
|---|---|---|---|
| Qwen2.5-1.5B + Hinglish adapter | Base: `Qwen/Qwen2.5-1.5B`; adapter candidate: `sarthaksenapati/qwen1.5b-hinglish-sft-v2` | Reference candidate with an adapter specifically described as Hinglish-oriented | Does the adapter load correctly and produce natural Romanized Hinglish on our test prompts? |
| Gemma 3 1B Instruct | `google/gemma-3-1b-it` | Compact instruction model with documented multilingual support | How natural are its Hindi and Hinglish outputs? Check license/access requirements. |
| Gemma 3 1B Hindi fine-tune | `pankajpandey-dev/gemma-3-1b-hindi-instruct` | Community checkpoint described as Hindi-focused | Are its training details, base-model compatibility, and license suitable? Does it handle Romanized Hinglish? |
| Llama 3.2 1B Instruct | `meta-llama/Llama-3.2-1B-Instruct` | Compact instruction model with documented Hindi support | Is its output quality competitive, and are access/license conditions acceptable? |
| Qwen3-0.6B | `Qwen/Qwen3-0.6B` | Smallest candidate; useful as a lightweight baseline | Is Hindi/Hinglish quality sufficient despite the smaller size? |
| MiniCPM5 Hindi Instruct candidate | `pankajpandey-dev/MiniCPM5-1B-Hindi-Instruct` | Community checkpoint described as Hindi-focused | Verify repository, base architecture, tokenizer, loading code, license, and checkpoint integrity before use. |

### 4.1 Candidate verification requirements

Before benchmarking a candidate, record:

- Exact repository ID and immutable revision/commit where available.
- Model-card URL and date checked.
- Base model and architecture.
- Parameter count as reported by a reliable source.
- License and any gated-access conditions.
- Tokenizer and chat-template requirements.
- Whether the checkpoint is a base model, instruction model, full fine-tune, or adapter.
- If it is an adapter: its base-model reference, adapter type/configuration, target modules, and any special tokenizer requirements.
- Loading method and any custom-code requirement.

Do not silently substitute a different model if a repository is missing, inaccessible, renamed, or incompatible. Mark it as blocked and document why.

## 5. Output modes

Evaluate these modes separately:

1. **Hindi-Devanagari:** response primarily in natural Hindi using Devanagari script.
2. **Hinglish-Roman:** conversational Hindi-English code-mixing primarily written in Latin/Roman script.

Do not combine the scores for these two modes into a single score without also reporting the individual mode scores. A model may perform well in one and poorly in the other.

If the model does not follow a requested script, record that as a result rather than silently correcting the generated output.

## 6. Test set

Create a fixed set of **20 prompts** before running the benchmark. Use the same semantic prompts for every candidate and both output modes where feasible.

Include varied scenarios:

- Friendship, trust, and betrayal.
- Everyday inconvenience, such as an internet outage.
- Workplace conflict and taking credit for another person's work.
- Honesty and moral choices.
- Humour and an otherwise boring day.
- Explaining a simple concept conversationally.
- An emotional but non-violent disagreement.
- A short supportive response.
- A request to explain something in plain language.
- Ambiguous or context-light prompts that test whether the model invents unnecessary details.

At least some prompts should originate in English and some in informal Hinglish. Preserve the original prompt exactly across candidates.

### 6.1 Prompt protocol

Each test case must specify:

- Stable `case_id`.
- Input text.
- Requested output mode (`hi-Deva` or `hinglish-Latn`).
- Expected response characteristics.
- Any known script or language constraints.

Use an explicit instruction to generate the requested output mode. Do not include cinematic persona tags in this first experiment, because the goal is to evaluate the language-generation starting point before persona fine-tuning.

## 7. Generation protocol

For a fair first comparison:

- Use each model's documented chat template, if it is an instruction-tuned model.
- Follow the checkpoint's documented loading and generation requirements.
- Use a consistent generation configuration where the architectures permit it.
- Record all deviations required by a model's documentation.
- Use a fixed seed where supported.
- Run greedy decoding (`do_sample=False`) for the initial reproducible pass.
- Set a consistent maximum generation length, such as 100 new tokens, unless the model requires a justified adjustment.
- Prevent accidental inclusion of the input prompt in the saved response.
- Record tokenizer and generation configuration with the output.
- Do not claim a model was tested until inference actually completed.

If sampling is later evaluated, run it as a separate experiment with the sampling parameters recorded.

## 8. Evaluation rubric

Score each output on a 1–5 scale. Save the individual scores and short rationale.

| Dimension | What to assess |
|---|---|
| Language naturalness | Does it sound like natural contemporary Hindi or Hinglish rather than word-for-word translation? |
| Semantic correctness | Does it respond to the prompt and preserve its intended meaning? |
| Script compliance | Does it use the requested script consistently, apart from reasonable English words in Hinglish? |
| Code-switching quality | For Hinglish, are Hindi-English transitions natural and appropriate rather than random? |
| Grammar and readability | Is the sentence structure understandable, grammatical, and easy to read? |
| Repetition and degeneration | Does it avoid loops, repeated phrases, broken endings, or unnecessary padding? |
| Instruction following | Does it obey the requested style, length, and output mode? |

### 8.1 Scoring and reporting

- Report each dimension's average for each model and output mode.
- Report per-prompt results as well as aggregate scores.
- Report the number of failed or unavailable runs.
- Include example outputs that represent strong, typical, and weak results.
- Do not use only an aggregate score to hide poor performance in one output mode.
- If multiple reviewers are available, use at least two reviewers for a subset and document disagreements.
- Any automated language metric must be described as supplementary; it must not replace qualitative review.

## 9. Adapter experiment for Qwen2.5-1.5B

For the Qwen Hinglish candidate, compare:

- **A. Base only:** `Qwen/Qwen2.5-1.5B`.
- **B. Base + existing Hinglish adapter:** load the adapter using its documented method.
- **C. Merged checkpoint (optional):** merge the existing adapter into a copy of the base model and evaluate the merged copy.

Requirements:

- First verify that the adapter actually targets the exact base checkpoint.
- Do not assume the adapter's name proves its method; inspect its configuration.
- Do not overwrite the original base weights.
- Keep model revision, tokenizer, chat template, and generation settings documented.
- Confirm that the base-plus-adapter and merged variants produce comparable results under the same inference conditions.
- Preserve the original adapter and base model so the experiment is reproducible.
- Treat a merge as a testable deployment option, not a prerequisite for evaluating the adapter.

A future persona LoRA may be trained on top of the Hinglish-adapted model. This comparison does not train that persona LoRA.

## 10. Integration considerations for the stitched decoder

Language quality is only one selection criterion. For the leading candidates, document:

- Decoder layer structure and hidden size.
- Attention head count and key/value head configuration.
- Positional embedding method and relevant configuration.
- Normalization and residual structure.
- Tokenizer vocabulary and special-token handling.
- How the pretrained decoder's causal self-attention and generation loop are implemented.
- Feasibility of adding cross-attention without replacing or breaking the pretrained pathways.
- Whether custom model code is needed and whether its license permits the intended use.
- Feasibility on the available two-NVIDIA-T4 setup, including memory use and inference latency if measured.

Do not assume that a small parameter count alone guarantees compatibility with the custom stitched architecture.

## 11. Deliverables

Produce the following artifacts:

1. `compare-hindi-model.req.md` — this requirement document.
2. `compare-hindi-model-prompts.jsonl` — fixed 20-prompt benchmark set.
3. `compare-hindi-model-results.jsonl` — raw outputs and run metadata.
4. `compare-hindi-model-scores.csv` — per-output scores and rationale.
5. `compare-hindi-model-report.md` — summary, candidate verification, results, caveats, and recommendation.
6. Optional scripts/notebooks to run the benchmark, with dependencies and execution instructions.

Each raw result should contain, at minimum:

- `case_id`
- `model_id`
- `model_revision`
- `adapter_id` or `null`
- `output_mode`
- `input`
- `generated_output`
- `generation_config`
- `status`
- `error` or `null`

Scores must reference the corresponding `case_id`, model variant, and output mode.

## 12. Acceptance criteria

The experiment is complete when:

- All candidate repository identifiers have been verified or explicitly marked blocked.
- The fixed test set is identical across candidates.
- Hindi-Devanagari and Hinglish-Roman are reported separately.
- Raw outputs and run configurations are saved.
- Failed runs are visible and not omitted from the report.
- The report distinguishes documented claims from measured results.
- At least one candidate is recommended based on evidence, with trade-offs stated.
- Any recommendation for the stitched architecture accounts for both language quality and integration complexity.
- No fabricated or manually invented response is represented as model-generated output.

## 13. Decision rule

Select the candidate that offers the best practical balance of:

1. Naturalness in the required output mode.
2. Correctness and instruction following.
3. Consistent script and, for Hinglish, natural code-switching.
4. Reproducibility and model-card transparency.
5. Compatibility with the custom stitched decoder.
6. License suitability and feasibility on available hardware.

If no candidate performs well in both modes, choose the target mode for the first implementation and treat the other mode as a separate follow-up experiment.

---

## 14. Current status and open questions

This document defines the intended experiment. It does **not** assert that the listed candidates have already been downloaded, executed, or benchmarked.

Before implementation, confirm:

- Whether the primary target is Hinglish-Roman, Hindi-Devanagari, or both.
- The runtime environment and available GPU memory.
- Whether model downloads can access Hugging Face and any gated repositories.
- Whether training will use the standard Hugging Face implementation before custom inference is built.
