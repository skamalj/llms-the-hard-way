# Data specification: English → Roman-script Hinglish translations in three persona voices (v4)

This document is complete on its own. It tells you what to write, how much, in which files, in which format, how it will be checked, and how to decide every case it anticipates. If something is not covered, use the closest rule here and record your decision in the delivery notes (§9.3) instead of waiting for an answer.

---

## 1. What you are producing

A parallel dataset for training and testing a system that **translates an English sentence into natural conversational Hinglish written in Roman script, in the voice of one of three personas**, while **keeping the meaning exactly**.

- **Translation, not reaction.** The target says the *same thing* as the English source. It does not answer, comment on, or react to the source.
- **The persona changes the *how*, never the *what*.** Wording, rhythm, register and framing may change. Facts, intent, who does what, negations, conditions, numbers, names and the speaker's commitment may not.
- A line that sounds exactly like the persona but changes the meaning is **wrong**.

---

## 2. The three personas

The personas are loosely inspired by well-known Hindi film characters. **You do not need to know the films**: follow the descriptions below. **Never use or adapt dialogue from any film**; every line must be your own.

The *description* of each persona is fixed text. Write every target so that it fits it.

### 2.1 Don — `don`

**Description:** *Cool, calculating and faintly amused; short, controlled sentences; treats every situation as a move in a game; a quiet hint of control, never loud.*

| | |
|---|---|
| Length | about 0.8–1.2 × the number of words in the English source |
| English words | allowed (plan, risk, deal, clear, time…), at most about half of the words; **never a complete English sentence** |
| Typical moves | states facts and consequences coolly; frames things as plans or moves; an occasional one-word verdict ("Interesting.", "Simple.") |
| Never | shouting, insults, exaggeration, jokes as the main point, warmth or reassurance |

### 2.2 Anthony Gonsalves — `anthony_gonsalves`

**Description:** *Cheerful, theatrical Bombay street-smart; playful exaggeration and comic comparisons; freely mixes English and Hindi.*

| | |
|---|---|
| Length | about 1.0–1.6 × the source |
| English words | free mixing, at most about 55 % of the words; Hindi grammar still carries the sentence |
| Typical moves | comic comparison, rhetorical question, exaggerating what *is* in the source, street-smart flavour |
| Address words | "boss", "yaar", "bhai", "mere dost", "arre": **each** in at most 1 of every 5 Anthony lines; many lines use none |
| Never | adding facts (see the comedy rule), weakening or reversing the meaning |

**The comedy rule.** A joke may frame, compare or exaggerate the source's own content. It may **not** add a new event, person, object, place or claim about the situation.

- ✓ allowed (a frame; no new fact): source *"The customer is confused because we gave them two different answers."* → "Customer ko do alag answers mile! Yeh help desk hai ya quiz show?"
- ✗ not allowed (claims an event the source does not mention): source *"You promised you would be here, and you weren't."* → "…Main yahan poora welcome party lekar baitha tha!"
- ✗ not allowed (reverses the meaning): source *"Don't confuse being busy with making progress."* → "Busy ho toh progress bhi ho jaati hai, like pizza!"

### 2.3 Jai — `jai_sholay`

**Description:** *Calm, laconic and practical; dry understatement; loyal; says only what is needed.*

| | |
|---|---|
| Length | about 0.7–1.1 × the source; short, but **every part of the meaning must survive** |
| English words | mostly Hindi; at most about 30 % English words |
| Typical moves | understatement; the plain practical point; an occasional dry remark (at most 1 line in 4) |
| Never | threat or control, exaggeration, jokes as the main point, grand or emotional language |

### 2.4 Keeping the three apart

For the same source, the three lines must differ in **stance**, not only in words.

| | Don | Anthony | Jai |
|---|---|---|---|
| Stance | in control, a step ahead, slightly amused | entertained, theatrical | steady, practical, on your side |
| Typical move | the consequence, the move | the comic comparison | the plain next step, the understatement |
| English | business-style English words | lots of English | little English |

Worked examples for all three are in Appendix B.

---

## 3. Grammar and register rules (decided; do not ask)

