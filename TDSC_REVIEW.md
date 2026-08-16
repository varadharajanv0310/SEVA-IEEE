# Review — *SEVA: Lightweight, LLM-Free Detection of Templated Corpus Poisoning in RAG*

**Venue:** IEEE Transactions on Dependable and Secure Computing
**Manuscript under review:** `SEVA_tdsc.tex` / `.pdf` (12 pp., IEEEtran `[10pt,journal,compsoc]`)
**Also consulted:** `SEVA_arxiv.tex` (21 pp.), `RESULTS.md`, `HOW_TO_REPRODUCE.md`, `KNOWN_ISSUES.md`,
`PAPER_EDITS_LOG.md`, `reproduction/*.json`, `results/in_domain/*.json`, `whitebox_attack_results/*.json`,
and the `exp*.py` / `pr_*.py` / `e4hh_*.py` sources.

---

## 1. Recommendation

### **Major revision**

The measurement programme behind this paper is real, unusually extensive, and better instrumented than
most of what this area publishes: the corpus and poison are hash-gated, the cross-platform agreement
claim holds when I check it (max |Δgap| = 4.17×10⁻⁷ across 9 cells), the primary in-domain grid
reproduces exactly from the committed JSON, and the authors have gone out of their way to run and
release the experiment that breaks their own defense. I want that work in the literature. But the
manuscript cannot be accepted in its current form, for one reason above all others: **the repository
contains a measurement that directly contradicts the paper's headline conceptual contribution, and the
paper does not report it.** Contribution C4 — the claim that the host-anchored-cloning blind spot
"belongs to the cohesion-detection family, not SEVA alone" — is supported in the paper by a single
CleanBase reproduction (another *corpus-level cohesion* detector, i.e. the most similar possible
witness). Meanwhile `whitebox_attack_results/e4hh_s042.json`, which `RESULTS.md` maps to the
head-to-head table, records RAGDefender catching **57–71%** of exactly those clones where SEVA catches
**11–13%**. That file is cited in the claim map; the templated half of it is reported; the clone half,
where the baseline beats SEVA five-fold, is not in either the 12-page or the 21-page version. Beyond
that, four headline numbers disagree with the artifacts they are mapped to or come from a different
detector than the one the abstract describes, including the 18% comparator on which the paper's most
consequential claim ("the bypass is not expensive") rests — the file and the run log both say 22%. None
of this requires new science to fix: the experiments already exist, and most of the corrections are
re-derivation from released data plus honest rewriting. That is a major revision, not a rejection. But
the corrected paper is a different and more modest paper than this one, and I would want to see it
before recommending acceptance.

---

## 2. Summary of the paper (in my words)

SEVA is a corpus-poisoning detector for RAG built on one statistic: for each document *d*, take its
K = 5 nearest neighbours **in the corpus** and average the pairwise cosines among them
(`cluster_coh`). Templated multi-passage poisoning of the PoisonedRAG kind injects several passages per
target query from a shared recipe, so those passages are each other's nearest neighbours and their
coherence approaches 1, while organic in-domain text sits near 0.75. SEVA thresholds this at a τ
calibrated to a 0.69% target false-positive rate on clean coherence, drops documents above τ, and flags
a query when ≥2 of its retrieved documents are flagged. The statistic is precomputed once per corpus,
so the per-query cost is a table lookup and a comparison — no LLM, no API, no provenance registry, which
is the deployability argument.

The paper's empirical spine is: (i) an in-domain Security Stack Exchange corpus, chosen so that clean
and poison share a domain and a geometric detector gets no topic shortcut; (ii) 0% templated
poison-evasion across 3 densities × 3 calibration seeds at ~0.56–0.58% document-FPR; (iii) detection of
PoisonedRAG's released poison on NQ (82%) and HotpotQA (97%) plus a Security-corpus build (98%);
(iv) three "invariance" observations — density, calibration-scaling, encoder; (v) a cross-platform
reproducibility result to 5×10⁻⁷ and a million-document scale run.

What makes the paper more interesting than "we built a detector" is the second half. The authors
concede the cohesion signal is not novel (CleanBase, SeCon-RAG, GRADA, TopoGuard, hubness detection all
sit nearby) and reposition the contribution as *characterizing and delimiting the family's envelope*.
They then attack their own defense: host-anchored cloning — paraphrase the target's top-ranked benign
document, splice in the payload, repeat per target with a *different* host each time — puts each
injected passage inside a different benign neighbourhood, so its coherence never leaves the clean band.
They report that this evades the gate on every target while staying retrievable, that the obvious
complementary signal (nearest-neighbour duplication) does not recover it, that a reproduced CleanBase
fails identically, and — the sharpest claim — that the bypass is *not* expensive: it corrupts 26–28% of
targets end to end, more than the 18% the templated attack achieves undefended. The paper's own summary
of what an operator buys is "a filter for known attack structure, not a security boundary."

**What actually landed versus what I think the authors think they wrote.** The deployability envelope,
the in-domain framing, the encoder and cross-platform work, and the intellectual honesty of the
boundary section all land, and land well. Three things do not land as written. First, the *scope* of
the boundary claim: the paper argues the blind spot is the family's, but the only witness it reports is
the one detector most structurally identical to SEVA, while its own data show a per-query filter
catching the clones far better. Second, the *quantitative* boundary claim: the "26% vs 18%, the bypass
is more effective" comparison does not survive contact with the two files it draws on. Third, the
*headline operating point*: the abstract's "0% evasion at 0.58% doc-FPR" mixes the deployed hard gate's
grid result (0.56%) with a single-seed, single-density run of the **composite ablation** that the paper
elsewhere disowns. The paper reads as more finished than it is, precisely because the artifact
discipline is good enough that a reviewer can check — and several checks fail.

---

## 3. Major issues

Ranked by how much each threatens acceptance.

---

### M1 — The paper's central conceptual claim (C4) is contradicted by a released file it cites, and the contradicting half is unreported

**Claim.** Abstract: "Reproducing CleanBase, the closest corpus-level peer, at a matched operating point
yields the same pattern (100% templated, 0% clones), so the boundary belongs to the shared
mutual-similarity assumption rather than to our statistic." C4 and §5.10 generalize this to "the
cohesion-detection family." Limitations: "this is a property of the mutual-similarity assumption—and of
the cohesion-detection family, not SEVA alone."

**Evidence I checked.** `whitebox_attack_results/e4hh_s042.json`, which `RESULTS.md:26` maps to the
head-to-head table:

```
ragd_benign_doc_fpr = 51.2   embedder = BAAI/bge-large-en-v1.5   task = single_hop
cloneinject_n1  seva_catch 10.98%   ragd_catch 70.73%
cloneinject_n2  seva_catch 12.90%   ragd_catch 63.71%
cloneinject_n3  seva_catch 12.41%   ragd_catch 57.24%
cloneinject_n5  seva_catch 12.27%   ragd_catch 58.28%
cloneinject_n8  seva_catch 12.57%   ragd_catch 57.14%
templated       seva_catch 100.0%   ragd_catch 81.15%
```

I grepped both `SEVA_tdsc.tex` and `SEVA_arxiv.tex` for `cloneinject`, `70.7`, `57.2`, `63.7`, and
"RAGDefender … clone": no occurrences. The paper reports this file's **templated** row (SEVA 100% vs
RAGDefender ~89% at matched FPR) and omits the five **clone** rows, which are the only rows where the
baseline beats SEVA — by a factor of 4.6–6.4×.

**Why it is a problem.** The paper's repositioning — "we don't claim the signal, we claim the envelope"
— stands or falls on the generality of the blind spot. As reported, the generalization rests on one
witness, CleanBase, which is a *corpus-level clique detector over a similarity graph*: the detector
whose assumptions overlap SEVA's most completely. Two corpus-level cohesion statistics agreeing that
host-anchored clones are invisible is close to a tautology — clones are constructed precisely to sit in
clean neighbourhoods, which is the input both statistics read. Meanwhile the authors possess a
measurement showing that a **per-query density filter**, from a *different* branch of the taxonomy in
their own Table 1, recovers 57–71% of those clones. That is a counterexample to "the boundary belongs
to the family," and it is in the file the claim map points at.

There is a legitimate rebuttal — RAGDefender achieves it at a 51.2% benign strip rate, which is not
deployable — but that is a *different* claim ("no deployable defense closes it") and a much weaker one
than the paper makes. It also cuts against the paper's own framing of per-query filters as structurally
blind ("a view a per-query filter structurally cannot reconstruct," §7.1): on the attack that matters,
the per-query view is the one that sees.

