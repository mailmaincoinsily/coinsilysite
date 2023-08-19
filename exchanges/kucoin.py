import ccxt
kukoin = ccxt.kucoin()
def get_exchange_data():
    try:
        kukoin_markets = kukoin.load_markets()
        kukoin_spot_markets = {symbol: market for symbol, market in kukoin_markets.items() if market['spot'] and market['active']}
        kukoin_tickers = kukoin.fetch_tickers(list(kukoin_spot_markets.keys()))
        return kukoin_tickers
    except Exception as e:
        return None, f"Error retrieving data from KuCoin API: {e}"
