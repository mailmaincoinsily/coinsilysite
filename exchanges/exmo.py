import ccxt

def get_exchange_data():
    exmo = ccxt.exmo()
    try:
        exmo_markets = exmo.load_markets()
        exmo_spot_markets = {symbol: market for symbol, market in exmo_markets.items() if market['spot'] and market['active']}
        exmo_tickers = exmo.fetch_tickers(list(exmo_spot_markets.keys()))
        return exmo_tickers
    except Exception as e:
        return None, f"Error retrieving data from Exmo API: {e}"
