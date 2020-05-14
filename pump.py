from rpi_rf import RFDevice


class pump:


    def __init__(self,frequencys):
        self.status=False
        self.frequencys=frequencys
        self.lock=False
        self.cach=False 



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
        else:
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
        self.rfdevice = RFDevice(17) 
        self.rfdevice.enable_tx()
        self.rfdevice.tx_repeat = 7
        self.rfdevice.tx_code(code,1,415,24)
        self.rfdevice.cleanup()
        
    
p = pump([0,1])
p.sendCode(1381716)
p.sendCode(1381716)

    
