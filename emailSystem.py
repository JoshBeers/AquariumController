import smtplib, ssl

class emailSystem:
    def __init__(self):
        self.port=587
        self.to='joshbeers999@gmail.com'
        self.fro='maintankwarnings@gmail.com'
        self.context=ssl.create_default_context()
        

    def sendMessage(self,message):
        
        server=smtplib.SMTP('smtp.gmail.com',self.port)
        server.starttls(context=self.context)
        try:
            server.login(self.fro,'Tank123?Warn')
            server.sendmail(self.fro,self.to,message)
        except:
            print('email error')
        server.quit()

'''
    email used:
    maintankwarnings@gmail.com
    Tanl123?Warn
'''

