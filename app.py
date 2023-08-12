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
currencies_to_consider = ['BTC', 'BNB', 'USDT']

# List to store arbitrage opportunities
arbitrage_opportunities = []

# Loop through all pairs
for pair in all_pairs:
    base_currency = pair.split('/')[0]
    quote_currency = pair.split('/')[1]

    if base_currency in currencies_to_consider and quote_currency in currencies_to_consider:
        ticker = binance.fetch_ticker(pair)

        if ticker['ask'] and ticker['bid']:
            rate_to_base = ticker['ask']
            rate_to_quote = 1 / ticker['bid']

            profit = (rate_to_quote / rate_to_base) - 1
            arbitrage_opportunities.append({
                'pair': pair,
                'profit': profit,
                'rate_to_base': rate_to_base,
                'rate_to_quote': rate_to_quote
            })

# Sort arbitrage opportunities by profit
arbitrage_opportunities.sort(key=lambda x: x['profit'], reverse=True)

@app.route('/')
def index():
    return render_template('index.html', arbitrage_opportunities=arbitrage_opportunities)

if __name__ == '__main__':
    app.run()
