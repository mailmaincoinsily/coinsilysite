import ccxt

def get_exchange_data():
    lbank = ccxt.lbank()
    try:
        lbank_markets = lbank.load_markets()
        lbank_spot_markets = {symbol: market for symbol, market in lbank_markets.items() if market['spot'] and market['active']}
        lbank_tickers = lbank.fetch_tickers(list(lbank_spot_markets.keys()))
        return lbank_tickers
    except Exception as e:
        return None, f"Error retrieving data from LBank API: {e}"
