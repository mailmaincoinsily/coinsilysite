from flask import Flask, jsonify

app = Flask(__name__)

def get_coin_info(exchange, coin_pair):
    if exchange == "gateio":
        # Replace with the logic to retrieve coin information from Gate.io API
        deposit_available = True
        withdrawal_available = True
        volume = 50000

    elif exchange == "mexc":
        # Replace with the logic to retrieve coin information from MXC API
        deposit_available = True
        withdrawal_available = True
        volume = 75000

    return deposit_available, withdrawal_available, volume

@app.route('/coin/<coin_pair>')
def get_coin_pair_info(coin_pair):
    # Split coin_pair into base and quote symbols
    base_symbol, quote_symbol = coin_pair.split('_')

    # Get coin information for Gate.io
    gateio_deposit, gateio_withdrawal, gateio_volume = get_coin_info("gateio", coin_pair)

    # Get coin information for MXC
    mexc_deposit, mexc_withdrawal, mexc_volume = get_coin_info("mexc", coin_pair)

    return jsonify({
        'base_symbol': base_symbol,
        'quote_symbol': quote_symbol,
        'gateio': {
            'deposit_available': gateio_deposit,
            'withdrawal_available': gateio_withdrawal,
            'volume': gateio_volume
        },
        'mexc': {
            'deposit_available': mexc_deposit,
            'withdrawal_available': mexc_withdrawal,
            'volume': mexc_volume
        }
    })

if __name__ == '__main__':
    app.run()