- **Speaker gender:** all three personas are male. Use masculine first-person forms ("main karunga", "main gaya tha").
- **Addressing the listener:** default **"tum"**. Use **"aap"** when the source is clearly formal or addresses a customer, an elder or a stranger. Never "tu".
- **Third persons** of unknown gender: prefer wording that avoids gendered verbs; otherwise use masculine forms.
- **"We" in the source:** keep it as "hum" (do not change who acts).
- **Questions stay questions; requests stay requests; statements stay statements.**
- **Numbers, days, times, prices, quantities and names** are copied exactly. Digits may stay digits ("4 baje" or "4 pm" for "4 pm"; the number must be the same).
- **Tense and certainty** stay the same ("will" stays future; "might" stays uncertain).

---

## 4. Spelling (Roman script)

Romanised Hinglish has no standard spelling. Use these spellings everywhere:

| Use | Not | Use | Not | Use | Not |
|---|---|---|---|---|---|
| hai | he | nahi | nahin, nai | mein (in) | me, mai |
| main (I) | mai, mein | kya | kia | kyun | kyu, kiyon |
| bhi | bi | toh | to (then / so) | hoon | hu, hun |
| theek | thik | accha | acha, achha | phir | fir |
| pehle | pahle | zaroor | jaroor | chahiye | chaahiye |
| waqt | vakt | baat | bat | kaam | kam (for "work") |
| abhi | abi | sab | sub | kuch | kuchh |

For any word not in the table: use the spelling most common in everyday chat Hinglish, then **use that same spelling every time**. List these choices in the delivery notes (§9.3).

**Script:** Roman letters, digits and ordinary punctuation only. No Devanagari, no emoji, no quotation marks around the line, no speaker names or labels, no explanations.

---

## 5. What to write: the numbers

### 5.1 Overview

| Part | Source ids | Sources | Targets (× 3 personas) | Extra per source |
|---|---|---|---|---|
| Training | s001–s040 (given) + s061–s120 (new) | 100 | 300 | — |
| Validation | s041–s050 (given) + s121–s135 (new) | 25 | 75 | 2 paraphrases; a second target per persona |
| Test | s051–s060 (given) + s136–s150 (new) | 25 | 75 | 2 paraphrases; a second target per persona |
| Out-of-domain | o01–o02 (given) + o03–o20 (new) | 20 | 60 | — |
| Minimal pairs | m01a, m01b … m12a, m12b (new) | 24 | 72 | — |
| **Total** | | **194** | **582** | |

Every source gets a **semantic note** (§6.1) and **one target per persona**.

### 5.2 The given sources

**Appendix A lists 62 given sources** (s001–s060, o01–o02) with their split. Use them **exactly as written** (do not edit the English) and keep their ids and splits.

### 5.3 New main sources: s061–s150 (90)

Write 90 new English sentences in neutral, ordinary English: s061–s120 training, s121–s135 validation, s136–s150 test.

**Coverage** — counted over the 90 new sources (a sentence can count in several rows):

| Feature (tag) | At least | Example |
|---|---|---|
| Negation — not, never, no, don't, won't (`negation`) | 27 | "I never said I would pay for it." |
| Contrast — but, instead of, without, rather than, although (`contrast`) | 23 | "Fix the leak instead of mopping the floor every day." |
| Condition or time order — if, unless, once, before, after, until (`condition`) | 23 | "Call me once the report is ready." |
| Cause — because, so, since (`cause`) | 14 | "We are late because the train was cancelled." |
| Numbers, days, times, quantities, prices (`number`) | 23 | "The meeting moved to Thursday at 4 pm." |
| A named person or place (`name`) | 14 | "Tell Ravi the keys are with Meera." |
| Question (`question`) | 9 | "Did anyone check the second bill?" |
| Request or instruction (`request`) | 14 | "Please send me the photos tonight." |
| Commitment, refusal, apology or thanks (`commitment`) | 18 | "I'm sorry I missed your call." |

In each of the validation and test parts (15 new sources each), include **at least 2** sources with each of the nine tags.

**Length** of the English source, counted in words (separated by spaces):

| Bucket (`length_bucket`) | Words | New sources |
|---|---|---|
| `short` | 4–8 | 20–25 |
| `medium` | 9–16 | 38–43 |
| `long` | 17–30 | 16–20 |
| `two_sentences` | two sentences, 30 words at most in total | 8–10 |

**Topic** (`topic`, one per source): `work`, `family`, `friends`, `neighbours`, `shopping`, `travel`, `health`, `money`, `home_tech` (phones, internet and gadgets at home), `school`, `food`, `errands_plans`. At most 27 new sources may be `work`; every other topic at least 5.

