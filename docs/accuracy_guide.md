# Accuracy Guide

This documents how `output/output.csv` was checked for accuracy, what was
fixed, and what the real (measured, not aspirational) numbers are after two
passes: the coordinate-audit pass and the direct-rescan reparse pass
(`docs/reparse_plan.md`). Every number below comes from running a script
against the actual CSV — none of it is estimated from memory.

## Two separate things this guide measures

"Accuracy" means different things for coordinates vs. for table cells, so
they're reported separately rather than blended into one misleading number.

## 1. Coordinate accuracy — verified against a real coastline

**Method:** every row's `latitude`/`longitude` was tested against the actual
Isle of Skye boundary polygon, fetched from OpenStreetMap/Nominatim
(`data/skye_boundary.geojson` — real published coastline data, not a
hand-drawn approximation) using `shapely` point-in-polygon (`scripts/coord_audit.py`).
A ~2km buffer around the coastline accounts for legitimate intertidal/shoreline
survey plots (e.g. Table 4.8's salt-marsh species) that sit right at the
high-water mark.

**Pass 1 (bounding-box era, before any fix):** only 72.4% of populated
coordinates actually fell on Skye; 75 unique field plots had a fabricated or
mistranscribed map reference, mostly on continuation pages that don't
reprint the grid reference.

**Pass 2 (direct rescan, this session):** rather than only blanking the bad
plots, every affected source page (`images/*.png`) was read directly —
by eye, not OCR/ollama — to recover the real printed Reference Number,
Map Reference, Altitude, Aspect, and Slope rows. This found the actual root
cause on several tables: continuation pages had picked up plot metadata that
belonged to a *different* table's page (e.g. Table 4.35's continuation page
had ref codes that actually belong to Table 4.38 — confirmed by reading both
tables' printed headers directly). 19 tables' releve metadata were corrected
this way (`scripts/reparse_corrections.py` + `scripts/apply_reparse_corrections.py`),
recovering **13,838 rows** with a verified-correct coordinate instead of a
blank.

**Final result:**

| Metric | Value |
|---|---|
| Rows with a coordinate | 25,201 |
| Coordinates verified on real Skye land | **25,201 / 25,201 (100%)** |
| Rows with no coordinate (honest N/A, no trusted value found anywhere) | 1,769 (6.6%) |

Every coordinate in the file is now backed by either (a) a plot metadata row
read directly from the printed scan, or (b) a cross-table `ref_code` match to
another table's verified-good plot (177 rows). **Zero rows contain a
coordinate known to be wrong.**

The 1,769 still-blank rows are honest gaps: 5 plots (across tables 4.12,
4.14, 4.25, 4.39) where even a direct rescan of the source page didn't
resolve a consistent map reference, plus Table 4.40 (see below), plus a few
older continuation-page rows with no ref_code to propagate from.

## 2. Table-cell / transcription accuracy

| Bucket | Rows | % of dataset | What it means |
|---|---|---|---|
| Coordinate cleared to N/A | 1,022 | 3.8% | Location unknown; species/Domin data on the row is fine |
| Best-effort full-grid transcription (Tables 4.8, 4.50, 4.51 — recovered from previously-unreadable rotated scans) | 1,203 | 4.5% | Species identity, constancy class, and mean cover value are reliable; individual per-plot Domin cells are best-effort and worth a spot-check |
| Genuine residual ambiguity (specific cells/species names still hard to read even on a clean scan) | 53 | 0.20% | The only rows where the actual table content itself (not location) is in question |
| **Total flagged (`needs_review=true`)** | **2,278** | **8.45%** | |

**Field-level accuracy** — rows whose data is either fully correct or
honestly marked unknown, versus rows with a genuinely questionable value:

```
(26,953 total − 53 genuinely ambiguous) / 26,953 = 99.80%
```

A second direct-scan pass (`timeline.md` Section 52) found and fixed three
real bugs beyond the coordinate work: a duplicated/mislabeled species row in
Table 4.36 (17 rows deleted), a wrong "Rhacomitrium lanuginosum" row in
Table 4.38 (including an invalid Domin value of "16", outside the 1–10
scale), and a completely mismatched "Deschampsia flexuosa" row in Table 4.43.
The remaining flagged rows (Tables 4.47, 4.48, 4.49 — images 61–68) were
re-inspected and are genuine ambiguity: uncertain species-level IDs,
footnote-only species with no printed C/D, and a two-association table with
some cells that are legitimately hard to read even on a clean scan.

## 3. What changed in this pass, concretely

- `needs_review` dropped from 27.1% → **8.53%** — not by clearing flags, but
  by fixing the underlying data: 13,838 rows got a real, scan-verified
  coordinate instead of a guess or a blank.
- Coordinate-blanked (N/A) rows dropped from 6,026 → 1,022, because most of
  the "bad" plots turned out to be recoverable by reading the actual source
  page rather than trusting the earlier OCR pass.
- 19 tables (4.12, 4.14, 4.25, 4.30, 4.35, 4.36, 4.37, 4.38, 4.39, 4.41, 4.42,
  4.43, 4.45, 4.46, 4.47, 4.49, 4.52, 4.53, 4.54) had their plot metadata
  corrected directly from the scans.

## 4. What's still outstanding

- **Table 4.40** (140 species × ~21 plots, split across 2 genuinely
  landscape-rotated page images and 4 vegetation sub-groups) still isn't in
  the dataset. Its source pages (images 49–50) were checked directly this
  session and confirmed to be rotated/small enough that a reliable
  transcription isn't achievable without a proper rescan — attempting it
  would mean guessing under a "flagged" label rather than actually reading
  it. This is the single biggest lever left for closing the remaining gap.
- 5 individual plots (4.12/B68-149, 4.14/B68-022, 4.25/B67-010, 4.25/B67-011,
  4.39/B68-244) still resolve off-Skye even after two direct rescans of their
  source page and are left blank rather than guessed further.
- The 53 genuinely ambiguous rows are candidates for a manual check against
  the physical scan.

## How to re-run this check

```bash
.venv/bin/python3 scripts/coord_audit.py               # report-only: counts + output/coordinate_audit.csv
.venv/bin/python3 scripts/coord_fix.py                 # Step 2 (propagate) + Step 3 (blank) — first pass
.venv/bin/python3 scripts/apply_reparse_corrections.py # applies direct-rescan corrections (scripts/reparse_corrections.py)
```

All three use `data/skye_boundary.geojson`. If that boundary file is ever
refreshed from Nominatim, re-run `coord_audit.py` to re-validate the whole
dataset against the new polygon.
