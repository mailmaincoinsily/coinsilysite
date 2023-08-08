from flask import Flask, render_template, request
from engine import calculate_arbitrage, get_exchange_name
from config import EXCHANGES
from coingecko import get_coingecko_price

app = Flask(__name__)

# Function to import exchange module dynamically
def get_exchange_module(module_name):
    return __import__(module_name)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', exchanges=EXCHANGES)

@app.route('/calculate', methods=['POST'])
def calculate():
    exchange1 = request.form['exchange1']
    exchange2 = request.form['exchange2']

    # Fetch ticker data for exchange1 and exchange2
    exchange1_config = EXCHANGES.get(exchange1)
    exchange2_config = EXCHANGES.get(exchange2)

    if not exchange1_config or not exchange2_config:
        return "Invalid exchanges selected"

    exchange1_module = get_exchange_module(exchange1_config['module'])
    exchange2_module = get_exchange_module(exchange2_config['module'])

    exchange1_tickers = exchange1_module.get_exchange_data()  # Fetch ticker data for exchange1
    exchange2_tickers = exchange2_module.get_exchange_data()  # Fetch ticker data for exchange2

    # Calculate arbitrage opportunities and related data
    data, positive_count, negative_count = calculate_arbitrage(
        exchange1_tickers,
        exchange2_tickers
    )

    exchange1_name = get_exchange_name(exchange1)
    exchange2_name = get_exchange_name(exchange2)

    # Fetch price from CoinGecko
    coingecko_price = get_coingecko_price()

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
    app.run(debug=True)
