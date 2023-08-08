from flask import Flask, render_template, request
from engine import calculate_arbitrage, get_exchange_name
from config import EXCHANGES

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', positive_count=0, negative_count=0, exchanges=EXCHANGES)

@app.route('/calculate', methods=['POST'])
def calculate():
    exchange1 = request.form['exchange1']
    exchange2 = request.form['exchange2']
    liquidity_amount_str = request.form['liquidityAmount']
    
    # Check if liquidityAmount field is not empty and is a valid numeric value
    if liquidity_amount_str and liquidity_amount_str.replace('.', '', 1).isdigit():
        liquidity_amount = float(liquidity_amount_str)
        data = calculate_arbitrage(exchange1, exchange2)
        positive_count = 0
        negative_count = 0
        valid_arbitrages = []
        
        for item in data:
            if item['arbitrage'] > 0 and item['arbitrage'] <= liquidity_amount:
                valid_arbitrages.append(item)
                positive_count += 1
            elif item['arbitrage'] < 0:
                valid_arbitrages.append(item)
                negative_count += 1
        
        exchange1_name = get_exchange_name(exchange1)
        exchange2_name = get_exchange_name(exchange2)
        
        return render_template(
            'index.html',
            positive_count=positive_count,
            negative_count=negative_count,
            data=valid_arbitrages,
            exchange1_name=exchange1_name,
            exchange2_name=exchange2_name,
            exchanges=EXCHANGES,
            liquidity_amount=liquidity_amount
        )
    else:
        return render_template(
            'index.html',
            error_message='Please enter a valid liquidity amount.',
            exchanges=EXCHANGES
        )

if __name__ == '__main__':
    app.run()
