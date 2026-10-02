
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BIOMASS_FILE = PROJECT_ROOT / "data/raw/biomass/Biomass.xlsx"
ENVIRONMENT_FILE = (
    PROJECT_ROOT / "data/raw/environment/Environment_Solution.xlsx"
)


def inspect_biomass():
    print("\n========== BIOMASS QUALITY CHECK ==========")

    excel = pd.ExcelFile(BIOMASS_FILE)

    for sheet in excel.sheet_names:
        df = pd.read_excel(BIOMASS_FILE, sheet_name=sheet)

        print(f"\nSheet: {sheet}")
        print("Last 3 rows:")
        print(df.tail(3).to_string(index=False))

        print("\nDate range:")
        print(df["Date"].min(), "to", df["Date"].max())

        print("\nCompletely empty rows:", df.isnull().all(axis=1).sum())


def inspect_environment():
    print("\n========== ENVIRONMENT QUALITY CHECK ==========")

    df = pd.read_excel(ENVIRONMENT_FILE)

    measurement_columns = [
        col for col in df.columns if col != "Timestamp"
    ]

    all_measurements_missing = df[measurement_columns].isnull().all(axis=1)

    print("\nTimestamp range:")
    print(df["Timestamp"].min(), "to", df["Timestamp"].max())

    print("\nTotal records:", len(df))
    print("Completely missing measurement records:",
          all_measurements_missing.sum())

    print("\nTimestamps of missing measurement records:")
    print(df.loc[all_measurements_missing, "Timestamp"].to_string(index=False))

    print("\nDuplicate timestamps:", df["Timestamp"].duplicated().sum())

    print("\nTime difference between consecutive records:")
    print(df["Timestamp"].diff().value_counts().head(10).to_string())


def main():
    inspect_biomass()
    inspect_environment()


if __name__ == "__main__":
    main()