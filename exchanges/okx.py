import ccxt

def get_exchange_data():
    okx = ccxt.okex()
    try:
        okx_markets = okx.load_markets()
        okx_spot_markets = {symbol: market for symbol, market in okx_markets.items() if market['spot'] and market['active']}
        okx_tickers = okx.fetch_tickers(list(okx_spot_markets.keys()))
        return okx_tickers
    except Exception as e:
        return None, f"Error retrieving data from OKEx API: {e}"
