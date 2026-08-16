# SEVA — Known Issues & Discrepancies

This file documents confirmed discrepancies between the paper and the
code/experimental record. Items are split by status: **FIXED** (resolved in the
repo) and **OPEN** (require a further code or paper change).

Audit date: 2026-08-16, against `main` after the TDSC-review correction pass.
Papers audited: `SEVA_tdsc.tex` (submission), `SEVA_arxiv.tex` (extended).

---

## FIXED

### CF-011 — BGE-M3 loaded but never used in scoring (dead compute)
- **Fixed in**: `7fcc7e9` ("Remove BGE-M3 dead code, fix legacy warning")
- BGE-M3 load/encode removed; VRAM and encoding overhead eliminated.
- Paper Limitation 7 should still be updated to say "single embedding encoder" accurately.

### CF-012 — Dead-code driver scripts and stale result files
- **Fixed in**: `c18654d` ("Add reproducibility scaffold: README, requirements, LICENSE, CI, legacy cleanup")
- Stale v5 scripts and superseded result files moved to `legacy/`.

### CF-002 — Production latency/ASR/FPR evidence not committed
- **Fixed in**: `7fcc7e9`
- All 9 `results/seva_v6_2_results_100k_p{density}_s{seed}.json` files committed.
- `.gitignore` whitelists `!results/seva_v6_2_results_100k_*.json`.

### CF-010 — "NOT publishable" fallback warning
- **Partially fixed in**: `7fcc7e9` / `eba1add`
- `poison_corpus_diverse.json` is now committed, so the fallback is never triggered
  in a fresh clone. The legacy warning string in `seva_benchmark_4060.py` can remain
  as a safeguard.

### Portable driver paths
- **Fixed in**: `d9b74b6`
- `run_seva_v6_100k.py` and `run_seva_v6_smoke.py` now use `sys.executable` and
  `os.path.dirname(os.path.abspath(__file__))` instead of hardcoded Windows paths.

---

## OPEN — Require code or paper changes

### CF-001 — Binary-search calibration iterations: code 50 vs paper 100

| | |
|---|---|
| **Severity** | High |
| **File** | `seva_benchmark_4060.py` line ~767 |
| **Paper claim** | §IV-E: "100 binary-search iterations" |
| **Code** | `for _ in range(50):` |
| **Fix** | Change `range(50)` to `range(100)` and re-run calibration, **or** update paper to "50 iterations" |

---

### CF-004 — "28x weaker" SNR ratio mixes densities

| | |
|---|---|
| **Severity** | Medium |
| **Paper claim** | §IV-C: avg_sent_len is "~28x weaker than kw_density by SNR" |
| **Issue** | 38.42 (kw_density @ 1%) / 1.38 (avg_sent_len @ 5%) = 27.8x — cross-density. Within 5%: 34.80/1.38 = 25.2x |
| **Fix** | Paper: use within-density ratio or clarify which densities are compared |

---

### CF-005 — "Hardware-agnostic" claim contradicts Section VI-F

| | |
|---|---|
| **Severity** | High |
| **Paper claim** | Abstract, §I-C C6, §IX: SEVA is "hardware-agnostic" |
| **Contradiction** | §VI-F: L3 ASR = 0% on M4 vs 17.07% on RTX 4060 for identical code and attack |
| **Fix** | Paper: qualify the claim; or unify cross-platform calibration in code |

---

### CF-006 — "We prove" without a formal proof

| | |
|---|---|
| **Severity** | High |
| **Paper claim** | §I-C C3: "We prove that cluster_coh is invariant under adversarial normalization" |
| **Reality** | §V-E gives an informal mechanistic argument — no theorem, no proof |
| **Fix** | Paper: change "We prove" to "We show" / "We argue"; or add formal theorem + proof |

---

### CF-007 — 50 adversarial queries = 25 unique queries issued twice

| | |
|---|---|
| **Severity** | Medium |
| **File** | `seva_benchmark_4060.py` lines ~507-508 |
| **Code** | `tq` has 25 entries; `for i in range(50): tq[i % len(tq)]` |
| **Fix** | Paper: disclose "25 unique queries x 2"; or code: expand `tq` to 50 unique entries |

