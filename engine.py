from gateio import get_gateio_data
from mexc import get_mexc_data
# Import other exchange modules if needed

def calculate_arbitrage(exchange1, exchange2):
    # Retrieve ticker data for the selected exchanges
    if exchange1 == 'gateio':
        exchange1_tickers = get_gateio_data()
    elif exchange1 == 'mexc':
        exchange1_tickers = get_mexc_data()
    # Add more cases for other exchanges if needed

    if exchange2 == 'gateio':
        exchange2_tickers = get_gateio_data()
    elif exchange2 == 'mexc':
        exchange2_tickers = get_mexc_data()
    # Add more cases for other exchanges if needed

    common_symbols = set(exchange1_tickers.keys()) & set(exchange2_tickers.keys())

    data = []
    for symbol in common_symbols:
        exchange1_price = float(exchange1_tickers[symbol]['last'])
        exchange2_price = float(exchange2_tickers[symbol]['last']) if exchange2_tickers[symbol]['last'] is not None else 0.0
        arbitrage = round((exchange2_price - exchange1_price) / exchange1_price * 100, 2)

        exchange1_trade_link = "https://www.example.com/exchange1/{}".format(symbol.replace("/", "_"))
        exchange2_trade_link = "https://www.example.com/exchange2/{}".format(symbol.replace("/", "_"))

        data.append({
            'symbol': symbol,
            'exchange1_price': exchange1_price,
            'exchange2_price': exchange2_price,
            'arbitrage': arbitrage,
            'exchange1_trade_link': exchange1_trade_link,
            'exchange2_trade_link': exchange2_trade_link
        })

    # Sort data by arbitrage value
    data.sort(key=lambda x: x['arbitrage'], reverse=True)

    return data