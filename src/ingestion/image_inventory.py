from pathlib import Path
import re

import pandas as pd

from src.ingestion.image_loader import find_images


PROJECT_ROOT = Path(__file__).resolve().parents[2]
IMAGE_DIR = PROJECT_ROOT / "data" / "raw" / "images"
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw" / "metadata"
OUTPUT_FILE = OUTPUT_DIR / "image_inventory.csv"


def parse_image_metadata(image_path: Path) -> dict:
    """
    Extract metadata from a lettuce canopy image filename.

    Example:
    002_2022-02-21_biomass_measured.png
    """

    pattern = (
        r"(?P<image_number>\d+)_"
        r"(?P<date>\d{4}-\d{2}-\d{2})"
        r"(?P<biomass_measured>_biomass_measured)?"
    )

    match = re.fullmatch(pattern, image_path.stem)

    if not match:
        return {
            "filename": image_path.name,
            "image_number": None,
            "image_date": None,
            "biomass_measured_marker": None,
            "parse_status": "invalid_filename",
        }

    return {
        "filename": image_path.name,
        "image_number": int(match.group("image_number")),
        "image_date": pd.to_datetime(match.group("date")),
        "biomass_measured_marker": (
            match.group("biomass_measured") is not None
        ),
        "parse_status": "valid",
    }


def build_image_inventory() -> pd.DataFrame:
    images = find_images(str(IMAGE_DIR))

    records = [
        parse_image_metadata(image_path)
        for image_path in images
    ]

    return pd.DataFrame(records)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    inventory = build_image_inventory()
    inventory.to_csv(OUTPUT_FILE, index=False)

    print(f"Images discovered: {len(inventory)}")
    print(
        "Valid filenames:",
        (inventory["parse_status"] == "valid").sum(),
    )
    print(
        "Invalid filenames:",
        (inventory["parse_status"] != "valid").sum(),
    )
    print(
        "Images marked biomass measured:",
        inventory["biomass_measured_marker"].sum(),
    )
    print(f"Inventory saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()