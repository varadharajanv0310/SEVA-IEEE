#!/usr/bin/env python3
"""Citation-integrity + percent-escaping + environment-balance checker for the SEVA papers.
Usage: python _tex_check.py SEVA_tdsc.tex"""
import sys, re

path = sys.argv[1] if len(sys.argv) > 1 else "SEVA_tdsc.tex"
with open(path, "r", encoding="utf-8") as f:
    raw = f.read()
lines = raw.splitlines()

# strip comments (a % not preceded by backslash starts a comment) for cite/ref scanning
def strip_comment(line):
    out = []
    i = 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line):
            out.append(line[i:i+2]); i += 2; continue
        if c == "%":
            break
        out.append(c); i += 1
    return "".join(out)

code = "\n".join(strip_comment(l) for l in lines)

errors, warnings = [], []

# --- citations vs bibitems ---
cited = set()
for m in re.finditer(r"\\cite\{([^}]*)\}", code):
    for k in m.group(1).split(","):
        k = k.strip()
        if k:
            cited.add(k)
defined = []
for m in re.finditer(r"\\bibitem\{([^}]*)\}", code):
    defined.append(m.group(1).strip())
defined_set = set(defined)

missing = sorted(cited - defined_set)       # cited but no bibitem -> undefined citation
orphan = [k for k in defined if k not in cited]  # bibitem but never cited
dupbib = sorted({k for k in defined if defined.count(k) > 1})

if missing:
    errors.append("CITED but NO \\bibitem (undefined): " + ", ".join(missing))
if orphan:
    warnings.append("\\bibitem never \\cite'd (orphan): " + ", ".join(orphan))
if dupbib:
    errors.append("duplicate \\bibitem keys: " + ", ".join(dupbib))

# --- labels vs refs ---
labels = set(re.findall(r"\\label\{([^}]*)\}", code))
refs = set()
for m in re.finditer(r"\\(?:ref|eqref|autoref)\{([^}]*)\}", code):
    refs.add(m.group(1).strip())
missing_lab = sorted(refs - labels)
if missing_lab:
    errors.append("\\ref to MISSING \\label: " + ", ".join(missing_lab))

# --- raw (unescaped) percent in text ---
raw_pct = []
for i, line in enumerate(lines, 1):
    j = 0
    while j < len(line):
        c = line[j]
        if c == "\\":
            j += 2; continue
        if c == "%":
            # comment start - rest is comment; only flag if it looks like text "NN%"
            before = line[:j]
            if re.search(r"[0-9A-Za-z]\s*$", before) and not before.rstrip().endswith("\\"):
                # could be a stray percent meant as literal; report context
                raw_pct.append((i, line.strip()[:80]))
            break
        j += 1
# Note: many % are legitimate comments/tags; report as info only
# We specifically want "NN%" without backslash in *rendered* text.
text_pct = []
for i, line in enumerate(lines, 1):
    # find digit followed by % not preceded by backslash
    for m in re.finditer(r"(?<!\\)%", line):
        k = m.start()
        if k > 0 and line[k-1].isdigit():
            text_pct.append((i, line.strip()[:90]))
            break
if text_pct:
    errors.append("UNESCAPED percent after digit (rendered text!):\n    " +
                  "\n    ".join(f"L{i}: {t}" for i, t in text_pct))

# --- environment balance ---
begins = re.findall(r"\\begin\{([^}]*)\}", code)
ends = re.findall(r"\\end\{([^}]*)\}", code)
from collections import Counter
cb, ce = Counter(begins), Counter(ends)
for env in set(list(cb) + list(ce)):
    if cb[env] != ce[env]:
        errors.append(f"env imbalance '{env}': {cb[env]} begin vs {ce[env]} end")

# --- report ---
print(f"=== {path} ===")
print(f"  \\cite keys: {len(cited)}   \\bibitem: {len(defined)}   labels: {len(labels)}   refs: {len(refs)}")
if warnings:
    print("  WARNINGS:")
    for w in warnings:
        print("   - " + w)
if errors:
    print("  ERRORS:")
    for e in errors:
        print("   - " + e)
    sys.exit(1)
print("  OK: no integrity/percent/balance errors.")
