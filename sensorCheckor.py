import pump
import floatSensor
import time
from threading import Thread

class sensorCheckor:

    def __init__(self,root,GUIcolors,pSize,tankPumps, atoPump, tankFloatSensor, sumpFloatSensor, atoFloarSensor):

        self.tankFloatSensor = tankFloatSensor
        self.sumpFloatSensor = sumpFloatSensor
        self.atoFloatSensor = atoFloarSensor

        self.tankPumps = tankPumps
        self.atoPump = atoPump

        self.pX=pSize[0]
        self.pY=pSize[1]
        self.root=root
        self.bgC=GUIcolors[0]
        self.fgC=GUIcolors[1]
        self.bdC=GUIcolors[2]
        self.frame=Frame()
        self.settupGUI()

        #need to setup run method
        self.t=Thread(target=self.run)
        self.t.start()
        self.opporationalStatus = False

    def stop(self):
        self.opporationalStatus = False



    def run(self):
        self.opporationalStatus = True
        while( self.opporationalStatus = True):
            self.tankFloatSensor.getLevel()
            self.sumpFloatSensor.getLevel()
            self.atoFloatSensor.getLevel()
            self.updateGUI()

    def updateGUI(self):
        self.mPS.config(text="{0}".format(self.tankPumps.status))
        self.tankPumpLock.config(text="{0}".format(self.tankPumps.lock))
        self.atoPumpStatus.config(text="{0}".format(self.atoPump.status))
        self.atoPumpLock.config(text="{0}".format(self.atoPump.lock))
        self.tankFloatSensorStatus.config(text="{0}".format(self.tankFloatSensor.level))
        self.sumpFloatSensorStatus.config(text="{0}".format(self.sumpFloatSensor.level))
        self.atoFloarSensorStatus.config(text="{0}".format(self.atoFloatSensor.level))







    def setupUI(self):
        root=self.root
        frame=self.frame
        bgC=self.bgC
        fgC=self.fgC
        bdC=self.bdC
        frame=Frame(root,width=self.pX,heigh=self.pY,highlightbackground=bdC,highlightthickness=1,bg=bgC)
        frame.grid_propagate(0)
        frame.grid(row=1,column=0)

        mainLabel=Label(frame,text="System equipment",fg=fgC,bg=bgC)
        mainLabel.grid(row=0,columnspan=3)

        pumpsLabel=Label(frame,text="pumos",fg=fgC,bg=bgC)
        pumpsLabel.grid(row=1,columnspan=3)

        mPSL=Label(frame,text="Tank Pumps Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        mPSL.grid(row=2,column=0)
        self.mPS=Label(frame,text="{0}".format(self.tankPumps.status),fg=fgC,bg=bgC,justify=LEFT)
        self.mPS.grid(row=2,column=1)

        tankPumpLockLabel=Label(frame,text="Tank Pumps locked: ",fg=fgC,bg=bgC,justify=RIGHT)
        tankPumpLockLabel.grid(row=3,column=0)
        self.tankPumpLock=Label(frame,text="{0}".format(self.tankPumps.lock),fg=fgC,bg=bgC,justify=LEFT)
        self.tankPumpLock.grid(row=3,column=1)

        atoPumpLabel=Label(frame,text="Ato Pumps Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        atoPumpLabel.grid(row=4,column=0)
        self.atoPumpStatus=Label(frame,text="{0}".format(self.atoPump.status),fg=fgC,bg=bgC,justify=LEFT)
        self.atoPumpStatus.grid(row=4,column=1)

        atoPumpLockLabel=Label(frame,text="sump Pumps locked: ",fg=fgC,bg=bgC,justify=RIGHT)
        atoPumpLockLabel.grid(row=5,column=0)
        self.atoPumpLock=Label(frame,text="{0}".format(self.atoPump.lock),fg=fgC,bg=bgC,justify=LEFT)
        self.atoPumpLock.grid(row=5,column=1)

        floatSensorLabel=Label(frame,text="Float sensors:",fg=fgC,bg=bgC)
        floatSensorLabel.grid(row=6,columnspan=3)

        tankFloatSensorLable=Label(frame,text="Tank float sensor Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        tankFloatSensorLable.grid(row=7,column=0)
        self.tankFloatSensorStatus=Label(frame,text="{0}".format(self.tankFloatSensor.level),fg=fgC,bg=bgC,justify=LEFT)
        self.tankFloatSensorStatus.grid(row=7,column=1)

        sumpFloatSensorLabel=Label(frame,text="Sump float sensor Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        sumpFloatSensorLabel.grid(row=8,column=0)
        self.sumpFloatSensorStatus=Label(frame,text="{0}".format(self.sumpFloatSensor.level),fg=fgC,bg=bgC,justify=LEFT)
        self.sumpFloatSensorStatus.grid(row=8,column=1)

        atoFloarSensorLabel=Label(frame,text="ato float sensor Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        atoFloarSensorLabel.grid(row=9,column=0)
        self.atoFloarSensorStatus=Label(frame,text="{0}".format(self.atoFloatSensor.level),fg=fgC,bg=bgC,justify=LEFT)
        self.atoFloarSensorStatus.grid(row=9,column=1)