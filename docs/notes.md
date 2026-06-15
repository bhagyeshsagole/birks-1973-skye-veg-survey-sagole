# Notes

## Output CSVs Explained

The `output/` folder has one main data file and two linked metadata files. Together, they describe a vegetation table in a form that can be analyzed later in Python.

## `output/output.csv`

This is the main species-observation file.

Current shape:

- 175 rows
- 33 columns

Each row means:

```text
one species in one releve / plot
```

So if one table has 25 species and 7 releves, the long-format observation file should have:

```text
25 species x 7 plots = 175 rows
```

Important columns:

- `table_id`: which vegetation table or association this row came from.
- `image_file`: source image or source note for this row.
- `class`, `order`, `alliance`, `association`: phytosociological classification.
- `releve_id`: plot number, such as `1`, `2`, or `3`.
- `ref_code`: original field/reference code, such as `B68-155`.
- `map_reference`: old map/grid reference from the printed table.
- `os_grid_square`: British National Grid square, such as `NG`.
- `os_grid_reference`: full British National Grid reference, such as `NG504446`.
- `easting`, `northing`: British National Grid metre coordinates derived from `os_grid_square` and `map_reference`.
- `latitude`, `longitude`: decimal-degree coordinates for mapping when printed directly or safely converted from the grid reference.
- `altitude_ft`, `altitude_m`, `aspect_deg`, `slope_deg`, `cover_pct`, `plot_area_m2`: environmental data for that plot.
- `species_reported`: number of species reported for that specific releve/plot.
- `species`: species name.
- `domin_value`: extracted Domin-scale abundance value.
- `domin_cover_min_pct`, `domin_cover_max_pct`: percent-cover range represented by numeric Domin categories.
- `presence_binary`: `1` means present, `0` means absent.
- `raw_value`: original printed symbol or value.
- `constancy_class`: summary column C, such as `II`, `III`, or `V`.
- `summary_value`: summary column D, such as `0.5`, `5.3`, or `6.3`.
- `total_species_reported`: total species count reported by the printed table.
- `needs_review`: whether the row needs manual checking.
- `note`: explanation for uncertainty or review flags.

Example:

```text
species = Festuca rubra
releve_id = 3
domin_value = 2
presence_binary = 1
```

This means `Festuca rubra` was present in plot 3 with Domin value 2.

If:

```text
domin_value = .
presence_binary = 0
```

That means the species was absent from that plot.

If:

```text
raw_value = x
domin_value = x
presence_binary = 1
```

That means the printed table showed a presence mark instead of a numeric Domin value.

Why this matters:

- This is the file used for richness calculations.
- It supports species composition analysis.
- It supports abundance summaries.
- It supports ordination such as NMDS or PCA.
- It supports beta-diversity and resurvey comparison work.

## `output/plots.csv`

This is the plot/releve metadata file.

Current shape:

- 7 rows
- 20 columns

Each row means:

```text
one releve / plot
```

Important columns:

- `table_id`: links the plot back to the table.
- `releve_id`: plot number.
- `ref_code`: original field/reference code.
- `map_reference`: original map/grid reference.
- `os_grid_square`: British National Grid square, such as `NG`.
- `os_grid_reference`: full British National Grid reference.
- `easting`, `northing`: British National Grid metre coordinates.
- `latitude`, `longitude`: decimal-degree coordinates for GIS/maps. Leave blank until the map reference can be safely converted.
- `altitude_ft`, `altitude_m`: elevation.
- `aspect_deg`: slope direction.
- `slope_deg`: slope steepness.
- `cover_pct`: vegetation cover percentage.
- `plot_area_m2`: plot size.
- `species_reported`: number of species reported for this plot in the printed table.
- `needs_review`: whether the plot row needs checking.
- `note`: explanation if anything is uncertain.

Why this matters:

- It lets us map historical plots.
- It lets us compare vegetation composition against environmental variables.
- It avoids repeating plot metadata by hand in multiple places.

## `output/tables.csv`

This is the table-level metadata file.

Current shape:

- 1 row
- 10 columns

Each row means:

```text
one vegetation table / association
```

Important columns:

- `table_id`: table or association identifier.
- `image_file`: source image or source note.
- `class`, `order`, `alliance`, `association`: phytosociological hierarchy.
- `n_releves`: number of plots in the table.
- `total_species_reported`: total species count reported by the table.
- `mean_species_per_releve`: reported mean species count, if available.
- `notes`: table-level notes.

Why this matters:

- It gives the scientific context for each plot and species observation.
- It lets later analysis group plots by vegetation community type.

## `output/output_validated.csv`

This is the species-name review file for the current tidy output.

Current shape:

- 25 rows
- 10 columns

Each row means:

```text
one unique species name from output/output.csv
```

Important columns:

- `table_id`: table where the species appears.
- `species`: species name as currently stored in `output/output.csv`.
- `corrected_species`: current corrected/review name. At this stage it matches `species`.
- `validation_status`: current review status.
- `confidence`: simple format-check confidence.
- `flag`: `true` means the name needs human review.
- `note`: why the row is flagged or what kind of check was done.
- `observations_count`: number of observation rows for that species.
- `present_count`: number of plots where that species is present.
- `domin_values_seen`: Domin values or presence/absence symbols seen for that species.

Current status:

```text
output_validated.csv is a format-check species review file, not a final taxonomic authority validation.
```

Why this matters:

- It separates species-name review from plot-by-plot observations.
- It highlights abbreviated names such as `R. heterostichum`.
- It highlights special source marks such as `*Parmelia glabratula`.
- It gives a clean place for later taxonomic authority validation.

## How The Files Connect

The current tidy structure is:

```text
tables.csv
  one row per vegetation table

plots.csv
  one row per plot/releve inside that table

output.csv
  one row per species per plot/releve
```

The key linking columns are:

```text
table_id
releve_id
```

That lets us connect:

```text
species observation -> plot metadata -> table classification
```

This structure is relevant because the project goal is not just OCR. The goal is to turn old vegetation tables into modern research data that can support richness, abundance, composition, mapping, functional-group, beta-diversity, and resurvey comparisons.
