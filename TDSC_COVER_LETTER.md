# Cover letter — TDSC submission

Paste the body below into the portal's cover-letter field. TDSC is single-anonymous --
the guidelines list it among the Transactions that do not offer double-anonymous review
-- so the letter is signed.

---

Dear Professor Vaidya and the TDSC Editorial Board,

We submit **"SEVA: Lightweight, LLM-Free Detection of Templated Corpus Poisoning in
Retrieval-Augmented Generation"** for consideration as a Regular Paper.

**What the paper contributes.** Retrieval-Augmented Generation relocates a system's
factual authority into a corpus an adversary may be able to write to, and the defenses
that drive published attack-success down all charge a price that offline, on-device
deployment cannot pay: LLM decoder access, multiplicative inference overhead, or a
cryptographic registration authority. We characterize what a single geometric signal —
per-document K-nearest-neighbour cluster coherence, operated as a hard gate — can and
cannot do in that setting. Under frozen, non-oracle calibration it drives templated
poison-evasion to 0% in-domain at a 0.56% document-level false-positive rate, catches
PoisonedRAG's own released poison at 82–98% across three corpora, and costs 13–38 ms per
query with no model call. The evaluation is deliberately hostile to our own result: an
in-domain corpus that denies a geometric detector any topic shortcut, complete per-seed
false-positive accounting, an adaptive adversary, three embedding lineages, two
accelerator backends, and validation to one million documents.

**Why we believe it is a fit for TDSC.** The contribution is an operational-envelope
result rather than a modelling advance — a defense characterized under adversarial
adaptation, with its deployment cost measured and its failure boundary located. That is
a dependability question more than a machine-learning one.

**A concurrency we want to raise ourselves.** CleanBase is contemporaneous work that
makes a closely related observation at corpus level. Rather than claim priority or
distance, we reproduced it: implemented its described algorithm, swept its threshold by
bisection to our own 0.69% clean false-positive operating point, and ran it on the same
corpus and attack. It performs identically to SEVA on both regimes — 100% on templated
poison, 0% on host-anchored clones. We report that agreement as the central evidence for
our sharpest claim rather than as a competitive result: the blind spot we document
belongs to the mutual-similarity assumption the detection family shares, not to our
statistic. We think this makes the concurrency an asset to the paper rather than a
threat to its novelty, but we raise it explicitly so the editorial board can judge.

**On the negative results.** The second half of the paper attacks our own defense.
Host-anchored cloning — paraphrase the target's top-ranked benign document, splice in
the payload, repeat with a different host per target — evades the gate on every target
while remaining retrievable, and the obvious complementary geometric signal does not
recover it. We also retract, in the paper itself, an earlier claim of ours that evading
the gate is expensive; three separate measurements contradicted it. We report the failed
repair and the retraction because a reader deciding whether to deploy a cohesion gate
needs them more than another confirmatory table.

**Artifacts.** Every headline number maps to a committed result file at
https://github.com/varadharajanv0310/SEVA-IEEE. Corpora and injected poison are gated by
order-sensitive SHA-256 hashes recorded in each result file, so a reproduction that does
not match the published corpus fails closed rather than diverging silently.

**Disclosures.** The work received no external grant funding and the authors declare no
conflicts of interest. Two locally hosted open-weight language models were used to
generate and judge experimental attack data; both are named in the Acknowledgments, and
neither is part of the detector, which calls no language model at any point.

The manuscript is 12 pages including references, with a 4-page supplement submitted as a
separate file. It is not under consideration elsewhere.

Thank you for your time and consideration.

Sincerely,

V. Varadharajan (corresponding author)
Abishek V. P. T.
