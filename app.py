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

# Loop through all pairs involving BTC
for btc_pair in all_pairs:
    if 'BTC' in btc_pair:
        for bnb_pair in all_pairs:
            if 'BNB' in bnb_pair:
                for usdt_pair in all_pairs:
                    if 'USDT' in usdt_pair:
                        ticker_btc = binance.fetch_ticker(btc_pair)
                        ticker_bnb = binance.fetch_ticker(bnb_pair)
                        ticker_usdt = binance.fetch_ticker(usdt_pair)

                        if (
                            ticker_btc['ask'] and ticker_btc['bid'] and
                            ticker_bnb['ask'] and ticker_bnb['bid'] and
                            ticker_usdt['ask'] and ticker_usdt['bid']
                        ):
                            rate_btc_to_bnb = ticker_btc['ask']
                            rate_bnb_to_usdt = ticker_bnb['bid']
                            rate_usdt_to_btc = 1 / ticker_usdt['ask']

                            profit = (
                                rate_btc_to_bnb * rate_bnb_to_usdt * rate_usdt_to_btc
                            ) - 1

                            if profit > 0:
                                arbitrage_opportunities.append({
                                    'pair_btc': btc_pair,
                                    'pair_bnb': bnb_pair,
                                    'pair_usdt': usdt_pair,
                                    'profit': profit,
                                    'rate_btc_to_bnb': rate_btc_to_bnb,
                                    'rate_bnb_to_usdt': rate_bnb_to_usdt,
                                    'rate_usdt_to_btc': rate_usdt_to_btc
                                })

# Sort arbitrage opportunities by profit
arbitrage_opportunities.sort(key=lambda x: x['profit'], reverse=True)

@app.route('/')
def index():
    return render_template('index.html', arbitrage_opportunities=arbitrage_opportunities)

if __name__ == '__main__':
    app.run()
