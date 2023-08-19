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
    },
    'exchanges.mexc': {
        'name': 'MEXC',
        'trade_base_url': 'https://www.mexc.com/exchange/',
        'module': 'exchanges.mexc',
    },
    'exchanges.binance': {
        'name': 'Binance',
        'trade_base_url': 'https://www.binance.com/en/trade/',
        'module': 'exchanges.binance',
    },
    'exchanges.bybit': {
        'name': 'Bybit',
        'trade_base_url': 'https://www.bybit.com/trade/',
        'module': 'exchanges.bybit'
    },
    'exchanges.coinbase_pro': {
        'name': 'Coinbase',
        'trade_base_url': 'https://www.coinbase.com/trade/',
        'module': 'exchanges.coinbase_pro',
    },
    'exchanges.kraken': {
        'name': 'Kraken',
        'trade_base_url': 'https://pro.kraken.com/app/trade/',
        'module': 'exchanges.kraken',
    },
    # Kukoin module
    'exchanges.kukoin': {
        'name': 'KuCoin',
        'trade_base_url': 'https://www.kucoin.com/trade/',
        'module': 'exchanges.kukoin',
    },
    # Okex module
    'exchanges.okex': {
        'name': 'OKEx',
        'trade_base_url': 'https://www.okex.com/',
        'module': 'exchanges.okex',
    },
    # Bitstamp module
    'exchanges.bitstamp': {
        'name': 'Bitstamp',
        'trade_base_url': 'https://www.bitstamp.net/market/tradeview/',
        'module': 'exchanges.bitstamp',
    },
    # Bitfinex module
    'exchanges.bitfinex': {
        'name': 'Bitfinex',
        'trade_base_url': 'https://www.bitfinex.com/',
        'module': 'exchanges.bitfinex',
    },
    # Gemini module
    'exchanges.gemini': {
        'name': 'Gemini',
        'trade_base_url': 'https://www.gemini.com/trade/',
        'module': 'exchanges.gemini',
    },
    # Bitflyer module
    'exchanges.bitflyer': {
        'name': 'Bitflyer',
        'trade_base_url': 'https://bitflyer.com/en-jp/trade',
        'module': 'exchanges.bitflyer',
    },
    # Bithumb module
    'exchanges.bithumb': {
        'name': 'Bithumb',
        'trade_base_url': 'https://www.bithumb.com/trade/order/',
        'module': 'exchanges.bithumb',
    },
    # Huobi module
    'exchanges.huobi': {
        'name': 'Huobi',
        'trade_base_url': 'https://www.huobi.com/',
        'module': 'exchanges.huobi',
    },
    # Crypto.com module
    'exchanges.crypto_com': {
        'name': 'Crypto.com',
        'trade_base_url': 'https://crypto.com/exchange/',
        'module': 'exchanges.crypto_com',
    },
    # LBank module
    'exchanges.lbank': {
        'name': 'LBank',
        'trade_base_url': 'https://www.lbank.info/',
        'module': 'exchanges.lbank',
    },
    # Coincheck module
    'exchanges.coincheck': {
        'name': 'Coincheck',
        'trade_base_url': 'https://coincheck.com/exchange/spot/trade',
        'module': 'exchanges.coincheck',
    },
    'exchanges.bitget': {
        'name': 'Bitget',
        'trade_base_url': 'https://www.bitget.com/en/contract',
        'module': 'exchanges.bitget',
    },
    # Upbit module
    'exchanges.upbit': {
        'name': 'Upbit',
        'trade_base_url': 'https://upbit.com/exchange?code=CRIX.UPBIT.',
        'module': 'exchanges.upbit',
    },
    # P2PB2B module
    'exchanges.p2pb2b': {
        'name': 'P2PB2B',
        'trade_base_url': 'https://p2pb2b.io/trade/',
        'module': 'exchanges.p2pb2b',
    },
    # Probit Global module
    'exchanges.probit_global': {
        'name': 'Probit Global',
        'trade_base_url': 'https://www.probit.com/app/exchange/',
        'module': 'exchanges.probit_global',
    },
    # Bitforex module
    'exchanges.bitforex': {
        'name': 'Bitforex',
        'trade_base_url': 'https://www.bitforex.com/',
        'module': 'exchanges.bitforex',
    },
    # Korbit module
    'exchanges.korbit': {
        'name': 'Korbit',
        'trade_base_url': 'https://www.korbit.co.kr/',
        'module': 'exchanges.korbit',
    },
    # XT module
    'exchanges.xt': {
        'name': 'XT',
        'trade_base_url': 'https://www.xt.com/',
        'module': 'exchanges.xt',
    },
    # Coinw module
    'exchanges.coinw': {
        'name': 'Coinw',
        'trade_base_url': 'https://www.coinw.com/',
        'module': 'exchanges.coinw',
    },
    # Pionex module
    'exchanges.pionex': {
        'name': 'Pionex',
        'trade_base_url': 'https://www.pionex.com/',
        'module': 'exchanges.pionex',
    },
    # Bitmart module
    'exchanges.bitmart': {
        'name': 'Bitmart',
        'trade_base_url': 'https://www.bitmart.com/trade',
        'module': 'exchanges.bitmart',
    },
    # Poloniex module
    'exchanges.poloniex': {
        'name': 'Poloniex',
        'trade_base_url': 'https://poloniex.com/trade/',
        'module': 'exchanges.poloniex',
    },
    # Whitebit module
    'exchanges.whitebit': {
        'name': 'Whitebit',
        'trade_base_url': 'https://whitebit.com/trade/',
        'module': 'exchanges.whitebit',
    },
    # Exmo module
    'exchanges.exmo': {
        'name': 'Exmo',
        'trade_base_url': 'https://exmo.com/',
        'module': 'exchanges.exmo',
    },
    # Indoex module
    'exchanges.indoex': {
        'name': 'Indoex',
        'trade_base_url': 'https://www.indoex.io/',
        'module': 'exchanges.indoex',
    },
    # Bingx module
    'exchanges.bingx': {
        'name': 'Bingx',
        'trade_base_url': 'https://www.bingx.com/',
        'module': 'exchanges.bingx',
    },
    # BtcTurk module
    'exchanges.btcturk': {
        'name': 'BtcTurk',
        'trade_base_url': 'https://pro.btcturk.com/pro/{pair}',
        'module': 'exchanges.btcturk',
    },
    # Indoex module
    'exchanges.indoex': {
        'name': 'Indoex',
        'trade_base_url': 'https://www.indoex.io/',
        'module': 'exchanges.indoex',
    },
    # Add more exchanges and their details here
}
