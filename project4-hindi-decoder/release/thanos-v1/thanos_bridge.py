"""Thanos bridge v1: everyday English -> the same message in a grave, Thanos-inspired voice.

ModernBERT-base (+ LoRA) reads the sentence; a small MLP bridge turns each encoder token into a vector in Gemma 3 4B IT's
input-embedding space; those vectors are placed after <bos> as a prefix, and Gemma (4-bit, + LoRA) writes the reply.
There is no text prompt: the sentence reaches Gemma only through the bridge.

    from thanos_bridge import ThanosBridge
    tb = ThanosBridge("path/to/thanos-v1", hf_token="hf_...")      # Gemma 3 is gated: accept its terms on the Hub first
    tb.translate("I'll be late to the office because of traffic.")
    tb.sample("I'll be late to the office because of traffic.", n=5, temperature=0.9)

Requires a CUDA GPU (Gemma is loaded in 4-bit with bitsandbytes), torch, transformers 5.17.0, peft 0.21.2, bitsandbytes.
This file reproduces the training notebook (project4-hindi-decoder/10-prefix-bridge-split/, run R15) exactly.
"""
from pathlib import Path

import torch
import torch.nn as nn
from peft import PeftModel
from transformers import AutoConfig, AutoModel, AutoTokenizer, BitsAndBytesConfig, Gemma3ForConditionalGeneration

ENCODER, ENCODER_REVISION = "answerdotai/ModernBERT-base", "8949b909ec900327062f0ebf497f51aef5e6f0c8"
DECODER, DECODER_REVISION = "google/gemma-3-4b-it", "093f9f388b31de276ce2de164bdc2081324b9767"
PERSONA = "Thanos"
DTYPE = torch.float32


class Bridge(nn.Module):
    """Encoder states -> vectors in Gemma's input-embedding space: a 2-layer MLP, then RMSNorm at the embeddings' scale."""

    def __init__(self, d_in, d_out):
        super().__init__()
        self.mlp = nn.Sequential(nn.Linear(d_in, d_out), nn.GELU(), nn.Linear(d_out, d_out))
        self.norm = nn.RMSNorm(d_out)

    def forward(self, h):
        return self.norm(self.mlp(h))


class ThanosBridge:
    def __init__(self, path, hf_token=None, enc_device="cuda:0", dec_device=None, max_new_tokens=64):
        if not torch.cuda.is_available():
            raise RuntimeError("a CUDA GPU is required: Gemma is loaded in 4-bit with bitsandbytes")
        path = Path(path)
        self.enc_device = torch.device(enc_device)
        self.dec_device = torch.device(dec_device or enc_device)
        self.max_new_tokens = max_new_tokens

        self.enc_tok = AutoTokenizer.from_pretrained(ENCODER, revision=ENCODER_REVISION)
        cfg = AutoConfig.from_pretrained(ENCODER, revision=ENCODER_REVISION)
        if hasattr(cfg, "reference_compile"):
            cfg.reference_compile = False
        encoder = AutoModel.from_pretrained(ENCODER, revision=ENCODER_REVISION, config=cfg, dtype=DTYPE,
                                            attn_implementation="sdpa").to(self.enc_device)
        self.encoder = PeftModel.from_pretrained(encoder, path / "encoder-lora").eval()

        self.dec_tok = AutoTokenizer.from_pretrained(DECODER, revision=DECODER_REVISION, token=hf_token)
        quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=DTYPE)
        decoder = Gemma3ForConditionalGeneration.from_pretrained(
            DECODER, revision=DECODER_REVISION, dtype=DTYPE, token=hf_token, quantization_config=quant,
            device_map={"": self.dec_device.index or 0}, attn_implementation="eager")
        self.start = self.dec_tok.bos_token_id
        eos = decoder.generation_config.eos_token_id
        self.stops = sorted(set((eos if isinstance(eos, list) else [eos]) + [self.dec_tok.convert_tokens_to_ids("<end_of_turn>")]))
        self.pad = self.dec_tok.pad_token_id
        self.decoder = PeftModel.from_pretrained(decoder, path / "decoder-lora").eval()

        saved = torch.load(path / "bridge.pt", map_location="cpu", weights_only=True)
        self.bridge = Bridge(encoder.config.hidden_size, decoder.config.text_config.hidden_size)
        self.bridge.load_state_dict(saved["bridge"])
        self.bridge.to(self.enc_device).eval()

        # Gemma's generate() cannot start from embeddings: pass <bos> + placeholder tokens and swap the placeholders'
        # embeddings for the prefix on the first (full-prompt) forward pass.
        self.placeholder = self.dec_tok(" .", add_special_tokens=False)["input_ids"][-1]
        self._pending = None
        self.decoder.get_input_embeddings().register_forward_hook(self._write_prefix)

    def _write_prefix(self, module, args, output):
        if self._pending is not None and output.dim() == 3 and output.shape[1] == 1 + len(self._pending):
            output = output.clone()
            output[:, 1:] = self._pending.to(output.dtype)
            self._pending = None
        return output

    @torch.no_grad()
    def _prefix(self, sentence):
        t = self.enc_tok([f"{PERSONA}: {sentence}"], truncation=True, max_length=128, return_tensors="pt").to(self.enc_device)
        h = self.encoder(input_ids=t["input_ids"], attention_mask=t["attention_mask"]).last_hidden_state
        return self.bridge(h)[0].to(self.dec_device)

    @torch.no_grad()
    def _generate(self, sentence, **sampling):
        p = self._prefix(sentence)
        ids = torch.tensor([[self.start] + [self.placeholder] * len(p)], device=self.dec_device)
        self._pending = p
        try:
            out = self.decoder.generate(input_ids=ids, attention_mask=torch.ones_like(ids),
                                        max_new_tokens=self.max_new_tokens, eos_token_id=self.stops,
                                        pad_token_id=self.pad, **sampling)
        finally:
            written, self._pending = self._pending is None, None
        assert written, "the prefix was not written into the prompt"
        return self.dec_tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True).strip()

    def translate(self, sentence):
        """The single most likely rendering (greedy)."""
        return self._generate(sentence, do_sample=False, num_beams=1, temperature=None, top_p=None, top_k=None)

    def sample(self, sentence, n=5, temperature=0.9, top_p=0.95):
        """n sampled renderings: more varied and dramatic, with a higher risk of a fact slipping."""
        return [self._generate(sentence, do_sample=True, temperature=temperature, top_p=top_p) for _ in range(n)]
