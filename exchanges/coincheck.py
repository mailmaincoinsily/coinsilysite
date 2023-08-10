import ccxt

def get_exchange_data():
    coincheck = ccxt.coincheck()
    try:
        coincheck_markets = coincheck.load_markets()
        coincheck_spot_markets = {symbol: market for symbol, market in coincheck_markets.items() if market['spot'] and market['active']}
        coincheck_tickers = coincheck.fetch_tickers(list(coincheck_spot_markets.keys()))
        return coincheck_tickers
    except Exception as e:
        return None, f"Error retrieving data from Coincheck API: {e}"
