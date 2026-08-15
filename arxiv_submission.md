# arXiv submission metadata

Everything here is the plain-text form arXiv's web form expects. The PDF abstract in
`SEVA_arxiv.tex` stays as written; this is the shorter metadata copy arXiv requires.

## Title

SEVA: Characterizing and Delimiting Cohesion-Based Detection of Corpus Poisoning in Retrieval-Augmented Generation (Extended Version)

## Categories

- Primary: **cs.CR** (Cryptography and Security)
- Cross-list: **cs.IR** (Information Retrieval), **cs.LG** (Machine Learning)

## License

Recommended: **CC BY 4.0** — it is the least restrictive of the arXiv options and does
not conflict with a later IEEE TDSC submission, since IEEE permits posting the author's
version on arXiv. (arXiv's own non-exclusive licence is the conservative alternative if
you would rather not grant redistribution rights.)

## Abstract (metadata copy, 1,920-character limit)

Retrieval-Augmented Generation (RAG) is vulnerable to corpus poisoning: adversarial document injection that corrupts retrieval without touching model weights or lexical filters. Existing defenses need LLM decoder access, multiplicative inference overhead, or cryptographic pre-registration, which offline on-device deployment cannot pay. We present SEVA, a fully local, LLM-free detector built on one geometric signal -- per-document K-nearest-neighbour cluster coherence -- operated as a hard gate against templated multi-passage poisoning, the dominant published pattern (PoisonedRAG). In-domain, where clean and poison share a security domain so no topic shortcut exists, it drives templated poison-evasion to 0% (95% Wilson upper bound 0.0154% over 25,000 encounters) at a 0.58% document-level false-positive rate under frozen non-oracle calibration. On PoisonedRAG's own released poison it catches 82-98%, while the lexical duplicate filtering PoisonedRAG itself dismissed proves corpus-fragile at matched FPR. End to end the gate removes all the corruption it detects: 18% of targets corrupted undefended, 0% with the gate in the loop. We then delimit its assumption. Host-anchored cloning -- one benign host mimicked per injected passage -- evades the gate on every target while staying retrievable; no complementary geometric signal we tested closes the gap, and the bypass is not expensive: it corrupts 26-28% of targets, more than the templated attack achieves undefended. Reproducing CleanBase at a matched operating point gives the same pattern (100% templated, 0% clones), so the boundary belongs to the mutual-similarity assumption the family shares rather than to our statistic. Detection is encoder-invariant across bge, e5 and gte, reproducible to 5e-7 across CUDA and Apple Silicon on a byte-identical hash-verified corpus, flat to 10^6 documents, and costs 13-38 ms per query with no LLM or API.

## Bundle

The arXiv version compiles from a **single file** — `SEVA_arxiv.tex`. All eleven figures
are pgfplots/TikZ; there are no external image dependencies. Upload the `.tex` alone.

## Comments field (suggested)

Extended version. 21 pages, 11 figures, 25 tables. Artifacts and reproduction scripts:
https://github.com/varadharajanv0310/SEVA-RAG

## Still needs a decision from you

- **Author name and affiliation.** The paper currently carries
  `Anonymous Author(s) / Manuscript submitted for blind review`, which must be replaced
  before posting — arXiv is not blind-reviewed. This is the one hard blocker I cannot
  resolve without you.
