"""Validator input for one score batch: each case with the three labellers' answers, their average (gold) and the
questions to look at closely (sharp disagreement, low agreement, or a labeller's note from notes_<batch>.json).
Usage: python prepare_validation.py L1"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODELS = ("opus", "sonnet", "fable")
batch = sys.argv[1]
labs = {m: {r["id"]: r["answers"] for r in map(json.loads, open(HERE / "labels" / f"labels_{batch}_{m}.jsonl", encoding="utf-8"))}
        for m in MODELS}
notes_file = HERE / "labels" / f"notes_{batch}.json"
notes = json.load(open(notes_file, encoding="utf-8")) if notes_file.exists() else {}
(HERE / "validation").mkdir(exist_ok=True)
n_look = 0
with open(HERE / "validation" / f"input_{batch}.jsonl", "w", encoding="utf-8") as out:
    for line in open(HERE / f"cases_{batch}.jsonl", encoding="utf-8"):
        c = json.loads(line)
        gold, look = {}, {}
        for qid, q in c["questions"].items():
            d = [labs[m][c["id"]][qid] for m in MODELS]
            avg = {k: round(sum(x[k] for x in d) / 3, 4) for k in d[0]}
            gold[qid] = {"type": q["type"], "probabilities": avg}
            why = []
            tops = [max(x, key=x.get) for x in d]
            for i, m in enumerate(MODELS):
                if all(d[j][tops[i]] < 0.15 for j in range(3) if j != i):
                    why.append(f"sharp disagreement: {m} differs from the other two")
            if max(avg.values()) < 0.55:
                why.append("low agreement: average top under 0.55")
            if f"{c['id']} {qid}" in notes:
                why.append("labeller note: " + notes[f"{c['id']} {qid}"])
            if why:
                look[qid] = "; ".join(why)
        n_look += len(look)
        out.write(json.dumps({"id": c["id"], "state": c["state"], "questions": c["questions"],
                              "labels": {m: labs[m][c["id"]] for m in MODELS}, "gold": gold, "look_closely": look},
                             ensure_ascii=False) + "\n")
print(batch, "questions to look at closely:", n_look)