Not reporting the one measurement in your repository where the baseline beats you, on the exact claim
you are staking your novelty on, is the issue most likely to sink this paper with a TDSC AE. I do not
read it as deliberate — the file's templated row is reported and the clone rows sit further down the
same JSON — but the effect is selective reporting on the central claim.

**What would fix it.** Report the full `e4hh_s042.json` table, clones included, in the main paper. Then
either (a) narrow C4 to what the data support — "the blind spot is shared by *corpus-level* cohesion
detectors (SEVA, CleanBase); a per-query density filter recovers 57–71% of clones but only at a 51%
benign strip rate, so no *deployable* detector we tested closes it" — or (b) do the extra work to
support the broader claim: run GRADA and TopoGuard (both LLM-free, both with public methods) on the
same clone set. Option (a) is writing plus a table; option (b) is roughly a day of compute on the
existing corpus. **Option (a) is the honest minimum and I would accept it.** It makes the paper's story
sharper, not weaker: the boundary is specifically a *corpus-level cohesion* boundary, and the escape
route costs half your corpus.

---

### M2 — The comparator carrying the paper's most consequential claim disagrees with its own artifact and run log (18% vs 22%), and the associated evasion figure is multiplicity-dependent in a way the text denies

This is two linked defects in the boundary section (§5.10, C4, Discussion §7.3, Limitations, abstract,
conclusion).

#### M2a — "18% undefended" is 22% in the file and in the log

**Claim.** §5.11: "Undefended, the attack corrupts 18% of the 50 targets and places 2.74 poison passages
in the average retrieval window." §5.10: "the templated attack the gate does stop reaches only 18%
undefended." Abstract: "the templated attack corrupts 18% of targets undefended." Also `RESULTS.md:75`
and the retraction entry at `PAPER_EDITS_LOG.md:763`.

**Evidence I checked.** `whitebox_attack_results/expA1_endtoend_s042.json`:

```
"mean_poison_in_topK": {"undefended": 2.74, "defended": 0.0}          <- 2.74 agrees
"corrupted": {"undefended": 11, "defended": 0,
              "undefended_pct": 22.0, "defended_pct": 0.0}            <- 22.0, not 18.0
```

Recounting `per_query` independently: 11 of 50 have `corrupted_undefended: true` → 22.0%. The run log
`expA1.log` says so in plain text: `END-TO-END: corrupted undefended 11/50 (22.0%) -> defended 0/50
(0.0%) | poison in top-K 2.74 -> 0.00`. The 2.74 in the same sentence of the paper is correct, so this
is a transcription error against a file the paper otherwise reads correctly.

**Why it is a problem.** 18% is not an incidental number. It is the denominator of the paper's most
rhetorically loaded claim — that the bypass "corrupts *more* targets end to end than the templated
attack it replaces" — repeated in the abstract, C4, §5.10, §7.3, Limitations, and the Conclusion. It is
also the number on which the authors rebuilt the section after retracting the earlier cost-of-evasion
claim (`PAPER_EDITS_LOG.md:767`). Correcting to 22% narrows the headline gap from 26 − 18 = 8 points to
26 − 22 = 4 points. The direction survives; the emphasis should not.

#### M2b — "evades on every target" is the V = 1 cell only; at the threat model's own V = 5 the gate catches 22.7%

**Claim.** §5.10: "Clone cohesion averages 0.751 against τ = 0.841—below the gate for *every* one of 50
targets (100% poison-evasion) … Multiplicity does not rescue detection: 1 to 5 clones per target moves
mean cohesion only from 0.722 to 0.790."

**Evidence I checked.** `whitebox_attack_results/expA2_cloneonly_s042.json`, the file `RESULTS.md:69`
maps the multiplicity sweep to. The two cohesion endpoints the paper quotes are exactly right. The
column beside them is not quoted:

| clones/target | clone_coh_mean | **coh_catch_pct** | coh_EVASION_pct | snd_catch | union gate |
|---|---|---|---|---|---|
| 1 | 0.7218 | **0.0** | 100.0 | 20.0 | 13.3 |
| 2 | 0.7458 | **0.0** | 100.0 | 13.3 | 6.7 |
| 3 | 0.7722 | **11.1** | 88.9 | 13.3 | 20.0 |
| 5 | 0.7901 | **22.7** | 77.3 | 18.7 | 33.3 |

The paper's "s_nd catches only 13–20%" and "union gate reaches just 6.7–33.3%" are both read off this
table correctly, across the whole sweep. The `coh_catch_pct` column from the same rows is not reported,
and it contradicts the sentence it sits under: multiplicity moves the gate's catch rate from 0% to
22.7%. So the paper quotes the *range* of the sweep for the signals that fail, and the *best single
cell* for the signal that is its own.

