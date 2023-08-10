import ccxt

def get_hitbtc_data():
    hitbtc = ccxt.hitbtc()
    try:
        hitbtc_markets = hitbtc.load_markets()
        hitbtc_spot_markets = {symbol: market for symbol, market in hitbtc_markets.items() if market['spot'] and market['active']}
        hitbtc_tickers = hitbtc.fetch_tickers(list(hitbtc_spot_markets.keys()))
        return hitbtc_tickers
    except Exception as e:
        return None, f"Error retrieving data from HitBTC API: {e}"
