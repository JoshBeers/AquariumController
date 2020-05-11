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
        self.setupGUI()
    
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
        self.updateGui()


    def atoPumpOnFromUser(self,newStatus):
        self.atoPump.userAction(newStatus)
        self.updateGui()
    
    def Noramlize(self):
        self.atoPump.normalize()
        self.updateGui()

        

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
        self.updateGui()
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
        self.sumpLevelStatus=Label(frame,text="{0}".format(not self.sumpwaterLevelSensor.getLevel()),fg=fgC,bg=bgC,justify=LEFT)
        self.sumpLevelStatus.grid(row=2,column=1)

        atoResLabel = Label(frame,text="Ato res level status: ",fg=fgC,bg=bgC,justify=RIGHT)
        atoResLabel.grid(row=3,column=0)
        self.atoResStatus=Label(frame,text="{0}".format(not self.atoResSensor.getLevel()),fg=fgC,bg=bgC,justify=LEFT)
        self.atoResStatus.grid(row=3,column=1)

        atoPumpLabel = Label(frame,text="Ato pump level status: ",fg=fgC,bg=bgC,justify=RIGHT)
        atoPumpLabel.grid(row=4,column=0)
        self.atoPumpStatus=Label(frame,text="{0}".format(not self.atoPump.status),fg=fgC,bg=bgC,justify=LEFT)
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
        self.sumpLevelStatus.config(text="{0}".format(not self.sumpwaterLevelSensor.getLevel()))
        self.atoResStatus.config(text="{0}".format(not self.atoResSensor.getLevel()))
        self.atoPumpStatus.config(text="{0}".format(not self.atoPump.status))



        


    