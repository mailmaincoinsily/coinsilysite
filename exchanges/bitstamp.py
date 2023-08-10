import ccxt

def get_exchange_data():
    bitstamp = ccxt.bitstamp()
    try:
        bitstamp_markets = bitstamp.load_markets()
        bitstamp_spot_markets = {symbol: market for symbol, market in bitstamp_markets.items() if market['spot'] and market['active']}
        bitstamp_tickers = bitstamp.fetch_tickers(list(bitstamp_spot_markets.keys()))
        return bitstamp_tickers
    except Exception as e:
        return None, f"Error retrieving data from Bitstamp API: {e}"
