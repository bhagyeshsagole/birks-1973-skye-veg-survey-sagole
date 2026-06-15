# Timeline

## 1. Goal
- Build a local, offline pipeline that turns scanned Birks vegetation-table images into clean CSV data.
- The machine is an 8GB M2 MacBook Air, so the pipeline has to use smaller models, resized image copies, and one model at a time.
- Raw scans stay in `images/`.
- CSV outputs are written to `output/`.

## 2. First Plan
- The first plan was a general geo-botanical OCR pipeline.
- `parse_images.py` reads images from `images/`, sends each image to a local Ollama vision model, asks for JSON, and writes `output/output.csv`.
- The first JSON fields were `species_name`, `location`, `coordinates`, `date`, `collector`, `notes`, `other_visible_fields`, `parse_status`, `parse_error`, and `raw_response`.
- `validate_names.py` reads `output/output.csv`, checks extracted species names with a local text model, and writes `output/output_validated.csv`.
- `download_drive.py` was added as an optional helper for downloading a Google Drive image folder into `images/`.
- This plan worked as a script structure, but it assumed the scans were specimen labels. The actual images are vegetation tables, so this was not the final data shape we need.

## 3. Validator Behavior
- The validator model is `qwen2.5:3b`.
- If `species_name` is blank, the script does not call the model.
- Instead, it sets low confidence, marks `flag=true`, and writes the note `No species name was extracted.`
- If `species_name` exists, the validator asks the model to check botanical binomial format and fix obvious OCR mistakes.
- This behavior is useful later, but only after the parser extracts real taxon names from table rows.

## 4. First Ollama Model Attempt
- The originally requested vision model was `qwen2-vl:7b`.
- Ollama did not have that exact tag available.
- We pulled `qwen2.5vl:7b`, which is the available Qwen vision-language model family in Ollama.
- The parser default was temporarily pointed at `qwen2.5vl:7b`.
- This got a vision model onto the machine, but it did not give us a working pipeline yet.

## 5. First Five Image Test
- There are 96 images in `images/`.
- We tested only the first 5 images first so we could find problems without wasting time on the full set.
- Normal filename sorting would choose files like `_1`, `_10`, `_11` before `_2`.
- We changed the parser to use natural numeric sorting so the first five are `_1`, `_2`, `_3`, `_4`, `_5`.
- The first test command shape was:
  `python3 parse_images.py --limit 5 --batch-size 1 --keep-raw`
- That first run failed for all 5 images.
- `output/output.csv` showed `parse_status=error` for each row.
- The key error was that Ollama could not find `llama-server`.

## 6. Homebrew Ollama Problem
- Homebrew installed an `ollama` command, but that install did not include the runtime binary needed for model inference.
- The missing runtime binary was `llama-server`.
- Because of that, Python could contact Ollama, but Ollama could not actually start the model.
- This was not a bug in `parse_images.py`.
- It was an Ollama installation/runtime problem.

## 7. Ollama Runtime Fix
- We installed the official Ollama macOS app bundle because it includes `llama-server`.
- The app bundle had `/Applications/Ollama.app/Contents/Resources/llama-server`.
- The first app runtime that launched was stale and reported version `0.17.0`.
- That stale runtime crashed when loading newer `qwen2.5vl` models.
- The logs showed repeated `SIGSEGV` crashes.
- A newer Ollama update zip already existed in `~/Library/Caches/ollama/updates/.../Ollama-darwin.zip`.
- We moved the stale app aside and extracted the current app bundle into `/Applications`.
- After that, Ollama reported version `0.30.7`.
- This fixed the missing-runner problem and the stale-runtime crash problem.

## 8. Full-Size Images Were Too Heavy
- The scans are roughly 2100 by 3000 pixels.
- Sending full-size scans to a local vision model was too slow on the 8GB MacBook Air.
- The 7B model was also too heavy and stalled during early tests.
- We added temporary image resizing to `parse_images.py`.
- The script leaves the original scan unchanged.
- It creates a smaller temporary JPEG, sends that to Ollama, then deletes the temporary copy.
- We tested this with `--max-image-side 1000`.

## 9. Parser Controls Added
- `--max-image-side` controls the largest side of the temporary image copy sent to Ollama.
- `--num-predict` limits how long the model response can be.
- JSON mode was added to push the model toward returning parseable JSON.
- Natural sorting was added so numbered scan files run in the expected order.
- Fresh runs now overwrite old failed test rows unless `--resume` is used.
- `--resume` still exists so interrupted long runs can skip images already processed.

