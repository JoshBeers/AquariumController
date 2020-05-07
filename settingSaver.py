
import os
import errno
class settingSaver:
    def __init__(self,n):
        self.location=n
        if not os.path.exists(os.path.dirname(self.location)):
            try:
                os.makedirs(os.path.dirname(self.location))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        

    def saveItems(self,a,b,c,d):
        open(self.location,"+w").close()
        File=open(self.location,"+w")
        string="{0} \n{1}\n{2}\n{3}".format(a,b,c,d)
        File.write(string)
        File.close()
        
    def getSaved(self):
        File=open(self.location,"r")
        content=File.read()
        itemizes=content.split("\n")
        File.close()
        itemizes[0]=int(itemizes[0])
        itemizes[1]=createArray(itemizes[1])
        itemizes[2]=createArray(itemizes[2])
        itemizes[3]=createArray(itemizes[3])
        return itemizes

    def setLoation(self,n):
        self.location=n

def createArray(n):
    hold=n[1:len(n)-1]
    hold=',{0}'.format(hold)
    hold=hold.split("]")
    hold.pop(len(hold)-1)
    array=[]
    for i in hold:
        ar=[]
        i=i[2:len(i)]
        ar=i.split(',')
        if(ar[0][0]=="["):
            ar[0]=ar[0][1:len(ar[0])]
        ar[0]=int(ar[0])
        ar[1]=int(ar[1])
        if(ar[2][1]=='T'):
            ar[2]=True
        else:
            ar[2]=False
        
        array.append(ar)
    return array
    



