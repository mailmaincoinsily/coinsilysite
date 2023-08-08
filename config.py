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
    'gateio': {
        'name': 'Gate.io',
        'trade_base_url': 'https://www.gate.io/trade/',
        'module': 'exchanges/gateio',  # Name of the module (gateio.py) without the .py extension
    },
    'mexc': {
        'name': 'MEXC',
        'trade_base_url': 'https://www.mexc.com/exchange/',
        'module': 'exchanges/mexc',
    },
    'binance': {
        'name': 'Binance',
        'trade_base_url': 'https://www.binance.com/en/trade/',
        'module': 'exchanges/binance',
    },
    # Add more exchanges and their details here
}
