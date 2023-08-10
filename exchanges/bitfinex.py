import ccxt

def get_exchange_data():
    bitfinex = ccxt.bitfinex()
    try:
        bitfinex_markets = bitfinex.load_markets()
        bitfinex_spot_markets = {symbol: market for symbol, market in bitfinex_markets.items() if market['spot'] and market['active']}
        bitfinex_tickers = bitfinex.fetch_tickers(list(bitfinex_spot_markets.keys()))
        return bitfinex_tickers
    except Exception as e:
        return None, f"Error retrieving data from Bitfinex API: {e}"
