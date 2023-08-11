import ccxt
import asyncio

# Function to handle WebSocket trade events
async def handle_trade(symbol, trade):
    print(f"Received trade for {symbol}: {trade}")

# Function to calculate triangular arbitrage opportunities with WebSocket
async def calculate_triangular_arbitrage_with_ws():
    try:
        binance = ccxt.binance()
        binance_markets = binance.load_markets()
        binance_spot_markets = {symbol: market for symbol, market in binance_markets.items() if market['spot'] and market['active']}

        # Create WebSocket connections for each trading pair
        ws_connections = []
        for base_symbol in binance_spot_markets:
            for quote_symbol in binance_spot_markets:
                if base_symbol != quote_symbol:
                    symbol = f"{base_symbol}/{quote_symbol}"
                    ws_symbol = symbol.replace("/", "").lower()
                    ws_url = f"wss://stream.binance.com:9443/ws/{ws_symbol}@trade"
                    ws_connection = await binance.ws_public_subscribe(ws_url, lambda trade, symbol=symbol: handle_trade(symbol, trade))
                    ws_connections.append(ws_connection)

        while True:
            await asyncio.sleep(1)

        # Close WebSocket connections
        for ws_connection in ws_connections:
            await ws_connection.close()

    except Exception as e:
        print("Exception:", e)

# Call the function to calculate triangular arbitrage opportunities with WebSocket
asyncio.get_event_loop().run_until_complete(calculate_triangular_arbitrage_with_ws())
