import ccxt

def check_coin_availability(symbol):
    gateio = ccxt.gateio()
    mexc_global = ccxt.mexc()

    try:
        gateio_markets = gateio.load_markets()
        gateio_symbol_info = gateio_markets[symbol]
        gateio_deposit = gateio_symbol_info['info']['depositEnable']
        gateio_withdrawal = gateio_symbol_info['info']['withdrawEnable']
        gateio_volume = gateio_symbol_info['info']['volume']
    except Exception as e:
        error_message = "Error retrieving data from Gateio API for {}: {}".format(symbol, e)
        return {
            'symbol': symbol,
            'error_message': error_message
        }

    try:
        mexc_markets = mexc_global.load_markets()
        mexc_symbol_info = mexc_markets[symbol]
        mexc_deposit = mexc_symbol_info['info']['deposit_status']
        mexc_withdrawal = mexc_symbol_info['info']['withdraw_status']
        mexc_volume = mexc_symbol_info['info']['vol']
    except Exception as e:
        error_message = "Error retrieving data from MEXC Global API for {}: {}".format(symbol, e)
        return {
            'symbol': symbol,
            'error_message': error_message
        }

    return {
        'symbol': symbol,
        'gateio_deposit': gateio_deposit,
        'gateio_withdrawal': gateio_withdrawal,
        'gateio_volume': gateio_volume,
        'mexc_deposit': mexc_deposit,
        'mexc_withdrawal': mexc_withdrawal,
        'mexc_volume': mexc_volume
    }
