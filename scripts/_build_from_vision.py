#!/usr/bin/env python3
"""One-off builder: expand hand-read table transcriptions into output.csv rows.

This reuses the real pipeline's normalization functions so every generated row
matches the gold schema exactly (coordinate conversion, Domin cover ranges,
presence inference, column order). Transcriptions live in tables_data.py.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import parse_images as P  # noqa: E402
from tables_data import NON_OBSERVATION_IMAGES, TABLES  # noqa: E402

try:  # noqa: SIM105
    from tables_data_25_40 import TABLES_25_40  # noqa: E402
except ImportError:
    TABLES_25_40 = []

ALL_TABLES = TABLES + TABLES_25_40


def cell_to_raw(cell: str) -> tuple[str, str]:
    """Map a printed table cell into (domin_value, raw_value)."""
    c = cell.strip()
    if c in {"x", "X", "×", "✗"}:
        return "x", "x"
    return c, c


def build_observation_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for t in ALL_TABLES:
        image_file = t["image"]
        table_row = P.normalize_table(
            {
                "table_id": t["table_id_raw"],
                "class": t.get("class", ""),
                "order": t.get("order", ""),
                "alliance": t.get("alliance", ""),
                "association": t.get("association", ""),
                "n_releves": t.get("n_releves", ""),
                "total_species_reported": t.get("total_species", ""),
                "mean_species_per_releve": t.get("mean_species", ""),
                "notes": t.get("notes", ""),
            },
            image_file,
        )
        table_id = table_row["table_id"]

        plot_rows = [P.normalize_plot(r, table_id, image_file) for r in t["releves"]]
        plots_by_releve = {p["releve_id"]: p for p in plot_rows if p["releve_id"]}

        releve_ids = [r["releve_id"] for r in t["releves"]]
        for sp in t["species"]:
            cells = sp["cells"]
            assert len(cells) == len(releve_ids), (
                f"{table_id} {sp['name']}: {len(cells)} cells vs {len(releve_ids)} releves"
            )
            for releve_id, cell in zip(releve_ids, cells, strict=True):
                domin_value, raw_value = cell_to_raw(cell)
                low_conf = t.get("low_confidence", False)
                obs = {
                    "releve_id": releve_id,
                    "species": sp["name"],
                    "domin_value": domin_value,
                    "raw_value": raw_value,
                    "presence_binary": "",
                    "constancy_class": sp.get("C", ""),
                    "summary_value": sp.get("D", ""),
                    "needs_review": sp.get("needs_review", low_conf),
                    "note": sp.get("note") or (
                        "Rotated multi-column scan; some abundance cells uncertain, verify."
                        if low_conf else ""
                    ),
                }
                rows.append(
                    P.normalize_observation(obs, table_row, plots_by_releve, image_file)
                )
    return rows


def main() -> None:
    rows = build_observation_rows()

    # Image 1 (table 4.1) is taken verbatim from the hand-verified gold backup.
    import csv

    gold_path = Path("/tmp/gold_prototype_table_4_1.csv")
    gold_rows: list[dict[str, str]] = []
    if gold_path.exists():
        with gold_path.open(newline="", encoding="utf-8") as fh:
            # Keep only the genuine hand-verified table 4.1 rows. The backup also
            # held 6 stray junk rows mislabeled table_4_9; drop those.
            gold_rows = [r for r in csv.DictReader(fh) if r.get("table_id") == "table_4_1"]

    all_rows = gold_rows + rows

    # Keep output.csv ordered by source image number (..._5.png before ..._6.png).
    # A stable sort preserves each image's internal table/species order.
    def image_number(row: dict[str, str]) -> int:
        m = re.search(r"_(\d+)\.png$", row.get("image_file", ""))
        return int(m.group(1)) if m else 10**9

    all_rows.sort(key=image_number)

    P.save_rows(all_rows, Path("output/output.csv"), P.OBSERVATION_COLUMNS)
    print(f"Wrote {len(all_rows)} rows ({len(gold_rows)} gold + {len(rows)} transcribed)")

    # Per-table summary.
    from collections import Counter

    counts = Counter(r["table_id"] for r in all_rows)
    for tid in sorted(counts):
        print(f"  {tid}: {counts[tid]} rows")

    # Rebuild image_tracking.csv for all 96 source images.
    obs_by_image = Counter(r["image_file"] for r in all_rows)
    images = P.find_images(Path("images"))
    # Image 8 (table 4.8) is the rotated 26-releve page; transcribed but kept flagged.
    flagged = {8}
    image_notes = {
        13: "Transcribed from scan; table 4.13 releve 5 printed total is one higher than visible entries.",
        15: "Transcribed from scan; chemistry-only Table 4.16 not included in species output.",
        17: "Transcribed from scan; table 4.17 releve 5 printed total is one higher than visible entries.",
        19: "Transcribed from scan; table 4.19 releves 7-8 have visible plus marks that make counts one higher than printed totals.",
        20: "Transcribed from scan; table 4.20 visible entries put releve 3 one below and releve 4 one above printed totals.",
        22: "Transcribed from scan; table 4.22 visible entries put releve 5 one above the printed total.",
        24: "Transcribed from scan; table 4.24 has unresolved count mismatches in releves 1, 3, and 5.",
    }
    tracking_rows = []
    for idx, img in enumerate(images, start=1):
        image_file = str(img)
        n_obs = obs_by_image.get(image_file, 0)
        if idx == 1:
            status, note = "successful", "Reference table 4.1 (verified)."
        elif n_obs and idx in flagged:
            status, note = "successful", "Transcribed from scan; rotated multi-column page, some cells flagged for review."
        elif n_obs:
            status, note = "successful", image_notes.get(idx, "Transcribed from scan.")
        elif idx in NON_OBSERVATION_IMAGES:
            status, note = "successful", NON_OBSERVATION_IMAGES[idx]
        else:
            status, note = "pending", ""
        tracking_rows.append({
            "image_file": image_file,
            "image_number": str(idx),
            "status": status,
            "last_attempt_at": P.utc_timestamp() if n_obs or idx in NON_OBSERVATION_IMAGES else "",
            "error_type": "",
            "error_message": "",
            "observations_added": str(n_obs) if n_obs or idx in NON_OBSERVATION_IMAGES else "",
            "plots_detected": "",
            "tables_detected": "",
            "note": note,
        })
    P.save_rows(tracking_rows, Path("output/image_tracking.csv"), P.TRACKING_COLUMNS)
    done = sum(1 for r in tracking_rows if r["status"] == "successful")
    print(f"image_tracking.csv: {done} successful, {len(tracking_rows)-done} pending")


if __name__ == "__main__":
    main()
