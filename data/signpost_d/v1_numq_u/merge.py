"""Final v1_numq_u: the code-built questions (systemone.jsonl, heldout.jsonl), filtered for the builder's known faults,
with the reworded wording (reword/reworded_R*.jsonl) where it passes the checks below; otherwise the code wording stays.

Filters (from the rewording reports):
- dates and date "extreme" questions whose field is not a single plain date (a range such as "2026-08-01 to 2026-08-15");
- ratio and difference questions whose two values are more than 10x apart (unrelated amounts, money against a rate);
- any question on a value that looks like a year (a whole number 1900-2100);
- questions on identifier fields: the whole key is a word such as req, lot, store, invoice, period, grade, day;
- percentage, accuracy or rate limits above 100, and age limits above 120;
- "extreme" questions over records with differing units, or whose labels are phrases rather than names or codes.
Checks on a rewrite: same type; choice labels identical; same number of score levels; every limit number of the original
instruction kept (numbers that were only part of a field key may change form); no backtick, underscore, "[" or dotted
path; no deciding value quoted; a noul instruction stays a statement. Writes systemone_final.jsonl and
heldout_final.jsonl; usage: merge.py"""
import collections
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAIN_DATE = re.compile(r"^(\d{4}-\d{2}-\d{2}([ T]\d{2}:\d{2}(:\d{2})?)?|\d{1,2} [A-Za-z]{3,9}\.? \d{4}|[A-Za-z]{3,9}\.? \d{1,2},? \d{4})$")
IDENT = re.compile(r"(?i)(_station$|^(req|requisition|lot|store|invoice|period|built|installed|station|asset|batch|order|ticket|"
                   r"case|shift|bay|gate|dock|aisle|zone|level|week|month|day|quarter|grade|class|tier|version|room|"
                   r"unit|flat|house|plot|seat|row|table|lane|route|bus|flight|ward|bed)(_no|_number|_id)?$)")   # the whole key
RATEY = re.compile(r"(?i)(pct|percent|accuracy|rate|ratio|share|score|utili[sz]ation|occupancy|completion)")
NUM = re.compile(r"(?<![\w.])-?\d[\d,]*(\.\d+)?")


def resolve(state, path):
    x = state
    for name, idx in re.findall(r"([^.\[\]]+)|\[(\d+)\]", path):
        if idx:
            x = x[int(idx)]
        else:
            x = x[name]
    return x


def numbers(text):
    return {m.group(0).replace(",", "") for m in NUM.finditer(text)}


def bad(case, qid):
    """Why a code-built question must go, or None."""
    info = case["meta"]["numq"][qid]
    t, keys = info["template"], [p.split(".")[-1].split("]")[-1] for p in info["paths"]]
    raws = [resolve(case["state"], p) for p in info["paths"]]
    if t == "dates" or (t == "extreme" and all(isinstance(r, str) for r in raws)):
        if not all(isinstance(r, str) and PLAIN_DATE.match(r.strip()) for r in raws):
            return "date field is not a single plain date"
    nums = [r for r in raws if isinstance(r, (int, float)) and not isinstance(r, bool)]
    if any(isinstance(r, int) and 1900 <= r <= 2100 for r in nums):
        return "value looks like a year"
    if t != "extreme" and any(IDENT.search(k) for k in keys):
        return "identifier field"
    if t in ("ratio", "difference") and len(nums) == 2 and max(nums) > 10 * min(nums):
        return "values more than 10x apart"
    if t in ("threshold", "twohop") and info["margin"]:
        limit = nums[0] / info["margin"]
        if RATEY.search(keys[0]) and limit > 100:
            return "percentage-like limit above 100"
        if re.search(r"(?i)(^|_)age($|_)", keys[0]) and limit > 120:
            return "age limit above 120"
    if t == "extreme":
        q = case["questions"][qid]
        if any(len(lab) > 30 or len(lab.split()) > 4 for lab in q["criteria"]):
            return "labels are phrases"
        list_path = re.sub(r"\[\d+\]\.[^.\[\]]+$", "", info["paths"][0])
        recs = resolve(case["state"], list_path)
        units = {r.get("unit") for r in recs if isinstance(r, dict) and "unit" in r}
        if len(units) > 1:
            return "records in different units"
    return None


def accept(orig, new, info, label_keys):
    """Why a rewrite is refused, or None."""
    if new.get("type") != orig["type"] or set(new) != {"type", "instructions", "criteria"}:
        return "fields or type changed"
    if orig["type"] == "choice" and list(new["criteria"]) != list(orig["criteria"]):
        return "choice labels changed"
    if orig["type"] == "score" and len(new["criteria"]) != len(orig["criteria"]):
        return "score level count changed"
    if orig["type"] == "noul" and (set(new["criteria"]) != {"true", "false"} or new["instructions"].rstrip().endswith("?")):
        return "noul form"
    text = new["instructions"] + " " + json.dumps(new["criteria"], ensure_ascii=False)
    if "`" in text or "_" in new["instructions"] or "[" in new["instructions"] or re.search(r"\w\.[a-z]\w*\.", new["instructions"]):
        return "path-like text"
    key_nums = set().union(*[numbers(re.sub(r"[_.]", " ", p)) for p in info["paths"]]) if info["paths"] else set()
    missing = numbers(orig["instructions"]) - numbers(new["instructions"]) - key_nums
    if missing:
        return f"limit numbers missing: {sorted(missing)}"
    if info["template"] != "extreme":
        for v in info["values"]:
            if re.fullmatch(r"-?\d+(\.\d+)?", v) and v.rstrip("0").rstrip(".") not in label_keys:
                vv = v[:-2] if v.endswith(".0") else v
                if vv in numbers(new["instructions"]) and vv not in numbers(orig["instructions"]):
                    return f"quotes the deciding value {vv}"
    return None


rewrites = {}
for f in sorted((HERE / "reword").glob("reworded_R*.jsonl")):
    for line in open(f, encoding="utf-8"):
        r = json.loads(line)
        rewrites[r["id"]] = r["questions"]
stats = collections.Counter()
for src, dst in (("systemone.jsonl", "systemone_final.jsonl"), ("heldout.jsonl", "heldout_final.jsonl")):
    out = []
    for line in open(HERE / src, encoding="utf-8"):
        c = json.loads(line)
        for qid in list(c["questions"]):
            why = bad(c, qid)
            if why:
                stats[f"dropped: {why}"] += 1
                for k in ("questions", "gold"):
                    c[k].pop(qid)
                c["meta"]["numq"].pop(qid); c["meta"]["kinds"].pop(qid)
                continue
            new = rewrites.get(c["id"], {}).get(qid)
            if new is None:
                stats["code wording (not reworded)"] += 1
                c["meta"]["numq"][qid]["wording"] = "code"
                continue
            refuse = accept(c["questions"][qid], new, c["meta"]["numq"][qid], set(c["questions"][qid]["criteria"]) if c["questions"][qid]["type"] == "choice" else set())
            if refuse:
                stats[f"rewrite refused: {refuse.split(':')[0]}"] += 1
                c["meta"]["numq"][qid]["wording"] = "code"
                continue
            c["questions"][qid] = new
            c["meta"]["numq"][qid]["wording"] = "reworded"
            stats["reworded"] += 1
        if c["questions"]:
            out.append(c)
        else:
            stats["cases emptied"] += 1
        stats[f"{dst} questions"] += len(c["questions"])
    with open(HERE / dst, "w", encoding="utf-8") as fh:
        for c in out:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    stats[f"{dst} cases"] = len(out)
print(json.dumps(dict(sorted(stats.items())), indent=1))
