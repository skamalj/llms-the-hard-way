# Data requirements v4 — persona-language translation, three personas

**For:** the data author and the independent Hinglish reviewer · **Project:** Project 4, stitched encoder–decoder (see `encoder_decoder_bridge_e2e_plan_v2.md`) · **Replaces:** data v3 for all further work · **Date:** 2026-10-19

This document is the complete data brief for the rest of the project. It covers everything we need, in priority order, so no further data requests should be necessary.

---

## 1. What changed since v3, and why

We trained and tested a decoder on v3 (Gemma 3 4B IT, LoRA). It learned to stop cleanly and to write Roman-script Hinglish, and its habits follow the data closely. That is good news, and it means **the data now decides most of what the model does, including its mistakes.** What we saw:

| What the model did | Where it comes from in v3 |
|---|---|
| Anthony says "boss" in almost every line, once looping "boss boss boss…" | "boss" appears in **49 of Anthony's 60** targets |
| Anthony's jokes sometimes add facts or reverse the meaning ("busy can be progress, like pizza") | some v3 jokes come close to adding events that are not in the source (s003: "Main yahan full reception lekar baitha tha!") |
| Meaning is lost on contrast, negation and conditions ("celebrate *without ignoring* the remaining work" → "progressing, but not fully") | the model needs many more examples of exactly these structures |
| Numbers, days, times and names are untested | only **2 of 60** sources contain a number, date or time; only **4** contain "because" |
| Long sentences are untested | the longest v3 source has **17 words** |
| Too few examples to learn from; the model over-fits after two passes over the data | 40 training sources |

**Decision: continue with three personas only — Don, Anthony Gonsalves and Jai (Sholay).** Vijay (Deewar), Shahenshah and Vijay Dinanath Chauhan (Agneepath) are dropped; do not write data for them.

---

## 2. The task (unchanged)

Translate an **English source sentence** into **natural conversational Hinglish in Roman script**, in the voice of one persona, **preserving the meaning**. The persona may change wording, rhythm, register and framing. The persona may **not** change the facts, the intent, who does what, negations, conditions, numbers, names, or the commitment the speaker makes.

A target that sounds exactly like the persona but changes the meaning is a **wrong** target.

---

## 3. The three personas (v4 specification)

The **description** below is the exact text the model will see in its prompt; keep the targets consistent with it. Persona ids stay as in v3.

### Don — `don`
**Description:** *Cool, calculating and faintly amused; short, controlled sentences; treats every situation as a move in a game; a quiet hint of control, never loud.*

- **Length:** about 0.8–1.2 × the source's word count.
- **English:** business and everyday English words are fine (plan, risk, deal, clear), but **never a complete English sentence**; roughly half or fewer of the words English.
- **Devices (use sparingly, vary them):** a one-word verdict ("Interesting.", "Simple."), stating consequences coolly, framing things as plans or moves.
- **Avoid:** shouting, insults, exaggeration (that is Anthony), warmth and reassurance (that is Jai).

### Anthony Gonsalves — `anthony_gonsalves`
**Description:** *Cheerful, theatrical Bombay street-smart; playful exaggeration and comic comparisons; freely mixes English and Hindi.*

- **Length:** about 1.0–1.6 × the source.
- **English:** free code-switching, up to about half the words; Hindi grammar must still carry the sentence.
- **Devices:** comic comparison, rhetorical question, exaggeration of what *is* in the source, filmy or street flavour.
- **Address words** ("boss", "yaar", "mere dost", "bhai", "arre"): **each in at most 1 line in 5**, and many lines with none at all.
- **The comedy rule:** a joke may frame, compare or exaggerate the source's own content. It may **not** add a new event, person, object, place or claim about the situation, and it may never weaken or reverse the meaning.
  - ✓ harmless: "Customer ko do opposite answers mile! Yeh help desk hai ya quiz show?" (a rhetorical frame; no new fact)
  - ✗ likely material: "Main yahan full reception lekar baitha tha!" (claims an event the source does not mention; borderline cases go to the reviewer, §7)
  - ✗ material: "Busy ho toh progress bhi ho sakti hai, like pizza!" (reverses the meaning)

### Jai (Sholay) — `jai_sholay`
**Description:** *Calm, laconic and practical; dry understatement; loyal; says only what is needed.*

- **Length:** about 0.7–1.1 × the source; short, but **every part of the meaning must survive** (short ≠ incomplete).
- **English:** mostly Hindi; about a third of the words English or fewer.
- **Devices:** understatement, plain practical next step, an occasional dry remark (at most 1 line in 4).
- **Avoid:** threat or control (that is Don), exaggeration or jokes as the main point (that is Anthony), grand or emotional language.

### Keeping Don and Jai apart

Both write short lines, and the model blurred them. For the same source the two should differ in **stance**, not just words:

