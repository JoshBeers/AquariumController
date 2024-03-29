import time as t
import pump as p
import floatSensor as s
from tkinter import * 
from threading import Thread

class pumpController:
    def __init__(self,root,GUIcolors,pSize,em,logger,pumps,tankWaterLevelSenso,sumpwaterLevelSensor,atoResSensor):
        self.pumps=pumps
        self.opperationalStatus=False
        self.tankLevelSensor=tankWaterLevelSenso  # sensor in tank
        self.sumpLevelSensor=sumpwaterLevelSensor # sensor that tells if too little water in resivour\
        self.atoReserveSensor = atoResSensor

        self.logger = logger


        self.waterLevelTooLow=False
        self.warning='none'
        self.hasWarning=False
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
        self.updateGUI()
        self.log('system turned off')


    def pumpChangeUser(self, newStatus):
        self.pumps.userAction(newStatus)
        self.updateGUI()
        self.log('user turned pumps to {}'.format(newStatus))



    def pumpsNorm(self):
        self.pumps.normalize()
        if(not self.opperationalStatus):
            self.pumps.Off()
        self.updateGUI()
        self.log('user normalized pumps')


# private methods

    def log(self,mes= '',warning = ''):
        self.logger.pump(self.opperationalStatus,self.pumps.status,self.tankLevelSensor.getLevel(),self.sumpLevelSensor.getLevel(),mes,warning)



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
            self.updateGUI()
            t.sleep(1)





#gui 

    def settupGUI(self):
        root=self.root
        frame=self.frame
        bgC=self.bgC
        fgC=self.fgC
        bdC=self.bdC
        frame=Frame(root,width=self.pX,heigh=self.pY,highlightbackground=bdC,highlightthickness=1,bg=bgC)
        frame.grid_propagate(0)
        frame.grid(row=0,column=0)

        mainLabel=Label(frame,text="Pump System",fg=fgC,bg=bgC)
        mainLabel.grid(row=0,columnspan=3)

        pSSL=Label(frame,text="Pump system Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        pSSL.grid(row=1,column=0)
        self.pSS=Label(frame,text="{0}".format(self.opperationalStatus),fg=fgC,bg=bgC,justify=LEFT)
        self.pSS.grid(row=1,column=1)
        wL=Label(frame,text="warnings: ",fg=fgC,bg=bgC,justify=RIGHT)
        wL.grid(row=8,column=0)
        self.w=Label(frame,text="{0}".format(self.warning),fg=fgC,bg=bgC,justify=LEFT)
        self.w .grid(row=8,columnspan=2,column=1)

        buttonWidth=13
        mPOnB=Button(frame,text="Pumps On",bg=bgC,fg=fgC,width=buttonWidth,command=lambda: self.pumpChangeUser(True))
        mPOnB.grid(row=9,column=0)
        mPOffB=Button(frame,text="Pumps Off",bg=bgC,fg=fgC,width=buttonWidth,command=lambda: self.pumpChangeUser(False))
        mPOffB.grid(row=9,column=1,columnspan=2)

        mPOnB=Button(frame,text="Pumps Normal",bg=bgC,fg=fgC,width=buttonWidth,command=lambda: self.pumpsNorm())
        mPOnB.grid(row=10,column=0)


        sOnB=Button(frame,text="System On",bg=bgC,fg=fgC,width=buttonWidth,command=self.On)
        sOnB.grid(row=12,column=0)
        
        sOffB=Button(frame,text="System Off",bg=bgC,fg=fgC,width=buttonWidth,command=self.Off)
        sOffB.grid(row=12,column=1,columnspan=2)



    def updateGUI(self):
        self.pSS.config(text="{0}".format(self.opperationalStatus))



    







    




    