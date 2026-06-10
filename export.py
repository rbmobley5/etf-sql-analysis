import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///etf_analysis.db")
df = pd.read_sql("SELECT * FROM prices", engine)
df.to_csv("etf_prices.csv", index=False)
print(f"Exported {len(df)} rows to etf_prices.csv")