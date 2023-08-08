import ccxt

bybit = ccxt.bybit()

def get_exchange_data():
    try:
        bybit_markets = bybit.load_markets()
        bybit_spot_markets = {symbol: market for symbol, market in bybit_markets.items() if market['spot'] and market['active']}
        bybit_tickers = bybit.fetch_tickers(list(bybit_spot_markets.keys()))
        return bybit_tickers
    except Exception as e:
        return None, "Error retrieving data from Bybit API: {}".format(e)
