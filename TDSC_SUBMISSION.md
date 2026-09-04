# TDSC submission — paste-ready values

Based on the IEEE Computer Society author guidelines, not inference.

---

## Settled: TDSC is single-anonymous. Submit the NAMED files.

The guidelines list the Transactions that do **not** offer double-anonymous review, and
TDSC is one of them:

> "Note: IEEE Transactions on Cloud Computing, IEEE Transactions on Computers, IEEE
> Transactions on Software Engineering, **IEEE Transactions on Dependable and Secure
> Computing**, and IEEE Transactions on Emerging Topics in Computing do not offer this
> option."

> "Unless a double-anonymous review is requested, each article undergoes a
> **single-anonymous** peer review process, where the authors do not know the identities
> of the reviewers, but **the reviewers know the identities of the authors**."

So the anonymized variants are not used. Do not submit `SEVA_tdsc.pdf`.

| Portal slot | File | Pages |
|---|---|---|
| Main manuscript (first in the file list) | `SEVA_tdsc_named.pdf` | 12 |
| Supplemental material (separate file) | `SEVA_tdsc_supp_named.pdf` | 4 |

The supplement must be a separate file — the guidelines are explicit that supplemental
material "must not be included within the same PDF file as the main paper submission,"
and that "all appendices in journal articles are considered supplemental material."
Ours already are.

---

## 1. Article Type

**Regular Paper**

---

## 2. Title

```
SEVA: Lightweight, LLM-Free Detection of Templated Corpus Poisoning in Retrieval-Augmented Generation
```

---

## 3. Abstract

The guidelines cap a regular paper's abstract at **100–200 words** and forbid
mathematical expressions and bibliographic references in it. The paper's abstract was
440 words with 7 math expressions; it has been rewritten to exactly 200 words with none.
The manuscript and this field now carry the same text:

```
Retrieval-Augmented Generation relocates a system's factual authority into a corpus an adversary may be able to write to. Existing defenses require LLM decoder access, multiplicative inference overhead, or cryptographic pre-registration, none of which offline on-device deployment can pay. We present SEVA, a fully local, LLM-free detector built on one geometric signal, per-document K-nearest-neighbour cluster coherence, operated as a hard gate against templated multi-passage poisoning. In-domain, where clean and poison share a security domain so no topic shortcut exists, SEVA drives templated poison-evasion to zero across three seeds at a 0.56 percent document-level false-positive rate under frozen, non-oracle calibration, and catches PoisonedRAG's released poison at 82 to 98 percent across three corpora. End to end the gate removes all the corruption it detects. We then delimit the assumption it rests on. Host-anchored cloning evades the gate on every target while remaining retrievable, no complementary geometric signal we tested closes the gap, and the bypass is cheap. Reproducing CleanBase at a matched operating point yields the same pattern, placing the boundary in the mutual-similarity assumption the detection family shares rather than in our statistic. Detection is encoder-invariant, reproducible across backends, flat to one million documents, at 13 to 38 milliseconds per query.
```

---

## 4. Authors / 5. Affiliations / 6. Author Details / 7. Match Organizations

| # | Name | Role |
|---|---|---|
| 1 | V. Varadharajan | Corresponding author |
| 2 | Abishek V. P. T. | Co-author |

**ORCID is required.** The guidelines state it is "required by all IEEE publications"
and you will be prompted for it. Register at orcid.org first if you do not have one —
both authors should.

**Affiliation — decide before you start.** The paper says "independent researchers" while
your account uses `vv0366@srmist.edu.in`. Under single-anonymous review the reviewers see
this, so it should be coherent. If the work is connected to SRM Institute of Science and
Technology, enter SRMIST (it will resolve in *Match Organizations*) and change the
`\thanks` line to match. If it is genuinely independent, enter "Independent Researcher"
and consider whether an institutional address is the right contact.

---

## 8. Additional Information

**Keywords — select from the ACM taxonomy in the portal, not free text.** The guidelines
note the taxonomy terms are linked to reviewer expertise and that free-text keywords are
not searchable. Enter at least three. The paper's own index terms, for reference:

```
Retrieval-Augmented Generation, Corpus Poisoning, Anomaly Detection, Embedding Security, Geometric Detection, On-Device Security
```

**Excluded reviewers.** Avoid anyone from the PoisonedRAG, CleanBase or RAGDefender
author lists — the paper reproduces or delimits all three.

**Preliminary versions.** None. arXiv posting is pending endorsement; if you post before
a decision, disclose it to the editorial office at that point.

**Human/animal subjects.** None.

---

## 9. Cover letter

See `TDSC_COVER_LETTER.md`.

---

## Before you upload

- **Run the IEEE LaTeX Analyzer** (latexqc.ieee.org) if you upload `.tex` rather than
  PDF. The guidelines recommend it explicitly to avoid processing delays.
- **Page limit is 12 formatted pages** including references and biographies, with
  **$220 per page** over after final layout. We are at exactly 12; biographies were
  removed because journals do not require them and they count against the limit.
- Keep the main manuscript **first** in the file list.
- Files cannot exceed 350 MB (ours are under 250 KB).
