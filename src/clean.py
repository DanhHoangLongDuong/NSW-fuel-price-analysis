import pandas as pd
from pathlib import Path

input_path = Path(__file__).resolve().parents[1] / "data" / "processed" / "fuel_combined.parquet"
output_path = Path(__file__).resolve().parents[1] / "data" / "processed" / "fuel_clean.parquet"

def clean(table):
    for col in table.columns:
        table[col] = table[col].str.strip()
    
    table.drop_duplicates(inplace=True)
    table["Price"] = table["Price"].astype("float64")

    oct_dates = (pd.to_datetime(table
                                .loc[(table["source_file"] == "price_history_checks_oct2025.csv"), "PriceUpdatedDate"],
                                      format="%d/%m/%Y %H:%M"))
    iso_dates = (pd.to_datetime(table
                                .loc[(table["source_file"] != "price_history_checks_oct2025.csv"),"PriceUpdatedDate"], 
                                      format="%Y-%m-%d %H:%M:%S"))
    
    table["PriceUpdatedDate"] = pd.concat([oct_dates, iso_dates]).sort_index()
    return table


if __name__ == "__main__":
    df = pd.read_parquet(input_path)
    table = clean(df)
    table.to_parquet(path=output_path, index=False)
    print(len(table))