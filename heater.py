#import RPi.GPIO as GPIO
class heater:
    def __init__(self,n):
        self.location=n
        self.status=False
  #      GPIO.setmode(GPIO.BCM)
  #      GPIO.setup(self.location,GPIO.OUT)

    def On(self):
        self.status=True
  #      GPIO.setup(self.location,GPIO.OUT)
  #      GPIO.output(self.location,GPIO.HIGH)

    def Off(self):
        self.status=False
   #     GPIO.output(self.location,0)


    def setLocation(self,n):
        self.location=n

    def getLocation(self):
        return self.location

    def getStatus(self):
        return self.status


    