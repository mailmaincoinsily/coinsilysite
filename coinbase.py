import ccxt

def get_coinbase_data():
    coinbase = ccxt.coinbase()
    try:
        coinbase_markets = coinbase.load_markets()
        coinbase_spot_markets = {symbol: market for symbol, market in coinbase_markets.items() if market['spot'] and market['active']}
        coinbase_tickers = coinbase.fetch_tickers(list(coinbase_spot_markets.keys()))
        return coinbase_tickers
    except Exception as e:
        return None, f"Error retrieving data from Coinbase API: {e}"
