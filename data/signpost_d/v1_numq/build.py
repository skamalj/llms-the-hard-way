"""Number questions built by code from the JSON states of v1_4's training cases (no model writes anything): thresholds,
two-field comparisons, the highest entry in a list of records, date order and day gaps, and a size band. Each gold
is computed from the data and softened as a clear-cut label (about 0.95 on the right answer). New case ids start with "N";
they are training only (a notebook must keep them out of dev, as the twins). Writes systemone.jsonl here; usage: build.py"""
import collections
import datetime as dt
import json
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "v1_4" / "systemone.jsonl"
SEED, DEV_FRACTION, PER_CASE = 42, 0.15, 3
SKIP = re.compile(r"(?i)(^|_)(id|ids|ref|refs|code|codes|no|number|phone|zip|postcode|sku|year|version|seq|index|rank)$")
DATE = re.compile(r"^(\d{4}-\d{2}-\d{2})")
ID_KEYS = ("id", "ref", "name", "code", "sku", "item", "supplier", "applicant", "candidate", "product", "vendor", "title")
rnd = random.Random(7)


def dev_split(ids):
    ids = sorted(ids)
    random.Random(SEED).shuffle(ids)
    return set(ids[: int(len(ids) * DEV_FRACTION)])


def path_str(p):
    out = ""
    for k in p:
        out += f"[{k}]" if isinstance(k, int) else (f".{k}" if out else str(k))
    return out


def fields(x, p=()):
    """Leaf (path, value) pairs: numbers (not bools) and ISO dates."""
    if isinstance(x, dict):
        for k, v in x.items():
            yield from fields(v, p + (k,))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from fields(v, p + (i,))
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        if p and isinstance(p[-1], str) and not SKIP.search(p[-1]) and abs(x) < 1e9:
            yield p, x
    elif isinstance(x, str) and DATE.match(x):
        yield p, dt.date.fromisoformat(DATE.match(x).group(1))


def record_lists(x, p=()):
    """Lists of 3-6 records that share an identifier key and a numeric key."""
    if isinstance(x, dict):
        for k, v in x.items():
            yield from record_lists(v, p + (k,))
    elif isinstance(x, list):
        if 3 <= len(x) <= 6 and all(isinstance(r, dict) for r in x):
            idk = next((k for k in x[0] if any(t in k.lower() for t in ID_KEYS) and all(isinstance(r.get(k), str) for r in x)), None)
            if idk and len({r[idk] for r in x}) == len(x):
                for k, v in x[0].items():
                    if k != idk and not SKIP.search(k) and all(isinstance(r.get(k), (int, float)) and not isinstance(r.get(k), bool) for r in x):
                        vals = [r[k] for r in x]
                        if len(set(vals)) == len(vals):
                            yield p, idk, k, x
        for i, v in enumerate(x):
            yield from record_lists(v, p + (i,))


def nice(v):
    """A round number near v (never equal to v)."""
    if abs(v) >= 100:
        r = round(v, -1 if abs(v) < 1000 else -2)
    elif abs(v) >= 10:
        r = round(v)
    else:
        r = round(v, 1)
    return r if r != v else r + (1 if abs(v) >= 10 else 0.1)


def fmt(v):
    return f"{v:g}" if isinstance(v, float) else str(v)


def noul(statement, true_desc, false_desc, truth):
    g = 0.95 if truth else 0.05
    return ({"type": "noul", "instructions": statement, "criteria": {"true": true_desc, "false": false_desc}},
            {"type": "noul", "probabilities": {"true": g, "false": round(1 - g, 2)}})


def q_threshold(nums):
    p, v = rnd.choice(nums)
    x = nice(v * rnd.choice([rnd.uniform(0.6, 0.9), rnd.uniform(1.1, 1.5)]))
    if x == v:
        return None
    s = path_str(p)
    return noul(f"The value of `{s}` is more than {fmt(x)}.", f"`{s}` is above {fmt(x)}", f"`{s}` is {fmt(x)} or less", v > x)


MONEY = {"net", "vat", "tax", "total", "subtotal", "amount", "fee", "fees", "cost", "price", "charge", "deposit", "freight", "discount"}


def unit(key):
    """A field's unit: its last '_' token if it names one (gbp, kg, hours, …), 'money' for plain money words."""
    if not isinstance(key, str):
        return None
    last = key.lower().split("_")[-1]
    if last in {"gbp", "usd", "eur", "inr", "aud", "kg", "g", "litres", "liters", "hours", "hrs", "days", "minutes", "mins",
                "units", "pcs", "m", "km", "m2", "sqm", "seats", "people", "guests", "pallets", "cases", "boxes", "pct"}:
        return last
    return "money" if key.lower() in MONEY else None


def q_pair(nums):
    """Two comparable values: sibling fields in the same unit, or the same field in two entries of a list."""
    groups = collections.defaultdict(list)
    for p, v in nums:
        if unit(p[-1]):
            groups[("unit", p[:-1], unit(p[-1]))].append((p, v))
        idx = [i for i, k in enumerate(p) if isinstance(k, int)]
        if idx:                                              # the same key path with the list index masked
            i = idx[-1]
            groups[("list", p[:i], p[i + 1:])].append((p, v))
    groups = [g for g in groups.values() if len(g) >= 2]
    if not groups:
        return None
    (pa, a), (pb, b) = rnd.sample(rnd.choice(groups), 2)
    sa, sb = path_str(pa), path_str(pb)
    if a == b:
        return None
    return noul(f"`{sa}` is greater than `{sb}`.", f"`{sa}` is the larger of the two", f"`{sb}` is at least as large", a > b)


