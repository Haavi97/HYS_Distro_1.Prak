import asyncio
import websockets
import json


async def hello():
    MainNodeUri = "ws://localhost:5000"
    async with websockets.connect(MainNodeUri) as websocket:
        #name = input("What's your name? ")
        IPAddress="127.0.0.1:6500"
        print("Sent IP aadress is {}".format(IPAddress))
        await websocket.send(IPAddress)

        jsonString = await websocket.recv()
        IPList = json.loads(jsonString)
        print("recieved IP list is: ")
        print(IPList)

        #print(f"< {IPList}")

asyncio.get_event_loop().run_until_complete(hello())
