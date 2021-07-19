class thermometer:
    def __init__(self,callback):
        self.callback = callback
        pass 
        
    def getTemperature(self):
        #if change call 
        self.callback()
        return 78