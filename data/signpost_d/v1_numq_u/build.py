"""Unhinted number questions built by code from the JSON states of v1_4's training cases (no model writes anything).
Unlike v1_numq, a question never names a field by its path or quotes the deciding value: fields are described by their
meaning ("the price in GBP of the car on offer"), rows of a list by another of their own fields ("the line whose sku is
K-22"). Kinds: a threshold on one field, a two-hop lookup in a list, a ratio or a difference of two fields and a gap
between two dates (each with a graded margin: the true value at 0.5x / 0.9x / 0.98x / 1.02x / 1.1x / 2x of the limit,
recorded in meta), the highest / lowest / latest entry of a list (choice), and a size band (score). Golds are exact,
softened as clear-cut labels (about 0.95 on the right answer).

Held out for measurement (never trained on): 15% of the source cases, and two phrasings ("threshold:at_least",
"twohop:under") that appear only in held-out cases. Dev cases of the notebooks are excluded entirely. New case ids start
with "U"; training only. Writes systemone.jsonl (training) and heldout.jsonl here; usage: build.py"""
import collections
import datetime as dt
import json
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "v1_4" / "systemone.jsonl"
SEED, DEV_FRACTION, HELDOUT_FRACTION, PER_CASE = 42, 0.15, 0.15, 4
MARGINS = [0.5, 0.9, 0.98, 1.02, 1.1, 2.0]
MARGIN_W = [1, 1, 0.5, 0.5, 1, 1]                 # narrow margins rarer: the benchmark's ~4B teacher is unreliable there too
HELD_PHRASINGS = {"threshold:at_least", "twohop:under"}
SKIP = re.compile(r"(?i)(^|_)(id|ids|ref|refs|code|codes|no|number|phone|zip|postcode|sku|year|version|seq|index|rank|"
                  r"page|line|floor|room|unit|account|policy)$")
ID_KEYS = ("id", "ref", "name", "code", "sku", "item", "supplier", "applicant", "candidate", "product", "vendor", "title",
           "invoice", "customer", "site", "room", "patient", "contractor", "service", "task", "ticket", "property")
UNITS = {"gbp": "GBP", "usd": "USD", "eur": "EUR", "inr": "INR", "aud": "AUD", "sek": "SEK", "kg": "kg", "g": "g",
         "pct": "%", "percent": "%", "hours": "hours", "hrs": "hours", "days": "days", "minutes": "minutes",
         "mins": "minutes", "months": "months", "weeks": "weeks", "km": "km", "m": "metres", "m2": "square metres",
         "sqm": "square metres", "litres": "litres", "liters": "litres", "seats": "seats", "people": "people",
         "years": "years"}
WORDS = {"qty": "quantity", "amt": "amount", "desc": "description", "est": "estimate", "max": "maximum", "min": "minimum",
         "avg": "average", "temp": "temperature", "apr": "APR", "mot": "MOT", "vat": "VAT", "kpi": "KPI", "sla": "SLA"}
MONTHS = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}
DATE_PATTERNS = [
    re.compile(r"^(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})"),
    re.compile(r"^(?P<d>\d{1,2}) (?P<mon>[A-Za-z]{3,9})\.? (?P<y>\d{4})"),
    re.compile(r"^(?P<mon>[A-Za-z]{3,9})\.? (?P<d>\d{1,2}),? (?P<y>\d{4})"),
]
rnd = random.Random(7)


def dev_split(ids, fraction=DEV_FRACTION, seed=SEED):
    ids = sorted(ids)
    random.Random(seed).shuffle(ids)
    return set(ids[: int(len(ids) * fraction)])


def as_date(s):
    if not isinstance(s, str):
        return None
    for pat in DATE_PATTERNS:
        m = pat.match(s.strip())
        if m:
            g = m.groupdict()
            month = int(g["m"]) if g.get("m") else MONTHS.get(g["mon"][:3].lower())
            try:
                return dt.date(int(g["y"]), month, int(g["d"])) if month else None
            except ValueError:
                return None
    return None