This matters because §3 fixes the threat model at **V = 5** ("Following the released PoisonedRAG
construction, each target query receives V = 5 injected passages"). At the paper's own V, clone evasion
is 77.3%, not 100%, and the union gate catches a third of clones. Independently,
`expA_snd_vs_paraclone_s042.json` (75 clones = V = 5) records `coh_catch_pct: 70.67` and
`two_signal_union_gate/paraphrase_clone_catch_pct: 66.67` in the corpus that also contains the
templated poison. "Evades on every target," "100% poison-evasion," and "no complementary geometric
signal we tested closes the gap" are all statements about V = 1.

**What would fix it.** (i) Correct 18% → 22% everywhere, including `RESULTS.md`. (ii) Report the clone
sweep as a table with the `coh_catch_pct` column present, and restate the boundary claim as it is:
*evasion is total at V = 1 and degrades to 77% at V = 5; the union gate recovers 6.7–33.3% depending on
multiplicity*. (iii) Say plainly that the headline "100%" is the V = 1 cell. Writing only — every number
is already in the repo. The corrected claim is still a strong negative result and still supports the
paper's thesis; it just cannot be stated with "every."

---

### M3 — The headline false-positive rate (0.58%) comes from the composite ablation, one seed, one density, and is absent from the claim map

**Claim.** "0% poison-evasion … at a 0.58% document-level false-positive rate" (abstract); "0%
poison-evasion across three seeds and 0.58% document-FPR under frozen, non-oracle calibration" (C2);
repeated in §4.3, §5.3, and the Conclusion. This is the paper's most-repeated single number.

**Evidence I checked.** `RESULTS.md:19` maps `tab:main` to the nine `results/in_domain/*.json` files and
quotes "0.58%/0.56% Doc-FPR". Aggregating those nine files myself:

```
GRAND MEAN L1 doc_fpr = 0.5617%     per-condition max = 0.829% (5% density, seed 7)
```

0.56% and the 0.83% maximum both check out. There is no 0.58% in the L1 rows. Hunting the repository,
0.58% traces to `whitebox_attack_results/linchpin_s042.json`:

```
"mode": "linchpin", "half_A": 2500, "half_B": 2500,
"stepA_tau_L1": 0.5870119035243986,
"L1": {"asr": 0.0, "doc_fpr": 0.5764411027568922,
       "counts": {"TP": 112, "FN": 0, "FP": 23, "TN": 3967, "poison_encounters": 112}}
```

Three problems. **(a) Wrong detector.** τ = 0.587 with `L1/weights/cluster_coh = 0.154` — this is the
**ten-signal composite** at L1, the thing §4.5 explicitly demotes to "the ablation that quantifies what
the soft signals cost." The deployed detector is the hard gate at τ ≈ 0.84. The abstract presents 0.58%
as the operating point of the detector it is selling. **(b) Wrong scope.** 112 poison encounters, seed
42, one density — while the sentence around it says "across three seeds." **(c) Not in the claim map.**
`grep -c linchpin RESULTS.md HOW_TO_REPRODUCE.md` returns 0 and 0. The single number the paper repeats
most often is the one number a reader cannot trace through the released map.

**Why it is a problem.** For a submission whose stated methodological contribution (C5) is traceability
and non-oracle rigor, having the headline FPR be (i) from the ablation rather than the deployed
detector, (ii) from one cell rather than nine, and (iii) untraceable through the released map, is
exactly the kind of thing a TDSC reviewer is obliged to catch. It also creates a real ambiguity: a
reader cannot tell whether the abstract's "0% poison-evasion at 0.58% FPR" describes the hard gate or
the composite.

**What would fix it.** Report the deployed hard gate's number — **0.56% grand mean, per-condition
0.40–0.83%, n = 9 cells** — in the abstract, C2 and the Conclusion. Keep the frozen disjoint-reference
run as the separate generalization check it is, state that it is the composite at L1 over 112
encounters at seed 42, and add `linchpin_s042.json` to `RESULTS.md`. Writing only.

---

### M4 — The Wilson bound: the arithmetic is right, the experimental condition is undisclosed, and the independence assumption is wrong

**Claim.** Abstract and §5.2: "a 95% Wilson upper bound of 0.0154% from 25,000 templated encounters at
the frozen gate," "0 evasions in 25,000."

**Arithmetic — verified.** For k = 0 the Wilson upper bound collapses to z²/(n + z²). With z = 1.96,
n = 25,000: 3.8416/25003.84 = **1.5364×10⁻⁴ = 0.01536%**. `reproduction/result_hienc_ci.json` records
`wilson_upper_pct: 0.015364039100295693` with `wilson_z: 1.96`. Agrees to five significant figures. No
issue here.

**Problem 1 — the density is disclosed nowhere.** The same file records:

```
"density_pct": 25.0,
"encounter_def": "each of 25k templated-poison docs scored by the frozen hard gate (coh<=tau=evasion);
                  injected at corpus[0:25000] of the 100k canonical corpus; tau from clean remainder."
```

I grepped both `SEVA_tdsc.tex` and `SEVA_arxiv.tex` for `25{,}000` and `high-encounter`: neither
version states that this run sits at **25% contamination**. The paper's evaluated band is 1–10%, and
Observation 1's density-invariance is explicitly scoped to "the evaluated 1–10% range, which we neither
evaluate beyond nor extrapolate." The tightest uncertainty claim in the abstract therefore comes from a
condition 2.5× outside the range the paper says it evaluated, and a reader of either version cannot
know.

**Problem 2 — 25,000 poison documents are not 25,000 independent trials.** A Wilson interval is a
binomial interval; it assumes i.i.d. Bernoulli draws. These 25,000 documents come from one
deterministic generator (`xplat_poison_gen.generate_corpus(25000)`), against one corpus, at one seed,
scored by one frozen τ. They are massively positively correlated by construction — that correlation is
the very signal the detector reads. The effective sample size is nearer the number of independent
*template families / corpora / seeds* than 25,000, and the real uncertainty is dominated by
generator-and-corpus variation, not by n. Reporting 0.0154% as a 95% bound on evasion invites the
reader to believe the residual risk is bounded at ~1.5 in 10,000 for this attack class, which the
experiment cannot support. This is textbook pseudo-replication, and in a security venue it is the kind
of over-precision that gets a paper's headline quoted back at it.

**Problem 3 (flagged, not resolved — see §7).** The same file records
`tau_recal_on_poisoned_corpus: 0.9766824861109247` against `poison_coh_min: 0.8905`. That is the
authors' own note that at 25% density a threshold re-derived on the poisoned corpus lands *above* the
minimum poison coherence. See M9 for what I did and did not verify here.

**What would fix it.** (i) State the 25% density wherever the 25,000 encounters are mentioned, in both
versions, and say why a density outside the evaluated band was chosen. (ii) Either drop the binomial
interval or replace it with an uncertainty statement whose unit of replication is the thing that
actually varies. The cheapest defensible version: regenerate poison under *m* independent generator
seeds (m = 5–10, minutes of compute on the existing corpus), report evasion per seed, and give a
bound over seeds. (iii) If the binomial number is kept for continuity, label it explicitly as
conditional on one corpus and one generator draw.

---

### M5 — The single most informative ablation for the paper's threat model exists in the repo and is reported in neither version

**Claim.** §3 scopes SEVA to "templated, multi-passage, clustered injection" and puts single-document
mimicry out of scope. §7.3: "Attacks that preserve the shared-recipe structure cannot [evade]." The
implication throughout is a clean boundary: multi-passage ⇒ detected, single-document ⇒ out of scope.

**Evidence I checked.** `whitebox_attack_results/pr_gate_s042.json` sweeps injection multiplicity on
the in-domain black-box PoisonedRAG build:

| V | Pn | reach | poison coh median | **cluster_coh catch** | composite L1 catch | s_nd catch |
|---|---|---|---|---|---|---|
| 1 | 50 | 82% | 0.827 | **48.0%** | 74.0% | 18.0% |
| 3 | 150 | 92% | 0.856 | **60.0%** | 64.0% | 94.0% |
| 5 | 250 | 100% | 0.903 | **98.0%** | 66.0% | 98.0% |
| 10 | 500 | 96% | 0.965 | **100.0%** | 78.0% | 100.0% |

The paper reports only the V = 5 cell (98%). Neither version reports the sweep.

**Why it is a problem.** This table is the most directly informative measurement in the whole repository
about *where the threat model's boundary actually is*, and it shows the boundary is a gradient, not a
cliff: detection degrades from 100% → 98% → 60% → 48% as V falls from 10 to 1. Three consequences.
First, it makes the scoping decision in §3 look considerably more like drawing the line around the wins
than it needs to — the reviewer's natural suspicion, which this table would have honestly pre-empted.
Second, it quantifies the threat from CorruptRAG-class single-injection attacks, which the paper cites
as out of scope but never measures: at V = 1 the gate is at 48%, i.e. barely better than a coin flip on
retrieved poison. Third, it is the strongest available evidence *for* the paper's own mechanism —
detection tracks multiplicity exactly as the cluster story predicts. Withholding it costs the paper
more than reporting it would.

I note the composite L1 column is non-monotone and beats the hard gate at V = 1 (74% vs 48%) and V = 3
(64% vs 60%). That is worth a sentence too; the paper's "the soft signals do not merely fail to help;
they *dilute*" (§5.9) is stated without the qualification that at low multiplicity they help.

**What would fix it.** Put the V-sweep in the paper (it is four rows) and rewrite §3's Out-of-Scope
paragraph to describe a measured gradient rather than a categorical exclusion. Writing only; the data
exist.

---

### M6 — "The authors' released attack code" is a re-implementation with a changed prompt and a different generator

**Claim.** §5.1: "the in-domain corpus additionally receives a faithful black-box PoisonedRAG generated
with the authors' released attack code." §5.6: "a faithful black-box PoisonedRAG, built with the
authors' *released* attack code, on the in-domain Security corpus." §5.6 leans on this: "Released poison
removes any question of a favourable re-implementation."

**Evidence I checked.** `pr_gen.py` line 8 is headed *"DISCLOSED prompt adaptation"*; it imports
payloads from the authors' own `whitebox_attack_seva.py`, not from the PoisonedRAG repository (a clone
of which sits unused at `../poisonedrag_repo/`), and generates with Ollama. The provenance block written
into `pr_gate_s042.json` says so:

```
"construction": "PoisonedRAG LM_targeted black-box: P=Q(verbatim)+I; documentation-style gen (DISCLOSED);
                 I varied via temp=0.8; empties/refusals dropped"
"V_GEN": 10, "N_WORDS": 55, "temp": 0.8, "generator": "gpt-oss:20b"
"prompt": "Write a concise technical knowledge-base entry ... in an authoritative documentation style
           with specific concrete details."
```

`PAPER_EDITS_LOG.md:438` is explicit: *"DISCLOSED reimpl: documentation-style prompt (gpt-oss refuses
PoisonedRAG's literal 'make the answer false' framing) + generator gpt-oss:20b≠GPT-4."*

**Why it is a problem.** The NQ and HotpotQA results genuinely do use PoisonedRAG's released passages,
and that is a real strength. The Security result does not — and it is the corpus that yields the highest
number (98%), the one used in the head-to-head, the geometric-core comparison, and the lexical-fragility
argument. The substitution is not neutral: an "authoritative documentation style with specific concrete
details" prompt at temperature 0.8, generating 10 passages per query from one template, is a
construction one would *expect* to raise mutual similarity, which is precisely the quantity the detector
reads. The authors know this is a reimplementation and documented it in their own log; the paper says
"released attack code" twice. That is a factual misstatement about provenance on the paper's strongest
number, and it undercuts exactly the objection the sentence is there to foreclose.

**What would fix it.** Say what was done: "a black-box PoisonedRAG build following the released
`LM_targeted` construction, with a disclosed prompt adaptation and gpt-oss:20b in place of GPT-4,
because the literal PoisonedRAG instruction is refused by the local model." Then add the one control
that neutralizes the concern: report sibling mutual similarity for the re-implementation against the
released NQ/HotpotQA poison, so a reader can see whether the substitution inflated cohesion. The edits
log already records `sibling word-Jaccard 0.444, shared-hook fraction 0.14` — surface it. Writing plus
one cheap measurement.

