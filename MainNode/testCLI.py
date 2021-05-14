import asyncio
import websockets
import json


async def hello():
    MainNodeUri = "ws://localhost:1234"
    async with websockets.connect(MainNodeUri) as websocket:
        #name = input("What's your name? ")
        IPAddress="127.0.0.1:6500"
        print("Sent IP aadress is {}".format(IPAddress))
        await websocket.send(IPAddress)

        jsonString = await websocket.recv()
        IPList = json.loads(jsonString)
        iplist = list(map(lambda x: str(x), IPList))
        print("recieved IP list is: ")
        print(iplist)
        print(type(iplist[0]))

        #print(f"< {IPList}")

asyncio.get_event_loop().run_until_complete(hello())
