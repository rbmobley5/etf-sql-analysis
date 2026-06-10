import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///etf_analysis.db")

# Query 1 — Basic aggregation
q1 = """
SELECT ticker,
       ROUND(AVG(close), 2) AS avg_close,
       ROUND(MAX(close), 2) AS peak_close,
       ROUND(MIN(close), 2) AS trough_close
FROM prices
GROUP BY ticker
ORDER BY avg_close DESC
"""

# Query 2 — Annual returns
q2 = """
WITH yearly AS (
  SELECT ticker,
         STRFTIME('%Y', date) AS year,
         FIRST_VALUE(close) OVER (
           PARTITION BY ticker, STRFTIME('%Y', date)
           ORDER BY date
         ) AS open_price,
         LAST_VALUE(close) OVER (
           PARTITION BY ticker, STRFTIME('%Y', date)
           ORDER BY date
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
         ) AS close_price
  FROM prices
)
SELECT ticker, year,
       ROUND((close_price - open_price) / open_price * 100, 2) AS annual_return_pct
FROM yearly
GROUP BY ticker, year
ORDER BY ticker, year
"""

# Query 3 — 30-day rolling average
q3 = """
SELECT date, ticker, ROUND(close, 2) AS close,
       ROUND(AVG(close) OVER (
         PARTITION BY ticker
         ORDER BY date
         ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
       ), 2) AS rolling_30d_avg
FROM prices
ORDER BY ticker, date
"""

# Query 4 — Daily returns + rolling mean
q4 = """
WITH returns AS (
  SELECT date, ticker, close,
         (close - LAG(close) OVER (PARTITION BY ticker ORDER BY date))
           / LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS daily_return
  FROM prices
)
SELECT date, ticker,
       ROUND(daily_return * 100, 4) AS daily_return_pct,
       ROUND(AVG(daily_return) OVER (
         PARTITION BY ticker
         ORDER BY date
         ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
       ) * 100, 4) AS rolling_30d_mean_return
FROM returns
WHERE daily_return IS NOT NULL
ORDER BY ticker, date
"""

print("=== Q1: Summary Statistics ===")
print(pd.read_sql(q1, engine))

print("\n=== Q2: Annual Returns ===")
print(pd.read_sql(q2, engine))

print("\n=== Q3: 30-Day Rolling Average (first 5 rows per ticker) ===")
df3 = pd.read_sql(q3, engine)
print(df3.groupby("ticker").head(5))

print("\n=== Q4: Daily Returns (first 5 rows per ticker) ===")
df4 = pd.read_sql(q4, engine)
print(df4.groupby("ticker").head(5))