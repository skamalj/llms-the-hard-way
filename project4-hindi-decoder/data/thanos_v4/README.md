# thanos_v4 — English → Thanos-voice English

Every input is ordinary English; every target says the same thing in a restrained, solemn, strategic, commanding voice (Thanos-inspired), keeping every fact, name, quantity, negation, condition and timing, and adding nothing.

| Split | Rows | From |
|---|---|---|
| train | 498 | 100 thanos_v3 training pairs + 398 generated pairs |
| validation | 25 | thanos_v3 (the curated voice reference), targets unchanged |
| test | 25 | thanos_v3, targets unchanged |

**What changed from v3.** No Roman-Hinglish inputs: the 75 v3 rows with a Hinglish input now take their English meaning (`source_meaning`) as input. Three rows whose meaning was word-for-word the target get a plainer everyday wording instead (`PLAIN` in `build_v4.py`: s114, s116, s138), so no target copies its input.

**Generated pairs** (`raw/generated_pairs.jsonl`, 400 lines, written by a Claude subagent with the v3 validation set as style reference). They cover everyday matters (work, home, family, money, travel, health, shopping). Numbers are written as words in targets. Checked: valid JSON, unique inputs and targets, no target equals its input, no digits in targets, names and negations carried (24 negations reworded rather than repeated, e.g. "haven't decided" → "remains undecided"; "Grandma" → "Grandmother"). Two were dropped for resembling a protected sentence (`DROP`): n086 (near a demo sentence of the notebook) and n221 (near an evaluation sentence). Not independently reviewed by a human.

Format: one JSON object per line: `id`, `source_id`, `split`, `persona_id`, `source`, `target`, `references`, `origin` (`thanos_v3` or `generated`). Rebuild: `python build_v4.py`.
