import ccxt

def get_indoex_data():
    indoex = ccxt.indoex()
    try:
        indoex_markets = indoex.load_markets()
        indoex_spot_markets = {symbol: market for symbol, market in indoex_markets.items() if market['spot'] and market['active']}
        indoex_tickers = indoex.fetch_tickers(list(indoex_spot_markets.keys()))
        return indoex_tickers
    except Exception as e:
        return None, f"Error retrieving data from Indoex API: {e}"
