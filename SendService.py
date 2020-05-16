class SendService:
    
    def __init__(self):
        self.workingList = []
        self.rfdevice = RFDevice(17) 
        self.rfdevice.enable_tx()
        self.rfdevice.tx_repeat = 7
        
    def sendCode(self, code):
        self.workingList.append(code)
        
    def run(self):
        
    
