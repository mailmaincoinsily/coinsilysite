import ccxt
bitflyer = ccxt.bitflyer()
def get_exchange_data():
    try:
        bitflyer_markets = bitflyer.load_markets()
        bitflyer_spot_markets = {symbol: market for symbol, market in bitflyer_markets.items() if market['spot'] and market['active']}
        bitflyer_tickers = bitflyer.fetch_tickers(list(bitflyer_spot_markets.keys()))
        return bitflyer_tickers
    except Exception as e:
        return None, f"Error retrieving data from Bitflyer API: {e}"
