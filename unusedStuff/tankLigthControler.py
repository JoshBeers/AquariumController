import light as l
import time as t
from tkinter import * 
from threading import Thread
import string
import os


class lightControler:
    

    def __init__(self,root,GUIcolors,pSize,ll=19,rl=26,sl=18):
        self.rightLight=l.light(rl)
        self.leftLight=l.light(ll)
        self.sumpLight=l.light(sl)
        self.rightLightSchedule=[[0,0,False]]
        self.leftLightSchedule=[[0,0,False]]
        self.sumpLightSchedule=[[0,0,False]]
        self.opperationStatus=False
        self.time=t.localtime() #3 for hour 4 for minute
        self.leftSchedulePlace=0
        self.rightSchedulePlace=0
        self.sumpSchedulePlace=0
        self.thread=Thread()
        self.thread.start()
        self.thread.join()

        self.rLC=False
        self.lLC=False
        self.sLC=False

        #gui stuff
        self.pX=pSize[0]
        self.pY=pSize[1]
        self.root=root
        self.bgC=GUIcolors[0]
        self.fgC=GUIcolors[1]
        self.bdC=GUIcolors[2]
        self.frame=Frame()
        self.settupGUI()

        self.setupSecondGUI()
        self.control=''
        
        self.currentProfile=0
        self.settupProfileGUI()
        

        

#public methods
    def On(self): 
        self.opperationStatus=True
        self.thread=Thread(target=self.mainProgram)
        self.thread.start()
        self.updateGUI()

    def Off(self):  
        self.opperationStatus=False
        self.rightLightOff()
        self.leftLightOff()
        self.sumpLightOff()
        self.thread.join()
        self.updateGUI()

    def rightLightOn(self):
        self.rightLight.lock=False
        self.rightLight.On()
        self.rightLight.lock=True
        self.updateGUI()

    def leftLightOn(self):
        self.leftLight.lock=False
        self.leftLight.On()
        self.leftLight.lock=True
        self.updateGUI()

    def sumpLightOn(self):
        self.sumpLight.lock=False
        self.sumpLight.On()
        self.sumpLight.lock=True
        self.updateGUI()

    def rightLightOff(self):
        self.rightLight.lock=False
        self.rightLight.Off()
        self.rightLight.lock=True
        self.updateGUI()

    def leftLightOff(self):
        self.leftLight.lock=False
        self.leftLight.Off()
        self.leftLight.lock=True
        self.updateGUI()

    def sumpLightOff(self):
        self.sumpLight.lock=False
        self.sumpLight.Off()
        self.sumpLight.lock=True
        self.updateGUI()

    def rightLightNormal(self):
        self.rightLight.lock=False
        if self.rLC:
            self.rightLight.On()
        else:
            self.rightLight.Off()
        self.updateGUI()

    def leftLightNormal(self):
        self.leftLight.lock=False
        if self.lLC:
            self.leftLight.On()
        else:
            self.leftLight.Off()
        self.updateGUI()

    def sumpLightNormal(self):
        self.sumpLight.lock=False
        if self.sLC:
            self.sumpLight.On()
        else:
            self.sumpLight.Off()
        self.updateGUI()

    def setLeftLightSchedule(self,sch):
        self.leftLightSchedule=sch
        self.findLeftNext()
        self.updateGUI()

    def setRightLightSchedule(self,sch):
        self.rightLightSchedule=sch
        self.findRightNext()
        self.updateGUI()

    def setSumpLightSchedule(self,sch):
        self.sumpLightSchedule=sch
        self.findSumpNext()
        self.updateGUI()

    def getLeftLightSchedule(self):
        return self.leftLightSchedule

    def getRightLightSchedule(self):
        return self.rightLightSchedule

    def getSumpLightSchedule(self):
        return self.sumpLightSchedule

