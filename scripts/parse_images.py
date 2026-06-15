#!/usr/bin/env python3
"""Extract botanical survey data from local images with Ollama vision.

This is the main digitizing script.

It can run in three modes:
- tidy: the preferred mode. It writes analysis-ready CSVs:
  output/output.csv for species observations,
  output/plots.csv for plot/releve metadata,
  output/tables.csv for table-level metadata.
- table: an older helper mode. It tries to copy the printed table shape.
- json: an older specimen-label mode. It extracts one JSON record per image.

The current research goal is tidy mode because it is easiest to analyze later
with pandas, ordination, richness calculations, and resurvey comparisons.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import tempfile
from datetime import datetime, timezone
from io import StringIO
from json import JSONDecodeError
from pathlib import Path
from typing import Any

import ollama
import pandas as pd
from PIL import Image


# These defaults let the script run without typing long paths every time.
# The model is the smaller local vision model that works on the 8GB MacBook Air.
DEFAULT_MODEL = "qwen2.5vl:3b"
DEFAULT_IMAGES_DIR = Path("images")
DEFAULT_OUTPUT_PATH = Path("output/output.csv")
DEFAULT_PLOTS_OUTPUT_PATH = Path("output/plots.csv")
DEFAULT_TABLES_OUTPUT_PATH = Path("output/tables.csv")
DEFAULT_STATUS_PATH = Path("output/processed_images.json")
DEFAULT_FAILED_OUTPUT_PATH = Path("output/failed_images.csv")
DEFAULT_PROMPT_FILE = Path("prompts/csv_parsing_instructions.md")
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

# Columns for the preferred long-format observation CSV.
# One row means: one species in one plot/releve.
OBSERVATION_COLUMNS = [
    "table_id",
    "image_file",
    "class",
    "order",
    "alliance",
    "association",
    "releve_id",
    "ref_code",
    "map_reference",
    "os_grid_square",
    "os_grid_reference",
    "easting",
    "northing",
    "latitude",
    "longitude",
    "altitude_ft",
    "altitude_m",
    "aspect_deg",
    "slope_deg",
    "cover_pct",
    "plot_area_m2",
    "species_reported",
    "species",
    "domin_value",
    "domin_cover_min_pct",
    "domin_cover_max_pct",
    "presence_binary",
    "raw_value",
    "constancy_class",
    "summary_value",
    "total_species_reported",
    "needs_review",
    "note",
]

# Columns for plot/releve metadata.
# These describe each plot once, instead of repeating them by species.
PLOT_COLUMNS = [
    "table_id",
    "image_file",
    "releve_id",
    "ref_code",
    "map_reference",
    "os_grid_square",
    "os_grid_reference",
    "easting",
    "northing",
    "latitude",
    "longitude",
    "altitude_ft",
    "altitude_m",
    "aspect_deg",
    "slope_deg",
    "cover_pct",
    "plot_area_m2",
    "species_reported",
    "needs_review",
    "note",
]

# Columns for table-level metadata.
# These describe one printed table or association page.
TABLE_COLUMNS = [
    "table_id",
    "image_file",
    "class",
    "order",
    "alliance",
    "association",
    "n_releves",
    "total_species_reported",
    "mean_species_per_releve",
    "notes",
]

# A separate failure file keeps errors out of the scientific observation data.
FAILURE_COLUMNS = [
    "filename",
    "error_type",
    "error_message",
    "timestamp",
]

# Columns for the older printed-table reconstruction mode.
# This keeps the visual table shape but is less useful for analysis.
TABLE_OUTPUT_COLUMNS = [
    "row_label",
    "plot_1",
    "plot_2",
    "plot_3",
    "plot_4",
    "plot_5",
    "plot_6",
    "plot_7",
    "C",
    "D",
]

# Columns for the older specimen-style JSON mode.
# This is kept for comparison but is not the current target.
JSON_OUTPUT_COLUMNS = [
    "image_file",
    "species_name",
    "location",
    "coordinates",
    "date",
    "collector",
    "notes",
    "other_visible_fields",
    "parse_status",
    "parse_error",
    "raw_response",
]

JSON_EXTRACTION_PROMPT = """
You are digitizing geo-botanical research scans for a CSV dataset.

Read the image carefully. Return exactly one JSON object and no markdown.
Use empty strings when a field is not visible. Preserve uncertain text in notes.

Required JSON keys:
{
  "species_name": "",
  "location": "",
  "coordinates": "",
  "date": "",
  "collector": "",
  "notes": "",
  "other_visible_fields": {}
}

