from flask import Flask
from binance.client import Client
from binance.websockets import BinanceSocketManager
import os

app = Flask(__name__)

@app.route('/')
def index():
    opportunities = find_triangular_arbitrage_opportunities()
    
    if opportunities:
        result = "<h1>Triangular Arbitrage Opportunities:</h1>"
        for opportunity in opportunities:
            result += f"<p>Opportunity: {opportunity['pair1']} -> {opportunity['pair2']} ({opportunity['arbitrage_percentage']:.2f}%)</p>"
        return result
    else:
        return "No arbitrage opportunities found."

def find_triangular_arbitrage_opportunities():
    client = Client(api_key=os.environ.get("BINANCE_API_KEY"), api_secret=os.environ.get("BINANCE_API_SECRET"))
    bm = BinanceSocketManager(client)
    
    markets = client.get_exchange_info()['symbols']
    usdt_markets = [market['symbol'] for market in markets if market['symbol'].endswith('USDT')]
    
    profitable_trades = []
    
    def process_message(msg):
        base_currency, _ = msg['symbol'].split('@')
        
        for intermediate_currency in usdt_markets:
            if intermediate_currency.endswith('USDT') or intermediate_currency == msg['symbol']:
                continue
            
            try:
                bid_price = float(msg['bidPrice'])
                ask_price = float(client.get_avg_price(symbol=intermediate_currency)['price'])
                
                arbitrage_percentage = ((ask_price / bid_price) - 1) * 100
                
                if arbitrage_percentage > 0:
                    profitable_trades.append({
                        'pair1': msg['symbol'],
                        'pair2': intermediate_currency,
                        'arbitrage_percentage': arbitrage_percentage
                    })
            except (ccxt.BaseError, IndexError):
                pass
    
    # Subscribe to live bid price updates for all trading pairs
    conn_key = bm.start_trade_socket(callback=process_message)
    bm.start()
    
    import time
    time.sleep(10)  # Let it run for 10 seconds to collect data
    
    bm.stop_socket(conn_key)
    bm.close()
    
    profitable_trades.sort(key=lambda trade: trade['arbitrage_percentage'], reverse=True)
    
    return profitable_trades

if __name__ == "__main__":
    app.run(debug=True)
