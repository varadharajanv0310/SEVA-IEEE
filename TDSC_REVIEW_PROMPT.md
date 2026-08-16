# Prompt: adversarial TDSC review of SEVA

Paste everything below the line into a fresh Claude Code session opened at
`D:\SEVA-RAG\SEVA-RAG`.

---

You are reviewing a manuscript for **IEEE Transactions on Dependable and Secure
Computing**. Act as a demanding but fair TDSC reviewer who is an expert in RAG
security, embedding geometry, and anomaly detection, and who has read PoisonedRAG,
CleanBase, RobustRAG, TrustRAG, GRADA, and the hubness-detection literature. Your
review decides whether this is published in a Q1 security venue.

The authors want the review that finds the problems, not the one that flatters them.
A review that concludes "this is strong, minor revisions" without having tried to
break the paper is a failed review. Equally, do not manufacture objections to look
rigorous: every criticism must be traceable to something you actually read or ran.

## The manuscript

Three versions of one paper, all in the repo root:

| File | What it is |
|---|---|
| `SEVA_tdsc.tex` / `.pdf` | **The submission under review.** 12 pages, IEEEtran `[10pt,journal,compsoc]`, at TDSC's hard regular-page limit. |
| `SEVA_arxiv.tex` / `.pdf` | Extended version, 21 pages, 11 figures, 25 tables. Contains every appendix and measurement. **Read this for detail the 12-page version had to cut.** |
| `SEVA_v8.tex` + `SEVA_v8_supp.tex` | Older conference-format pair. Superseded; consult only if you need history. |

Supporting material you should treat as part of the submission:
`README.md`, `RESULTS.md` (claim → source-file map), `HOW_TO_REPRODUCE.md`,
`KNOWN_ISSUES.md`, `PAPER_EDITS_LOG.md` (decision history, including a retraction),
`reproduction/*.json` (released measurements), `results/in_domain/*.json`,
`adaptive_attack_results/`, and the `exp*.py` experiment scripts in the root.

## What the paper claims

SEVA is an LLM-free corpus-poisoning detector for RAG. The signal is `cluster_coh(d)`
— the mean pairwise cosine among a document's K=5 nearest **corpus** neighbours —
operated as a hard gate: flag a document when `coh > τ`, flag a query when ≥2 of its
retrieved documents are flagged. τ is calibrated non-oracle, as the (1−0.0069)
percentile of clean coherence, with no labelled poison and no density oracle.

Headline claims, each of which you should try to falsify:

1. **0% poison-evasion** on templated multi-passage poisoning in-domain, at 0.58%
   document-FPR, under frozen non-oracle calibration, across 3 seeds × 3 densities.
   95% Wilson upper bound 0.0154% from 25,000 encounters.
2. **82–98% detection** on PoisonedRAG's own released poison (NQ, HotpotQA) and a
   faithful black-box build on the in-domain Security corpus.
3. **End to end**, the gate removes all corruption it detects: 18% of targets
   corrupted undefended → 0% with the gate in the loop.
4. **Three invariance observations**: density-invariance (Obs 1), calibration scaling
   O(1/√N) argued from Dvoretzky–Kiefer–Wolfowitz (Obs 2), encoder-invariance across
   bge/e5/gte (Obs 3).
5. **A self-declared boundary**: host-anchored cloning (paraphrase the top-ranked
   benign host per target, splice in the payload) evades the gate on *every* target
   while staying retrievable; no complementary geometric signal they tested closes it;
   and the bypass is **not** expensive — it corrupts 26–28% of targets, more than the
   templated attack achieves undefended.
6. **The boundary is the family's, not theirs**: a reproduced CleanBase at a matched
   0.69% FPR gives the identical pattern (100% templated, 0% clones), so the blind
   spot follows from the shared mutual-similarity assumption.
7. **Reproducibility**: agreement to 5×10⁻⁷ across CUDA and Apple Silicon on a
   byte-identical hash-verified corpus, flat to 10⁶ documents, 13–38 ms/query.

## How to build and inspect

The environment is already set up — do not create a new one, and do not `pip install`
anything into it. It is pinned (numpy 1.26.4) and matplotlib was deliberately removed
because it crashed against that pin.

- Python: `/c/Users/varad/miniconda3/envs/seva/python.exe` (PyMuPDF `fitz`, pypdf, PIL available)
- LaTeX: `tectonic` in `_texbin/` — `export PATH="$PWD/_texbin:$PATH"` then
  `tectonic -X compile SEVA_tdsc.tex --outdir _texbin`
- `_tex_check.py <file.tex>` — citation/bibitem/label/ref/percent/environment integrity
- `_texbin/layout_audit.py <file.pdf>` — renders the PDF and reports content outside
  the text block and overlapping blocks

Read pages as images (`page.get_pixmap(dpi=140).save(...)` then open the PNG). **Layout
has just been audited page by page and is clean** — do not spend your effort re-checking
margins and float placement. If you happen to notice a layout defect, note it under
minor comments and move on. Your job is the substance.

