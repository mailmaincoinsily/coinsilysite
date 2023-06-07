
import requests
import hmac
import hashlib
import time

api_key = 'mx0vglpV8ICvJHIwgM'
api_secret = '95199bdf8657439989cfdc51521e341f'

timestamp = str(int(time.time() * 1000))
request_path = '/open/api/v3/asset/currency'
method = 'GET'
body = ''

message = timestamp + method + request_path + body
signature = hmac.new(api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

headers = {
    'Content-Type': 'application/json',
    'Apiid': api_key,
    'Timestamp': timestamp,
    'Sign': signature
}

url = "https://www.mxc.com" + request_path

response = requests.get(url, headers=headers)
data = response.json()

for currency in data['data']:
    print(f"{currency['currency']}: {currency['withdraw_fee']}")
