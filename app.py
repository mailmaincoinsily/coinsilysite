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

# ... (Previous code)

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

    # Filter currencies with deposit and withdrawal enabled on both exchanges
    gateio_currencies = gateio.fetch_currencies()
    mexc_currencies = mexc_global.fetch_currencies()

    if gateio_currencies is None or mexc_currencies is None:
        error_message = "Failed to fetch currencies from one or both exchanges."
        logger.error(error_message)
        return render_template('error.html', error_message=error_message)

    gateio_currencies = {symbol: currency_info for symbol, currency_info in gateio_currencies.items() if 'depositEnable' in currency_info and 'withdrawEnable' in currency_info and currency_info['depositEnable'] and currency_info['withdrawEnable']}
    mexc_currencies = {symbol: currency_info for symbol, currency_info in mexc_currencies.items() if 'depositEnable' in currency_info and 'withdrawEnable' in currency_info and currency_info['depositEnable'] and currency_info['withdrawEnable']}

    # Filter currencies with the same contract address on both exchanges (for tokens)
    common_symbols = set([symbol for symbol in gateio_currencies.keys() if 'contract' in gateio_currencies[symbol] and 'contract' in mexc_currencies[symbol] and gateio_currencies[symbol]['contract'] == mexc_currencies[symbol]['contract']])

    # Filter currencies with the same network available for transactions on both exchanges (for tokens)
    common_symbols = common_symbols.intersection([symbol for symbol in common_symbols if 'networkList' in gateio_currencies[symbol] and 'networkList' in mexc_currencies[symbol] and any(network_info['network'] == 'common_network' for network_info in gateio_currencies[symbol]['networkList'] if 'common_network' in [network_info['network'] for network_info in mexc_currencies[symbol]['networkList']])])

    data = []
    for symbol in common_symbols:
        gateio_price = gateio_tickers.get(symbol, {}).get('last', 0.0)
        mexc_price = mexc_tickers.get(symbol, {}).get('last', 0.0)
        arbitrage = round((mexc_price - gateio_price) / gateio_price * 100, 2)

        # Deduct withdrawal fee from the arbitrage profit
        gateio_withdrawal_fee = gateio_currencies[symbol].get('withdrawFee', 0.0)
        mexc_withdrawal_fee = mexc_currencies[symbol].get('withdrawFee', 0.0)

        profit_after_fees = arbitrage - (gateio_withdrawal_fee + mexc_withdrawal_fee)

        if profit_after_fees > 0 and profit_after_fees > 100:
            gateio_trade_link = "https://www.gate.io/trade/{}".format(symbol.replace("/", "_"))
            mexc_trade_link = "https://www.mexc.com/exchange/{}".format(symbol.replace("/", "_"))

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

    # Count the number of positive and negative arbitrage opportunities
    positive_count = sum(1 for item in data if item['arbitrage'] > 0)
    negative_count = sum(1 for item in data if item['arbitrage'] < 0)

    logger.info("Data: %s", data)
    return render_template('index.html', data=data, positive_count=positive_count, negative_count=negative_count)

if __name__ == '__main__':
    app.run()
