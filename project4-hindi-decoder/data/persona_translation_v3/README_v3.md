# Persona Language Translation Dataset — v3

## Task definition
Translate **English source sentences** into **natural conversational Hinglish written in Roman script**, using one of six persona voices. This is translation/persona-language realization, **not open-ended reaction generation or style transfer**.

The source proposition should remain intact. Persona-specific wording, syntax, rhythm, register, and framing may change, but the target must not invent a new event, change the speaker's factual claim, or reverse the meaning.

## Personas
- `vijay_deewar`: proud, self-made, quietly defiant
- `don`: cool, calculating, concise, faintly amused
- `shahenshah`: grand, justice-driven, regal, Urdu-tinged
- `anthony_gonsalves`: playful, theatrical, comic, freely code-switches
- `vijay_agneepath`: intense, terse, controlled anger
- `jai_sholay`: calm, laconic, dry humour, practical loyalty

These are original paraphrases inspired by broad character traits; they are not copied film dialogue.

## Size and splits
- 60 English source statements
- 6 target personas per source
- 360 source-target pairs total
- Train: 40 source statements / 240 pairs (`s001`–`s040`)
- Validation: 10 source statements / 60 pairs (`s041`–`s050`)
- Test: 10 source statements / 60 pairs (`s051`–`s060`)

**Leakage prevention:** split by `source_id`; a source sentence and its six persona translations occur in exactly one split.

## Files
- `persona_translation_dataset_v3.json`: complete manifest, persona descriptions, source inventory and all pairs
- `train_v3.json` / `train_v3.jsonl`
- `validation_v3.json` / `validation_v3.jsonl`
- `test_v3.json` / `test_v3.jsonl`

Each pair includes `source`, `target`, `persona_id`, `split`, and `input`. The `input` explicitly asks for English-to-Roman-Hinglish translation.

## Quality caveats
This is a manually authored starter dataset for an educational experiment, not a production-quality linguistic benchmark. Hinglish varies by speaker and region; before training, review target naturalness, persona distinctiveness, and semantic fidelity with fluent Hinglish speakers. The held-out test split should remain untouched during model selection.
