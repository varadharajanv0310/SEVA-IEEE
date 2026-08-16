# Results manifest — every headline claim → committed file

This maps each table/observation in the paper (`SEVA_tdsc.tex` for submission, `SEVA_arxiv.tex`
for the extended version) to the
committed result file(s) behind it. All detector runs are frozen and non-oracle; the corpus and
poison are hash-gated (see [HOW_TO_REPRODUCE.md](HOW_TO_REPRODUCE.md)).

## Corpus / poison identity

| Artifact | SHA-256 |
|---|---|
| 100k in-domain corpus | `28ec38114ee64e6010ec489d01e6d3ee13d9b3758fd30a169c99ed078732f8a9` |
| Templated poison (10k) | `4f7ee3f368cc6aae82180df261f4ee60bbd1f02b0834a4c4be72615ba68a733c` |
| 1M multi-site corpus | `317eb43c337c1970c4d80e14f8eb2a9f785b75b1cbac780c620d05fe765e98f4` |

## Main paper

| Table / claim | Headline number | File(s) |
|---|---|---|
| `tab:main` — primary in-domain grid | 0% poison-evasion, 0.58%/0.56% Doc-FPR; L2/L3 composite 42–72% | `results/in_domain/seva_v6_2_results_100k_secqa_p{010,050,100}_s{042,007,123}.json` (9) |
| `tab:coh` — `cluster_coh` geometry | gap +0.235→+0.247, SNR 5.8–6.0, density-invariant | same 9 in-domain files (clean/poison coh per cell) |
| `tab:percond` / Wilson bound | 0 evasions in 25,000 encounters → ≤ 0.0154% | `reproduction/result_hienc_ci.json` |
| Obs 2 — calibration scaling | Doc-FPR 0.765% → 0.674% → 0.701% (10k/100k/1M) | `reproduction/result_scale10k.json`, `result_scale100k.json`, `result_1M.json` |
| Obs 3 / `tab:encoder` — encoder-invariance | 0% evasion on bge / e5 / gte | `reproduction/result_encoder_{bge,e5,gte}.json` |
| `tab:xdomain` / `tab:roc` — cross-domain PoisonedRAG + lexical fragility | NQ 82% / HotpotQA 97% / Security 98%; MinHash 0% < 2% FPR | `whitebox_attack_results/pr_xgate_s042.json`, `pr_xgate_hotpotqa_s042.json`, `s_nd_gate_s042.json`, `s_lex_templated_gate_s042.json` |
| `tab:core` — geometric core vs composite | hard gate 0%/2%/0% vs composite 0%/28%/49–57% | `whitebox_attack_results/cheap_must1_s042.json`, `pr_gate_s042.json`, `ecal2_s042.json`, `seeds3_s042.json` |
| `tab:h2h` — head-to-head vs RAGDefender | SEVA 100% vs ~89% @ matched ~0.8% FPR; 50.4% strip | `whitebox_attack_results/e4hh_fair_s042.json`, `e4hh_s042.json`, `e4hh_ragd_flags_s042.json` |
| `tab:xplat` — cross-platform | identical detection; gap agrees < 5×10⁻⁷; 13–38 ms | `reproduction/result_4060.json`, `result_M4.json` (5080 = `result_scale100k.json` / in-domain grid) |
| `tab:scale` — million-document scale | 0% evasion, 0.70% FPR, 15.0 ms | `reproduction/result_1M.json` (+ `bench_1m.json`, `build_provenance_1m.json`) |
| §VI-D — diversity-injection adaptive attack | SEVA holds 0% (poison coh 0.9488, 0% below gate) | `adaptive_attack_results/summary.md` |

## The two composite-collapse figures (distinct measurements)

The 10-signal composite is an **ablation**, not the detector. It collapses under adaptation in
two distinct, separately-measured senses:

- **42–72%** — cost of *ablating* the soft signals from the detector (L2/L3 tiers, swept across
  density). Source: the 9 `results/in_domain/` files (`L2.asr` / `L3.asr` fields).
- **49–57%** — composite under an attack that *neutralizes the soft feature values* at the
  frozen operating point (E-CAL-2). Source: `whitebox_attack_results/ecal2_s042.json`
  (`L2.b` / `c1_value_clean` / `c2_drop_term` = 53.6 / 48.8 / 56.8).

The geometric hard gate holds **0%** against both.

## Supplementary material

