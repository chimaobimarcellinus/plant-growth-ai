
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BIOMASS_FILE = PROJECT_ROOT / "data/raw/biomass/Biomass.xlsx"
ENVIRONMENT_FILE = (
    PROJECT_ROOT / "data/raw/environment/Environment_Solution.xlsx"
)


def inspect_workbook(file_path: Path):
    print(f"\n{'=' * 60}")
    print(f"WORKBOOK: {file_path.name}")
    print(f"{'=' * 60}")

    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    excel_file = pd.ExcelFile(file_path)

    print(f"Sheets: {excel_file.sheet_names}")

    for sheet in excel_file.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet)

        print(f"\n--- Sheet: {sheet} ---")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")
        print("\nColumn names:")
        print(df.columns.tolist())

        print("\nFirst 5 rows:")
        print(df.head().to_string(index=False))

        print("\nMissing values per column:")
        print(df.isnull().sum().to_string())


def main():
    inspect_workbook(BIOMASS_FILE)
    inspect_workbook(ENVIRONMENT_FILE)


if __name__ == "__main__":
    main()