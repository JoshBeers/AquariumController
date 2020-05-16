from rpi_rf import RFDevice
import time


class pump:


    def __init__(self,frequencys,sendService):
        self.status=False
        self.frequencys=frequencys
        self.lock=False
        self.cach=False 
        self.sendService = sendService



    def On(self):
        if not self.lock:
            self.status=True
            self.sendCode(self.frequencys[0])
            self.cach=True            
        else:
            self.cach=True            

    def Off(self):     
        if not self.lock:
            self.status=False
            self.sendCode(self.frequencys[1])
            self.cach=False
        else:
            self.cach=False

    def normalize(self):
        self.lock = False
        if(self.cach):
            self.On()
            return
        self.Off()

    def userAction(self, status):
        #print(status)
        self.lock = False
        if(status):
            self.On()
            self.lock = True
            return
        self.Off()
        self.lock = True

    def sendCode(self, code):
        self.sendService.sendCode(code)
                
           
        
'''
p = pump([0,1])
p.sendCode(1381716)
p.sendCode(1381716)
'''

    
