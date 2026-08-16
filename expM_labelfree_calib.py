"""Measure the label-free calibration the paper describes for deployment.

The harness calibrates tau as the (1 - FPR_TARGET) quantile over the corpus's *benign*
partition, which requires knowing which documents are poison. A deployment has no such
partition. This script computes tau without any poison labels and reports whether the
gate's behaviour changes.

We use the strictly hardest label-free estimator: the quantile over the ENTIRE poisoned
corpus, poison included. A real deployment would take the quantile over documents its
benign query stream returns, which contains far less poison than the whole corpus (the
injected passages are engineered to rank for adversarial queries, not benign ones), so
whatever holds here holds a fortiori for that estimator.

Frozen constants only: K=5 neighbourhood coherence as cached, FPR_TARGET=0.0069,
seeds 42/7/123, 60/40 cal/eval split -- identical to reproduction/hardgate_xrun.py.
"""
import json, os, numpy as np

FPR_TARGET = 0.0069
SEEDS = (42, 7, 123)
CAL_FRAC = 0.60
DIRS = {1: "seva_checkpoints_4060_100k_secqa_p010",
        5: "seva_checkpoints_4060_100k_secqa_p050",
        10: "seva_checkpoints_4060_100k_secqa_p100"}
ROOT = os.path.dirname(os.path.abspath(__file__))
q = lambda a: float(np.percentile(a, 100.0 - FPR_TARGET * 100.0))

out = {"experiment": "M-label-free-calibration", "FPR_TARGET": FPR_TARGET,
       "estimator": "quantile over the whole poisoned corpus (no poison labels)",
       "grid": []}

for dens, d in DIRS.items():
    path = os.path.join(ROOT, d)
    coh = np.load(os.path.join(path, "p2_doc_coh.npy"))
    corpus = json.load(open(os.path.join(path, "p1_corpus.json"), encoding="utf-8"))
    ispois = np.array([bool(c["is_poisoned"]) for c in corpus])
    assert len(ispois) == len(coh), "corpus/coherence length mismatch"
    P = int(ispois.sum())
    # the harness assumes poison occupies the prefix; verify before relying on either view
    prefix_ok = bool(ispois[:P].all() and not ispois[P:].any())
    pc, cc = coh[ispois], coh[~ispois]

    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        # 60/40 split of the CLEAN documents, exactly as the harness does
        idx = rng.permutation(len(cc))
        ncal = int(len(cc) * CAL_FRAC)
        cal_clean, eval_clean = cc[idx[:ncal]], cc[idx[ncal:]]

        # (a) the harness estimator: quantile over known-clean calibration documents
        tau_lab = q(cal_clean)
        # (b) label-free: same split fraction, but over ALL documents, poison included
        allc = coh
        idx2 = rng.permutation(len(allc))
        cal_all = allc[idx2[:int(len(allc) * CAL_FRAC)]]
        tau_free = q(cal_all)

        row = {"density_pct": dens, "seed": seed, "n_poison": P,
               "prefix_convention_holds": prefix_ok,
               "tau_labelled": tau_lab, "tau_labelfree": tau_free,
               "tau_delta": tau_free - tau_lab,
               "evasion_labelled_pct": float(100.0 * np.mean(pc <= tau_lab)),
               "evasion_labelfree_pct": float(100.0 * np.mean(pc <= tau_free)),
               "docfpr_labelled_pct": float(100.0 * np.mean(eval_clean > tau_lab)),
               "docfpr_labelfree_pct": float(100.0 * np.mean(eval_clean > tau_free))}
        out["grid"].append(row)
        print("  d=%2d%% s=%-4d tau %.4f -> %.4f (D%+.4f)  evasion %.2f%% -> %.2f%%  "
              "docFPR %.3f%% -> %.3f%%" % (dens, seed, tau_lab, tau_free, row["tau_delta"],
              row["evasion_labelled_pct"], row["evasion_labelfree_pct"],
              row["docfpr_labelled_pct"], row["docfpr_labelfree_pct"]))

g = out["grid"]
out["verdict"] = {
    "max_tau_shift": max(abs(r["tau_delta"]) for r in g),
    "max_evasion_labelfree_pct": max(r["evasion_labelfree_pct"] for r in g),
    "evasion_unchanged": all(r["evasion_labelfree_pct"] == r["evasion_labelled_pct"] for r in g),
    "mean_docfpr_labelfree_pct": float(np.mean([r["docfpr_labelfree_pct"] for r in g])),
    "mean_docfpr_labelled_pct": float(np.mean([r["docfpr_labelled_pct"] for r in g])),
}
print("\nVERDICT:", json.dumps(out["verdict"], indent=1))
dst = os.path.join(ROOT, "whitebox_attack_results", "expM_labelfree_calib.json")
json.dump(out, open(dst, "w", encoding="utf-8"), indent=1)
print("wrote", dst)
