import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

tickers = ["VTI", "BND", "VOO"]
engine = create_engine("sqlite:///etf_analysis.db")

for ticker in tickers:
    df = yf.download(ticker, start="2021-01-01", end="2024-12-31")
    df = df.reset_index()
    df.columns = [c[0].lower().replace(" ", "_") if isinstance(c, tuple) else c.lower().replace(" ", "_") for c in df.columns]
    df["ticker"] = ticker
    df.to_sql("prices", engine, if_exists="append", index=False)
    print(f"{ticker} done — {len(df)} rows inserted")

print("\nAll done!")
total = pd.read_sql("SELECT COUNT(*) as n FROM prices", engine).iloc[0,0]
print(f"Total rows in database: {total}")