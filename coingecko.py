from pycoingecko import CoinGeckoAPI

coingecko = CoinGeckoAPI()

def get_coingecko_price(symbol):
    try:
        coingecko_price = coingecko.get_price(ids=symbol, vs_currencies='usd')[symbol]['usd']
        return coingecko_price
    except Exception as e:
        return None  # Handle exception gracefully or set a default value
