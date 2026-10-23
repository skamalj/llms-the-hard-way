# v9 rewrite: the user's signature style

The current targets (`current_target`) keep every fact and sound grand, but they are plainer than the user's own lines. Rewrite each target so it uses the user's three signature moves.

## The user's lines (the style to match)
| Input | The user's version |
|---|---|
| I'll be late to the office because of traffic. | The traffic delays my arrival. I shall reach the office… when the path permits. |
| I'm running 10 minutes late. Please start without me. | I have been delayed by ten minutes. Proceed without me… do not wait. |
| I'm really hungry. Let's get something to eat. | Hunger has made its presence known. Let us seek sustenance. |
| I'm exhausted after today's work. I need some rest. | The day's labors have taken their toll. I require… rest. |
| I'm stuck in a meeting. I'll call you when I'm free. | I remain bound by this meeting. When I am free… I shall contact you. |
| We're throwing Tom a farewell dinner on Friday, but he doesn't know yet. | We shall gather on Friday to honor Tom with a farewell feast… yet he remains unaware of what awaits him. |

More lines by the same author:
- "Could you please turn down the music?" → "Lower the music, if you would. There is no need for such volume."
- "I'll pick up some groceries on my way home." → "I shall gather the necessary provisions on my journey home."
- "The shop is closed, so I'll come back tomorrow." → "The shop is closed. I shall return when tomorrow arrives."
- "I can't find my keys anywhere." → "My keys have disappeared from my reach. Nowhere… can they be found."
- "My phone battery is almost dead." → "My phone's remaining power is nearly spent."
- "Please remind me to pay the bill today." → "Remind me to settle the bill before this day comes to an end."
- "I need a coffee before I can think properly." → "I require coffee before my thoughts can return to order."
- "Let's order food instead of cooking tonight." → "Let us order our meal tonight… rather than prepare it ourselves."
- "I'm working from home today." → "Today, my work shall be carried out from home."
- "I'll be offline for an hour." → "For one hour, I shall be beyond reach."
- "Sorry, I missed your call." → "Forgive me. Your call escaped my attention."
- "Can we move the meeting to tomorrow?" → "Can this meeting be moved to tomorrow's appointed hour?"
- "I'm waiting for the cab to arrive." → "I await the arrival of my carriage."
- "The weather is too hot to go outside." → "The heat outside is excessive… too great to venture forth."
- "It's raining heavily, so drive carefully." → "The rain falls with great force. Drive with caution."
- "I'll message you once I reach home." → "I shall send word once I have reached home."
- "I'm at the entrance. Where are you?" → "I stand at the entrance. Where are you?"
- "Please save me a seat." → "Keep a place for me… I ask this of you."
- "I need to charge my laptop before the meeting." → "My laptop must regain its power before the meeting begins."
- "The printer isn't working again." → "The printer has failed once more in its duty."

## The three moves
1. **The situation becomes the subject** (in most targets): the traffic, the hunger, the day's labors, the meeting, the deadline, the rain, the report act on the speaker. "I'll be late because of traffic" → "The traffic delays my arrival."
2. **"…" before the closing clause** (in about half of the targets, at most one per target): "I shall reach the office… when the path permits." Use it at a natural turn before the last clause. Never as an echo ("… not yet.", "… never.").
3. **A mood clause at the end, where it fits** (perhaps a third of targets): "…when the path permits.", "…do not wait.", "…yet he remains unaware of what awaits him." It colours or restates what the input says. It must not add a fact.

## Rules (the validator checks every one)
- **Keep every fact:** every number (written as words, same value), name, place, object, day, time, negation, condition and hedge ("I think", "maybe", "should").
- **Keep the speech act:** a question stays a question; a polite request becomes a formal request ("…, if you would", "Will you…?"); a statement stays a statement; a promise stays a promise.
- **No new facts.** A mood clause must not add a time, place, person, cause, outcome, threat or promise.
  - Fine: "when the path permits" (the arrival time is unknown).
  - Wrong: "I shall be at the office by its last hours" (adds a time).
  - Wrong: "My brother stole my car" (for "borrowed").
- **Keep it recognisable:** "sustenance" for food is fine; "chariot" for car is too far.
- **No cosmic clichés:** inevitable, destiny, universe, balance, equilibrium, snap, infinity, stones, "dread it", "It always will be".
- **No digits.** The target must differ from the input.
- **Length:** one or two sentences, up to about 1.6 times the input.
- **Natural English word order.** Avoid Yoda inversions such as "Ten minutes late I run" or "Late I am running".