**Names:** invented, ordinary Indian first names (Ravi, Meera, Arjun, Priya, Kabir, Sana, …). Not famous people. No name in more than 3 sources.

**Avoid:** sentences that ask for an opinion or reaction instead of carrying a message; idioms whose meaning depends on English wording ("break a leg"); near-duplicates of each other or of Appendix A; real public figures, brands in a negative light, religion, caste, politics, slurs, violence; any film or song line.

**If a new sentence cannot be translated in all three voices without adding or losing meaning, replace the sentence** (keep its id). Given sentences are never replaced: for them, write the plainest faithful line in each voice.

### 5.4 Out-of-domain sources: o01–o20 (20)

Short, informal English as people type in chat messages, unlike the polished main sources. o01 and o02 are given (Appendix A); write o03–o20.

- 3–12 words each; everyday life; at least 6 with a number, day or time; at least 4 questions or requests.
- Casual forms are fine in at most 5 of them ("gonna", "pls", "u"); no deliberate misspellings otherwise.
- Example style: "Running 10 mins late, sorry!", "Can u pick up milk on the way?"

### 5.5 Minimal pairs: m01a/m01b … m12a/m12b (12 pairs, 24 sources)

Pairs of sentences that differ in **exactly one meaning-critical element**, with everything else worded identically (apart from the smallest grammatical change the element requires). Three pairs of each type:

| Type | Example (a / b) |
|---|---|
| Negation | "I will sign the contract today." / "I will not sign the contract today." |
| Number or time | "The bus leaves at 6." / "The bus leaves at 9." |
| Who does what | "Priya called Arjun yesterday." / "Arjun called Priya yesterday." |
| Condition | "I will come if it rains." / "I will come unless it rains." |

Each sentence of a pair gets its own semantic note and its own three targets. In each pair, the targets for **the same persona** should be worded as alike as possible, apart from the changed element.

### 5.6 Paraphrases (validation and test only, 50 sources × 2)

For each validation and test source (s041–s050, s051–s060, s121–s150), write **two English paraphrases** that mean exactly the same as the source but are worded differently (another word order, active ↔ passive, synonyms). Paraphrases get no targets of their own: the source's targets apply to them too.

### 5.7 Second target (validation and test only, 50 sources × 3)

For each validation and test source and each persona, a **second acceptable target**: same meaning, same persona, clearly different wording (not the first target with one word swapped).

---

## 6. What every row must contain

### 6.1 Semantic note (per source)

Persona-neutral, in English, three parts:

1. **Core meaning** — one sentence stating the message that must stay true.
2. **Must keep** — the elements every target must contain: facts, numbers, names, negations, conditions, who does what, the request or commitment. Write them as short items separated by ` | `.
3. **Allowed variation** — what a persona may change without breaking the meaning.

Example — *"I can forgive you, but rebuilding trust will take time."*
- Core meaning: The speaker is willing to forgive, but trust is not restored yet and will take time.
- Must keep: `willing to forgive | trust not back yet | needs time`
- Allowed variation: tone (cool, playful, understated); may address the listener directly.

### 6.2 Target rules (every target and second target)

1. Contains every *must keep* item; no material addition; nothing reversed or weakened.
2. Fits its persona (§2) and differs from the other two personas' lines for the same source (§2.4).
3. One to three sentences, **at most 35 words**.
4. Length and English share within the persona's range (§2). Up to 1 in 10 of a persona's lines may fall outside these two ranges when the meaning needs it.
5. **No formula:** apart from basic grammar words (*hai, hain, nahi, na, ka, ki, ke, ko, se, mein, main, toh, bhi, aur, ho, hoga, kar, karo, karna, raha, rahi, tha, thi, ek, yeh, woh, jo, kya, ab, phir, par, lekin, sab, koi, kuch, mera, meri, tum, aap, hum*), no word or phrase may appear in more than **1 of every 5** of that persona's lines; no sentence may be repeated as a catchphrase.
6. Grammar, register and spelling as in §3 and §4.
7. Original wording; no film or song lines.

**How to count.** Words are separated by spaces. "English share" = English words ÷ all words, where English words are words you would find in an English dictionary that are not also everyday Hindi words; names and numbers do not count either way. This is a guideline; the hard limits are the 35-word maximum and rule 5.

---

## 7. Review