#private methods



    def findLeftNext(self):
        if len(self.leftLightSchedule)==0:
            self.leftSchedulePlace=0
            return
        self.updateTime()
        self.leftSchedulePlace=0
        lastPositon=len(self.leftLightSchedule)-1
        if(self.leftLightSchedule[lastPositon][0]<self.time[3] and self.leftLightSchedule[lastPositon][1]>self.time[4]):
            self.leftSchedulePlace=0
        else:
            b=True
            i=0
            while b and i<=lastPositon:
            
                if(self.leftLightSchedule[i][0]==self.time[3] and self.leftLightSchedule[i][1]>self.time[4]):
                    self.leftSchedulePlace=i
                    b=False
                elif(self.leftLightSchedule[i][0]>self.time[3]):
                    self.leftSchedulePlace=(i)
                    b=False
                else:
                    i=i+1

        if self.leftSchedulePlace==0:
            if self.leftLightSchedule[lastPositon][2]:
                self.leftLight.On()
                self.lLC=True
            else:
                self.leftLight.Off()
                self.lLC=False
        else:
            if self.leftLightSchedule[self.leftSchedulePlace-1][2]:
                self.leftLight.On()
                self.lLC=True
            else:
                self.leftLight.Off()
                self.lLC=False
        
    def findRightNext(self):
        if len(self.rightLightSchedule)==0:
            self.rightSchedulePlace=0
            return
        self.updateTime()
        self.rightSchedulePlace=0
        lastPositon=len(self.rightLightSchedule)-1
        if(self.rightLightSchedule[lastPositon][0]<self.time[3] and self.rightLightSchedule[lastPositon][1]>self.time[4]):
            self.rightSchedulePlace=0
        else:
            b=True
            i=0
            while b and i<=lastPositon:
            
                if(self.rightLightSchedule[i][0]==self.time[3] and self.rightLightSchedule[i][1]>self.time[4]):
                    self.rightSchedulePlace=i
                    b=False
                elif(self.rightLightSchedule[i][0]>self.time[3]):
                    self.rightSchedulePlace=(i)
                    b=False
                else:
                    i=i+1

        if self.rightSchedulePlace==0:
            if self.rightLightSchedule[lastPositon][2]:
                self.rightLight.On()
                self.rLC=True
            else:
                self.rightLight.Off()
                self.rLC=False
        else:
            if self.rightLightSchedule[self.rightSchedulePlace-1][2]:
                self.rightLight.On()
                self.rLC=True
            else:
                self.rightLight.Off()
                self.rLC=False

    def findSumpNext(self):
        if len(self.sumpLightSchedule)==0:
            self.sumpSchedulePlace=0
            return
        self.updateTime()
        self.sumpSchedulePlace=0
        lastPositon=len(self.sumpLightSchedule)-1
        if(self.sumpLightSchedule[lastPositon][0]<self.time[3] and self.sumpLightSchedule[lastPositon][1]>self.time[4]):
            self.sumpSchedulePlace=0
        else:
            
            b=True
            i=0
            while b and i<=lastPositon:
            
                if(self.sumpLightSchedule[i][0]==self.time[3] and self.sumpLightSchedule[i][1]>self.time[4]):
                    self.sumpSchedulePlace=i
                    b=False
                elif(self.sumpLightSchedule[i][0]>self.time[3]):
                    self.sumpSchedulePlace=(i)
                    b=False
                else:
                    i=i+1

        if self.sumpSchedulePlace==0:
            if self.sumpLightSchedule[lastPositon][2]:
                self.sumpLight.On()
                self.sLC=True
            else:
                self.rightLight.Off()
                self.sLC=False
        else:
            if self.sumpLightSchedule[self.rightSchedulePlace-1][2]:
                self.sumpLight.On()
                self.sLC=True
            else:
                self.rightLight.Off()
                self.sLC=False

        

    def updateTime(self):
        self.time=t.localtime()

    def mainProgram(self):
        self.findLeftNext()
        self.findRightNext()
        self.findSumpNext()
        self.rightLight.lock=False
        self.leftLight.lock=False
        self.sumpLight.lock=False
        while self.opperationStatus:
            self.updateTime()
            #for left light
            try:
                if(self.time[3]==self.leftLightSchedule[self.leftSchedulePlace][0] and self.time[4]==self.leftLightSchedule[self.leftSchedulePlace][1]):
                    if(self.leftLightSchedule[self.leftSchedulePlace][2]==True):
                        self.leftLight.On()
                        self.lLC=True
                    else:
                        self.leftLight.Off()
                        self.lLC=False
                    if(self.leftSchedulePlace==len(self.leftLightSchedule)-1):
                        self.leftSchedulePlace=0
                    else:
                        self.leftSchedulePlace+=1
            except:
                pass
            
            #for right light
            try:
                if(self.time[3]==self.rightLightSchedule[self.rightSchedulePlace][0] and self.time[4]==self.rightLightSchedule[self.rightSchedulePlace][1]):
                    if(self.rightLightSchedule[self.rightSchedulePlace][2]==True):
                        self.rightLight.On()
                        self.rLC=True
                    else:
                        self.rightLight.Off()
                        self.rLC=False
                    if(self.rightSchedulePlace==len(self.rightLightSchedule)-1):
                        self.rightSchedulePlace=0
                    else:
                        self.rightSchedulePlace+=1
            except:
                pass

            #for sump light
            try:
                if(self.time[3]==self.sumpLightSchedule[self.sumpSchedulePlace][0] and self.time[4]==self.sumpLightSchedule[self.sumpSchedulePlace][1]):
                    if(self.sumpLightSchedule[self.sumpSchedulePlace][2]==True):
                        self.sumpLight.On()
                        self.sLC=True
                    else:
                        self.sumpLight.Off()
                        self.sLC=False
                    if(self.sumpSchedulePlace==len(self.sumpLightSchedule)-1):
                        self.sumpSchedulePlace=0
                    else:
                        self.sumpSchedulePlace+=1  
            except:
                pass
            self.updateGUI()          
            t.sleep(1)

