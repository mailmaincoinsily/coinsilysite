import asyncio
from binance.client import Client

async def get_usdt_pairs():
    client = Client()
    markets = await client.get_exchange_info()
    usdt_pairs = []

    for symbol in markets['symbols']:
        if 'USDT' in symbol['symbol']:
            usdt_pairs.append(symbol['symbol'])
    
    return usdt_pairs

async def calculate_arbitrage(pair1, pair2, pair3):
    client = Client()
    
    ticker1 = await client.get_ticker(symbol=pair1)
    ticker2 = await client.get_ticker(symbol=pair2)
    ticker3 = await client.get_ticker(symbol=pair3)
    
    # Perform triangular arbitrage calculations here
    
    return {
        'pair1': pair1,
        'pair2': pair2,
        'pair3': pair3,
        'profit_percentage': calculated_profit
    }

async def main():
    usdt_pairs = await get_usdt_pairs()
    arbitrage_opportunities = []

    for i in range(len(usdt_pairs)):
        for j in range(i + 1, len(usdt_pairs)):
            for k in range(j + 1, len(usdt_pairs)):
                pair1 = usdt_pairs[i]
                pair2 = usdt_pairs[j]
                pair3 = usdt_pairs[k]
                
                arbitrage_data = await calculate_arbitrage(pair1, pair2, pair3)
                
                if arbitrage_data['profit_percentage'] > 0:
                    arbitrage_opportunities.append(arbitrage_data)

    # Display arbitrage opportunities
    for opportunity in arbitrage_opportunities:
        print("Triangular Arbitrage Opportunity:")
        print("Buy", opportunity['pair1'].replace("USDT", ""), "with USDT,", 
              "Sell", opportunity['pair2'].replace("USDT", ""), "with", opportunity['pair1'].replace("USDT", ""), ",",
              "Sell", opportunity['pair3'].replace("USDT", ""), "with", opportunity['pair2'].replace("USDT", ""), ",",
              "Profit Percentage:", opportunity['profit_percentage'], "%")
        print()

# Run the event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
