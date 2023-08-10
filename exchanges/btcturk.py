import ccxt

def get_exchange_data():
    btcturk = ccxt.btcturk()
    try:
        btcturk_markets = btcturk.load_markets()
        btcturk_spot_markets = {symbol: market for symbol, market in btcturk_markets.items() if market['spot'] and market['active']}
        btcturk_tickers = btcturk.fetch_tickers(list(btcturk_spot_markets.keys()))
        return btcturk_tickers
    except Exception as e:
        return None, f"Error retrieving data from BTCTurk API: {e}"
