import ccxt

def get_huobi_data():
    huobi = ccxt.huobipro()
    try:
        huobi_markets = huobi.load_markets()
        huobi_spot_markets = {symbol: market for symbol, market in huobi_markets.items() if market['spot'] and market['active']}
        huobi_tickers = huobi.fetch_tickers(list(huobi_spot_markets.keys()))
        return huobi_tickers
    except Exception as e:
        return None, f"Error retrieving data from Huobi API: {e}"
