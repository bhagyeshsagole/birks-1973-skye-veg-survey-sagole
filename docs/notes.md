# Dataset Guide

A plain-English reference for working with the Birks 1973 Skye vegetation survey data.
Read this before doing any analysis or cleaning.

---

## What This Dataset Is

H.J.B. Birks surveyed the vegetation of the Isle of Skye (Scotland) in 1967–1968 as part of his 1973 PhD thesis. He recorded plant communities using the **phytosociological releve method**: at each field plot, he listed every vascular plant, bryophyte, and lichen present and scored its abundance on the **Domin scale** (1–10).

The result was a set of printed vegetation tables — each table = one plant community type. Each column in a table = one field plot (releve). Each row = one species. Each cell = a Domin abundance score.

This project digitised all 96 scanned pages of those tables into a single tidy CSV.

---

## The Output File

```
output/output.csv
```

**28,856 rows × 33 columns**

One row = **one species recorded in one plot**.

---

## Column Guide

### Identity

| Column | What it means | Example |
|---|---|---|
| `table_id` | Which printed table this row comes from | `table_4_1`, `table_4_35` |
| `image_file` | Source scan page | `images/Birks-HJB-1973-Present-Flora-Veg-Skye_2.png` |
| `releve_id` | Plot number within that table | `1`, `7`, `12` |
| `ref_code` | Birks' original field notebook code for the plot | `B68-155`, `B67-097` |

### Vegetation Classification

These come from the printed table header. They describe what community type the table covers.

| Column | What it means | Example |
|---|---|---|
| `class` | Broadest phytosociological level | `CARICETEA CURVULAE` |
| `order` | Next level down | `CARICETALIA CURVULAE` |
| `alliance` | Next level | `Arctostaphyleto-Cetrariion nivalis` |
| `association` | The specific named community | `Cariceto-Rhacomitrium lanuginosi` |

Think of these as a taxonomy for vegetation types, not for species.

### Plot Location

| Column | What it means | Example |
|---|---|---|
| `map_reference` | Digits from the printed map reference | `504446` |
| `os_grid_square` | Two-letter British National Grid square | `NG` |
| `os_grid_reference` | Full grid reference | `NG504446` |
| `easting` | Grid easting in metres (OSGB36) | `150447` |
| `northing` | Grid northing in metres (OSGB36) | `844632` |
| `latitude` | WGS84 decimal degrees | `57.274318` |
| `longitude` | WGS84 decimal degrees | `-6.215441` |

> **95% of rows have lat/lon.** The 5% missing are from 5 pages that were scanned in landscape orientation and could not be read reliably — new scans are pending.

### Plot Environment

All values are as printed in the table header rows.

| Column | What it means |
|---|---|
| `altitude_ft` | Altitude in feet (as printed) |
| `altitude_m` | Altitude converted to metres |
| `aspect_deg` | Aspect in degrees (compass bearing of slope face) |
| `slope_deg` | Slope angle in degrees |
| `cover_pct` | Total vegetation cover percentage |
| `plot_area_m2` | Plot size in square metres (usually 4) |
| `species_reported` | Number of species recorded for **this specific plot** |

### The Species Observation

| Column | What it means | Example |
|---|---|---|
| `species` | Taxon name as printed | `Calluna vulgaris` |
| `domin_value` | Raw Domin scale value from the table | `5`, `.`, `+`, `x` |
| `raw_value` | Same as domin_value (direct copy from cell) | `5` |
| `presence_binary` | `1` = present, `0` = absent | `1` |
| `domin_cover_min_pct` | Lower bound of percent-cover range | `10` |
| `domin_cover_max_pct` | Upper bound of percent-cover range | `25` |
| `constancy_class` | Summary column C (Roman numerals I–V) | `IV` |
| `summary_value` | Summary column D (mean Domin across releves) | `3.2` |
| `total_species_reported` | Total species in the whole printed table | `54` |

### Data Quality

| Column | What it means |
|---|---|
| `needs_review` | `True` = this row has some uncertainty; `False` = confirmed clean |
| `note` | Short explanation of why it needs review |

**88.6% of rows are `needs_review=False`** (clean, confirmed from scan).
**11.4% are `needs_review=True`** — see the quality section below.

---

## The Domin Scale

Birks used the 10-point Domin scale to score abundance. Here is what each value means:

| Value | Cover range | Description |
|---|---|---|
| `10` | 90–100% | Dominant, complete cover |
| `9` | 75–90% | Very abundant |
| `8` | 50–75% | Abundant |
| `7` | 33–50% | Frequent |
| `6` | 25–33% | Frequent |
| `5` | 10–25% | Frequent |
| `4` | 4–10% | Occasional |
| `3` | 0–4% | Frequent individuals |
| `2` | 0–4% | Scattered individuals |
| `1` | 0–4% | Very rare, one or a few individuals |
| `.` | 0% | **Absent / not detected** |
| `+` | trace | Present but below Domin 1 threshold |
| `x` | — | Presence mark only (no abundance scored) |

The columns `domin_cover_min_pct` and `domin_cover_max_pct` already convert numeric values to their percent-cover ranges. A single midpoint column can be added during cleaning if needed.

**`.` = not detected.** This is printed in the table to mean the species was looked for but absent. Rows with `domin_value = '.'` have `presence_binary = 0`.

---

## What Tables Are In The Dataset

The dataset covers 54 vegetation tables (Table 4.1 through Table 4.56), spanning the full range of Skye plant communities:

