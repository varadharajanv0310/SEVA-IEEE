"""The deployment calibration described in Section 4.3, measured.

The harness takes tau as the (1 - FPR_TARGET) quantile over the corpus's benign
partition, which needs poison labels. Section 4.3 describes what a deployment would do
instead: issue benign queries against the (possibly poisoned) corpus and take the
quantile over the scores of the documents those queries return. No poison labels, no
density estimate. This measures that estimator.

(A first attempt used the quantile over the whole corpus. That estimator is broken by
construction here: contamination is 1-10% while FPR_TARGET is 0.69%, so the top quantile
of the full corpus lies inside the poison mass and tau is dragged to ~0.99. Benign
retrieval is the relevant estimator because the injected passages are engineered to rank
for adversarial queries, not benign ones -- which is exactly what this measures.)

Frozen constants: K_FETCH=20, K=5, FPR_TARGET=0.0069, seeds 42/7/123, 60/40 split.
"""
import json, os, numpy as np, faiss
from sentence_transformers import SentenceTransformer

FPR_TARGET, K_FETCH, K = 0.0069, 20, 5
SEEDS = (42, 7, 123)
CAL_FRAC = 0.60
DIRS = {1: "seva_checkpoints_4060_100k_secqa_p010",
        5: "seva_checkpoints_4060_100k_secqa_p050",
        10: "seva_checkpoints_4060_100k_secqa_p100"}
ROOT = os.path.dirname(os.path.abspath(__file__))
q = lambda a: float(np.percentile(a, 100.0 - FPR_TARGET * 100.0))

print("loading encoder ...")
enc = SentenceTransformer("BAAI/bge-large-en-v1.5")
out = {"experiment": "M2-benign-retrieval-calibration", "FPR_TARGET": FPR_TARGET,
       "K_FETCH": K_FETCH, "K": K,
       "estimator": "quantile over cluster_coh of documents retrieved by BENIGN queries "
                    "(no poison labels, no density estimate)", "grid": []}

for dens, d in DIRS.items():
    path = os.path.join(ROOT, d)
    coh = np.load(os.path.join(path, "p2_doc_coh.npy"))
    corpus = json.load(open(os.path.join(path, "p1_corpus.json"), encoding="utf-8"))
    queries = json.load(open(os.path.join(path, "p1_query.json"), encoding="utf-8"))
    ispois = np.array([bool(c["is_poisoned"]) for c in corpus])
    benign = [x["q"] for x in queries if str(x["adv"]).lower() != "true"]
    index = faiss.read_index(os.path.join(path, "p2_faiss.index"))

    qe = enc.encode(benign, batch_size=64, normalize_embeddings=True,
                    convert_to_numpy=True, show_progress_bar=False).astype("float32")
    _, I = index.search(qe, K_FETCH)
    I = I[:, :K]                                   # rerank to top-K, as deployed
    pc = coh[ispois]

    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        perm = rng.permutation(len(benign))
        ncal = int(len(benign) * CAL_FRAC)
        cal_q, eval_q = perm[:ncal], perm[ncal:]

        # calibration: every document the benign calibration queries retrieved,
        # scored WITHOUT knowing which of them (if any) are poison
        cal_docs = np.unique(I[cal_q].ravel())
        tau_free = q(coh[cal_docs])
        n_pois_seen = int(ispois[cal_docs].sum())

        # evaluation: false positives among clean docs retrieved by held-out benign
        # queries, excluding documents seen during calibration (decontamination)
        eval_docs = np.unique(I[eval_q].ravel())
        eval_docs = eval_docs[~np.isin(eval_docs, cal_docs)]
        eval_clean = eval_docs[~ispois[eval_docs]]

        row = {"density_pct": dens, "seed": seed,
               "n_cal_docs": int(len(cal_docs)),
               "n_poison_in_cal_pool": n_pois_seen,
               "poison_frac_in_cal_pool_pct": float(100.0 * n_pois_seen / len(cal_docs)),
               "tau_labelfree": tau_free,
               "evasion_pct": float(100.0 * np.mean(pc <= tau_free)),
               "docfpr_pct": float(100.0 * np.mean(coh[eval_clean] > tau_free))}
        out["grid"].append(row)
        print("  d=%2d%% s=%-4d tau=%.4f  poison-in-cal-pool %d/%d (%.2f%%)  "
              "evasion %.2f%%  docFPR %.3f%%" % (dens, seed, tau_free, n_pois_seen,
              len(cal_docs), row["poison_frac_in_cal_pool_pct"], row["evasion_pct"],
              row["docfpr_pct"]))

g = out["grid"]
out["verdict"] = {
    "tau_range": [min(r["tau_labelfree"] for r in g), max(r["tau_labelfree"] for r in g)],
    "max_evasion_pct": max(r["evasion_pct"] for r in g),
    "evasion_zero_everywhere": all(r["evasion_pct"] == 0.0 for r in g),
    "mean_docfpr_pct": float(np.mean([r["docfpr_pct"] for r in g])),
    "max_poison_frac_in_cal_pool_pct": max(r["poison_frac_in_cal_pool_pct"] for r in g),
}
print("\nVERDICT:", json.dumps(out["verdict"], indent=1))
dst = os.path.join(ROOT, "whitebox_attack_results", "expM2_benign_retrieval_calib.json")
json.dump(out, open(dst, "w", encoding="utf-8"), indent=1)
print("wrote", dst)
