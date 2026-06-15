# Notes

## Current Output Files

The `output/` folder is intentionally simple now:

- `output/output.csv`: the main scientific data file.
- `output/image_tracking.csv`: one-row-per-image progress tracker.

We removed the separate `plots.csv`, `tables.csv`, `output_validated.csv`,
`failed_images.csv`, and `processed_images.json` files because they made the
output folder harder to understand. The useful plot and table fields are now
kept directly inside `output/output.csv`.

## `output/output.csv`

This is the main species-observation file.

Current shape:

- 175 rows
- 33 columns

Each row means:

```text
one species in one releve / plot
```

For example, a table with 25 species and 7 releves should produce about:

```text
25 species x 7 plots = 175 rows
```

Important columns:

- `table_id`: printed table number in machine form, such as `table_4_1`.
- `image_file`: source image or source note for the row.
- `class`, `order`, `alliance`, `association`: vegetation classification.
- `releve_id`: plot number inside the table.
- `ref_code`: original field/reference code, such as `B68-155`.
- `map_reference`: printed map/grid reference.
- `os_grid_square`: British National Grid square, such as `NG`.
- `os_grid_reference`: full grid reference, such as `NG504446`.
- `easting`, `northing`: British National Grid metre coordinates.
- `latitude`, `longitude`: WGS84 decimal-degree coordinates when safely available.
- `altitude_ft`, `altitude_m`, `aspect_deg`, `slope_deg`, `cover_pct`, `plot_area_m2`: plot environmental fields.
- `species_reported`: number of species reported for that specific releve.
- `species`: taxon name as extracted from the table.
- `domin_value`: original Domin-scale value or symbol.
- `domin_cover_min_pct`, `domin_cover_max_pct`: numeric percent-cover range for Domin values 1-10.
- `presence_binary`: `1` means present, `0` means absent.
- `raw_value`: original printed table cell.
- `constancy_class`: summary column C, such as `II`, `III`, or `V`.
- `summary_value`: summary column D, such as `0.5`, `5.3`, or `6.3`.
- `total_species_reported`: total species count for the whole printed table.
- `needs_review`: whether the row needs manual checking.
- `note`: short explanation for uncertainty.

## Gavin Review Checklist

Gavin asked for four main fixes. Current status:

- Releve-specific species counts: done with `species_reported`.
- Table number as table id: done with values like `table_4_1`.
- Latitude/longitude from British mapping framework: implemented when a full British National Grid reference is available.
- Domin-scale numeric equivalents: done with `domin_cover_min_pct` and `domin_cover_max_pct`.

## Answer To Gavin's Mapping Question

The mapping framework is the British National Grid, maintained by Ordnance
Survey. The table gives map-reference numbers, but coordinate conversion needs
both parts:

```text
os_grid_square + map_reference
```

Example:

```text
NG + 504446 = NG504446
```

The script can convert a complete British National Grid reference into:

```text
easting, northing, latitude, longitude
```

The latitude/longitude output is WGS84 decimal degrees. We should not guess
coordinates from only a partial map reference. If the two-letter grid square is
missing or uncertain, the coordinate fields should stay blank until checked.

The BGS bulk-conversion page is useful as a reference/validation source. For
the local offline pipeline, the parser uses an internal OSGB36 to WGS84
conversion so we do not depend on a web service during batch extraction.

## Domin Scale Handling

The current conversion follows the 10-point Domin scale Gavin provided:

```text
1 = 0-4%, very rare / one or a few individuals
2 = 0-4%, scattered individuals
3 = 0-4%, frequent individuals
4 = 4-10%
5 = 10-25%
6 = 25-33%
7 = 33-50%
8 = 50-75%
9 = 75-90%
10 = 90-100%
. = absent / not detected
```

The original printed value stays in `domin_value` and `raw_value`. The converted
range goes into `domin_cover_min_pct` and `domin_cover_max_pct`.

## `output/image_tracking.csv`

This is the simple progress tracker for the image batch.

Current shape:

- 96 rows
- 10 columns

Each row means:

```text
one image in images/
```

Important columns:

- `image_file`: image path.
- `image_number`: natural sort position from 1 to 96.
- `status`: `successful`, `pending`, or `unsuccessful`.
- `last_attempt_at`: timestamp for the latest parse attempt.
- `error_type`: Python/Ollama error type when unsuccessful.
- `error_message`: what failed.
- `observations_added`: number of rows added to `output.csv`.
- `plots_detected`: number of plot objects found in the model response.
- `tables_detected`: number of table metadata objects found.
- `note`: short explanation, such as first-five prototype status.

Current tracker initialization:

- Images 1-5 are marked `successful` because the first accepted prototype batch is already represented in `output.csv`.
- Images 6-96 are marked `pending`.

## How The Files Connect

The working structure is now:

```text
output.csv
  scientific data, one species per releve/plot row

image_tracking.csv
  image-level progress, one image per row
```

This keeps the folder readable while preserving the data needed for richness,
abundance, composition, mapping, beta-diversity, and future resurvey analysis.
