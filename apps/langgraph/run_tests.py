"""Run the app's tests and write a report to reports/.

    uv run python run_tests.py                  # all tests, agents answer with Claude
    uv run python run_tests.py --router-only    # agents reply with a stub (no Claude calls); routing is the same
    uv run python run_tests.py --only A,B       # a subset: A first messages, B conversations, C persistence, D reducer
    uv run python run_tests.py --cleanup        # delete the test threads from DynamoDB afterwards

A  first messages: a new thread each
B  conversations: Signpost routes live from the real history and the current agent
C  persistence: half a conversation, then a NEW checkpointer and graph continue the thread from DynamoDB
D  reducer: a long conversation with a small window, so routing works from a pruned history
"""
import argparse
import json
import statistics
import time
from pathlib import Path

from graph import build_checkpointer, build_graph, send, stored_messages
from router import SignpostRouter
from scenarios import (CONVERSATIONS, FIRST_MESSAGES, LONG_CONVERSATION, PERSIST_CONVERSATION, PERSIST_SPLIT,
                       REDUCER_WINDOW)
from settings import AGENT_MODEL, MAX_MESSAGES, MIN_MESSAGES, TABLE_NAME

ROWS = []


def turn(graph, test, thread, i, text, expected, kind):
    before = graph.get_state({"configurable": {"thread_id": thread}})
    current_before = (before.values or {}).get("current_agent") if before else None
    out = send(graph, thread, text)
    r = out["route"]
    row = {"test": test, "thread": thread, "turn": i, "type": kind, "message": text, "expected": expected,
           "picked": r["agent"], "p": round(r["p"], 3), "ok": r["agent"] == expected, "current_before": current_before,
           "messages_seen": r["messages_seen"], "stored_after": stored_messages(graph, thread), "ms": round(r["ms"]),
           "reply": out["messages"][-1].content}
    ROWS.append(row)
    flag = "  " if row["ok"] else " x"
    print(f"  [{test}] {i:>2} {kind:12s} | {text[:58]:58s} -> {r['agent'].replace(' Agent', ''):20s} p {r['p']:.2f}{flag} "
          f"| saw {r['messages_seen']:>2}, stored {row['stored_after']:>2} | {r['ms']:.0f} ms")
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--router-only", action="store_true")
    ap.add_argument("--only", default="A,B,C,D")
    ap.add_argument("--cleanup", action="store_true")
    args = ap.parse_args()
    tests = set(args.only.split(","))
    stamp = time.strftime("%Y%m%d-%H%M%S")
    call_llm = not args.router_only

    print(f"loading Signpost ...", flush=True)
    router = SignpostRouter()
    print(f"Signpost loaded in {router.load_seconds:.1f}s | agents: {AGENT_MODEL if call_llm else 'stub replies'} | "
          f"DynamoDB table {TABLE_NAME} | reducer window {MAX_MESSAGES}/{MIN_MESSAGES}")
    saver = build_checkpointer()
    graph = build_graph(router, saver, call_llm)
    threads = []

    if "A" in tests:
        print("\nA. first messages (a new thread each)")
        for i, (text, expected, kind) in enumerate(FIRST_MESSAGES, 1):
            tid = f"test-{stamp}-A{i:02d}"
            threads.append(tid)
            turn(graph, "A", tid, 1, text, expected, kind)

    if "B" in tests:
        print("\nB. conversations (routed live)")
        for name, turns in CONVERSATIONS.items():
            tid = f"test-{stamp}-B-{name}"
            threads.append(tid)
            for i, (text, expected, kind) in enumerate(turns, 1):
                turn(graph, "B", tid, i, text, expected, kind)

    if "C" in tests:
        print(f"\nC. persistence: {PERSIST_SPLIT} turns, then a new checkpointer and graph continue from DynamoDB")
        tid = f"test-{stamp}-C"
        threads.append(tid)
        turns = CONVERSATIONS[PERSIST_CONVERSATION]
        for i, (text, expected, kind) in enumerate(turns[:PERSIST_SPLIT], 1):
            turn(graph, "C", tid, i, text, expected, kind)
        fresh = build_graph(router, build_checkpointer(), call_llm)          # nothing shared in memory
        snap = fresh.get_state({"configurable": {"thread_id": tid}}).values
        restored = {"messages": len(snap.get("messages", [])), "current_agent": snap.get("current_agent")}
        print(f"  restored from DynamoDB by a new checkpointer: {restored}")
        ROWS.append({"test": "C-restore", "thread": tid, **restored,
                     "ok": restored["messages"] == 2 * PERSIST_SPLIT and restored["current_agent"] == turns[PERSIST_SPLIT - 1][1]})
        for i, (text, expected, kind) in enumerate(turns[PERSIST_SPLIT:], PERSIST_SPLIT + 1):
            turn(fresh, "C", tid, i, text, expected, kind)

    if "D" in tests:
        mx, mn = REDUCER_WINDOW
        print(f"\nD. reducer: prune above {mx} messages down to {mn}; routing from the pruned history")
        small = build_graph(router, build_checkpointer(mx, mn), call_llm)
        tid = f"test-{stamp}-D"
        threads.append(tid)
        for i, (text, expected, kind) in enumerate(LONG_CONVERSATION, 1):
            turn(small, "D", tid, i, text, expected, kind)

    # ---- summary and report
    routed = [r for r in ROWS if "picked" in r]
    print("\nSUMMARY")
    lines = [f"# Signpost in LangGraph: test report ({stamp})", "",
             f"- Agents: {AGENT_MODEL if call_llm else 'stub replies (router-only)'}; Signpost on CPU (load {router.load_seconds:.1f}s)",
             f"- Checkpointer: DynamoDB `{TABLE_NAME}` + agentstate-reducer (window {MAX_MESSAGES}/{MIN_MESSAGES}; test D {REDUCER_WINDOW[0]}/{REDUCER_WINDOW[1]})", "",
             "| Test | Correct | Routing ms p50 / p95 |", "|---|---|---|"]
    for t in ["A", "B", "C", "D"]:
        rr = [r for r in routed if r["test"] == t]
        if rr:
            ms = sorted(r["ms"] for r in rr)
            s = f"{sum(r['ok'] for r in rr)} / {len(rr)}"
            p50, p95 = ms[len(ms) // 2], ms[min(len(ms) - 1, int(0.95 * len(ms)))]
            print(f"  {t}: {s} correct | routing p50 {p50} ms, p95 {p95} ms")
            lines.append(f"| {t} | {s} | {p50} / {p95} |")
    restore = [r for r in ROWS if r["test"] == "C-restore"]
    if restore:
        print(f"  C restore from DynamoDB: {'OK' if restore[0]['ok'] else 'FAILED'} ({restore[0]['messages']} messages, current agent {restore[0]['current_agent']})")
        lines += ["", f"Persistence: a new checkpointer restored {restore[0]['messages']} messages and current agent "
                      f"`{restore[0]['current_agent']}` from DynamoDB: **{'OK' if restore[0]['ok'] else 'FAILED'}**"]
    d = [r for r in routed if r["test"] == "D"]
    if d:
        print(f"  D stored messages per turn: {[r['stored_after'] for r in d]} (window {REDUCER_WINDOW})")
        lines += ["", f"Reducer (test D): messages stored after each turn: {[r['stored_after'] for r in d]}"]
    lines += ["", "| Test | Thread | Turn | Type | Message | Expected | Picked | p | OK | Current before | Seen | Stored | ms | Reply |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in routed:
        reply = r["reply"].replace("\n", " ").replace("|", "/")[:160]
        lines.append(f"| {r['test']} | {r['thread'].split('-', 3)[-1]} | {r['turn']} | {r['type']} | {r['message']} | {r['expected']} | "
                     f"{r['picked']} | {r['p']} | {'✓' if r['ok'] else '✗'} | {r['current_before'] or '—'} | {r['messages_seen']} | "
                     f"{r['stored_after']} | {r['ms']} | {reply} |")
    out_dir = Path(__file__).resolve().parent / "reports"
    out_dir.mkdir(exist_ok=True)
    (out_dir / f"report_{stamp}.md").write_text("\n".join(lines), encoding="utf-8")
    (out_dir / f"report_{stamp}.json").write_text(json.dumps(ROWS, indent=1), encoding="utf-8")
    print(f"\nreport: reports/report_{stamp}.md (+ .json)")

    if args.cleanup:
        for tid in threads:
            saver.delete({"configurable": {"thread_id": tid}})
        print(f"deleted {len(threads)} test threads from DynamoDB")


if __name__ == "__main__":
    main()
