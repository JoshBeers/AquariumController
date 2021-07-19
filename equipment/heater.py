#import RPi.GPIO as GPIO
class heater:
    def __init__(self,n, callback):
        self.location=n
        self.status=False
  #      GPIO.setmode(GPIO.BCM)
  #      GPIO.setup(self.location,GPIO.OUT)
        self.callback = callback

    def On(self):
        self.status=True
        self.callback()
  #      GPIO.setup(self.location,GPIO.OUT)
  #      GPIO.output(self.location,GPIO.HIGH)

    def Off(self):
        self.status=False
        self.callback()
   #     GPIO.output(self.location,0)


    def setLocation(self,n):
        self.location=n

    def getLocation(self):
        return self.location

    def getStatus(self):
        return self.status


    