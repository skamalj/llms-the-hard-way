# persona_translation_v4 — two deliveries, one merged dataset

English source → natural conversational Roman-script Hinglish in one of three persona voices (Don, Anthony Gonsalves, Jai), meaning preserved. Specification: [`../../docs/data-requirements-v4.md`](../../docs/data-requirements-v4.md).

| Folder | What |
|---|---|
| `raw_A/` | delivery A, unchanged (`persona_translation_v4.zip`; JSONL per split, written to the first draft of the specification) |
| `raw_B/` | delivery B, unchanged (`persona_translation_v4_1.zip`; `sources.csv`, `targets.csv`, `delivery_notes.md`, written to the final specification) |
| `merged/` | **use this**: `train.jsonl`, `validation.jsonl`, `test.jsonl`, `ood.jsonl`, `minimal_pairs.jsonl`, `manifest.json` |
| `build_merged.py` | rebuilds `merged/` from the two raw folders |

**Neither delivery has had an independent human review.** Both were written by AI sessions (B by one Claude session and reviewed by another; A marked "draft, not independently approved"). The specification's human Hinglish review is still open.

## Checks on the two deliveries (2026-10-19)

| Check | A | B |
|---|---|---|
| Counts, ids, given sentences s001–s060 unchanged | ✓ | ✓ |
| Roman script, ≤ 35 words, no quotes or labels | ✓ (4 lines start lowercase) | ✓ |
| Every number in the source kept in every target | ✗ 9 targets miss it, incl. both number-type minimal pairs | ✓ |
| Semantic notes specific to the sentence | ✗ templated ("Preserve who does what…" on all 194) | ✓ |
| Anthony's address words within the 1-in-5 limit | ✓ | ✓ |
| Given sentences: targets written fresh | 130 of 180 are the old v3 lines | ✓ all 180 fresh |
| "New" sentences really new | ✗ 16 of 90 copy a given sentence (all of s121–s135, and s136) | ✓ |
| Review status | all "draft" | 17 revised, 565 approved |

## How the merge works

- **Evaluation is delivery B only:** `validation` (25 sources × 3), `test` (25 × 3) and `minimal_pairs` (24 × 3), with B's semantic notes, paraphrases and second targets. For the 20 given validation and test sentences, A's lines are added to `references` (extra reference translations for scoring; never trained on). `ood` is B's 20 sentences plus A's 18 others (A's two shared sentences skipped).
- **Training** (`train.jsonl`, 768 pairs) is B's 300 pairs plus, from A:
  - 74 genuinely new sentences × 3 personas (222 pairs) and their second targets where A wrote one (42);
  - A's two English paraphrases of its 14 new test-split sentences, each with the sentence's target (84 pairs; same meaning, different wording);
  - A's version of the 40 given training sentences (120 pairs; a second translation of the same sentence).
- **Dropped from A:** the 16 copies of given sentences (with their targets, paraphrases and second targets); all minimal pairs (missing numbers); all semantic notes (templated).
- **Leakage guard:** no training sentence matches or nearly matches (word overlap ≥ 0.6) any validation, test, out-of-domain or minimal-pair sentence; no sentence appears in two splits.

## Record format (one JSON object per line)

`id`, `source_id`, `split`, `persona_id`, `source` (English), `target` (Hinglish), `references` (all acceptable targets: the target first), `paraphrases` (validation and test), `semantic_note` (`core_meaning`, `must_keep`; B only), `tags`, `pair_id` (minimal pairs), `origin` (`B` or which part of A). Persona names and descriptions are in `manifest.json`.
