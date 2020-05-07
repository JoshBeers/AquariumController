#import RPi.GPIO as GPIO
class powerhead:
    def __init__(self,loc,stat=False):
        self.location=loc
        self.status=stat
        self.lock=False
        self.cach=False
  #      GPIO.setmode(GPIO.BCM)
  #      GPIO.setup(self.location,GPIO.OUT)

    def On(self): 
        if not self.lock:
            self.status=True
   #         GPIO.setup(self.location,GPIO.OUT)
   #         GPIO.output(self.location,GPIO.HIGH)
        

    def Off(self):
        if not self.lock:
            self.status=False

    def setLocation(self,n):
        self.location=n
    
    def getLocation(self):
        return self.location

    def getStatus(self):
        return self.status