#Gui methods

    def settupGUI(self):
        root=self.root
        frame=self.frame
        bgC=self.bgC
        fgC=self.fgC
        bdC=self.bdC
        frame=Frame(root,width=self.pX,heigh=self.pY,highlightbackground=bdC,highlightthickness=1,bg=bgC)
        frame.grid_propagate(0)
        frame.grid(row=0,column=1)   

        mainLabel=Label(frame,text="Light System",fg=fgC,bg=bgC)
        mainLabel.grid(row=0,columnspan=3)

        lSSL=Label(frame,text="Light system Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        lSSL.grid(row=1,column=0)
        self.lSS=Label(frame,text="{0}".format(self.opperationStatus),fg=fgC,bg=bgC,justify=LEFT)
        self.lSS.grid(row=1,column=1)      

        rLSL=Label(frame,text="right Light Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        rLSL.grid(row=2,column=0)
        self.rLS=Label(frame,text="{0}".format(self.rightLight.status),fg=fgC,bg=bgC,justify=LEFT)
        self.rLS.grid(row=2,column=1)

        lLSL=Label(frame,text="left light Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        lLSL.grid(row=3,column=0)
        self.lLS=Label(frame,text="{0}".format(self.leftLight.status),fg=fgC,bg=bgC,justify=LEFT)
        self.lLS.grid(row=3,column=1)

        tLSL=Label(frame,text="sump light Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        tLSL.grid(row=4,column=0)
        self.tLS=Label(frame,text="{0}".format(self.sumpLight.status),fg=fgC,bg=bgC,justify=LEFT)
        self.tLS .grid(row=4,column=1)

        rLLSL=Label(frame,text="right light locked: ",fg=fgC,bg=bgC,justify=RIGHT)
        rLLSL.grid(row=5,column=0)
        self.rLLS=Label(frame,text="{0}".format(self.rightLight.lock),fg=fgC,bg=bgC,justify=LEFT)
        self.rLLS .grid(row=5,column=1)

        lLLSL=Label(frame,text="left light locked: ",fg=fgC,bg=bgC,justify=RIGHT)
        lLLSL.grid(row=6,column=0)
        self.lLLS=Label(frame,text="{0}".format(self.leftLight.lock),fg=fgC,bg=bgC,justify=LEFT)
        self.lLLS .grid(row=6,column=1)

        sLLSL=Label(frame,text="sump light locked: ",fg=fgC,bg=bgC,justify=RIGHT)
        sLLSL.grid(row=7,column=0)
        self.sLLS=Label(frame,text="{0}".format(self.sumpLight.lock),fg=fgC,bg=bgC,justify=LEFT)
        self.sLLS .grid(row=7,column=1)

        if len(self.rightLightSchedule):
            texted=self.rightLightSchedule[self.rightSchedulePlace][0],":",self.rightLightSchedule[self.rightSchedulePlace][1],"-",self.rightLightSchedule[self.rightSchedulePlace][2]
        RNEL=Label(frame,text="next right event: ",fg=fgC,bg=bgC,justify=RIGHT)
        RNEL.grid(row=8,column=0)
        texted="no events"
        self.RNE=Label(frame,text=texted,fg=fgC,bg=bgC,justify=LEFT)
        self.RNE.grid(row=8,column=1,columnspan=2)

        lNEL=Label(frame,text="next left event: ",fg=fgC,bg=bgC,justify=RIGHT)
        lNEL.grid(row=9,column=0)
        if len(self.leftLightSchedule):
            texted=self.leftLightSchedule[self.leftSchedulePlace][0],":",self.leftLightSchedule[self.leftSchedulePlace][1],"-",self.leftLightSchedule[self.leftSchedulePlace][2]
        texted="no events"
        self.lNE=Label(frame,text=texted,fg=fgC,bg=bgC,justify=LEFT)
        self.lNE.grid(row=9,column=1,columnspan=2)

        sNEL=Label(frame,text="next sump event: ",fg=fgC,bg=bgC,justify=RIGHT)
        sNEL.grid(row=10,column=0)
        if len(self.sumpLightSchedule):
            texted=self.sumpLightSchedule[self.sumpSchedulePlace][0],":",self.sumpLightSchedule[self.sumpSchedulePlace][1],"-",self.sumpLightSchedule[self.sumpSchedulePlace][2]
        texted="no events"
        self.sNE=Label(frame,text=texted,fg=fgC,bg=bgC,justify=LEFT)
        self.sNE.grid(row=10,column=1,columnspan=2)

        buttonWidth=10
        rLOnB=Button(frame,text="Right light no",bg=bgC,fg=fgC,command=self.rightLightOn,width=buttonWidth)
        rLOnB.grid(row=11,column=0)

        rLOffB=Button(frame,text="Right light off",bg=bgC,fg=fgC,command=self.rightLightOff,width=buttonWidth)
        rLOffB.grid(row=11,column=1, columnspan=2)

        lLOnB=Button(frame,text="left light no",bg=bgC,fg=fgC,command=self.leftLightOn,width=buttonWidth)
        lLOnB.grid(row=12,column=0)

        lLOffB=Button(frame,text="left light off",bg=bgC,fg=fgC,command=self.leftLightOff,width=buttonWidth)
        lLOffB.grid(row=12,column=1, columnspan=2)

        rBNor=Button(frame,text="right normal",bg=bgC,fg=fgC,command=self.rightLightNormal,width=buttonWidth)
        rBNor.grid(row=13,column=0)

        lLNorm=Button(frame,text="left normal",bg=bgC,fg=fgC,command=self.leftLightNormal,width=buttonWidth)
        lLNorm.grid(row=13,column=1, columnspan=2)

        sLOn=Button(frame,text="Sump on",bg=bgC,fg=fgC,command=self.sumpLightOn,width=buttonWidth)
        sLOn.grid(row=14,column=0)

        sLOff=Button(frame,text="Sump off",bg=bgC,fg=fgC,command=self.sumpLightOff,width=buttonWidth)
        sLOff.grid(row=14,column=1, columnspan=2)

        sLNorm=Button(frame,text="Sump Norm",bg=bgC,fg=fgC,command=self.sumpLightNormal,width=buttonWidth)
        sLNorm.grid(row=15,column=0)

        sOn=Button(frame,text="system on",bg=bgC,fg=fgC,command=self.On,width=buttonWidth)
        sOn.grid(row=16,column=0)

        sOff=Button(frame,text="system off",bg=bgC,fg=fgC,command=self.Off,width=buttonWidth)
        sOff.grid(row=16,column=1, columnspan=2)







    def updateGUI(self):#
        self.lSS.config(text="{0}".format(self.opperationStatus))
        self.rLS.config(text="{0}".format(self.rightLight.status))
        self.lLS.config(text="{0}".format(self.leftLight.status))
        self.tLS.config(text="{0}".format(self.sumpLight.status))
        self.rLLS.config(text="{0}".format(self.rightLight.lock))
        self.lLLS.config(text="{0}".format(self.leftLight.lock))
        self.sLLS.config(text="{0}".format(self.sumpLight.lock))
        texted="no items"
        if len(self.rightLightSchedule):
            texted=self.rightLightSchedule[self.rightSchedulePlace][0],":",self.rightLightSchedule[self.rightSchedulePlace][1],"-",self.rightLightSchedule[self.rightSchedulePlace][2]
        self.RNE.config(text=texted)
        texted="no items"
        if len(self.leftLightSchedule):
            texted=self.leftLightSchedule[self.leftSchedulePlace][0],":",self.leftLightSchedule[self.leftSchedulePlace][1],"-",self.leftLightSchedule[self.leftSchedulePlace][2]
        self.lNE.config(text=texted)
        texted="no items"
        if len(self.sumpLightSchedule):
            texted=self.sumpLightSchedule[self.sumpSchedulePlace][0],":",self.sumpLightSchedule[self.sumpSchedulePlace][1],"-",self.sumpLightSchedule[self.sumpSchedulePlace][2]
        self.sNE.config(text=texted)

#scheduling gui

    def rightLightScheduleButton(self):
        self.control='r'
        self.clearList()
        n=len(self.rightLightSchedule)
        if len(self.rightLightSchedule)>len(self.display):
            n=len(self.display)
        for i in range(n):
            self.display[i].config(text="{0}:{1} {2}".format(self.rightLightSchedule[i][0],self.rightLightSchedule[i][1],self.rightLightSchedule[i][2]))
            self.boxesVariables.append(IntVar())
            self.checkBoxes.append(Checkbutton(self.frame,text="",bg=self.bgC,fg=self.fgC,variable=self.boxesVariables[i]))
            self.checkBoxes[i].grid(row=i+2,column=2)
        self.updateProfile()

    def leftLightScheduleButton(self):
        self.control='l'
        self.clearList()
        n=len(self.leftLightSchedule)
        if len(self.leftLightSchedule)>len(self.display):
            n=len(self.display)
        for i in range(n):
            self.display[i].config(text="{0}:{1} {2}".format(self.leftLightSchedule[i][0],self.leftLightSchedule[i][1],self.leftLightSchedule[i][2]))
            self.boxesVariables.append(IntVar())
            self.checkBoxes.append(Checkbutton(self.frame,text="",bg=self.bgC,fg=self.fgC,variable=self.boxesVariables[i]))
            self.checkBoxes[i].grid(row=i+2,column=2)
        self.updateProfile()

    def sumpLightScheduleButton(self):
        self.control='s'
        self.clearList()
        n=len(self.sumpLightSchedule)
        if len(self.sumpLightSchedule)>len(self.display):
            n=len(self.display)
        for i in range(n):
            self.display[i].config(text="{0}:{1} {2}".format(self.sumpLightSchedule[i][0],self.sumpLightSchedule[i][1],self.sumpLightSchedule[i][2]))
            self.boxesVariables.append(IntVar())
            self.checkBoxes.append(Checkbutton(self.frame,text="",bg=self.bgC,fg=self.fgC,variable=self.boxesVariables[i]))
            self.checkBoxes[i].grid(row=i+2,column=2)
        self.updateProfile()


    def clearList(self):
        for i in range(len(self.display)):
            self.display[i].config(text="")
        for i in range(len(self.checkBoxes)):
            self.checkBoxes[0].destroy()
            self.checkBoxes.pop(0)
            self.boxesVariables.pop(0)

    def deletAction(self):
        temp=[]     
        for i in range(len(self.boxesVariables)):
            if(self.boxesVariables[i].get()):
                temp.append(i)
        if(self.control=='r'): 
            for i in temp:
                self.rightLightSchedule.pop(i)      
            self.findRightNext()
            self.rightLightScheduleButton() 
            self.updateGUI()
        elif(self.control=='l'):
            for i in temp:
                self.leftLightSchedule.pop(i)
            self.leftLightScheduleButton()
            self.findLeftNext()
            self.updateGUI()
        elif(self.control=='s'):
            for i in temp:
                self.sumpLightSchedule.pop(i)
            self.sumpLightScheduleButton() 
            self.findSumpNext()
            self.updateGUI()
       
        
               

    def addItem(self):
        if self.control=='':
            self.l1.config(text='choose light')
            self.l1.grid(row=16)
            return
        self.l1.config(text='')

        hrs=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)
        self.h=IntVar()
        self.h.set(hrs[0])
        self.hours=OptionMenu(self.frame,self.h,*hrs)
        self.hours.grid(row=16,column=0)

        self.m=IntVar()
        self.m.set(hrs[0])
        self.mins=OptionMenu(self.frame,self.m,*hrs)
        self.mins.grid(row=16,column=1)

        cs=('True','False')
        self.c=BooleanVar()
        self.c.set(cs[0])
        self.choices=OptionMenu(self.frame,self.c,*cs)
        self.choices.grid(row=16,column=2)

        b=Button(self.frame,text="Add",command=self.addEnter)
        b.grid(row=15,column=2)
        
    def addEnter(self):
        temp=temp=[self.h.get(),self.m.get(),self.c.get()]
        if self.control=='r':
            self.rightLightSchedule=addEntry(self.rightLightSchedule,temp)
            self.rightLightScheduleButton() 
            self.findRightNext()
        elif self.control=='l':
            self.leftLightSchedule=addEntry(self.leftLightSchedule,temp)
            self.leftLightScheduleButton() 
            self.findLeftNext()
        elif self.control=='s':
            self.sumpLightSchedule=addEntry(self.sumpLightSchedule,temp)
            self.sumpLightScheduleButton() 
            self.findSumpNext()
        self.updateGUI()

    def setupSecondGUI(self):
        root=self.root
        bgC=self.bgC
        fgC=self.fgC
        bdC=self.bdC
        self.frame=Frame(root,width=self.pX,heigh=self.pY,highlightbackground=bdC,highlightthickness=1,bg=bgC)
        self.frame.grid_propagate(0)
        self.frame.grid(row=1,column=1)

        mainLabel=Label(self.frame,text="Light System Schedules",fg=fgC,bg=bgC)
        mainLabel.grid(row=0,columnspan=3)      

        buttonWidth=10
        rLB=Button(self.frame,text="Right light",bg=bgC,fg=fgC,width=buttonWidth,command=self.rightLightScheduleButton)
        rLB.grid(row=1,column=0)

        lLB=Button(self.frame,text="Left light",bg=bgC,fg=fgC,width=buttonWidth,command=self.leftLightScheduleButton)
        lLB.grid(row=1,column=1)

        sLB=Button(self.frame,text="sump light",bg=bgC,fg=fgC,width=buttonWidth,command=self.sumpLightScheduleButton)
        sLB.grid(row=1,column=2)
        
        self.display=[]
        self.checkBoxes=[]
        self.boxesVariables=[]
        for i in range(12):
            self.display.append(Label(self.frame,text='',fg=fgC,bg=bgC))
            self.display[i].grid(row=i+2,column=0,columnspan=2)

        
        deletButton=Button(self.frame,text="delete item",bg=bgC,fg=fgC,width=buttonWidth,command=self.deletAction)
        deletButton.grid(row=15,column=0)

        addButton=Button(self.frame,text="add item",bg=bgC,fg=fgC,width=buttonWidth,command=self.addItem)
        addButton.grid(row=15,column=1)

        self.question=Label(self.frame,text="",fg=fgC,bg=bgC)
        self.question.grid(row=16)

        self.l1=Label(self.frame,fg=self.fgC,bg=self.bgC,text="")

# profiles GUI
    
    def settupProfileGUI(self):
        bgC=self.bgC
        bdC=self.bdC
        self.numberOfProfiles=self.checkForProfiles()
        self.profileFrame=Frame(self.root,width=self.pX,heigh=self.pY,highlightbackground=bdC,highlightthickness=1,bg=bgC)
        self.profileFrame.grid_propagate(0)
        self.profileFrame.grid(row=1,column=0)  

        mL=Label(self.profileFrame,fg=self.fgC,bg=self.bgC,text="Lighting Profiles")
        mL.grid(row=0)

        self.profiles=[]
        for i in range(self.numberOfProfiles):
            self.profiles.append(Button(self.profileFrame,text="Profile {0}".format(i+1),bg=self.bgC,fg=self.fgC,command=lambda i=i:self.buttonPress(i+1)))
            self.profiles[i].grid(row=i+1)

        createNew=Button(self.profileFrame,text="Creat new Profile",bg=self.bgC,fg=self.fgC,command=self.creatNew)
        lbl=Label(self.profileFrame,fg=self.fgC,bg=self.bgC,text="max profiles is 9")
        if(self.numberOfProfiles<9):
            createNew.grid(row=12,column=0)
        else:
            lbl.grid(row=12,column=0)
        
        deletPB=Button(self.profileFrame,text="delet profile",bg=self.bgC,fg=self.fgC,command=self.deletProfile)
        if(self.numberOfProfiles):
            deletPB.grid(row=12,column=1)
        

        
    def creatNew(self):
        
        try:
            if(open("profiles.txt","+r").read()[0]==''):
                pass
            fi=open("profiles.txt","+r")
            c=fi.read() 
            fi.close()
            File=open("profiles.txt","+w")
            string="{0}\n({1}):\n.l\n".format(c,self.numberOfProfiles+1)
            for i in self.leftLightSchedule:
                string='{0}{1}'.format(string,i)
            string='{0}\n.r\n'.format(string)
            for i in self.rightLightSchedule:
                string='{0}{1}'.format(string,i)
            string='{0}\n.s\n'.format(string)
            for i in self.sumpLightSchedule:
                string='{0}{1}'.format(string,i)
            File.write(string)
            File.close()
            self.settupProfileGUI()
        except:
            File=open("profiles.txt","+w")
            string="({0}):\n.l\n".format(self.numberOfProfiles+1)
            for i in self.leftLightSchedule:
                string='{0}{1}'.format(string,i)
            string='{0}\n.r\n'.format(string)
            for i in self.rightLightSchedule:
                string='{0}{1}'.format(string,i)
            string='{0}\n.s\n'.format(string)
            for i in self.sumpLightSchedule:
                string='{0}{1}'.format(string,i)
            File.write(string)
            File.close()
            self.settupProfileGUI()
        self.currentProfile=self.numberOfProfiles
        self.profiles[self.currentProfile-1].config(bg=self.fgC,fg=self.bgC)


    def buttonPress(self, n):
        self.clearList()
        fi=open("profiles.txt","+r")
        c=fi.read() 
        c=c.split('(')
        c.pop(0)
        c=c[n-1]
        c=c.split('.')
        c.pop(0)
        c1=c[0]
        c2=c[1]
        c3=c[2]
        c1=c1[2:len(c1)-1]
        c2=c2[2:len(c2)-1]
        c3=c3[2:len(c3)]
        c1=createArray(c1)
        c2=createArray(c2)
        c3=createArray(c3)
        self.setLeftLightSchedule(c1)
        self.setRightLightSchedule(c2)
        self.setSumpLightSchedule(c3)
        self.clearButtons()
        
        self.currentProfile=n
        self.profiles[n-1].config(bg=self.fgC,fg=self.bgC)
    
    def clearButtons(self):
        self.currentProfile=0
        for i in self.profiles:
            i.config(bg=self.bgC,fg=self.fgC)

    def deletProfile(self):
        if(self.currentProfile==0):
            return
        ogFile=open("profiles.txt","r")
        content=ogFile.read()
        ogFile.close()
        content=content.split("(")
        content.pop(self.currentProfile)
        content.pop(0)
        n=0
        string=''
        for i in content:
            string="{0}({1}{2}".format(string,n+1,i[1:len(i)])
            n+=1
        open("profiles.txt","w").close()
        File=open("profiles.txt","w")
        File.write(string)
        File.close()
        self.settupProfileGUI()

    def updateProfile(self):
        if(self.currentProfile==0):
            return
        ogFile=open("profiles.txt","r")
        content=ogFile.read()
        ogFile.close()
        content=content.split("(")
        content.pop(self.currentProfile)
        content.pop(0)

        string=''
        for i in range(1,self.currentProfile):
            string='{0}({1}'.format(string,content[i-1])

        secondHalf=''
        for i in range(self.currentProfile,len(content)+1):
            secondHalf='{0}({1}'.format(secondHalf,content[i-1])

        s="({0}):\n.l\n".format(self.currentProfile)
        for i in self.leftLightSchedule:
            s='{0}{1}'.format(s,i)
        s='{0}\n.r\n'.format(s)
        for i in self.rightLightSchedule:
            s='{0}{1}'.format(s,i)
        s='{0}\n.s\n'.format(s)
        for i in self.sumpLightSchedule:
            s='{0}{1}'.format(s,i)
        s='{0}\n'.format(s)

        content="{0}{1}{2}".format(string,s,secondHalf)


        open("profiles.txt","+w").close()
        File=open("profiles.txt","+w")
        File.write(content)
        File.close()

        
        


        

    def checkForProfiles(self):     
        try:    
            File=open("profiles.txt","r")
            content=File.read()
            content=content.split("\n")
            n=0
            i=0
            while i<len(content)-2:
                try:
                    if content[i][0]=='(':
                        n=int(content[i][1])
                except:
                    pass
                i+=1
            return n
        except:
            return 0


def addEntry(list,entry):
    t=False
    i=0
    while not t and i<len(list):
        if list[i][0]==entry[0]:
            if list[i][1]<entry[1] or list[i][1]==entry[1]:
                list.insert(i+1,entry)
                t=True
        elif list[i][0]>entry[0]:
            list.insert(i,entry)
            t=True
        i+=1
    if not t:
        list.insert(len(list),entry)
    return list

def createArray(n):
    hold=n
    hold=',{0}'.format(hold)
    hold=hold.split("]")
    hold.pop(len(hold)-1)
    array=[]
    for i in hold:
        ar=[]
        i=i[1:len(i)]
        ar=i.split(',')
        if(ar[0][0]=="["):
            ar[0]=ar[0][1:len(ar[0])]
        ar[0]=int(ar[0])
        ar[1]=int(ar[1])
        if(ar[2][1]=='T'):
            ar[2]=True
        else:
            ar[2]=False
        array.append(ar)
    return array

            
        









    