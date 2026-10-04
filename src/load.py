import pandas as pd
from pathlib import Path

folder_path = Path(__file__).resolve().parents[1] / "data" / "raw"
output_path = Path(__file__).resolve().parents[1] / "data" / "processed" / "fuel_combined.parquet"

def load_raw(dir_path):
    merge_file = []

    for file_path in sorted(dir_path.iterdir()):
        if file_path.suffix.lower() == ".csv":
            merge_file.append(pd.read_csv(file_path, dtype=str, keep_default_na=False).assign(source_file=file_path.name))
        elif file_path.suffix.lower() == ".xlsx":
            merge_file.append(pd.read_excel(file_path, dtype=str, keep_default_na=False).assign(source_file=file_path.name))

    full_table = pd.concat(merge_file, ignore_index=True)

    return full_table


if __name__ == "__main__":
    table = load_raw(folder_path)
    table.to_parquet(path=output_path, index=False)
