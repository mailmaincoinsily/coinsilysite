import ccxt
import asyncio
from flask import Flask, render_template

app = Flask(__name__)

# Initialize Binance API
binance = ccxt.binance({
    'rateLimit': 20,
    'enableRateLimit': True,
})

# Fetch all trading pairs
all_pairs = binance.load_markets()

# List to store arbitrage opportunities
arbitrage_opportunities = []

async def process_pair(pair1, pair2, pair3):
    ticker1 = await binance.fetch_ticker(pair1)
    ticker2 = await binance.fetch_ticker(pair2)
    ticker3 = await binance.fetch_ticker(pair3)

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

# Loop through pairs involving USDT
usdt_pairs = [pair for pair in all_pairs if 'USDT' in pair]
loop = asyncio.get_event_loop()

for pair1 in usdt_pairs:
    for pair2 in usdt_pairs:
        for pair3 in usdt_pairs:
            if pair1 != pair2 and pair2 != pair3 and pair3 != pair1:
                loop.run_until_complete(process_pair(pair1, pair2, pair3))

# Sort arbitrage opportunities by potential profit percentage
arbitrage_opportunities.sort(key=lambda x: x['potential_profit_percentage'], reverse=True)

@app.route('/')
def index():
    return render_template('index.html', arbitrage_opportunities=arbitrage_opportunities)

if __name__ == '__main__':
    app.run()
