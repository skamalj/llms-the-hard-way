"""Averages the three labellers (Opus 5.5 cautious, Sonnet 5.5 pragmatic, Fable 5.1 neutral; each a different model)
into soft labels for every v1 question, reports how much each pair of models agrees, and flags questions where one
labeller's top pick gets < 0.15 from both others (a run of these inside one case points to answers filed under the
wrong id). Inputs: labels/labels_<chunk>_<model>.jsonl for chunks G1..G8 and S01..S04. Output: soft_labels.jsonl."""
import collections
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODELS = ("opus", "sonnet", "fable")
CHUNKS = [f"G{k}" for k in range(1, 9)] + [f"S0{k}" for k in range(1, 5)]


def names(q):
    return [l["name"] for l in q["levels"]] if q["type"] == "score" else list(q["options"])


cases = {}
for f in ["cases_G.jsonl"] + [f"raw/gen_S0{k}.jsonl" for k in range(1, 5)]:
    for line in open(HERE / f, encoding="utf-8"):
        c = json.loads(line)
        cases[c["id"]] = c
labs = {m: {} for m in MODELS}
for m in MODELS:
    for ch in CHUNKS:
        for line in open(HERE / "labels" / f"labels_{ch}_{m}.jsonl", encoding="utf-8"):
            r = json.loads(line)
            labs[m][r["id"]] = r["answers"]
assert all(set(labs[m]) == set(cases) for m in MODELS), "a labeller file is missing cases"

out, agree, pair, sharp, per_case = [], collections.Counter(), collections.Counter(), [], collections.Counter()
tops = []
for cid, c in cases.items():
    soft = {}
    for q in c["questions"]:
        n = names(q)
        d = [labs[m][cid][q["qid"]] for m in MODELS]
        for x in d:
            assert list(x) == n, (cid, q["qid"], list(x), n)
        avg = {k: round(sum(x[k] for x in d) / 3, 4) for k in n}
        soft[q["qid"]] = avg
        t = [max(x, key=x.get) for x in d]
        agree[("n", q["type"])] += 1
        agree[("all", q["type"])] += len(set(t)) == 1
        for (i, a), (j, b) in itertools.combinations(enumerate(MODELS), 2):
            pair[(a, b)] += t[i] == t[j]
        tops.append(max(avg.values()))
        for i, m in enumerate(MODELS):
            if all(d[j][t[i]] < 0.15 for j in range(3) if j != i):
                sharp.append((cid, q["qid"], m))
                per_case[(cid, m)] += 1
    out.append({"id": cid, "soft_labels": soft})
with open(HERE / "soft_labels.jsonl", "w", encoding="utf-8") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
with open(HERE / "labels" / "sharp_disagreements.json", "w", encoding="utf-8") as f:
    json.dump([{"id": c, "qid": q, "outlier": m} for c, q, m in sharp], f, indent=1)
n = sum(agree[("n", t)] for t in ("yes_no", "choice", "score"))
print({"cases": len(cases), "questions": n,
       "all three agree on top": round(sum(agree[("all", t)] for t in ("yes_no", "choice", "score")) / n, 3),
       **{t: round(agree[("all", t)] / agree[("n", t)], 3) for t in ("yes_no", "choice", "score")},
       "mean top of average": round(sum(tops) / len(tops), 3)})
print("pairwise top agreement:", {f"{a}-{b}": round(v / n, 3) for (a, b), v in pair.items()})
print("sharp disagreements:", len(sharp), collections.Counter(m for _, _, m in sharp))
print("cases with 2+ sharp disagreements by one labeller (check for misfiling):",
      sorted(k for k, v in per_case.items() if v >= 2)[:30])
