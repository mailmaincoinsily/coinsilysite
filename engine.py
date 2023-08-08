from importlib import import_module
from config import EXCHANGES
from coingecko import get_coingecko_price

def get_exchange_name(exchange_key):
    return EXCHANGES[exchange_key]['name']

def get_exchange_module(exchange_key):
    module_name = EXCHANGES[exchange_key]['module']
    return import_module(module_name)

def calculate_arbitrage(exchange1, exchange2, exchange1_coingecko_price, exchange2_coingecko_price):
    exchange1_config = EXCHANGES.get(exchange1)
    exchange2_config = EXCHANGES.get(exchange2)

    if not exchange1_config or not exchange2_config:
        return [], 0, 0  # Return empty data and zero counts

    exchange1_module = get_exchange_module(exchange1_config['module'])
    exchange2_module = get_exchange_module(exchange2_config['module'])

    exchange1_tickers = exchange1_module.get_exchange_data()
    exchange2_tickers = exchange2_module.get_exchange_data()

    exchange1_trade_base_url = exchange1_config['trade_base_url']
    exchange2_trade_base_url = exchange2_config['trade_base_url']

    common_symbols = set(exchange1_tickers.keys()) & set(exchange2_tickers.keys())

    data = []
    for symbol in common_symbols:
        exchange1_price = float(exchange1_tickers[symbol]['last'])
        exchange2_price = float(exchange2_tickers[symbol]['last']) if exchange2_tickers[symbol]['last'] is not None else 0.0
        arbitrage = round((exchange2_price - exchange1_price) / exchange1_price * 100, 2)

        # Calculate price differences
        exchange1_price_diff = exchange1_price - exchange1_coingecko_price
        exchange2_price_diff = exchange2_price - exchange2_coingecko_price

        exchange1_trade_link = "{}{}".format(exchange1_trade_base_url, symbol.replace("/", "_"))
        exchange2_trade_link = "{}{}".format(exchange2_trade_base_url, symbol.replace("/", "_"))

        data.append({
            'symbol': symbol,
            'exchange1_price': exchange1_price,
            'exchange2_price': exchange2_price,
            'arbitrage': arbitrage,
            'exchange1_price_diff': exchange1_price_diff,
            'exchange2_price_diff': exchange2_price_diff,
            'exchange1_trade_link': exchange1_trade_link,
            'exchange2_trade_link': exchange2_trade_link,
            'exchange1_name': exchange1_config['name'],
            'exchange2_name': exchange2_config['name']
        })

    # Sort data by arbitrage value
    data.sort(key=lambda x: x['arbitrage'], reverse=True)

    # Calculate positive and negative counts
    positive_count = sum(1 for item in data if item['arbitrage'] > 0)
    negative_count = sum(1 for item in data if item['arbitrage'] < 0)

    return data, positive_count, negative_count
