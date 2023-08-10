import ccxt

def get_exchange_data():
    bitforex = ccxt.bitforex()
    try:
        bitforex_markets = bitforex.load_markets()
        bitforex_spot_markets = {symbol: market for symbol, market in bitforex_markets.items() if market['spot'] and market['active']}
        bitforex_tickers = bitforex.fetch_tickers(list(bitforex_spot_markets.keys()))
        return bitforex_tickers
    except Exception as e:
        return None, f"Error retrieving data from Bitforex API: {e}"
