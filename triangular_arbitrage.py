import ccxt

# Initialize the Binance exchange
binance = ccxt.binance()

# Function to calculate triangular arbitrage opportunities
def calculate_triangular_arbitrage():
    print("Function is being executed")
    try:
        binance_markets = binance.load_markets()
        print("Loaded Binance markets:", binance_markets)
        
        binance_spot_markets = {symbol: market for symbol, market in binance_markets.items() if market['spot'] and market['active']}
        print("Binance spot markets:", binance_spot_markets)

        triangular_data = []

        for symbol in binance_spot_markets:
            print("Processing symbol:", symbol)
            base, _, quote = symbol.split('/')
            print("Base:", base)
            print("Quote:", quote)
            reverse_symbol = f"{quote}/{base}"
            print("Reverse symbol:", reverse_symbol)
            
            if reverse_symbol in binance_spot_markets:
                print("Reverse symbol found:", reverse_symbol)
                base_market = binance_spot_markets[symbol]
                quote_market = binance_spot_markets[reverse_symbol]
                
                print("Base market:", base_market)
                print("Quote market:", quote_market)
                
                if quote_market['quote'] == quote:
                    print("Quote matching:", quote)
                    arbitrage = (1 / base_market['bid']) * quote_market['ask'] * base_market['ask'] - 1
                    print("Arbitrage:", arbitrage)
                    triangular_data.append({'symbol': symbol, 'profit': round(arbitrage * 100, 2)})
        print("Triangular data:", triangular_data)
        return triangular_data
    except Exception as e:
        print("Exception:", e)
        return []

# You can add more functions related to triangular arbitrage here if needed
