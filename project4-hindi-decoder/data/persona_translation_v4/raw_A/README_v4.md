# Persona Language Translation Dataset v4

Translate English source sentences into natural conversational Roman-script Hinglish while preserving meaning, facts, intent, negation, conditions, names and numbers. This is translation, not reaction generation.

## Personas
- Don: Cool, calculating and faintly amused; short, controlled sentences; treats every situation as a move in a game; a quiet hint of control, never loud.
- Anthony Gonsalves: Cheerful, theatrical Bombay street-smart; playful exaggeration and comic comparisons; freely mixes English and Hindi.
- Jai (Sholay): Calm, laconic and practical; dry understatement; loyal; says only what is needed.

## Main dataset
150 sources × 3 personas = 450 pairs. Train: 100 sources / 300 pairs; validation: 25 / 75; test: 25 / 75. Split by source ID.
Files: manifest_v4.json; train_v4.jsonl; validation_v4.jsonl; test_v4.jsonl; ood_v4.jsonl; minimal_pairs_v4.jsonl; changelog_v4.csv.

## Evaluation-only sets
OOD contains 20 informal sources × 3 personas. Minimal pairs contain 12 meaning-critical pairs (24 sources) × 3 personas. Keep both out of training and checkpoint selection.

## Review status
Draft, not independently approved. A fluent Hinglish reviewer must check naturalness, meaning preservation, persona separation, spelling and unsupported additions. Keep test, OOD and minimal-pair sets out of training and checkpoint selection.
