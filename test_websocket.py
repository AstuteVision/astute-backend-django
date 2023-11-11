import asyncio

import websockets


async def test_websocket():
    headers = {'client-id': '1'}
    async with websockets.connect("ws://127.0.0.1:8000/ws", extra_headers=headers) as websocket:
        # here goods uuids to buy
        await websocket.send("['f360b82d-8e49-41d4-adf2-5b409a256dea']")
        while True:
            data = await websocket.recv()
            print(data)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(test_websocket())
