"""Splits the 1,200 v1 cases into 12 validator batches of 100 (V01..V12). Each line holds the case, every question's
three labels (opus, sonnet, fable) and their average, and a list of questions to look at closely: those a labeller
flagged (flagged_by_labellers.json), sharp disagreements (one labeller's top under 0.15 for both others) and low
agreement (average top under 0.55)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = HERE.parent
MODELS = ("opus", "sonnet", "fable")
CHUNKS = [f"G{k}" for k in range(1, 9)] + [f"S0{k}" for k in range(1, 5)]

cases = {}
for f in ["cases_G.jsonl"] + [f"raw/gen_S0{k}.jsonl" for k in range(1, 5)]:
    for line in open(V1 / f, encoding="utf-8"):
        c = json.loads(line)
        cases[c["id"]] = c
labs = {m: {} for m in MODELS}
for m in MODELS:
    for ch in CHUNKS:
        for line in open(V1 / "labels" / f"labels_{ch}_{m}.jsonl", encoding="utf-8"):
            r = json.loads(line)
            labs[m][r["id"]] = r["answers"]
soft = {r["id"]: r["soft_labels"] for r in map(json.loads, open(V1 / "soft_labels.jsonl", encoding="utf-8"))}
flags = json.load(open(HERE / "flagged_by_labellers.json", encoding="utf-8"))
sharp = {(s["id"], s["qid"]): s["outlier"]
         for s in json.load(open(V1 / "labels" / "sharp_disagreements.json", encoding="utf-8"))}

ids = sorted(cases)
look_total = 0
for b in range(12):
    with open(HERE / f"input_V{b + 1:02d}.jsonl", "w", encoding="utf-8") as out:
        for cid in ids[b * 100:(b + 1) * 100]:
            c = cases[cid]
            look = {}
            for q in c["questions"]:
                why = []
                key = f"{cid} {q['qid']}"
                if key in flags:
                    why.append("labeller note: " + flags[key])
                if (cid, q["qid"]) in sharp:
                    why.append(f"sharp disagreement: {sharp[(cid, q['qid'])]} differs from the other two")
                if max(soft[cid][q["qid"]].values()) < 0.55:
                    why.append("low agreement: average top under 0.55")
                if why:
                    look[q["qid"]] = "; ".join(why)
            look_total += len(look)
            out.write(json.dumps({**c, "labels": {m: labs[m][cid] for m in MODELS}, "average": soft[cid],
                                  "look_closely": look}, ensure_ascii=False) + "\n")
print("batches: 12 x 100, questions to look at closely:", look_total)
