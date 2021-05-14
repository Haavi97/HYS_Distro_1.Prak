import asyncio
import websockets
import json

nodeIPAadress = "localhost"
nodePort = "1234"



async def server(websocket, path):
    # Get received data from websocket
    data = await websocket.recv() # in the data is the new IP aadress of a new user
    addToIPList(data)
    IPList = getListWithoutIP(data)
    jsonString = json.dumps(IPList)
    # Send response back to client to acknowledge receiving message
    await websocket.send(jsonString) #Sends a python List containing all the IP aadresses (except for the IP address that was just sent)



def addToIPList(newIP):
    masterList=getGeneralIP()
    if newIP in masterList:
        print("IP aadress already exists.")
        return False
    else:  
        print("IP aadress Not found in Master list. ")
        try:
            file_object = open('IP_List.txt', 'a')
            file_object.write(newIP+"\n")
            file_object.close()
            return True
        except:
            print("Error in writing File")
            pass

# This list is neccesary so that if the client´s IP aadress is somewhere in the middle of the list, then the system will edit that entry out. 
def getListWithoutIP(newIP):
    with open('./IP_List.txt', "r") as f: result = f.readlines()
    cleanedList=[]
    for element in result:
        Length=len(element)
        element=element[:Length-1]
        if element==newIP:
            pass
        else:
            cleanedList.append(element[:Length-1])
    return cleanedList


# This list is neccesary for the general search for a existing IP aadress
def getGeneralIP():
    with open('./IP_List.txt', "r") as f: result = f.readlines()
    cleanedList=[]
    for element in result:
        Length=len(element)
        cleanedList.append(element[:Length-1])
    return cleanedList


# Create websocket server
start_server = websockets.serve(server, nodeIPAadress, nodePort)
# Start and run websocket server forever
asyncio.get_event_loop().run_until_complete(start_server)
print("Main Node running at {} with port: {}".format(nodeIPAadress, nodePort))

asyncio.get_event_loop().run_forever()
