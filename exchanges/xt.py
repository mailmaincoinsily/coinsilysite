import ccxt

def get_exchange_data():
    xt = ccxt.xt()
    try:
        xt_markets = xt.load_markets()
        xt_spot_markets = {symbol: market for symbol, market in xt_markets.items() if market['spot'] and market['active']}
        xt_tickers = xt.fetch_tickers(list(xt_spot_markets.keys()))
        return xt_tickers
    except Exception as e:
        return None, f"Error retrieving data from XT API: {e}"