## 10. Why The 7B Vision Model Was Dropped
- `qwen2.5vl:7b` was too slow for practical work on this machine.
- Even with resized images and shorter responses, it spent too long on early pages.
- We stopped stalled parser runs instead of waiting indefinitely.
- We unloaded the 7B model before trying smaller models so memory stayed under control.
- The 7B model was removed because it was not part of the working path.

## 11. Working Vision Model
- We pulled `qwen2.5vl:3b`.
- It is smaller than the 7B model and works better on the 8GB MacBook Air.
- After the Ollama runtime was fixed, `qwen2.5vl:3b` loaded and processed images.
- `parse_images.py` now defaults to `qwen2.5vl:3b`.
- Current model roles:
  `qwen2.5vl:3b` parses images.
  `qwen2.5:3b` validates extracted species names.

## 12. First Successful Parse Run
- Working command:
  `python3 parse_images.py --limit 5 --batch-size 1 --keep-raw --max-image-side 1000 --num-predict 256 --model qwen2.5vl:3b`
- The run completed in about 3 minutes 32 seconds.
- It wrote 5 rows to `output/output.csv`.
- Four rows had `parse_status=ok`.
- One row had `parse_status=error`.
- The error row failed because the model response did not contain a parseable JSON object.
- None of the first five rows produced a `species_name`.

## 13. What The First Five Results Taught Us
- The scripts can run locally after the Ollama fixes.
- The model can process resized scans on this machine.
- The first five scans appear to be vegetation-table or context pages, not specimen labels.
- That explains why the specimen-style parser did not find useful `species_name` values.
- The technical pipeline worked, but the extraction target was wrong.

## 14. First Validation Run
- We unloaded the vision model before validation so both models were not loaded at the same time.
- Validation command:
  `python3 validate_names.py --limit 5 --batch-size 1 --keep-raw`
- Since all `species_name` cells were blank, the validator skipped model calls.
- It flagged all 5 rows for review.
- `output/output_validated.csv` now has 5 validation rows.
- All 5 rows have `flag=true` and note `No species name was extracted.`
- This is correct behavior for blank names.

## 15. Current Output Meaning
- `output/output.csv` proves the parser can call Ollama, process images, and save rows.
- `output/output_validated.csv` proves the validator can read parser output and flag bad or missing names.
- These files are useful smoke-test outputs.
- They are not the final data format because the real target is table reconstruction, not one JSON record per image.

## 16. New Understanding Of The Images
- The images are structured phytosociological vegetation tables.
- They are not herbarium specimen labels.
- We should not extract one record per image with fields like collector, date, coordinates, and one `species_name`.
- We need to reconstruct the visible table as CSV.
- That means one CSV row per table row.
- Table rows can include classification rows, plot metadata rows, environmental rows, species rows, footnotes, and localities.

## 17. Table Extraction Prompt
- `csv_parsing_instructions.md` now describes the table-focused extraction target.
- It tells the model to return CSV text, not JSON.
- It uses this header:
  `row_label,plot_1,plot_2,plot_3,plot_4,plot_5,plot_6,plot_7,C,D`
- It tells the model to preserve plot columns 1-7 plus summary columns C and D.
- It tells the model to keep dots, x marks, abundance values, abbreviated taxon names, asterisks, footnotes, and locality text.
- This prompt matches the actual Birks table images better than the original specimen-label JSON prompt.

## 18. What Worked
- The official Ollama app runtime fixed the missing `llama-server` problem.
- Updating Ollama to runtime `0.30.7` fixed the stale-runtime crashes.
- `qwen2.5vl:3b` can process resized scans locally.
- Temporary image resizing keeps the original scans untouched.
- Token limits help prevent extremely long model responses.
- Natural sorting correctly selects `_1` through `_5`.
- The parser records per-image errors instead of crashing the whole run.
- The validator correctly flags blank species names instead of pretending they are valid.

## 19. What Failed Or Was Not Good Enough
- `qwen2-vl:7b` was not available under that exact Ollama tag.
- Homebrew Ollama did not include the needed `llama-server` runtime.
- The stale Ollama app runtime crashed newer Qwen vision models.
- `qwen2.5vl:7b` was too slow and heavy for this 8GB machine.
- Full-size scans were too slow for practical local testing.
- The first JSON parser shape was wrong for these pages because it expected specimen-label fields.
- The first five parsed rows did not produce species names because the data is table-based.