Rules:
- species_name should be the botanical name exactly as visible.
- coordinates should include any grid reference, latitude/longitude, or map reference.
- notes should include uncertainty, illegible text, page side, abundance, habitat, or table context.
- other_visible_fields should contain any visible labels that do not fit the required fields.
"""


def build_parser() -> argparse.ArgumentParser:
    """Define all command-line options for the script.

    argparse turns terminal flags like --limit 5 into Python values.
    Keeping these options here makes the script reusable for small tests,
    resumed runs, and full-batch processing.
    """
    parser = argparse.ArgumentParser(
        description="Parse local botanical images into CSV outputs using Ollama."
    )
    parser.add_argument("--images-dir", type=Path, default=DEFAULT_IMAGES_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--plots-output", type=Path, default=DEFAULT_PLOTS_OUTPUT_PATH)
    parser.add_argument("--tables-output", type=Path, default=DEFAULT_TABLES_OUTPUT_PATH)
    parser.add_argument("--status-file", type=Path, default=DEFAULT_STATUS_PATH)
    parser.add_argument("--failed-output", type=Path, default=DEFAULT_FAILED_OUTPUT_PATH)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument(
        "--mode",
        choices=("tidy", "table", "json"),
        default="tidy",
        help="Use tidy mode for analysis-ready CSVs, table mode for printed-table CSV, or json mode for older specimen-style extraction.",
    )
    parser.add_argument(
        "--prompt-file",
        type=Path,
        default=DEFAULT_PROMPT_FILE,
        help="Prompt file used in tidy and table modes.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Retained for command compatibility. Durable runs now save after every image.",
    )
    parser.add_argument(
        "--skip",
        type=int,
        default=0,
        help="Skip this many naturally sorted images before applying --limit. Example: --skip 5 --limit 10 parses images 6-15.",
    )
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="With --resume, retry images whose previous extraction attempt failed.",
    )
    parser.add_argument("--keep-raw", action="store_true")
    parser.add_argument(
        "--max-image-side",
        type=int,
        default=1600,
        help="Resize a temporary copy so the longest image side is at most this many pixels. Use 0 to send originals.",
    )
    parser.add_argument(
        "--num-predict",
        type=int,
        default=2048,
        help="Maximum response tokens Ollama can generate per image. Use 0 for the model default.",
    )
    return parser


def find_images(images_dir: Path) -> list[Path]:
    """Find all supported image files and return them in natural order.

    Natural order matters because filenames like image_10 should come after
    image_2, not immediately after image_1.
    """
    if not images_dir.exists():
        raise FileNotFoundError(f"Images directory does not exist: {images_dir}")

    images = [
        path
        for path in images_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(images, key=natural_sort_key)


def natural_sort_key(path: Path) -> list[int | str]:
    """Split a filename into text and number pieces for human-style sorting."""
    parts = re.split(r"(\d+)", str(path))
    return [int(part) if part.isdigit() else part.lower() for part in parts]


def read_prompt(prompt_file: Path) -> str:
    """Load the extraction prompt that tells the model what to return."""
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file does not exist: {prompt_file}")
    return prompt_file.read_text(encoding="utf-8").strip()


def prepare_image_for_ollama(image_path: Path, max_image_side: int) -> tuple[Path, Path | None]:
    """Create a smaller temporary image for Ollama when the scan is large.

    The original file is never changed. If the image is already small enough,
    the original path is returned. If it is too large, the function saves a
    temporary JPEG and returns that path plus the same path as a cleanup target.
    """
    with Image.open(image_path) as image:
        image.load()

        # A max side of 0 means "do not resize".
        if max_image_side <= 0 or max(image.size) <= max_image_side:
            return image_path, None

        # thumbnail keeps the aspect ratio, so the page is not stretched.
        image.thumbnail((max_image_side, max_image_side), Image.Resampling.LANCZOS)
        if image.mode not in {"RGB", "L"}:
            image = image.convert("RGB")

        with tempfile.NamedTemporaryFile(
            prefix=f"{image_path.stem}_",
            suffix=".jpg",
            delete=False,
        ) as temporary_file:
            resized_path = Path(temporary_file.name)

        image.save(resized_path, format="JPEG", quality=92)
        return resized_path, resized_path


def extract_json_object(text: str) -> dict[str, Any]:
    """Pull the first valid JSON object out of a model response.

    Local models sometimes add text before or after JSON. This scans forward
    until it finds a parseable object, instead of failing on the first extra
    character.
    """
    decoder = json.JSONDecoder()
    for index, character in enumerate(text):
        if character != "{":
            continue
        try:
            parsed, _ = decoder.raw_decode(text[index:])
        except JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    raise ValueError("The model response did not contain a JSON object.")


def normalize_cell(value: Any) -> str:
    """Convert any extracted value into a clean string for CSV writing."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value).strip()


def normalize_table_id(value: Any, fallback: str) -> str:
    """Return table ids in a stable machine-readable form like table_4_1."""
    text = normalize_cell(value).lower()
    match = re.search(r"table\s+(\d+)\.(\d+)", text)
    if match:
        return f"table_{match.group(1)}_{match.group(2)}"

    cleaned = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return cleaned or fallback


def domin_cover_range(domin_value: str) -> tuple[str, str]:
    """Convert Domin scale categories into approximate percent-cover ranges.

    Values 1-10 follow the 10-point Domin scale Gavin provided. A period means
    the species was not detected, so its cover range is 0-0. Presence-only
    marks like x do not have a cover range, so those stay blank.
    """
    ranges = {
        "1": ("0", "4"),
        "2": ("0", "4"),
        "3": ("0", "4"),
        "4": ("4", "10"),
        "5": ("10", "25"),
        "6": ("25", "33"),
        "7": ("33", "50"),
        "8": ("50", "75"),
        "9": ("75", "90"),
        "10": ("90", "100"),
        ".": ("0", "0"),
    }
    return ranges.get(domin_value.strip(), ("", ""))


def normalize_os_grid_square(value: Any) -> str:
    """Keep only a valid two-letter British National Grid square code."""
    text = normalize_cell(value).upper().replace(" ", "")
    return text if re.fullmatch(r"[A-HJ-Z]{2}", text) else ""


def normalize_map_reference(value: Any) -> str:
    """Keep map reference digits only, for example 504446."""
    return re.sub(r"\D", "", normalize_cell(value))


def build_os_grid_reference(os_grid_square: str, map_reference: str) -> str:
    """Combine grid square and numeric reference, for example NG504446."""
    if not os_grid_square or not map_reference:
        return ""
    return f"{os_grid_square}{map_reference}"


