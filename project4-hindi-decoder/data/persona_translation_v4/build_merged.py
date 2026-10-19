"""Rebuilds merged/ from the two raw deliveries (raw_A, raw_B): B is canonical for evaluation and training; A adds
training volume and extra references. Run from anywhere:  python build_merged.py"""
import collections
import csv
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
A_DIR, B_DIR, OUT = HERE / "raw_A", HERE / "raw_B", HERE / "merged"


def load_a(A_DIR):
    src, tgt = {}, []
    for f in ("train", "validation", "test", "ood", "minimal_pairs"):
        for line in open(f"{A_DIR}/{f}_v4.jsonl", encoding="utf-8-sig"):
            r = json.loads(line)
            sn = r.get("semantic_note") or {}
            src.setdefault(r["source_id"], {
                "id": r["source_id"], "split": r["split"], "text": r["source"],
                "paraphrases": r.get("source_paraphrases") or [], "core": sn.get("core_meaning", ""),
                "must_keep": sn.get("must_keep", []), "tags": (r.get("tags") or {}).get("logic", []),
                "pair_id": (r.get("tags") or {}).get("pair_id")})
            tgt.append({"source_id": r["source_id"], "persona": r["persona_id"], "target": r["target"],
                        "alt": r.get("alt_target") or "", "review": r.get("review_status", "")})
    return src, tgt


def load_b(B_DIR):
    src = {}
    for r in csv.DictReader(open(f"{B_DIR}/sources.csv", encoding="utf-8-sig")):
        src[r["source_id"]] = {"id": r["source_id"], "split": r["split"], "text": r["source_text"],
                               "paraphrases": [x for x in (r["paraphrase_1"], r["paraphrase_2"]) if x],
                               "core": r["core_meaning"], "must_keep": [x.strip() for x in r["must_keep"].split("|")],
                               "tags": [] if r["logic_tags"] == "none" else [x.strip() for x in r["logic_tags"].split("|")],
                               "pair_id": r["pair_id"] or None}
    tgt = [{"source_id": r["source_id"], "persona": r["persona_id"], "target": r["target_text"],
            "alt": r["alt_target_text"], "review": r["review_status"]}
           for r in csv.DictReader(open(f"{B_DIR}/targets.csv", encoding="utf-8-sig"))]
    return src, tgt



P = ["don", "anthony_gonsalves", "jai_sholay"]
PERSONAS = {
    "don": {"name": "Don", "description": "Cool, calculating and faintly amused; short, controlled sentences; treats "
            "every situation as a move in a game; a quiet hint of control, never loud."},
    "anthony_gonsalves": {"name": "Anthony Gonsalves", "description": "Cheerful, theatrical Bombay street-smart; playful "
                          "exaggeration and comic comparisons; freely mixes English and Hindi."},
    "jai_sholay": {"name": "Jai (Sholay)", "description": "Calm, laconic and practical; dry understatement; loyal; says "
                   "only what is needed."},
}
A_src, A_tgt = load_a(A_DIR)
B_src, B_tgt = load_b(B_DIR)
A_by = collections.defaultdict(dict)
for t in A_tgt:
    A_by[t["source_id"]][t["persona"]] = t
B_by = collections.defaultdict(dict)
for t in B_tgt:
    B_by[t["source_id"]][t["persona"]] = t
GIVEN = {f"s{i:03d}" for i in range(1, 61)}
EVAL_SPLITS = ("validation", "test")


def note(s):
    return {"core_meaning": s["core"], "must_keep": s["must_keep"]}


rows = collections.defaultdict(list)

# --- evaluation and training from B (canonical)
for sid, s in B_src.items():
    split = s["split"]
    for p in P:
        t = B_by[sid][p]
        refs = [t["target"]] + ([t["alt"]] if t["alt"] else [])
        if sid in GIVEN and split in EVAL_SPLITS:      # A's lines for the given validation/test sentences: references only
            a = A_by[sid][p]
            refs += [x for x in (a["target"], a["alt"]) if x and x not in refs]
        rows[split].append({"id": f"{sid}_{p}", "source_id": sid, "split": split, "persona_id": p, "source": s["text"],
                            "target": t["target"], "references": refs, "paraphrases": s["paraphrases"],
                            "semantic_note": note(s), "tags": s["tags"], "pair_id": s["pair_id"], "origin": "B"})

