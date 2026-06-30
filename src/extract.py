import requests

BINANCE_URL = "https://api.binance.com/api/v3/klines"

def fetch_klines(symbol: str, interval: str = "1h", limit: int = 100):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(BINANCE_URL, params=params, timeout=10)
    response.raise_for_status()

    return response.json()

