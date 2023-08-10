import ccxt

def get_exchange_data():
    coinw = ccxt.coinw()
    try:
        coinw_markets = coinw.load_markets()
        coinw_spot_markets = {symbol: market for symbol, market in coinw_markets.items() if market['spot'] and market['active']}
        coinw_tickers = coinw.fetch_tickers(list(coinw_spot_markets.keys()))
        return coinw_tickers
    except Exception as e:
        return None, f"Error retrieving data from Coinw API: {e}"