def os_grid_to_easting_northing(os_grid_square: str, map_reference: str) -> tuple[str, str]:
    """Convert a British National Grid reference into easting/northing metres.

    The two-letter grid square gives the 100 km square. The numeric reference
    gives the finer easting/northing inside that square. Six digits means
    100 m precision, eight digits means 10 m precision, and ten digits means
    1 m precision.
    """
    square = normalize_os_grid_square(os_grid_square)
    digits = normalize_map_reference(map_reference)
    if not square or len(digits) % 2 != 0 or len(digits) < 2:
        return "", ""

    letters = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
    first = letters.find(square[0])
    second = letters.find(square[1])
    if first < 0 or second < 0:
        return "", ""

    easting_100km = ((first - 2) % 5) * 5 + (second % 5)
    northing_100km = 19 - (first // 5) * 5 - (second // 5)

    half = len(digits) // 2
    easting_digits = digits[:half]
    northing_digits = digits[half:]
    scale = 10 ** (5 - half)

    easting = easting_100km * 100000 + int(easting_digits) * scale
    northing = northing_100km * 100000 + int(northing_digits) * scale
    return str(easting), str(northing)


def osgb36_to_wgs84(easting: str, northing: str) -> tuple[str, str]:
    """Convert British National Grid easting/northing to WGS84 lat/lon.

    This is an offline implementation of the standard OSGB36 to WGS84
    transformation, so the pipeline can run without calling an external API.
    """
    if not easting or not northing:
        return "", ""

    easting_float = float(easting)
    northing_float = float(northing)

    airy_a = 6377563.396
    airy_b = 6356256.909
    f0 = 0.9996012717
    lat0 = math.radians(49)
    lon0 = math.radians(-2)
    n0 = -100000
    e0 = 400000
    e2 = 1 - (airy_b * airy_b) / (airy_a * airy_a)
    n = (airy_a - airy_b) / (airy_a + airy_b)

    lat = lat0
    meridional_arc = 0.0
    while northing_float - n0 - meridional_arc >= 0.00001:
        lat = (northing_float - n0 - meridional_arc) / (airy_a * f0) + lat
        ma = (1 + n + 1.25 * n**2 + 1.25 * n**3) * (lat - lat0)
        mb = (3 * n + 3 * n**2 + 2.625 * n**3) * math.sin(lat - lat0) * math.cos(lat + lat0)
        mc = (1.875 * n**2 + 1.875 * n**3) * math.sin(2 * (lat - lat0)) * math.cos(2 * (lat + lat0))
        md = (35 / 24 * n**3) * math.sin(3 * (lat - lat0)) * math.cos(3 * (lat + lat0))
        meridional_arc = airy_b * f0 * (ma - mb + mc - md)

    sin_lat = math.sin(lat)
    cos_lat = math.cos(lat)
    nu = airy_a * f0 / math.sqrt(1 - e2 * sin_lat**2)
    rho = airy_a * f0 * (1 - e2) / (1 - e2 * sin_lat**2) ** 1.5
    eta2 = nu / rho - 1
    tan_lat = math.tan(lat)
    sec_lat = 1 / cos_lat
    d_easting = easting_float - e0

    vii = tan_lat / (2 * rho * nu)
    viii = tan_lat / (24 * rho * nu**3) * (5 + 3 * tan_lat**2 + eta2 - 9 * tan_lat**2 * eta2)
    ix = tan_lat / (720 * rho * nu**5) * (61 + 90 * tan_lat**2 + 45 * tan_lat**4)
    x = sec_lat / nu
    xi = sec_lat / (6 * nu**3) * (nu / rho + 2 * tan_lat**2)
    xii = sec_lat / (120 * nu**5) * (5 + 28 * tan_lat**2 + 24 * tan_lat**4)
    xiia = sec_lat / (5040 * nu**7) * (61 + 662 * tan_lat**2 + 1320 * tan_lat**4 + 720 * tan_lat**6)

    osgb_lat = lat - vii * d_easting**2 + viii * d_easting**4 - ix * d_easting**6
    osgb_lon = lon0 + x * d_easting - xi * d_easting**3 + xii * d_easting**5 - xiia * d_easting**7
    wgs_lat, wgs_lon = helmert_osgb36_to_wgs84(osgb_lat, osgb_lon)
    return f"{wgs_lat:.6f}", f"{wgs_lon:.6f}"


def helmert_osgb36_to_wgs84(lat: float, lon: float) -> tuple[float, float]:
    """Apply the OSGB36 to WGS84 Helmert transform."""
    airy_a = 6377563.396
    airy_b = 6356256.909
    wgs_a = 6378137.0
    wgs_b = 6356752.3141

    x, y, z = lat_lon_to_cartesian(lat, lon, airy_a, airy_b)
    tx, ty, tz = 446.448, -125.157, 542.060
    rx = math.radians(0.1502 / 3600)
    ry = math.radians(0.2470 / 3600)
    rz = math.radians(0.8421 / 3600)
    s = -20.4894 * 1e-6

    x2 = tx + (1 + s) * x - rz * y + ry * z
    y2 = ty + rz * x + (1 + s) * y - rx * z
    z2 = tz - ry * x + rx * y + (1 + s) * z
    return cartesian_to_lat_lon(x2, y2, z2, wgs_a, wgs_b)


def lat_lon_to_cartesian(lat: float, lon: float, axis_a: float, axis_b: float) -> tuple[float, float, float]:
    """Convert latitude/longitude radians to Cartesian x/y/z."""
    e2 = 1 - (axis_b * axis_b) / (axis_a * axis_a)
    nu = axis_a / math.sqrt(1 - e2 * math.sin(lat) ** 2)
    x = nu * math.cos(lat) * math.cos(lon)
    y = nu * math.cos(lat) * math.sin(lon)
    z = (1 - e2) * nu * math.sin(lat)
    return x, y, z


def cartesian_to_lat_lon(x: float, y: float, z: float, axis_a: float, axis_b: float) -> tuple[float, float]:
    """Convert Cartesian x/y/z to latitude/longitude decimal degrees."""
    e2 = 1 - (axis_b * axis_b) / (axis_a * axis_a)
    p = math.sqrt(x * x + y * y)
    lat = math.atan2(z, p * (1 - e2))
    previous_lat = 0.0
    while abs(lat - previous_lat) > 1e-12:
        previous_lat = lat
        nu = axis_a / math.sqrt(1 - e2 * math.sin(lat) ** 2)
        lat = math.atan2(z + e2 * nu * math.sin(lat), p)
    lon = math.atan2(y, x)
    return math.degrees(lat), math.degrees(lon)


def clean_csv_response(text: str) -> str:
    """Remove markdown wrappers and keep the CSV-looking part of a response."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:csv)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    lines = [line for line in cleaned.splitlines() if line.strip()]
    for index, line in enumerate(lines):
        if line.strip().lower().startswith("row_label,"):
            return "\n".join(lines[index:])
    return "\n".join(lines)


def parse_table_csv(text: str) -> list[dict[str, str]]:
    """Parse older printed-table CSV output into row dictionaries.

    This mode is kept because it can be useful for debugging OCR alignment.
    It is not the preferred final research format.
    """
    cleaned = clean_csv_response(text)
    reader = csv.reader(StringIO(cleaned))
    rows = list(reader)
    if not rows:
        raise ValueError("The model response did not contain CSV rows.")

    header = [cell.strip() for cell in rows[0]]
    data_rows = rows[1:] if header == TABLE_OUTPUT_COLUMNS else rows

    parsed_rows: list[dict[str, str]] = []
    for row in data_rows:
        normalized = [cell.strip() for cell in row]
        if not any(normalized):
            continue
        if len(normalized) < len(TABLE_OUTPUT_COLUMNS):
            normalized.extend([""] * (len(TABLE_OUTPUT_COLUMNS) - len(normalized)))
        if len(normalized) > len(TABLE_OUTPUT_COLUMNS):
            normalized = normalized[: len(TABLE_OUTPUT_COLUMNS) - 1] + [
                ",".join(normalized[len(TABLE_OUTPUT_COLUMNS) - 1 :])
            ]
        parsed_rows.append(dict(zip(TABLE_OUTPUT_COLUMNS, normalized, strict=True)))

    if not parsed_rows:
        raise ValueError("The model response contained only a CSV header.")
    return parsed_rows


def call_ollama_image(
    image_path: Path,
    model: str,
    prompt: str,
    max_image_side: int,
    num_predict: int,
    response_format: str | None = None,
) -> str:
    """Send one image and one prompt to Ollama, then return the model text.

    This is the only function that talks directly to Ollama. Keeping the
    Ollama call in one place makes resizing, token limits, and cleanup easier
    to reason about.
    """
    ollama_image_path, temporary_path = prepare_image_for_ollama(image_path, max_image_side)
    options = {"temperature": 0}
    if num_predict > 0:
        options["num_predict"] = num_predict

    request: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "images": [str(ollama_image_path)],
        "options": options,
    }
    if response_format is not None:
        request["format"] = response_format

    try:
        response = ollama.generate(**request)
    finally:
        # Delete temporary resized images even if Ollama errors.
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    return response.get("response", "")


def normalize_observation(
    raw_row: dict[str, Any],
    table_row: dict[str, str],
    plots_by_releve: dict[str, dict[str, str]],
    image_file: str,
) -> dict[str, str]:
    """Turn one model observation into one clean output/output.csv row.

    The model only has to provide the species, releve id, and cell value.
    This function adds table metadata and plot metadata so every observation
    row is self-contained and easy to analyze later.
    """
    releve_id = normalize_cell(raw_row.get("releve_id"))
    plot_row = plots_by_releve.get(releve_id, {})
    raw_value = normalize_cell(raw_row.get("raw_value"))
    domin_value = normalize_cell(raw_row.get("domin_value"))
    cover_min, cover_max = domin_cover_range(domin_value)
    presence = normalize_cell(raw_row.get("presence_binary"))

    # If the model forgets the presence flag, infer it from the extracted cell.
    # "." means absent. Anything else is treated as present unless reviewed.
    if not presence:
        presence = "0" if raw_value == "." or domin_value == "." else "1"

    return {
        "table_id": table_row["table_id"],
        "image_file": image_file,
        "class": table_row["class"],
        "order": table_row["order"],
        "alliance": table_row["alliance"],
        "association": table_row["association"],
        "releve_id": releve_id,
        "ref_code": plot_row.get("ref_code", ""),
        "map_reference": plot_row.get("map_reference", ""),
        "os_grid_square": plot_row.get("os_grid_square", ""),
        "os_grid_reference": plot_row.get("os_grid_reference", ""),
        "easting": plot_row.get("easting", ""),
        "northing": plot_row.get("northing", ""),
        "latitude": plot_row.get("latitude", ""),
        "longitude": plot_row.get("longitude", ""),
        "altitude_ft": plot_row.get("altitude_ft", ""),
        "altitude_m": plot_row.get("altitude_m", ""),
        "aspect_deg": plot_row.get("aspect_deg", ""),
        "slope_deg": plot_row.get("slope_deg", ""),
        "cover_pct": plot_row.get("cover_pct", ""),
        "plot_area_m2": plot_row.get("plot_area_m2", ""),
        "species_reported": plot_row.get("species_reported", ""),
        "species": normalize_cell(raw_row.get("species")),
        "domin_value": domin_value,
        "domin_cover_min_pct": cover_min,
        "domin_cover_max_pct": cover_max,
        "presence_binary": presence,
        "raw_value": raw_value,
        "constancy_class": normalize_cell(raw_row.get("constancy_class")),
        "summary_value": normalize_cell(raw_row.get("summary_value")),
        "total_species_reported": table_row["total_species_reported"],
        "needs_review": normalize_cell(raw_row.get("needs_review")),
        "note": normalize_cell(raw_row.get("note")),
    }


def normalize_plot(
    raw_row: dict[str, Any],
    table_id: str,
    image_file: str,
) -> dict[str, str]:
    """Turn one model plot object into one output/plots.csv row."""
    map_reference = normalize_map_reference(raw_row.get("map_reference"))
    os_grid_square = normalize_os_grid_square(raw_row.get("os_grid_square"))
    os_grid_reference = build_os_grid_reference(os_grid_square, map_reference)
    easting, northing = os_grid_to_easting_northing(os_grid_square, map_reference)
    latitude = normalize_cell(raw_row.get("latitude"))
    longitude = normalize_cell(raw_row.get("longitude"))
    if not latitude and not longitude:
        latitude, longitude = osgb36_to_wgs84(easting, northing)

    return {
        "table_id": table_id,
        "image_file": image_file,
        "releve_id": normalize_cell(raw_row.get("releve_id")),
        "ref_code": normalize_cell(raw_row.get("ref_code")),
        "map_reference": map_reference,
        "os_grid_square": os_grid_square,
        "os_grid_reference": os_grid_reference,
        "easting": easting,
        "northing": northing,
        "latitude": latitude,
        "longitude": longitude,
        "altitude_ft": normalize_cell(raw_row.get("altitude_ft")),
        "altitude_m": normalize_cell(raw_row.get("altitude_m")),
        "aspect_deg": normalize_cell(raw_row.get("aspect_deg")),
        "slope_deg": normalize_cell(raw_row.get("slope_deg")),
        "cover_pct": normalize_cell(raw_row.get("cover_pct")),
        "plot_area_m2": normalize_cell(raw_row.get("plot_area_m2")),
        "species_reported": normalize_cell(raw_row.get("species_reported")),
        "needs_review": normalize_cell(raw_row.get("needs_review")),
        "note": normalize_cell(raw_row.get("note")),
    }


def normalize_table(
    raw_metadata: dict[str, Any],
    image_file: str,
) -> dict[str, str]:
    """Turn table-level model metadata into one output/tables.csv row."""
    return {
        "table_id": normalize_table_id(raw_metadata.get("table_id"), Path(image_file).stem),
        "image_file": image_file,
        "class": normalize_cell(raw_metadata.get("class")),
        "order": normalize_cell(raw_metadata.get("order")),
        "alliance": normalize_cell(raw_metadata.get("alliance")),
        "association": normalize_cell(raw_metadata.get("association")),
        "n_releves": normalize_cell(raw_metadata.get("n_releves")),
        "total_species_reported": normalize_cell(raw_metadata.get("total_species_reported")),
        "mean_species_per_releve": normalize_cell(raw_metadata.get("mean_species_per_releve")),
        "notes": normalize_cell(raw_metadata.get("notes")),
    }


def parse_tidy_image(
    image_path: Path,
    model: str,
    prompt: str,
    max_image_side: int,
    num_predict: int,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    """Parse one image into table rows, plot rows, and observation rows.

    Tidy mode asks the model for JSON because JSON is easier to validate than
    raw CSV when the answer contains nested data. The script then converts the
    JSON into normal CSV files.
    """
    raw_response = call_ollama_image(
        image_path=image_path,
        model=model,
        prompt=prompt,
        max_image_side=max_image_side,
        num_predict=num_predict,
        response_format="json",
    )
    parsed = extract_json_object(raw_response)

    metadata = parsed.get("table_metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}

    table_row = normalize_table(metadata, str(image_path))
    table_id = table_row["table_id"] or image_path.stem

    # Plot rows are normalized first so observation rows can inherit plot data.
    raw_plots = parsed.get("plots", [])
    if not isinstance(raw_plots, list):
        raw_plots = []
    plot_rows = [
        normalize_plot(plot, table_id, str(image_path))
        for plot in raw_plots
        if isinstance(plot, dict)
    ]
    plots_by_releve = {
        plot["releve_id"]: plot
        for plot in plot_rows
        if plot["releve_id"]
    }

    # Observation rows are long format: one species in one releve per row.
    raw_observations = parsed.get("observations", [])
    if not isinstance(raw_observations, list):
        raw_observations = []
    observation_rows = [
        normalize_observation(observation, table_row, plots_by_releve, str(image_path))
        for observation in raw_observations
        if isinstance(observation, dict)
    ]

    if not plot_rows and not observation_rows:
        raise ValueError("The model response did not contain plots or observations.")

    # If no printed table id was found, use the image filename as a stable id.
    if not table_row["table_id"]:
        table_row["table_id"] = table_id

    return [table_row], plot_rows, observation_rows


def parse_json_image(
    image_path: Path,
    model: str,
    keep_raw: bool,
    max_image_side: int,
    num_predict: int,
) -> dict[str, str]:
    """Run the older specimen-style parser for one image.

    This is not the current research path, but keeping it available makes it
    possible to compare against earlier tests.
    """
    raw_response = call_ollama_image(
        image_path=image_path,
        model=model,
        prompt=JSON_EXTRACTION_PROMPT.strip(),
        max_image_side=max_image_side,
        num_predict=num_predict,
        response_format="json",
    )
    parsed = extract_json_object(raw_response)

    return {
        "image_file": str(image_path),
        "species_name": normalize_cell(parsed.get("species_name")),
        "location": normalize_cell(parsed.get("location")),
        "coordinates": normalize_cell(parsed.get("coordinates")),
        "date": normalize_cell(parsed.get("date")),
        "collector": normalize_cell(parsed.get("collector")),
        "notes": normalize_cell(parsed.get("notes")),
        "other_visible_fields": normalize_cell(parsed.get("other_visible_fields")),
        "parse_status": "ok",
        "parse_error": "",
        "raw_response": raw_response if keep_raw else "",
    }


def parse_table_image(
    image_path: Path,
    model: str,
    prompt: str,
    max_image_side: int,
    num_predict: int,
) -> list[dict[str, str]]:
    """Run the older printed-table reconstruction parser for one image."""
    raw_response = call_ollama_image(
        image_path=image_path,
        model=model,
        prompt=prompt,
        max_image_side=max_image_side,
        num_predict=num_predict,
    )
    return parse_table_csv(raw_response)


def load_existing_rows(output_path: Path, columns: list[str]) -> pd.DataFrame:
    """Load a previous CSV, or return an empty frame with the expected columns."""
    if not output_path.exists():
        return pd.DataFrame(columns=columns)
    return pd.read_csv(output_path, dtype=str).fillna("")


def save_rows(rows: list[dict[str, str]], output_path: Path, columns: list[str]) -> None:
    """Atomically save rows to CSV in a stable column order.

    Stable column order keeps the output easy to compare in git and easy to
    read in spreadsheet tools. Writing a temporary file first prevents a crash
    during saving from leaving a half-written CSV.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(rows)
    for column in columns:
        if column not in frame.columns:
            frame[column] = ""
    frame = frame[columns]
    temporary_path = output_path.with_name(f".{output_path.name}.tmp")
    frame.to_csv(temporary_path, index=False)
    temporary_path.replace(output_path)


def utc_timestamp() -> str:
    """Return a timezone-aware timestamp suitable for logs and JSON files."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def empty_status_data() -> dict[str, Any]:
    """Create the top-level structure used by processed_images.json."""
    return {"version": 1, "images": {}}


def load_status_data(status_path: Path, resume: bool) -> dict[str, Any]:
    """Load durable image statuses, or start a fresh status file.

    A non-resume run intentionally starts fresh. A resume run validates the
    existing JSON so damaged state is reported instead of silently ignored.
    """
    if not resume or not status_path.exists():
        return empty_status_data()

    with status_path.open(encoding="utf-8") as status_file:
        data = json.load(status_file)
    if not isinstance(data, dict) or not isinstance(data.get("images"), dict):
        raise ValueError(f"Invalid status file structure: {status_path}")
    return data


def save_status_data(status_data: dict[str, Any], status_path: Path) -> None:
    """Atomically save processed image status so resume data remains valid."""
    status_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = status_path.with_name(f".{status_path.name}.tmp")
    with temporary_path.open("w", encoding="utf-8") as status_file:
        json.dump(status_data, status_file, indent=2, ensure_ascii=False, sort_keys=True)
        status_file.write("\n")
    temporary_path.replace(status_path)


def status_record(status_data: dict[str, Any], image_path: Path) -> dict[str, Any]:
    """Return one image's saved status record, or an empty record."""
    record = status_data["images"].get(str(image_path), {})
    return record if isinstance(record, dict) else {}


def previous_result(record: dict[str, Any]) -> str:
    """Return the last extraction result even if the latest action was skipped."""
    result = record.get("result_status")
    if result in {"success", "failed"}:
        return result
    status = record.get("status")
    return status if status in {"success", "failed"} else ""


def skip_reason(record: dict[str, Any], retry_failed: bool) -> str:
    """Explain why resume should skip an image, or return an empty string."""
    result = previous_result(record)
    if result == "success":
        return "already successful"
    if result == "failed" and not retry_failed:
        return "previously failed; use --retry-failed to retry"
    return ""


def update_status(
    status_data: dict[str, Any],
    image_path: Path,
    status: str,
    *,
    error_message: str = "",
    output_row_counts: dict[str, int] | None = None,
    reason: str = "",
) -> None:
    """Record the latest action and preserve the last real extraction result.

    The visible status can be success, failed, or skipped. result_status keeps
    the last actual extraction outcome, so marking an already successful image
    as skipped does not make a later resume accidentally process it again.
    """
    old_record = status_record(status_data, image_path)
    result_status = previous_result(old_record)
    if status in {"success", "failed"}:
        result_status = status

    if status == "skipped" and not error_message:
        error_message = str(old_record.get("error_message", ""))

    status_data["images"][str(image_path)] = {
        "filename": str(image_path),
        "status": status,
        "result_status": result_status,
        "timestamp": utc_timestamp(),
        "error_message": error_message,
        "skip_reason": reason,
        "output_row_counts": output_row_counts or old_record.get("output_row_counts", {}),
    }


def append_failure(
    failure_rows: list[dict[str, str]], image_path: Path, error: Exception
) -> None:
    """Append one failed extraction attempt to failed_images.csv data."""
    failure_rows.append(
        {
            "filename": str(image_path),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": utc_timestamp(),
        }
    )


def record_command_skips(status_data: dict[str, Any], args: argparse.Namespace) -> int:
    """Record images deliberately excluded by --skip without marking them done.

    Their visible status is skipped, but result_status remains empty unless an
    earlier run actually succeeded or failed. A later full resume can therefore
    still process an image that was only excluded by command selection.
    """
    for image_path in args.explicitly_skipped:
        reason = "excluded by --skip"
        update_status(status_data, image_path, "skipped", reason=reason)
        print(f"SKIPPED: {image_path.name} - {reason}", flush=True)
    return len(args.explicitly_skipped)


def save_tidy_outputs(
    args: argparse.Namespace,
    observation_rows: list[dict[str, str]],
    plot_rows: list[dict[str, str]],
    table_rows: list[dict[str, str]],
    status_data: dict[str, Any],
    failure_rows: list[dict[str, str]],
) -> None:
    """Save all tidy CSVs, statuses, and failures after one image."""
    save_rows(observation_rows, args.output, OBSERVATION_COLUMNS)
    save_rows(plot_rows, args.plots_output, PLOT_COLUMNS)
    save_rows(table_rows, args.tables_output, TABLE_COLUMNS)
    save_status_data(status_data, args.status_file)
    save_rows(failure_rows, args.failed_output, FAILURE_COLUMNS)


def print_run_summary(
    args: argparse.Namespace,
    successful: int,
    skipped: int,
    failed: int,
) -> None:
    """Print the counts and files needed to review or resume the run."""
    print("\nRun summary")
    print(f"Total images found: {args.total_images_found}")
    print(f"Processed successfully: {successful}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")
    print(f"Observations: {args.output}")
    if args.mode == "tidy":
        print(f"Plots: {args.plots_output}")
        print(f"Tables: {args.tables_output}")
    print(f"Status: {args.status_file}")
    print(f"Failures: {args.failed_output}")


def run_tidy_mode(args: argparse.Namespace, images: list[Path]) -> None:
    """Run the preferred analysis-ready extraction workflow.

    This writes three linked files:
    - output/output.csv for long-format species observations
    - output/plots.csv for plot/releve metadata
    - output/tables.csv for table-level metadata
    """
    prompt = read_prompt(args.prompt_file)

    # Resume mode starts from existing CSVs instead of starting over.
    observation_rows = (
        load_existing_rows(args.output, OBSERVATION_COLUMNS).to_dict("records")
        if args.resume
        else []
    )
    plot_rows = (
        load_existing_rows(args.plots_output, PLOT_COLUMNS).to_dict("records")
        if args.resume
        else []
    )
    table_rows = (
        load_existing_rows(args.tables_output, TABLE_COLUMNS).to_dict("records")
        if args.resume
        else []
    )
    status_data = load_status_data(args.status_file, args.resume)
    failure_rows = (
        load_existing_rows(args.failed_output, FAILURE_COLUMNS).to_dict("records")
        if args.resume
        else []
    )
    successful = 0
    failed = 0

    # If this is the first run with a status file, import successful image paths
    # from tables.csv so older resume data still protects completed work.
    if args.resume:
        for row in table_rows:
            image_file = row.get("image_file", "")
            if (
                image_file
                and Path(image_file).exists()
                and image_file not in status_data["images"]
            ):
                update_status(status_data, Path(image_file), "success")

    skipped = record_command_skips(status_data, args)

    save_tidy_outputs(
        args,
        observation_rows,
        plot_rows,
        table_rows,
        status_data,
        failure_rows,
    )

    for image_path in images:
        position = args.image_positions[str(image_path)]
        record = status_record(status_data, image_path)
        reason = skip_reason(record, args.retry_failed) if args.resume else ""
        if reason:
            skipped += 1
            update_status(status_data, image_path, "skipped", reason=reason)
            save_tidy_outputs(
                args,
                observation_rows,
                plot_rows,
                table_rows,
                status_data,
                failure_rows,
            )
            print(f"SKIPPED: {image_path.name} - {reason}", flush=True)
            continue

        print(
            f"Processing {position}/{args.total_images_found}: {image_path.name}",
            flush=True,
        )
        try:
            # Remove this image's old rows before a retry. This prevents
            # duplicates if a previous run saved CSVs but stopped before its
            # success status reached processed_images.json.
            image_name = str(image_path)
            observation_rows = [
                row for row in observation_rows if row.get("image_file") != image_name
            ]
            plot_rows = [
                row for row in plot_rows if row.get("image_file") != image_name
            ]
            table_rows = [
                row for row in table_rows if row.get("image_file") != image_name
            ]
            image_tables, image_plots, image_observations = parse_tidy_image(
                image_path,
                args.model,
                prompt,
                args.max_image_side,
                args.num_predict,
            )
            table_rows.extend(image_tables)
            plot_rows.extend(image_plots)
            observation_rows.extend(image_observations)
            successful += 1
            update_status(
                status_data,
                image_path,
                "success",
                output_row_counts={
                    "observations": len(image_observations),
                    "plots": len(image_plots),
                    "tables": len(image_tables),
                },
            )
            print(f"SUCCESS: {image_path.name}", flush=True)
        except Exception as error:
            failed += 1
            append_failure(failure_rows, image_path, error)
            update_status(status_data, image_path, "failed", error_message=str(error))
            print(f"FAILED: {image_path.name} - {error}", flush=True)

        # Saving every image makes interruption recovery independent of batch size.
        save_tidy_outputs(
            args,
            observation_rows,
            plot_rows,
            table_rows,
            status_data,
            failure_rows,
        )

    # Create all state files even when every selected image was skipped.
    save_tidy_outputs(
        args,
        observation_rows,
        plot_rows,
        table_rows,
        status_data,
        failure_rows,
    )
    print_run_summary(args, successful, skipped, failed)


def run_table_mode(args: argparse.Namespace, images: list[Path]) -> None:
    """Run the older printed-table reconstruction workflow."""
    prompt = read_prompt(args.prompt_file)
    rows = (
        load_existing_rows(args.output, TABLE_OUTPUT_COLUMNS).to_dict("records")
        if args.resume
        else []
    )
    status_data = load_status_data(args.status_file, args.resume)
    failure_rows = (
        load_existing_rows(args.failed_output, FAILURE_COLUMNS).to_dict("records")
        if args.resume
        else []
    )
    successful = 0
    failed = 0
    skipped = record_command_skips(status_data, args)

    save_rows(rows, args.output, TABLE_OUTPUT_COLUMNS)
    save_status_data(status_data, args.status_file)
    save_rows(failure_rows, args.failed_output, FAILURE_COLUMNS)

    for image_path in images:
        position = args.image_positions[str(image_path)]
        reason = (
            skip_reason(status_record(status_data, image_path), args.retry_failed)
            if args.resume
            else ""
        )
        if reason:
            skipped += 1
            update_status(status_data, image_path, "skipped", reason=reason)
            save_rows(rows, args.output, TABLE_OUTPUT_COLUMNS)
            save_status_data(status_data, args.status_file)
            save_rows(failure_rows, args.failed_output, FAILURE_COLUMNS)
            print(f"SKIPPED: {image_path.name} - {reason}", flush=True)
            continue

        print(
            f"Processing {position}/{args.total_images_found}: {image_path.name}",
            flush=True,
        )
        try:
            image_rows = parse_table_image(
                image_path,
                args.model,
                prompt,
                args.max_image_side,
                args.num_predict,
            )
            rows.extend(image_rows)
            successful += 1
            update_status(
                status_data,
                image_path,
                "success",
                output_row_counts={"table_rows": len(image_rows)},
            )
            print(f"SUCCESS: {image_path.name}", flush=True)
        except Exception as error:
            failed += 1
            append_failure(failure_rows, image_path, error)
            update_status(status_data, image_path, "failed", error_message=str(error))
            print(f"FAILED: {image_path.name} - {error}", flush=True)

        save_rows(rows, args.output, TABLE_OUTPUT_COLUMNS)
        save_status_data(status_data, args.status_file)
        save_rows(failure_rows, args.failed_output, FAILURE_COLUMNS)

    save_rows(rows, args.output, TABLE_OUTPUT_COLUMNS)
    save_status_data(status_data, args.status_file)
    save_rows(failure_rows, args.failed_output, FAILURE_COLUMNS)
    print_run_summary(args, successful, skipped, failed)


def run_json_mode(args: argparse.Namespace, images: list[Path]) -> None:
    """Run the older specimen-label extraction workflow."""
    existing_frame = (
        load_existing_rows(args.output, JSON_OUTPUT_COLUMNS)
        if args.resume
        else pd.DataFrame(columns=JSON_OUTPUT_COLUMNS)
    )
    rows = existing_frame.to_dict("records")
    status_data = load_status_data(args.status_file, args.resume)
    failure_rows = (
        load_existing_rows(args.failed_output, FAILURE_COLUMNS).to_dict("records")
        if args.resume
        else []
    )
    successful = 0
    failed = 0

    if args.resume:
        for row in rows:
            if (
                row.get("parse_status") == "ok"
                and row.get("image_file")
                and row["image_file"] not in status_data["images"]
            ):
                update_status(status_data, Path(row["image_file"]), "success")

    skipped = record_command_skips(status_data, args)

    save_rows(rows, args.output, JSON_OUTPUT_COLUMNS)
    save_status_data(status_data, args.status_file)
    save_rows(failure_rows, args.failed_output, FAILURE_COLUMNS)

    for image_path in images:
        position = args.image_positions[str(image_path)]
        reason = (
            skip_reason(status_record(status_data, image_path), args.retry_failed)
            if args.resume
            else ""
        )
        if reason:
            skipped += 1
            update_status(status_data, image_path, "skipped", reason=reason)
            save_rows(rows, args.output, JSON_OUTPUT_COLUMNS)
            save_status_data(status_data, args.status_file)
            save_rows(failure_rows, args.failed_output, FAILURE_COLUMNS)
            print(f"SKIPPED: {image_path.name} - {reason}", flush=True)
            continue

        print(
            f"Processing {position}/{args.total_images_found}: {image_path.name}",
            flush=True,
        )
        try:
            image_name = str(image_path)
            rows = [row for row in rows if row.get("image_file") != image_name]
            image_row = parse_json_image(
                image_path,
                args.model,
                args.keep_raw,
                args.max_image_side,
                args.num_predict,
            )
            rows.append(image_row)
            successful += 1
            update_status(
                status_data,
                image_path,
                "success",
                output_row_counts={"json_rows": 1},
            )
            print(f"SUCCESS: {image_path.name}", flush=True)
        except Exception as error:
            failed += 1
            append_failure(failure_rows, image_path, error)
            update_status(status_data, image_path, "failed", error_message=str(error))
            print(f"FAILED: {image_path.name} - {error}", flush=True)

        save_rows(rows, args.output, JSON_OUTPUT_COLUMNS)
        save_status_data(status_data, args.status_file)
        save_rows(failure_rows, args.failed_output, FAILURE_COLUMNS)

    save_rows(rows, args.output, JSON_OUTPUT_COLUMNS)
    save_status_data(status_data, args.status_file)
    save_rows(failure_rows, args.failed_output, FAILURE_COLUMNS)
    print_run_summary(args, successful, skipped, failed)


def main() -> None:
    """Read command-line arguments, find images, and dispatch to one mode."""
    args = build_parser().parse_args()
    all_images = find_images(args.images_dir)
    args.total_images_found = len(all_images)
    args.image_positions = {
        str(image_path): index
        for index, image_path in enumerate(all_images, start=1)
    }
    args.explicitly_skipped = all_images[: args.skip] if args.skip else []
    images = all_images
    if args.skip:
        images = images[args.skip :]
    if args.limit is not None:
        images = images[: args.limit]

    if args.mode == "tidy":
        run_tidy_mode(args, images)
    elif args.mode == "table":
        run_table_mode(args, images)
    else:
        run_json_mode(args, images)


if __name__ == "__main__":
    main()
