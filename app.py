from flask import Flask, render_template
from gateio import get_gateio_data
from mexc import get_mexc_data
from binance import get_binance_data
from config import app, logger

@app.route('/')
def index():
    gateio_tickers = get_gateio_data()
    mexc_tickers = get_mexc_data()
    binance_tickers = get_binance_data()

    if gateio_tickers is None or mexc_tickers is None or binance_tickers is None:
        error_message = "Error retrieving data"
        logger.error(error_message)
        return render_template('error.html', error_message=error_message)

    common_symbols = set(gateio_tickers.keys()) & set(mexc_tickers.keys()) & set(binance_tickers.keys())

    data = []
    for symbol in common_symbols:
        gateio_price = float(gateio_tickers[symbol]['last'])
        mexc_price = float(mexc_tickers[symbol]['last']) if mexc_tickers[symbol]['last'] is not None else 0.0
        
        # Safely get the binance price using .get() method
        binance_price = float(binance_tickers[symbol].get('last_price', 0.0))

        arbitrage_gateio_mexc = round((mexc_price - gateio_price) / gateio_price * 100, 2)
        arbitrage_gateio_binance = round((binance_price - gateio_price) / gateio_price * 100, 2)

        gateio_trade_link = "https://www.gate.io/trade/{}".format(symbol.replace("/", "_"))
        mexc_trade_link = "https://www.mexc.com/exchange/{}".format(symbol.replace("/", "_"))
        binance_trade_link = "https://www.binance.com/en/trade/{}".format(symbol.replace("/", "_"))

        data.append({
            'symbol': symbol,
            'gateio_price': gateio_price,
            'mexc_price': mexc_price,
            'binance_price': binance_price,
            'arbitrage_gateio_mexc': arbitrage_gateio_mexc,
            'arbitrage_gateio_binance': arbitrage_gateio_binance,
            'gateio_trade_link': gateio_trade_link,
            'mexc_trade_link': mexc_trade_link,
            'binance_trade_link': binance_trade_link
        })

    # Sort data by arbitrage value for Gate.io and MEXC
    data.sort(key=lambda x: x['arbitrage_gateio_mexc'], reverse=True)

    # Count the number of positive and negative arbitrage opportunities
    positive_count_gateio_mexc = sum(1 for item in data if item['arbitrage_gateio_mexc'] > 0)
    negative_count_gateio_mexc = sum(1 for item in data if item['arbitrage_gateio_mexc'] < 0)

    return render_template('index.html', data=data, positive_count_gateio_mexc=positive_count_gateio_mexc, negative_count_gateio_mexc=negative_count_gateio_mexc)

if __name__ == '__main__':
    app.run()