## How to review

Work from the artifacts, not from the prose. For every quantitative claim you assess,
open the JSON in `reproduction/` or `results/` that `RESULTS.md` maps it to and check
the number yourself. Where a claim has no traceable artifact, that is itself a finding.
Where the paper's number and the file disagree, quote both.

Push hard on at least these, and add your own:

**Novelty and positioning.** The paper concedes the cohesion signal is not novel and
claims the contribution is *characterizing and delimiting* the family's envelope. Is
that a sufficient TDSC contribution, or is it a negative result dressed as a positive
one? CleanBase is concurrent and closest — is the reproduction faithful enough to
support "the boundary belongs to the family"? Does reproducing one peer license a claim
about a whole family (SeCon-RAG, GRADA, TrustRAG, TopoGuard are named but not run)?

**Threat model.** §3 scopes to templated multi-passage injection and explicitly puts
single-document mimicry out of scope — while §5.10 shows an in-scope-looking attack
(host-anchored cloning) that defeats the defense completely. Is the scoping principled
or is it drawing the boundary around the wins? Is the adaptive adversary (L2/L3 keyword
and structure ablation) the strongest reasonable one, or a convenient one? What about
an adversary who tunes payload similarity, injects at multiple densities simultaneously,
or targets the calibration channel?

**Whether the defense is worth deploying at all.** Claim 5 says the bypass is cheap and
*more* effective than the attack the gate stops. Confront that directly: if a
one-paraphrase-per-target adversary defeats it entirely, what does an operator actually
buy? Is the paper's own answer ("a filter for known attack structure, not a security
boundary") honest and sufficient, or does it undercut the contribution?

**Statistical and methodological rigor.** Check the Wilson bound arithmetic (0 evasions
in 25,000). Check whether the DKW argument in Obs 2 actually supports what the text says
— the bound is distribution-free and loose, and three corpus sizes is three points; is
"O(1/√N)" claimed or merely illustrated? Is 3 seeds enough? Is the 60/40 cal/eval split
and decontamination sound? Are FPRs reported per-seed as claimed? Is the RAGDefender
head-to-head fair given the paper grants it an idealized threshold at a *looser* matched
FPR — does that help or hurt SEVA's case?

**Encoder-invariance.** The absolute gap shrinks 0.236 → 0.123 → 0.115 across bge/e5/gte
while the paper argues SNR is preserved. Is "invariance" the right word, or is this
"works on three encoders with quite different margins"? What would a poison-aware or
adversarially-trained encoder do — the paper explicitly disclaims that class.

**Reproducibility.** 5×10⁻⁷ cross-platform agreement is a strong claim. Verify the hash
gating actually does what is claimed. Note that `KNOWN_ISSUES.md` and the edits log
record a deviation: the boundary attack's paraphraser is `mistral:7b-instruct` because
`gpt-oss:20b` looped, while the corruption judge stays `gpt-oss:20b`. Does that weaken
the potency comparison?

**Presentation for TDSC specifically.** Is the 12-page version self-contained, or does
it lean on the extended version for load-bearing evidence? TDSC allows unlimited
supplemental material in separate files — is the split in the right place? Is the title
("Characterizing and Delimiting…") right for a security transaction, or does it read as
a survey/negative result and undersell?

## Things the authors already know (do not re-report as discoveries)

- Layout, float placement, table overflow, figure quality — just audited and fixed.
- The paper is currently anonymized (`Anonymous Author(s)`); de-anonymization and author
  bios are pending and will consume space against the 12-page limit.
- A "cost of evasion" claim was written, contradicted by the authors' own data, and
  **retracted**; the paper now makes no cost-of-attack claim. If you think the retraction
  went too far or not far enough, say so — but do not report the retracted claim as
  though it were still in the paper.

## What to produce

Do not fabricate results, do not guess at numbers, and do not claim you verified
something you did not open. If you run out of budget before finishing a thread, say
which threads are unfinished rather than implying full coverage. If a check you ran
disagrees with the paper, show the command and the output.

Deliver, in this order:

1. **Recommendation** — Accept / Minor revision / Major revision / Reject, with the
   one-paragraph reason a TDSC AE would need.
2. **Summary of the paper** in your own words, so the authors can see what actually
   landed versus what they think they wrote.
3. **Major issues**, numbered, each with: the claim, the evidence you checked, why it
   is a problem, and what would fix it. Rank by how much each threatens acceptance.
4. **Minor issues**, terse.
5. **Verification log** — a table of every claim you checked against an artifact, with
   the file, the paper's value, the file's value, and agree/disagree.
6. **Prioritized action list** — what to do before submitting, split into
   *must-do-before-submission*, *would-materially-strengthen*, and *optional*. For each,
   estimate whether it needs a new experiment (and roughly what compute) or only writing.
7. **Your read on venue fit** — is TDSC right, and if the answer is "borderline", what
   specific change would move it from borderline to clear.

Write the review to `TDSC_REVIEW.md` in the repo root, and give me the recommendation
and the top three major issues in your reply.