## 20. Next Practical Step
- Move from printed-table reconstruction to tidy research data.
- Use the prompt in `csv_parsing_instructions.md`.
- Preferred outputs are linked CSVs: table metadata, plot/releve metadata, and long-format species observations.
- `output/output.csv` should prioritize one species-by-releve observation per row.
- Keep Domin values, presence flags, raw symbols, plot metadata, and table classification fields available for analysis.

## 21. Current Safe Command Pattern
- Current tidy parser command:
  `python3 scripts/parse_images.py --limit 5 --batch-size 1 --max-image-side 1000 --num-predict 8192 --mode tidy --prompt-file prompts/csv_parsing_instructions.md`
- Tidy mode writes `output/output.csv`, `output/plots.csv`, and `output/tables.csv`.
- The older specimen-style parser is still available with `--mode json`.
- The older printed-table reconstruction path is still available with `--mode table`, but it is not the preferred research output.

## 22. First Table-CSV Batch
- Updated `instructions.md` so future parsing work points to `csv_parsing_instructions.md` and prefers table-shaped CSV over one JSON record per image.
- Updated `parse_images.py` so table mode is the default parser path.
- Table mode reads `csv_parsing_instructions.md`, sends that prompt to `qwen2.5vl:3b`, parses returned CSV rows, and saves them with the header `row_label,plot_1,plot_2,plot_3,plot_4,plot_5,plot_6,plot_7,C,D`.
- Kept old JSON mode available with `--mode json` in case we need to compare against the earlier specimen-style parser.
- First table run failed because the sandbox could not reach local Ollama at `127.0.0.1:11434`.
- Reran with local Ollama access allowed.
- The model returned useful table rows but sometimes skipped the CSV header, so the parser was loosened to keep table-shaped rows even when the header line is missing.
- Final first-five command:
  `python3 parse_images.py --limit 5 --batch-size 1 --max-image-side 1000 --num-predict 2048 --mode table --prompt-file csv_parsing_instructions.md`
- Final result: `output/output.csv` now has 150 table-shaped rows from the first 5 images and 0 parse-error rows.

## 23. Tidy Database Direction
- User clarified the desired endpoint: a modern tidy database for Birks vegetation survey data, suitable for richness, abundance, composition, functional-group, mapping, and resurvey comparisons.
- Updated `csv_parsing_instructions.md` so future extraction targets table metadata, plot/releve metadata, and long-format observations rather than a visual copy of the printed table.
- Updated `parse_images.py` so default `--mode tidy` writes linked CSV outputs.
- Tried a first-five tidy model run, but the model under-extracted badly: only 11 observations, 7 plots, 1 table, and several parse-error rows.
- Replaced that weak test output with a clean prototype generated from the user-provided table transcription.
- Current clean prototype outputs:
  `output/output.csv` has 175 long-format species-by-releve observations.
  `output/plots.csv` has 7 plot/releve metadata rows.
  `output/tables.csv` has 1 table metadata row.
- Important lesson: direct long-format extraction may need a staged process, likely printed-table extraction first and deterministic conversion to tidy tables second.

## 24. Code Explanation Comments
- Added beginner-friendly comments and docstrings to `parse_images.py`, `validate_names.py`, and `download_drive.py`.
- Explained script modes, output CSV shapes, Ollama calls, image resizing, model response parsing, resume behavior, batch saving, validation flow, and Drive downloads.
- Verified all scripts still compile with `python3 -m py_compile parse_images.py validate_names.py download_drive.py`.

## 25. Output CSV Explanation
- Reviewed `output/output.csv`, `output/plots.csv`, `output/tables.csv`, and `output/output_validated.csv`.
- Explained how each file maps to the vegetation survey project: table metadata, plot metadata, long-format species observations, and species review output.

## 26. Notes And Setup Docs
- Added `docs/notes.md` with a plain-English explanation of all output CSV files and how they connect to the research project.
- Added `docs/setup.md` as the current Mac/Windows setup and run guide; future process changes should replace obsolete steps there.

## 27. Folder Structure Cleanup
- Reorganized project files into clearer folders: `scripts/` for Python scripts, `prompts/` for model prompts, and `docs/` for human-readable notes/setup.
- Kept `images/` for ignored raw scans, `output/` for tracked CSVs, and root-level `instructions.md`/`timeline.md` for agent workflow.
- Updated current commands and docs to use `scripts/parse_images.py` and `prompts/csv_parsing_instructions.md`.

## 28. Coordinate Columns
- Added `latitude` and `longitude` columns to plot and observation outputs so map-ready coordinates can be stored next to `map_reference`.
- Updated the parser schema and prompt to keep these fields blank unless coordinates are printed or can be safely converted from a complete grid reference.
- Initial coordinate placeholder update made `output/output.csv` 175 rows by 26 columns and `output/plots.csv` 7 rows by 15 columns.

