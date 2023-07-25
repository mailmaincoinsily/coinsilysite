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

    common_symbols = set(gateio_tickers.keys()) & set(mexc_tickers.keys())
    logger.info("Common symbols: %s", common_symbols)

    data = []
    for symbol in common_symbols:
        gateio_price = float(gateio_tickers[symbol]['last'])
        mexc_price = float(mexc_tickers[symbol]['last']) if mexc_tickers[symbol]['last'] is not None else 0.0
        arbitrage = round((mexc_price - gateio_price) / gateio_price * 100, 2)

        gateio_withdrawal_fee = float(gateio.currencies[symbol]['withdrawFee'])
        mexc_withdrawal_fee = float(mexc_global.currencies[symbol]['withdrawFee'])

        symbol_profit = arbitrage - gateio_withdrawal_fee - mexc_withdrawal_fee
        symbol['profit'] = symbol_profit

        # Filter out arbitrage opportunities that are not profitable
        if symbol_profit > 0:
            data.append(symbol)

    # Sort data by profit value
    data.sort(key=lambda x: x['profit'], reverse=True)

    # Count the number of profitable arbitrage opportunities
    profit_count = len(data)

    logger.info("Data: %s", data)
    return render_template('index.html', data=data, profit_count=profit_count)

if __name__ == '__main__':
    app.run()
