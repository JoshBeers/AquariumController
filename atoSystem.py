import time as t
import pump as p
import floatSensor as s
from tkinter import * 
from threading import Thread

class atoSystem:

    def __init__(self,root,GUIcolors,pSize,emailSystem,pumpFrequency=[17,18],sumpwaterLevelSensor=3,atoResSensor = 4):

        self.atoPump=p.pump(pumpFrequency)
        self.sumpwaterLevelSensor = s.floatSensor(sumpwaterLevelSensor)
        self.atoResSensor = s.floatSensor(atoResSensor)

        self.opperationalStatus=False

        self.warning = ""
        self.needsWater = False

        self.emailSystem  = emailSystem
        self.pX=pSize[0]
        self.pY=pSize[1]
        self.root=root
        self.bgC=GUIcolors[0]
        self.fgC=GUIcolors[1]
        self.bdC=GUIcolors[2]
        self.frame=Frame()
        self.t=Thread()
        self.t.start()
        self.t.join()


    def on(self) :
        self.t=Thread(target=self.run)
        self.t.start()

    def Off(self):
        self.opperationalStatus=False
        self.atoPump.lock=False
        self.atoPump.Off()
        self.updateGUI()

    '''
        rules:
            if res is low water doesnt pump
            if tank is low water pumped
    '''

    def run(self):
        self.atoPump.lock=False
        self.opperationalStatus=True
        t.sleep(1)
        sleepTime = 300
        while self.opperationalStatus:
            #if suimp level low and res has water
            if(self.sumpwaterLevelSensor and self.atoResSensor):
                sleepTime = .1
                self.atoPump.On()
            elif not self.atoResSensor:
                if not self.needsWater:
                    self.emailSystem.sendMessage("ato res needs water")
                self.needsWater = True
                self.atoPump.Off()
                self.opperationalStatus = False
            else:
               self.atoPump.Off()
               sleepTime = 300
            t.sleep(sleepTime)


    #gui stuff

    def setupGUI(self):
        return
    
    def updateGui(self):
        return 

        


    