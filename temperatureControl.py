import time
import heater as h
from threading import Thread
from tkinter import * 
import thermometer as te
import os
import errno


class temperatureControl:

    def __init__(self,tempSet,root,GUIcolors,pSize,em,logger,heaterLoaction=22):
        self.heater=h.heater(heaterLoaction)
        self.thermometer=te.thermometer()
        self.temperatureSetting=tempSet
        self.opperationStatus=True
        self.heaterLock=False
        self.warning='none'
        self.warned=False
        self.emails=em

        self.logger= logger

        self.thread=Thread()
        self.thread.start()
        self.thread.join()

        self.pX=pSize[0]
        self.pY=pSize[1]
        self.root=root
        self.bgC=GUIcolors[0]
        self.fgC=GUIcolors[1]
        self.bdC=GUIcolors[2]
        self.frame=Frame()
        self.settupGUI()

        self.secondPartOgGUI()


#Public stuff
    def On(self):
        self.opperationStatus=True
        self.heaterLock=False
        self.thread=Thread(target=self.main)
        self.thread.start()
        self.log('system turned on')

    def End(self):
        self.opperationStatus=False
        self.heater.Off()
        self.thread.join()
        self.updateGUI()
        self.log('system turned off')


    def heaterOff(self):
        self.heaterLock=False
        self.heater.Off()
        self.heaterLock=True
        self.updateGUI()
        self.log('heater turned off by user')

        
    def heaterOn(self):
        self.heaterLock=False
        self.heater.On()
        self.heaterLock=True
        self.updateGUI()
        self.log('heater turned on by user')


    def heaterNormal(self):
        self.heaterLock=False
        self.updateGUI()
        self.log('heater turned normal by user')


    def getHeaterStatus(self):
        return self.heater.getStatus()

    def getTankTemperatur(self):
        return self.thermometer.getTemperature()  

    def setTankTemp(self,n):
        self.temperatureSetting=n
        self.updateGUI()

    def getTankTempSetting(self):
        return self.temperatureSetting 

    def temperatureFixed(self):
        self.warning='none'
        self.warned=False
       
#private methods   

    def log(message='',warning=''):
        self.logger.temp(self.opperationStatus,self.getHeaterStatus(),self.temperatureSetting,self.thermometer.getTemperature(),message,warning)

    
    def main(self):
        lastMin=0
        while self.opperationStatus:
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
            self.updateGUI()
            time.sleep(1)

#GUI 

    def settupGUI(self):#
        root=self.root
        self.frame
        bgC=self.bgC
        fgC=self.fgC
        bdC=self.bdC
        self.frame=Frame(root,width=self.pX,heigh=self.pY,highlightbackground=bdC,highlightthickness=1,bg=bgC)
        self.frame.grid_propagate(0)
        self.frame.grid(row=0,column=2)

        mainLabel=Label(self.frame,text="heater system",fg=fgC,bg=bgC)
        mainLabel.grid(row=0,columnspan=3)

        hSL=Label(self.frame,text="Heater Status: ",fg=fgC,bg=bgC,justify=RIGHT)
        hSL.grid(row=1,column=0)
        self.hS=Label(self.frame,text="{0}".format(self.heater.status),fg=fgC,bg=bgC,justify=LEFT)
        self.hS.grid(row=1,column=1)

        tempL=Label(self.frame,text="Temperature: ",fg=fgC,bg=bgC,justify=RIGHT)
        tempL.grid(row=2,column=0)
        self.temp=Label(self.frame,text="{0}".format(self.thermometer.getTemperature()),fg=fgC,bg=bgC,justify=LEFT)
        self.temp.grid(row=2,column=1)

        tempSetL=Label(self.frame,text="Temperature setting: ",fg=fgC,bg=bgC,justify=RIGHT)
        tempSetL.grid(row=3,column=0)
        self.tempSet=Label(self.frame,text="{0}".format(self.temperatureSetting),fg=fgC,bg=bgC,justify=LEFT)
        self.tempSet.grid(row=3,column=1)

        hLL=Label(self.frame,text="heater lock: ",fg=fgC,bg=bgC,justify=RIGHT)
        hLL.grid(row=4,column=0)
        self.hL=Label(self.frame,text="{0}".format(self.heaterLock),fg=fgC,bg=bgC,justify=LEFT)
        self.hL.grid(row=4,column=1)

        buttonWidth=13
        hOn=Button(self.frame,text="Heater On",bg=bgC,fg=fgC,width=buttonWidth,command=self.heaterOn)
        hOn.grid(row=5,column=0)
        hOff=Button(self.frame,text="Heater Off",bg=bgC,fg=fgC,width=buttonWidth,command=self.heaterOff)
        hOff.grid(row=5,column=1,columnspan=2)
        hNorm=Button(self.frame,text="Heater Normal",bg=bgC,fg=fgC,width=buttonWidth,command=self.heaterNormal)
        hNorm.grid(row=6,column=0)

        sOff=Button(self.frame,text="reset warning",bg=bgC,fg=fgC,width=buttonWidth,command=self.temperatureFixed)
        sOff.grid(row=6,column=1,columnspan=2)

        sOn=Button(self.frame,text="System on",bg=bgC,fg=fgC,width=buttonWidth,command=self.On)
        sOn.grid(row=7,column=0)

        sOff=Button(self.frame,text="System off",bg=bgC,fg=fgC,width=buttonWidth,command=self.End)
        sOff.grid(row=7,column=1,columnspan=2)

        wL=Label(self.frame,text="warnings: ",fg=fgC,bg=bgC,justify=RIGHT)
        wL.grid(row=8,column=0)
        self.w=Label(self.frame,text="{0}".format(self.warning),fg=fgC,bg=bgC,justify=LEFT)
        self.w.grid(row=9,columnspan=3)       

    def updateGUI(self):
        self.hS.config(text="{0}".format(self.heater.status))
        self.temp.config(text="{0}".format(self.thermometer.getTemperature()))
        self.tempSet.config(text="{0}".format(self.temperatureSetting))
        self.hL.config(text="{0}".format(self.heaterLock))
        self.w.config(text="{0}".format(self.warning))
   
    def secondPartOgGUI(self):
        self.frame2=Frame(self.frame,bg=self.bgC)
        self.frame2.grid(row=10,column=0,rowspan=8,columnspan=3)

        lb=Label(self.frame2,text="new temperature setting:",bg=self.bgC,fg=self.fgC)
        lb.grid(row=0,column=0)

        self.tempTempSetting=IntVar()

        entry=Entry(self.frame2,width=10,textvariable=self.tempTempSetting)
        entry.grid(row=0,column=1)

        updButton=Button(self.frame2,text="update",bg=self.bgC,fg=self.fgC,command=self.update)
        updButton.grid(row=1)

        self.lbl=Label(self.frame2,text="",wraplength=150,justify=LEFT,bg=self.bgC,fg='red')
        self.lbl.grid(row=2)

    def update(self):
        try:
            if self.tempTempSetting.get()<150 and self.tempTempSetting.get()>50:
                self.setTankTemp(self.tempTempSetting.get())
                self.lbl.config(text="")
            else:            
                self.lbl.config(text="please enter number between 50 and 150")
        except:
            self.lbl.config(text="please enter number between 50 and 150")
