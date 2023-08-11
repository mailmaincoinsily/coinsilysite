from flask import Flask, render_template, request
from engine import calculate_arbitrage, get_exchange_name
from config import EXCHANGES  # Import the EXCHANGES dictionary
from triangular_arbitrage import calculate_triangular_arbitrage  # Import the new function

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', positive_count=0, negative_count=0, exchanges=EXCHANGES)

@app.route('/calculate', methods=['POST'])
def calculate():
    exchange1 = request.form['exchange1']
    exchange2 = request.form['exchange2']

    data = calculate_arbitrage(exchange1, exchange2)
    
    # Count the number of positive and negative arbitrage opportunities
    positive_count = sum(1 for item in data if item['arbitrage'] > 0)
    negative_count = sum(1 for item in data if item['arbitrage'] < 0)
    
    # Get the exchange names for display
    exchange1_name = get_exchange_name(exchange1)
    exchange2_name = get_exchange_name(exchange2)
    
    return render_template(
        'index.html',
        positive_count=positive_count,
        negative_count=negative_count,
        data=data,
        exchange1_name=exchange1_name,
        exchange2_name=exchange2_name,
        exchanges=EXCHANGES
    )

# New route for triangular arbitrage
@app.route('/triangular')
def triangular():
    triangular_data = calculate_triangular_arbitrage()
    print(triangular_data)
    return render_template('triangular.html', triangular_data=triangular_data)

if __name__ == '__main__':
    app.run()
