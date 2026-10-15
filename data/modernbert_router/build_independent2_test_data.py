"""Second independent test set (run 27): written by a subagent that saw none of our data or code, only a neutral brief
(formats, rules, a list of businesses to avoid, a self-check). Its raw files are kept as delivered in independent2/raw/;
this converts them to the format the notebooks read, and re-checks them.

    independent2/raw/questions.jsonl   200 questions: 50 yes_no, 50 choice, 50 score (levels low -> high), 50 many_choice (10-50 options)
    independent2/raw/first_turn.jsonl  50 first messages, 8-15 agents each
    independent2/raw/routing.jsonl     conversations with 8-15 agents, 4-7 user turns each

    python build_independent2_test_data.py   -> independent2/{questions,first_turn,routing}.json
"""
import collections
import json
from pathlib import Path

HERE = Path(__file__).parent / "independent2"
RAW = HERE / "raw"
STAY, SWITCH = {"answer", "follow", "aspect", "closing", "also_stay"}, {"switch", "short_switch", "return"}
TYPE = {"yes_no": "noul", "choice": "choice", "score": "score", "many_choice": "many_choice"}


def load(name):
    return [json.loads(line) for line in open(RAW / name, encoding="utf-8") if line.strip()]


def build():
    questions, first, routing = load("questions.jsonl"), load("first_turn.jsonl"), load("routing.jsonl")

    items = []
    for q in questions:
        assert q["answer"] in q["options"] and len(set(q["options"])) == len(q["options"]), q["id"]
        items.append({"id": q["id"], "type": TYPE[q["type"]], "state": q["text"], "question": q["question"],
                      "options": q["options"], "answer": q["answer"], "answer_index": q["options"].index(q["answer"])})

    messages = []
    for f in first:
        assert f["expected_agent"] in f["agents"], f["id"]
        messages.append({"id": f["id"], "company": f["company"], "agents": f["agents"], "message": f["message"],
                         "target_agent": f["expected_agent"], "type": f["kind"], "n_agents": len(f["agents"])})

    convs = []
    for r in routing:
        msgs, user_turns, prev = [], [], None
        for t in r["turns"]:
            assert t["expected_agent"] in r["agents"], (r["id"], t["user"])
            if prev and t["turn_type"] in STAY:
                assert t["expected_agent"] == prev, (r["id"], t["user"])
            if prev and t["turn_type"] in SWITCH:
                assert t["expected_agent"] != prev, (r["id"], t["user"])
            msgs.append({"role": "user", "content": t["user"]})
            user_turns.append({"message_index": len(msgs) - 1, "expected_agent": t["expected_agent"], "turn_type": t["turn_type"]})
            if t.get("assistant"):
                msgs.append({"role": "assistant", "content": t["assistant"]})
            prev = t["expected_agent"]
        convs.append({"id": r["id"], "company": r["company"], "agents": r["agents"], "messages": msgs,
                      "user_turns": user_turns, "n_agents": len(r["agents"])})

    json.dump({"items": items}, open(HERE / "questions.json", "w"), indent=1)
    json.dump({"messages": messages}, open(HERE / "first_turn.json", "w"), indent=1)
    json.dump(convs, open(HERE / "routing.json", "w"), indent=1)
    types = collections.Counter(it["type"] for it in items)
    print(f"questions {len(items)} {dict(types)} | first messages {len(messages)} "
          f"({len({m['company'] for m in messages})} businesses) | conversations {len(convs)} / "
          f"{sum(len(c['user_turns']) for c in convs)} turns ({len({c['company'] for c in convs})} businesses)")


if __name__ == "__main__":
    build()
