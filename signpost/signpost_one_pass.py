"""Signpost one-pass: routes a conversation to the right agent, and answers grounded choice questions about a text,
reading every option in ONE encoder pass.

Fine-tuned from answerdotai/ModernBERT-large (Apache 2.0): LoRA adapters (merged into the weights at export) + a small
scoring head. All options go into one input; each option is scored from the mean of its own tokens by the shared head,
and a softmax over the options gives the answer.

    from signpost_one_pass import SignpostOnePass
    sp = SignpostOnePass("path/to/signpost-one-pass")     # the saved folder (encoder/, head.pt, signpost_config.json)
    agent, probs = sp.route(messages, agents, current_agent=None)
    p_yes = sp.yes_no("Help! My payouts have failed for 3 days!", "Does this convey urgency?")
    pick, probs = sp.choice(text, "Which team should handle this?", ["billing", "sales", "retail"])
    level, expected, probs = sp.score(text, "How frustrated is the writer?", ["calm", "frustrated", "furious"])

`messages` is a list of {"role": "user" | "assistant", "content": str}, oldest first, ending with the user's latest message.
`agents` maps agent name -> one-sentence description. `current_agent` is the agent that answered the previous turn (or None).
Up to `max_options` options (50); if the input is longer than `max_len` tokens, the oldest messages are dropped, never an option.
"""
import json
from pathlib import Path

import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer


class ScoreHead(nn.Module):
    """Signpost's scoring head (Dropout, Linear(H, 256), GELU, Dropout, Linear(256, 1)) with `extra` residual blocks of 256
    units between its two layers. Each block's last layer starts at zero, so a head loaded from Signpost starts out exactly as
    published, and the blocks then learn on top of it."""

    def __init__(self, hidden, extra=0):
        super().__init__()
        self.inp = nn.Sequential(nn.Dropout(0.1), nn.Linear(hidden, 256), nn.GELU())
        self.blocks = nn.ModuleList([nn.Sequential(nn.Dropout(0.1), nn.Linear(256, 256), nn.GELU(), nn.Linear(256, 256))
                                     for _ in range(extra)])
        for b in self.blocks:
            nn.init.zeros_(b[3].weight); nn.init.zeros_(b[3].bias)
        self.out = nn.Sequential(nn.Dropout(0.1), nn.Linear(256, 1))

    def forward(self, x):
        h = self.inp(x)
        for b in self.blocks:
            h = h + b(h)
        return self.out(h)

    def load_published(self, sd):
        """Signpost's head (a plain Sequential: layers 1 and 4) into this head."""
        self.inp[1].load_state_dict({"weight": sd["1.weight"], "bias": sd["1.bias"]})
        self.out[1].load_state_dict({"weight": sd["4.weight"], "bias": sd["4.bias"]})

ROUTE_Q = "Which agent should handle the user's latest message?"


class SignpostOnePass:
    def __init__(self, path, device=None, dtype=None):
        path = Path(path)
        self.cfg = json.load(open(path / "signpost_config.json"))
        assert self.cfg.get("format") == "one-pass", "this folder is not a one-pass Signpost (use signpost.py)"
        self.device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
        dtype = dtype or (torch.float16 if self.device.type == "cuda" else torch.float32)
        self.tok = AutoTokenizer.from_pretrained(path / "encoder")
        self.enc = AutoModel.from_pretrained(path / "encoder", dtype=dtype).to(self.device).eval()
        head = torch.load(path / "head.pt", map_location="cpu")
        if "extra_blocks" in head:                                       # ScoreHead layout (Signpost-D run 7 onwards)
            self.head = ScoreHead(head["hidden"], head["extra_blocks"])
        else:
            self.head = nn.Sequential(nn.Dropout(0.1), nn.Linear(head["hidden"], 256), nn.GELU(), nn.Dropout(0.1), nn.Linear(256, 1))
        self.head.load_state_dict(head["state_dict"])
        self.head.to(self.device).eval()

    def _text(self, messages, current, question, options, drop=0):
        """Exactly the training format: messages SEP current agent SEP question SEP option: A SEP option: B ...
        -> (text, character span of each option)."""
        sep = self.cfg["sep"]
        text = sep.join([f"{m['role']}: {m['content']}" for m in messages[drop:]]
                        + [f"current agent: {current or 'none'}", f"question: {question}"])
        spans = []
        for name, desc in options.items():
            seg = f"{name}. {desc}" if desc else name
            text += sep + "option: "
            spans.append((len(text), len(text) + len(seg)))
            text += seg
        return text, spans

    def _fit(self, messages, current, question, options):
        """Drop the oldest messages until the input fits max_len; the latest message and every option always stay."""
        assert len(options) <= self.cfg["max_options"], f"{len(options)} options > max_options={self.cfg['max_options']}"
        for drop in range(len(messages)):
            text, spans = self._text(messages, current, question, options, drop)
            if len(self.tok(text)["input_ids"]) <= self.cfg["max_len"]:
                return text, spans
        raise ValueError(f"{len(options)} options don't fit in max_len={self.cfg['max_len']}, even with only the latest message")

    @torch.no_grad()
    def probs(self, messages, options, question=ROUTE_Q, current=None):
        """options: {name: description} or a list of names -> {name: probability}, in the given order."""
        opts = options if isinstance(options, dict) else {o: "" for o in options}
        text, spans = self._fit(messages, current, question, opts)
        enc = self.tok(text, return_offsets_mapping=True, return_tensors="pt")
        offsets = enc.pop("offset_mapping")[0]                                   # [T, 2] characters of each token
        hidden = self.enc(input_ids=enc["input_ids"].to(self.device),
                          attention_mask=enc["attention_mask"].to(self.device)).last_hidden_state[0].float()   # [T, H]
        s, e = offsets[:, 0], offsets[:, 1]
        sp = torch.tensor(spans)                                                 # [K, 2]
        member = ((e > s) & (s < sp[:, 1:]) & (e > sp[:, :1])).float().to(self.device)   # [K, T]: the tokens of each option
        pooled = (member @ hidden) / member.sum(-1, keepdim=True)                # [K, H]: mean of each option's tokens
        scores = self.head(pooled).squeeze(-1)
        return dict(zip(opts, torch.softmax(scores, dim=0).tolist()))

    def route(self, messages, agents, current_agent=None):
        """-> (chosen agent, {agent: probability})."""
        p = self.probs(messages, agents, ROUTE_Q, current_agent)
        return max(p, key=p.get), p

    def yes_no(self, text, question):
        """-> P(yes)."""
        return self.probs([{"role": "user", "content": text}], ["yes", "no"], question)["yes"]

    def choice(self, text, question, options):
        """-> (chosen option, {option: probability})."""
        p = self.probs([{"role": "user", "content": text}], options, question)
        return max(p, key=p.get), p

    def score(self, text, question, levels):
        """levels ordered low -> high -> (most likely level, expected level index, {level: probability})."""
        p = self.probs([{"role": "user", "content": text}], levels, question)
        expected = sum(i * p[l] for i, l in enumerate(levels))
        return max(p, key=p.get), expected, p
