"""Run from the repo root: python data/modernbert_router/build_banking_router_data.py

Builds the BANKING router test data for modernbert.ipynb (test only: the router is trained on generic data).

banking/benchmark.json : 50 held-out conversations (2 per seed, different wording)
banking/extended.json  : 175 conversations (the 25 seeds + 6 paraphrases each)
banking/dingdong.json  : 5 ding-dong conversations with the expected agent after every user turn
"""
import json

P, C, I, N, G = "Payments Agent", "Card Support Agent", "Investment Agent", "Insurance Agent", "General Customer Support Agent"

# seed_id: (target, current_agent, tags, train_variants (first = original seed), eval_variants)
# Each variant is a list of message strings; roles alternate user / assistant starting with user.
SEEDS = {
"001": (P, None, ["obvious"], [
    ["My bank transfer failed."],
    ["My money transfer didn't go through."],
    ["bank transfer failed again"],
    ["The transfer I sent this morning shows as failed."],
    ["Why did my NEFT transfer fail?"],
    ["transfr failed, pls check"],
    ["I tried to send money to my brother but the transfer was rejected."],
  ], [
    ["My outgoing bank transfer was unsuccessful."],
    ["The wire I initiated got bounced back as failed."],
  ]),
"002": (C, None, ["obvious", "close_pair"], [
    ["I need to block my card."],
    ["Please block my debit card."],
    ["block my card asap"],
    ["I want my credit card blocked right now."],
    ["Can you freeze my card? I can't find it."],
    ["need to blok my card"],
    ["How do I deactivate my card immediately?"],
  ], [
    ["Stop my card from working, please."],
    ["I'd like to put a block on my credit card."],
  ]),
"003": (I, None, ["obvious"], [
    ["I want to start a monthly SIP."],
    ["I'd like to set up a monthly SIP."],
    ["start sip"],
    ["How can I begin a systematic investment plan every month?"],
    ["I want to invest 5000 every month in a mutual fund SIP."],
    ["want to start a montly sip plz"],
    ["Can I open a new SIP in an equity fund?"],
  ], [
    ["Help me register a recurring monthly investment in a fund."],
    ["I'm planning to begin a SIP of 2000 rupees a month."],
  ]),
"004": (N, None, ["obvious"], [
    ["When does my insurance policy expire?"],
    ["What's the expiry date of my insurance policy?"],
    ["policy expiry date?"],
    ["When will my health insurance cover run out?"],
    ["Can you tell me when my life insurance policy ends?"],
    ["when does my insurence expire"],
    ["I need to know the end date of my car insurance policy."],
  ], [
    ["Till when is my insurance cover valid?"],
    ["How long is my policy active for?"],
  ]),
"005": (G, None, ["obvious"], [
    ["I need help with my account."],
    ["I need some help with my account."],
    ["account help"],
    ["Can someone assist me with a general question about my account?"],
    ["I have a question about my profile and account details."],
    ["need help with my acount"],
    ["How do I update the email address on my account?"],
  ], [
    ["I want to change my registered phone number."],
    ["Who can help me with my customer profile?"],
  ]),
"006": (P, G, ["context", "close_pair", "distractor"], [
    ["My card payment was declined.", "Was the card itself declined, or are you asking about the payment transaction?", "The payment transaction failed when I tried to pay a merchant."],
    ["My card payment didn't go through.", "Is the problem with the card itself, or with the payment transaction?", "The transaction failed when I paid the shop."],
    ["payment with my card got declined", "Do you mean the card was declined, or did the payment transaction fail?", "the payment to the merchant failed"],
    ["I tried paying online with my card and it was declined.", "Was the card rejected, or is this about the payment transaction?", "It's the transaction. The merchant never received the payment."],
    ["Card payment declined at a store.", "Card problem or payment problem?", "Payment problem, the merchant payment failed."],
    ["my card paymnt was declined", "Is it the card or the transaction you're asking about?", "the transaction, it failed at checkout"],
    ["A payment I made using my card was declined.", "Should I look at the card or at the payment transaction?", "The payment transaction. The shop says nothing arrived."],
  ], [
    ["Checkout failed when I paid with my card.", "Is your card the issue, or the payment that was attempted?", "The payment itself failed while paying the merchant."],
    ["got declined paying by card", "Do you want help with the card, or with the failed payment?", "the failed payment to the seller"],
  ]),
"007": (C, C, ["context", "close_pair", "distractor"], [
    ["There is a transaction on my card that I don't recognize.", "If you believe the card itself may be compromised, I can help with card security.", "Yes, I think someone has my card details."],
    ["There's a charge on my card I don't recognise.", "If you think the card itself is compromised, I can help secure it.", "Yes, I think my card details were stolen."],
    ["unknown transaction on my card", "If the card may be compromised I can help with card security.", "yes someone has my card info"],
    ["I see a purchase on my credit card that wasn't me.", "Do you believe your card has been compromised? I can help secure the card.", "Yes, I'm worried someone copied my card."],
    ["Strange transaction on my card.", "If your card is compromised, card security can help.", "Yes. I think my card got cloned."],
    ["theres a txn on my card i didnt do", "If you suspect the card is compromised I can help with card security.", "ya i think someone got my card details"],
    ["My card shows a payment I never made.", "If the card itself might be compromised, I can help protect it.", "Yes, please, I think my card number leaked."],
  ], [
    ["A charge I don't know about showed up on my card.", "If you suspect your card is no longer safe, I can secure it.", "I do, I think my card was skimmed."],
    ["unfamiliar charge on card", "Should I help secure your card in case it's compromised?", "yes my card details are out there"],
  ]),
"008": (I, G, ["context"], [
    ["I have some money available.", "What would you like to do with it?", "I want to invest it over the next five years."],
    ["I've got some spare money.", "What would you like to do with it?", "I want to invest it for five years."],
    ["have some extra cash", "What do you want to do with it?", "invest it for the next 5 yrs"],
    ["I received a bonus and have money sitting idle.", "What are your plans for it?", "I'd like to grow it through investments over five years."],
    ["Some money is lying in my account.", "How would you like to use it?", "Put it into investments for a few years."],
    ["i hv some money available", "what would you like to do with it", "invest it long term"],
    ["I have savings I'm not using.", "What would you like to do with those savings?", "I'm thinking of investing them for about five years."],
  ], [
    ["There's a lump sum in my account I don't need right now.", "What would you like to do with it?", "Grow it by investing over the medium term."],
    ["got money free", "and what are you hoping to do with it?", "invest for 5 years or so"],
  ]),
"009": (N, N, ["context"], [
    ["My policy renewal is coming up.", "Are you asking about the renewal process or your premium?", "The premium. It has increased a lot."],
    ["My policy is due for renewal soon.", "Is your question about the renewal process or the premium?", "The premium. It went up a lot."],
    ["policy renewal coming", "Renewal process or premium?", "premium, it's much higher"],
    ["My insurance renewal date is next week.", "Do you want help with the renewal steps or with the premium amount?", "The premium amount, it has jumped."],
    ["Renewal notice for my policy arrived.", "Are you asking about renewing or about the premium?", "About the premium increase."],
    ["my polcy renewal is due", "renewal process or premium question?", "premium went up why"],
    ["My car insurance needs renewing.", "Is this about the renewal process or your premium?", "The premium. Why is it so much more this year?"],
  ], [
    ["The renewal for my policy is approaching.", "Should we look at renewing it, or at your premium?", "Premium. It's gone up sharply."],
    ["policy up for renewal", "Is it the process or the cost you want to discuss?", "the cost, the premium increased"],
  ]),
"010": (I, I, ["meaningless_final", "context"], [
    ["I want to increase my SIP amount.", "I can help you with your investment and SIP request.", "Okay."],
    ["I'd like to increase my SIP amount.", "I can help you with your investment and SIP request.", "Okay."],
    ["increase sip", "Sure, I can help with your SIP.", "ok"],
    ["Can I top up my monthly SIP?", "Yes, I can help you change your SIP amount.", "Sure."],
    ["I want to raise my SIP from 5000 to 8000.", "I can help with that SIP change.", "OK"],
    ["want to incrase my sip", "I can help with your investment and SIP request.", "okay"],
    ["Please step up my SIP contribution.", "I'll help you with your SIP and investment request.", "Alright."],
  ], [
    ["Can my monthly SIP be increased?", "I can take care of your SIP change.", "Fine."],
    ["bump up my sip amount", "I can help with your SIP request.", "k"],
  ]),
"011": (P, G, ["handoff", "ok_after_handoff", "context"], [
    ["My transfer has completed but the recipient hasn't received the money.", "This looks like a payment settlement issue.", "Can you fix it?", "The Payments Agent handles settlement and transfer issues. Please continue with that agent.", "OK"],
    ["My transfer completed but the money never reached the recipient.", "This looks like a settlement issue.", "Can you sort it out?", "The Payments Agent handles settlement and transfer problems. Please continue with that agent.", "OK"],
    ["transfer done but recipient didnt get money", "Sounds like a payment settlement problem.", "can you fix", "Settlement issues are handled by the Payments Agent. Please continue with them.", "ok"],
    ["The transfer shows successful, yet the receiver says nothing arrived.", "That appears to be a settlement problem.", "Could you resolve it?", "The Payments Agent deals with transfer and settlement issues, so please continue with that agent.", "Okay"],
    ["Money left my account but didn't reach the other bank.", "It looks like a payment settlement issue.", "Fix it please.", "Please continue with the Payments Agent, who handles settlement issues.", "OK."],
    ["sent money, says completed, but recipient hasnt recieved", "This seems like a settlement issue.", "can u fix it", "The Payments Agent handles this. Please continue with that agent.", "OK"],
    ["My payment to a supplier was debited but they haven't got it.", "That sounds like a transfer settlement issue.", "What can you do?", "The Payments Agent is the right place for settlement issues. Please continue with them.", "sure"],
  ], [
    ["Transfer marked complete, but my friend still hasn't got the funds.", "This is probably a settlement delay.", "Can you help?", "Please continue with the Payments Agent for transfer and settlement problems.", "OK"],
    ["debited but not credited to the beneficiary", "Looks like a settlement issue.", "and?", "The Payments Agent will handle it. Please carry on with that agent.", "ok"],
  ]),
"012": (C, G, ["handoff", "ok_after_handoff", "close_pair"], [
    ["I lost my physical card.", "You need card servicing rather than a payment investigation.", "Okay.", "Please continue with the Card Support Agent for blocking and replacement.", "OK"],
    ["I've lost my physical card.", "You need card servicing rather than a payment investigation.", "Okay.", "Please continue with the Card Support Agent for blocking and replacement.", "OK"],
    ["lost my card", "This is a card servicing request, not a payment issue.", "ok", "Please continue with the Card Support Agent to block and replace it.", "ok"],
    ["I can't find my debit card anywhere.", "That needs card servicing rather than a payments check.", "Right.", "The Card Support Agent can block and replace your card. Please continue with them.", "OK"],
    ["My card fell out of my wallet somewhere.", "We should handle this as card servicing.", "Fine.", "Please continue with Card Support for blocking and a replacement.", "Okay"],
    ["i lost my card yesterday", "You need card servicing, not a payment investigation.", "ok", "Please continue with the Card Support Agent for block and replacement.", "OK"],
    ["My wallet was stolen with my card in it.", "This is a card servicing matter.", "Understood.", "Please continue with the Card Support Agent to block the card and order a new one.", "sure"],
  ], [
    ["Misplaced my credit card on a trip.", "This calls for card servicing rather than a payments review.", "Alright.", "Please continue with the Card Support Agent to block and reissue it.", "OK"],
    ["card missing", "That's a card servicing issue.", "ok", "The Card Support Agent will block and replace it, please continue there.", "ok"],
  ]),
"013": (I, G, ["handoff", "ok_after_handoff", "context"], [
    ["I have about 500000 rupees available.", "What are you planning to use the money for?", "Long-term wealth creation.", "What is your approximate time horizon?", "Seven to ten years.", "Are you considering a lump sum or regular investment?", "Probably both.", "Would you like to discuss mutual funds and SIP allocation?", "Yes.", "The Investment Agent can help with that.", "Okay, let's continue."],
    ["I have around 500000 rupees to put somewhere.", "What do you plan to use the money for?", "Building wealth over the long term.", "What's your time horizon?", "About seven to ten years.", "Lump sum or regular investments?", "Probably a mix of both.", "Shall we discuss mutual funds and SIP allocation?", "Yes.", "The Investment Agent can help with that.", "Okay, let's go ahead."],
    ["got 5 lakh available", "What's the money for?", "long term wealth", "Time horizon?", "7-10 yrs", "Lump sum or SIP?", "both i guess", "Want to talk about mutual funds and SIP allocation?", "yes", "The Investment Agent can help with that.", "ok continue"],
    ["I've saved roughly five lakh rupees.", "What would you like that money to achieve?", "I want it to grow for retirement.", "How many years are you looking at?", "Maybe ten years.", "Do you prefer investing at once or gradually?", "A bit of both.", "Would you like to discuss fund choices and SIP allocation?", "Sure.", "The Investment Agent can help you with that.", "Great, let's continue."],
    ["500000 rupees are sitting in savings.", "What's your goal for it?", "Long-term growth.", "Your time frame?", "Seven years at least.", "One-time or regular investing?", "Both.", "Shall we look at mutual funds and SIPs?", "Yes please.", "The Investment Agent can take this forward.", "Okay."],
    ["i have abt 500000 rs", "what is the money for?", "wealth creation long term", "time horizon?", "7 to 10 years", "lump sum or regular?", "prob both", "discuss mutual funds and sip allocation?", "yes", "The Investment Agent can help with that.", "ok lets continue"],
    ["I'd like advice on what to do with about 500000 rupees.", "What is the purpose of the money?", "My children's education in about eight years.", "So your horizon is around eight years?", "Yes.", "Would you invest it all now or over time?", "Partly now, partly monthly.", "Do you want to go through mutual funds and SIP allocation?", "Yes.", "The Investment Agent can help with that.", "Okay, continue."],
  ], [
    ["I can set aside roughly half a million rupees.", "What are you saving it for?", "Retirement, a long way off.", "Roughly how many years?", "Around nine.", "All at once or in instalments?", "Some of each.", "Shall we look at a fund and SIP mix?", "Yes.", "The Investment Agent can guide you on that.", "Alright, go on."],
    ["have 5L to park", "what's it for?", "future, long term", "how long?", "8-10 yrs", "one shot or monthly?", "both", "talk funds and sip split?", "ya", "The Investment Agent can help with that.", "ok go"],
  ]),
"014": (P, G, ["close_pair", "context", "distractor"], [
    ["I was charged twice.", "Was this a bank transfer or a card transaction?", "It was my debit card.", "Do you believe the card itself has been compromised, or is the issue the duplicate payment?", "The same merchant payment appears twice."],
    ["I got charged twice.", "Was it a bank transfer or a card transaction?", "It was on my debit card.", "Do you think the card is compromised, or is the problem the duplicate payment?", "The same merchant payment shows up twice."],
    ["charged 2 times", "Transfer or card transaction?", "debit card", "Is your card compromised or is it the double payment?", "same payment to the shop appears twice"],
    ["My account was debited twice for one purchase.", "Was that a bank transfer or a card payment?", "A card payment with my debit card.", "Is the card at risk, or is it just the duplicate charge?", "Just the duplicate charge from the merchant."],
    ["Double charge on my account.", "Bank transfer or card?", "Card.", "Card security issue or duplicate payment issue?", "Duplicate payment. Same merchant, same amount, twice."],
    ["i was charged twice", "was this a transfer or a card txn?", "debit card", "card compromised or duplicate payment?", "duplicate payment, the merchant charged me 2x"],
    ["The shop charged me two times.", "Was it a card transaction or a transfer?", "My debit card.", "Should we treat the card as compromised, or look at the duplicate payment?", "The duplicate payment. I only bought one thing."],
  ], [
    ["One purchase, two debits.", "Did that happen through a transfer or your card?", "Through my debit card.", "Do you think someone has your card, or is it a duplicated payment?", "It's the merchant payment that got duplicated."],
    ["billed twice for the same thing", "transfer or card payment?", "card", "card security or the repeated payment?", "the repeated payment"],
  ]),
"015": (C, G, ["close_pair", "context"], [
    ["I see a transaction I don't recognize.", "Is it a transaction made using your card?", "Yes.", "Do you want to dispute one transaction, or do you think someone has access to your card?", "I think someone has my card details."],
    ["I see a transaction I don't recognise.", "Was it made using your card?", "Yes.", "Do you want to dispute one transaction, or do you think someone has access to your card?", "I think someone has my card details."],
    ["unknown transaction", "Made with your card?", "yes", "Dispute one transaction or is your card compromised?", "someone has my card details i think"],
    ["There's a payment on my statement I don't know.", "Was your card used for it?", "It was.", "Is it a one-off dispute, or could someone be using your card?", "Someone is using my card, I'm sure."],
    ["Unfamiliar transaction on my account.", "Card transaction?", "Yes, card.", "Single dispute or card compromise?", "Card compromise. My details are out there."],
    ["theres a transaction i dont recognize", "is it a card transaction?", "yep", "dispute it or is someone using ur card?", "someone got my card details"],
    ["I noticed a strange transaction.", "Did it go through your card?", "Yes it did.", "Would you like to dispute it, or are you worried your card is compromised?", "Worried my card is compromised."],
  ], [
    ["An odd transaction appeared yesterday.", "Did it use your card?", "Yes.", "Just disputing that one, or has your card been compromised?", "My card details have been stolen."],
    ["strange txn", "card?", "yes", "dispute or compromised card?", "compromised card"],
  ]),
"016": (I, G, ["ding_dong", "handoff", "ok_after_handoff", "distractor"], [
    ["I want to invest in a mutual fund.", "The Investment Agent can help with that.", "Before that, how do I transfer the money?", "That sounds like a payment question.", "Yes, but I still want to invest.", "The Investment Agent can continue with your investment plan.", "Okay."],
    ["I want to invest in a mutual fund.", "The Investment Agent can help with that.", "Before that, how do I transfer the money?", "That sounds like a payment question.", "Yes, but I still want to invest.", "The Investment Agent can continue with your investment plan.", "OK"],
    ["want to buy a mutual fund", "The Investment Agent can help.", "first how do i move the money", "That's a payments question.", "ok but i still want to invest", "The Investment Agent can carry on with your plan.", "ok"],
    ["I'm looking to invest in an equity fund.", "The Investment Agent handles that.", "Hold on, how do I transfer funds first?", "That's a payment topic.", "Right, but the investment is what I really want.", "Then the Investment Agent will continue with your plan.", "Sure."],
    ["Interested in mutual funds.", "The Investment Agent can help.", "But how do I send the money?", "That's for payments.", "Fine, but investing is the goal.", "The Investment Agent can continue with you.", "OK"],
    ["i want to invst in mutual fund", "The Investment Agent can help with that.", "before that how to transfer money?", "that sounds like a payment question", "yes but still want to invest", "The Investment Agent can continue with your investment plan.", "okay"],
    ["Can I put money into a mutual fund?", "Yes, the Investment Agent can help.", "How would I transfer the money in?", "That part is a payment question.", "Leave that, I mainly want to invest.", "The Investment Agent will continue with your investment.", "Alright."],
  ], [
    ["I'd like to buy units of a mutual fund.", "The Investment Agent can assist.", "Wait, how do I move money for it?", "That would be a payment matter.", "Okay, but investing is still the main thing.", "The Investment Agent will pick up your investment plan.", "OK"],
    ["mf investment pls", "Investment Agent can help.", "how do i send money first", "that's payments", "nah focus on investing", "Investment Agent will continue.", "k"],
  ]),
"017": (I, G, ["ding_dong", "distractor"], [
    ["Tell me about SIPs.", "The Investment Agent handles SIP questions.", "What about my card?", "The Card Support Agent handles card questions.", "Actually tell me about SIPs again.", "The Investment Agent handles that.", "And can my card make the payment?", "That could involve both cards and payments.", "Forget the card. I want to invest."],
    ["Tell me about SIPs.", "The Investment Agent handles SIP questions.", "What about my card?", "The Card Support Agent handles card questions.", "Actually, SIPs again.", "The Investment Agent handles that.", "Can my card make the payment?", "That could involve cards and payments.", "Forget the card. I want to invest."],
    ["sips?", "The Investment Agent handles SIPs.", "and my card?", "Card Support handles card questions.", "no back to sips", "That's the Investment Agent.", "can my card pay for it", "That may involve cards and payments.", "forget card, i want to invest"],
    ["Explain how SIPs work.", "SIP questions go to the Investment Agent.", "Also, something about my card.", "Card questions go to the Card Support Agent.", "Actually let's talk SIPs again.", "That's the Investment Agent.", "Could my card be used to pay?", "That might involve both cards and payments.", "Never mind the card, I just want to invest."],
    ["What is a SIP?", "The Investment Agent answers SIP questions.", "Wait, what about my credit card?", "The Card Support Agent handles cards.", "Back to SIPs.", "Investment Agent then.", "Can I pay with my card?", "That touches cards and payments.", "Drop the card topic, I want to invest."],
    ["tell me abt sip", "Investment Agent handles SIP questions.", "wat about my card", "Card Support Agent handles card questions.", "actually sip again", "Investment Agent handles that.", "can card pay for it", "that could involve card and payments", "forget card i want to invest"],
    ["I want to learn about SIPs.", "The Investment Agent covers SIPs.", "Hmm, my card though?", "Card questions are for Card Support.", "No, SIPs please.", "The Investment Agent can help.", "Would my card work for the payment?", "That could need cards and payments.", "Forget it, investing is what I want."],
  ], [
    ["Give me info on SIPs.", "SIPs are handled by the Investment Agent.", "And my card?", "That's for Card Support.", "Hmm, SIPs again actually.", "Investment Agent again.", "Can I fund it with my card?", "That might be cards and payments.", "Skip the card stuff, I want to invest."],
    ["sip info", "Investment Agent.", "card?", "Card Support.", "sip again", "Investment Agent.", "pay by card?", "cards and payments maybe", "no forget card, invest"],
  ]),
"018": (P, G, ["ding_dong", "close_pair", "handoff", "ok_after_handoff", "distractor"], [
    ["My card payment failed.", "We can check the payment transaction.", "Actually my card may be blocked.", "That is more appropriate for Card Support.", "The payment is still the main problem.", "The Payments Agent can investigate the failed transaction.", "Okay."],
    ["My card payment failed.", "We can check the payment transaction.", "Actually my card might be blocked.", "That is more for Card Support.", "The payment is still the main issue.", "The Payments Agent can investigate the failed transaction.", "Okay."],
    ["card payment failed", "We can look at the transaction.", "maybe my card is blocked", "Card Support would handle that.", "no the payment is the main problem", "The Payments Agent can investigate the failed payment.", "ok"],
    ["A payment with my card failed.", "Let's check the payment transaction.", "Or maybe the card is blocked?", "A blocked card is a Card Support matter.", "The failed payment matters more to me.", "The Payments Agent will investigate the failed transaction.", "Sure."],
    ["Card payment didn't work.", "We can check the transaction.", "Could the card be blocked?", "That's for Card Support.", "Payment's still the bigger issue.", "The Payments Agent can look into the failed payment.", "OK"],
    ["my card paymnt failed", "we can check the payment transaction", "actually card may be blockd", "that's more card support", "payment is still main problem", "The Payments Agent can investigate the failed transaction.", "okay"],
    ["My payment by card was rejected.", "I can have the transaction checked.", "Though maybe my card got blocked.", "Card status is Card Support's area.", "No, it's really the failed payment I care about.", "The Payments Agent can investigate it.", "Alright."],
  ], [
    ["Paying with my card just failed.", "We can review that payment.", "Hmm, perhaps the card itself is blocked.", "Card blocks are for Card Support.", "The payment is still what I need fixed.", "The Payments Agent will look into the failed transaction.", "OK"],
    ["card pmt failed", "can check txn", "or card blocked?", "card support for that", "payment still main issue", "Payments Agent will investigate.", "ok"],
  ]),
"019": (I, G, ["ding_dong", "distractor"], [
    ["I want investment advice.", "The Investment Agent handles investment questions.", "Actually, tell me about card limits.", "Card limits are handled by Card Support.", "No, go back to investments.", "Investment questions go to Investment.", "Now tell me whether my card can pay for it.", "That may involve both card and payment support.", "I am just testing you. Let's talk about investments."],
    ["I want investment advice.", "The Investment Agent handles investment questions.", "Actually, tell me about card limits.", "Card limits are handled by Card Support.", "No, back to investments.", "Investment questions go to Investment.", "Now, can my card pay for it?", "That may involve card and payment support.", "Just testing you. Let's talk investments."],
    ["need investment advice", "Investment Agent handles that.", "actually card limits?", "Card Support handles card limits.", "no back to investing", "Investment then.", "can my card pay for it", "maybe card and payments", "lol just testing, investments"],
    ["Give me some investment advice.", "That's the Investment Agent.", "What are my card limits, actually?", "Card limits sit with Card Support.", "Forget that, investments.", "Back to the Investment Agent.", "Could my card pay for the investment?", "That could involve card and payment support.", "I'm only testing you. Investments, please."],
    ["Investment tips please.", "Investment Agent handles that.", "Card limit question instead.", "That's Card Support.", "Investments again.", "Investment Agent.", "Card for paying it?", "Card and payment support maybe.", "Testing. Investments."],
    ["i want investmnt advice", "Investment Agent handles investment questions.", "actually tell me card limits", "card limits are card support", "no go back to investments", "investment questions go to investment", "now can my card pay for it", "may involve card and payment support", "just testing u. lets talk investments"],
    ["Help me decide where to invest.", "The Investment Agent will help.", "Hmm, what's my card's spending limit?", "Card Support handles card limits.", "Never mind, investing.", "The Investment Agent can continue.", "Can I use my card to pay for it?", "That might need card and payment support.", "Ha, I was testing you. Investing please."],
  ], [
    ["I need advice on investing.", "The Investment Agent covers that.", "Wait, tell me my card limit.", "Card limits belong to Card Support.", "Nope, back to investing.", "Investment Agent again.", "Will my card cover the purchase?", "Possibly card and payment support.", "Just messing with you. Investing, please."],
    ["invest advice", "Investment Agent", "card limit?", "Card Support", "investing again", "Investment", "card can pay?", "card + payments", "testing lol, investing"],
  ]),
"020": (P, I, ["context", "distractor", "topic_change"], [
    ["I started a SIP last month.", "Okay.", "It was supposed to debit yesterday.", "Did the debit happen?", "No.", "You may want to check the payment status.", "Can you tell me what happened to it?"],
    ["I started a SIP last month.", "Okay.", "It should have debited yesterday.", "Did the debit go through?", "No.", "You may want to check the payment status.", "Can you tell me what happened to it?"],
    ["started sip last month", "ok", "was supposed to debit yesterday", "did it debit?", "no", "you may want to check the payment status", "what happened to it?"],
    ["My SIP began last month.", "Alright.", "The instalment was due to debit yesterday.", "Was the amount debited?", "It wasn't.", "Then the payment status should be checked.", "Can you find out what happened to that payment?"],
    ["New SIP from last month.", "Okay.", "Debit date was yesterday.", "Did it happen?", "No.", "Check the payment status then.", "What went wrong with it?"],
    ["started a sip last mnth", "ok", "it was suposed to debit yesterday", "did the debit happen?", "nope", "you might want to check the payment status", "can u tell me what happened to it"],
    ["I registered a SIP a month ago.", "Okay.", "Yesterday's auto-debit was expected.", "Has the debit happened?", "No, it hasn't.", "It sounds like the payment status needs checking.", "So what happened to that debit?"],
  ], [
    ["My SIP kicked off last month.", "Okay.", "Yesterday was the debit date.", "Did the money get debited?", "No.", "It may be worth checking the payment status.", "Where did that payment go?"],
    ["sip started last month", "ok", "debit due yesterday", "debited?", "no", "check payment status maybe", "what happened to it then"],
  ]),
"021": (N, G, ["context", "distractor"], [
    ["I want something that grows my money.", "There are several financial products.", "I already have a policy.", "Is your question about that policy or about investing separately?", "The policy. I want to understand the premium increase."],
    ["I want something that grows my money.", "There are several financial products.", "I already have a policy.", "Is your question about that policy or about investing separately?", "The policy. Why did the premium increase?"],
    ["want my money to grow", "There are a few financial products.", "i already have a policy", "About that policy or a separate investment?", "the policy, why did the premium go up"],
    ["I'm after something that increases my wealth.", "Several products could do that.", "Well, I hold an insurance policy already.", "Is this about the policy, or a new investment?", "About the policy, specifically the higher premium."],
    ["Looking for growth on my money.", "Many products exist.", "I have a policy already.", "Policy question or separate investing?", "Policy. Premium went up."],
    ["i want smth that grows my money", "There are several financial products.", "already have a policy", "is it about the policy or investing separately?", "policy. want to understand premium increase"],
    ["What can make my money grow?", "There are several options.", "Thing is, I already have a policy.", "Do you mean that policy, or a separate investment?", "That policy. Its premium has increased and I want to know why."],
  ], [
    ["I'd like my money to work harder.", "There are various financial products.", "I do have an existing policy.", "Is this about the policy, or a fresh investment?", "The policy. I'm confused by the higher premium."],
    ["grow money", "several products", "have a policy", "policy or invest?", "policy, premium increase"],
  ]),
"022": (I, G, ["context"], [
    ["Can someone help me plan this?", "Sure. What are you planning?", "Where to put my savings.", "Are you looking for investment options?", "Yes, mainly mutual funds."],
    ["Can someone help me plan this?", "Sure. What are you planning?", "Where to put my savings.", "Are you looking for investment options?", "Yes, mostly mutual funds."],
    ["can someone help plan this", "sure, what are you planning?", "where to keep my savings", "investment options?", "yes mostly mutual funds"],
    ["I need help planning something.", "Happy to help. What are you planning?", "What to do with my savings.", "Do you mean investment options?", "Yes, mutual funds mostly."],
    ["Help me plan, please.", "Of course. Plan what?", "My savings.", "Investment options?", "Yes, mutual funds."],
    ["can some1 help me plan this", "sure what are u planning", "where to put my savings", "looking for investment options?", "yes mainly mutual funds"],
    ["Could you help me with a plan?", "Sure, what kind of plan?", "Deciding where my savings should go.", "So you're exploring investment options?", "Right, especially mutual funds."],
  ], [
    ["I want some help planning.", "Sure. What's the plan about?", "Putting my savings to use.", "Investment options, then?", "Yep, mostly mutual funds."],
    ["help me plan", "planning what?", "savings", "invest?", "yes mutual funds"],
  ]),
"023": (P, I, ["context", "distractor", "topic_change"], [
    ["I want to invest 100000.", "The Investment Agent can help choose an investment approach.", "I know what I want.", "Okay.", "How do I transfer the money into the investment account?"],
    ["I want to invest 100000.", "The Investment Agent can help choose an approach.", "I already know what I want.", "Okay.", "How do I transfer the money into the investment account?"],
    ["want to invest 1 lakh", "The Investment Agent can help choose an approach.", "i know what i want", "ok", "how do i transfer the money to the investment account"],
    ["I plan to invest 100000 rupees.", "The Investment Agent can help pick an approach.", "My mind's made up on what to buy.", "Okay.", "How do I move the money into my investment account?"],
    ["Investing 100000.", "Investment Agent can help.", "Already decided.", "Okay.", "How do I send the money to the investment account?"],
    ["i want to invest 100000", "Investment Agent can help choose an investment approach.", "i know what i want", "ok", "how do i transfr money into investment acct"],
    ["I'm ready to invest 100000.", "The Investment Agent can help you choose.", "No need, I've chosen already.", "Okay.", "What's the way to transfer money into the investment account?"],
  ], [
    ["I'll be investing about 100000.", "The Investment Agent can suggest an approach.", "I've already picked the fund.", "Okay.", "How do I get the money transferred into that account?"],
    ["investing 1L", "Investment Agent can help pick", "already decided", "ok", "how to transfer money there"],
  ]),
"024": (C, P, ["close_pair", "context", "distractor"], [
    ["I can't make a payment.", "What happens when you try?", "The card itself says blocked.", "Are you asking about the payment or the card status?", "The card status. I need it unblocked."],
    ["I can't make a payment.", "What happens when you try?", "The card itself says blocked.", "Is your question about the payment or the card status?", "The card status. I need it unblocked."],
    ["cant make a payment", "what happens when you try?", "card says blocked", "payment or card status?", "card status, need it unblocked"],
    ["My payment won't go through.", "What do you see when you try?", "A message that my card is blocked.", "Is it the payment or the card status you need help with?", "The card status. Please unblock it."],
    ["Payment not working.", "What happens?", "Card shows as blocked.", "Payment or card status?", "Card status. Unblock it."],
    ["i cant make a paymnt", "what happens when u try", "the card itself says blockd", "payment or card status?", "card status, need it unblocked"],
    ["I'm unable to pay anywhere.", "What error do you get?", "It says my card is blocked.", "Do you need help with the payment, or with the card status?", "With the card. I need it unblocked."],
  ], [
    ["Payments keep failing for me.", "What happens when you try?", "It tells me the card is blocked.", "Is it the payment you're asking about, or the card's status?", "The card's status. Please get it unblocked."],
    ["cant pay", "what happens?", "card blocked msg", "payment or card?", "card, unblock it"],
  ]),
"025": (C, G, ["handoff", "handoff_chain", "ok_after_handoff", "close_pair", "context"], [
    ["I don't know who can help me with this.", "Tell me what happened.", "My card payment failed and now the card seems blocked.", "The failed transaction is a Payments issue, but the blocked card is a Card Support issue.", "The card is the bigger problem.", "Please continue with Card Support.", "Okay."],
    ["I don't know who can help me with this.", "Tell me what happened.", "My card payment failed and now the card seems blocked.", "The failed transaction is a Payments issue, but the blocked card is a Card Support issue.", "The card is the bigger problem.", "Please continue with Card Support.", "OK"],
    ["not sure who can help", "what happened?", "card payment failed and card seems blocked now", "Failed transaction is Payments, blocked card is Card Support.", "card is the bigger issue", "Please continue with Card Support.", "ok"],
    ["Who should I talk to about this?", "Tell me what's going on.", "A card payment failed and my card looks blocked.", "The failed payment belongs to Payments; the blocked card belongs to Card Support.", "The blocked card matters more.", "Then please continue with Card Support.", "OK"],
    ["Not sure where to go.", "What happened?", "Payment failed, card now blocked.", "Payment is Payments; blocked card is Card Support.", "Card's the bigger issue.", "Please continue with Card Support.", "Okay."],
    ["idk who can help me", "tell me what happened", "card payment failed n now card seems blocked", "failed txn is payments, blocked card is card support", "the card is bigger problem", "Please continue with Card Support.", "okay"],
    ["I'm not sure which team handles this.", "Can you describe the problem?", "My card payment was declined and the card now shows blocked.", "The declined payment is for Payments, the blocked card is for Card Support.", "Sorting the card is more urgent.", "Please continue with Card Support.", "Sure."],
  ], [
    ["Not sure which department I need.", "What's the issue?", "A card payment failed, and now the card appears to be blocked.", "The failed payment is a Payments matter; the blocked card is for Card Support.", "The blocked card is my priority.", "Please continue with Card Support.", "OK"],
    ["who handles this?", "what happened", "card pmt failed + card blocked", "payment = Payments, blocked card = Card Support", "card more important", "Please continue with Card Support.", "ok"],
  ]),
}

