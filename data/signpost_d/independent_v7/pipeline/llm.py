"""Model calls for the v7 (R26) pipeline: the Anthropic API through the Python SDK, billed to the key in ANTHROPIC_KEY
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


# ----------------------------------------------------------------------------- R26: Message Batches API and the budget cap

BATCH_DISCOUNT = 0.5  # the Batches API bills every token at half the standard rate
BUDGET_USD = float(os.environ.get("SIGNPOST_BUDGET_USD", "100"))


class BudgetStop(RuntimeError):
    pass


def spent() -> float:
    """Total cost so far in this run's ledger (every call, kept or not, including retries)."""
    if not LEDGER or not os.path.exists(LEDGER):
        return 0.0
    return sum(json.loads(x)["cost"] for x in open(LEDGER, encoding="utf-8") if x.strip())


def check_budget(estimate: float, what: str) -> None:
    s = spent()
    if s + estimate > BUDGET_USD:
        raise BudgetStop(f"budget cap: spent ${s:.2f}, {what} could cost up to ${estimate:.2f}, cap ${BUDGET_USD:.2f}")


def usage_cost(mid: str, u: dict, batch: bool) -> float:
    pin, pout = PRICES[mid]
    c = ((u.get("input") or 0) * pin + (u.get("output") or 0) * pout + (u.get("cache_read") or 0) * pin * 0.1
         + (u.get("cache_write") or 0) * pin * 1.25) / 1e6
    return c * (BATCH_DISCOUNT if batch else 1.0)


def batch_params(model: str, system, user: str, schema: dict, effort: str, max_tokens: int) -> dict:
    return {"model": MODELS[model], "max_tokens": max_tokens, "system": system,
            "messages": [{"role": "user", "content": user}],
            "output_config": {"effort": effort, "format": {"type": "json_schema", "schema": schema}}}


def run_batch(state_dir: str, name: str, items: list, estimate: float, poll_s: int = 30) -> dict:
    """items: [(custom_id, params, tag)]. Submits one Message Batch (or resumes the one recorded under state_dir/name),
    waits for it, logs every result's cost to the ledger at batch rates, and returns {custom_id: result}, where a result
    is {"ok": True, "data", "cost", "model", "usage"} or {"ok": False, "error"}. Results are saved, so a rerun reuses them."""
    os.makedirs(state_dir, exist_ok=True)
    meta_p = os.path.join(state_dir, f"{name}.json")
    res_p = os.path.join(state_dir, f"{name}_results.jsonl")
    if os.path.exists(res_p):
        return {r["custom_id"]: r["result"] for r in map(json.loads, open(res_p, encoding="utf-8"))}
    tags = {cid: tag for cid, _, tag in items}
    if os.environ.get("SIGNPOST_FAKE"):
        from fake import fake_call
        out = {}
        for cid, prm, tag in items:
            sys_text = prm["system"] if isinstance(prm["system"], str) else "\n".join(b["text"] for b in prm["system"])
            out[cid] = fake_call(prm["model"], sys_text, prm["messages"][0]["content"], prm["output_config"]["format"]["schema"], tag)
        _save_results(res_p, out)
        return out
    client = _get_client()
    if os.path.exists(meta_p):
        bid = json.load(open(meta_p))["batch_id"]
    else:
        check_budget(estimate, f"batch {name} ({len(items)} requests)")
        b = client.messages.batches.create(requests=[{"custom_id": cid, "params": prm} for cid, prm, _ in items])
        bid = b.id
        json.dump({"batch_id": bid, "requests": len(items), "estimate_usd": round(estimate, 2), "created": time.time()}, open(meta_p, "w"))
        print(f"batch {name}: {bid}, {len(items)} requests, estimate ${estimate:.2f}", flush=True)
    t0 = time.time()
    while True:
        b = client.messages.batches.retrieve(bid)
        if b.processing_status == "ended":
            break
        rc = b.request_counts
        print(f"batch {name}: {b.processing_status}, processing {rc.processing}, succeeded {rc.succeeded}, errored {rc.errored}, {int(time.time() - t0)}s", flush=True)
        time.sleep(poll_s)
    out = {}
    for r in client.messages.batches.results(bid):
        cid = r.custom_id
        if r.result.type != "succeeded":
            err = getattr(r.result, "error", None)
            out[cid] = {"ok": False, "error": f"{r.result.type}: {str(err)[:200]}"}
            continue
        msg = r.result.message
        u = msg.usage
        usage = {"input": u.input_tokens, "output": u.output_tokens, "cache_read": getattr(u, "cache_read_input_tokens", 0) or 0,
                 "cache_write": getattr(u, "cache_creation_input_tokens", 0) or 0}
        cost = usage_cost(msg.model if msg.model in PRICES else next(k for k in PRICES if k.startswith(msg.model)), usage, True)
        _log({"t": time.time(), "tag": tags.get(cid, cid), "model": msg.model, "usage": usage, "cost": round(cost, 6), "stop": msg.stop_reason, "batch": bid})
        if msg.stop_reason in ("refusal", "max_tokens"):
            out[cid] = {"ok": False, "error": msg.stop_reason, "cost": cost}
            continue
        text = next((blk.text for blk in msg.content if blk.type == "text"), None)
        try:
            out[cid] = {"ok": True, "data": json.loads(text), "cost": cost, "model": msg.model, "usage": usage}
        except (TypeError, json.JSONDecodeError) as e:
            out[cid] = {"ok": False, "error": f"bad JSON: {e}", "cost": cost}
    _save_results(res_p, out)
    return out


def _save_results(path: str, out: dict) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        for cid, r in out.items():
            fh.write(json.dumps({"custom_id": cid, "result": r}, ensure_ascii=False) + "\n")