| Supplement table | Backed by |
|---|---|
| `tab:confL1` / `tab:confL23` — per-seed confusion matrices | the 9 `results/in_domain/` files (L1/L2/L3 `counts`) |
| `tab:percond` — per-condition rates + Wilson | the 9 in-domain files + `reproduction/result_hienc_ci.json` |
| `tab:tau` — calibrated thresholds | per-run `tau_L1/L2/L3` and the hard-gate τ (≈0.84) in the result files |
| `tab:caps` — deployment-capability comparison | factual properties per cited defense (no lifted numbers) |

## The boundary: host-anchored cloning

The deployed gate's measured limitation (main paper, "The Boundary: Host-Anchored Cloning";
Limitations). Each injected passage mimics a *distinct* benign host, so cohesion never leaves
the clean band. Scored in the corpus the attack actually creates (95k clean + injected clones,
no templated poison present).

| Claim | Number | File |
|---|---|---|
| Clone evasion of `cluster_coh` (deployed gate) | **100%** of 50 targets; coh 0.751 vs tau 0.841 | `whitebox_attack_results/expD_deployed_gate_s042.json` |
| Retrievable @K=5 | 84% | same |
| Answer corruption among evading+retrieved | **31.0%** (13/42; Wilson 19.1-46.0) | same |
| **End-to-end ASR vs deployed gate** | **26.0%** of all 50 targets | same |
| CleanBase reproduced, matched 0.69% FPR | **100%** templated / **0%** clones -- identical to SEVA | `expT3_cleanbase_s042.json` |
| Payload-prominence frontier (Figure 1) | evasion 100->46%, retrievable 90->38%, **ASR peaks 28% at 25% payload** | `expT2b_potency_frontier_s042.json` |
| Complementary signal `s_nd` on clones | catches 13-20%; two-signal union gate 6.7-33.3% | `expA_snd_vs_paraclone_s042.json`, `expA2_cloneonly_s042.json` |
| Multiplicity sweep (1->5 clones/target) | coh 0.722 -> 0.790, still under tau | `expA2_cloneonly_s042.json` |

## Prevention, robustness, sensitivity

| Claim | Number | File |
|---|---|---|
| **End-to-end prevention (templated)** | corruption **22% -> 0%** (11/50); poison in top-K **2.74 -> 0.00** | `whitebox_attack_results/expA1_endtoend_s042.json` |

| **Per-query aggregation (benign query-FPR)** | `>=1 flagged` **3.06%** -> `>=2 flagged` **0.97%** (3.2x); means over the nine in-domain conditions | `reproduction/result_scale100k.json` (grid) |
| **Frozen disjoint-reference protocol** | held-out poison at 0% evasion, **0.58%** doc-FPR (composite L1, seed 42) | `whitebox_attack_results/linchpin_s042.json` |
| K-sensitivity | **100% catch** at K = 3, 5, 10, 20 (recalibrated per K) | `expA23_sensitivity_s042.json` |
| Operating-point sweep | **100% catch** at FPR targets 0.1-5%; **AUC 0.99994** | same |
| Chunking + cross-encoder reranking | 168,865 chunks; clean/poison coh 0.752/0.991; **100% catch**; reranker moves 3.6 positions/query, poison@5 unchanged | `expS1_chunk_rerank_s042.json` |

**No cost-of-evasion claim is made.** Harmonized on one criterion and one generator: templated
undefended **22%**, templated with gate **0%**, host-anchored clones **26%**, prominence-optimal
clones **28%**. The bypass is at least as effective as the attack it replaces, and the gate does
not bind at the adversary's optimum (25% payload, where evasion is still 100%).

Attack generation used `mistral:7b-instruct` (temperature 0); the answer-corruption judge used
`gpt-oss:20b` (temperature 0), identical to the earlier `expC_potency_s042.json` run, so potency
figures stay comparable. Detection is LLM-free throughout.

## Notes

- `results/general_domain/` holds the **general-domain baseline** (WikiText-style background):
  there the soft signals look strong and the composite does *not* collapse (`L2.asr ≈ 0`) — this
  is the permissive-evaluation contrast that motivates the in-domain control.
- Large intermediate dumps (poison/paraphrase embeddings, retrieval squeezes) are **not**
  committed; they are regenerated deterministically by the scripts. Multi-GB embedding caches
  and FAISS indices are gitignored.
