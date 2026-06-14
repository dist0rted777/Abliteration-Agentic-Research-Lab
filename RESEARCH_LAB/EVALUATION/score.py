"""
Score detector.py against labels.json. Reports precision / recall / F1 and lists
every misclassification so you can decide whether the *detector* needs a new rule.
"""

import json
import os

from detector import scan

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLES = os.path.join(HERE, "samples")


def main():
    with open(os.path.join(HERE, "labels.json"), encoding="utf-8") as f:
        labels = json.load(f)["samples"]

    tp = fp = tn = fn = 0
    misses = []

    for rel, meta in labels.items():
        path = os.path.join(SAMPLES, rel)
        with open(path, encoding="utf-8") as f:
            r = scan(f.read(), rel)
        truth_injected = meta["label"] == "injected"
        if r.flagged and truth_injected:
            tp += 1
        elif r.flagged and not truth_injected:
            fp += 1
            misses.append(("FALSE POSITIVE", rel, r.score))
        elif not r.flagged and truth_injected:
            fn += 1
            misses.append(("FALSE NEGATIVE", rel, r.score))
        else:
            tn += 1

    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0

    print(f"samples={len(labels)}  TP={tp} FP={fp} TN={tn} FN={fn}")
    print(f"precision={prec:.3f}  recall={rec:.3f}  f1={f1:.3f}")
    if misses:
        print("\nmisclassified (candidates for a new DETECTOR rule):")
        for kind, rel, score in misses:
            print(f"  {kind:14} {rel}  (score={score:.1f})")


if __name__ == "__main__":
    main()
