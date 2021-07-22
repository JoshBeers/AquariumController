import threading
import websockets
import logging
from websockets import WebSocketServerProtocol 
import asyncio
from threading import Thread
import json




connected = set()
authed = set()



class websocketStuff:

    def __init__(self,stuff):
        self.pumpSystem = stuff[0]
        self.heating = stuff[1]
        self.ato = stuff[2]
        self.sensors = stuff[3]
        self.server = Server(stuff,self)
        self.start_server = websockets.serve(self.server.ws_handler,"localhost", 5000)

    
    def start(self):
        #print('test1')
    
        self.loop = asyncio.get_event_loop()
        asyncio.get_event_loop().run_until_complete(self.start_server)
       # print('websocket Started')
        #thread = Thread(target=asyncio.get_event_loop().run_forever)
        self.loop = asyncio.get_event_loop().run_forever()



    async def update(self):
        print('update')
        await self.server.updateClients(json.dumps({
            'pumpController': {
                'status': self.pumpSystem.operationalStatus,
                'warning':  self.pumpSystem.warning,
                'pump': {
                    'status':self.pumpSystem.pumps.status,
                    'locked' :self.pumpSystem.pumps.lock
                }
            },
            'atoController' :{
                'status': self.ato.operationalStatus,
                'warning': self.ato.warning,
                'pump': {
                    'status':self.ato.atoPump.status,
                    'locked' :self.ato.atoPump.lock
                }
            },
            'sensors':{
                'displayFloatSensorLevel' : self.sensors.tankFloatSensor.level,
                'sumpFloatSensorLevel' : self.sensors.sumpFloatSensor.level,
                'atoReservoirSensorLevel' : self.sensors.atoFloatSensor.level
            }
        }))

    async def close(self):
        asyncio.get_event_loop().stop()
        print('websocket close')

    def receiveCommand(self,message):
        print(message)
        thread = Thread(target= self.rC(message))
        thread.run()
        

    def rC(self,message):

        #for the webiste toggle main pump button
        if(message == 'toggleMainPump'):
            self.pumpSystem.togglePump()

        #for the website toggle main pump lock button 
        elif(message == 'toggleMainPumpLock'):
            self.pumpSystem.togglePumpLock()

        #for the website toggle pump system button
        elif(message == 'togglePumpSystem'):
            self.pumpSystem.toggleSystem()

        #for the website toggle ato system button
        elif(message == 'toggleATOSystem'):
            self.ato.toggleSystem()

        #for the website toggle ato pump button
        elif(message == 'toggleATOPump'):
            self.ato.togglePump()

        #for the website toggle ato pump lock button
        elif(message == 'toggleATOPumpLock'):
            self.ato.togglePumpLock()

    

class Server:
    clients = set()

    def __init__(self,stuff, obj):
        self.pumpSystem = stuff[0]
        self.heating = stuff[1]
        self.ato = stuff[2]
        self.sensors = stuff[3]
        self.obj =obj

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} conneted.')

        await self.updateClients(json.dumps({
            'pumpController': {
                'status': self.pumpSystem.operationalStatus,
                'warning':  self.pumpSystem.warning,
                'pump': {
                    'status':self.pumpSystem.pumps.status,
                    'locked' :self.pumpSystem.pumps.lock
                }
            },
            'atoController' :{
                'status': self.ato.operationalStatus,
                'warning': self.ato.warning,
                'pump': {
                    'status':self.ato.atoPump.status,
                    'locked' :self.ato.atoPump.lock
                }
            },
            'sensors':{
                'displayFloatSensorLevel' : self.sensors.tankFloatSensor.level,
                'sumpFloatSensorLevel' : self.sensors.sumpFloatSensor.level,
                'atoReservoirSensorLevel' : self.sensors.atoFloatSensor.level
            }
        }))
        

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
            self.obj.receiveCommand(message)
        
    
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
