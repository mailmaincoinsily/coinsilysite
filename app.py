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
    coingecko_data = get_coingecko_price(exchange1, exchange2)  # Fetch Coingecko prices dynamically
    exchange1_coingecko_price = coingecko_data['exchange1_coingecko_price']
    exchange2_coingecko_price = coingecko_data['exchange2_coingecko_price']

    data, positive_count, negative_count = calculate_arbitrage(exchange1, exchange2)

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
        coingecko_price=exchange1_coingecko_price,  # Pass the Coingecko price to the template
    )

if __name__ == '__main__':
    app.run()
