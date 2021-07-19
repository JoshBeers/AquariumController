import asyncio
from asyncio.windows_events import NULL
from threading import Thread

import websockets
import pumpController
import temperatureControl
import emailSystem
import settingSaver
import atoSystem as atoo
import sensorCheckor
from equipment import pump,floatSensor
from GUI import GUI
import websocketObj
from websocketObj import websocketStuff




'''
    notes:
        pump system should be setup isnt tested fully
        tempuature sensor at gpio4
        tank level sensor at gpio14
            when tank is overfull returns false
        sump level sensor at gpio23
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


listeners = set()
def updateListeners():
    if listeners:
        for l in listeners:
            if isinstance(l, websocketStuff):
                asyncio.run(l.update())
            else:    
                l.update()


callback = updateListeners
#model setup

tankPumps = pump.pump([1381717,1381716],callback)
atoPump = pump.pump([1397077,1397076],callback)

tankFloatSensor = floatSensor.floatSensor(27, callback)
sumpFloatSensor = floatSensor.floatSensor(23,callback)
atoFloatSensor = floatSensor.floatSensor(2,callback)






#GPIO.setmode(GPIO.BCM)
#GPIO.setup(21,GPIO.OUT)


emails= emailSystem.emailSystem()
pumps= pumpController.pumpController(emails,tankPumps,tankFloatSensor,sumpFloatSensor,atoFloatSensor, callback)  #ad DNC loactions
heating= temperatureControl.temperatureControl(78,emails,22 , callback) #add locations
ato= atoo.atoSystem(emails,atoPump,sumpFloatSensor,atoFloatSensor,callback) #add locations
saveUtility=settingSaver.settingSaver("saves/saved.txt") 
sensorChecker = sensorCheckor.sensorCheckor(tankPumps,atoPump,tankFloatSensor,sumpFloatSensor,atoFloatSensor)





allStuff= [pumps,heating,ato,sensorChecker]
# saved in order temp setting, left light, right light, sump light


def on_closing():
    saveUtility.saveItems(heating.getTankTempSetting(),"[]","[]","[]")
    pumps.Off()
    ato.Off()
    sensorChecker.stop()
    heating.End()

    
    #lights.Off()
    #heating.End()

def opening():
    temp=saveUtility.getSaved()
    heating.setTankTemp(temp[0])







websocket = websocketObj.websocketStuff(allStuff)
listeners.add(websocket)



allStuff.append(websocket)



#gui stuff


def startRest():
    gui = GUI.GUI(on_closing,allStuff)
    listeners.add(gui)
    opening()
    gui.start()
    

guiThread= Thread(target= startRest)
guiThread.start()
websocket.start()





















