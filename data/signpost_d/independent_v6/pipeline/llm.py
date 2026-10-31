"""Model calls for the v6 pipeline: the Anthropic API through the Python SDK, billed to the key in ANTHROPIC_KEY
(or ANTHROPIC_API_KEY). Every call returns JSON that matches a schema (structured outputs, output_config.format).

SIGNPOST_FAKE=1 swaps in a deterministic offline stand-in (fake.py) so the pipeline can be tested without a key.
"""
from __future__ import annotations

import json
import os
import threading
import time

MODELS = {"opus": "claude-opus-5-5", "sonnet": "claude-sonnet-5-5", "haiku": "claude-haiku-5-5"}
# USD per million tokens (input, output), first-party API rates
PRICES = {"claude-opus-5-5": (4.0, 20.0), "claude-sonnet-5-5": (2.0, 10.0), "claude-haiku-5-5": (0.10, 0.50)}

_client = None
_lock = threading.Lock()
LEDGER = os.environ.get("SIGNPOST_LEDGER", "")


def _get_client():
    global _client
    if _client is None:
        import anthropic
        key = os.environ.get("ANTHROPIC_KEY") or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError("no API key: set ANTHROPIC_KEY (or ANTHROPIC_API_KEY)")
        # base_url is pinned so a host-managed ANTHROPIC_BASE_URL can never route these calls elsewhere
        _client = anthropic.Anthropic(api_key=key, base_url="https://api.anthropic.com", max_retries=6, timeout=600)
    return _client


def _log(entry: dict) -> None:
    if not LEDGER:
        return
    with _lock:
        with open(LEDGER, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")


def call(model: str, system: str, user: str, schema: dict, effort: str = "medium", max_tokens: int = 16000, tag: str = "") -> dict:
    """One structured call. Returns {"ok", "data", "cost", "model", "usage"} or {"ok": False, "error"}."""
    if os.environ.get("SIGNPOST_FAKE"):
        from fake import fake_call
        return fake_call(model, system, user, schema, tag)
    import anthropic
    mid = MODELS[model]
    client = _get_client()
    last = None
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=mid, max_tokens=max_tokens, system=system,
                messages=[{"role": "user", "content": user}],
                output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}},
            )
            u = resp.usage
            pin, pout = PRICES[mid]
            cost = ((u.input_tokens or 0) * pin + (u.output_tokens or 0) * pout
                    + (getattr(u, "cache_read_input_tokens", 0) or 0) * pin * 0.1
                    + (getattr(u, "cache_creation_input_tokens", 0) or 0) * pin * 1.25) / 1e6
            usage = {"input": u.input_tokens, "output": u.output_tokens}
            _log({"t": time.time(), "tag": tag, "model": mid, "usage": usage, "cost": round(cost, 6), "stop": resp.stop_reason})
            if resp.stop_reason == "refusal":
                last = f"refusal: {getattr(resp, 'stop_details', None)}"
                continue
            if resp.stop_reason == "max_tokens":
                last = "max_tokens"
                max_tokens = min(64000, max_tokens * 2)
                continue
            text = next((b.text for b in resp.content if b.type == "text"), None)
            if text is None:
                last = "no text block"
                continue
            return {"ok": True, "data": json.loads(text), "cost": cost, "model": mid, "usage": usage}
        except (anthropic.BadRequestError, anthropic.AuthenticationError, anthropic.PermissionDeniedError, anthropic.NotFoundError) as e:
            return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:300]}", "model": mid}
        except (anthropic.RateLimitError, anthropic.APIStatusError, anthropic.APIConnectionError) as e:
            last = f"{type(e).__name__}: {str(e)[:200]}"
            time.sleep(10 * (attempt + 1))
        except json.JSONDecodeError as e:
            last = f"bad JSON: {e}"
    return {"ok": False, "error": last, "model": mid}
