import asyncio
import websockets
import json

async def p2ring(ip_address, port, iphandler):
    MainNodeUri = "ws://localhost:1234"
    async with websockets.connect(MainNodeUri) as websocket:
        IPAddress = str(ip_address) + ':' + str(port)
        print("Sent IP aadress is {}".format(IPAddress))
        await websocket.send(IPAddress)

        jsonString = await websocket.recv()
        IPList = json.loads(jsonString)
        iplist = list(map(lambda x: str(x), IPList))
        print("recieved IP list is: ")
        print(iplist)
        iphandler.add_ip_list(iplist)
        return iplist