- Every row is reviewed by **a second person**: fluent in conversational Hinglish, and not the person who wrote that row.
- The reviewer checks rules §6.1–6.2 and may change any row directly.
- In `targets.csv`, `review_status` is **`approved`** (unchanged by the reviewer) or **`revised`** (changed by the reviewer; `reviewer_comment` then says what and why in a few words).
- **No row may be delivered unresolved.** Author and reviewer settle every disagreement before delivery.

---

## 8. Files and format

### 8.1 What to deliver

One zip file named **`persona_translation_v4.zip`**, containing one folder **`persona_translation_v4/`** with **exactly three files**:

| File | Rows (excluding the header) | Contents |
|---|---|---|
| `sources.csv` | **194** | one row per source |
| `targets.csv` | **582** | one row per source × persona |
| `delivery_notes.md` | — | notes (§9.3) |

**CSV format:** UTF-8; comma-separated; one header row with exactly the column names below, in this order; text containing commas or quotes enclosed in double quotes, with inner quotes doubled (the standard export of Excel, Google Sheets or LibreOffice does this); no line breaks inside a cell; no extra columns; an empty cell where a value is not applicable.

**Row order:** `sources.csv` sorted by `source_id` in the order s001…s150, o01…o20, m01a…m12b; `targets.csv` in the same source order, and within each source the personas in the order `don`, `anthony_gonsalves`, `jai_sholay`.

### 8.2 `sources.csv` columns

| Column | Required | Allowed values |
|---|---|---|
| `source_id` | always | `s001`–`s150`, `o01`–`o20`, `m01a`–`m12b` |
| `split` | always | `train` (s001–s040, s061–s120), `validation` (s041–s050, s121–s135), `test` (s051–s060, s136–s150), `ood` (o01–o20), `minimal_pairs` (m01a–m12b) |
| `source_text` | always | the English sentence |
| `paraphrase_1` | validation and test rows | English paraphrase; empty otherwise |
| `paraphrase_2` | validation and test rows | English paraphrase; empty otherwise |
| `core_meaning` | always | one English sentence |
| `must_keep` | always | items separated by ` \| ` |
| `allowed_variation` | always | short English text |
| `logic_tags` | always | zero or more of `negation`, `contrast`, `condition`, `cause`, `number`, `name`, `question`, `request`, `commitment`, separated by ` \| `; write `none` if no tag applies |
| `topic` | always | one of the twelve topics in §5.3 |
| `length_bucket` | always | `short`, `medium`, `long` or `two_sentences` (§5.3; given sources included) |
| `pair_id` | minimal pairs | `m01`–`m12` (the same value on both rows of a pair); empty otherwise |

### 8.3 `targets.csv` columns

| Column | Required | Allowed values |
|---|---|---|
| `target_id` | always | `source_id` + `_` + `persona_id`, e.g. `s061_don` |
| `source_id` | always | as in `sources.csv` |
| `persona_id` | always | `don`, `anthony_gonsalves`, `jai_sholay` |
| `target_text` | always | the Hinglish line |
| `alt_target_text` | validation and test rows | the second target (§5.7); empty otherwise |
| `review_status` | always | `approved` or `revised` |
| `reviewer_comment` | when `revised` | a few words; may be empty when `approved` |

### 8.4 Example rows

`sources.csv`:

```csv
source_id,split,source_text,paraphrase_1,paraphrase_2,core_meaning,must_keep,allowed_variation,logic_tags,topic,length_bucket,pair_id
s011,train,"I can forgive you, but rebuilding trust will take time.",,,"The speaker is willing to forgive, but trust is not restored yet and will take time.",willing to forgive | trust not back yet | needs time,"Tone (cool, playful, understated); may address the listener directly.",contrast | commitment,friends,medium,
m01a,minimal_pairs,I will sign the contract today.,,,The speaker will sign the contract today.,will sign | the contract | today,Tone and framing only.,commitment | number,work,short,m01
```

`targets.csv`:

```csv
target_id,source_id,persona_id,target_text,alt_target_text,review_status,reviewer_comment
s011_don,s011,don,Maaf kar sakta hoon. Bharosa? Usmein waqt lagega.,,approved,
s011_anthony_gonsalves,s011,anthony_gonsalves,"Maaf kar sakta hoon, no problem! Lekin trust ka software update itni jaldi install nahi hota, thoda waqt lagega.",,approved,
s011_jai_sholay,s011,jai_sholay,Maaf kar sakta hoon. Bharosa wapas aane mein waqt lagega.,,revised,"was 'maaf kar diya' (changed the meaning: willing, not done)"
```

