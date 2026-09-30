import numpy as np 
import pandas as pd
from pathlib import Path

folder_path = Path(__file__).resolve().parents[1] / "data" / "raw"

merge_file = []

for file_path in sorted(folder_path.iterdir()):
    if file_path.suffix.lower() == ".csv":
        merge_file.append(pd.read_csv(file_path, dtype=str, keep_default_na=False, ignore_index=True).assign(source_file=file_path.name))
    elif file_path.suffix.lower() == ".xlsx":
        merge_file.append(pd.read_excel(file_path, dtype=str, keep_default_na=False, ignore_index=True).assign(source_file=file_path.name))

full_table = pd.concat(merge_file)
