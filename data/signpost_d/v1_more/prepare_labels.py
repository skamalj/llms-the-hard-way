"""Labeller input for one batch: each case's id, state and questions only (no kinds, features or notes).
Usage: python prepare_labels.py M08"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
batch = sys.argv[1]
n = 0
with open(HERE / "labels" / f"input_{batch}.jsonl", "w", encoding="utf-8") as out:
    for line in open(HERE / f"cases_{batch}.jsonl", encoding="utf-8"):
        c = json.loads(line)
        out.write(json.dumps({"id": c["id"], "state": c["state"], "questions": c["questions"]}, ensure_ascii=False) + "\n")
        n += 1
print(batch, n, "cases")
