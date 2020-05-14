import RPi.GPIO as gpio

class floatSensor:
    def __init__(self,loc):
        self.location=loc


    def getLevel(self):#
        gpio.setmode(gpio.BCM)
        gpio.setup(self.location,gpio.IN)
        rtn = gpio.input(self.location)
        gpio.cleanup()
        return rtn