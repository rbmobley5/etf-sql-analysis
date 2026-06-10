# Vanguard ETF Performance Analysis (2021–2024)

A end-to-end data pipeline analyzing three Vanguard ETFs — VTI (total market), VOO 
(S&P 500), and BND (bonds) — across a four-year period that included aggressive Fed 
rate hikes, a broad market selloff, and a strong equity recovery.

The pipeline runs locally (SQLite + R) and in the cloud (AWS Lambda + S3 + Athena).

## Key Findings

- **2022 was the worst year across all three funds.** VTI fell 20%, VOO fell 18.7%, 
  and BND fell 12.5% — driven by the fastest Fed rate hiking cycle since the 1980s.
- **Equities recovered fully; bonds did not.** VOO and VTI posted 26%+ returns in both 
  2023 and 2024, more than erasing 2022 losses. BND returned to positive growth but 
  had not recovered lost principal by end of 2024.
- **VOO and VTI are highly correlated.** The S&P 500 and total US market track closely 
  because large-cap stocks dominate the total market index.
- **BND volatility persisted longer than equity volatility.** Bond prices remain 
  sensitive to rate expectations even after equity markets stabilized.

## Figures

![Indexed ETF Performance](etf-sql-R/figures/indexed_performance.png)
![Rolling 30-Day Volatility](etf-sql-R/figures/rolling_volatility.png)
![Annual Returns by ETF](etf-sql-R/figures/annual_returns.png)

## Architecture

### Local Pipeline
- **Ingestion:** Python + yfinance + SQLAlchemy → SQLite database
- **Analysis:** SQL queries (aggregation, CTEs, window functions)
- **Visualization:** R + ggplot2 + zoo

### Cloud Pipeline (AWS)
- **Ingestion:** AWS Lambda (Python) pulls fresh data from Yahoo Finance
- **Storage:** AWS S3 (CSV)
- **Query:** AWS Athena (serverless Presto SQL) — same analytical queries, cloud scale

## Methods

- **Data:** Daily OHLCV pricing data for VTI, VOO, and BND — 2021 to 2024 
  (~1,004 trading days per ticker, 3,012 rows total)
- **SQL:** Aggregation, window functions (LAG, FIRST_VALUE, LAST_VALUE, rolling AVG), 
  and CTEs to compute summary statistics, annual returns, rolling averages, and 
  daily return series
- **Cloud:** Lambda function automates data refresh and uploads to S3; 
  Athena queries CSV directly with Presto SQL — no server required

## Reproducing This Analysis

### Local
1. Install dependencies: `pip install yfinance pandas sqlalchemy`
2. Run `python ingest.py` to build the SQLite database
3. Run `python queries.py` to execute SQL queries
4. Open `etf-sql-R` as an R project and run `scripts/00_setup.R` then `scripts/01_plots.R`

### Cloud
1. Deploy `lambda/lambda_function.py` to AWS Lambda (Python 3.12)
2. Add the AWS SDK for Pandas layer
3. Grant Lambda S3 write permissions via IAM
4. Point Athena at your S3 bucket and run queries from `sql/`

## Repository Structure

```
etf-sql-analysis/
├── ingest.py
├── export.py
├── queries.py
├── check.py
├── etf_analysis.db
├── etf_prices.csv
├── sql/
│   ├── 01_aggregation.sql
│   ├── 02_annual_returns.sql
│   ├── 03_rolling_avg.sql
│   └── 04_volatility.sql
├── lambda/
│   └── lambda_function.py
└── etf-sql-R/
    ├── scripts/
    │   ├── 00_setup.R
    │   └── 01_plots.R
    └── figures/
        ├── indexed_performance.png
        ├── rolling_volatility.png
        └── annual_returns.png
```