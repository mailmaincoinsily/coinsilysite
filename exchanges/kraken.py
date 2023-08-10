import ccxt

def get_exchange_data():
    kraken = ccxt.kraken()
    try:
        kraken_markets = kraken.load_markets()
        kraken_spot_markets = {symbol: market for symbol, market in kraken_markets.items() if market['spot'] and market['active']}
        kraken_tickers = kraken.fetch_tickers(list(kraken_spot_markets.keys()))
        return kraken_tickers
    except Exception as e:
        return None, f"Error retrieving data from Kraken API: {e}"