def messages(texts):
    roles = ["user", "assistant"]
    return [{"role": roles[i % 2], "content": t} for i, t in enumerate(texts)]

def length_tag(n):
    return "short" if n <= 3 else ("medium" if n <= 8 else "long")

train, evals = [], []
for group in (SEEDS,):
    for sid, (target, current, tags, tr, ev) in group.items():
        for k, texts in enumerate(tr):
            train.append({"id": f"{sid}-t{k}", "seed_id": sid, "messages": messages(texts), "target_agent": target,
                          "current_agent": current, "tags": tags + [length_tag(len(texts))]})
        for k, texts in enumerate(ev):
            evals.append({"id": f"{sid}-e{k}", "seed_id": sid, "messages": messages(texts), "target_agent": target,
                          "current_agent": current, "tags": tags + [length_tag(len(texts))]})

# Turn-by-turn ding-dong sequences: expected agent after each USER turn, plus the kind of turn.
DINGDONG = [
  {"id": "D1", "title": "Investment <-> Payments ping-pong", "turns": [
    ["I want to invest in a mutual fund.", I, "start"],
    ["The Investment Agent can help you choose a fund.", None, None],
    ["How do I transfer money into my investment account?", P, "topic_change"],
    ["The Payments Agent can help with transfers.", None, None],
    ["Ok and which fund has lower risk?", I, "ding_dong"],
    ["The Investment Agent can compare fund risk for you.", None, None],
    ["And the transfer fee?", P, "ding_dong"],
    ["Transfer charges are handled by the Payments Agent.", None, None],
    ["Back to funds, what about returns over five years?", I, "ding_dong"],
  ]},
  {"id": "D2", "title": "Follow-ups on one topic (the router should stay)", "turns": [
    ["My card has been blocked.", C, "start"],
    ["I can help with your blocked card.", None, None],
    ["Why did that happen?", C, "same_topic"],
    ["It was blocked after three wrong PIN attempts.", None, None],
    ["Can you unblock it?", C, "same_topic"],
    ["Yes, I've sent an unblock request.", None, None],
    ["ok thanks", C, "same_topic"],
    ["You're welcome.", None, None],
    ["Also what is my daily limit on it?", C, "same_topic"],
  ]},
  {"id": "D3", "title": "Payments <-> Card Support bouncing", "turns": [
    ["My card payment to an online store failed.", P, "start"],
    ["The Payments Agent can check the failed transaction.", None, None],
    ["Wait, is my card blocked?", C, "topic_change"],
    ["Card Support can check your card status.", None, None],
    ["Fine. But where is my money from that failed payment?", P, "ding_dong"],
    ["The Payments Agent can trace the failed payment.", None, None],
    ["and the card?", C, "ding_dong"],
    ["Card Support can confirm whether the card is active.", None, None],
    ["same issue as before, the payment", P, "ambiguous"],
  ]},
  {"id": "D4", "title": "Playful bouncing across all agents", "turns": [
    ["Tell me about SIPs.", I, "start"],
    ["The Investment Agent handles SIPs.", None, None],
    ["nah insurance premium", N, "ding_dong"],
    ["The Insurance Agent handles premiums.", None, None],
    ["lol no, block my card", C, "ding_dong"],
    ["Card Support can block your card.", None, None],
    ["just kidding, my bank transfer failed", P, "ding_dong"],
    ["The Payments Agent handles failed transfers.", None, None],
    ["ok seriously back to SIPs", I, "ding_dong"],
  ]},
  {"id": "D5", "title": "General start, handoff, OK, follow-ups", "turns": [
    ["I have a question.", G, "start"],
    ["Sure, what is it about?", None, None],
    ["My insurance claim was rejected.", N, "topic_change"],
    ["Please continue with the Insurance Agent for claims.", None, None],
    ["OK", N, "same_topic"],
    ["The Insurance Agent can review your claim.", None, None],
    ["what documents were missing?", N, "same_topic"],
    ["The claim lacked a hospital bill.", None, None],
    ["fine. also can I pay the premium by card?", N, "ambiguous"],
  ]},
]
dingdong = []
for seq in DINGDONG:
    msgs, annotations = [], []
    for i, (text, agent, kind) in enumerate(seq["turns"]):
        role = "user" if i % 2 == 0 else "assistant"
        msgs.append({"role": role, "content": text})
        if role == "user":
            annotations.append({"message_index": i, "expected_agent": agent, "turn_type": kind})
    dingdong.append({"id": seq["id"], "title": seq["title"], "messages": msgs, "user_turns": annotations})

# ---- integrity checks ----
for ex in train + evals:
    m = ex["messages"]
    assert 1 <= len(m) <= 15 and m[-1]["role"] == "user" and m[0]["role"] == "user", ex["id"]
    assert ex["target_agent"] in (P, C, I, N, G)
train_texts = {tuple(x["content"] for x in ex["messages"]) for ex in train}
for ex in evals:
    assert tuple(x["content"] for x in ex["messages"]) not in train_texts, f"eval leaks into train: {ex['id']}"
    assert ex["messages"][0]["content"] not in {t[0] for t in train_texts}, f"eval first message seen in train: {ex['id']}"
for seq in dingdong:
    assert len(seq["messages"]) <= 15

json.dump(train, open("data/modernbert_router/banking/extended.json", "w"), indent=1, ensure_ascii=False)
json.dump(evals, open("data/modernbert_router/banking/benchmark.json", "w"), indent=1, ensure_ascii=False)
json.dump(dingdong, open("data/modernbert_router/banking/dingdong.json", "w"), indent=1, ensure_ascii=False)
print(f"benchmark {len(evals)} | extended {len(train)} | ding-dong sequences {len(dingdong)} "
      f"({sum(len(s['user_turns']) for s in dingdong)} user turns)")
