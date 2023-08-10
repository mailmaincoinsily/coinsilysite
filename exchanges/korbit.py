import ccxt

def get_exchange_data():
    korbit = ccxt.korbit()
    try:
        korbit_markets = korbit.load_markets()
        korbit_spot_markets = {symbol: market for symbol, market in korbit_markets.items() if market['spot'] and market['active']}
        korbit_tickers = korbit.fetch_tickers(list(korbit_spot_markets.keys()))
        return korbit_tickers
    except Exception as e:
        return None, f"Error retrieving data from Korbit API: {e}"