def words(key):
    """A key as plain words with its unit: "price_gbp" -> ("price", "GBP")."""
    parts = [p for p in re.split(r"[_\s]+", str(key)) if p]
    unit = None
    if len(parts) > 1 and parts[-1].lower() in UNITS:
        unit = UNITS[parts.pop().lower()]
    return " ".join(WORDS.get(p.lower(), p.lower()) for p in parts), unit


def describe(path):
    """A field's meaning, without its path: ("car_on_offer", "price_gbp") -> "the price in GBP of the car on offer"."""
    if not path or any(isinstance(k, int) for k in path) or any(re.match(r"\d", str(k)) for k in path):
        return None
    name, unit = words(path[-1])
    if not name or name.endswith((" since", " from", " to", " until")) or name in ("from", "to", "since", "until"):
        return None
    if name == "today":
        return "today's date" if len(path) == 1 else None
    d = f"the {name}" + (f" in {unit}" if unit and unit != "%" else " (%)" if unit == "%" else "")
    if len(path) > 1:
        parent, _ = words(path[-2])
        if parent in ("min", "minimum", "max", "maximum"):
            return None
        d += f" of the {parent}"
    return d


def fmt(v):
    if isinstance(v, float):
        return f"{v:,.2f}".rstrip("0").rstrip(".")
    return f"{v:,}"


def nice(v, whole=False):
    """A rounded limit near v (a whole number for whole-number fields)."""
    a = abs(v)
    if whole:
        return int(round(v, -2) if a >= 5000 else round(v, -1) if a >= 200 else round(v))
    r = round(v, -2) if a >= 5000 else round(v, -1) if a >= 200 else round(v) if a >= 20 else round(v, 1)
    return int(r) if float(r).is_integer() else r


def fields(x, p=()):
    """(path, value) leaves: plain numbers (not bools) and dates."""
    if isinstance(x, dict):
        for k, v in x.items():
            yield from fields(v, p + (k,))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from fields(v, p + (i,))
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        if p and isinstance(p[-1], str) and not SKIP.search(p[-1]) and 0 < abs(x) < 1e9:
            yield p, x
    elif as_date(x):
        yield p, as_date(x)


def record_lists(x, p=()):
    """Lists of 3-6 records that share an identifying text key: (path, id key, records)."""
    if isinstance(x, dict):
        for k, v in x.items():
            yield from record_lists(v, p + (k,))
    elif isinstance(x, list):
        if 3 <= len(x) <= 6 and all(isinstance(r, dict) for r in x):
            idk = next((k for k in x[0] if any(t in k.lower() for t in ID_KEYS)
                        and all(isinstance(r.get(k), str) and len(r[k]) <= 40 for r in x)), None)
            if idk and len({r[idk] for r in x}) == len(x):
                yield p, idk, x
        for i, v in enumerate(x):
            yield from record_lists(v, p + (i,))


def noul(statement, true_desc, false_desc, truth):
    g = 0.95 if truth else 0.05
    return ({"type": "noul", "instructions": statement, "criteria": {"true": true_desc, "false": false_desc}},
            {"type": "noul", "probabilities": {"true": g, "false": round(1 - g, 2)}})


def margin():
    return rnd.choices(MARGINS, MARGIN_W)[0]


# Each maker returns (question, gold, info) or None; info: template, phrasing, margin, deciding paths, raw values

def q_threshold(c):
    named = [(p, v) for p, v in c["nums"] if describe(p)]
    if not named:
        return None
    p, v = rnd.choice(named)
    m = margin()
    x = nice(v / m, isinstance(v, int))
    if x == v or x <= 0:
        return None
    d = describe(p)
    phrasing = rnd.choice(["more", "at_least"])
    if phrasing == "more":
        q = noul(f"{d[0].upper() + d[1:]} is more than {fmt(x)}.", f"above {fmt(x)}", f"{fmt(x)} or less", v > x)
    else:
        q = noul(f"{d[0].upper() + d[1:]} is at least {fmt(x)}.", f"{fmt(x)} or more", f"under {fmt(x)}", v >= x)
    return (*q, {"template": "threshold", "phrasing": f"threshold:{phrasing}", "margin": round(v / x, 3), "paths": [p], "values": [v]})


