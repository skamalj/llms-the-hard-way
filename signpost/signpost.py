"""Signpost: routes a conversation to the right agent, and answers grounded choice questions about a text.

Fine-tuned from answerdotai/ModernBERT-large (Apache 2.0): LoRA adapters (merged into the weights at export) + a small
scoring head. One forward pass per option; a softmax over the options' scores gives the answer.

    from signpost import Signpost
    sp = Signpost("path/to/signpost")                     # the exported folder (encoder/, head.pt, signpost_config.json)
    agent, probs = sp.route(messages, agents, current_agent=None)
    p_yes = sp.yes_no("Help! My payouts have failed for 3 days!", "Does this convey urgency?")
    pick, probs = sp.choice(text, "Which team should handle this?", ["billing", "sales", "retail"])
    level, expected, probs = sp.score(text, "How frustrated is the writer?", ["calm", "frustrated", "furious"])

`messages` is a list of {"role": "user" | "assistant", "content": str}, oldest first, ending with the user's latest message.
`agents` maps agent name -> one-sentence description. `current_agent` is the agent that answered the previous turn (or None).
"""
import json
from pathlib import Path

import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer

ROUTE_Q = "Which agent should handle the user's latest message?"


class Signpost:
    def __init__(self, path, device=None, dtype=None):
        path = Path(path)
        self.cfg = json.load(open(path / "signpost_config.json"))
        self.device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
        dtype = dtype or (torch.float16 if self.device.type == "cuda" else torch.float32)
        self.tok = AutoTokenizer.from_pretrained(path / "encoder")
        self.tok.padding_side, self.tok.truncation_side = "right", "left"      # if too long, the oldest history is cut
        self.enc = AutoModel.from_pretrained(path / "encoder", dtype=dtype).to(self.device).eval()
        head = torch.load(path / "head.pt", map_location="cpu")
        self.head = nn.Sequential(nn.Dropout(0.1), nn.Linear(head["hidden"], 256), nn.GELU(), nn.Dropout(0.1), nn.Linear(256, 1))
        self.head.load_state_dict(head["state_dict"])
        self.head.to(self.device).eval()

    def _text(self, messages, current, question, name, description):
        """Exactly the training format: messages SEP current agent SEP question SEP candidate."""
        sep = self.cfg["sep"]
        parts = [f"{m['role']}: {m['content']}" for m in messages]
        parts += [f"current agent: {current or 'none'}", f"question: {question}",
                  f"candidate: {name}. {description}" if description else f"candidate: {name}"]
        return self.cfg["prefix"] + sep.join(parts)

    @torch.no_grad()
    def probs(self, messages, options, question=ROUTE_Q, current=None):
        """options: {name: description} or a list of names -> {name: probability}, in the given order."""
        opts = options if isinstance(options, dict) else {o: "" for o in options}
        texts = [self._text(messages, current, question, n, d) for n, d in opts.items()]
        enc = self.tok(texts, padding=True, truncation=True, max_length=self.cfg["max_len"], return_tensors="pt").to(self.device)
        hidden = self.enc(input_ids=enc["input_ids"], attention_mask=enc["attention_mask"]).last_hidden_state
        m = enc["attention_mask"].unsqueeze(-1).float()
        scores = self.head((hidden.float() * m).sum(1) / m.sum(1)).squeeze(-1)
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
