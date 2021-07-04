import time as t
from equipment import pump as p
from equipment import floatSensor as s
from tkinter import * 
from threading import Thread












class pumpController:
    def __init__(self,em,pumps,tankWaterLevelSenso,sumpwaterLevelSensor,atoResSensor):
        self.pumps=pumps
        self.opperationalStatus=False
        self.tankLevelSensor=tankWaterLevelSenso  # sensor in tank
        self.sumpLevelSensor=sumpwaterLevelSensor # sensor that tells if too little water in resivour\
        self.atoReserveSensor = atoResSensor


        self.waterLevelTooLow=False
        self.warning='none'
        self.hasWarning=False

        '''
        self.pX=pSize[0]
        self.pY=pSize[1]
        self.root=root
        self.bgC=GUIcolors[0]
        self.fgC=GUIcolors[1]
        self.bdC=GUIcolors[2]
        self.frame=Frame()
        self.settupGUI()
        self.t=Thread()
        self.t.start()
        self.t.join()
        self.emailSystem=em
'''

        
#public methods

    def On(self): 
        self.t=Thread(target=self.run)
        self.t.start()
        self.log('system turned on')
        

    def Off(self):
        self.opperationalStatus=False
        self.pumps.lock=False
        self.pumps.Off()
        t.sleep(.1)
        self.pumps.Off()
        t.sleep(.1)
        self.pumps.Off()
        self.log('system turned off')


    def pumpChangeUser(self, newStatus):
        self.pumps.userAction(newStatus)
        self.log('user turned pumps to {}'.format(newStatus))



    def pumpsNorm(self):
        self.pumps.normalize()
        if(not self.opperationalStatus):
            self.pumps.Off()
        self.log('user normalized pumps')


# private methods

    def log(self,mes= '',warning = ''):
        pass
       # self.logger.pump(self.opperationalStatus,self.pumps.status,self.tankLevelSensor.getLevel(),self.sumpLevelSensor.getLevel(),mes,warning)



    '''
        rules:
            pumps are off till reset if:
                tankWaterLevel goes too high
                sumpwaterLevel goes too low and ato res is too low
            if user controls pump it is locked till normalized
    '''

    def run(self):
        self.hasWarning=True
        self.warning='none'
        #self.pumps.normalize()
        self.pumps.lock = False
        self.opperationalStatus=True
        t.sleep(.1)
        self.pumps.On()
        tempForPumpOn = 0
        while self.opperationalStatus:
            #checks the sump and ato res if bad turn off system and locks pumps off  or if the tank is over full
           # print(self.tankLevelSensor.getLevel())
            sumpSensor = self.sumpLevelSensor.level
            atoSensor = self.atoReserveSensor.level
            tankSensor = self.tankLevelSensor.level

            if (sumpSensor==0 and atoSensor == 1) or (tankSensor==1):
                #print("something is wrong")
                self.pumps.lock = False
                self.pumps.Off()
                t.sleep(.34)
                self.pumps.Off()
                t.sleep(.56)
                self.pumps.Off()
                self.pumpsCach=False
                self.pumps.lock=True
                self.opperationalStatus=False
                self.warning='sump too low, ato is empty'
                if tankSensor == 1:
                    self.warning='tank high'
                try:
                    self.emailSystem.sendMessage(self.warning)
                except:
                    self.log('error in email system')
                self.hasWarning=True
                self.log('',self.warning)
                #if everything is ok it turns the pumps on
            else:
                if(tempForPumpOn%10 ==0):
                    self.pumps.On()
                    #print('pumps on from pump Controller')
                self.pumpsCach=True
                tempForPumpOn+=1
                #print("it is on")
            t.sleep(1)










    




    