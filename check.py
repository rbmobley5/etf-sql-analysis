import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///etf_analysis.db")

print(pd.read_sql("SELECT ticker, COUNT(*) as rows FROM prices GROUP BY ticker", engine))
print(pd.read_sql("PRAGMA table_info(prices)", engine))