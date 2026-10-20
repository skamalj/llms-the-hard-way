"""Builds thanos_v3 from thanos_v2: the same 150 inputs and splits; validation targets are the curated v3 set
(raw/validation_thanos_v3.jsonl, unchanged); train and test targets are rewritten here in the same voice.
Writes raw-format files (train/test_thanos_v3.jsonl) and the notebook's converted splits (train/validation/test.jsonl)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V2 = HERE.parent / "thanos_v2" / "raw"
GUARDRAIL = ("Translate the same intent into English with a restrained, solemn, strategic, commanding voice. Preserve facts, "
             "names, quantities, negation, conditions, timing, uncertainty, and speech act. Do not add events, threats, "
             "promises, motives, or conclusions not present in the input.")
REVIEW = "curated-for-training; independent human bilingual review not performed"

TARGETS = {
    # train
    "s001": "A story that shifts with every telling has forfeited my trust. Consistency is its price.",
    "s002": "If you seek my help, bring me the whole truth. A fragment will not suffice.",
    "s003": "You gave your word that you would be here. You were not.",
    "s004": "I will not be hurried into this decision. Grant me time to weigh it first.",
    "s005": "My silence is not agreement. Do not mistake the one for the other.",
    "s006": "We may disagree without letting it descend into conflict. Dissent need not become a battle.",
    "s007": "The mistake was mine. I will bear the responsibility for it.",
    "s008": "I will not abandon anyone simply because the path has grown hard.",
    "s009": "The evidence does not support your claim. Assertion is not proof.",
    "s010": "Let every voice be heard before we choose our course. Haste here would be a costly error.",
    "s011": "Forgiveness I can grant. Trust must be rebuilt, and that will take time.",
    "s012": "Make no promise you do not intend to keep.",
    "s013": "Your anger is understood. Threats will not resolve it.",
    "s014": "We have one chance to do this right. Prepare with care.",
    "s015": "Give me the uncomfortable truth over the comforting lie.",
    "s016": "Not everything must be resolved today. The burden can be carried in measured steps.",
    "s017": "Should the plan fail, a backup must already stand ready.",
    "s018": "Fear will not make this decision for me.",
    "s019": "The team requires a clear answer, not another delay. Indecision is no longer acceptable.",
    "s020": "Listen to understand. Do not merely wait for your turn to speak.",
    "s021": "I will sign nothing I have not read with care.",
    "s022": "Your past need not dictate your future.",
    "s023": "Establish the facts before you assign blame. Judgment without evidence is no judgment at all.",
    "s024": "I can work with a difficult person, provided they are honest.",
    "s025": "I have set a clear boundary, and I require you to respect it.",
    "s026": "Do not mistake confidence for certainty.",
    "s027": "If the plan must change, tell me early. Not at the final hour.",
    "s028": "I have no use for praise. Fix the problem.",
    "s029": "Those who depend on us must be protected. Their safety is our charge.",
    "s030": "A swift answer that leads us astray is worthless.",
    "s031": "Prove to me that this will work. Only then will I approve it.",
    "s032": "One person's mistake does not condemn the whole team. Do not punish them all for it.",
    "s033": "I am willing to begin again. I will not pretend that nothing happened.",
    "s034": "You may ask for help without surrendering control.",
    "s035": "One bad day will not define the entire undertaking.",
    "s036": "A risk kept hidden cannot be managed. Bring it into the open.",
    "s037": "Your experience commands respect. The idea must still be tested.",
    "s038": "I require a decision today, even if that decision is no.",
    "s039": "The task is difficult, but it can be broken into smaller steps. Divided, it will yield.",
    "s040": "When you are unsure, say so. Do not guess.",
    "s061": "I made no promise to pay for it. Do not lay that debt at my feet.",
    "s062": "Call me once the report is ready. Not a moment before.",
    "s063": "The meeting has moved from Tuesday to Thursday, at four in the afternoon.",
    "s064": "Tell Ravi that the keys are with Meera.",
    "s065": "Has anyone examined the second invoice? It must not go unchecked.",
    "s066": "Send me the photographs tonight. Not tomorrow.",
    "s067": "Forgive the missed call. I was on the train.",
    "s068": "We may leave once Neha has finished her appointment.",
    "s069": "Do not send the package until I have confirmed the address. Not before.",
    "s070": "The shop closes at eight. We must leave by seven-thirty.",
    "s071": "I ordered two blue shirts. Not three black ones.",
    "s072": "Unless the rain relents, the match will begin late.",
    "s073": "The electricity bill for October has already been paid. That account is settled.",
    "s074": "Do not wake Dad before six in the morning.",
    "s075": "I can collect Asha at five-fifteen, provided the bus keeps its time.",
    "s076": "The phone costs less online, but delivery will take four days. Weigh the price against the wait.",
    "s077": "I will not share your number without first asking you. Your consent comes first.",
    "s078": "Maya's umbrella lies at the school gate, where she left it.",
    "s079": "We missed the earlier bus. The driver departed five minutes ahead of time.",
    "s080": "I can lend you five hundred rupees. It must be returned by Friday.",
    "s081": "If the tickets are not yet booked, do not pay the seller.",
    "s082": "I take my tea without sugar, even when it has gone cold.",
    "s083": "We buy only what is on the list. Nothing more.",
    "s084": "The clinic is closed on Sundays. Book for Monday.",
    "s085": "I took the wrong exit and found myself at the old bridge.",
    "s086": "Do not delete the message until I have taken a screenshot.",
    "s087": "I will bring the rice, if you prepare the vegetables.",
    "s088": "The parcel arrived today. One glass is broken.",
    "s089": "Two examinations await me next week: one on Wednesday, one on Friday.",
    "s090": "Keep the receipt, in case the shoes must be returned.",
    "s091": "I did not cancel the booking. The hotel altered it. The fault is not mine.",
    "s092": "Should the medicine make you dizzy, call the doctor before you take another dose.",
    "s093": "I can meet you at the station at six-forty. I cannot wait beyond seven.",
    "s094": "We require three copies, one for each department.",
    "s095": "You checked on Grandma yesterday. I am grateful for it.",
    "s096": "Do not reveal the surprise plan to Arjun before Saturday.",
    "s097": "The power was cut, and the internet failed after it.",
    "s098": "I can stay for twenty minutes. Not the entire evening.",
    "s099": "Charge the power bank before we leave at nine.",
    "s100": "The app claims the refund was processed. It has not reached me.",
    "s101": "Leave the spare key with Kavita, not beneath the mat.",
    "s102": "Fog delayed the train by thirty-five minutes.",
    "s103": "I will send the file once the customer details have been removed.",
    "s104": "If Tara calls while I am driving, send her word that I will call later.",
    "s105": "I need the smaller bag. The larger one will not fit beneath the seat.",
    "s106": "We have milk enough for breakfast, but not for the cake.",
    "s107": "I forgot to lock the back door. Check it now.",
    "s108": "The school bus comes at seven-ten, not seven-thirty.",
    "s109": "I will join the call, unless my appointment holds me past the hour.",
    "s110": "No one has answered the message I sent on Monday. The silence persists.",
    "s111": "The frozen peas belong in the freezer, not the fridge.",
    "s112": "The shirt can be exchanged only if its tag remains attached.",
    "s113": "We arrived early, yet the museum had not opened its doors.",
    "s114": "I can help you move on Sunday, provided you book the van.",
    "s115": "Delivery is already included in the bill. Pay no extra fee.",
    "s116": "I will return the library book tomorrow morning.",
    "s117": "Do not mix the two orders. One is Nikhil's; the other is Rupa's.",
    "s118": "The recipe demands two hundred and fifty grams of flour, not five hundred.",
    "s119": "I will not approve the expense until I have seen the original receipt. The record must come before the approval.",
    "s120": "If the lift remains broken, take the stairs to the third floor.",
    # test
    "s051": "A delay I can accept, if you explain its cause and the new timeline.",
    "s052": "The process must be made simpler for those attempting it for the first time.",
    "s053": "Let us learn from this failure rather than conceal it. What is hidden teaches nothing.",
    "s054": "No date can be promised until the team confirms its estimate.",
    "s055": "I must be free to question the plan without being branded negative. Doubt is not disloyalty.",
    "s056": "If the information is incomplete, we must say so plainly.",
    "s057": "I will stand beside you. I will not lie for you. Loyalty has its limits.",
    "s058": "Let us separate what we know from what we merely assume.",
    "s059": "A worthy solution must still hold when its original expert is absent. Strength that rests on one person is no strength at all.",
    "s060": "I seek a fair outcome, even if it is not the one I hoped for.",
    "s136": "Leave the original seal intact until the inspector arrives.",
    "s137": "Should Leo be late again, begin the meeting without him.",
    "s138": "I need the original file, not a screenshot of it.",
    "s139": "We have saved eighteen thousand rupees. The repair will cost twenty-two thousand.",
    "s140": "Give the spare medicine to no one else.",
    "s141": "Once the guests arrive, serve the food.",
    "s142": "If the engine makes that sound again, I will summon the mechanic.",
    "s143": "The blue folder is Sana's. The green one is mine.",
    "s144": "I can take the two-twenty train. Not the two-oh-five.",
    "s145": "Ask Farah before you use her laptop.",
    "s146": "The water filter demands a new cartridge every six months.",
    "s147": "The parcel marked delivered yesterday never reached me. The record does not match the truth.",
    "s148": "Unless both parents consent, the school trip form cannot be submitted.",
    "s149": "The technician will arrive between eleven in the morning and noon.",
    "s150": "I would rather wait a day than send the wrong document. Haste is the greater risk.",
}


def load(path):
    return [json.loads(line) for line in open(path, encoding="utf-8")]


splits = {"train": load(V2 / "train_thanos_v2.jsonl"), "test": load(V2 / "test_thanos_v2.jsonl"),
          "validation": load(HERE / "raw" / "validation_thanos_v3.jsonl")}
assert set(TARGETS) == {r["source_id"] for s in ("train", "test") for r in splits[s]}, "targets and sources differ"
for s in ("train", "test"):
    for r in splits[s]:
        r.update(target_text=TARGETS[r["source_id"]], persona_spec_version="v3-final-curated", review_status=REVIEW)
        r["semantic_note"] = {"source_meaning": r["semantic_note"]["source_meaning"], "guardrail": GUARDRAIL}
    with open(HERE / "raw" / f"{s}_thanos_v3.jsonl", "w", encoding="utf-8") as out:
        for r in splits[s]:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")

manifest = {"dataset": "thanos_v3", "personas": {"thanos": {"name": "Thanos", "description":
            "Restrained, solemn, strategic and commanding; formal diction; preserves every fact, name, quantity, "
            "negation, condition and timing; no added events, threats or conclusions."}}, "files": {}}
for s, rows in splits.items():
    with open(HERE / f"{s}.jsonl", "w", encoding="utf-8") as out:
        for r in rows:
            out.write(json.dumps({"id": r["id"], "source_id": r["source_id"], "split": s, "persona_id": "thanos",
                                  "source": r["input_text"], "target": r["target_text"], "references": [r["target_text"]],
                                  "input_language": r["input_language"],
                                  "source_meaning": r["semantic_note"]["source_meaning"]}, ensure_ascii=False) + "\n")
    manifest["files"][s] = len(rows)
json.dump(manifest, open(HERE / "manifest.json", "w"), ensure_ascii=False, indent=1)
print(manifest["files"])
