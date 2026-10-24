"""Assembles the Signpost-D pilot: the six generators' batches (raw/gen_A..F.jsonl, 50 cases each, written by Opus 5.5
subagents from ../brief.md) into cases.jsonl, with form labels normalised. No answers yet: labels come from three
independent labeller stances (labeller_instructions.md)."""
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FORMS = {"form": "form or checklist", "email or message thread": "message thread", "email": "message thread"}

cases = []
for b in "ABCDEF":
    for line in open(HERE / "raw" / f"gen_{b}.jsonl", encoding="utf-8"):
        c = json.loads(line)
        c["form"] = FORMS.get(c["form"], c["form"])
        cases.append(c)
assert len({c["id"] for c in cases}) == len(cases) == 300
with open(HERE / "cases.jsonl", "w", encoding="utf-8") as out:
    for c in cases:
        out.write(json.dumps(c, ensure_ascii=False) + "\n")
qs = [q for c in cases for q in c["questions"]]
print({"cases": len(cases), "questions": len(qs)}, collections.Counter(c["form"] for c in cases),
      collections.Counter(q["type"] for q in qs), collections.Counter(q["kind"] for q in qs))
