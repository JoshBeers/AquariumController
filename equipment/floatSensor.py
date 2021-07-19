#import RPi.GPIO as gpio

class floatSensor:
    def __init__(self,loc,callback):
        self.location=loc
        self.level = 0
        self.callback = callback


    def getLevel(self):#
       # gpio.setmode(gpio.BCM)
       # gpio.setup(self.location,gpio.IN)
       # rtn = gpio.input(self.location)
      #  gpio.cleanup()
      # need to delete next line to get working properly
      rtn = 0
      if self.level != rtn:
          self.callback()

      self.level = rtn
      return rtn