---

### M7 — The RAGDefender head-to-head compares against two different systems, only one of which is RAGDefender

**Claim.** §5.8 and C5: "the first *reproduced*—not number-lifted—matched-FPR head-to-head with the
LLM-free per-query state of the art (SEVA 100% vs ~89%)." Also: "its grouping step always partitions a
retrieval window and removes a side, so on benign in-domain queries it strips 50.4% of clean documents."

**Evidence I checked.** `e4hh_fair.py` runs two different checks:

- **CHECK 1** uses RAGDefender's actual implementation — `from ragdefender.grouping import
  ClusteringBasedGrouping`, then `grp.estimate_n_adv(...)` on clean retrieval sets. This produces the
  50.4%-strip finding. Genuine reproduction.
- **CHECK 2**, which produces the 89%, does *not* use RAGDefender's filter. It defines its own
  statistic:
  ```python
  def smean(R):
      E = enc.encode(R, ...); S = E @ E.T; k = len(R)
      return [float((S[i].sum() - S[i,i]) / (k-1)) ... ]
  ```
  and sweeps a threshold on it. `smean` is the mean cosine of each retrieved document to the others in
  its window — i.e. **a per-query version of SEVA's own cluster coherence**, not RAGDefender's
  clustering-based grouping.

The paper does disclose that a threshold was granted ("we grant it an idealized threshold its actual
filter does not expose") and that the matched FPR is looser (~0.8% vs SEVA's ~0.6%; the file confirms
`benign_fpr_actual: 0.8`). Both disclosures are honest and I credit them.

**Why it is still a problem.** "Grant an idealized threshold" understates the substitution. What was
measured is not RAGDefender-with-a-knob; it is a different statistic, from SEVA's own family, evaluated
per-window. So the paper attributes 89% to a named published system whose algorithm did not produce it,
while attributing 50.4% to the same name from the real algorithm. Those are two different systems under
one label, and C5's "reproduced—not number-lifted" claim covers only half of the comparison.

The irony is that CHECK 2 is *scientifically better* than testing RAGDefender's real filter: a
per-window mean-similarity ablation of SEVA's own statistic is the cleanest possible isolation of the
corpus-level-vs-per-query question, and it supports the paper's structural conclusion (§5.8) exactly.
The fix is labelling, not new work.

**What would fix it.** Relabel CHECK 2 as what it is — *a per-query ablation of cluster coherence*,
which is the honest and stronger framing — and restrict "reproduced RAGDefender" to CHECK 1 and the
strip-rate result. Adjust C5 accordingly. Writing only. (Also reconcile 50.4% with the file's
`ragd_benign_doc_fpr: 51.2`; see minor issues.)

---

### M8 — Observation 2 is an over-claim: the DKW bound does not constrain the data, the measured points do not follow the predicted rate, and all three deviations are inside one standard error

**Claim.** Observation 2: "The realized non-oracle document false-positive rate converges toward the
calibration target as the clean calibration corpus grows; its deviation from the target shrinks with
corpus size," with a DKW derivation giving "O(1/√n)."

**Numbers — verified.** `result_scale10k.json` / `result_scale100k.json` / `result_1M.json` give grand
means 0.7653% / 0.6741% / 0.7008%, deviations 0.0753 / 0.0159 / 0.0108 pp. All three match the paper.

**What the analysis actually shows.** I computed the DKW bound and the sampling error of a single cell
at each N:

| N | realized FPR | deviation (pp) | DKW 95% bound (pp) | 1-cell SE (pp) | eval n |
|---|---|---|---|---|---|
| 10,000 | 0.7653% | 0.0753 | 1.3581 | 0.1315 | 3,960 |
| 100,000 | 0.6741% | 0.0159 | 0.4295 | 0.0416 | 39,600 |
| 1,000,000 | 0.7008% | 0.0108 | 0.1358 | 0.0132 | 396,000 |

Three things follow.

1. **The bound is 12–18× looser than the observations at every point.** It excludes nothing that was
   measured; it would have been satisfied by data an order of magnitude worse. The paper concedes the
   bound is "distribution-free and hence loose" but then says "we report it for the rate it predicts,
   which is the trend the three measured points follow." They do not follow it: the observed ratios are
   **4.74** (10k→100k) and **1.47** (100k→1M), against 1/√10 = 3.16 — overshooting then undershooting.
2. **Every deviation is smaller than one standard error of a single cell's own FPR estimate**
   (0.0753 < 0.1315; 0.0159 < 0.0416; 0.0108 ≈ 0.0132). What the data show is that the plug-in quantile
   estimator is unbiased and hits target at all three sizes — a true and useful statement. What they
   cannot show is a *rate*, because the "shrinking deviation" is indistinguishable from the Monte-Carlo
   noise of the measurement itself shrinking with n. That is a 1/√n effect, but the trivial one.
3. **There are effectively two comparable points, not three.** The paper states that the 1M run uses a
   broader ten-site corpus and is therefore "direction, not a fitted exponent" — good, but that
   concession removes the third point from the scaling argument entirely, leaving one interval.

Separately, the derivation as written applies the DKW deviation of the *calibration* empirical CDF to a
false-positive rate measured on a *held-out* eval split. Those are two samples; the stated chain
`|FPR(τ) − α| ≤ sup_x |F_n(x) − F(x)| ≤ (ln(2/δ)/2n)^{1/2}` needs a second term or a union bound to be
correct as an inequality.

**Why it is a problem.** Observation 2 is presented as one of three formal "invariance" properties, with
a named theorem behind it. What is actually established is "the non-oracle calibration hits its 0.69%
target at 10k, 100k and 1M." That is worth reporting and is entirely sufficient for the deployability
argument. Dressing it as a scaling law with a distribution-free bound that constrains nothing invites a
statistically literate reviewer to discount the other two observations by association.

**What would fix it.** Demote Observation 2 to a measurement: "realized FPR tracks the target to within
0.08 pp at every corpus size tested; the deviation is within sampling error at all three points." Keep
the DKW remark as a one-line motivation for *why* one should expect the plug-in threshold to be
consistent, explicitly not as a rate claim, and fix the two-sample gap. If a rate claim is wanted, it
needs ≥5 sizes on one corpus family with repeated draws per size — a few hours of compute at 10k–100k,
but I do not think it is worth it. Writing only, if demoted.

---

### M9 — Calibration is described one way in the paper and implemented another; the label-free variant works at 1–10% but is not the one that produced the numbers

**Claim.** §4.3: "benign queries are issued against the (possibly poisoned) corpus; for every retrieved
document the detection score is computed, and τ is set to the (1−FPR_TARGET) quantile of the resulting
clean-score distribution by 50-iteration binary search." Framed throughout as "non-oracle" — "no
labeled poison and no oracle knowledge of the contamination density."

**Evidence I checked.** Every headline number comes from code that consumes ground-truth poison labels:

- `reproduction/hardgate_xrun.py:210` — `tau = float(np.percentile(ccoh, 100 - C.FPR_TARGET*100))`
  where `pcoh, ccoh = coh[:P], coh[P:]`. τ is the quantile over the **ground-truth-clean partition of
  the whole corpus**, identified by index. This is not "benign queries issued against the corpus" at
  all.
- `reproduction/scale_xrun.py:89` — same, on the calibration half.
- `seva_benchmark_4060.py:793–794` — calibration does run over benign-query retrievals, but then
  `cal_labels = [... corpus[i]["is_poisoned"]]; cal_clean = ~cal_labels`, and calibration uses
  `scores[cal_clean]`. The comment rationalizes it ("benign queries only, so clean = not poisoned"),
  but the label is still read.

**What I tested.** Using the released cached coherence arrays plus the released benign query
embeddings, I compared three thresholds at each density on the 100k corpus:

```
dens | tau(clean-LABEL)  ev    docFPR | tau(benign-retrieval, NO label)  ev | poison in cal-sample
  1% |   0.8425        0.00%   0.691% |   0.8439                       0.00% |  1/10000 = 0.01%
  5% |   0.8408        0.00%   0.691% |   0.8440                       0.00% | 13/10000 = 0.13%
 10% |   0.8403        0.00%   0.690% |   0.8505                       0.00% | 34/10000 = 0.34%