def q_twohop(c):
    opts = []
    for lp, idk, recs in c["lists"]:
        for k in recs[0]:
            if k != idk and not SKIP.search(k) and all(isinstance(r.get(k), (int, float)) and not isinstance(r.get(k), bool)
                                                       for r in recs):
                opts.append((lp, idk, recs, k))
    if not opts:
        return None
    lp, idk, recs, k = rnd.choice(opts)
    r = rnd.choice(recs)
    v = r[k]
    m = margin()
    x = nice(v / m, isinstance(v, int)) if v else None
    if not x or x == v:
        return None
    name, unit = words(k)
    idn, _ = words(idk)
    what = f"the {name}" + (f" in {unit}" if unit and unit != "%" else "")
    phrasing = rnd.choice(["over", "under"])
    who = f"For the entry whose {idn} is {r[idk]}"
    if phrasing == "over":
        q = noul(f"{who}, {what} is more than {fmt(x)}.", f"above {fmt(x)}", f"{fmt(x)} or less", v > x)
    else:
        q = noul(f"{who}, {what} is below {fmt(x)}.", f"below {fmt(x)}", f"{fmt(x)} or more", v < x)
    path = lp + (recs.index(r), k)
    return (*q, {"template": "twohop", "phrasing": f"twohop:{phrasing}", "margin": round(v / x, 3), "paths": [path], "values": [v]})


MONEY = {"net", "vat", "tax", "total", "subtotal", "amount", "fee", "fees", "cost", "price", "charge", "deposit", "freight",
         "discount", "budget", "balance", "spend", "refund", "payment", "salary", "rent", "value", "limit", "estimate"}


def unit_of(key):
    """A field's unit: from its suffix (price_gbp -> GBP), or "money" for plain money words."""
    name, unit = words(key)
    if unit:
        return unit
    return "money" if name.split(" ")[-1] in MONEY else None


def comparable_pairs(c):
    """Sibling fields with the same unit (both named), as (path a, a, path b, b)."""
    groups = collections.defaultdict(list)
    for p, v in c["nums"]:
        if describe(p) and unit_of(p[-1]) and unit_of(p[-1]) != "%":
            groups[(p[:-1], unit_of(p[-1]))].append((p, v))
    return [(pa, a, pb, b) for g in groups.values() for (pa, a) in g for (pb, b) in g if pa != pb and a > 0 and b > 0]


def q_ratio(c):
    pairs = comparable_pairs(c)
    if not pairs:
        return None
    pa, a, pb, b = rnd.choice(pairs)
    m = margin()
    pct = round(100 * a / b / m, 1)
    if pct <= 0 or abs(100 * a / b - pct) < 1e-9:
        return None
    da, db = describe(pa), describe(pb)
    q = noul(f"{da[0].upper() + da[1:]} is more than {fmt(pct)}% of {db}.", f"more than {fmt(pct)}%",
             f"{fmt(pct)}% or less", 100 * a / b > pct)
    return (*q, {"template": "ratio", "phrasing": "ratio:more", "margin": round(100 * a / b / pct, 3), "paths": [pa, pb], "values": [a, b]})


def q_difference(c):
    pairs = [(pa, a, pb, b) for pa, a, pb, b in comparable_pairs(c) if a > b]
    if not pairs:
        return None
    pa, a, pb, b = rnd.choice(pairs)
    m = margin()
    d = nice((a - b) / m, isinstance(a, int) and isinstance(b, int))
    if d <= 0 or d == a - b:
        return None
    da, db = describe(pa), describe(pb)
    q = noul(f"{da[0].upper() + da[1:]} exceeds {db} by more than {fmt(d)}.", f"the gap is more than {fmt(d)}",
             f"the gap is {fmt(d)} or less", a - b > d)
    return (*q, {"template": "difference", "phrasing": "difference:more", "margin": round((a - b) / d, 3), "paths": [pa, pb], "values": [a, b]})


