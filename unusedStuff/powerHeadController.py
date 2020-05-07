import powerhead as PH
import time as t
from threading import Thread
import schedule 





    



class powerheadController:

    def __init__(self,root="",GUIColors="",panelSize="",leftLocation=0,rightLocation=0):
        
        #creats the powerheads
        self.leftPowerhead=PH.powerhead(leftLocation)
        self.rightPoerhead=PH.powerhead(rightLocation)
        
        #instanciates the schedues for the powerheads
        self.leftPowerheadScheduleCurrent=schedule.schedule()
        self.rightPowerheadScheduleCurrent=schedule.schedule()
        
        self.leftSchedulePlace=0
        self.rightSchedulePlace=0
        self.lefPowerheadCurrent=False
        self.rightPowerheadCurrent=False

        #system variables
        self.opperationalStatus=False
        self.time=t.localtime() #3 for hour 4 for minute

        #sets up the thread
        self.thread=Thread()
        self.thread.start()
        self.thread.join()


#public methods
    def on(self):
        self.opperationalStatus=True
        self.thread=Thread(target=self.mainLoop)
        self.thread.start()
        self.updateGUI()
        

    def off(self):
        self.opperationalStatus=False
        self.leftPowerheadOff()
        self.rightPowerheadOff()
        self.thread.join()
        self.updateGUI()


    #powerhead public 
    def rightPowerheadOff(self):
        self.rightPoerhead.lock=False
        self.rightPoerhead.Off()
        self.rightPoerhead.lock=True
        self.updateGUI()

    def leftPowerheadOff(self):
        self.leftPowerhead.lock=False
        self.leftPowerhead.Off()
        self.leftPowerhead.lock=True
        self.updateGUI()
    
    def rightPowerHeadOn(self):
        self.rightPoerhead.lock=False
        self.rightPoerhead.On()
        self.rightPoerhead.lock=True
        self.updateGUI()

    def leftPowerheadOn(self):
        self.leftPowerhead.lock=False
        self.leftPowerhead.On()
        self.leftPowerhead.lock=True
        self.updateGUI()

    def leftPowerheadNormal(self):
        self.leftPowerhead.lock=False
        if self.lefPowerheadCurrent:
            self.leftPowerhead.On()
        else:
            self.leftPowerhead.Off()
        self.updateGUI()

    def rightPoerheadNormal(self):
        self.rightPoerhead.lock=False
        if self.rightPowerheadCurrent:
            self.rightPoerhead.On()
        else:
            self.rightPoerhead.Off()
        self.updateGUI()

    def setRightSchedule(self,s):
        self.rightPowerheadScheduleCurrent=s

    def setLeftSchedule(self,s):
        self.leftPowerheadScheduleCurrent=s


#private methods


    def mainLoop(self):
        self.leftPowerhead.lock=False
        self.rightPoerhead.lock=False
        self.updateGUI()
        while self.opperationalStatus:
            currentTime=t.localtime()

            #left powerhead stuff
            if self.leftPowerheadScheduleCurrent.getCurrentState([currentTime[3],currentTime[4]]):
                self.leftPowerhead.On()
                self.lefPowerheadCurrent=True
            else :
                self.leftPowerhead.Off()
                self.lefPowerheadCurrent=False

            #right powerhead stuff
            if self.rightPowerheadScheduleCurrent.getCurrentState([currentTime[3],currentTime[4]]):
                self.rightPoerhead.On()
                self.rightPowerheadCurrent=True
            else:
                self.rightPoerhead.Off()
                self.rightPowerheadCurrent=False
            self.updateGUI()
            t.sleep(60)
 
    




# GUI Stuff
    def updateGUI(self):
        print(self.leftPowerhead.getStatus(),"      ",self.rightPoerhead.getStatus())



        
phc=powerheadController()
rs=schedule.schedule()

        
