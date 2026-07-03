import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5433"))
DB_NAME = os.getenv("DB_NAME", "crypto_dwh")
DB_USER = os.getenv("DB_USER", "crypto_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

BINANCE_API_URL = os.getenv("BINANCE_API_URL", "https://api.binance.com/api/v3/klines")
BINANCE_KLINES_LIMIT = int(os.getenv("BINANCE_KLINES_LIMIT", "100"))
BINANCE_REQUEST_TIMEOUT = int(os.getenv("BINANCE_REQUEST_TIMEOUT", "10"))

KLINE_SYMBOLS = [
    s.strip()
    for s in os.getenv("KLINE_SYMBOLS", "BTCUSDT,ETHUSDT,SOLUSDT").split(",")
    if s.strip()
]
KLINE_INTERVAL = os.getenv("KLINE_INTERVAL", "1h")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s | %(levelname)s | %(name)s | %(message)s")
LOG_DATE_FORMAT = os.getenv("LOG_DATE_FORMAT", "%Y-%m-%d %H:%M:%S")
