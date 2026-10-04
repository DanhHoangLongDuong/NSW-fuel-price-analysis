import pandas as pd
from pathlib import Path

input_path = Path(__file__).resolve().parents[1] / "data" / "processed" / "fuel_combined.parquet"
output_path = Path(__file__).resolve().parents[1] / "data" / "processed" / "fuel_clean.parquet"

fuelCode_dict = {"P98": "Premium Unleaded Petrol 98",
                 "U91": "Unleaded 91",
                 "E10": "Ethanol 10%",
                 "P95": "Premium Unleaded Petrol 95",
                 "PDL": "Premium Diesel",
                 "DL": "Diesel",
                 "LPG": "Liquefied Petroleum Gas",
                 "E85": "Ethanol fuel blend, 85%",
                 "B20": "B20 Biodiesel Blend"}

def clean(table):
    # trim columns
    for col in table.columns:
        table[col] = table[col].str.strip()
    
    # drop duplicates
    table.drop_duplicates(inplace=True)
    # change price datatype
    table["Price"] = table["Price"].astype("float64")
    # fix date formats
    oct_dates = (pd.to_datetime(table
                                .loc[(table["source_file"] == "price_history_checks_oct2025.csv"), "PriceUpdatedDate"],
                                      format="%d/%m/%Y %H:%M"))
    iso_dates = (pd.to_datetime(table
                                .loc[(table["source_file"] != "price_history_checks_oct2025.csv"),"PriceUpdatedDate"], 
                                      format="%Y-%m-%d %H:%M:%S"))
    
    table["PriceUpdatedDate"] = pd.concat([oct_dates, iso_dates]).sort_index()
    # drop price error
    table = table.loc[(table["Price"] >= 100) | (table["FuelCode"] == "LPG")]
    # add state, brand_group, fuel_name
    table = table.assign(state=(table["Address"]
                                .str.upper()
                                .str.findall(r"\b(NSW|ACT|VIC|QLD|SA|WA|TAS|NT|"
                                            r"NEW\s+SOUTH\s+WALES|AUSTRALIAN\s+CAPITAL\s+TERRITORY|VICTORIA|QUEENSLAND|SOUTH\s+AUSTRALIA|WESTERN\s+AUSTRALIA|TASMANIA|NORTHERN\s+TERRITORY)\b"
                                            ).str[-1].replace({"NEW SOUTH WALES": "NSW", 
                                                               "AUSTRALIAN CAPITAL TERRITORY": "ACT",
                                                               "VICTORIA":"VIC",
                                                               "QUEENSLAND": "QLD",
                                                               "SOUTH AUSTRALIA": "SA",
                                                               "WESTERN AUSTRALIA": "WA",
                                                               "TASMANIA": "TAS",
                                                               "NORTHERN TERRITORY": "NT"})),
                         brand_group=table["Brand"].replace({
                                                                "Ampol Foodary": "Ampol",
                                                                "Ampol Breeze": "Ampol",
                                                                "EBM Ampol": "Ampol", 
                                                                "Caltex": "Ampol",
                                                                "Coles Express": "Reddy Express",
                                                                "BOOST FUEL BERMAGUI": "Boost Fuel",
                                                                "24Xpress logo": "24Xpress",
                                                                "Mobil 1 Carlingford Car Care": "Mobil"
                                                                }))
    brand_counts = table["brand_group"].value_counts()
    brand_counts = brand_counts[brand_counts < 2000].index
    table["brand_group"] = table["brand_group"].mask((table["brand_group"].isin(brand_counts)), other="Other")
    
    table["fuel_name"] = table["FuelCode"].map(fuelCode_dict)
    
    return table


if __name__ == "__main__":
    df = pd.read_parquet(input_path)
    table = clean(df)
    table.to_parquet(path=output_path, index=False)
    print(len(table))
    print(table.isna().sum())