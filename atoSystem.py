from equipment.pump import pump
import time as t
from equipment import pump as p
from equipment import floatSensor as s
from tkinter import * 
from threading import Thread
import asyncio

#import RPi.GPIO as gpio


class atoSystem:

    def __init__(self,emailSystem,pumpFrequency,sumpwaterLevelSensor,atoResSensor,callback):

        self.atoPump=pumpFrequency
        self.sumpwaterLevelSensor = sumpwaterLevelSensor
        self.atoResSensor = atoResSensor
        self.operationalStatus=False

        self.callback  = callback

        self.warning = ""
        self.needsWater = False

        self.emailSystem  = emailSystem

        self.on()



    def on(self) :
        self.t=Thread(target=self.start, name = 'ATO Thread')
        self.t.start()


    def start(self):
        print('ato start 1')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run())
        print('tet2')

    def Off(self):
        self.operationalStatus=False
        self.atoPump.lock=False
        t.sleep(.1)
        self.atoPump.Off()
        t.sleep(.1)
        self.atoPump.Off()
        self.callback()


# gui methods

    def atoPumpOnFromUser(self,newStatus):
        self.atoPump.userAction(newStatus)
        self.log('pump {} from user'.format(newStatus))
        self.callback()
        
    
    def Noramlize(self):
        self.atoPump.normalize()
        self.log('pump normalized')
        self.callback()
        self.callback()
        
# Websocket methods
    #toggles the system on and off
    #used by websocket
    def toggleSystem(self):
        print('toggleSystemATO')
        if(self.operationalStatus):
            print('atosoff')
            self.Off()
        else:
            print('atosom')
            self.on()

    #toggles ato pump 
    #used by websocket
    def togglePump(self):
        if(self.atoPump.status):
            self.atoPumpOnFromUser(False)
        else:
            self.atoPumpOnFromUser(True)

    #toggles atop pump lock
    # normalizes if locked
    def togglePumpLock(self):
        if(self.atoPump.lock):
            self.Noramlize()
        else:
            self.atoPump.lock = True
            self.callback()


        

    '''
        rules:
            if res is low water doesnt pump
            if tank is low water pumped
    '''

    def log(self,message= '',warning=''):
        pass
        #self.logger.ato(self.operationalStatus,self.sumpwaterLevelSensor.getLevel(),self.atoResSensor.getLevel(),message,warning)



    async def run(self):
        self.atoPump.lock=False
        self.operationalStatus=True
        sleepTime = 1
        tempForPumpOn = 0
        self.callback()
        #print('ato run[')
        while self.operationalStatus:
           # print('aotThread')
            
            sumpLevel = self.sumpwaterLevelSensor.level
            atoLevel = self.atoResSensor.level
            
            #if sump level low and res has water
            if(sumpLevel == 0 and atoLevel == 0):
                if( not self.atoPump.status and not self.atoPump.lock):
                    self.atoPump.On()
                    self.callback()
                    #print('pump on from ato temp var = {0} and temp%50={1}'.format(tempForPumpOn,tempForPumpOn%50))
                self.log('pump turned on')
                sleepTime = .1
                #tempForPumpOn = tempForPumpOn+1
                #print("Test1")

            #if res needs refilled
            elif atoLevel == 1:
                #print("Test2")
                if not self.needsWater:
                    self.warning = 'ato res needs water'
                    self.callback()
                try:
                    self.emailSystem.sendMessage(self.warning)
                except:
                    self.log('error in email system')
                self.needsWater = True
                self.atoPump.Off()
                self.operationalStatus = False
                self.log('res too low','res to low')
                tempForPumpOn = 0
                self.callback()

            
            else:
                #print("Test3")
                if(self.atoPump.status and not self.atoPump.lock):
                    self.atoPump.Off()
                    self.callback()
                self.log('pump turned off')
                sleepTime = 1
                #tempForPumpOn = 0
            t.sleep(sleepTime)