```

**The paper's described procedure works.** Benign queries pull in 0.01–0.34% poison — below the 0.69%
target quantile — so the tail stays clean-dominated and evasion remains 0% without any label. I want to
be clear that this substantially defuses what I initially took to be the paper's most serious problem,
and I report it as a positive finding. (The benchmark path is likewise near-immune: the run log
`step3_baseline_secqa_s42.log` records `Cal records: 6000 (5999 clean, 1 poison)` / `(5994, 6)` /
`(5963, 37)` at the three densities.)

**What remains a problem.** Three things.

1. **The released code does not implement the paper's stated method.** For a submission whose C5 is
   methodological rigor and whose selling point is a hash-gated reproducible pipeline, the calibration
   procedure in §4.3 and the calibration procedure in `hardgate_xrun.py` are not the same procedure.
   A reader reproducing from `HOW_TO_REPRODUCE.md` §1 runs the label-consuming path.
2. **The label-free τ is not density-agnostic.** It drifts 0.8439 → 0.8440 → 0.8505 as density goes
   1% → 5% → 10%, whereas the label-based τ drifts the other way (0.8425 → 0.8403). The paper claims
   density-agnostic calibration; what the label-free data show is a threshold that rises with
   contamination and simply has not risen far enough to matter by 10%.
3. **The margin is not established at the density of the paper's own headline CI run.** For contrast,
   with no labels at all (quantile over the whole poisoned corpus, which is what an operator with no
   clean reference has) the gate fails outright:
   ```
   dens  1%: tau=0.9849 -> evasion 31.20%
   dens  5%: tau=0.9966 -> evasion 86.22%
   dens 10%: tau=0.9975 -> evasion 93.12%
   ```
   That variant is a strawman — the paper never claims it — but it shows how much work the "benign
   query channel is clean" assumption is doing, and that assumption is stated in one sentence in §4.3
   without being stressed.

**Unfinished thread.** I intended to run the label-free benign-retrieval calibration at the **25%**
density of `result_hienc_ci.json` (M4), to check whether the paper's described procedure survives where
its headline confidence bound is computed. That requires recomputing `cluster_coh` over 100k documents
and I did not run it. What the authors' own file records is `tau_recal_on_poisoned_corpus: 0.9767`
against `poison_coh_min: 0.8905` — i.e. a poisoned-corpus recalibration at 25% lands *above* the weakest
poison document. Whether the *benign-retrieval* variant also breaks there is open, and given that the
threshold already drifts upward through 10%, I think it is the single most important experiment the
authors should run before resubmitting.

**What would fix it.** (i) Change `hardgate_xrun.py` and `scale_xrun.py` to calibrate on benign-query
retrievals without the label filter, and re-run the grid — my numbers say the results will not move at
1–10%, so this is cheap insurance that costs the authors nothing but compute. (ii) Report the
label-free τ drift versus density as an honest caveat on "density-agnostic." (iii) Run the label-free
variant at 25% and either report that it holds or narrow the CI claim. (iv) State the clean-query-channel
assumption as a threat-model requirement with its failure mode, not as a parenthetical. Compute:
one grid re-run (hours on one GPU) plus one 25% run.

---

### M10 — The released artifact for the boundary claim contradicts the paper, because the quantity the paper reports is never serialized

**Claim.** `RESULTS.md:62–65` maps "Clone evasion of `cluster_coh` (deployed gate) = **100%** of 50
targets; coh 0.751 vs tau 0.841", "Retrievable @K=5 = 84%", "31.0% (13/42)" and "End-to-end ASR vs
deployed gate = 26.0%" to `whitebox_attack_results/expD_deployed_gate_s042.json`.

**Evidence I checked.** That file records, at the top level:

```
"tau_coh": 0.8408008857190609,  "clean_coh_mean": 0.7501878142356873
"paraphrase": { "retrievable_pct": 84.0,            <- agrees
                "evade_coh_pct": 78.0,              <- paper says 100%
                "coh_arr": [...] }                  <- mean 0.7991, 11 of 50 above tau
