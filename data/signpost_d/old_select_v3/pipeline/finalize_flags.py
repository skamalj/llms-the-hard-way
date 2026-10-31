#!/usr/bin/env python3
"""R28 follow-up: a few review flags contradict themselves (the reviewer's own note says there is no problem, e.g. "not one of
the excluded settings"). Move those to meta.v3_flags_withdrawn, so they do not drop good records, and recount stats.json.
Nothing else in the records changes; the raw reviews stay in qc/work/reviews/.

Usage: python finalize_flags.py [--dir ..]
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rejudge import shape  # noqa: E402

WITHDRAWN = re.compile(r"(not (one of )?(the |an )?excluded|no (exclusion|excluded setting) (applies|applied)|not covered by the excluded"
                       r"|so (this|it) is not (a problem|excluded)|but (more importantly )?it is fine|is not a problem|no problem"
                       r"|so the rule decides it|this is answerable)", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    a = ap.parse_args()
    path = os.path.join(a.dir, "selection_rejudged.jsonl")
    rows = [json.loads(x) for x in open(path, encoding="utf-8")]
    moved = 0
    for r in rows:
        m = r["meta"]
        allf = m.get("v3_flags", []) + m.get("v3_flags_withdrawn", [])
        keep = [f for f in allf if not WITHDRAWN.search(f["note"])]
        gone = [f for f in allf if WITHDRAWN.search(f["note"])]
        moved += len(gone)
        m["v3_flags"], m["v3_flags_withdrawn"] = keep, gone
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    st = json.load(open(os.path.join(a.dir, "stats.json")))
    codes = collections.Counter(f["code"] for r in rows for f in r["meta"]["v3_flags"])
    rec_codes = collections.Counter(c for r in rows for c in {f["code"] for f in r["meta"]["v3_flags"]})
    flagged = [r for r in rows if r["meta"]["v3_flags"]]
    st.update({"flagged_records": len(flagged), "unflagged_records": len(rows) - len(flagged), "flag_codes": dict(codes),
               "records_by_flag_code": dict(rec_codes), "flags_withdrawn": moved,
               "flags_on_whole_record": sum(f["question"] == "record" for r in rows for f in r["meta"]["v3_flags"]),
               "flags_on_a_question": sum(f["question"] != "record" for r in rows for f in r["meta"]["v3_flags"]),
               "unflagged_by_source": dict(collections.Counter(r["source"] for r in rows if not r["meta"]["v3_flags"])),
               "unflagged_questions": sum(len(r["questions"]) for r in rows if not r["meta"]["v3_flags"]),
               "new_gold_unflagged": shape([(q["type"], r["gold"][n]["probabilities"]) for r in rows if not r["meta"]["v3_flags"]
                                            for n, q in r["questions"].items()]),
               "old_gold_unflagged": shape([(q["type"], r["meta"]["old_gold"][n]["probabilities"]) for r in rows if not r["meta"]["v3_flags"]
                                            for n, q in r["questions"].items()])})
    json.dump(st, open(os.path.join(a.dir, "stats.json"), "w"), indent=2)
    print(json.dumps({k: st[k] for k in ("flagged_records", "unflagged_records", "unflagged_questions", "flag_codes", "records_by_flag_code", "flags_withdrawn")}))


if __name__ == "__main__":
    main()
