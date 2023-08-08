def get_coingecko_price(exchange1, exchange2):
    try:
        exchange1_coingecko_price = coingecko.get_price(ids=exchange1, vs_currencies='usd')[exchange1]['usd']
        exchange2_coingecko_price = coingecko.get_price(ids=exchange2, vs_currencies='usd')[exchange2]['usd']
        
        return {
            'exchange1_coingecko_price': exchange1_coingecko_price,
            'exchange2_coingecko_price': exchange2_coingecko_price
        }
    except Exception as e:
        return {
            'exchange1_coingecko_price': 0.0,
            'exchange2_coingecko_price': 0.0
        }
