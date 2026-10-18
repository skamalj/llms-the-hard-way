"""Many-option training questions (exp/listwise-index) from hand-written texts: many_train_texts_*.py.

Every text is written individually (no sentence templates). Each text is used for several questions with different option
lists, so the model sees the same reading problem with 2 to 50 options. Options besides the ones named in the text come
from the same topic's TRAIN pool (many_options_pools.py), so they are always the same kind of thing as the answer.

Checks: the answer and every value named in the text belong to the TRAIN pool; the answer appears in the text (except for
numbers and teams, where it is worked out or routed); no text repeats.

    python build_many_options_train_data.py     -> many_train/items.json
"""
import importlib
import json
import math
import random
from pathlib import Path

from many_options_pools import TRAIN

HERE = Path(__file__).parent
OUT = HERE / "many_train"
TARGET = 2500                      # questions in total
SEED = 7
INFERRED = {"number", "team"}       # answers that may be worked out rather than quoted


def load_texts():
    items = []
    for part in sorted(HERE.glob("many_train_texts_*.py")):
        items += importlib.import_module(part.stem).ITEMS
    return items


def validate(texts):
    seen = set()
    for topic, text, question, answer, others in texts:
        pool = TRAIN[topic]
        assert answer in pool, (topic, answer, text)
        assert all(o in pool for o in others), (topic, others, text)
        assert answer not in others, (text,)
        if topic not in INFERRED:
            assert answer.lower() in text.lower(), ("answer not in text", text, answer)
        assert text not in seen, ("repeated text", text)
        seen.add(text)


def build():
    texts = load_texts()
    validate(texts)
    rng = random.Random(SEED)
    per_text = math.ceil(TARGET / len(texts))
    items = []
    for k, (topic, text, question, answer, others) in enumerate(texts):
        pool = TRAIN[topic]
        named = [answer] + list(others)
        for copy in range(per_text):
            n = rng.randint(max(2, len(named)), min(50, len(pool)))         # 2..50 options, capped by the pool
            options = named + rng.sample([v for v in pool if v not in named], n - len(named))
            rng.shuffle(options)
            items.append({"id": f"mt{k:04d}-{copy}", "domain": f"many/{topic}", "type": "choice", "category": f"many_{topic}",
                          "state": text, "question": question, "options": options, "answer": answer})
    rng.shuffle(items)
    items = items[:TARGET]
    OUT.mkdir(exist_ok=True)
    json.dump({"items": items}, open(OUT / "items.json", "w"), indent=1)
    sizes = [len(it["options"]) for it in items]
    by_topic = {}
    for t in texts:
        by_topic[t[0]] = by_topic.get(t[0], 0) + 1
    print(f"{len(texts)} hand-written texts {by_topic} -> {len(items)} questions | options {min(sizes)}-{max(sizes)} "
          f"(mean {sum(sizes) / len(sizes):.1f})")


if __name__ == "__main__":
    build()