def q_dates(c):
    named = [(p, v) for p, v in c["dates"] if describe(p)]
    pairs = [(x, y) for x in named for y in named if x[1] < y[1]]
    if not pairs:
        return None
    (pa, a), (pb, b) = rnd.choice(pairs)
    gap = (b - a).days
    m = margin()
    n = max(1, round(gap / m))
    if n == gap:
        return None
    da, db = describe(pa), describe(pb)
    q = noul(f"{db[0].upper() + db[1:]} is more than {n} days after {da}.", f"more than {n} days later",
             f"{n} days later or less", gap > n)
    return (*q, {"template": "dates", "phrasing": "dates:after", "margin": round(gap / n, 3), "paths": [pa, pb], "values": [str(a), str(b)]})


def q_extreme(c):
    opts = []
    for lp, idk, recs in c["lists"]:
        for k in recs[0]:
            if k == idk or SKIP.search(k):
                continue
            vals = [r.get(k) for r in recs]
            if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in vals) and len(set(vals)) == len(vals):
                opts.append((lp, idk, recs, k, vals, rnd.choice(["highest", "lowest"])))
            elif all(as_date(v) for v in vals) and len({as_date(v) for v in vals}) == len(vals):
                opts.append((lp, idk, recs, k, [as_date(v) for v in vals], rnd.choice(["latest", "earliest"])))
    if not opts:
        return None
    lp, idk, recs, k, vals, how = rnd.choice(opts)
    pick = vals.index(max(vals) if how in ("highest", "latest") else min(vals))
    name, unit = words(k)
    idn, _ = words(idk)
    labels = [r[idk] for r in recs]
    crit = {lab: f"The entry whose {idn} is {lab}" for lab in labels}
    probs = {lab: (0.94 if i == pick else round(0.06 / (len(recs) - 1), 4)) for i, lab in enumerate(labels)}
    what = f"{name}" + (f" in {unit}" if unit and unit != "%" else "")
    return ({"type": "choice", "instructions": f"Which entry has the {how} {what}?", "criteria": crit},
            {"type": "choice", "probabilities": probs},
            {"template": "extreme", "phrasing": f"extreme:{how}", "margin": None,
             "paths": [lp + (i, k) for i in range(len(recs))], "values": [str(v) for v in vals]})


def q_band(c):
    named = [(p, v) for p, v in c["nums"] if describe(p) and abs(v) >= 4]
    if not named:
        return None
    p, v = rnd.choice(named)
    level = rnd.randrange(4)
    width = max(abs(v) * rnd.uniform(0.15, 0.35), 1)
    lo = v - width * (level + rnd.uniform(0.25, 0.75))
    cuts = [nice(lo + width * (i + 1)) for i in range(3)]
    if len(set(cuts)) < 3 or v in cuts or sum(v >= x for x in cuts) != level or cuts != sorted(cuts):
        return None
    d = describe(p)
    crit = [f"Under {fmt(cuts[0])}: {d} is below {fmt(cuts[0])}",
            f"{fmt(cuts[0])} to under {fmt(cuts[1])}: {d} is at least {fmt(cuts[0])} and below {fmt(cuts[1])}",
            f"{fmt(cuts[1])} to under {fmt(cuts[2])}: {d} is at least {fmt(cuts[1])} and below {fmt(cuts[2])}",
            f"{fmt(cuts[2])} or more: {d} is {fmt(cuts[2])} or above"]
    probs = {str(i): (0.94 if i == level else 0.03 if abs(i - level) == 1 else 0.0) for i in range(4)}
    probs[str(level)] = round(probs[str(level)] + 1 - sum(probs.values()), 4)
    return ({"type": "score", "instructions": f"How large is {d}?", "criteria": crit},
            {"type": "score", "probabilities": probs},
            {"template": "band", "phrasing": "band:size", "margin": None, "paths": [p], "values": [v]})


MAKERS = [q_ratio, q_difference, q_twohop, q_extreme, q_dates, q_threshold, q_band]   # rarest first; at most one band


def path_text(p):
    out = ""
    for k in p:
        out += f"[{k}]" if isinstance(k, int) else (f".{k}" if out else str(k))
    return out


