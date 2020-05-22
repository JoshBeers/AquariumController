from threading import Thread
from tkinter import * 
import pumpController
#import tankLigthControler
import temperatureControl
import signal
import emailSystem
import settingSaver
import atoSystem as ato
import logger
import pump,floatSensor, sensorCheckor


'''
    notes:
        pump system should be setup isnt tested fully
        tempuature sensor at gpio4
        tank level sensor at gpio14
            when tank is overfull returns false
        sump level sensor at gpio15
            when sump is full false
        ato sensor at gpio18
            when res is full returns true
        receiver at 27 big one is receiver
                    check these so that the pumps are not active if disconnected

    

    remote frenq:
        loc | on    |off    | length~415 | protocol 1
        1.1 |1381717|1381716
        1.2 |1394005|1394005
        1.3 |1397077|1397076


        

'''

#model setup

tankPumps = pump.pump([1381717,1381716])
atoPump = pump.pump([1397077,1397076])

tankFloatSensor = floatSensor.floatSensor(27)
sumpFloatSensor = floatSensor.floatSensor(22)
atoFloatSensor = floatSensor.floatSensor(2)



#GPIO.setmode(GPIO.BCM)
#GPIO.setup(21,GPIO.OUT)


root=Tk()
root.geometry('1000x800')
colors=["grey","black","black"]
panelSize=[300,400]
root.config(bg=colors[0])


#objects
logger = logger.Logger()
emails=emailSystem.emailSystem()
pumps=pumpController.pumpController(root,colors,panelSize,emails,logger,tankPumps,tankFloatSensor,sumpFloatSensor,atoFloatSensor)  #ad DNC loactions
#lights=tankLigthControler.lightControler(root,colors,panelSize)  #add locations
heating=temperatureControl.temperatureControl(78,root,colors,panelSize,emails,logger) #add locations
ato = ato.atoSystem(root,colors,panelSize,emails,logger,atoPump,sumpFloatSensor,atoFloatSensor) #add locations
saveUtility=settingSaver.settingSaver("saves/saved.txt") 
sensorChecker = sensorChecker.sensorChecker(root,colors,panelSize,tankPumps,atoPump,tankFloatSensor,sumpFloatSensor,atoFloatSensor)


# saved in order temp setting, left light, right light, sump light


def on_closing():
    saveUtility.saveItems(heating.getTankTempSetting(),"[]","[]","[]")
    pumps.Off()
    ato.Off()
    #lights.Off()
    #heating.End()
    root.destroy()

def opening():
    temp=saveUtility.getSaved()
    heating.setTankTemp(temp[0])













root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()







