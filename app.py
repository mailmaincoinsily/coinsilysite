from flask import Flask, render_template
import ccxt

app = Flask(__name__)

@app.route('/')
def index():
    gateio = ccxt.gateio()
    mexc_global = ccxt.mexc()

    try:
        gateio_markets = gateio.load_markets()
        gateio_spot_markets = {symbol: market for symbol, market in gateio_markets.items() if market['spot'] and market['active']}
        gateio_tickers = gateio.fetch_tickers(list(gateio_spot_markets.keys()))
        print("Gateio data:", gateio_tickers)
    except Exception as e:
        error_message = "Error retrieving data from Gateio API: {}".format(e)
        print(error_message)
        return render_template('error.html', error_message=error_message)

    try:
        mexc_markets = mexc_global.load_markets()
        mexc_spot_markets = {symbol: market for symbol, market in mexc_markets.items() if market['spot'] and market['active']}
        mexc_tickers = mexc_global.fetch_tickers(list(mexc_spot_markets.keys()))
        print("MEXC Global data:", mexc_tickers)
    except Exception as e:
        error_message = "Error retrieving data from MEXC Global API: {}".format(e)
        print(error_message)
        return render_template('error.html', error_message=error_message)

    common_symbols = set(gateio_tickers.keys()) & set(mexc_tickers.keys())
    print("Common symbols:", common_symbols)

    data = []
    for symbol in common_symbols:
        gateio_price = float(gateio_tickers[symbol]['last'])
        mexc_price = float(mexc_tickers[symbol]['last'])
        arbitrage = round((mexc_price - gateio_price) / gateio_price * 100, 2)

        # Get trade links
        gateio_trade_link = gateio.market(gateio_tickers[symbol]['symbol'])['info']['url']
        mexc_trade_link = mexc_global.market(mexc_tickers[symbol]['symbol'])['info']['url']

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

    print("Data:", data)
    return render_template('index.html', data=data, positive_count=positive_count, negative_count=negative_count)

if __name__ == '__main__':
    app.run()
