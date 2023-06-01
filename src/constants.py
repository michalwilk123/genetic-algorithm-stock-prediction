from pathlib import Path

"""
I assume that after 2 years people do not remember brands. No data to back that up
"""
CONSUMER_RECALL = 24
SHORT_CONSUMER_RECALL = 2

# paths to data
TRENDS_CSV_PATH = Path("data") / "trends.csv"
STOCK_TRENDS_CSV_PATH = Path("data") / "stock_trends.csv"
STOCK_PRICES_CSV_PATH = Path("data") / "stock_prices.csv"
