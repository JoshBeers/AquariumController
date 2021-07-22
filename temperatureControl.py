import time
from equipment import heater as h
from threading import Thread
from tkinter import * 
from equipment import thermometer as te
import os
import errno
import asyncio




class temperatureControl:

    def __init__(self,tempSet,em,heaterLoaction, callback):
        self.heater=h.heater(heaterLoaction,callback)
        self.thermometer=te.thermometer(callback)
        self.temperatureSetting=tempSet
        self.opperationStatus=True
        self.heaterLock=False
        self.warning='none'
        self.warned=False
        self.emails=em


        self.thread=Thread()
        self.thread.start()
        self.thread.join()



#Public stuff
    def On(self):
        pass
        self.opperationStatus=True
        self.heaterLock=False
        self.thread=Thread(target=self.start, name = 'Temp Thread',daemon=True)
        self.thread.start()
        self.log('system turned on')

    def start(self):
        print('tet1')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run())
        print('temp ended')

    def End(self):
        self.opperationStatus=False
        self.heater.Off()
        self.thread.join()
        self.log('system turned off')


    def heaterOff(self):
        self.heaterLock=False
        self.heater.Off()
        self.heaterLock=True
        self.log('heater turned off by user')

        
    def heaterOn(self):
        self.heaterLock=False
        self.heater.On()
        self.heaterLock=True
        self.log('heater turned on by user')


    def heaterNormal(self):
        self.heaterLock=False
        self.log('heater turned normal by user')


    def getHeaterStatus(self):
        return self.heater.getStatus()

    def getTankTemperatur(self):
        return self.thermometer.getTemperature()  

    def setTankTemp(self,n):
        self.temperatureSetting=n

    def getTankTempSetting(self):
        return self.temperatureSetting 

    def temperatureFixed(self):
        self.warning='none'
        self.warned=False
       
#private methods   

    def log(message='',warning=''):
        pass

    
    async def run(self):
        lastMin=0
        while self.opperationStatus:
         #   print('tempThreads')
            t=time.localtime()
            
            temp=self.thermometer.getTemperature()
            if(self.heaterLock==False):
                if(temp<self.temperatureSetting):
                  self.heater.On()
                  self.log("heater turned on")
                else:
                    self.heater.Off()
                    self.log('heater turned off')
            if (temp-5)>self.temperatureSetting and not self.warned:
                self.warning='tank temperature is too low'
                self.emails.sendMessage(self.warning)
                self.log('problem',self.warning)
            elif (temp+5)<self.temperatureSetting and not self.warned:
                self.warning='tank temperature is too high'
                self.emails.sendMessage(self.warning)
                self.log('problem',self.warning)
            if not t[4]==lastMin:
                self.log()
                lastMin=t[4]
            time.sleep(1)