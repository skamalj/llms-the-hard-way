# thanos_v3 — the same 150 statements, targets in the curated Thanos voice

| Path | What |
|---|---|
| `raw/validation_thanos_v3.jsonl` | the curated validation set (25), as provided — **the style reference** |
| `raw/train_thanos_v3.jsonl`, `raw/test_thanos_v3.jsonl` | train (100) and test (25): thanos_v2's inputs and meanings, **targets rewritten** in the reference voice |
| `train.jsonl`, `validation.jsonl`, `test.jsonl`, `manifest.json` | converted for the prefix-bridge notebook (`TARGET = "thanos"`) |
| `build_v3.py` | holds the rewritten targets and rebuilds everything above from `../thanos_v2/raw/` and the validation file |

**Voice** (from the reference set): restrained, solemn, strategic, commanding; formal diction ("laid bare", "lend my support", "Should the alarm sound twice…"); numbers written as words; often a short second sentence that restates what follows from the source ("Not a moment sooner.", "Neither alone is sufficient."). Every fact, name, quantity, negation, condition and timing kept; no new events, threats, promises or conclusions.

**Changes from v2 in train and test:**
- all 125 targets rewritten in the reference voice; 53 of 100 training targets have a second sentence (validation: 17 of 25);
- s137 restored as a condition ("*Should* Leo be late again…"; v2 stated it as a fact);
- s139's computed fact ("The shortfall is four thousand") removed;
- no target repeats its input (v2: s121 in validation; v3 first draft: s078, s109; all fixed).

**Checked:** every number (as digits or words), name and negation of the source meaning appears in its target; splits unchanged from v2 (no meaning shared or near-duplicated across splits). Inputs unchanged (half English, half Roman Hinglish).

**Status:** validation curated by the project owner's author; train and test targets rewritten by Claude (an AI). Neither has had an independent human review.
