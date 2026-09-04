# TDSC submission — paste-ready values

Everything the IEEE Author Portal asks for, in the order its progress list shows.
Upload the **blind** pair unless the portal says otherwise (see the note at the end).

---

## Files to upload

| Portal slot | File | Pages |
|---|---|---|
| Main manuscript | `SEVA_tdsc.pdf` | 12 |
| Supplemental material (separate file) | `SEVA_tdsc_supp.pdf` | 4 |

Do **not** upload the named variants (`*_named.pdf`) unless the portal states the review
is single-blind.

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

The abstract in the PDF is 462 words. IEEE portals normally cap the metadata abstract
near 250, so paste this condensed version (238 words):

```
Retrieval-Augmented Generation (RAG) is vulnerable to corpus poisoning: adversarial document injection that corrupts retrieval without touching model weights or lexical filters. Existing defenses require LLM decoder access, multiplicative inference overhead, or cryptographic pre-registration, none of which offline on-device deployment can pay. We present SEVA, a fully local, LLM-free detector built on one geometric signal - per-document K-nearest-neighbour cluster coherence - operated as a hard gate against templated multi-passage poisoning, the dominant published attack pattern. In-domain, where clean and poison share a security domain so no topic shortcut exists, SEVA drives templated poison-evasion to 0% across three seeds, with a 95% Wilson upper bound of 0.0154% over 25,000 encounters, at a 0.56% document-level false-positive rate under frozen non-oracle calibration. On PoisonedRAG's own released poison it catches 82-98%, while the lexical duplicate filtering PoisonedRAG itself dismissed proves corpus-fragile at matched false-positive rate. End to end the gate removes all the corruption it detects: 22% of targets corrupted undefended, 0% with the gate in the loop. We then delimit the assumption the detector rests on. Host-anchored cloning evades the gate on every target while remaining retrievable, no complementary geometric signal we tested closes the gap, and the bypass is not expensive. Reproducing CleanBase at a matched operating point gives the same pattern, placing the boundary in the mutual-similarity assumption the detection family shares rather than in our statistic. Detection is encoder-invariant, reproducible to 5e-7 across CUDA and Apple Silicon, flat to one million documents, and costs 13-38 ms per query.
```

---

## 4. Authors

| # | Name | Role |
|---|---|---|
| 1 | V. Varadharajan | Corresponding author |
| 2 | Abishek V. P. T. | Co-author |

---

## 5. Affiliations / 6. Author Details / 7. Match Organizations

**Decide this before you start — it must be consistent.** The manuscript currently says
"independent researchers" while your portal account uses `vv0366@srmist.edu.in`. Pick one:

- **If this work is affiliated with SRM Institute of Science and Technology**, enter SRMIST
  as the organization (it will match in *Match Organizations*), and change the named
  variant's `\thanks` line to say so. This is the stronger option — an institutional
  affiliation helps at desk-review.
- **If the work is genuinely independent of SRM**, enter "Independent Researcher" as the
  organization and consider a personal contact address, since an institutional email with
  no institutional affiliation invites a question.

Corresponding author email: `vv0366@srmist.edu.in` (or your chosen address).

---

## 8. Additional Information

**Index terms** (as printed in the paper):

```
Retrieval-Augmented Generation, Corpus Poisoning, Anomaly Detection, Embedding Security, Geometric Detection, On-Device Security
```

If the portal asks for suggested reviewers, avoid anyone from the PoisonedRAG, CleanBase
or RAGDefender author lists — the paper reproduces or delimits all three, and proposing
them reads badly.

If it asks whether the work has been posted as a preprint: **not yet** (arXiv is pending
endorsement). If you post before a decision, disclose it then.

---

## 9. Cover letter

See `TDSC_COVER_LETTER.md`.

---

## The one thing I could not verify

**Whether TDSC review is single- or double-blind.** `computer.org` is blocked in my
browser and JS-rendered, and neither official template mentions "blind" or "anonymous"
in 53,000 characters. Click **AUTHOR GUIDELINES** in the portal nav bar — it states the
policy directly.

The risk is asymmetric, so absent confirmation upload the blind pair: submitting
anonymised to a single-blind journal is harmless, while submitting named to a
double-blind one is a desk reject.
