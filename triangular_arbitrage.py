import ccxt
import time

# Initialize the Binance exchange
binance = ccxt.binance({
    'rateLimit': 20,  # Set a reasonable rate limit (requests per second)
})

# Function to calculate triangular arbitrage opportunities
def calculate_triangular_arbitrage():
    try:
        binance_markets = binance.load_markets()
        binance_spot_markets = {symbol: market for symbol, market in binance_markets.items() if market['spot'] and market['active']}

        triangular_data = []

        for base_symbol in binance_spot_markets:
            for quote_symbol in binance_spot_markets:
                if base_symbol != quote_symbol:
                    intermediate_symbol = None

                    # Find the intermediate symbol
                    for symbol in binance_spot_markets:
                        if symbol != base_symbol and symbol != quote_symbol:
                            intermediate_symbol = symbol
                            break

                    if intermediate_symbol:
                        ticker_data = binance.fetch_tickers([base_symbol, intermediate_symbol, quote_symbol])
                        base_to_intermediate = ticker_data[base_symbol]['ask']
                        intermediate_to_quote = ticker_data[intermediate_symbol]['ask']
                        quote_to_base = ticker_data[quote_symbol]['bid']

                        arbitrage_ratio = (1 / base_to_intermediate) * intermediate_to_quote * quote_to_base - 1

                        if arbitrage_ratio > 0.001:  # Considering fees
                            triangular_data.append({
                                'base_symbol': base_symbol,
                                'intermediate_symbol': intermediate_symbol,
                                'quote_symbol': quote_symbol,
                                'arbitrage_ratio': round(arbitrage_ratio * 100, 2)
                            })

                        time.sleep(1)  # Add a delay to avoid exceeding rate limits

        return triangular_data
    except Exception as e:
        print("Exception:", e)
        return []

# Call the function to calculate triangular arbitrage opportunities
triangular_arbitrage_data = calculate_triangular_arbitrage()

# Print the calculated triangular arbitrage opportunities
for data in triangular_arbitrage_data:
    print("Opportunity:")
    print("Base Symbol:", data['base_symbol'])
    print("Intermediate Symbol:", data['intermediate_symbol'])
    print("Quote Symbol:", data['quote_symbol'])
    print("Arbitrage Ratio:", data['arbitrage_ratio'], "%")
    print()