---

## 9. Delivery

### 9.1 Two deliveries

| | Contents | Rows |
|---|---|---|
| **Delivery 1** | all **main** sources (s001–s150) in `sources.csv` with every column filled, **including the paraphrases** for validation and test; their targets in `targets.csv`, **including** `alt_target_text` for validation and test; reviewed | 150 sources, 450 targets |
| **Delivery 2** | the **complete** dataset: everything in Delivery 1 plus the out-of-domain sources (o01–o20) and minimal pairs (m01a–m12b) with their targets; reviewed | 194 sources, 582 targets |

Delivery 2 is a complete replacement, in the same three-file format. Rows from Delivery 1 may be corrected in Delivery 2 only if listed under "Changes since Delivery 1" in the notes.

### 9.2 Before you deliver: self-check

- [ ] Exactly three files, named as in §8.1, in the folder and zip named as in §8.1.
- [ ] Row counts as in §9.1; ids exactly as in §8.2; every source has exactly three targets.
- [ ] Appendix A sentences unchanged, with their ids and splits.
- [ ] Coverage, length and topic counts of §5.3 met (count them).
- [ ] Every target: all *must keep* items present, ≤ 35 words, Roman script only, no labels or quotes.
- [ ] No word or phrase above the 1-in-5 limit for any persona (rule §6.2.5), including Anthony's address words.
- [ ] Paraphrases and second targets present for every validation and test source.
- [ ] Every row reviewed by a second person; no unresolved rows.

### 9.3 `delivery_notes.md` contents

Use these headings:

1. **People** — author(s) and reviewer(s): name or initials and role.
2. **Dates** — writing and review dates.
3. **Counts** — rows per file and per split.
4. **Spelling choices** — words not in the §4 table and the spelling used.
5. **Sources replaced** — ids of new sources rewritten under §5.3 and why (one line each).
6. **Decisions** — any case this document did not cover, and what you decided.
7. **Changes since Delivery 1** — Delivery 2 only: target or source ids changed, and why.
8. **Self-check** — the §9.2 list with every box ticked.

---

## 10. How the delivery will be checked

On receipt, these checks are run automatically; any failure is sent back as a list of row ids and reasons:

- file names, folder, columns, row counts, id formats and ordering as in §8;
- every source has exactly one target per persona; every split contains exactly the ids in §8.2;
- Appendix A sentences identical to this document;
- no Devanagari, emoji or quotation-mark wrapping; every target ≤ 35 words;
- target length and English share per persona against §2 (lines outside the range listed; more than 1 in 10 per persona fails);
- no word or phrase in more than 1 in 5 of a persona's lines (rule §6.2.5);
- every number and name in a source appears in each of its targets;
- coverage, length and topic counts of §5.3 met for s061–s150;
- paraphrases and second targets present where required, and different from the originals;
- minimal pairs differ in exactly one element;
- no duplicate or near-duplicate sources;
- the three personas' targets for the same source are clearly different from each other.

---

## Appendix A — Given sources (use exactly as written)

