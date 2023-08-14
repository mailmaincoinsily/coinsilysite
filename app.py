from flask import Flask, render_template, request, flash
from engine import calculate_arbitrage, get_exchange_name
from config import EXCHANGES  # Import the EXCHANGES dictionary
from flask_login import LoginManager, login_required, current_user
from auth import auth_bp
from init import login_manager

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secret key

app.register_blueprint(auth_bp)

login_manager.init_app(app)

# ... Your existing code ...

@app.route('/')
@login_required
def index():
    return render_template('index.html', positive_count=0, negative_count=0, exchanges=EXCHANGES)

@app.route('/calculate', methods=['POST'])
@login_required
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

if __name__ == '__main__':
    app.run()
