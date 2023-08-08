from flask import Flask, render_template, request
from engine import calculate_arbitrage, get_exchange_name
from coingecko import get_coingecko_price
from config import EXCHANGES

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', positive_count=0, negative_count=0, exchanges=EXCHANGES)

@app.route('/calculate', methods=['POST'])
def calculate():
    exchange1 = request.form['exchange1']
    exchange2 = request.form['exchange2']

    coingecko_price = get_coingecko_price(symbol=exchange1)  # Fetch Coingecko price using the symbol of the first exchange

    data = calculate_arbitrage(exchange1, exchange2, coingecko_price)

    positive_count = sum(1 for item in data if item['arbitrage'] > 0)
    negative_count = sum(1 for item in data if item['arbitrage'] < 0)

    exchange1_name = get_exchange_name(exchange1)
    exchange2_name = get_exchange_name(exchange2)

    return render_template(
        'index.html',
        positive_count=positive_count,
        negative_count=negative_count,
        data=data,
        exchange1_name=exchange1_name,
        exchange2_name=exchange2_name,
        exchanges=EXCHANGES,
        coingecko_price=coingecko_price
    )

if __name__ == '__main__':
    app.run()
