import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello from Python!")
        await websocket.recv()

asyncio.get_event_loop().run_until_complete(hello())
