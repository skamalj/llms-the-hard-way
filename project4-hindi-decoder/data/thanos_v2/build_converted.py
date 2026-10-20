"""Converts raw/ (the author's thanos_english_translation_v2_curated files, unchanged) into the record format the
prefix-bridge notebook reads: train / validation / test .jsonl + manifest.json. Run from anywhere: python build_converted.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
manifest = {"dataset": "thanos_v2 (converted)", "source": "raw/manifest_thanos_v2.json",
            "personas": {"thanos": {"name": "Thanos",
                                    "description": json.load(open(HERE / "raw/manifest_thanos_v2.json"))["persona_spec"]["voice"]}},
            "files": {}}
for split in ("train", "validation", "test"):
    rows = [json.loads(line) for line in open(HERE / f"raw/{split}_thanos_v2.jsonl", encoding="utf-8")]
    with open(HERE / f"{split}.jsonl", "w", encoding="utf-8") as out:
        for r in rows:
            out.write(json.dumps({"id": r["id"], "source_id": r["source_id"], "split": r["split"], "persona_id": "thanos",
                                  "source": r["input_text"], "target": r["target_text"], "references": [r["target_text"]],
                                  "input_language": r["input_language"],
                                  "source_meaning": r["semantic_note"]["source_meaning"]}, ensure_ascii=False) + "\n")
    manifest["files"][split] = len(rows)
json.dump(manifest, open(HERE / "manifest.json", "w"), ensure_ascii=False, indent=1)
print(manifest["files"])