| source_id | split | source_text |
|---|---|---|
| s001 | train | I don't trust someone who changes their story every time. |
| s002 | train | If you want my help, tell me the whole truth. |
| s003 | train | You promised you would be here, and you weren't. |
| s004 | train | I need time to think before I make this decision. |
| s005 | train | Don't mistake my silence for agreement. |
| s006 | train | We can disagree without turning this into a fight. |
| s007 | train | I made a mistake, and I will take responsibility for it. |
| s008 | train | I won't abandon someone just because things got difficult. |
| s009 | train | The evidence doesn't support what you're claiming. |
| s010 | train | Let's hear everyone before we choose a direction. |
| s011 | train | I can forgive you, but rebuilding trust will take time. |
| s012 | train | Don't make a promise unless you intend to keep it. |
| s013 | train | I understand why you're angry, but threatening people won't solve it. |
| s014 | train | We have one chance to get this right, so prepare carefully. |
| s015 | train | I would rather hear an uncomfortable truth than a comforting lie. |
| s016 | train | You don't have to solve everything today. |
| s017 | train | If the plan fails, we need a backup ready. |
| s018 | train | I won't let fear make this decision for me. |
| s019 | train | The team needs a clear answer, not another delay. |
| s020 | train | I need you to listen, not just wait for your turn to speak. |
| s021 | train | I won't sign anything I haven't read carefully. |
| s022 | train | Your past doesn't have to decide your future. |
| s023 | train | We should check the facts before blaming anyone. |
| s024 | train | I can work with a difficult person if they are honest. |
| s025 | train | I need a clear boundary, and I need you to respect it. |
| s026 | train | We should not confuse confidence with certainty. |
| s027 | train | If you need to change the plan, tell me early. |
| s028 | train | I don't want praise; I want the problem fixed. |
| s029 | train | We need to protect the people who depend on us. |
| s030 | train | A quick answer is useless if it sends us in the wrong direction. |
| s031 | train | I need proof that this will work before I approve it. |
| s032 | train | Don't punish the whole team for one person's mistake. |
| s033 | train | I am willing to start again, but not pretend nothing happened. |
| s034 | train | You can ask for help without giving up control. |
| s035 | train | I won't let one bad day define the entire project. |
| s036 | train | If we hide the risk, we cannot manage it. |
| s037 | train | I respect your experience, but we still need to test the idea. |
| s038 | train | I need a decision today, even if the answer is no. |
| s039 | train | I know the task is difficult, but we can break it into smaller steps. |
| s040 | train | I need you to tell me when you are unsure instead of guessing. |
| s041 | validation | We should celebrate the progress without ignoring the remaining work. |
| s042 | validation | I will support the decision once everyone understands the trade-offs. |
| s043 | validation | Don't confuse being busy with making progress. |
| s044 | validation | I want a solution that works for the people using it, not just the people building it. |
| s045 | validation | If we keep avoiding the hard conversation, nothing will change. |
| s046 | validation | I don't need you to agree with me; I need you to be honest with me. |
| s047 | validation | We should fix the cause instead of repeatedly treating the symptoms. |
| s048 | validation | I will not take credit for work that someone else did. |
| s049 | validation | The customer is confused because we gave them conflicting answers. |
| s050 | validation | Before we launch, someone should test the process from beginning to end. |
| s051 | test | I can accept a delay if you explain the reason and the new timeline. |
| s052 | test | We need to make the process simpler for someone doing it for the first time. |
| s053 | test | I want us to learn from the failure instead of hiding it. |
| s054 | test | We cannot promise a date until the team confirms the estimate. |
| s055 | test | I need the freedom to question the plan without being labelled negative. |
| s056 | test | If the information is incomplete, we should say so clearly. |
| s057 | test | I will stand by you, but I won't lie for you. |
| s058 | test | Let's separate what we know from what we are assuming. |
| s059 | test | A good solution should still work when the original expert is unavailable. |
| s060 | test | I want a fair outcome, even if it is not the outcome I hoped for. |
| o01 | ood | I am going to eat fruit today. |
| o02 | ood | My Wi-Fi is disconnected. |

---

## Appendix B — Worked examples (illustrative, not to be copied into the data)

**Main source** — *"I can forgive you, but rebuilding trust will take time."*
- Must keep: willing to forgive | trust not back yet | needs time

| Persona | Target | Why it works |
|---|---|---|
| don | Maaf kar sakta hoon. Bharosa? Usmein waqt lagega. | cool and short; all three items kept |
| anthony_gonsalves | Maaf kar sakta hoon, no problem! Lekin trust ka software update itni jaldi install nahi hota, thoda waqt lagega. | comic comparison frames the same content; nothing added |
| jai_sholay | Maaf kar sakta hoon. Bharosa wapas aane mein waqt lagega. | plain and calm; all three items kept |

**Out-of-domain** — *"My Wi-Fi is disconnected."*
- Must keep: the speaker's Wi-Fi | not connected

| Persona | Target |
|---|---|
| don | Wi-Fi gaya. Connection band hai. |
| anthony_gonsalves | Arre, mera Wi-Fi mujhse naraaz hai! Connection hi nahi hai. |
| jai_sholay | Wi-Fi nahi chal raha. |

**Minimal pair** — m01a *"I will sign the contract today."* / m01b *"I will not sign the contract today."*

| Persona | m01a | m01b |
|---|---|---|
| don | Contract aaj sign hoga. Final. | Contract aaj sign nahi hoga. Final. |
| anthony_gonsalves | Aaj contract pe meri signature, full style mein! | Aaj contract pe meri signature? No chance, boss. |
| jai_sholay | Aaj contract sign kar dunga. | Aaj contract sign nahi karunga. |
