import ccxt
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

# Loop through all pairs
for pair in all_pairs:
    base_currency = pair.split('/')[0]
    quote_currency = pair.split('/')[1]

    if base_currency in base_currencies and quote_currency != base_currency:
        ticker = binance.fetch_ticker(pair)

        if ticker['ask'] and ticker['bid']:
            rate_base_to_quote = ticker['ask']
            rate_quote_to_base = 1 / ticker['bid']

            profit_percentage = (rate_base_to_quote * rate_quote_to_base) * 100 - 100

            if profit_percentage > 0:
                arbitrage_opportunities.append({
                    'pair': pair,
                    'profit_percentage': profit_percentage
                })

# Sort arbitrage opportunities by profit percentage
arbitrage_opportunities.sort(key=lambda x: x['profit_percentage'], reverse=True)

@app.route('/')
def index():
    return render_template('index.html', arbitrage_opportunities=arbitrage_opportunities)

if __name__ == '__main__':
    app.run()
