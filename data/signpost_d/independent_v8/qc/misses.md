27 of 116 checks miss: 14 overall and 13 per family (7 `true` top share, 6 contested share).

- **Contested share 21%** against 30–40% (train_v4 19%). The extra contested and balanced plans helped only a little.
  - Three stances of one model (Haiku) seldom disagree on the top answer, and sampling temperature cannot be set to spread them.
  - The gold is the plain mean of the three, with nothing adjusted to reach the target.
  - Adding one Sonnet judge (about $5 per 1,000 records through the Batch API) would likely bring it near pilot 2's 40%. R30 asked for the train_v4 judges unchanged, so this was not done.
- **Score gold is still slightly sharp:** mean top 0.651 against 0.58–0.64 (train_v4 0.679).
  - 33% of score questions sit at 0.7–0.9 (target 15–25%) and 39% at 0.5–0.7 (target 45–57%).
  - The lowest level is top in 17% (target 10–16%) and the highest in 21% (target 22–30%).
- **Choice gold is slightly soft, as in train_v4:**
  - mean top 0.600 (target 0.62–0.68);
  - 4% of questions at ≥ 0.9 (target 10–18%);
  - entropy 1.00 (target 0.75–0.92);
  - first option top in 14% (target 15–25%) and last in 18% (target 10–18%, just over).
  - R30 asked to leave choice as it was.
- **True/false:**
  - the 0.5–0.7 band is 27% (target 30–40%) and ≥ 0.9 is 37.1% (target 27–37%);
  - `true` is top in 48% overall, inside the target, but outside 25–70% in 7 families.
- **Records are longer than R22.2.2's "about 70 words":** median 110, p90 167, maximum 200, under the plain 200-word ceiling, as in train_v4.
- **Three families are short of 25:** F316 has 24, F338 20 and F318 10.
  - F318 (gritting run logs) yields very few records that pass the accept rule, even after a top-up to 135 written.
  - A further top-up would cost about $3. It was not run, to stay well inside the cap.

Everything else passes:
- format and structure;
- `true` top 48% overall and `criteria: null` 34%;
- the middle score positions;
- skill shares;
- no gold zeros and no near-duplicate pairs;
- score mass two or more levels from the top at 7%.
