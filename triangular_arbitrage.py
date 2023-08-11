import ccxt
import concurrent.futures

# Initialize the Binance exchange
binance = ccxt.binance()
binance_markets = binance.load_markets()
binance_spot_markets = {symbol: market for symbol, market in binance_markets.items() if market['spot'] and market['active']}

# Function to fetch ticker data
def fetch_ticker_data(symbol):
    return symbol, binance.fetch_ticker(symbol)

# Function to calculate arbitrage ratio
def calculate_arbitrage_ratio(base_data, intermediate_data, quote_data):
    base_to_intermediate = base_data['ask']
    intermediate_to_quote = intermediate_data['ask']
    quote_to_base = quote_data['bid']
    return (1 / base_to_intermediate) * intermediate_to_quote * quote_to_base - 1

# Function to calculate triangular arbitrage opportunities
def calculate_triangular_arbitrage():
    triangular_data = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        ticker_data = executor.map(fetch_ticker_data, binance_spot_markets.keys())
    
    for base_symbol, base_data in ticker_data:
        for intermediate_symbol, intermediate_data in ticker_data:
            if base_symbol != intermediate_symbol:
                for quote_symbol, quote_data in ticker_data:
                    if quote_symbol != base_symbol and quote_symbol != intermediate_symbol:
                        arbitrage_ratio = calculate_arbitrage_ratio(base_data, intermediate_data, quote_data)
                        if arbitrage_ratio > 0.001:  # Considering fees
                            triangular_data.append({
                                'base_symbol': base_symbol,
                                'intermediate_symbol': intermediate_symbol,
                                'quote_symbol': quote_symbol,
                                'arbitrage_ratio': round(arbitrage_ratio * 100, 2)
                            })
    
    return triangular_data

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
