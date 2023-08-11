import ccxt

# Initialize the Binance exchange
binance = ccxt.binance()

# Function to calculate triangular arbitrage opportunities
def calculate_triangular_arbitrage():
    print("Function is being executed")
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
                    print(f"Processing symbol: {symbol}")
                    print(f"Base Market: {base_market}")
                    print(f"Quote Market: {quote_market}")
                    
                    base_bid = base_market['bid']
                    quote_ask = quote_market['ask']
                    base_ask = base_market['ask']
                    
                    print(f"Base Bid: {base_bid}, Quote Ask: {quote_ask}, Base Ask: {base_ask}")
                    
                    arbitrage = (1 / base_bid) * quote_ask * base_ask - 1
                    print(f"Calculated Arbitrage: {arbitrage}")
                    
                    triangular_data.append({'symbol': symbol, 'profit': round(arbitrage * 100, 2)})
                    print(f"Added to triangular_data: {triangular_data[-1]}")
                    
        return triangular_data
    except Exception as e:
        print(f"Exception: {e}")
        return []

# You can add more functions related to triangular arbitrage here if needed

if __name__ == "__main__":
    print("Triangular Arbitrage Opportunities")
    results = calculate_triangular_arbitrage()
    print("Symbol\tProfit (%)")
    for result in results:
        print(f"{result['symbol']}\t{result['profit']}")

