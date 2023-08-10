import ccxt
bingx = ccxt.bingx()
def get_exchange_data():
    try:
        bingx_markets = bingx.load_markets()
        bingx_spot_markets = {symbol: market for symbol, market in bingx_markets.items() if market['spot'] and market['active']}
        bingx_tickers = bingx.fetch_tickers(list(bingx_spot_markets.keys()))
        return bingx_tickers
    except Exception as e:
        return None, f"Error retrieving data from BingX API: {e}"
