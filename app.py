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

    # Get deposit and withdrawal information for currencies on Gate.io
    gateio_currencies = gateio.fetch_currencies()
    if gateio_currencies is None:
        error_message = "Failed to fetch currencies from Gate.io"
        logger.error(error_message)
        return render_template('error.html', error_message=error_message)

    # Filter currencies with deposit and withdrawal enabled on Gate.io
    gateio_currencies = {symbol: currency_info for symbol, currency_info in gateio_currencies.items() if 'depositEnable' in currency_info and 'withdrawEnable' in currency_info and currency_info['depositEnable'] and currency_info['withdrawEnable']}

    # Get deposit and withdrawal information for currencies on MEXC Global
    mexc_currencies = mexc_global.fetch_currencies()
    if mexc_currencies is None:
        error_message = "Failed to fetch currencies from MEXC Global"
        logger.error(error_message)
        return render_template('error.html', error_message=error_message)

    # Filter currencies with deposit and withdrawal enabled on MEXC Global
    mexc_currencies = {symbol: currency_info for symbol, currency_info in mexc_currencies.items() if 'depositEnable' in currency_info and 'withdrawEnable' in currency_info and currency_info['depositEnable'] and currency_info['withdrawEnable']}

    common_symbols = set(gateio_tickers.keys()) & set(mexc_tickers.keys()) & set(gateio_currencies.keys()) & set(mexc_currencies.keys())
    logger.info("Common symbols: %s", common_symbols)

    data = []
    for symbol in common_symbols:
        gateio_price = float(gateio_tickers[symbol]['last'])
        mexc_price = float(mexc_tickers[symbol]['last']) if mexc_tickers[symbol]['last'] is not None else 0.0
        arbitrage = round((mexc_price - gateio_price) / gateio_price * 100, 2)

        gateio_withdraw_fee = float(gateio_currencies[symbol]['withdrawFee'])
        mexc_withdraw_fee = float(mexc_currencies[symbol]['withdrawFee'])

        # Calculate profit after deducting withdrawal fees
        initial_investment = 100.0  # Your initial investment in USD or USDT
        profit_after_fees = initial_investment * (arbitrage / 100) - gateio_withdraw_fee - mexc_withdraw_fee

        if profit_after_fees > 0:
            gateio_trade_link = "https://www.gate.io/trade/{}".format(symbol.replace("/", "_"))
            mexc_trade_link = "https://www.mexc.com/exchange/{}".format(symbol.replace("/", "_"))

            data.append({
                'symbol': symbol,
                'gateio_price': gateio_price,
                'mexc_price': mexc_price,
                'arbitrage': arbitrage,
                'profit_after_fees': profit_after_fees,
                'gateio_trade_link': gateio_trade_link,
                'mexc_trade_link': mexc_trade_link
            })

    # Sort data by profit_after_fees value
    data.sort(key=lambda x: x['profit_after_fees'], reverse=True)

    # Count the number of positive and negative arbitrage opportunities
    positive_count = sum(1 for item in data if item['arbitrage'] > 0)
    negative_count = sum(1 for item in data if item['arbitrage'] < 0)

    logger.info("Data: %s", data)
    return render_template('index.html', data=data, positive_count=positive_count, negative_count=negative_count)

if __name__ == '__main__':
    app.run()
