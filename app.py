import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
import ccxt

app = Flask(__name__)
app.static_folder = 'static'
logger = logging.getLogger(__name__)

# Configure logger to write logs to a file
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def is_deposit_withdraw_enabled(exchange, symbol):
    currency_info = exchange.fetch_currency(symbol)
    return currency_info.get('active', False) and currency_info.get('deposit', False) and currency_info.get('withdraw', False)

def are_contacts_matching(exchange1, symbol1, exchange2, symbol2):
    currency_info1 = exchange1.fetch_currency(symbol1)
    currency_info2 = exchange2.fetch_currency(symbol2)
    return currency_info1.get('contract', '') == currency_info2.get('contract', '')

def are_networks_matching(exchange1, symbol1, exchange2, symbol2):
    currency_info1 = exchange1.fetch_currency(symbol1)
    currency_info2 = exchange2.fetch_currency(symbol2)
    return currency_info1.get('network', '') == currency_info2.get('network', '')

def get_arbitrage_opportunities(gateio_tickers, mexc_tickers):
    common_symbols = set(gateio_tickers.keys()) & set(mexc_tickers.keys())
    
    data = []
    for symbol in common_symbols:
        gateio_price = float(gateio_tickers[symbol]['last'])
        mexc_price = float(mexc_tickers[symbol]['last']) if mexc_tickers[symbol]['last'] is not None else 0.0
        arbitrage = round((mexc_price - gateio_price) / gateio_price * 100, 2)

        gateio_trade_link = "https://www.gate.io/trade/{}".format(symbol.replace("/", "_"))
        mexc_trade_link = "https://www.mexc.com/exchange/{}".format(symbol.replace("/", "_"))

        if (is_deposit_withdraw_enabled(gateio, symbol) and 
            is_deposit_withdraw_enabled(mexc_global, symbol) and 
            are_contacts_matching(gateio, symbol, mexc_global, symbol) and 
            are_networks_matching(gateio, symbol, mexc_global, symbol)):
            
            data.append({
                'symbol': symbol,
                'gateio_price': gateio_price,
                'mexc_price': mexc_price,
                'arbitrage': arbitrage,
                'gateio_trade_link': gateio_trade_link,
                'mexc_trade_link': mexc_trade_link
            })

    # Sort data by arbitrage value
    data.sort(key=lambda x: x['arbitrage'], reverse=True)

    return data

@app.route('/')
def index():
    gateio = ccxt.gateio()
    mexc_global = ccxt.mexc()

    try:
        gateio_markets = gateio.load_markets()
        gateio_spot_markets = {symbol: market for symbol, market in gateio_markets.items() if market['spot'] and market['active']}
        gateio_tickers = gateio.fetch_tickers(list(gateio_spot_markets.keys()))
        logger.info("Gateio data: %s", gateio_tickers)
    except Exception as e:
        error_message = "Error retrieving data from Gateio API: {}".format(e)
        logger.error(error_message)
        return render_template('error.html', error_message=error_message)

    try:
        mexc_markets = mexc_global.load_markets()
        mexc_spot_markets = {symbol: market for symbol, market in mexc_markets.items() if market['spot'] and market['active']}
        mexc_tickers = mexc_global.fetch_tickers(list(mexc_spot_markets.keys()))
        logger.info("MEXC Global data: %s", mexc_tickers)
    except Exception as e:
        error_message = "Error retrieving data from MEXC Global API: {}".format(e)
        logger.error(error_message)
        return render_template('error.html', error_message=error_message)

    data = get_arbitrage_opportunities(gateio_tickers, mexc_tickers)
    
    # Count the number of positive and negative arbitrage opportunities
    positive_count = sum(1 for item in data if item['arbitrage'] > 0)
    negative_count = sum(1 for item in data if item['arbitrage'] < 0)

    logger.info("Data: %s", data)
    return render_template('index.html', data=data, positive_count=positive_count, negative_count=negative_count)

if __name__ == '__main__':
    app.run()
