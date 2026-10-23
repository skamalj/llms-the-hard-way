---
license: gemma
language:
- en
base_model:
- google/gemma-3-4b-it
- answerdotai/ModernBERT-base
library_name: peft
pipeline_tag: text-generation
tags:
- style-transfer
- persona
- encoder-decoder
- prefix-tuning
- lora
- modernbert
- gemma3
---

# Thanos bridge (v1)

Rewrites an everyday English sentence as the **same message in a grave, formal, Thanos-inspired voice**.

| Input | Output (v1, greedy) |
|---|---|
| I worked all weekend to fix the bug, and nobody noticed. | All weekend I toiled to fix the bug, and no one noticed. |
| The project is three weeks late, but the client still wants it by Friday. | Three weeks the project has been delayed, yet the client still demands it by Friday. |
| I'm not angry that you lied; I'm disappointed that you thought you had to. | Your lie did not anger me. It was your belief in your own necessity that I find disappointing. |
| I'm really hungry. Let's get something to eat. | My hunger gnaws at me. Let us find something to eat. |
| I'm stuck in a meeting. I'll call you when I'm free. | I am trapped in a meeting. I shall call you when I am free. |

It is also an experiment in **stitching a bidirectional encoder to a decoder LLM**. The sentence reaches the decoder only as vectors, with no text prompt.

## How it works

```
"Thanos: <sentence>" → ModernBERT-base + LoRA → bridge (MLP 768 → 2560 → 2560, RMSNorm) → one vector per token
[<bos>] + those vectors → Gemma 3 4B IT (4-bit) + LoRA → the Thanos-voice sentence
```

The bridge turns each encoder token into a vector in Gemma's own input-embedding space. The vectors are placed after `<bos>` as a **prefix**, and Gemma reads them with its own attention.

Trained parameters:

| Part | Parameters |
|---|---|
| encoder LoRA | 3.4 M |
| bridge | 8.5 M |
| Gemma LoRA | 29.8 M |

The base models stay frozen.

## Usage

Requires a CUDA GPU, `torch`, `transformers==5.17.0`, `peft==0.21.2` and `bitsandbytes`. Gemma 3 is gated: accept its terms on the Hub and pass a token.

```python
import sys
from huggingface_hub import snapshot_download

path = snapshot_download("skamalj/thanos-bridge", revision="v1")
sys.path.insert(0, path)
from thanos_bridge import ThanosBridge

tb = ThanosBridge(path, hf_token="hf_...")
print(tb.translate("I'll be late to the office because of traffic."))
# -> Traffic shall keep me late to the office.
print(tb.sample("I'll be late to the office because of traffic.", n=5, temperature=0.9))
# varied renderings, e.g. "The office will not see me early. Traffic has forced me to delay my arrival."
```

`translate()` is greedy, so it gives the most likely and plainest rendering. `sample()` gives more varied and more dramatic renderings, with a higher risk of a fact slipping.

## Training

Two stages on Kaggle (2 × T4), from [`project4-hindi-decoder/10-prefix-bridge-split/`](https://github.com/skamalj/llms-the-hard-way/tree/hindi-decoder-compare/project4-hindi-decoder/10-prefix-bridge-split) (run R15 in the project ledger).

1. **Reconstruction** (encoder LoRA + bridge + Gemma LoRA): 12,000 English sentences, input `Plain: <sentence>`, target the same sentence. 1,500 steps of 8. This teaches the bridge to carry a sentence into Gemma intact: chrF **98.7** on 120 held-out sentences.
2. **Thanos voice:** Gemma's LoRA is **reset to zero**, then trained alone, with the encoder and bridge frozen, on 1,157 pairs (`thanos_v8`: everyday and serious English sentences, each rewritten in one consistent dramatic voice). Early stopping on a held-out everyday set kept epoch 1.

**Data:**
- **Stage 1:** the English side of Hinglish-TOP (Apache-2.0) and PHINC (CC BY 4.0).
- **Stage 2:** written for this project, partly by the author and partly with LLM assistance, every target checked for facts. See [`data/thanos_v8/`](https://github.com/skamalj/llms-the-hard-way/tree/hindi-decoder-compare/project4-hindi-decoder/data/thanos_v8).

## Evaluation

chrF against one reference rewrite. There are many good Thanos versions of a sentence, so this mostly measures closeness to one author's wording; read the examples too.

| Set | chrF |
|---|---|
| Everyday held-out (24) | 48.3 |
| Test (25) | 56.1 |
| Earlier interpretive set (25), reference | 36.2 |

Every output stopped properly, and all outputs were distinct.

## Limitations

- **Facts can slip:** "My brother **borrowed** my car" came out as "My brother **stole** my car". Numbers and names are usually kept, but not always. Check outputs where facts matter.
- **Occasional odd word order:** "Ten minutes late I run."
- **The greedy output is often plainer than the training data;** `sample()` shows more of the style.
- English only. One or two sentences in, one or two out. Not a chat model.
- A Thanos-*inspired* register for fun and for research on encoder–decoder stitching. Not affiliated with or endorsed by Marvel or Disney.

## License

The adapters are derived from Gemma 3 and are distributed under the [Gemma Terms of Use](https://ai.google.dev/gemma/terms). ModernBERT-base is Apache-2.0.

## Versions

- **v1** (this tag): run R15, the more dramatic voice.
- Later versions will be added as tags on this repo.
