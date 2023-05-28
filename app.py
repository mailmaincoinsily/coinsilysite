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
    uniswap = ccxt.uniswapv2()
    pancakeswap = ccxt.pancakeswapv2()

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

    try:
        uniswap_markets = uniswap.load_markets()
        uniswap_tickers = uniswap.fetch_tickers()
        logger.info("Uniswap V2 data: %s", uniswap_tickers)
    except Exception as e:
        error_message = "Error retrieving data from Uniswap V2 API: {}".format(e)
        logger.error(error_message)
        return render_template('error.html', error_message=error_message)

    try:
        pancakeswap_markets = pancakeswap.load_markets()
        pancakeswap_tickers = pancakeswap.fetch_tickers()
        logger.info("PancakeSwap V2 data: %s", pancakeswap_tickers)
    except Exception as e:
        error_message = "Error retrieving data from PancakeSwap V2 API: {}".format(e)
        logger.error(error_message)
        return render_template('error.html', error_message=error_message)

    common_symbols = (
        set(gateio_tickers.keys())
        & set(mexc_tickers.keys())
        & set(uniswap_tickers.keys())
        & set(pancakeswap_tickers.keys())
    )
    logger.info("Common symbols: %s", common_symbols)

    data = []
    for symbol in common_symbols:
        gateio_price = float(gateio_tickers[symbol]['last'])
        mexc_price = float(mexc_tickers[symbol]['last']) if mexc_tickers[symbol]['last'] is not None else 0.0
        uniswap_price = float(uniswap_tickers[symbol]['last']) if symbol in uniswap_tickers else 0.0
        pancakeswap_price = float(pancakeswap_tickers[symbol]['last']) if symbol in pancakeswap_tickers else 0.0

        gateio_trade_link = "https://www.gate.io/trade/{}".format(symbol.replace("/", "_"))
        mexc_trade_link = "https://www.mexc.com/exchange/{}".format(symbol.replace("/", "_"))
        uniswap_trade_link = "https://app.uniswap.org/#/swap?inputCurrency={}&outputCurrency={}".format(symbol.split("/")[0], symbol.split("/")[1])
        pancakeswap_trade_link = "https://exchange.pancakeswap.finance/#/swap?inputCurrency={}&outputCurrency={}".format(symbol.split("/")[0], symbol.split("/")[1])

        arbitrage_uniswap = round((uniswap_price - gateio_price) / gateio_price * 100, 2)
        arbitrage_pancakeswap = round((pancakeswap_price - gateio_price) / gateio_price * 100, 2)

        data.append({
            'symbol': symbol,
            'gateio_price': gateio_price,
            'mexc_price': mexc_price,
            'uniswap_price': uniswap_price,
            'pancakeswap_price': pancakeswap_price,
            'arbitrage_uniswap': arbitrage_uniswap,
            'arbitrage_pancakeswap': arbitrage_pancakeswap,
            'gateio_trade_link': gateio_trade_link,
            'mexc_trade_link': mexc_trade_link,
            'uniswap_trade_link': uniswap_trade_link,
            'pancakeswap_trade_link': pancakeswap_trade_link
        })

    # Sort data by Uniswap arbitrage value
    data.sort(key=lambda x: x['arbitrage_uniswap'], reverse=True)

    # Count the number of positive and negative arbitrage opportunities for Uniswap
    positive_uniswap_count = sum(1 for item in data if item['arbitrage_uniswap'] > 0)
    negative_uniswap_count = sum(1 for item in data if item['arbitrage_uniswap'] < 0)

    # Sort data by PancakeSwap arbitrage value
    data.sort(key=lambda x: x['arbitrage_pancakeswap'], reverse=True)

    # Count the number of positive and negative arbitrage opportunities for PancakeSwap
    positive_pancakeswap_count = sum(1 for item in data if item['arbitrage_pancakeswap'] > 0)
    negative_pancakeswap_count = sum(1 for item in data if item['arbitrage_pancakeswap'] < 0)

    logger.info("Data: %s", data)
    return render_template(
        'index.html',
        data=data,
        positive_uniswap_count=positive_uniswap_count,
        negative_uniswap_count=negative_uniswap_count,
        positive_pancakeswap_count=positive_pancakeswap_count,
        negative_pancakeswap_count=negative_pancakeswap_count
    )

if __name__ == '__main__':
    app.run()
