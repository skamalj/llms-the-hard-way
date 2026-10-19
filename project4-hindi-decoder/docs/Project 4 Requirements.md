# Project 4: Character Personality Classifier & Dialogue Style Transfer (Stitched Encoder-Decoder Architecture)

## 1. Project Overview
The objective of Project 4 is to build and train a custom **Stitched Encoder-Decoder Transformer** from scratch. The model takes a neutral English scenario combined with a cinematic persona tag and generates an iconic, stylized dialogue response in the voice of legendary characters from classic Indian cinema (Amitabh Bachchan personas across *Deewar*, *Don*, *Shahenshah*, *Amar Akbar Anthony*, *Agneepath*, and *Sholay*).

Rather than using a standard decoder-only prompt or training an entire architecture from scratch, this project implements **Cross-Attention Model Stitching**: a bidirectional encoder reads the input prompt, and an autoregressive decoder uses custom cross-attention layers to condition its generation on the encoder's representations.

---

## 2. System Architecture & Data Flow
* **Encoder Stack:** Reads the input text bidirectionally to extract semantic intent and persona constraints.
* **Projection Bridge ($nn.Linear$):** Maps the encoder's hidden dimensionality ($d_{\text{enc}}$) to match the decoder's hidden dimensionality ($d_{\text{dec}}$).
* **Cross-Attention Module ($nn.MultiheadAttention$):** Injected into the decoder layers where queries ($Q$) come from the decoder's hidden states, and keys/values ($K, V$) come from the projected encoder states.
* **Decoder Stack:** Generates the stylized target text autoregressively using causal self-attention and cross-attention conditioning.

---

## 3. Dataset Requirements
* **Total Samples:** ~360 structured training examples (~60 samples per persona).
* **Persona Distribution:**
  1. *Vijay (Deewar)* - The Angry Young Man / Moral Defiance
  2. *Don* - Cool, Calculated, and Uncatchable
  3. *Shahenshah* - Vigilante Justice & Authority
  4. *Anthony Gonsalves (Amar Akbar Anthony)* - Eccentric Bambaiya & Street Smart
  5. *Vijay Dinanath Chauhan (Agneepath)* - Gritty Crime Boss / Identity Declaration
  6. *Jai (Sholay)* - Fatalistic, Cynical, and Loyal Friend
* **Data Format Structure:**
  ```json
  {
    "input": "[Persona: <CHARACTER_TAG>] Scenario: <NEUTRAL_OR_ACTION_PROMPT>",
    "target": "<ICONIC_AMITABH_STYLE_RESPONSE>"
  }
  ```

---

## 4. Hardware Deployment Strategy (2x NVIDIA T4 GPUs)
Leveraging a dual-GPU 32GB VRAM setup via **Pipeline Parallelism / Device Splitting**:
* **GPU 0 (`cuda:0`):** Hosts the Bidirectional Encoder + Projection Bridge.
* **GPU 1 (`cuda:1`):** Hosts the Autoregressive Decoder (with LoRA adapters) + Custom Cross-Attention Layers.
* **Optimization Flags:** Mixed precision training (`FP16`), frozen encoder/base decoder weights, and active training restricted to the LoRA weights, cross-attention blocks, and projection layers.

---

## 5. Recommended Model Combinations (Dual-T4 Optimized)

### Option A: The Balanced Baseline (Fast & Lightweight)
* **Encoder:** `bert-base-uncased` (768 hidden dim) on `cuda:0`
* **Decoder:** `Qwen/Qwen2.5-0.5B` (896 hidden dim, LoRA-adapted) on `cuda:1`
* **Pros:** Extremely fast compilation, minimal VRAM usage (~4GB total per GPU), ideal for verifying cross-attention tensor mathematics and rapid iteration.

### Option B: The High-Fidelity Cinematic Upgrade (Recommended)
* **Encoder:** `microsoft/deberta-v3-base` or `answerdotai/ModernBERT-base` on `cuda:0`
* **Decoder:** `Qwen/Qwen2.5-1.5B-Instruct` (LoRA-adapted) on `cuda:1`
* **Pros:** DeBERTa provides superior syntactic token representation, while Qwen-1.5B delivers significantly sharper nuance, dramatic timing, and stylistic execution for movie dialogues. Fits comfortably within the 32GB dual-T4 budget when utilizing FP16.

---

## 6. Evaluation & Success Criteria
1. **Generalization Test:** Pass unseen, out-of-domain everyday inputs (e.g., *"I am going to eat fruit today"* or *"My Wi-Fi is disconnected"*) to verify that the model maps semantic concepts into distinct cinematic personas rather than memorizing exact training strings.
2. **Loss Convergence:** Monitor cross-entropy loss under teacher forcing to ensure the cross-attention bridge successfully aligns encoder memory tokens with decoder output logits.
