#import RPi.GPIO as GPIO
class pump:
    def __init__(self,frequencys):
        self.status=False
        self.frequencys=frequencys
        self.lock=False
        self.cach=False
 #       GPIO.setmode(GPIO.BCM)
  #      GPIO.setup(self.location,GPIO.OUT)
        
        


    def On(self):
        if not self.lock:
            self.status=True
  #          GPIO.setup(self.location,GPIO.OUT)
  #          GPIO.output(self.location,GPIO.HIGH)
        else:
            self.cach=True            

    def Off(self):     
        if not self.lock:
            self.status=False
   #         GPIO.output(self.location,0)
        else:
            self.cach=False
            
    def checkCach(self):
        if self.cach:
            self.On()
        else:
            self.Off()

    def setLocation(self,n):
        self.location=n
    
    def getLocation(self):
        return self.location
'''
    def lock(self):
        self.lock=1
        pass

    def unlock(self):
        self.lock=0

'''

    
