"""Many-option TEST questions (exp/listwise-index) from hand-written texts: many_test_texts.py.

Values come only from the TEST pools, which share no value with the training pools (numbers aside). Departments resemble the
training "teams" family in kind, but every name differs. Each text is one question, with 10, 15, 20, 30, 40 or 50 options
(cycled; capped by the pool size). Guards: answers and named values belong to the TEST pool; answers appear in the text
(except numbers, worked out, and departments, routed); no 5-word sequence is shared with any training text.

    python build_many_options_test_data.py     -> many_test/questions.json
"""
import json
import random
from pathlib import Path

from many_options_pools import TEST
from many_test_texts import ITEMS
import build_many_options_train_data as train

OUT = Path(__file__).parent / "many_test"
SEED = 11
BUCKETS = [10, 15, 20, 30, 40, 50]
INFERRED = {"number", "department"}


def ngrams(text, n=5):
    w = text.lower().replace(",", " ").replace(".", " ").replace(";", " ").replace(":", " ").split()
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def build():
    rng = random.Random(SEED)
    train_texts = [t[1] for t in train.load_texts()]
    train_grams = set().union(*(ngrams(t) for t in train_texts))
    items, seen = [], set()
    for k, (topic, text, question, answer, others) in enumerate(ITEMS):
        pool = TEST[topic]
        assert answer in pool and all(o in pool for o in others) and answer not in others, (topic, text)
        if topic not in INFERRED:
            assert answer.lower() in text.lower(), ("answer not in text", text)
        assert text not in seen and not ngrams(text) & train_grams, ("repeated, or shares a 5-word sequence with training", text)
        seen.add(text)
        named = [answer] + list(others)
        n = min(BUCKETS[k % len(BUCKETS)], len(pool))
        options = named + rng.sample([v for v in pool if v not in named], n - len(named))
        rng.shuffle(options)
        items.append({"id": f"mq{k:03d}", "family": topic, "type": "choice", "state": text, "question": question,
                      "options": options, "answer": answer, "n_options": len(options)})
    OUT.mkdir(exist_ok=True)
    json.dump({"items": items}, open(OUT / "questions.json", "w"), indent=1)
    counts = {}
    for it in items:
        counts[it["n_options"]] = counts.get(it["n_options"], 0) + 1
    print(f"{len(items)} hand-written many-option test questions | {len({it['family'] for it in items})} topics | "
          f"option counts {dict(sorted(counts.items()))} | guard: no shared value, no shared 5-word sequence with training")


if __name__ == "__main__":
    build()
