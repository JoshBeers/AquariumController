
import os
import errno
import datetime
class Logger:

    def __init__(self):
        self.tempFile = 'logs/tempLog.csv'
        self.pumpFile = 'logs/pumpLog.csv'
        self.atoFile = 'logs/atoLog.csv'
        self.checkFile()

    def checkFile(self):
        path = 'logs'
        if not os.path.exists('logs'):
            try:
                os.makedirs(path)
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        if not os.path.isfile(self.tempFile):
            file = open(self.tempFile,'w+')
            file.write('date,time,system status,heater status,temp setting,temp,message,warning')
            file.close()
        if not os.path.isfile(self.pumpFile):
            file = open(self.pumpFile,'w+')
            file.write('date,time,system status,pumps status,tank water level status(0 good),sump water level status(1 good),message,warning')
            file.close()
        if not os.path.isfile(self.atoFile):
            file = open(self.atoFile,'w+')
            file.write('date,time,system status,sump sensor(1 good),ato res status(0 good),message, warning')
            file.close()
        


    def temp(self,systemStatus,heaterStatus,tempSetting,temperature,message='', warning=''):
        file = open(self.tempFile,'a+')
        now = datetime.datetime.now()
        file.write('\n{0},{1},{2},{3},{4},{5},{6}'.format(now.strftime("%x"),now.strftime("%X"),systemStatus,heaterStatus,tempSetting,temperature,message,warning))
        file.close()

    def pump(self,systemStatus,pumpsStaus,tankStatus,sumpStatus,message='', warning=''):
        file = open(self.pumpFile,'a+')
        now = datetime.datetime.now()
        file.write('\n{0},{1},{2},{3},{4},{5},{6},{7}'.format(now.strftime("%x"),now.strftime("%X"),systemStatus,pumpsStaus,tankStatus,sumpStatus,message,warning))
        file.close()

    def ato(self,systemStatus,sumpStatus,atoResStatus,message='', warning=''):
        file = open(self.atoFile,'a+')
        now = datetime.datetime.now()
        file.write('\n{0},{1},{2},{3},{4},{5},{6}'.format(now.strftime("%x"),now.strftime("%X"),systemStatus,sumpStatus,atoResStatus,message,warning))
        file.close()



