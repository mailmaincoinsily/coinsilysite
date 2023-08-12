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

# Loop through all pairs involving base currencies
for base_currency in base_currencies:
    for pair1 in all_pairs:
        if base_currency in pair1:
            for pair2 in all_pairs:
                if base_currency in pair2:
                    for pair3 in all_pairs:
                        if pair1 != pair2 and pair2 != pair3 and pair3 != pair1 and base_currency in pair3:
                            ticker1 = binance.fetch_ticker(pair1)
                            ticker2 = binance.fetch_ticker(pair2)
                            ticker3 = binance.fetch_ticker(pair3)

                            if (
                                ticker1['ask'] and ticker1['bid'] and
                                ticker2['ask'] and ticker2['bid'] and
                                ticker3['ask'] and ticker3['bid']
                            ):
                                rate1_to_2 = ticker1['ask']
                                rate2_to_3 = 1 / ticker2['bid']
                                rate3_to_1 = 1 / ticker3['bid']

                                potential_profit_percentage = (
                                    rate1_to_2 * rate2_to_3 * rate3_to_1
                                ) * 100 - 100

                                if potential_profit_percentage > 0:
                                    arbitrage_opportunities.append({
                                        'pair1': pair1,
                                        'pair2': pair2,
                                        'pair3': pair3,
                                        'potential_profit_percentage': potential_profit_percentage
                                    })

# Sort arbitrage opportunities by potential profit percentage
arbitrage_opportunities.sort(key=lambda x: x['potential_profit_percentage'], reverse=True)

@app.route('/')
def index():
    return render_template('index.html', arbitrage_opportunities=arbitrage_opportunities)

if __name__ == '__main__':
    app.run()
