# thanos_v2 — English or Roman-Hinglish statement → the same meaning in a Thanos-inspired English voice

| Path | What |
|---|---|
| `raw/` | the author's delivery `thanos_english_translation_v2_curated.zip`, unchanged (README, manifest, splits, all records) |
| `train.jsonl`, `validation.jsonl`, `test.jsonl` | converted for the prefix-bridge notebook (`TARGET = "thanos"`): `source` = input text, `target` = Thanos line, plus `input_language` and the English `source_meaning` |
| `manifest.json` | persona name and voice description |
| `build_converted.py` | rebuilds the converted files from `raw/` |

**Counts:** 150 records, one per meaning — train 100 (50 English + 50 Roman-Hinglish inputs), validation 25, test 25. Splits are by source meaning; no meaning is shared or near-duplicated across splits (checked).

**Checks (2026-10-20):** no Devanagari; every number in the source is kept in the target, written out in words ("4 pm" → "four in the afternoon"); targets median 16 words, about 1.5× the source meaning. Status as delivered: *curated draft, not human-reviewed*.

**Review notes:** s139 adds a calculated fact ("The shortfall is four thousand"); many targets end with a short persona remark ("The terms are clear."), a few close to an added consequence (s070 "or we accept the consequence of arriving too late"). Half the inputs are Roman Hinglish while the encoder (ModernBERT) is English-only: the notebook reports scores per input language and can be limited to English inputs (`THANOS_INPUTS` in Cell 0).
