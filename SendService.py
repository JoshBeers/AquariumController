import time
import RFSSendingCode
from threading import Thread
from RPi import GPIO



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
        self.opperationalStatus = True
        self.t=Thread(target=self._run)
        self.t.start()

    def close(self):
        SendService.rfdevice.cleanup()
        self.opperationalStatus = False
        
    def _run(self):
        while(self.opperationalStatus):
            print('test')
            if(len(self.workingList) != 0):
                self._sendingCode(self.workingList.pop())
                print('code out')

    def _sendingCode(self,code):
        
        temp = True
        while temp:
            #try:
                GPIO.setmode(GPIO.BCM)
                self.rfdevice = RFSSendingCode.RFDevice(17) 
                self.rfdevice.enable_tx()
                self.rfdevice.tx_repeat = 7
                self.rfdevice.tx_code(code,1,415,24)
                self.rfdevice.cleanup()
                temp = False
            #except:
                print('send error')
        
        
            

            


        
    
