import ccxt

def get_crypto_com_data():
    crypto_com = ccxt.crypto_com()
    try:
        crypto_com_markets = crypto_com.load_markets()
        crypto_com_spot_markets = {symbol: market for symbol, market in crypto_com_markets.items() if market['spot'] and market['active']}
        crypto_com_tickers = crypto_com.fetch_tickers(list(crypto_com_spot_markets.keys()))
        return crypto_com_tickers
    except Exception as e:
        return None, f"Error retrieving data from Crypto.com API: {e}"
