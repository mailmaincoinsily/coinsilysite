import ccxt

def get_whitebit_data():
    whitebit = ccxt.whitebit()
    try:
        whitebit_markets = whitebit.load_markets()
        whitebit_spot_markets = {symbol: market for symbol, market in whitebit_markets.items() if market['spot'] and market['active']}
        whitebit_tickers = whitebit.fetch_tickers(list(whitebit_spot_markets.keys()))
        return whitebit_tickers
    except Exception as e:
        return None, f"Error retrieving data from Whitebit API: {e}"
