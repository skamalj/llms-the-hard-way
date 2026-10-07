"""Realistic multi-turn TRAINING conversations for modernbert.ipynb (Phase 6). Added to the generic template data.

Run from the repo root: python data/modernbert_router/build_realistic_train_data.py

The conversations are written free-form in realistic_train_parts/part*.py (40 businesses x 4 conversations, 5 agents
each), in the same format and with the same turn types as the realistic TEST set (build_realistic_test_data.py).
None of these businesses or agent names appear in any test set (E10 realistic, E11 first turn, banking, Cell 59).

Each user turn becomes one training record in the generic format:
  messages        every turn up to and including this user message (assistant replies in between)
  target_agent    the agent that should handle this message
  current_agent   the agent that answered the previous user message (None for the first message)
  context_change  None for the first message; False for handoff_ok ("ok" after being handed over) and when the
                  agent stays; True when the agent changes
  tags            [turn type, "realistic"]
"""
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "realistic_train"
TURN_TYPES = {"start", "answer", "follow", "aspect", "closing", "also_stay", "switch", "short_switch", "return",
              "handoff_ok", "branch"}
STOP = {"agent", "and", "the", "of", "&", "-"}


def load_part(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.COMPANIES, mod.CONVERSATIONS


def slug(company):
    return re.sub(r"[^a-z0-9]+", "_", company.lower()).strip("_")


def test_agent_names():
    """Agent names used by any test set or by the generic templates: none may be reused here."""
    names = {}
    for dom, info in json.load(open(HERE / "generic" / "domains.json")).items():
        names.update({a: f"generic/{dom}" for a in info["agents"]})
    for conv in json.load(open(HERE / "realistic" / "conversations.json")):
        names.update({a: "E10" for a in conv["agents"]})
    for agents in json.load(open(HERE / "first_turn" / "messages.json"))["companies"].values():
        names.update({a: "E11" for a in agents})
    for f in ["benchmark.json", "extended.json"]:
        names.update({ex["target_agent"]: "banking" for ex in json.load(open(HERE / "banking" / f))})
    nb = (HERE.parent.parent / "modernbert.ipynb")
    if nb.exists():                                  # Cell 59 agents are written inside the notebook
        names.update({a: "notebook" for a in re.findall(r'"([A-Z][A-Za-z&\- ]+ Agent)"', nb.read_text())})
    return names


companies, conversations = {}, []
for path in sorted((HERE / "realistic_train_parts").glob("part*.py")):
    comps, convs = load_part(path)
    assert not set(comps) & set(companies), f"{path.name}: company defined twice"
    companies.update(comps)
    conversations += convs

# ---- validation ----
taken = test_agent_names()
test_companies = ({c["company"] for c in json.load(open(HERE / "realistic" / "conversations.json"))}
                  | set(json.load(open(HERE / "first_turn" / "messages.json"))["companies"]))
assert not set(companies) & test_companies, set(companies) & test_companies
owner = {}
for company, agents in companies.items():
    assert len(agents) == 5, f"{company}: {len(agents)} agents (the router trains on 5 per domain)"
    for a in agents:
        assert a not in taken, f"{company}: '{a}' is already used by {taken[a]}"
        assert a not in owner, f"'{a}' used by both {owner[a]} and {company}"
        owner[a] = company
ids = Counter(cid for _, cid, _ in conversations)
assert all(n == 1 for n in ids.values()), [i for i, n in ids.items() if n > 1]

records, type_count = [], Counter()
switch_pairs = {c: Counter() for c in companies}
for company, cid, turns in conversations:
    assert company in companies, cid
    messages, prev = [], None
    for k, (user, agent, ttype, reply) in enumerate(turns):
        assert agent in companies[company], f"{cid}: unknown agent {agent}"
        assert ttype in TURN_TYPES, f"{cid}: unknown turn type {ttype}"
        assert (ttype == "start") == (k == 0), f"{cid} turn {k}: 'start' only on the first turn"
        if ttype in {"answer", "follow", "aspect", "closing", "also_stay"}:
            assert agent == prev, f"{cid} turn {k}: '{ttype}' must stay with {prev}"
        if ttype in {"switch", "short_switch", "return", "handoff_ok"}:
            assert agent != prev, f"{cid} turn {k}: '{ttype}' must change agent"
        messages.append({"role": "user", "content": user})
        records.append({"id": f"rt-{cid}-{k}", "domain": slug(company), "messages": list(messages),
                        "target_agent": agent, "current_agent": prev,
                        "context_change": None if prev is None else (agent != prev and ttype != "handoff_ok"),
                        "tags": [ttype, "realistic"]})
        type_count[ttype] += 1
        if prev and agent != prev:
            switch_pairs[company][frozenset((prev, agent))] += 1
        if k < len(turns) - 1:                       # a None reply is a turn the user ended without an answer
            messages.append({"role": "assistant", "content": reply or "You're welcome."})
        prev = agent
    assert len(messages) <= 15, cid

banking_names = ["payments agent", "card support", "investment agent", "insurance agent", "general customer support"]
leaks = [r["id"] for r in records if any(w in " ".join(m["content"].lower() for m in r["messages"]) for w in banking_names)]
assert not leaks, leaks

domains = {}
for company, agents in companies.items():
    pair = switch_pairs[company].most_common(1)
    close = sorted(pair[0][0]) if pair else list(agents)[:2]   # the two agents users move between most often
    keywords = {a: [w for w in re.findall(r"[a-z][a-z\-]+", a.lower()) if w not in STOP] for a in agents}
    domains[slug(company)] = {"close_pair": close, "agents": agents, "keywords": keywords}

OUT.mkdir(exist_ok=True)
json.dump(domains, open(OUT / "domains.json", "w"), indent=2, ensure_ascii=False)
json.dump(records, open(OUT / "conversations.json", "w"), indent=2, ensure_ascii=False)

cc = Counter(r["context_change"] for r in records)
print(f"{len(companies)} businesses, {len(conversations)} conversations -> {len(records)} training records")
print("turn types:", dict(type_count.most_common()))
print(f"context_change: None {cc[None]} | True {cc[True]} | False {cc[False]}")
print("wrote", OUT / "domains.json", "and", OUT / "conversations.json")
