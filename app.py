from flask import Flask, render_template, request
from engine import calculate_arbitrage
from coingecko import get_coingecko_price

app = Flask(__name__)

# Import the EXCHANGES dictionary from the config module
from config import EXCHANGES

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        exchange1_name = request.form.get('exchange1')
        exchange2_name = request.form.get('exchange2')
        coingecko_price = float(request.form.get('coingecko_price'))

        positive_count, negative_count, data = calculate_arbitrage(exchange1_name, exchange2_name, coingecko_price)
        coingecko_data = get_coingecko_price()  # Call the coingecko function

        return render_template(
            'index.html',
            positive_count=positive_count,
            negative_count=negative_count,
            data=data,
            exchange1_name=exchange1_name,
            exchange2_name=exchange2_name,
            exchanges=EXCHANGES,  # Pass the correct EXCHANGES dictionary here
            coingecko_price=coingecko_price,
            coingecko_data=coingecko_data  # Pass the coingecko data to the template
        )

    return render_template('index.html', exchanges=EXCHANGES)  # Pass the correct EXCHANGES dictionary here

if __name__ == '__main__':
    app.run(debug=True)
