"""Averages the three labeller stances (cautious, pragmatic, neutral) into soft labels for each question, and reports
how much they agree. Also flags questions where one stance sharply disagrees with the other two (a sudden run of these
inside one case or a stretch of cases points to answers filed under the wrong id)."""
import collections
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STANCES = ("cautious", "pragmatic", "neutral")


def load(stance):
    rows = {}
    for half in (1, 2):
        for line in open(HERE / "labels" / f"labels_{stance}_{half}.jsonl", encoding="utf-8"):
            r = json.loads(line)
            rows[r["id"]] = r["answers"]
    return rows


cases = [json.loads(l) for l in open(HERE / "cases.jsonl", encoding="utf-8")]
labs = {s: load(s) for s in STANCES}
out, stats, sharp = [], collections.Counter(), []
per_case_sharp = collections.Counter()
for c in cases:
    soft = {}
    for q in c["questions"]:
        names = list(q["options"]) if q["type"] != "score" else [l["name"] for l in q["levels"]]
        dists = [labs[s][c["id"]][q["qid"]] for s in STANCES]
        for d in dists:
            assert list(d) == names, (c["id"], q["qid"], list(d), names)
        avg = {n: round(sum(d[n] for d in dists) / 3, 4) for n in names}
        soft[q["qid"]] = avg
        tops = [max(d, key=d.get) for d in dists]
        stats[("agree_all", q["type"])] += len(set(tops)) == 1
        stats[("n", q["type"])] += 1
        stats["max_avg_sum"] += max(avg.values())
        for i, s in enumerate(STANCES):           # sharp: this stance's top choice gets < 0.15 from both others
            others = [dists[j] for j in range(3) if j != i]
            if all(o[tops[i]] < 0.15 for o in others) and tops[i] != max(avg, key=avg.get):
                sharp.append((c["id"], q["qid"], s, tops[i], max(avg, key=avg.get)))
                per_case_sharp[c["id"]] += 1
    out.append({"id": c["id"], "soft_labels": soft})
with open(HERE / "soft_labels.jsonl", "w", encoding="utf-8") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
n = sum(stats[("n", t)] for t in ("yes_no", "choice", "score"))
print({"questions": n, "all three agree on the top answer": round(sum(stats[("agree_all", t)] for t in ("yes_no", "choice", "score")) / n, 3),
       **{f"agree_{t}": round(stats[("agree_all", t)] / stats[("n", t)], 3) for t in ("yes_no", "choice", "score")},
       "mean top probability of the average": round(stats["max_avg_sum"] / n, 3)})
print("sharp disagreements:", len(sharp), "| by stance:", collections.Counter(s for _, _, s, _, _ in sharp))
print("cases with 2+ sharp disagreements (check for misfiled answers):", sorted(k for k, v in per_case_sharp.items() if v >= 2))
for x in sharp[:15]:
    print("  ", x)