def unhinted(q, info):
    """The question names no path (dotted or bracketed) and quotes no deciding value."""
    text = q["instructions"] + " " + json.dumps(q["criteria"], ensure_ascii=False)
    if any(path_text(p) in text for p in info["paths"] if len(p) > 1) or "`" in text or re.search(r"\w\.\w+\[|\[\d+\]", text):
        return False
    for v in info["values"]:
        s = fmt(v) if isinstance(v, (int, float)) else str(v)
        if info["template"] != "extreme" and re.search(rf"(?<![\d.,]){re.escape(s)}(?![\d.,]*\d)", q["instructions"]):
            return False
    return True


cases = [json.loads(l) for l in open(SRC, encoding="utf-8")]
dev = dev_split(c["id"] for c in cases if not c["id"].startswith(("I", "K", "L", "T")))
for g in ("I", "K", "L"):
    dev |= dev_split(c["id"] for c in cases if c["id"].startswith(g))
sources = [c for c in cases if c["id"] not in dev and not isinstance(c["state"], str)]
held_src = dev_split((c["id"] for c in sources), HELDOUT_FRACTION, seed=SEED + 1)
train_out, held_out, stats = [], [], collections.Counter()
for c in sources:
    fl = list(fields(c["state"]))
    ctx = {"nums": [(p, v) for p, v in fl if not isinstance(v, dt.date)],
           "dates": [(p, v) for p, v in fl if isinstance(v, dt.date)], "lists": list(record_lists(c["state"]))}
    held = c["id"] in held_src
    qs, golds, infos, seen = {}, {}, {}, set()
    for make in MAKERS * 2:                                    # two passes: a second question of a kind if room is left
        if len(qs) == PER_CASE:
            break
        if make is q_band and any(i["template"] == "band" for i in infos.values()):
            continue
        for _ in range(4):                                     # redraw a held-out phrasing on a training case, or a repeat
            r = make(ctx)
            if r and r[0]["instructions"] not in seen and (held or r[2]["phrasing"] not in HELD_PHRASINGS):
                break
        else:
            r = None
        if not r:
            continue
        q, g, info = r
        if not unhinted(q, info):
            stats["rejected: names a path or quotes a deciding value"] += 1
            continue
        qid = f"q{len(qs) + 1}"
        qs[qid], golds[qid] = q, g
        infos[qid] = {**info, "paths": [path_text(p) for p in info["paths"]], "values": [str(v) for v in info["values"]],
                      "phrasing_heldout": info["phrasing"] in HELD_PHRASINGS}
        seen.add(q["instructions"])
        stats[f"{'held' if held else 'train'} {info['template']}"] += 1
    if qs:
        rec = {"id": f"U-{c['id']}", "state": c["state"], "questions": qs, "gold": golds,
               "meta": {"domain": c["meta"]["domain"], "form": c["meta"]["form"], "kinds": {q: "compare" for q in qs},
                        "synthetic": "unhinted number questions", "source": c["id"], "heldout": held, "numq": infos}}
        (held_out if held else train_out).append(rec)
for name, rows in (("systemone.jsonl", train_out), ("heldout.jsonl", held_out)):
    with open(HERE / name, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
types = collections.Counter(q["type"] for c in train_out for q in c["questions"].values())
margins = collections.Counter(i["margin"] is not None and min(MARGINS, key=lambda m: abs(m - i["margin"]))
                              for c in train_out for i in c["meta"]["numq"].values())
truth = collections.Counter(max(g["probabilities"], key=g["probabilities"].get) for c in train_out for g in c["gold"].values()
                            if g["type"] == "noul")
print(json.dumps({"train cases": len(train_out), "train questions": sum(types.values()), "types": types,
                  "held-out cases": len(held_out), "held-out questions": sum(len(c["questions"]) for c in held_out),
                  "noul top": truth, "margins (nearest grade)": {str(k): v for k, v in margins.items()},
                  "source cases in dev": sum(c["meta"]["source"] in dev for c in train_out + held_out),
                  **dict(sorted(stats.items()))}, indent=1, default=str))
