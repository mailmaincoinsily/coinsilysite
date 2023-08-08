from flask import Flask, render_template, request
from engine import calculate_arbitrage

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    exchange1 = request.form['exchange1']
    exchange2 = request.form['exchange2']

    data = calculate_arbitrage(exchange1, exchange2)
    
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()
