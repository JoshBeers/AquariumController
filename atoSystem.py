import time as t
import pump as p
import floatSensor as s
from tkinter import * 
from threading import Thread
import RPi.GPIO as gpio


class atoSystem:

    def __init__(self,root,GUIcolors,pSize,emailSystem,logger,sender,pumpFrequency,sumpwaterLevelSensor,atoResSensor):
        self.logger = logger

        self.atoPump=p.pump(pumpFrequency,sender)
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
        self.setupGUI()
    
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
        self.updateGui()
        self.log('system stopped')


    def atoPumpOnFromUser(self,newStatus):
        self.atoPump.userAction(newStatus)
        self.updateGui()
        self.log('pump {} from user'.format(newStatus))
    
    def Noramlize(self):
        self.atoPump.normalize()
        self.updateGui()
        self.log('pump normalized')

        

    '''
        rules:
            if res is low water doesnt pump
            if tank is low water pumped
    '''

    def log(self,message= '',warning=''):
        self.logger.ato(self.opperationalStatus,self.sumpwaterLevelSensor.getLevel(),self.atoResSensor.getLevel(),message,warning)
        

    def run(self):
        self.atoPump.lock=False
        self.opperationalStatus=True
        t.sleep(1)
        sleepTime = 1
        self.updateGui()
        tempForPumpOn = 0
        while self.opperationalStatus:
            #print(self.atoPump.status)
            #if sump level low and res has water
            if(self.sumpwaterLevelSensor.getLevel() == 0 and self.atoResSensor.getLevel() == 0):
                if(tempForPumpOn%50 == 0):
                    self.atoPump.On()
                    #print('pump on from ato temp var = {0} and temp%50={1}'.format(tempForPumpOn,tempForPumpOn%50))
                self.log('pump turned on')
                sleepTime = .1
                tempForPumpOn = tempForPumpOn+1
                #print("Test1")
            #if res needs refilled
            elif self.atoResSensor.getLevel() == 1:
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
            self.updateGui()
            t.sleep(sleepTime)


    #gui stuff

    def setupGUI(self):
        root=self.root
        frame=self.frame
        bgC=self.bgC
        fgC=self.fgC
        buttonWidth=13
        bdC=self.bdC
        frame=Frame(root,width=self.pX,heigh=self.pY,highlightbackground=bdC,highlightthickness=1,bg=bgC)
        frame.grid_propagate(0)
        frame.grid(row=0,column=3)

        mainLabel=Label(frame,text="ATO System",fg=fgC,bg=bgC)
        mainLabel.grid(row=0,columnspan=3)

        atoLabel =Label(frame,text="ATO system Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        atoLabel.grid(row=1,column=0)
        self.atoStatus=Label(frame,text="{0}".format(self.opperationalStatus),fg=fgC,bg=bgC,justify=LEFT)
        self.atoStatus.grid(row=1,column=1)

        sumpLevelLabel = Label(frame,text="sump level status: ",fg=fgC,bg=bgC,justify=RIGHT)
        sumpLevelLabel.grid(row=2,column=0)
        self.sumpLevelStatus=Label(frame,text="{0}".format(self.sumpwaterLevelSensor.getLevel()),fg=fgC,bg=bgC,justify=LEFT)
        self.sumpLevelStatus.grid(row=2,column=1)

        atoResLabel = Label(frame,text="Ato res needs filled: ",fg=fgC,bg=bgC,justify=RIGHT)
        atoResLabel.grid(row=3,column=0)
        self.atoResStatus=Label(frame,text="{0}".format(self.atoResSensor.getLevel()),fg=fgC,bg=bgC,justify=LEFT)
        self.atoResStatus.grid(row=3,column=1)

        atoPumpLabel = Label(frame,text="Ato pump status: ",fg=fgC,bg=bgC,justify=RIGHT)
        atoPumpLabel.grid(row=4,column=0)
        self.atoPumpStatus=Label(frame,text="{0}".format(self.atoPump.status),fg=fgC,bg=bgC,justify=LEFT)
        self.atoPumpStatus.grid(row=4,column=1)

        systemOnButton = Button(frame,text="System On",bg=bgC,fg=fgC,width=buttonWidth,command=lambda: self.on())
        systemOnButton.grid(row=5,column=0)

        systemOffButton = Button(frame,text="System Off",bg=bgC,fg=fgC,width=buttonWidth,command=lambda: self.Off())
        systemOffButton.grid(row=5,column=1) 

        atoPumpOnButton = Button(frame,text="ato pump on",bg=bgC,fg=fgC,width=buttonWidth,command=lambda: self.atoPumpOnFromUser(True))
        atoPumpOnButton.grid(row=6,column=0) 

        atoPumpOffButton = Button(frame,text="ato pump off",bg=bgC,fg=fgC,width=buttonWidth,command=lambda: self.atoPumpOnFromUser(False))
        atoPumpOffButton.grid(row=6,column=1) 

        atoPumpNormButton = Button(frame,text="ato pump Noramlize",bg=bgC,fg=fgC,width=buttonWidth,command=lambda: self.Noramlize())
        atoPumpNormButton.grid(row=7,column=0) 





    
    def updateGui(self):
        self.atoStatus.config(text="{0}".format(self.opperationalStatus))
        self.sumpLevelStatus.config(text="{0}".format(self.sumpwaterLevelSensor.getLevel()))
        self.atoResStatus.config(text="{0}".format(self.atoResSensor.getLevel()))
        self.atoPumpStatus.config(text="{0}".format(self.atoPump.status))



        


    