"flip_check": { "n_candidates": 42, "n_flipped": 13 }
```

Computing directly from `coh_arr`: mean 0.7991, median 0.7800, and **11 of 50 clones sit above
τ = 0.8408**. Within `flip_check.results`, 5 of the 13 flips carry a `cluster_coh` above τ.

Reading `expD_deployed_gate.py` resolves it. The script computes *two* coherence arrays: `coh_par`
(against the full 100k pool, which still contains 5,000 templated poison documents that share the
payload family and pull clones upward) and `coh_par_cloneonly` (against 95k clean + clones, the corpus
the attack actually creates). The candidate set for the flip check correctly uses the clone-only
array — `ev_coh_deployed = coh_par_cloneonly < tau_coh` — so **13/42 and 26% are internally consistent
with the clone-only threat model, and my initial reading that they were inflated was wrong.** But the
JSON serializes only `coh_par`: `evade_coh_pct`, `coh_arr`, and the per-record `cluster_coh` fields are
all the contaminated-pool values. The clone-only array is computed, printed to stdout, and discarded.

**Why it is a problem.** The claim map points a reader at a file in which every visible number
contradicts the paper: 78% where the paper says 100%, 0.799 where the paper says 0.751, and five
apparently gate-caught documents counted as successes. There is no way to reconstruct the paper's
figures from the released artifact — the only corroboration anywhere is the
`expC_clone_only_pool` block in `expC_potency_s042.json` (`coh_mean: 0.7428`, `evade_coh_pct: 100.0`),
which is a *different run* with different retrievability (86% vs 84%). For a paper whose distinguishing
strength is artifact-backed traceability, its most contested claim is the one a reviewer cannot verify
from the mapped file. I spent real effort on a false trail here, and a less patient reviewer would have
written it up as fabrication.

I also note the paper's "clone cohesion averages 0.751" matches neither expD's clone-only run
(0.7428) nor expD's serialized array (0.7991); it matches `expT2b_potency_frontier_s042.json`'s
`k=1` cell (`mean_coh: 0.75176`) and coincidentally the clean mean (0.7502). The boundary paragraph
appears to draw cohesion and evasion from the prominence-frontier run and retrievability and corruption
from expD, while presenting them as one experiment.

**What would fix it.** Serialize `coh_par_cloneonly` into `expD_deployed_gate_s042.json` as the primary
array, keep `coh_par` as a clearly-labelled secondary with a note explaining the contamination, and
state in the paper which run each boundary number comes from. Re-running expD's geometry is cheap (no
LLM calls needed — only the coherence recomputation); the flip check need not be repeated.

---

### M11 — "Encoder-invariance" holds for detection but not for calibration, and the paper's own caption is more honest than its claim

**Claim.** Observation 3 and C7: templated detection holds "at preserved signal-to-noise" across bge,
e5, gte, "and the document-FPR holds near the 0.69% target."

**Evidence I checked.** `reproduction/result_encoder_{bge,e5,gte}.json`:

| encoder | clean coh | poison coh | gap | SNR | evasion | **realized doc-FPR (1/5/10%)** |
|---|---|---|---|---|---|---|
| bge | 0.7495–0.7509 | 0.987–0.994 | +0.236…+0.245 | 5.93–6.10 | 0% | 0.850 / 0.731 / 0.703 |
| e5 | 0.8650–0.8656 | 0.988–0.992 | +0.122…+0.127 | 6.43–6.66 | 0% | **0.350 / 0.251 / 0.311** |
| gte | 0.8812–0.8817 | 0.995–0.998 | +0.113…+0.117 | 5.21–5.27 | 0% | **0.984 / 0.991 / 0.725** |

The gap sequence (+0.236 → +0.123 → +0.115), the clean-coherence sequence (0.751 → 0.866 → 0.881), the
SNR band (5.2–6.7) and 0% evasion on all nine conditions per encoder all check out exactly.

**Why it is still a problem.** "The document-FPR holds near the 0.69% target" is doing too much work.
e5 realizes 0.25–0.35% — roughly *half* the target — and gte realizes up to 0.99%, roughly 1.4× it. That
is a ~4× spread between encoders in the quantity the operator is supposed to be able to set. The
paper's central deployability pitch is "an operator sets a target false-positive rate, not a guess at
how poisoned the corpus is" (§4.3); across encoders, what the operator sets and what they get differ by
a factor of four. That is a more interesting and more actionable finding than "invariance," and it is
currently buried.

I want to credit the figure caption, which is exactly right and more honest than the surrounding text:
"What generalizes is that the gate works, not that the margin is the same size on every manifold."
Promote that sentence into Observation 3 and retitle. On the prompt's question — I think "invariance"
is the wrong word for a 2× spread in absolute margin and a 4× spread in realized FPR; "the gate
transfers across encoder lineages, with encoder-dependent margin and calibration fidelity" is what was
measured. The paper's explicit disclaimer about adversarially-trained/poison-aware encoders is
appropriate and I would not push further there.

**What would fix it.** Report the realized-FPR column in `tab:encoder`, say that calibration fidelity
is encoder-dependent, and rename Observation 3. Writing only.

---

### M12 — "Three seeds" are three partitions of one query pool, and the geometry is identical across them

**Claim.** "0% poison-evasion across three seeds," "not a single lucky split: the 0% is identical at all
three seeds and every density," and mean ± sample std (n = 3) throughout `tab:main`.

**Evidence I checked.** Aggregating `results/in_domain/*.json`, within each density the
`cluster_coh` clean mean, poison mean, gap and SNR are **bit-identical across seeds 42/7/123**
(1%: 0.7518/0.9871/+0.2353/5.99 in all three files), and `poison_encounters` is identical too
(125/138/156 at 1/5/10%). Only τ and the FP counts move. Total L1 poison encounters across all nine
cells: **1,257**.

The paper does disclose the design honestly — "three calibration-partition seeds (42, 7, 123) over a
fixed pool of 2,000 benign queries" (§5.1) — and I credit that; `KNOWN_ISSUES.md` CF-009 records the
same thing. But two implications are not drawn. First, the ± values in `tab:main` are the spread over
three *partitions of one query sample*, not a sampling standard deviation, and should not be read as
one; the FP counts per cell are 15–27 out of ~3,250 encounters, so a single cell's Wilson interval
(e.g. 24/3279 → roughly 0.49–1.09%) is wider than the entire across-seed spread the table reports.
Second, "the 0% is identical at all three seeds" is guaranteed by construction once τ sits below
`poison_coh_min` — the same poison documents are scored three times with three thresholds. It is
evidence about threshold stability, not about attack-sampling variability.

**What would fix it.** State that seeds vary the calibration partition only, and that the geometry is
seed-invariant by construction. Add per-cell Wilson intervals on the FPR (they exist in the arxiv
supplement — surface the implication). If genuine replication is wanted, resample the benign query pool
per seed (`np.random.default_rng(self.cal_seed)`, one line — CF-009 already prescribes it) and
regenerate poison per seed. Writing, plus one cheap re-run if replication is wanted.

---

## 4. Minor issues

- **"Several cells bit-identical" is not supported as written.** §5.12 says "the two independently
  re-embedded external machines agree on the coherence gap to within 5×10⁻⁷, several cells
  bit-identical." Max |Δgap| between 4060 and M4 is 4.17×10⁻⁷ ✓, but **zero** of the 9 cells are
  bit-identical between those two machines. Exactly one density cell (5%) is bit-identical between the
  **5080 and M4**. If "several" counts the three seed-repeats of one density, that is a misleading way
  to count, since the gap does not depend on the seed. Restate or drop.
- **50.4% vs 51.2%.** `e4hh_s042.json` records `ragd_benign_doc_fpr: 51.2`; the paper says 50.4% in
  both versions and `RESULTS.md`. `e4hh_fair.py` CHECK 1 gives mean n_adv 2.3/5 = 46%. Three numbers,
  one claim — pin it to a file.
- **The mistral/gpt-oss deviation is absent from the 12-page version.** `SEVA_arxiv.tex:1457` and
  `SEVA_v8_supp.tex:154` disclose that the clone paraphraser is `mistral:7b-instruct`; `SEVA_tdsc.tex`
  says only "an offline LLM." The 12-page version makes the potency comparison ("On the *same* targets,
  generator, and corruption criterion") in §5.10 — the *judge* generator is indeed the same
  (gpt-oss:20b), but the *attack-text* generator differs, and "same generator" reads as covering both.
  Move the disclosure into the main text and reword to "same targets, same answering generator, same
  corruption criterion; the clone paraphraser is mistral:7b-instruct because gpt-oss:20b loops on the
  rewrite prompt." On the prompt's question: I do not think the mismatched paraphraser materially
  weakens the comparison, since the judge and criterion are held fixed — but it must be visible where
  the comparison is made.
- **`KNOWN_ISSUES.md` is stale.** Dated 2026-04-30 against v6.2.3 and commit `eba1add`; it does not
  mention the mistral deviation (contrary to the review brief), and several OPEN items are resolved in
  the current draft — CF-001 (the paper now says "50-iteration binary search" ✓), CF-006 ("we prove" is
  gone ✓), W-002 (K_FETCH = 20 now disclosed ✓), W-007 (90th percentile still not stated in
  `SEVA_tdsc.tex`). CF-005 ("hardware-agnostic" vs M4/4060 L3 divergence) and CF-008 (benign queries
  derived from corpus documents, which deflates FPR) appear unaddressed and CF-008 is worth a sentence
  in the paper. Refresh the file before release.
- **`RESULTS.md` header still points at the superseded paper.** Line 3 says "each table/observation in
  the paper (`SEVA_v8.tex`, `SEVA_v8_supp.tex`)". Update to the TDSC/arXiv pair.
- **The 3.15% → 0.90% query-FPR claim needs a source.** §5.9 gives it as a 3.5× reduction. The 5080
  grid in `result_scale100k.json` gives `query_fpr_ge1` 2.95/3.00/3.10 and `query_fpr_ge2`
  0.90/1.05/0.75 → 3.35×; `result_4060.json` gives 3.372/1.017 → 3.32×. 3.15% appears in neither. Add
  it to `RESULTS.md`.
- **`s_nd` dominates `cluster_coh` at tight operating points on HotpotQA, unreported.** From
  `pr_xgate_hotpotqa_s042.json`: at 0.1% FPR, `s_nd` catches 79% and `cluster_coh` 7%; at 0.5%, 97% vs
  95%; at 0.69%, 98% vs 97%. The paper's "matches or exceeds it, with a clear edge on Natural
  Questions … parity elsewhere" is defensible at the 0.69% point but hides that on HotpotQA the
  embedding deduplicator is uniformly ≥ and dramatically better at low FPR. C3 should say so.
- **At N = 10k the gate is not at 0%.** `result_scale10k.json` records `asr_pct: 4.00` at 1% density
  (all three seeds). Figure 4's caption honestly notes the gap collapses there, but no text states that
  evasion is nonzero at small N. Worth one clause, since it bounds the deployability claim downward.
- **Non-monotone L2/L3 in `tab:main`.** L3 (which ablates strictly more) equals L2 at 5% and 10% and is
  *lower* at 1% (42.4 vs 44.0). This is in the data (`s_lex_templated_gate_s042.json` notes
  "L2=L3 (frozen avg_sent_len wt=0)"), so it is explicable — but an unexplained non-monotonicity in the
  primary table invites doubt. One footnote.
- **Table 1 (`tab:family`) marks TopoGuard and Hubness as ✓FPR without running them.** Fine as a
  capability table, but the caption should state that ✓ means "reports an FPR in its own paper," not
  "verified at a matched operating point here."

---

## 5. Verification log

Every row is something I opened and computed, not something I read off the prose. "—" means the
artifact does not contain the paper's quantity.

| # | Claim (paper) | Paper value | Artifact | Artifact value | Verdict |
|---|---|---|---|---|---|
| 1 | `tab:main` L1 evasion, all 9 cells | 0.0 ± 0.0 | `results/in_domain/*.json` (9) | 0.0 in all 9 | **agree** |
| 2 | `tab:main` L1 Doc-FPR by density | 0.54/0.63/0.52 | same | 0.540/0.626/0.519 | **agree** |
| 3 | `tab:main` L2 evasion | 44.0/57.0/72.4 | same | 44.00/57.00/72.44 | **agree** |
| 4 | `tab:main` L3 evasion | 42.4/57.0/72.4 | same | 42.40/57.00/72.44 | **agree** |
| 5 | Grand-mean Doc-FPR | 0.56% | same | 0.5617% | **agree** |
| 6 | Per-condition max FPR, seed 7 | 0.83% | same (p050_s007) | 0.829% | **agree** |
| 7 | **Headline Doc-FPR** | **0.58%** | not in `RESULTS.md`; found in `linchpin_s042.json` | 0.5764% — but **composite L1**, τ=0.587, seed 42, 1 density, 112 encounters | **disagree (M3)** |
| 8 | `tab:coh` geometry | 0.7518/0.9871/+0.2353/5.99 etc. | `results/in_domain/*.json` | identical to 4 dp, all 3 densities | **agree** |
| 9 | Wilson upper bound arithmetic | 0.0154% | `result_hienc_ci.json` + recomputed z²/(n+z²) | 0.015364% (mine: 0.0153635%) | **agree** |
| 10 | Wilson run density | not stated | `result_hienc_ci.json` | `density_pct: 25.0` | **disagree — undisclosed (M4)** |
| 11 | Wilson run independence | "25,000 encounters" | `encounter_def` field | 25,000 docs, 1 corpus, 1 generator, 1 seed | **disagree (M4)** |
| 12 | poison_coh_min / clean mean (Fig. 2) | 0.8905 / 0.7510 | `result_hienc_ci.json` | 0.8905 / 0.75100 | **agree** |
| 13 | Obs 2 scaling FPRs | 0.765/0.674/0.701 | `result_scale{10k,100k}.json`, `result_1M.json` | 0.7653/0.6741/0.7008 | **agree** |
| 14 | Obs 2 deviations | 0.075/0.016/0.011 | same | 0.0753/0.0159/0.0108 | **agree** |
| 15 | Obs 2 "the trend the points follow" (1/√n) | O(1/√N) | computed ratios | 4.74, 1.47 vs predicted 3.16 | **disagree (M8)** |
| 16 | Obs 2 DKW bound tightness | "loose" | computed | 12–18× looser than data at every N | **agree, but vacuous (M8)** |
| 17 | Encoder gaps | +0.236 → +0.123 → +0.115 | `result_encoder_*.json` | +0.2363 / +0.1223 / +0.1130 | **agree** |
| 18 | Encoder clean coherence | 0.751 → 0.866 → 0.881 | same | 0.7509 / 0.8656 / 0.8817 | **agree** |
| 19 | Encoder SNR band | 5.2–6.7 | same | 5.21–6.66 | **agree** |
| 20 | Encoder evasion | 0% all | same | 0.00 on all 9 per encoder | **agree** |
| 21 | Encoder "Doc-FPR holds near 0.69%" | near target | same | e5 0.25–0.35%; gte 0.73–0.99% | **disagree (M11)** |
| 22 | Cross-platform gap agreement | < 5×10⁻⁷ | `result_4060.json` vs `result_M4.json` | max \|Δ\| = 4.172×10⁻⁷ | **agree** |
| 23 | "Several cells bit-identical" | several | same | 0 of 9 (4060 vs M4); 1 of 3 (5080 vs M4) | **disagree (minor)** |
| 24 | Cross-platform evasion | 0% both | same | 0.0 in all 9 cells, both machines | **agree** |
| 25 | 1M: gap, FPR | +0.245/+0.249, 0.70% | `result_1M.json` | +0.2454/+0.2489, 0.7008% | **agree** |
| 26 | NQ catch @0.69% FPR | 82% | `pr_xgate_s042.json` | `coh69 = 82.0` | **agree** |
| 27 | HotpotQA catch @0.69% | 97% | `pr_xgate_hotpotqa_s042.json` | `coh69 = 97.0` | **agree** |
| 28 | MinHash catch, both | 0% | both files | `mh69 = 0.0` both | **agree** |
| 29 | s_nd catch NQ / HotpotQA | 52% / (parity) | both files | 52.0 / 98.0 | **agree (framing, M-minor)** |
| 30 | Benign duplication rates | 1.15% / 9.06% / 0.24% | both files | 1.1514 / 9.0627 | **agree** |
| 31 | Security black-box catch | 98% | `pr_gate_s042.json` V=5 | 98.0 | **agree** |
| 32 | Security build = "released attack code" | released code | `pr_gen.py`, `pr_gate_s042.json` provenance | reimpl., adapted prompt, gpt-oss:20b | **disagree (M6)** |
| 33 | V-multiplicity sensitivity | not reported | `pr_gate_s042.json` | 48/60/98/100% at V=1/3/5/10 | **omitted (M5)** |
| 34 | Composite on real PoisonedRAG | 72% catch / 28% evasion | `pr_gate_s042.json` (mapped by `RESULTS.md:25`) | L1 catch = 66.0% at V=5, 78.0% at V=10; no 72% in the file, nor in `pr_gate2a_s042.json` | **disagree — untraceable (minor)** |
| 35 | RAGDefender templated catch | ~89% @ ~0.8% FPR | `e4hh_fair_s042.json` | 89.34% @ 0.8% actual | **agree** |
| 36 | RAGDefender at 5% / 50% FPR | ~93% / ~98% | same | 93.44 / 97.54 | **agree** |
| 37 | RAGDefender clean strip | 50.4% | `e4hh_s042.json` | `ragd_benign_doc_fpr: 51.2` | **disagree (minor)** |
| 38 | RAGDefender detection = reproduction | "reproduced" | `e4hh_fair.py` CHECK 2 | own `smean` statistic, not RAGDefender's filter | **disagree (M7)** |
| 39 | **RAGDefender vs SEVA on clones** | not reported | `e4hh_s042.json` | RAGDefender 57–71%, SEVA 11–13% | **omitted — contradicts C4 (M1)** |
| 40 | Clone evasion of gate | 100% of 50 | `expD_deployed_gate_s042.json` | `evade_coh_pct: 78.0`; 11/50 above τ | **disagree in file (M10)** |
| 41 | Clone cohesion mean | 0.751 | `expD…json` `coh_arr` | 0.7991 (clone-only run elsewhere: 0.7428) | **disagree (M10)** |
| 42 | Clone retrievable @K=5 | 84% | `expD…json` | 84.0 | **agree** |
| 43 | Clone flip rate | 31.0% (13/42) | `expD…json` + `expD_deployed_gate.py` | 13/42; candidates correctly gated on clone-only coh | **agree (script), unverifiable from JSON** |
| 44 | Clone end-to-end ASR | 26% | `expD…json` | 13/50 = 26.0 | **agree** |
| 45 | **Templated undefended corruption** | **18%** | `expA1_endtoend_s042.json` + `expA1.log` | **22.0% (11/50)** | **disagree (M2a)** |
| 46 | Poison in top-K, undefended → defended | 2.74 → 0.00 | `expA1_endtoend_s042.json` | 2.74 → 0.0 | **agree** |
| 47 | Templated corruption with gate | 0% | same | 0/50 | **agree** |
| 48 | Multiplicity: cohesion 0.722 → 0.790 | 0.722→0.790 | `expA2_cloneonly_s042.json` | 0.7218 → 0.7901 | **agree** |
| 49 | "Multiplicity does not rescue detection" | implied 0% | same file, `coh_catch_pct` | 0.0 / 0.0 / 11.1 / **22.7** | **disagree (M2b)** |
| 50 | s_nd on clones | 13–20% | same | 13.3–20.0 | **agree** |
| 51 | Two-signal union gate | 6.7–33.3% | same | 6.7 / 13.3 / 20.0 / 33.3 | **agree** |
| 52 | Prominence frontier peak ASR | 28% @ 25% payload | `expT2b_potency_frontier_s042.json` | k=2: payload 24.7%, evade 100%, ASR 28.0 | **agree** |
| 53 | Frontier evasion / retrievability | 100→46% / 90→38% | same | 100/100/86/46; 90/78/72/38 | **agree** |
| 54 | CleanBase reproduction | 100% templated / 0% clones @0.69% | `expT3_cleanbase_s042.json` | 100.0 / 0.0 at matched 0.6895% FPR | **agree** |
| 55 | K-sensitivity | 100% at K=3,5,10,20 | `expA23_sensitivity_s042.json` | 100.0 at all four | **agree** |
| 56 | Operating-point sweep + AUC | 100% at 0.1–5%; AUC 0.9999 | same | 100.0 at all 7; AUC 0.99994 | **agree** |
| 57 | Chunking + reranking | 168,865 chunks; 0.752/0.991; 100%; 3.6 pos | `expS1_chunk_rerank_s042.json` | 168,865; 0.7523/0.9909; 100.0; 3.56 | **agree** |
| 58 | Query aggregation 3.15% → 0.90% | 3.5× | `result_scale100k.json`, `result_4060.json` | 3.02→0.90 (3.35×); 3.37→1.02 (3.32×) | **partial — 3.15 unsourced** |
| 59 | Calibration = non-oracle as described | benign-retrieval quantile | `hardgate_xrun.py:210`, `scale_xrun.py:89`, `seva_benchmark_4060.py:794` | quantile over ground-truth-clean docs | **disagree (M9)** |
| 60 | Described (label-free) calibration works | implied | my run on cached coh + benign queries | τ 0.8439/0.8440/0.8505 → **0% evasion** at 1/5/10% | **agree — paper's method is sound (M9)** |
| 61 | Label-free τ is density-agnostic | implied | same | drifts 0.8439 → 0.8505 with density | **disagree (M9)** |
| 62 | 10k scale evasion | not stated | `result_scale10k.json` | `asr_pct: 4.00` at 1% density | **omitted (minor)** |
| 63 | Corpus hash gating works | hash-gated | `result_hienc_ci.json` | `hash_match: true`, fingerprint ok, 100,000/100,000, `first_divergent_index: null` | **agree** |
| 64 | Page count / limit | 12 pp. | `SEVA_tdsc.pdf` | 12 pages | **agree** |

**Threads I did not finish** (stated so coverage is not overstated): (i) the label-free calibration at
25% density — the condition of the headline Wilson run — which I could not run without recomputing
coherence over 100k documents; (ii) I did not attempt to re-derive the CleanBase reproduction's
faithfulness against the CleanBase paper's own algorithm, only that the released script's numbers match
the table; (iii) I did not audit the supplementary tables in `SEVA_arxiv.tex` cell by cell, only the
main-paper claims and the arxiv passages bearing on them; (iv) I did not re-verify layout, per the
brief.

---

## 6. Prioritized action list

### Must do before submission

| # | Action | Type | Cost |
|---|---|---|---|
| 1 | Report the clone rows of `e4hh_s042.json` (RAGDefender 57–71% vs SEVA 11–13%) and narrow C4 to *corpus-level* cohesion detectors, or run GRADA/TopoGuard on the clone set to support the wider claim | writing (or ~1 GPU-day for the wider claim) | M1 |
| 2 | Correct 18% → **22%** everywhere (abstract, C4, §5.10, §5.11, §7.3, Limitations, Conclusion, `RESULTS.md`) | writing | M2a |
| 3 | Restate the clone evasion claim with its multiplicity dependence (100% at V=1, 77.3% at V=5) and publish the `coh_catch_pct` column | writing | M2b |
| 4 | Replace the headline 0.58% with the deployed gate's 0.56% (n=9); relabel the frozen-split run as the composite at seed 42; add `linchpin_s042.json` to `RESULTS.md` | writing | M3 |
| 5 | Disclose the **25% density** of the high-encounter run in both versions | writing | M4 |
| 6 | Fix the provenance sentence: the Security PoisonedRAG is a disclosed re-implementation, not "the authors' released attack code" | writing | M6 |
| 7 | Relabel the RAGDefender detection comparison as a per-query ablation of cluster coherence; restrict "reproduced" to the strip-rate result; adjust C5 | writing | M7 |
| 8 | Add the V-multiplicity sweep (4 rows) and rewrite §3 Out-of-Scope as a measured gradient | writing | M5 |
| 9 | Demote Observation 2 to a measurement; fix the two-sample gap in the DKW chain; drop the rate claim | writing | M8 |
| 10 | Move the mistral:7b-instruct disclosure into the 12-page main text where the potency comparison is made | writing | minor |

### Would materially strengthen

| # | Action | Type | Cost |
|---|---|---|---|
| 11 | Run the paper's *described* (label-free, benign-retrieval) calibration at 25% density and report whether the gate holds | new experiment | one 100k coherence recompute + retrieval; ~1–2 GPU-hours |
| 12 | Change `hardgate_xrun.py` / `scale_xrun.py` to the label-free calibration and re-run the grid; my check says results will not move at 1–10% | code + re-run | a few GPU-hours |
| 13 | Replace the binomial CI with an uncertainty statement over independent generator seeds (m = 5–10) | new experiment | poison regeneration + scoring; ~1 GPU-day |
| 14 | Serialize `coh_par_cloneonly` as the primary array in `expD_deployed_gate_s042.json`; re-run the geometry (no LLM calls needed) | code + cheap re-run | minutes |
| 15 | Add the realized-FPR column to `tab:encoder` and rename Observation 3 to reflect encoder-dependent calibration fidelity | writing | — |
| 16 | Report the label-free τ drift with density as a caveat on "density-agnostic" | writing | — |
| 17 | Report sibling mutual similarity of the re-implemented Security poison against the released NQ/HotpotQA poison, to show the prompt substitution did not inflate cohesion | cheap measurement | minutes |
| 18 | Refresh `KNOWN_ISSUES.md`; address CF-008 (corpus-derived benign queries deflate FPR) with a sentence in the paper | writing | — |
| 19 | Per-cell Wilson intervals on FPR in the main table; state that seeds vary the partition only | writing | — |

### Optional

| # | Action | Type |
|---|---|---|
| 20 | Resample the benign query pool per seed (CF-009: `default_rng(self.cal_seed)`) and regenerate poison per seed, for genuine replication | one-line change + full re-run |
| 21 | Report `s_nd`'s dominance at tight FPR on HotpotQA in C3 | writing |
| 22 | Footnote the L2/L3 non-monotonicity at 1% density | writing |
| 23 | Note the 4% evasion at N = 10k in the text, not only the figure caption | writing |
| 24 | Reconcile 50.4% / 51.2% / 46% for the RAGDefender strip rate | writing |
| 25 | Update `RESULTS.md`'s header to the TDSC/arXiv pair | writing |

---

## 7. Venue fit

**TDSC is the right venue, and the fit is currently borderline — but for fixable reasons, not
structural ones.**

The paper belongs in a dependability/security transaction rather than an ML venue. Its contribution is
not a modelling advance; it is an operational-envelope result: a defense characterized under frozen
non-oracle calibration, complete false-positive accounting, adaptive adversaries, three encoder
lineages, two accelerator backends, and a hash-gated reproducible pipeline, together with a measured
statement of where the defense stops. That combination — especially the reproducibility discipline and
the willingness to publish the attack that breaks the system — is what TDSC readers want and what
NeurIPS/ACL-style venues systematically under-reward. `tab:family` and the deployability framing are
squarely in TDSC's idiom.

On the prompt's sharpest question — *is this a negative result dressed as a positive one?* — I do not
think so, but the paper currently gets the worst of both. Characterizing and delimiting a family's
operating envelope **is** a sufficient TDSC contribution; the field has too many defenses whose
envelopes were never measured, and a rigorous "here is exactly what this class of signal buys you and
where it stops" is worth more than the eleventh incremental detector. What undermines it is that the
delimitation is currently the *least* rigorously supported part of the paper (M1, M2, M10) while the
positive results are the most rigorous. That inverts the paper's own stated priorities and reads, to a
sceptical AE, as the boundary section having been written to a conclusion. It has not — the retraction
recorded in `PAPER_EDITS_LOG.md:767` is evidence of genuine intellectual honesty, and I want to say
plainly that the willingness to run and publish the experiment that breaks your own defense is the best
thing about this submission. But honesty in process has to show up as precision in the artifacts, and
here it does not yet.

**What moves it from borderline to clear acceptance:** fix the boundary section so it is the paper's
most defensible claim rather than its least. Concretely, items 1–3 of the must-do list. Report the
RAGDefender clone result even though it is unflattering; state the multiplicity dependence; correct the
comparator. The resulting claim — *corpus-level cohesion detection eliminates the dominant published
attack at negligible cost and is defeated by host-anchored cloning; the blind spot is shared by
CleanBase and is only partly recovered by a per-query filter that costs half the clean corpus* — is
narrower than what is written, better supported, and more useful to a practitioner. A reviewer who
checks it will find it holds.

**On the split and the title.** The 12-page version is *nearly* self-contained but leans on the
extended version for two load-bearing things: the mistral disclosure (M-minor) and the per-condition
Wilson intervals underpinning "complete per-seed false-positive reporting" (C5). TDSC allows unlimited
supplemental material, so the split is in roughly the right place — but anything a headline claim
depends on has to be in the 12 pages. Given that de-anonymization and bios will consume space, I would
buy that space from §7 (Discussion), which restates §5 at length; the V-sweep and the clone
head-to-head are worth more than the third restatement of the deployability envelope.

On the title: the manuscript's actual title is `SEVA: Lightweight, LLM-Free Detection of Templated
Corpus Poisoning in Retrieval-Augmented Generation`, which is fine and does *not* read as a survey. The
brief refers to a "Characterizing and Delimiting…" title — if that variant is under consideration, I
would not use it. For a security transaction it undersells and primes reviewers to read the paper as a
negative result. The current title is right; the abstract already carries the delimitation in its second
half, which is the correct place for it.
