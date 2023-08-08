from flask import Flask, render_template, request
from engine import calculate_arbitrage

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', positive_count=0, negative_count=0)

@app.route('/calculate', methods=['POST'])
def calculate():
    exchange1 = request.form['exchange1']
    exchange2 = request.form['exchange2']

    data = calculate_arbitrage(exchange1, exchange2)
    
    # Count the number of positive and negative arbitrage opportunities
    positive_count = sum(1 for item in data if item['arbitrage'] > 0)
    negative_count = sum(1 for item in data if item['arbitrage'] < 0)
    
    return render_template('index.html', positive_count=positive_count, negative_count=negative_count, data=data, exchange1=exchange1, exchange2=exchange2)

if __name__ == '__main__':
    app.run()
