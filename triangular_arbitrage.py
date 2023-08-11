import ccxt

# Initialize the Binance exchange
binance = ccxt.binance()

# Function to calculate triangular arbitrage opportunities
def calculate_triangular_arbitrage():
    try:
        binance_markets = binance.load_markets()
        binance_spot_markets = {symbol: market for symbol, market in binance_markets.items() if market['spot'] and market['active']}

        triangular_data = []

        for symbol in binance_spot_markets:
            base, _, quote = symbol.split('/')
            reverse_symbol = f"{quote}/{base}"
            
            if reverse_symbol in binance_spot_markets:
                base_market = binance_spot_markets[symbol]
                quote_market = binance_spot_markets[reverse_symbol]
                
                if quote_market['quote'] == quote:
                    arbitrage = (1 / base_market['bid']) * quote_market['ask'] * base_market['ask'] - 1
                    triangular_data.append({'symbol': symbol, 'profit': round(arbitrage * 100, 2)})

        return triangular_data
    except Exception as e:
        return []

# You can add more functions related to triangular arbitrage here if needed
