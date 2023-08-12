import ccxt

def find_arbitrage_opportunities():
    binance = ccxt.binance()
    markets = binance.fetch_markets()
    
    usdt_assets = set()
    
    # Collect assets trading with USDT
    for market in markets:
        if 'USDT' in market['symbol']:
            base, quote = market['symbol'].split('/')
            if base != 'USDT':
                usdt_assets.add(base)
            if quote != 'USDT':
                usdt_assets.add(quote)
    
    usdt_assets = list(usdt_assets)
    
    for base in usdt_assets:
        for quote in usdt_assets:
            if base != quote:
                pair1 = f"{base}/USDT"
                pair2 = f"USDT/{quote}"
                pair3 = f"{quote}/{base}"
                
                try:
                    orderbook1 = binance.fetch_order_book(pair1)
                    orderbook2 = binance.fetch_order_book(pair2)
                    orderbook3 = binance.fetch_order_book(pair3)
                    
                    bid1 = orderbook1['bids'][0][0] if len(orderbook1['bids']) > 0 else None
                    ask1 = orderbook1['asks'][0][0] if len(orderbook1['asks']) > 0 else None
                    bid2 = orderbook2['bids'][0][0] if len(orderbook2['bids']) > 0 else None
                    ask2 = orderbook2['asks'][0][0] if len(orderbook2['asks']) > 0 else None
                    bid3 = orderbook3['bids'][0][0] if len(orderbook3['bids']) > 0 else None
                    ask3 = orderbook3['asks'][0][0] if len(orderbook3['asks']) > 0 else None
                    
                    if bid1 and ask2 and ask3:
                        rate = (1 / bid1) * ask2 * ask3
                        if rate > 1:
                            print(f"Arbitrage Opportunity Found: {pair1} -> {pair2} -> {pair3}")
                            print(f"Profit Rate: {rate:.8f}")
                            print("======================")
                except:
                    pass

find_arbitrage_opportunities()
