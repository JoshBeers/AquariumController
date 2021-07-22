from equipment  import pump
from equipment  import floatSensor
import time
from threading import Thread
from tkinter import * 
import asyncio



class sensorCheckor:

    def __init__(self,tankPumps, atoPump, tankFloatSensor, sumpFloatSensor, atoFloarSensor):

        self.tankFloatSensor = tankFloatSensor
        self.sumpFloatSensor = sumpFloatSensor
        self.atoFloatSensor = atoFloarSensor

        self.callback = self.fakeCallback

        self.tankPumps = tankPumps
        self.atoPump = atoPump


        #need to setup run method
        self.t=Thread()
        self.t.start()
        self.t.join()
        
        self.t=Thread(target=self.start, name = 'Sensor Thread',daemon=True)
        self.t.start()
        

    def stop(self):
        self.opporationalStatus = False
        self.callback()

    def fakeCallback(self):
        pass

    def start(self):
        print('tet1')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run())
        print('sensors ended')
    



    async def run(self):
        self.opporationalStatus = True
        self.callback()
        while( self.opporationalStatus):
         #   print('sensorThread')
            self.tankFloatSensor.getLevel()
            self.sumpFloatSensor.getLevel()
            self.atoFloatSensor.getLevel()
            #print(self.opporationalStatus)
            self.callback()
            time.sleep(.1)