# --- training additions from A (never an evaluation sentence of B, never a copy of a given sentence)
words = lambda t: set(re.findall(r"[a-z0-9']+", t.lower()))
similar = lambda a, b: len(words(a) & words(b)) / len(words(a) | words(b)) >= 0.6
b_eval_text = [s["text"] for s in B_src.values() if s["split"] != "train"]
given_text = [B_src[g]["text"] for g in sorted(GIVEN)]
A_COPIES = sorted(sid for sid, s in A_src.items() if sid not in GIVEN and s["split"] in ("train", "validation", "test")
                  and any(similar(s["text"], g) for g in given_text))
added = collections.Counter()


def add_train(source_id, source, p, target, origin):
    assert not any(similar(source, e) for e in b_eval_text), f"would leak an evaluation sentence: {source}"
    rows["train"].append({"id": f"{source_id}_{p}", "source_id": source_id, "split": "train", "persona_id": p,
                          "source": source, "target": target, "references": [target], "paraphrases": [],
                          "semantic_note": None, "tags": [], "pair_id": None, "origin": origin})
    added[origin] += 1


for sid, s in A_src.items():
    if s["split"] in ("ood", "minimal_pairs"):
        continue
    for p in P:
        a = A_by[sid][p]
        if sid in GIVEN:
            if s["split"] == "train":
                add_train(f"A_{sid}", s["text"], p, a["target"], "A: second version of a given training sentence")
            continue                                    # given validation/test sentences: used as references above
        if sid in A_COPIES:                             # A's "new" sentence copies a given one: dropped
            continue
        add_train(f"A_{sid}", s["text"], p, a["target"], "A: new sentence")
        if a["alt"]:
            add_train(f"A_{sid}_alt", s["text"], p, a["alt"], "A: second target of a new sentence")
        for k, para in enumerate(s["paraphrases"], 1):
            add_train(f"A_{sid}_para{k}", para, p, a["target"], "A: paraphrase of a new sentence")

# --- extra out-of-domain sentences from A (evaluation only), skipping the two shared with B
b_ood_text = {s["text"].lower() for s in B_src.values() if s["split"] == "ood"}
for sid, s in A_src.items():
    if s["split"] != "ood" or s["text"].lower() in b_ood_text:
        continue
    for p in P:
        a = A_by[sid][p]
        rows["ood"].append({"id": f"A_{sid}_{p}", "source_id": f"A_{sid}", "split": "ood", "persona_id": p,
                            "source": s["text"], "target": a["target"], "references": [a["target"]],
                            "paraphrases": [], "semantic_note": None, "tags": s["tags"], "pair_id": None,
                            "origin": "A"})

# --- checks: no source text in two splits; no duplicate pairs
split_of = collections.defaultdict(set)
for split, rs in rows.items():
    for r in rs:
        split_of[r["source"].lower()].add(split)
leak = {t: s for t, s in split_of.items() if len(s) > 1}
assert not leak, leak
for split, rs in rows.items():
    assert len({r["id"] for r in rs}) == len(rs), split

for split, rs in rows.items():
    with open(f"{OUT}/{split}.jsonl", "w", encoding="utf-8") as fh:
        for r in rs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

manifest = {
    "dataset": "persona_translation_v4 (merged)",
    "task": "English source -> natural conversational Roman-script Hinglish in one persona's voice, meaning preserved",
    "personas": PERSONAS,
    "files": {split: len(rs) for split, rs in rows.items()},
    "sources": {split: len({r["source_id"] for r in rs}) for split, rs in rows.items()},
    "train_origin": dict(collections.Counter(r["origin"] for r in rows["train"])),
    "evaluation": "validation, test and minimal_pairs are delivery B only; ood is B plus 18 extra sentences from A",
    "dropped_from_A": {"copies_of_given_sentences": A_COPIES, "minimal_pairs": "all (9 targets miss the "
                       "distinguishing number)", "semantic_notes": "all (templated)"},
    "notes": "Both deliveries were written by AI sessions; neither has had the independent human Hinglish review the "
             "specification requires. Delivery A's semantic notes are templated and not used; its minimal pairs are "
             "dropped (9 targets miss the number that distinguishes the pair).",
}
json.dump(manifest, open(f"{OUT}/manifest.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: manifest[k] for k in ("files", "sources", "train_origin")}, indent=1))
