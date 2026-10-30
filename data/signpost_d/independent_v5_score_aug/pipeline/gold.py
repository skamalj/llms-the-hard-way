"""Gold rule, unchanged from train_v2: mean of the four labelling calls, renormalised; where the Opus checking
pass marks a read / compare / infer question SETTLED with confidence >= 0.9, 0.92 on the checked option and the
remaining 0.08 spread over the other options in proportion to the labellers' mean. Judge questions are never adjusted."""
from __future__ import annotations

VERIFY_CONF = 0.9
VERIFY_TOP = 0.92


def renorm(d):
    tot = sum(d.values())
    out = {k: round(v / tot, 4) for k, v in d.items()}
    drift = round(1.0 - sum(out.values()), 4)
    if drift:
        kmax = max(out, key=out.get)
        out[kmax] = round(out[kmax] + drift, 4)
    return out


def gold_for(q: dict, labels: dict, check: dict | None, key: str):
    """Returns (mean, gold, verified, adjusted, overrode_confident_mean)."""
    opts = [str(i) for i in range(len(q["criteria"]))]
    acc = {o: 0.0 for o in opts}
    for l in labels.values():
        pr = l["probabilities"][key]
        for o in opts:
            acc[o] += pr[o] / len(labels)
    mean = renorm(acc)
    g, verified, adjusted, overrode = dict(mean), "not_checked", False, False
    if q["kind"] != "judge" and check is not None:
        if check["settled"] and check["confidence"] >= VERIFY_CONF:
            verified = "settled"
            ans = check["answer"]
            top_before = max(mean, key=mean.get)
            overrode = top_before != ans and mean[top_before] >= 0.85
            rest = {o: mean[o] for o in opts if o != ans}
            rest_tot = sum(rest.values())
            g = {o: (VERIFY_TOP if o == ans else (1 - VERIFY_TOP) * (rest[o] / rest_tot if rest_tot > 0 else 1.0 / max(1, len(rest)))) for o in opts}
            g = renorm(g)
            adjusted = (top_before != ans) or (mean[ans] < 0.85)
        else:
            verified = "open"
    return mean, g, verified, adjusted, overrode
