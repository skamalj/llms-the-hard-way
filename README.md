# LLMs the Hard Way

Small, CPU-friendly Jupyter notebooks that open up real language models and rebuild their internals by hand: embeddings, attention, RoPE, the KV cache and LoRA fine-tuning. Each notebook computes every step manually and then checks the result against the Hugging Face implementation.

Everything runs on a laptop CPU. The models are tiny (a 2-dimensional GPT-2 and the 135M-parameter SmolLM family), so every tensor can be printed and inspected.

## Notebooks

The suggested reading order is top to bottom.

| Notebook | Model | What it covers |
|---|---|---|
| [`kv_cache_experiment.ipynb`](kv_cache_experiment.ipynb) | `sshleifer/tiny-gpt2` | A complete GPT-2 forward pass by hand on a model with 2-dim embeddings: token + position embeddings, LayerNorm, the packed `c_attn` Q/K/V projection, multi-head split, causal mask, softmax, residuals, the GELU MLP, both blocks, `ln_f` and the LM head. Ends with an end-to-end check that the manual result matches the model. |
| [`smollm2_forward_pass_kv_cache.ipynb`](smollm2_forward_pass_kv_cache.ipynb) | `HuggingFaceTB/SmolLM2-135M` | The same walkthrough for a modern Llama-style model: RMSNorm, grouped-query attention (9 query / 3 KV heads), RoPE, `repeat_kv` and the SwiGLU MLP. Layer 0 is traced by hand and layers 1–28 run through `layer.forward()`. The last layer runs as a **KV-cache decode step**: cached K/V for earlier tokens, and fresh Q/K/V only for the new token. Final logits match Hugging Face to within about 3e-5, and the notebook works for any prompt length. |
| [`rope.ipynb`](rope.ipynb) | `HuggingFaceTB/SmolLM2-135M` | Rotary position embeddings from scratch: the 32 rotation pairs of a 64-dim head, the `inv_freq` frequencies, per-position angles, rotating one pair and then a whole head by hand, length preservation, an exact match with `apply_rotary_pos_emb`, and why RoPE makes attention depend on relative position. |
| [`smoll_json_lora.ipynb`](smoll_json_lora.ipynb) | `HuggingFaceTB/SmolLM2-135M` + LoRA | Fine-tunes a LoRA adapter (r = 8, attention projections only) so the base model answers a question with a single `{"answer": "..."}` JSON object and then stops. Covers data splitting, prompt masking, EOS handling, training with 🤗 `Trainer`, base-vs-LoRA evaluation and optional debugging cells. |

## Setup

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/skamalj/llms-the-hard-way.git
cd llms-the-hard-way

uv sync
uv pip install peft datasets accelerate matplotlib   # used by the RoPE and LoRA notebooks

uv run jupyter lab
```

The models download from the Hugging Face Hub on first use. No GPU is needed. Setting `HF_TOKEN` is optional and only raises the download rate limit.

## The LoRA notebook

`smoll_json_lora.ipynb` is controlled by a single **run configuration** cell at the top:

| Setting | Purpose |
|---|---|
| `DATA_FILE` | Training data, as a JSON list of `{"prompt": "...", "answer": "..."}` records |
| `TRAIN_FRAC` / `VAL_FRAC` / `TEST_FRAC`, `SEED`, `DEDUPLICATE` | How the data is split |
| `RUN_TRAINING` | `False` skips training and evaluates the adapter already at `ADAPTER_PATH` |
| `ADAPTER_PATH` | Where the adapter is saved and loaded from |
| `RUN_DEBUG` | Turns the diagnostic cells at the end on or off |

The included dataset, [`data/lora_json_answer/smollm2_answer_250_fresh.json`](data/lora_json_answer/smollm2_answer_250_fresh.json), has 250 short technical Q&A pairs. Training for 10 epochs on its 200-record training split takes about 7 minutes on a CPU.

Not committed: the trained adapters (`smollm2-*-lora*/`) and the train/validation/test split files, which the notebook regenerates from `data/`.

## Tags

| Tag | Marks |
|---|---|
| `lora-json-answer-round3` | LoRA JSON-answer adapter, round 3 settings and results |
| `rope-walkthrough-v1` | RoPE walkthrough with a verified exact match against Hugging Face |
| `forward-pass-walkthrough-v1` | SmolLM2 forward pass by hand, ending in a KV-cache decode step |
