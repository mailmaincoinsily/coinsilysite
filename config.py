# config.py

# Existing code for logging configuration
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

app = Flask(__name__)
app.static_folder = 'static'
logger = logging.getLogger(__name__)

# Configure logger to write logs to a file
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# New code for exchange configuration
EXCHANGES = {
    'exchanges.gateio': {
        'name': 'Gate.io',
        'trade_base_url': 'https://www.gate.io/trade/',
        'module': 'exchanges.gateio',  # Name of the module (gateio.py) without the .py extension
        'sign': '_' 
    },
    'exchanges.mexc': {
        'name': 'MEXC',
        'trade_base_url': 'https://www.mexc.com/exchange/',
        'module': 'exchanges.mexc',
        'sign': '_' 
    },
    'exchanges.binance': {
        'name': 'Binance',
        'trade_base_url': 'https://www.binance.com/en/trade/',
        'module': 'exchanges.binance',
        'sign': '_' 
    },
    'exchanges.bybit': {
        'name': 'Bybit',
        'trade_base_url': 'https://www.bybit.com/trade/spot/',
        'module': 'exchanges.bybit'
        'sign': '/'
    },
    'exchanges.coinbase_pro': {
        'name': 'Coinbase',
        'trade_base_url': 'https://www.coinbase.com/trade/',
        'module': 'exchanges.coinbase_pro',
        'sign': '_' 
    },
    'exchanges.kraken': {
        'name': 'Kraken',
        'trade_base_url': 'https://pro.kraken.com/app/trade/',
        'module': 'exchanges.kraken',
        'sign': '_' 
    },
    # Kukoin module
    'exchanges.kukoin': {
        'name': 'KuCoin',
        'trade_base_url': 'https://www.kucoin.com/trade/',
        'module': 'exchanges.kukoin',
        'sign': '_' 
    },
    # Okex module
    'exchanges.okex': {
        'name': 'OKEx',
        'trade_base_url': 'https://www.okex.com/',
        'module': 'exchanges.okex',
        'sign': '_' 
    },
    # Bitstamp module
    'exchanges.bitstamp': {
        'name': 'Bitstamp',
        'trade_base_url': 'https://www.bitstamp.net/market/tradeview/',
        'module': 'exchanges.bitstamp',
        'sign': '_' 
    },
    # Bitfinex module
    'exchanges.bitfinex': {
        'name': 'Bitfinex',
        'trade_base_url': 'https://www.bitfinex.com/',
        'module': 'exchanges.bitfinex',
        'sign': '_' 
    },
    # Gemini module
    'exchanges.gemini': {
        'name': 'Gemini',
        'trade_base_url': 'https://www.gemini.com/trade/',
        'module': 'exchanges.gemini',
        'sign': '_' 
    },
    # Bitflyer module
    'exchanges.bitflyer': {
        'name': 'Bitflyer',
        'trade_base_url': 'https://bitflyer.com/en-jp/trade',
        'module': 'exchanges.bitflyer',
        'sign': '_' 
    },
    # Bithumb module
    'exchanges.bithumb': {
        'name': 'Bithumb',
        'trade_base_url': 'https://www.bithumb.com/trade/order/',
        'module': 'exchanges.bithumb',
        'sign': '_' 
    },
    # Huobi module
    'exchanges.huobi': {
        'name': 'Huobi',
        'trade_base_url': 'https://www.huobi.com/',
        'module': 'exchanges.huobi',
        'sign': '_' 
    },
    # Crypto.com module
    'exchanges.crypto_com': {
        'name': 'Crypto.com',
        'trade_base_url': 'https://crypto.com/exchange/',
        'module': 'exchanges.crypto_com',
        'sign': '_' 
    },
    # LBank module
    'exchanges.lbank': {
        'name': 'LBank',
        'trade_base_url': 'https://www.lbank.info/',
        'module': 'exchanges.lbank',
        'sign': '_' 
    },
    # Coincheck module
    'exchanges.coincheck': {
        'name': 'Coincheck',
        'trade_base_url': 'https://coincheck.com/exchange/spot/trade',
        'module': 'exchanges.coincheck',
        'sign': '_' 
    },
    'exchanges.bitget': {
        'name': 'Bitget',
        'trade_base_url': 'https://www.bitget.com/en/contract',
        'module': 'exchanges.bitget',
        'sign': '_' 
    },
    # Upbit module
    'exchanges.upbit': {
        'name': 'Upbit',
        'trade_base_url': 'https://upbit.com/exchange?code=CRIX.UPBIT.',
        'module': 'exchanges.upbit',
        'sign': '_' 
    },
    # P2PB2B module
    'exchanges.p2pb2b': {
        'name': 'P2PB2B',
        'trade_base_url': 'https://p2pb2b.io/trade/',
        'module': 'exchanges.p2pb2b',
        'sign': '_' 
    },
    # Probit Global module
    'exchanges.probit_global': {
        'name': 'Probit Global',
        'trade_base_url': 'https://www.probit.com/app/exchange/',
        'module': 'exchanges.probit_global',
        'sign': '_' 
    },
    # Bitforex module
    'exchanges.bitforex': {
        'name': 'Bitforex',
        'trade_base_url': 'https://www.bitforex.com/',
        'module': 'exchanges.bitforex',
        'sign': '_' 
    },
    # Korbit module
    'exchanges.korbit': {
        'name': 'Korbit',
        'trade_base_url': 'https://www.korbit.co.kr/',
        'module': 'exchanges.korbit',
        'sign': '_' 
    },
    # XT module
    'exchanges.xt': {
        'name': 'XT',
        'trade_base_url': 'https://www.xt.com/',
        'module': 'exchanges.xt',
        'sign': '_' 
    },
    # Coinw module
    'exchanges.coinw': {
        'name': 'Coinw',
        'trade_base_url': 'https://www.coinw.com/',
        'module': 'exchanges.coinw',
        'sign': '_' 
    },
    # Pionex module
    'exchanges.pionex': {
        'name': 'Pionex',
        'trade_base_url': 'https://www.pionex.com/',
        'module': 'exchanges.pionex',
        'sign': '_' 
    },
    # Bitmart module
    'exchanges.bitmart': {
        'name': 'Bitmart',
        'trade_base_url': 'https://www.bitmart.com/trade',
        'module': 'exchanges.bitmart',
        'sign': '_' 
    },
    # Poloniex module
    'exchanges.poloniex': {
        'name': 'Poloniex',
        'trade_base_url': 'https://poloniex.com/trade/',
        'module': 'exchanges.poloniex',
        'sign': '_' 
    },
    # Whitebit module
    'exchanges.whitebit': {
        'name': 'Whitebit',
        'trade_base_url': 'https://whitebit.com/trade/',
        'module': 'exchanges.whitebit',
        'sign': '_' 
    },
    # Exmo module
    'exchanges.exmo': {
        'name': 'Exmo',
        'trade_base_url': 'https://exmo.com/',
        'module': 'exchanges.exmo',
        'sign': '_' 
    },
    # Indoex module
    'exchanges.indoex': {
        'name': 'Indoex',
        'trade_base_url': 'https://www.indoex.io/',
        'module': 'exchanges.indoex',
        'sign': '_' 
    },
    # Bingx module
    'exchanges.bingx': {
        'name': 'Bingx',
        'trade_base_url': 'https://www.bingx.com/',
        'module': 'exchanges.bingx',
        'sign': '_' 
    },
    # BtcTurk module
    'exchanges.btcturk': {
        'name': 'BtcTurk',
        'trade_base_url': 'https://pro.btcturk.com/pro/{pair}',
        'module': 'exchanges.btcturk',
        'sign': '_' 
    },
    # Indoex module
    'exchanges.indoex': {
        'name': 'Indoex',
        'trade_base_url': 'https://www.indoex.io/',
        'module': 'exchanges.indoex',
        'sign': '_' 
    },
    # Add more exchanges and their details here
}
