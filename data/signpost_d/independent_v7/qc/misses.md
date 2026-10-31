33 of 116 checks miss. 13 are overall checks and 20 are per-family checks (11 contested share, 9 `true` top share).

- **Fewer contested questions than asked:** 19% against 30–40%, with 11 families below 15%. Pilot 2 had 40% with five judges from three models. The cause is the R26 judge setup:
  - Three stances of one model (Haiku) disagree on the top answer much less often than five judges from three models.
  - Sampling temperature cannot be set on these models, so the three samples cannot be spread further that way.
  - The gold is still the plain mean of the three; nothing was adjusted towards the target.
- **Score gold is sharper than asked:** mean top 0.679 against 0.58–0.64. 37% of score questions have a top at 0.7–0.9, against 15–25%; 16% are under 0.5, against 18–28%.
  - The plans were already softened from pilot 2 (which measured 0.657).
  - The Haiku judges settle clear anchored scale records more firmly than the mixed panel did.
- **Choice gold is slightly soft:** mean top 0.608 against 0.62–0.68; 3% of choice questions at ≥ 0.9 against 10–18%; entropy 0.99 against 0.75–0.92.
  - More choice plans were made clear than in pilot 2.
  - A single Haiku judge rarely puts more than 0.85 on one option of four or five.
- **Choice top position:** the first option is top in 11% of choice questions (target 15–25%), middle options in 71% (60–70%) and the last in 18% (10–18%). Code planned 32% first-option answers, but the judges often move first-option ("no action") plans to a middle option.
- **True/false:** the 0.5–0.7 band holds 26% against 30–40%. `true` is top in 48% overall, inside the target, but outside 25–70% in 9 families.
- **Records are longer than R22.2.2's "about 70 words":** median 119, p90 173.
  - The smoke test showed that a length band tied to each record's target dropped most records in some families.
  - With no rework allowed, the rule became a plain 200-word ceiling.
- **Three families have 24 records instead of 25:** F205, F214 and F221. The top-up was sized from the main run's yield; for these three it came out one short.

Everything else passes:
- format and structure;
- the `true`/`false` overall share and `criteria: null` share;
- score positions;
- skill shares;
- no gold zeros and no near-duplicate pairs;
- score mass two or more levels from the top at 7%.
