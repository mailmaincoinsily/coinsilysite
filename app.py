from flask import Flask, render_template, request
from engine import calculate_arbitrage
from coingecko import get_coingecko_price  # Import the coingecko function here

app = Flask(__name__)

EXCHANGES = ['Exchange 1', 'Exchange 2', 'Exchange 3']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        exchange1_name = request.form.get('exchange1')
        exchange2_name = request.form.get('exchange2')
        coingecko_price = float(request.form.get('coingecko_price'))

        positive_count, negative_count, data = calculate_arbitrage(exchange1_name, exchange2_name, coingecko_price)
        coingecko_data = coingecko_function()  # Call the coingecko function

        return render_template(
            'index.html',
            positive_count=positive_count,
            negative_count=negative_count,
            data=data,
            exchange1_name=exchange1_name,
            exchange2_name=exchange2_name,
            exchanges=EXCHANGES,
            coingecko_price=coingecko_price,
            coingecko_data=coingecko_data  # Pass the coingecko data to the template
        )

    return render_template('index.html', exchanges=EXCHANGES)

if __name__ == '__main__':
    app.run(debug=True)