| | Don | Jai |
|---|---|---|
| Stance | in control, a step ahead, slightly amused | steady, practical, on your side |
| Typical move | states the consequence or the move | states the plain next step or understates |
| English | business English words welcome | little English |
| Example (source: *"If we keep avoiding the hard conversation, nothing will change."*) | "Hard conversation avoid karte raho. Problem wahin ki wahin rahegi. Simple." | "Baat karni padegi. Chup rehne se kuch nahi badlega." |

---

## 4. What to deliver

### 4.1 Source sentences: 150 in total

- **Keep all 60 v3 sources** (s001–s060) and their split. **Add 90 new sources** (s061–s150).
- **Splits by source** (a source and all its targets live in exactly one split):

| Split | v3 sources | New sources | Total sources | Pairs (× 3 personas) |
|---|---|---|---|---|
| train | s001–s040 | s061–s120 (60) | 100 | 300 |
| validation | s041–s050 | s121–s135 (15) | 25 | 75 |
| test | s051–s060 | s136–s150 (15) | 25 | 75 |

- **Coverage of the 90 new sources** (each source may count in several rows):

| Feature | Share of new sources | Example |
|---|---|---|
| Negation (not, never, no, don't, won't) | ≥ 30 % | "I never said I would pay for it." |
| Contrast (but, instead of, without, rather than, although) | ≥ 25 % | "Fix the cause instead of the symptoms." |
| Condition or time order (if, unless, once, before, after, until) | ≥ 25 % | "Call me once the report is ready." |
| Cause (because, so, since) | ≥ 15 % | "We are late because the train was cancelled." |
| Numbers, days, times, quantities, prices | ≥ 25 % | "The meeting moved to Thursday at 4 pm." |
| Named people or places (invented names) | ≥ 15 % | "Tell Ravi the keys are with Meera." |
| Questions | ≥ 10 % | "Did anyone check the second invoice?" |
| Requests or instructions | ≥ 15 % | "Please send me the photos tonight." |
| Commitments, refusals, apologies, thanks | ≥ 20 % together | "I'm sorry I missed your call." |

- **Length mix of the new sources:** short (4–8 words) about 25 %; medium (9–16) about 45 %; long (17–30) about 20 %; two sentences about 10 %.
- **Topics:** work at most 30 %; the rest from family, friends, neighbours, shopping, travel, health, money, phones and the internet at home, school, food, plans and errands.
- **Avoid:** sentences that invite the persona to *react* instead of translating (e.g. "What do you think about this?" with nothing to translate); idioms whose meaning depends on English wording; near-duplicates of existing sources; film quotes; real public figures; offensive content.

### 4.2 Targets: one per persona per source (450)

