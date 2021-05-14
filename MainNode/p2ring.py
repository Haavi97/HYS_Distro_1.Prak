import asyncio
import websockets
import json

async def p2ring(ip_address, port, iphandler):
    MainNodeUri = "ws://localhost:1234"
    async with websockets.connect(MainNodeUri) as websocket:
        IPAddress=ip_address + ':' + port
        print("Sent IP aadress is {}".format(IPAddress))
        await websocket.send(IPAddress)

        jsonString = await websocket.recv()
        IPList = json.loads(jsonString)
        print("recieved IP list is: ")
        print(IPList)
        iphandler.add_ip_list(IPList)