---

### CF-008 — Benign query construction couples queries to corpus docs

| | |
|---|---|
| **Severity** | Medium |
| **File** | `seva_benchmark_4060.py` lines ~511-515 |
| **Issue** | Each benign query is the first sentence of a randomly selected corpus doc, creating tight retrieval coupling that deflates FPR |
| **Fix** | Code: use an independent benign query set; or paper: quantify and bound the effect |

---

### CF-009 — Benign query pool hardcoded to seed 42 across all three seeds

| | |
|---|---|
| **Severity** | High |
| **File** | `seva_benchmark_4060.py` line ~516 |
| **Code** | `rng = np.random.default_rng(42)` — hardcoded, same for all three experiment seeds |
| **Paper claim** | Results reported as "3 independent random seeds" |
| **Impact** | Seeds differ only in the 60/40 cal/eval split partition; FPR variance does not reflect query-sampling variance |
| **Fix** | Change `np.random.default_rng(42)` to `np.random.default_rng(self.cal_seed)` and re-run experiments |

---

### W-002 — K_FETCH = 20 over-fetch not disclosed in paper

| | |
|---|---|
| **Severity** | Low-Medium |
| **File** | `seva_benchmark_4060.py` constant `K_FETCH = 20` |
| **Paper claim** | §IV-B: "retrieve K=5 nearest neighbours" — over-fetch factor not mentioned |
| **Fix** | Paper: disclose K_FETCH=20 in retrieval description |

---

### W-007 — NORM_PERCENTILE = 90 not disclosed in paper

| | |
|---|---|
| **Severity** | Low-Medium |
| **File** | `seva_benchmark_4060.py` constant `NORM_PERCENTILE = 90` |
| **Paper claim** | §IV-B describes normalisation but omits the percentile value |
| **Fix** | Paper: add "90th percentile" to normalisation description |

---

*Last updated: 2026-04-30 — SEVA v6.2.3 audit.*

---

## OPEN (added 2026-08-16, from the TDSC-review verification pass)

- **KI-010 — calibration: harness vs deployment.** `reproduction/hardgate_xrun.py:210` (and the
  equivalent line in `scale_xrun.py`) computes `tau = percentile(ccoh, ...)` where `ccoh = coh[P:]`,
  i.e. the quantile is taken over the corpus's benign partition, which the harness knows by
  construction. This uses no labelled poison, no poison scores and no density estimate, so the
  non-oracle claim holds in those senses; but a deployment has no benign partition and would take
  the quantile over the scores its benign query stream returns. §4.3 of both papers now states the
  distinction explicitly. **The label-free estimator has not been measured.** Closing this means
  running it and reporting whether the gate holds.

- **KI-011 — clone-attack multiplicity.** The boundary headline (100% poison-evasion) is the
  one-clone-per-target configuration. At V=5, the multiplicity the threat model fixes for the
  *templated* attack, `whitebox_attack_results/expA2_cloneonly_s042.json` records catch rising to
  22.7% (evasion 77.3%). §5.10 now reports the sweep rather than the single cell.

- **KI-012 — clone rows of the head-to-head are unreported.** `whitebox_attack_results/e4hh_s042.json`
  contains five `cloneinject_n*` rows in which RAGDefender catches 57-71% of host-anchored clones
  against SEVA's 11-13%, at RAGDefender's 51.2% benign strip rate. The templated row of the same
  file is reported in the paper; the clone rows are not. Unresolved editorial decision.

- **KI-013 — Observation 2 is a measurement, not a rate result.** The DKW bound is 12-18x wider
  than the realized deviation at every N, and the three measured deviations do not follow the
  predicted 1/sqrt(n) decay (ratios 4.74 and 1.47 against 3.16). Both papers now report the
  direction only and fit no exponent.

- **KI-014 — clone paraphraser differs from the answering generator.** Host-anchored clones are
  rewritten with `mistral:7b-instruct` because `gpt-oss:20b` loops on the rewrite prompt; the
  answering generator and corruption judge remain `gpt-oss:20b` at temperature 0, so the potency
  comparison holds targets, judge and criterion fixed. Now disclosed in the main text of both
  papers, not only the supplement.
