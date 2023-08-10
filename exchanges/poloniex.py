import ccxt

def get_poloniex_data():
    poloniex = ccxt.poloniex()
    try:
        poloniex_markets = poloniex.load_markets()
        poloniex_spot_markets = {symbol: market for symbol, market in poloniex_markets.items() if market['spot'] and market['active']}
        poloniex_tickers = poloniex.fetch_tickers(list(poloniex_spot_markets.keys()))
        return poloniex_tickers
    except Exception as e:
        return None, f"Error retrieving data from Poloniex API: {e}"
