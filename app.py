import ccxt
import asyncio

async def find_arbitrage_opportunities():
    binance = ccxt.binance()
    markets = await binance.fetch_markets()
    
    usdt_pairs = [market['symbol'] for market in markets if 'USDT' in market['symbol']]
    
    for pair1 in usdt_pairs:
        for pair2 in usdt_pairs:
            for pair3 in usdt_pairs:
                if pair1 != pair2 and pair2 != pair3 and pair1 != pair3:
                    orderbook1 = await binance.fetch_order_book(pair1)
                    orderbook2 = await binance.fetch_order_book(pair2)
                    orderbook3 = await binance.fetch_order_book(pair3)
                    
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

asyncio.run(find_arbitrage_opportunities())