def q_dates(dates):
    if len(dates) < 2:
        return None
    (pa, a), (pb, b) = rnd.sample(dates, 2)
    if a == b:
        return None
    sa, sb = path_str(pa), path_str(pb)
    if rnd.random() < 0.5:
        return noul(f"The date in `{sa}` is earlier than the date in `{sb}`.", f"`{sa}` comes first",
                    f"`{sa}` is the same day or later", a < b)
    lo, hi = (pa, a), (pb, b)
    if a > b:
        lo, hi = hi, lo
    gap = (hi[1] - lo[1]).days
    n = max(1, round(gap * rnd.choice([rnd.uniform(0.6, 0.9), rnd.uniform(1.1, 1.5)])))
    if n == gap:
        return None
    sl, sh = path_str(lo[0]), path_str(hi[0])
    return noul(f"The date in `{sh}` is more than {n} days after the date in `{sl}`.",
                f"The gap is more than {n} days", f"The gap is {n} days or less", gap > n)


def q_max(lists):
    if not lists:
        return None
    p, idk, k, recs = rnd.choice(lists)
    vals = [r[k] for r in recs]
    top = recs[vals.index(max(vals))][idk]
    crit = {r[idk]: f"The entry whose {idk} is {r[idk]}" for r in recs}
    probs = {r[idk]: (0.94 if r[idk] == top else round(0.06 / (len(recs) - 1), 4)) for r in recs}
    return ({"type": "choice", "instructions": f"In `{path_str(p)}`, which entry has the highest `{k}`?", "criteria": crit},
            {"type": "choice", "probabilities": probs})


def q_band(nums):
    p, v = rnd.choice([(p, v) for p, v in nums if abs(v) >= 4] or [(None, None)])
    if p is None:
        return None
    s = path_str(p)
    level = rnd.randrange(4)                                    # the band v falls in, chosen first
    width = max(abs(v) * rnd.uniform(0.15, 0.35), 1)
    lo = v - width * (level + rnd.uniform(0.25, 0.75))           # v sits strictly inside its band
    cuts = [nice(lo + width * (i + 1)) for i in range(3)]
    if len(set(cuts)) < 3 or v in cuts or sum(v >= c for c in cuts) != level:
        return None
    crit = [f"Under {fmt(cuts[0])}: `{s}` is below {fmt(cuts[0])}",
            f"{fmt(cuts[0])} to under {fmt(cuts[1])}: `{s}` is at least {fmt(cuts[0])} and below {fmt(cuts[1])}",
            f"{fmt(cuts[1])} to under {fmt(cuts[2])}: `{s}` is at least {fmt(cuts[1])} and below {fmt(cuts[2])}",
            f"{fmt(cuts[2])} or more: `{s}` is {fmt(cuts[2])} or above"]
    probs = {str(i): (0.94 if i == level else 0.03 if abs(i - level) == 1 else 0.0) for i in range(4)}
    rest = round(1 - sum(probs.values()), 4)
    probs[str(level)] = round(probs[str(level)] + rest, 4)
    return ({"type": "score", "instructions": f"How large is the value of `{s}`?", "criteria": crit},
            {"type": "score", "probabilities": probs})


cases = [json.loads(l) for l in open(SRC, encoding="utf-8")]
dev = dev_split(c["id"] for c in cases if not c["id"].startswith(("I", "K", "L", "T")))
for g in ("I", "K", "L"):
    dev |= dev_split(c["id"] for c in cases if c["id"].startswith(g))
out, kinds = [], collections.Counter()
for c in cases:
    if c["id"] in dev or isinstance(c["state"], str):
        continue
    fl = list(fields(c["state"]))
    nums = [(p, v) for p, v in fl if not isinstance(v, dt.date)]
    dates = [(p, v) for p, v in fl if isinstance(v, dt.date)]
    lists = list(record_lists(c["state"]))
    makers = [("threshold", lambda: q_threshold(nums) if nums else None), ("pair", lambda: q_pair(nums)),
              ("max", lambda: q_max(lists)), ("dates", lambda: q_dates(dates)),   # sums dropped: too often meaningless
              ("band", lambda: q_band(nums) if nums else None)]
    rnd.shuffle(makers)
    qs, golds, seen = {}, {}, set()
    for name, make in makers:
        if len(qs) == PER_CASE:
            break
        r = make()
        if r and r[0]["instructions"] not in seen:
            qid = f"q{len(qs) + 1}"
            qs[qid], golds[qid] = r
            seen.add(r[0]["instructions"])
            kinds[name] += 1
    if qs:
        out.append({"id": f"N-{c['id']}", "state": c["state"], "questions": qs, "gold": golds,
                    "meta": {"domain": c["meta"]["domain"], "form": c["meta"]["form"],
                             "kinds": {q: "compare" for q in qs}, "synthetic": "number questions", "source": c["id"]}})
with open(HERE / "systemone.jsonl", "w", encoding="utf-8") as fh:
    for c in out:
        fh.write(json.dumps(c, ensure_ascii=False) + "\n")
types = collections.Counter(q["type"] for c in out for q in c["questions"].values())
truth = collections.Counter(max(g["probabilities"], key=g["probabilities"].get) for c in out for g in c["gold"].values()
                            if g["type"] == "noul")
print({"cases": len(out), "questions": sum(types.values()), **types, "by template": dict(kinds), "noul top": dict(truth),
       "source cases in dev": sum(c["meta"]["source"] in dev for c in out)})
