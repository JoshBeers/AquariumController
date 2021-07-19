from tkinter import * 
from equipment import *


backgroundColor = "grey"
forgroundColor = "black"
accentColor = "black"
panelHeight = 300
panelWidth = 220




class GUI:


    def __init__(self,callback, allstuff):
        self.root=Tk()
        self.root.geometry('1000x800')
        self.root.config(bg=backgroundColor)

        self.pumpSystem = allstuff[0]
        self.temperatureSystem = allstuff[1]
        self.atoSystem = allstuff[2]
        self.sensors = allstuff[3]

        self.onClosing = callback
        self.setup()

        self.root.protocol("WM_DELETE_WINDOW", self.onClose)
    
    def start(self):
        self.root.mainloop()

    def onClose(self):
        self.onClosing()
        self.root.destroy()

    def setup(self):
        self.pumpFrameSetup()
        self.setupATO()
        self.setupSensors()
        #pump area

    def pumpFrameSetup(self):
        #self.pumpSystem.callback = self.updatePumps
        frame=Frame(self.root,width=panelWidth,heigh=panelHeight,highlightbackground=forgroundColor,highlightthickness=1,bg=backgroundColor)
        frame.grid_propagate(0)
        frame.grid(row=0,column=0)

        mainLabel=Label(frame,text="Pump System",fg=forgroundColor,bg=backgroundColor)
        mainLabel.grid(row=0,columnspan=3)

        pSSL=Label(frame,text="Pump system Status: ",fg=forgroundColor,bg=backgroundColor,justify=RIGHT)
        pSSL.grid(row=1,column=0)
        self.pumpSystemState=Label(frame,text="{0}".format(self.pumpSystem.operationalStatus),fg=forgroundColor,bg=backgroundColor,justify=LEFT)
        self.pumpSystemState.grid(row=1,column=1)
        wL=Label(frame,text="warnings: ",fg=forgroundColor,bg=backgroundColor,justify=RIGHT)
        wL.grid(row=8,column=0)
        self.pumpSystemWarning=Label(frame,text="{0}".format(self.pumpSystem.warning),fg=forgroundColor,bg=backgroundColor,justify=LEFT)
        self.pumpSystemWarning.grid(row=8,columnspan=2,column=1)

        buttonWidth=13
        mPOnB=Button(frame,text="Pumps On",bg=backgroundColor,fg=forgroundColor,width=buttonWidth,command=self.pumpSystem.pumpTurnedOnByUser)
        mPOnB.grid(row=9,column=0)
        mPOffB=Button(frame,text="Pumps Off",bg=backgroundColor,fg=forgroundColor,width=buttonWidth,command=self.pumpSystem.pumpTurnedOffByUser)
        mPOffB.grid(row=9,column=1,columnspan=2)

        mPOnB=Button(frame,text="Pumps Normal",bg=backgroundColor,fg=forgroundColor,width=buttonWidth,command=self.pumpSystem.pumpsNorm)
        mPOnB.grid(row=10,column=0)

        sOnB=Button(frame,text="System On",bg=backgroundColor,fg=forgroundColor,width=buttonWidth,command=self.pumpSystem.On)
        sOnB.grid(row=12,column=0)
        
        sOffB=Button(frame,text="System Off",bg=backgroundColor,fg=forgroundColor,width=buttonWidth,command=self.pumpSystem.Off)
        sOffB.grid(row=12,column=1,columnspan=2)
    
    def updatePumps(self):
        self.pumpSystemWarning.config(text="{0}".format(self.pumpSystem.warning))
        self.pumpSystemState.config(text="{0}".format(self.pumpSystem.operationalStatus))
    
    def setupATO(self):
        self.atoSystem.callback  = self.updateATO
        bgC=backgroundColor
        fgC=forgroundColor
        buttonWidth=13
        bdC=forgroundColor
        frame=Frame(self.root,width=panelWidth,heigh=panelHeight,highlightbackground=bdC,highlightthickness=1,bg=bgC)
        frame.grid_propagate(0)
        frame.grid(row=0,column=3)

        mainLabel=Label(frame,text="ATO System",fg=fgC,bg=bgC)
        mainLabel.grid(row=0,columnspan=3)

        atoLabel =Label(frame,text="ATO system Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        atoLabel.grid(row=1,column=0)
        self.atoStatus=Label(frame,text="{0}".format(self.atoSystem.operationalStatus),fg=fgC,bg=bgC,justify=LEFT)
        self.atoStatus.grid(row=1,column=1)

        systemOnButton = Button(frame,text="System On",bg=bgC,fg=fgC,width=buttonWidth,command=lambda: self.atoSystem.on())
        systemOnButton.grid(row=5,column=0)

        systemOffButton = Button(frame,text="System Off",bg=bgC,fg=fgC,width=buttonWidth,command=lambda: self.atoSystem.Off())
        systemOffButton.grid(row=5,column=1) 

        atoPumpOnButton = Button(frame,text="ato pump on",bg=bgC,fg=fgC,width=buttonWidth,command=lambda: self.atoSystem.atoPumpOnFromUser(True))
        atoPumpOnButton.grid(row=6,column=0) 

        atoPumpOffButton = Button(frame,text="ato pump off",bg=bgC,fg=fgC,width=buttonWidth,command=lambda: self.atoSystem.atoPumpOnFromUser(False))
        atoPumpOffButton.grid(row=6,column=1) 

        atoPumpNormButton = Button(frame,text="ato pump Noramlize",bg=bgC,fg=fgC,width=buttonWidth,command=lambda: self.atoSystem.Noramlize())
        atoPumpNormButton.grid(row=7,column=0) 

    def updateATO(self):
        self.atoStatus.config(text="{0}".format(self.atoSystem.operationalStatus))

    def setupSensors(self):
        self.sensors.callback = self.updateSensors
        bgC=backgroundColor
        fgC=forgroundColor
        bdC=forgroundColor
        frame=Frame(self.root,width=panelWidth,heigh=panelHeight,highlightbackground=bdC,highlightthickness=1,bg=bgC)
        frame.grid_propagate(0)
        frame.grid(row=0,column=2)

        mainLabel=Label(frame,text="System equipment",fg=fgC,bg=bgC)
        mainLabel.grid(row=0,columnspan=3)

        pumpsLabel=Label(frame,text="pumos",fg=fgC,bg=bgC)
        pumpsLabel.grid(row=1,columnspan=3)

        mPSL=Label(frame,text="Tank Pumps Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        mPSL.grid(row=2,column=0)
        self.mPS=Label(frame,text="{0}".format(self.sensors.tankPumps.status),fg=fgC,bg=bgC,justify=LEFT)
        self.mPS.grid(row=2,column=1)

        tankPumpLockLabel=Label(frame,text="Tank Pumps locked: ",fg=fgC,bg=bgC,justify=RIGHT)
        tankPumpLockLabel.grid(row=3,column=0)
        self.tankPumpLock=Label(frame,text="{0}".format(self.sensors.tankPumps.lock),fg=fgC,bg=bgC,justify=LEFT)
        self.tankPumpLock.grid(row=3,column=1)

        atoPumpLabel=Label(frame,text="Ato Pumps Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        atoPumpLabel.grid(row=4,column=0)
        self.atoPumpStatus=Label(frame,text="{0}".format(self.sensors.atoPump.status),fg=fgC,bg=bgC,justify=LEFT)
        self.atoPumpStatus.grid(row=4,column=1)

        atoPumpLockLabel=Label(frame,text="sump Pumps locked: ",fg=fgC,bg=bgC,justify=RIGHT)
        atoPumpLockLabel.grid(row=5,column=0)
        self.atoPumpLock=Label(frame,text="{0}".format(self.sensors.atoPump.lock),fg=fgC,bg=bgC,justify=LEFT)
        self.atoPumpLock.grid(row=5,column=1)

        floatSensorLabel=Label(frame,text="Float sensors:",fg=fgC,bg=bgC)
        floatSensorLabel.grid(row=6,columnspan=3)

        tankFloatSensorLable=Label(frame,text="Tank float sensor Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        tankFloatSensorLable.grid(row=7,column=0)
        self.tankFloatSensorStatus=Label(frame,text="{0}".format(self.sensors.tankFloatSensor.level == 0),fg=fgC,bg=bgC,justify=LEFT)
        self.tankFloatSensorStatus.grid(row=7,column=1)

        sumpFloatSensorLabel=Label(frame,text="Sump float sensor Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        sumpFloatSensorLabel.grid(row=8,column=0)
        self.sumpFloatSensorStatus=Label(frame,text="{0}".format(self.sensors.sumpFloatSensor.level == 1),fg=fgC,bg=bgC,justify=LEFT)
        self.sumpFloatSensorStatus.grid(row=8,column=1)

        atoFloarSensorLabel=Label(frame,text="ato float sensor Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        atoFloarSensorLabel.grid(row=9,column=0)
        self.atoFloarSensorStatus=Label(frame,text="{0}".format(self.sensors.atoFloatSensor.level ==0),fg=fgC,bg=bgC,justify=LEFT)
        self.atoFloarSensorStatus.grid(row=9,column=1)

    def updateSensors(self):
        self.mPS.config(text="{0}".format(self.sensors.tankPumps.status))
        self.tankPumpLock.config(text="{0}".format(self.sensors.tankPumps.lock))
        self.atoPumpStatus.config(text="{0}".format(self.sensors.atoPump.status))
        self.atoPumpLock.config(text="{0}".format(self.sensors.atoPump.lock))
        self.tankFloatSensorStatus.config(text="{0}".format(self.sensors.tankFloatSensor.level == 0))
        self.sumpFloatSensorStatus.config(text="{0}".format(self.sensors.sumpFloatSensor.level == 1))
        self.atoFloarSensorStatus.config(text="{0}".format(self.sensors.atoFloatSensor.level == 0))

    def update(self):
        print('gui update')
        self.updatePumps()
        









