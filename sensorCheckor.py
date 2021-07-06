from equipment  import pump
from equipment  import floatSensor
import time
from threading import Thread
from tkinter import * 


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
        
        self.t=Thread(target=self.run)
        self.t.start()
        

    def stop(self):
        self.opporationalStatus = False
        self.callback()

    def fakeCallback(self):
        pass
    



    def run(self):
        self.opporationalStatus = True
        self.callback()
        while( self.opporationalStatus):
            self.tankFloatSensor.getLevel()
            self.sumpFloatSensor.getLevel()
            self.atoFloatSensor.getLevel()
            #print(self.opporationalStatus)
            self.callback()
            time.sleep(.1)
