import time
from rpi_rf import RFDevice
from threading import Thread


class SendService:
    
    def __init__(self):
        self.workingList = []
        self.opperationalStatus = False
        self.t=Thread()
        self.t.start()
        self.t.join()

        
    def sendCode(self, code):
        self.workingList.append(code)
        print('code added')

    def startUp(self):
        self.rfdevice = RFDevice(17) 
        self.rfdevice.enable_tx()
        self.rfdevice.tx_repeat = 7
        self.opperationalStatus = True
        self.t=Thread(target=self._run)
        self.t.start()

    def close(self):
        self.rfdevice.cleanup()
        self.opperationalStatus = False
        
    def _run(self):
        while(self.opperationalStatus):
            if(len(self.workingList) != 0):
                self._sendingCode(self.workingList.pop())
                print('code out')

    def _sendingCode(self,code):
        while True:
            try:
                self.rfdevice.tx_code(code,1,415,24)
                break
            except:
                print('send code error')


        
    
