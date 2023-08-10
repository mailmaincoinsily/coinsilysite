import ccxt

coinbase_pro = ccxt.coinbasepro()

def get_exchange_data():
    try:
        coinbase_pro_markets = coinbase_pro.load_markets()
        coinbase_pro_spot_markets = {symbol: market for symbol, market in coinbase_pro_markets.items() if market['spot'] and market['active']}
        coinbase_pro_tickers = coinbase_pro.fetch_tickers(list(coinbase_pro_spot_markets.keys()))
        return coinbase_pro_tickers
    except Exception as e:
        return None, f"Error retrieving data from Coinbase Pro API: {e}"
