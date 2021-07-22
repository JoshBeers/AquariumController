#from rpi_rf import RFDevice
import time
#import RFSendingCode



class pump:


    def __init__(self,frequencys,callback):
        self.status=False
        self.frequencys=frequencys
        self.lock=False
        self.cach=False
        self.callback = callback



    def On(self):
        if not self.lock:
            self.status=True
            self.sendCode(self.frequencys[0])
            self.cach=True       
            #self.callback()    
        else:
            self.cach=True   
            

    def Off(self):     
        if not self.lock:
            self.status=False
            self.sendCode(self.frequencys[1])
            self.cach=False
            #self.callback()
        else:
            self.cach=False


    def normalize(self):
        self.lock = False
        if(self.cach):
            self.On()
        else:
            self.Off()
        #self.callback() 

    def userAction(self, status):
        #print(status)
        self.lock = False
        if(status):
            self.On()
            self.lock = True
        else:
            self.Off()
            self.lock = True
        #self.callback()

    def sendCode(self, code):
        return
        #self.sendService.sendCode(code)
        '''
        try:
            self.rfdevice = RFSendingCode.RFDevice(17)
            self.rfdevice.enable_tx()
            self.rfdevice.tx_repeat = 7
            self.rfdevice.tx_code(code,1,415,24)
            self.rfdevice.cleanup()
        except:
            print('send code error')
           '''
        
'''
p = pump([0,1])
p.sendCode(1381716)
p.sendCode(1381716)
'''

    
