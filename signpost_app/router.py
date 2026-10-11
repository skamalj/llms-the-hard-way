"""Signpost as a router: loads the exported model folder and picks the agent for the latest user message."""
import importlib.util
import os
import time

import torch
from langchain_core.messages import AIMessage, HumanMessage

from settings import SIGNPOST_PATH


def _load_signpost_class(path):
    """Import Signpost from the exported folder's own signpost.py, so the app uses exactly the exported code."""
    spec = importlib.util.spec_from_file_location("signpost_model", path / "signpost.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Signpost


def message_text(m):
    """The plain text of a LangChain message (content is a string, or a list of content blocks)."""
    if isinstance(m.content, str):
        return m.content
    return " ".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in m.content)


def to_signpost_messages(messages):
    """LangChain messages -> Signpost's format: [{"role": "user" | "assistant", "content": str}], oldest first."""
    roles = {HumanMessage: "user", AIMessage: "assistant"}
    return [{"role": roles[type(m)], "content": message_text(m)} for m in messages if type(m) in roles]


class SignpostRouter:
    def __init__(self, path=SIGNPOST_PATH):
        torch.set_num_threads(os.cpu_count() or 4)
        t0 = time.perf_counter()
        self.model = _load_signpost_class(path)(path)          # CPU -> float32
        self.load_seconds = time.perf_counter() - t0

    def route(self, messages, agents, current_agent=None):
        """-> (agent, {agent: probability}, milliseconds, number of messages Signpost saw)."""
        history = to_signpost_messages(messages)
        t0 = time.perf_counter()
        agent, probs = self.model.route(history, agents, current_agent)
        return agent, probs, (time.perf_counter() - t0) * 1000, len(history)
