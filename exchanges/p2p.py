import ccxt

def get_exchange_data():
    p2p = ccxt.p2p()
    try:
        p2p_markets = p2p.load_markets()
        p2p_spot_markets = {symbol: market for symbol, market in p2p_markets.items() if market['spot'] and market['active']}
        p2p_tickers = p2p.fetch_tickers(list(p2p_spot_markets.keys()))
        return p2p_tickers
    except Exception as e:
        return None, f"Error retrieving data from P2P API: {e}"