| Community group | Tables | Approximate ecology |
|---|---|---|
| Grasslands and heaths | 4.1–4.8 | Maritime grassland, salt marsh, Asteretea |
| Mires and bogs | 4.13–4.24 | Blanket bog, flush, Scheuchzerio-Caricetea |
| Alpine communities | 4.35–4.40 | Caricetea curvulae, fell-field, snow-bed |
| Woodland communities | 4.41–4.49 | Betulo-Adenostyletea, Quercetea, Corylus woodland |
| Epiphytic bryophytes | 4.50–4.54 | On tree bark; sites shared with Table 4.49 |
| Aquatic/rupestral | 4.55–4.56 | Stream-side, rock ledge |

Table 4.57 (images 75–96) is a **synoptic constancy table** — it summarises all communities in one large matrix. It is not a standard species-by-releve table and is excluded from output.csv.

---

## Coordinate Coverage

Coordinates (lat/lon) are derived from the **British National Grid** map references printed in each table header. The conversion is OSGB36 → WGS84, computed offline in the pipeline.

| Status | Rows | Notes |
|---|---|---|
| Has lat/lon | 27,401 (95%) | Reliable, converted from printed grid references |
| Missing lat/lon | 1,455 (5%) | 5 unreadable pages; new scans requested |

Missing coordinates break down as:
- **553 rows** — Tables 4.50 and 4.51 (landscape-rotated scans, releve metadata unreadable)
- **902 rows** — Tables 4.53 and 4.54 (epiphyte sub-tables whose map references appear only in Table 4.49, which could not be read reliably)

---

## Data Quality Flags

| Flag | Rows | Main cause |
|---|---|---|
| `needs_review=False` | 25,572 (88.6%) | Clean — verified from scan |
| `needs_review=True` | 3,284 (11.4%) | Genuine uncertainty |

What is still flagged and why:

| Image(s) | Table | Rows | Issue |
|---|---|---|---|
| 8 | 4.8 | 676 | Landscape rotation, ~26 cramped columns — **need new scan** |
| 49–50 | 4.40 | 1,860 | Wide landscape, multiple associations — **need new scan** |
| 66 | 4.50 | 322 | Landscape rotation — **need new scan** |
| 69 | 4.51 | 231 | Landscape rotation — **need new scan** |
| 44 | 4.36 | 17 | Duplicate species entry with uncertain value |
| 48 | 4.38 | 11 | Last releve column value uncertain |
| 53 | 4.43 | 14 | Cells approximate in one section |
| 61–64 | 4.47 | 84 | Two-association layout; assoc 2 values and two species names uncertain |
| 65 | 4.48 | 3 | Footnote species names approximate |
| 67–68 | 4.49 | 39+13 | Assoc 2 approximate; one partially legible name |

> For analysis: filtering to `needs_review == 'False'` gives you **25,572 clean rows** covering 90+ tables with full confidence.

---

## Quick Python Start

```python
import pandas as pd

df = pd.read_csv("output/output.csv", dtype=str)

# Work with clean rows only
clean = df[df["needs_review"] == "False"].copy()

# Convert numeric columns
numeric_cols = [
    "altitude_ft", "altitude_m", "aspect_deg", "slope_deg",
    "cover_pct", "plot_area_m2", "species_reported",
    "domin_cover_min_pct", "domin_cover_max_pct",
    "latitude", "longitude"
]
for col in numeric_cols:
    clean[col] = pd.to_numeric(clean[col], errors="coerce")

# Present-only rows (exclude absent species)
present = clean[clean["presence_binary"] == "1"]

# Species richness per releve
richness = present.groupby(["table_id", "releve_id"])["species"].nunique()

# All releves with coordinates
mapped = clean[clean["latitude"].notna()][["releve_id", "ref_code", "latitude", "longitude", "association"]].drop_duplicates("releve_id")
```

---

## Key Things To Know Before Analysis

1. **One row ≠ one species.** Absent species (`.`) are also rows. Filter by `presence_binary == '1'` for presence-only analysis, or keep dots for full matrix analysis.

2. **`domin_value` is a string.** Values include digits `1–10`, `.`, `+`, and `x`. Convert to numeric carefully — `.`, `+`, `x` are not numbers.

3. **`constancy_class` is Roman numerals.** I = lowest (rare across releves), V = highest (present in most releves). These are table-level summary statistics, not per-releve data.

4. **`summary_value` (column D)** is the mean Domin score across all releves in the table for that species. Useful for ranking species by typical abundance within a community.

5. **Coordinates are plot-level, not row-level.** All rows for the same releve have the same lat/lon. To get a plot-level table, `drop_duplicates("releve_id")` after selecting coordinate columns.

6. **`ref_code`** links the same physical plot across multiple tables. For example, `B67-097` appears in both Table 4.45 (vascular) and Table 4.53 (epiphyte bryophytes) — same location, different survey focus.

7. **Multiple pages can belong to one table.** Table 4.35 spans images 41 and 42, Table 4.36 spans images 43 and 44, etc. The `table_id` is the same for both pages.

8. **`species_reported`** is the per-releve species count printed in the original table. Use it to cross-check richness calculations. The total for the table is in `total_species_reported`.

---

## image_tracking.csv

```
output/image_tracking.csv
```

**96 rows × 10 columns** — one row per source scan page.

Useful for knowing which pages are fully clean vs still pending new scans:

```python
tracking = pd.read_csv("output/image_tracking.csv")
tracking[tracking["note"].str.contains("new scan", na=False)]
```

---

## What Needs To Happen Before Full Analysis

- [ ] 5 new scans from Gavin (images 8, 49, 50, 66, 69) to fill the 3,089 remaining uncertain/missing rows
- [ ] Decide on Domin → single numeric conversion strategy (midpoint, min, max, or keep range)
- [ ] Standardise species names to a modern checklist if resurvey comparison is planned (1973 nomenclature differs from current)
- [ ] Confirm coordinate datum — pipeline outputs WGS84; confirm that is correct for intended mapping tools
