# NSW Fuel Price Analysis

Python pipeline that cleans 1.26M NSW FuelCheck price records (Aug 2025 – Aug 2026)
and analyses when and where a vehicle fleet should refuel to minimise fuel cost.

## Business question
A Sydney-based fleet operator (140 vans and light trucks) asked:
**"Are we filling up at the wrong places, on the wrong days?"**

## Key findings
- **Day of week:** In Sydney, diesel is cheapest on **Sunday/Monday** and most expensive on
  **Tuesday** – a gap of **2.2 c/L**. For a 140-vehicle fleet refuelling weekly (80 L tank),
  timing fill-ups saves roughly **$12,800 per year**.
- **Brand:** For diesel, **Pearl Energy, Metro Fuel and ASTRON** are the cheapest brands;
  **7-Eleven, Inland Petroleum and Reddy Express** the most expensive.
  The cheapest vs. most expensive brand gap is **32.8 c/L**.\
  *(Brand averages are not adjusted for location or time period.)*
- **Region:** Regional NSW diesel is on average **1.5 c/L higher** than Sydney.

## Data
- Source: [NSW FuelCheck price history – Data.NSW](https://data.nsw.gov.au/data/dataset/fuel-check)
- 13 monthly files (10 XLSX, 3 CSV), Aug 2025 – Aug 2026, 1,258,332 rows
- Each row is a **price change** at a station (not a sale)
- Data files are not included in this repo. Download them into `data/raw/`.

## How to run
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/pipeline.py
```
Then open the notebooks in `notebooks/`.

## Project structure
```
data/raw/          raw downloaded files (not in repo)
data/processed/    fuel_combined.parquet, fuel_clean.parquet (generated)
notebooks/
  01_load_and_profile.ipynb   data profiling: completeness, consistency, validity, duplicates
  02_analysis.ipynb           answers the business question
src/
  load.py       reads and combines the 13 raw files
  clean.py      applies all cleaning rules
  pipeline.py   runs load → clean in one command
```

## Data quality issues found and fixed
| Issue | Rows | Fix |
|---|---|---|
| Two date formats; Oct 2025 file is day-first with no seconds | 69,132 | Parsed with an explicit format per source |
| Impossible prices (< 100 c/L, excluding LPG) | 147 | Removed |
| Exact duplicate rows | 15 | Removed |
| Brand name variants (e.g. Caltex → Ampol, Coles Express → Reddy Express) | – | `brand_group` column; brands < 2,000 rows grouped as "Other" (22 groups) |
| State written differently in addresses ("NEW SOUTH WALES", "NSW AUSTRALIA") | 835 | State extracted from address with regex |
| Cross-border postcodes (2620, 3644, 4383) | 992 | State taken from address, not postcode |
| ACT stations in the NSW dataset | 30,963 | Labelled `ACT`; excluded from NSW analysis |

Final clean dataset: **1,258,170 rows**, 0 missing values.

## Limitations
- Prices appear capped at 300 c/L.
- Averages are based on price updates, not volume sold.
- Station identity is not fully resolved (2,605 names vs 2,519 addresses, e.g. rebrands).

## Future work
- Load into PostgreSQL as a star schema
- Power BI dashboard
- Resolve station identity (rebrands, address variants)

## Tools
Python 3.14, pandas, pyarrow, matplotlib, Jupyter