import ccxt

def get_exchange_data():
    pionex = ccxt.pionex()
    try:
        pionex_markets = pionex.load_markets()
        pionex_spot_markets = {symbol: market for symbol, market in pionex_markets.items() if market['spot'] and market['active']}
        pionex_tickers = pionex.fetch_tickers(list(pionex_spot_markets.keys()))
        return pionex_tickers
    except Exception as e:
        return None, f"Error retrieving data from Pionex API: {e}"
