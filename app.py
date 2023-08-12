import ccxt

async def find_triangular_arbitrage_opportunities():
    binance = ccxt.binance()
    
    markets = await binance.load_markets()
    usdt_markets = [market for market in markets if market.endswith('/USDT')]
    
    profitable_trades = []
    
    for market in usdt_markets:
        base_currency, _ = market.split('/')
        
        for intermediate_currency in markets:
            if intermediate_currency.endswith('/USDT') or intermediate_currency == market:
                continue
            
            try:
                order_book = await binance.fetch_order_book(market)
                bid_price = order_book['bids'][0][0]
                
                intermediate_order_book = await binance.fetch_order_book(intermediate_currency)
                ask_price = intermediate_order_book['asks'][0][0]
                
                arbitrage_percentage = ((ask_price / bid_price) - 1) * 100
                
                if arbitrage_percentage > 0:
                    profitable_trades.append({
                        'pair1': market,
                        'pair2': intermediate_currency,
                        'arbitrage_percentage': arbitrage_percentage
                    })
            except (ccxt.BaseError, IndexError):
                pass
            
    profitable_trades.sort(key=lambda trade: trade['arbitrage_percentage'], reverse=True)
    
    return profitable_trades

async def main():
    opportunities = await find_triangular_arbitrage_opportunities()
    
    if opportunities:
        for opportunity in opportunities:
            print(f"Opportunity: {opportunity['pair1']} -> {opportunity['pair2']} ({opportunity['arbitrage_percentage']:.2f}%)")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
