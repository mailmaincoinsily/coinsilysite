import ccxt

def get_probit_global_data():
    probit_global = ccxt.probit_global()
    try:
        probit_global_markets = probit_global.load_markets()
        probit_global_spot_markets = {symbol: market for symbol, market in probit_global_markets.items() if market['spot'] and market['active']}
        probit_global_tickers = probit_global.fetch_tickers(list(probit_global_spot_markets.keys()))
        return probit_global_tickers
    except Exception as e:
        return None, f"Error retrieving data from Probit Global API: {e}"
