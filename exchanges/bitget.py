import ccxt
bitget = ccxt.bitget()
def get_bitget_data():
    try:
        bitget_markets = bitget.load_markets()
        bitget_spot_markets = {symbol: market for symbol, market in bitget_markets.items() if market['spot'] and market['active']}
        bitget_tickers = bitget.fetch_tickers(list(bitget_spot_markets.keys()))
        return bitget_tickers
    except Exception as e:
        return None, f"Error retrieving data from Bitget API: {e}"
