import smtplib, ssl

class emailSystem:
    def __init__(self):
        self.port=587
        self.to=''
        self.fro=''
        self.context=ssl.create_default_context()
        

    def sendMessage(self,message):
        
        server=smtplib.SMTP('smtp.gmail.com',self.port)
        server.starttls(context=self.context)
        try:
            server.login(self.fro,'')
            server.sendmail(self.fro,self.to,message)
        except:
            print('email error')
        server.quit()



