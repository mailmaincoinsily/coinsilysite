import ccxt
import concurrent.futures
from flask import Flask, render_template

app = Flask(__name__)

# Initialize Binance API
binance = ccxt.binance({
    'rateLimit': 20,
    'enableRateLimit': True,
})

# Fetch all trading pairs
all_pairs = binance.load_markets()

# Currencies to consider
base_currencies = ['BTC', 'BNB', 'USDT']

# List to store arbitrage opportunities
arbitrage_opportunities = []

# Function to fetch ticker data for a pair
def fetch_ticker(pair):
    ticker = binance.fetch_ticker(pair)
    return ticker

# Loop through all pairs involving base currencies
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for base_currency in base_currencies:
        for pair1 in all_pairs:
            if base_currency in pair1:
                for pair2 in all_pairs:
                    if base_currency in pair2:
                        for pair3 in all_pairs:
                            if (
                                pair1 != pair2 and pair2 != pair3 and pair3 != pair1 and
                                base_currency in pair3
                            ):
                                futures.append(executor.submit(fetch_ticker, pair1))
                                futures.append(executor.submit(fetch_ticker, pair2))
                                futures.append(executor.submit(fetch_ticker, pair3))

    for future in concurrent.futures.as_completed(futures):
        ticker = future.result()
        # Perform calculations and store arbitrage opportunities

# Sort arbitrage opportunities by potential profit percentage
arbitrage_opportunities.sort(key=lambda x: x['potential_profit_percentage'], reverse=True)

@app.route('/')
def index():
    return render_template('index.html', arbitrage_opportunities=arbitrage_opportunities)

if __name__ == '__main__':
    app.run()