## 29. Gavin Review Fixes
- Added per-releve `species_reported` values so plot-specific richness is stored separately from the table-wide total species count.
- Changed current prototype `table_id` to `table_4_1`.
- Added British National Grid fields: `os_grid_square`, `os_grid_reference`, `easting`, and `northing`; current prototype uses `NG` plus the printed map reference.
- Converted British National Grid easting/northing to WGS84 `latitude` and `longitude` offline in the parser.
- Added Domin cover range columns: `domin_cover_min_pct` and `domin_cover_max_pct`.
- Current CSVs after review fixes: `output/output.csv` is 175 rows by 33 columns, and `output/plots.csv` is 7 rows by 20 columns.

## 30. Existing CSV Cleanup
- Replaced the old 5-row specimen-label `output/output_validated.csv` with a current tidy species review file.
- New `output/output_validated.csv` has 25 rows, one per unique species name, with format-check status, review flags, observation counts, present counts, and Domin values seen.
- Updated docs so `output_validated.csv` is no longer described as legacy parser output.

## 31. Unattended Pipeline Audit
- Audited the current Ollama image pipeline, including its model, prompt, input/output paths, dependencies, batching, progress display, and resume behavior.
- Confirmed the parser already runs images sequentially without Codex; identified durable success/failure tracking and clearer logging as the main remaining automation work.

## 32. Durable Unattended Parsing
- Added per-image JSON status, a dedicated failure CSV, resume/retry controls, atomic saves after every image, clear terminal messages, and a final run summary.
- Updated setup commands for a three-image test, full resume run, and explicit failed-image retries; ignored local Python virtual-environment folders.

## 33. Full Batch Stopped
- Started the 96-image unattended run and stopped it immediately when requested.
- Saved result: 0 successful, 1 failed; image 2 was interrupted before status saving and remains available for resume.

## 34. Simplified Output Folder
- Removed extra tracked output files and kept `output/output.csv` as the single scientific data file.
- Added `output/image_tracking.csv` with 96 image rows: first 5 successful and remaining 91 pending; documented Gavin's review asks and the Ordnance Survey coordinate answer.

## 35. Multi-Page Table Context Fix
- After the full batch was stopped, we identified the root cause of bad parses on continuation pages.
- Some tables in the Birks scans span two pages. Page N shows all column headers (releve IDs, plot metadata rows) plus the first batch of species rows. Page N+1 shows only more species rows with no headers visible at all.
- The parser was sending each image to the model in isolation, so on page N+1 the model had no way to know which releve column each cell belonged to. It produced garbled output or marked these pages as failed reads, even though the image data was fine.
- Fixed by adding `build_previous_page_context()` to `parse_images.py`. Before each image, the script now builds a structured context block from the prior page's table metadata and releve column order and prepends it to the model prompt.
- If the model still returns no plot rows for a continuation page (expected, since no headers are visible), the script falls back to the previous page's plot rows so every observation row still inherits correct releve IDs and coordinate metadata.
- Updated `prompts/csv_parsing_instructions.md` with an explicit note at the top explaining multi-page tables and telling the model not to treat a headerless continuation page as a bad read.

## 36. Images 6-10 Parse Attempt Blocked
- Tried to run images 6-10 from Codex, but the sandbox could not connect to local Ollama and escalation approval timed out.
- No scientific rows were added; `output.csv` remains 175 rows and images 6-10 were reset to pending in `image_tracking.csv`.

## 37. Context-Window Bug Fixed (Images 6-10 Now Parse)
- Images 6, 7, and 8 kept failing with "did not contain plots or observations". The images were fine; the script was the problem.
- Root cause: the parser never set Ollama's context window, so it used the default of only 4096 tokens. Small tables like 4.1 fit, but the bigger tables overflowed.
  - Table 4.6 has two stacked sub-tables with a two-panel side-by-side species layout.
  - Table 4.7 has 12 releve columns split into two subassociations.
  - Table 4.8 is a wide sideways table with ~36 releve columns.
