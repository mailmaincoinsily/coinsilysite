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
    coingecko_price_input = request.form.get('coingecko_price')

    try:
        coingecko_price = float(coingecko_price_input)
    except ValueError:
        coingecko_price = 0.0

    data = calculate_arbitrage(exchange1, exchange2, coingecko_price)

    positive_count = sum(1 for item in data if item['arbitrage'] > 0)
    negative_count = sum(1 for item in data if item['arbitrage'] < 0)

    exchange1_name = get_exchange_name(exchange1)
    exchange2_name = get_exchange_name(exchange2)

    coingecko_data = get_coingecko_price()  # Call the coingecko function

    return render_template(
        'index.html',
        positive_count=positive_count,
        negative_count=negative_count,
        data=data,
        exchange1_name=exchange1_name,
        exchange2_name=exchange2_name,
        exchanges=EXCHANGES,
        coingecko_price=coingecko_price,
        coingecko_data=coingecko_data
    )

if __name__ == '__main__':
    app.run()
