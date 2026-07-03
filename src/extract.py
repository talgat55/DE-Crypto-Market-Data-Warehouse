import requests

from config import BINANCE_API_URL, BINANCE_KLINES_LIMIT, BINANCE_REQUEST_TIMEOUT, KLINE_INTERVAL


def fetch_klines(
    symbol: str,
    interval: str = KLINE_INTERVAL,
    limit: int = BINANCE_KLINES_LIMIT,
    start_time_ms: int | None = None,
):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
    }

    if start_time_ms is not None:
        params["startTime"] = start_time_ms

    response = requests.get(BINANCE_API_URL, params=params, timeout=BINANCE_REQUEST_TIMEOUT)
    response.raise_for_status()

    return response.json()

