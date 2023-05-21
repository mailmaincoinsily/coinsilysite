import requests

def get_coin_info(exchange, coin_symbol):
    if exchange == "gateio":
        url = f"https://api.gateio.ws/api/v4/spot/currencies/{coin_symbol}/deposits"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            deposit_available = data.get("can_deposit")
        else:
            deposit_available = "N/A"

        url = f"https://api.gateio.ws/api/v4/spot/currencies/{coin_symbol}/withdrawals"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            withdrawal_available = data.get("can_withdraw")
        else:
            withdrawal_available = "N/A"

        url = f"https://api.gateio.ws/api/v4/spot/trades/{coin_symbol}_usdt"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            volume = data[0].get("base_volume")
        else:
            volume = "N/A"

    elif exchange == "mexc":
        url = f"https://www.mxc.com/open/api/v2/asset/detail?symbol={coin_symbol}"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            deposit_available = data.get("data").get("canDeposit")
            withdrawal_available = data.get("data").get("canWithdraw")
            volume = data.get("data").get("vol24")
        else:
            deposit_available = "N/A"
            withdrawal_available = "N/A"
            volume = "N/A"

    return deposit_available, withdrawal_available, volume

# Example usage
coin_symbol = "BTC"  # Specify the symbol of the coin you want to check
gateio_deposit, gateio_withdrawal, gateio_volume = get_coin_info("gateio", coin_symbol)
mexc_deposit, mexc_withdrawal, mexc_volume = get_coin_info("mexc", coin_symbol)

print(f"Gate.io - Deposit Available: {gateio_deposit}")
print(f"Gate.io - Withdrawal Available: {gateio_withdrawal}")
print(f"Gate.io - Volume: {gateio_volume}")

print(f"MEXC - Deposit Available: {mexc_deposit}")
print(f"MEXC - Withdrawal Available: {mexc_withdrawal}")
print(f"MEXC - Volume: {mexc_volume}")