- **Revise the 180 v3 targets for these three personas** to the rules in §3 and §5 (especially Anthony's "boss" and additions). Keep good ones unchanged.
- **Write 270 new targets** for the 90 new sources.
- **Record every change** to a v3 target in the changelog (§6.3) with a one-line reason.

### 4.3 Semantic note per source (150, plus §4.6 and §4.7)

Persona-neutral, three parts:

1. **Core meaning:** one sentence stating the proposition that must stay true.
2. **Must keep:** a short list of elements every target must contain — facts, numbers, names, negations, conditions, who does what, the commitment or request.
3. **Allowed variation:** what a persona may change (tone, framing, word order, softening or sharpening) without breaking the meaning.

Example — source: *"I can forgive you, but rebuilding trust will take time."*
- Core meaning: the speaker is willing to forgive, but trust is not restored yet and will take time.
- Must keep: `forgiveness: yes`, `trust: not yet back`, `needs time`.
- Allowed variation: more forceful, playful or understated; may address the listener directly.

### 4.4 A second reference translation for validation and test (150)

For each **validation and test** source, a **second, different acceptable target** per persona: same meaning, same persona, different wording (not a copy with one word changed). Two references let the automatic score accept more than one good phrasing.

### 4.5 English paraphrases of validation and test sources (100)

For each **validation and test** source, **two English paraphrases** with exactly the same meaning and different wording (e.g. active ↔ passive, different word order, a synonym). No new targets are needed: the source's targets apply. These test whether the system understands the meaning or only the surface words.

### 4.6 Out-of-domain set (20 sources × 3 = 60 targets)

A separate split `ood`: **20 short, informal, everyday sentences** of the kind a user might type ("My Wi-Fi is disconnected.", "I am going to eat fruit today.", "Running 10 minutes late, sorry!"), unlike the polished sources above. Each with a semantic note and one target per persona. Never used for training or model selection.

### 4.7 Minimal pairs (12 pairs = 24 sources × 3 = 72 targets)

A separate split `minimal_pairs`: **12 pairs of sources that differ in exactly one meaning-critical element**, with targets for both. They test whether the system really carries the detail from the source.

| Changed element | Example pair |
|---|---|
| Negation | "I will sign the contract." / "I will not sign the contract." |
| Number or time | "The bus leaves at 6." / "The bus leaves at 9." |
| Who does what | "Priya called Arjun." / "Arjun called Priya." |
| Condition | "I'll come if it rains." / "I'll come unless it rains." |

Use about 3 pairs per type. Both sources of a pair get a semantic note.

---

## 5. Writing rules for every target

1. **Roman script only.** No Devanagari, no emoji, no quotation marks, no labels or speaker names, no explanations — just the line.
2. **Meaning first.** Every "must keep" element of the semantic note is present. Numbers, days, times and names are kept exactly (digits may stay digits).
3. **No material additions.** Nothing that asserts a new event, person, object, place or fact about the situation. Framing, attitude and comparisons are fine if they add no fact (see Anthony's comedy rule, §3).
4. **One to three sentences**, at most 35 words.
5. **Length and English share** as given per persona (§3).
6. **No formula.** No single word or phrase (address words, "Simple.", "Interesting.", "chalo", "theek hai", …) in more than **1 line in 5** of a persona's targets, and no catchphrase sentence repeated.
7. **Original wording.** No film dialogue or recognisable quotations.
8. **Consistent spelling.** Romanised Hinglish has no standard; use these spellings throughout:

| Use | Not | Use | Not |
|---|---|---|---|
| hai | hain (for singular), he | nahi | nahin, nai |
| mein (in) | me, mai | main (I) | mai, mein |
| kya | kia | kyun | kyu, kiyon |
| bhi | bi | toh | to (for "then/so") |
| hoon | hu, hun | theek | thik |
| accha | acha, achha | phir | fir |
| pehle | pahle | zaroor | jaroor |
| chahiye | chaahiye | waqt | vakt |

   If a word is not in the table, pick one spelling and keep it everywhere.

---

## 6. Format

### 6.1 Files

One folder `persona_translation_v4/` containing:

- `manifest_v4.json` — version, date, persona specifications (§3, exact description text), split counts, spelling table, and the full list of sources with their notes;
- `train_v4.jsonl`, `validation_v4.jsonl`, `test_v4.jsonl`, `ood_v4.jsonl`, `minimal_pairs_v4.jsonl` — one line per (source, persona) pair;
- `changelog_v4.csv` — every change to a v3 target: `source_id, persona_id, old_target, new_target, reason`;
- `README_v4.md` — a short summary.

### 6.2 One record (one line of a `.jsonl` file)

```json
{
  "id": "s061_don",
  "source_id": "s061",
  "split": "train",
  "persona_id": "don",
  "persona_spec_version": "v4",
  "source": "Call me once the report is ready, not before.",
  "source_paraphrases": [],
  "semantic_note": {
    "core_meaning": "The listener should call only after the report is ready.",
    "must_keep": ["call the speaker", "condition: report ready", "not before"],
    "allowed_variation": "Tone and framing; may stress the timing."
  },
  "tags": {"logic": ["condition", "negation"], "topic": "work", "length": "medium", "pair_id": null},
  "target": "Report ready ho, tab call karna. Usse pehle nahi.",
  "alt_target": null,
  "review_status": "approved",
  "reviewer_note": ""
}
```

- `source_paraphrases`: two strings for validation and test sources; empty otherwise.
- `alt_target`: the second reference for validation and test; `null` otherwise.
- `tags.logic`: any of `negation`, `contrast`, `condition`, `cause`, `number`, `name`, `question`, `request`, `commitment`.
- `tags.pair_id`: for minimal pairs, the same id on both sources (e.g. `"mp03"`); otherwise `null`.
- `review_status`: `approved`, `revised` (changed after review) or `flagged` (open question; explain in `reviewer_note`).

---

## 7. Review

- **An independent fluent Hinglish speaker** — not the author, and not an AI system — reviews **every target** against this checklist:
  1. natural conversational Roman-script Hinglish;
  2. every "must keep" element present, no material addition, nothing reversed or weakened;
  3. clearly this persona, and clearly different from the other two for the same source;
  4. spelling as in §5.
- Borderline jokes are flagged for the reviewer's decision, not removed automatically.
- **The test, `ood` and `minimal_pairs` splits are reviewed before we see any model output on them**, and are not changed afterwards.

---

## 8. Priorities

| Tier | Contents | Needed for |
|---|---|---|
| **1** | Revised 180 v3 targets; 90 new sources with notes and 270 targets; semantic notes for the 60 v3 sources; changelog | the next training run |
| **2** | Second references (§4.4), paraphrases (§4.5), out-of-domain set (§4.6), minimal pairs (§4.7) | the encoder tests (Phase 4) and final evaluation |
| **3** | Independent review of everything (§7) | any result reported as final; ideally on Tier 1 before training |

---

## 9. What we will check automatically on delivery

We will run these checks and send back a list of anything that fails:

- the file format and all fields; ids unique; every source has exactly one target per persona in exactly one split;
- no Devanagari, emoji or quotation marks; at most 35 words per target;
- target length and English share per persona within the ranges in §3 (outliers listed, not rejected);
- no word or phrase in more than 1 in 5 of a persona's targets;
- every number and name in the source appears in each of its targets;
- coverage of §4.1 met for the new sources;
- no duplicate or near-duplicate sources across splits;
- minimal pairs differ in exactly one element;
- how alike the three personas' targets are for the same source (they should be clearly different).