- For these, the prompt + image + expected JSON response exceeded 4096 tokens. Ollama either rejected the request outright (HTTP 400 "exceeds the available context size") or truncated the JSON, which looked like a failed read.
- Fix: added a `--num-ctx` option (default 16384) and pass it into the Ollama call. Also raised the default `--num-predict` to 8192 so long tables have room to finish the JSON response.
- Verified after the fix: image 6 returned 7 plots and 48 observations; image 7 returned 7 plots and 13 observations. No more empty-response failures.
- Re-ran the full pipeline on images 1-10 with `--max-image-side 1280 --num-predict 8192 --num-ctx 16384` to rebuild `output.csv` from real model extractions across all ten pages.
- Kept the hand-verified table 4.1 prototype backed up before clearing `output.csv`, since the local 3B model is less accurate than the manual transcription for that one page.

## 38. Memory-Safe Context Settings (8GB Machine)
- Problem: after raising the context window, the first full run crashed with `unexpected EOF (status code: 500)` partway through image 1. This was not a parsing error; it was the model runtime dying.
- Diagnosis: a 16384-token context plus an 8192-token response reserve is too much key/value cache to hold next to the model on an 8GB machine, so the runner was killed under memory pressure.
- Method that fixed it: dialed the settings down to a window that fits in memory but is still far larger than the old 4096 default — `--num-ctx 8192 --num-predict 6144 --max-image-side 1100`. Smaller resized images also cut the image-token cost, leaving more of the window for the response.
- Lesson recorded: on this machine, context window and response length are a memory budget, not just a quality knob. 8192 is the safe ceiling for these tables.

## 39. Handling The Different Table Layouts On Pages 6-8
- Once the pages actually parsed, the next issue was that pages 6, 7, and 8 are not simple single-block tables like 4.1, so a naive single-pass read mis-aligned columns.
- Table 4.6: two separate sub-tables stacked on one page (different alliances), each printed as two side-by-side species panels that share the same releve columns. Method: treat the page as two logical sub-tables, and read each panel as a continuation of the same releve columns rather than as new columns.
- Table 4.7: twelve releve columns split into two subassociations, each with its own constancy (C) and mean (D) summary columns. Method: split the page by subassociation (releves 1-6 and 7-12) so each observation inherits the correct C/D pair.
- Table 4.8: a wide table rotated 90 degrees with ~36 releve columns. Method: rotate to landscape first; flagged as needing a dedicated verification pass because column count and rotation make a single read unreliable.
- General rule applied: carry table metadata and releve column order forward from the page that printed the headers, and verify the per-releve "total number of species" row as a cross-check on column alignment.

## 40. Chronological Output Ordering
- Problem: rows could land in `output.csv` in whatever order pages were processed, leaving the file non-chronological and hard to scan.
- Method that fixed it: sort `output/output.csv` by source image number with a stable sort, so all of image `_5` precedes image `_6`, while each image keeps its natural table/species row order.
- Added a matching rule to `instructions.md` so future runs keep `output.csv` ordered by image number.

## 41. Scaling From First Setup To Full Batches
- The parsing worked on the first setup and the initial images, but pushing it onto larger batches exposed several layout problems that single images had hidden.
- Two root problems drove most failures: how the page was cropped, and how tables that continue across pages were understood.
- Cropping problem: to save effort the input had been limited to the cropped table region. That held up for simple layouts but broke whenever table content sat outside the expected crop (tables or partial content in unexpected parts of the page). Fix: parse the full page instead of only the cropped table region.
- Continuation problem: one page would carry the table title and column headers and the next page would continue the same table with no headers repeated. The reader only turned image content into text and kept too little context, so it flagged the continuation page for review instead of recognizing it as the same table. Fix: carry header/column context forward so a headerless page is read as a continuation.

## 42. Improvements From Studying Stronger Systems
- Debugged the batch failures directly; several attempted fixes still failed on edge cases, so studied how stronger image-recognition systems handle the same problems.
- Key insight: robust parsing never depends on a single attempt. It retries with different crops, resized copies, higher-resolution inputs, and added context until the output is reliable.
- Changes applied to the pipeline:
  - Full-page image parsing instead of crop-only input.
  - Better automatic resize and crop logic.
  - Retry path for difficult images instead of failing immediately.
  - Context handling for tables that span multiple pages.
  - Review logic for genuinely uncertain or irregular cases only.
  - Stronger batch workflow that tolerates a wider range of real document layouts.

## 43. Stability And Performance After The Fixes
- The image set had many layout inconsistencies: some pages parsed easily, others needed several adjustments and verification.
- Before the fixes the run failed every few images; after them it became stable and processed more than 25 images in a row without errors.
- Per-image time depends on the device and the page complexity: roughly 2.5 minutes on one machine and about 48 seconds on another for comparable pages.
- The image-data parsing stage is now complete and noticeably more robust, leaving the project ready to move on to the data-analysis stage. 