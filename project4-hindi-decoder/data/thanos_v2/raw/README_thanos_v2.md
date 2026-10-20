# Thanos-inspired single-statement dataset — v2 curated draft

## Purpose
A single standalone statement in English or Roman-script Hinglish is mapped to an English response with an original Thanos-inspired voice. This is not dialogue generation and contains no conversation history.

## Why this version has 150 records
The earlier 450-record construction used three input variants for each of 150 meanings, with the same target repeated three times. That inflated the record count without adding 450 independent training examples. This version keeps one record per meaning and removes that duplication. Correctness is more important than preserving an inflated count.

## Files
- `train_thanos_v2.jsonl`: 100 records
- `validation_thanos_v2.jsonl`: 25 records
- `test_thanos_v2.jsonl`: 25 records
- `all_records_thanos_v2.jsonl`: 150 records
- `manifest_thanos_v2.json`: counts, policy and validation status

## Important quality status
This is a deduplicated curated draft, not a human-certified dataset. It retains the v1 target drafts and selected English/Roman Hinglish inputs. Every Hinglish input and every persona target should be reviewed by a fluent reviewer before training. Do not interpret structural checks as proof of semantic accuracy.

## Labeling principles
- Preserve meaning, names, quantities, negation, conditions and timing.
- Keep the persona controlled and recognizable, not melodramatic in every line.
- Do not invent a consequence, threat, motive, or fact absent from the source.
- Do not use direct film quotations.
- Keep validation/test source meanings out of training.
