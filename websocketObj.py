import websockets
import logging
from websockets import WebSocketServerProtocol 
import asyncio
from threading import Thread

connected = set()



class websocketStuff:

    def __init__(self,stuff):
        self.stuff = stuff
        self.server = Server(stuff)
        self.start_server = websockets.serve(self.server.ws_handler,"localhost", 5000)

    
    def start(self):
        print('test1')
        asyncio.get_event_loop().run_until_complete(self.start_server)
        print('test2')
        #thread = Thread(target=asyncio.get_event_loop().run_forever)
        asyncio.get_event_loop().run_forever()


    async def update(self):
        print('update Websocket')
        await self.server.updateClients('test update Clients')

    def close(self):
        asyncio.get_event_loop().stop()

class Server:
    clients = set()

    def __init__(self,stuff):
        self.stuff = stuff

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} conneted.')

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnected')

    async def updateClients(self, message:str) -> None:
        if(self.clients):
            await asyncio.wait([client.send(message) for client in self.clients])
    
    async def ws_handler(self, ws:WebSocketServerProtocol, uri:str) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)
    
    async def distribute(self,  ws:WebSocketServerProtocol) -> None:
        async for message in ws: 
            print(self.stuff[0].operationalStatus)
    
    async def update(self):
        print('test update')
        #self.updateClients('test Update')
        

    
            

        
'''
class testWs:


    websockets.enableTrace(True)
    ws = websockets.WebSocketApp("ws://localhost/5000")
    t = Thread(target=ws.run_forever)
    t.daemon =True
    t.start()


    def start():

'''

