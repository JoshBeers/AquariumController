from equipment.pump import pump
import time as t
from equipment import pump as p
from equipment import floatSensor as s
from tkinter import * 
from threading import Thread
#import RPi.GPIO as gpio


class atoSystem:

    def __init__(self,emailSystem,pumpFrequency,sumpwaterLevelSensor,atoResSensor):

        self.atoPump=pumpFrequency
        self.sumpwaterLevelSensor = sumpwaterLevelSensor
        self.atoResSensor = atoResSensor

        self.opperationalStatus=False

        self.warning = ""
        self.needsWater = False

        self.emailSystem  = emailSystem
    
        self.t=Thread()
        self.t.start()
        self.t.join()


    def on(self) :
        self.t=Thread(target=self.run)
        self.t.start()
        self.log('system started')
    

    def Off(self):
        self.opperationalStatus=False
        self.atoPump.lock=False
        self.atoPump.Off()
        self.log('system stopped')


    def atoPumpOnFromUser(self,newStatus):
        self.atoPump.userAction(newStatus)
        self.log('pump {} from user'.format(newStatus))
    
    def Noramlize(self):
        self.atoPump.normalize()
        self.log('pump normalized')

        

    '''
        rules:
            if res is low water doesnt pump
            if tank is low water pumped
    '''

    def log(self,message= '',warning=''):
        pass
        #self.logger.ato(self.opperationalStatus,self.sumpwaterLevelSensor.getLevel(),self.atoResSensor.getLevel(),message,warning)
        

    def run(self):
        self.atoPump.lock=False
        self.opperationalStatus=True
        sleepTime = 1
        tempForPumpOn = 0
        while self.opperationalStatus:
            #print(self.atoPump.status)
            #if sump level low and res has water
            sumpLevel = self.sumpwaterLevelSensor.level
            atoLevel = self.atoResSensor.level
            
            if(sumpLevel == 0 and atoLevel == 0):
                if(tempForPumpOn%50 == 0):
                    self.atoPump.On()
                    #print('pump on from ato temp var = {0} and temp%50={1}'.format(tempForPumpOn,tempForPumpOn%50))
                self.log('pump turned on')
                sleepTime = .1
                tempForPumpOn = tempForPumpOn+1
                #print("Test1")
            #if res needs refilled
            elif atoLevel == 1:
                #print("Test2")
                if not self.needsWater:
                    self.warning = 'ato res needs water'
                try:
                    self.emailSystem.sendMessage(self.warning)
                except:
                    self.log('error in email system')
                self.needsWater = True
                self.atoPump.Off()
                self.opperationalStatus = False
                self.log('res too low','res to low')
                tempForPumpOn = 0
            else:
                #print("Test3")
                self.atoPump.Off()
                self.log('pump turned off')
                sleepTime = 10
                tempForPumpOn = 0
            t.sleep(sleepTime)
