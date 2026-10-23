"""Builds thanos_v8: thanos_v7 with ONE dramatic voice throughout.

v7 mixed voices (older v3/v4 light rewording, the strict handwritten h001-h200, and the user's everyday grand style).
Here every target except the lines from the user's own file of 75 (d75_*, same author as the user's bar) is rewritten
to the user's bar (raw/pass2_brief.md):
  "We're throwing Tom a farewell dinner on Friday, but he doesn't know yet."
  -> "We shall gather on Friday to honor Tom with a farewell feast… yet he remains unaware of what awaits him."
Three rewriter subagents (raw/pass2_out_*.jsonl) and three validator subagents (raw/pass2_verdicts_*.jsonl: pass, or
fix for facts and/or drama with a corrected target), then my review (REVIEW). A first, milder rewrite was rejected.
Inputs are unchanged. Covers the 1,088 non-d75 training targets and the 25 test targets. validation.jsonl (curated
interpretive set, a reference only) and validation_daily.jsonl (the user's everyday held-out set) are unchanged.
Each rewritten row keeps its v7 target as previous_target."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
V7 = HERE.parent / "thanos_v7"
REVIEW = {}
BANNED = re.compile(r"\b(inevitab\w*|destiny|universe|balance\w*|equilibrium|snap|infinity|stones)\b", re.I)


def load(path):
    return [json.loads(line) for line in open(path, encoding="utf-8")]


new_target = {}
for k in (1, 2, 3):
    rows = {r["id"]: r for r in load(HERE / "raw" / f"pass2_out_{k}.jsonl")}
    for v in load(HERE / "raw" / f"pass2_verdicts_{k}.jsonl"):
        new_target[v["id"]] = v["fixed_target"] if v["verdict"] == "fix" else rows[v["id"]]["target"]
new_target.update(REVIEW)

splits = {s: load(V7 / f"{s}.jsonl") for s in ("train", "validation", "test", "validation_daily")}
used = set()
for s, key in (("train", lambda r: r["id"]), ("test", lambda r: "test_" + r["id"])):
    for r in splits[s]:
        k = key(r)
        if k in new_target:
            r.update(previous_target=r["target"], target=new_target[k], references=[new_target[k]])
            r["origin"] = r.get("origin", "thanos_v3") + "+dramatic"
            used.add(k)
        else:
            assert r["id"].startswith("d75_"), ("not rewritten", r["id"])
assert used == set(new_target), "a rewritten id was not found"
for r in splits["train"] + splits["test"]:
    assert r["source"] != r["target"] and not re.search(r"\d", r["target"]) and not BANNED.search(r["target"]), r["id"]

manifest = json.load(open(V7 / "manifest.json"))
manifest.update(dataset="thanos_v8", files={})
for s, rows in splits.items():
    with open(HERE / f"{s}.jsonl", "w", encoding="utf-8") as out:
        for r in rows:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
    manifest["files"][s] = len(rows)
json.dump(manifest, open(HERE / "manifest.json", "w"), ensure_ascii=False, indent=1)
print(manifest["files"], "rewritten:", len(used))
