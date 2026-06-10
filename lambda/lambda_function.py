import json
import subprocess
import sys

subprocess.call([sys.executable, "-m", "pip", "install", "yfinance", "-q", 
                 "--target", "/tmp/packages"])
sys.path.insert(0, "/tmp/packages")

import boto3
import yfinance as yf
import pandas as pd
from io import StringIO

def lambda_handler(event, context):
    tickers = ["VTI", "BND", "VOO"]
    bucket = "mobley-etf-analysis"
    
    dfs = []
    for ticker in tickers:
        df = yf.download(ticker, start="2021-01-01", end="2024-12-31")
        df = df.reset_index()
        df["ticker"] = ticker
        df.columns = [c[0].lower().replace(" ", "_") if isinstance(c, tuple) 
                      else c.lower().replace(" ", "_") for c in df.columns]
        dfs.append(df)
    
    combined = pd.concat(dfs, ignore_index=True)
    
    csv_buffer = StringIO()
    combined.to_csv(csv_buffer, index=False)
    
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=bucket,
        Key="etf_prices.csv",
        Body=csv_buffer.getvalue()
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps(f"Uploaded {len(combined)} rows to S3")
    }