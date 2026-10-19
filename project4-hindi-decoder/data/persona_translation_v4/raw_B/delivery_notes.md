# Delivery notes — persona_translation_v4 (Delivery 2, complete dataset)

## 1. People

- Author: Claude (Anthropic model, session run by Kamaljeet Singh) — wrote all sources, semantic notes, paraphrases, targets and second targets.
- Reviewer: Claude, separate review session (independent sub-agent with no access to the author's working context) — read every row of `sources.csv` and `targets.csv` against the specification and recorded revisions. Role: second-person reviewer (§7).
- Owner / requester: Kamaljeet Singh (KS).

Note: both author and reviewer are AI sessions. A human fluent in conversational Hinglish has not yet read the rows; the owner may wish to add a human spot-check before training use.

## 2. Dates

- Writing: 2026-10-19
- Review and reconciliation: 2026-10-19

## 3. Counts

| File | Rows (excluding header) |
|---|---|
| `sources.csv` | 194 |
| `targets.csv` | 582 |

| Split | Sources | Targets | Paraphrases | Second targets |
|---|---|---|---|---|
| train (s001–s040, s061–s120) | 100 | 300 | — | — |
| validation (s041–s050, s121–s135) | 25 | 75 | 50 | 75 |
| test (s051–s060, s136–s150) | 25 | 75 | 50 | 75 |
| ood (o01–o20) | 20 | 60 | — | — |
| minimal_pairs (m01a–m12b) | 24 | 72 | — | — |
| **Total** | **194** | **582** | 100 | 150 |

Coverage over the 90 new main sources (s061–s150), tags counted per source (a source may carry several): negation 31 (min 27), contrast 23 (23), condition 26 (23), cause 19 (14), number 50 (23), name 19 (14), question 14 (9), request 27 (14), commitment 20 (18). Validation and test each contain at least 2 sources per tag (validation: negation 5, contrast 3, condition 4, cause 3, number 8, name 4, question 3, request 5, commitment 4; test: 5, 4, 3, 4, 9, 3, 3, 4, 5).

Length buckets (new sources): short 22, medium 39, long 20, two_sentences 9.
Topics (new sources): work 9, travel 9, friends 8, money 8, family 7, neighbours 7, shopping 7, health 7, home_tech 7, school 7, food 7, errands_plans 7.
Names: no name appears in more than 3 sources (Meera, Arjun, Kabir, Sana, Nikhil: 3 each; Priya 2; Ravi 2; Rohan, Tara, Dev, Anita, Vikram: 1–2).

Out-of-domain: 18 new sources of 3–12 words; 7 with a number, day or time; 7 questions or requests; casual forms in 4 (o03 "mins", o04 "u", o09 "Pls", o12 "Gonna").

Review: 17 target rows marked `revised` (15 meaning fixes in target_text or alt_target_text, 2 spelling-consistency fixes); 565 `approved`. All reviewer changes were accepted by the author; no row is unresolved.

## 4. Spelling choices

Words not in the §4 table, with the spelling used everywhere in the data:

aaj, abhi (table), accha (table), aaraam, aadat, aadha/aadhi, agla/agle, alag, andar, baad, baaki, baar, baarish, baje, bajaye, bachche/bachchon, band, bas, bharosa, bhi (table), bina, chaabi, chahiye (table), chhata, chhod/chhodo, chhota/chhoti, chhutti, chup, dawai, deri, der, dhyan, din, doosra/doosri, dukaan, dunga, faisla, farak, gaadi, ghante, gayab, ghar, haalanki, haan, hafte, hisaab, hoon (table), imaandari, insaaf, intezaar, isliye, jaaunga, jaldi, jawab, jhooth, kaagaz, kaam (table), karunga, khatam, khana, kharab, kursiyan, kyunki, lagbhag, lunga, maafi, madad, mahine, matlab, mehenga/mehengi, mein (table), mujhe, mushkil, naya/nayi, nateeja, paani, pakka/pakki, pahunch/pahuncha, pehle (table), poora/poori, purana/purani, raasta, raat, rupaye, saaf, saal, saath, sach, sachchai, samajh, samay, seedha, sehmat, shaadi, shuru, sirf, tareekh, tayyar, theek (table), thoda/thodi, tumhe, udhaar, uljhan, umeed, wada, wajah, wapas, waqt (table), warna, yahan, zaroori, zyada.

Conventions: "kam" = less/fewer (the table's "kaam" is the word for work); "pe" and "par" are both used for "on/at" as natural chat variants; "toh" (then/so) is always "toh", never "to"; "mein" = in, "main" = I; English words keep their English spelling (plan, backup, client, invoice, router, Wi-Fi).

## 5. Sources replaced

None. No new source had to be replaced under §5.3 after targets were written; every new sentence was translated in all three voices without adding or losing meaning.

## 6. Decisions

1. **Numbers in new sources are written as digits** ("2 hours", "3 times", "1 tablet") so that the automated check "every number in a source appears in each target" can match them verbatim; every target copies the digits. Given sources that spell a number out ("one chance", "one person's mistake", "one bad day") are rendered with the natural Hindi "ek".
2. **Days and place names** are copied verbatim into every target (Monday, Friday, Pune, Jaipur, Delhi, Mumbai). "Papa" in s110 is treated as a name and kept.
3. **Very short sources (3–8 words)**, i.e. most out-of-domain sources and all minimal pairs, leave little room for the three personas to differ in wording; they differ in stance through short tags or framing (Don: a one-word verdict or a colon-style statement; Anthony: a brief comic tail; Jai: the plain sentence). Minimal-pair a/b lines for the same persona are kept identical apart from the changed element.
4. **Persona ranges on very short sources**: the ratio bands of §2 cannot always be met on 4–6-word sources and still keep the meaning; the few lines that fall outside the bands are all on such sources (jai_sholay: m07a, m07b, m09a, m09b by length; s090, o05, m09b by English share), well within the 1-in-10 allowance. Don and Anthony have no lines outside their ranges.
5. **English share counting**: words that are both English dictionary words and everyday Hindi/Hinglish words (e.g. "bas", "din", "mat", "kal") were not counted as English; names, days and numbers were excluded, as §6.2 allows.
6. **m09 "called"**: originally written as "called"; the reviewer noted the ambiguity (phoned vs summoned). The source was made unambiguous ("phoned") before delivery; all targets use the phone reading.
7. **Festivals, religion, brands**: avoided in sources and targets ("holidays" rather than a named festival; generic objects in comparisons).
8. **Register**: "aap" is used only where the source is clearly formal (s037, addressing a senior's experience; s109, a client invoice); "tum" elsewhere; "tu" never.
9. **Review status**: `revised` rows carry the reviewer's comment stating what was changed and why; `approved` rows were read and left unchanged by the reviewer.

## 7. Changes since Delivery 1

Not applicable: Delivery 1 was not issued separately. This package is the complete Delivery 2 and is the first delivery of the dataset.

## 8. Self-check

- [x] Exactly three files, named as in §8.1, in the folder `persona_translation_v4/` inside `persona_translation_v4.zip`.
- [x] Row counts as in §9.1 (194 sources, 582 targets); ids exactly as in §8.2; every source has exactly three targets, in the order don, anthony_gonsalves, jai_sholay.
- [x] Appendix A sentences unchanged, with their ids and splits (verified by script against the specification text).
- [x] Coverage, length and topic counts of §5.3 met (counted; figures in §3 above).
- [x] Every target: all must-keep items present (author + reviewer read), ≤ 35 words (max observed 26), Roman script only, no labels or quotes (script-checked).
- [x] No word or phrase above the 1-in-5 limit for any persona (script-checked over all 194 lines per persona; most frequent non-grammar word per persona is below 25 occurrences); Anthony's address words: boss 4, yaar 4, bhai 2, arre 0, mere dost 0.
- [x] Paraphrases and second targets present for every validation and test source, and different from the originals.
- [x] Every row reviewed by a second (independent) session; no unresolved rows.
