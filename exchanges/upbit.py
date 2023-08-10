import ccxt

def get_exchange_data():
    upbit = ccxt.upbit()
    try:
        upbit_markets = upbit.load_markets()
        upbit_spot_markets = {symbol: market for symbol, market in upbit_markets.items() if market['spot'] and market['active']}
        upbit_tickers = upbit.fetch_tickers(list(upbit_spot_markets.keys()))
        return upbit_tickers
    except Exception as e:
        return None, f"Error retrieving data from Upbit API: {e}"
