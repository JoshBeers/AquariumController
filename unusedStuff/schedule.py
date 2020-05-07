
class schedule:

    def __init__(self,text=" "):
        strings=text.split("\n")
        self.sc=[]
        if text==" ":
            return 
        for i in strings:
            s=i.split(",")
            self.addTime([int(s[0]),int(s[1]),bool(self.getBool(s[2]))])


    def getSchedule(self):
        return self.sc

    def removePlace(self,n):
        self.sc.remove(n)

    def addTime(self,entry):
        if len(self.sc)==0:
            self.sc.append(entry)
            return
        place=0
        while place<len(self.sc):
            if(self.sc[place][0]>entry[0]):
                self.sc.insert(place,entry)
                return 
            if(self.sc[place][0]==entry[0] and self.sc[place][1]>entry[1]):
                self.sc.insert(place,entry)
                return 
            place=place+1
        self.sc.append(entry)


    def toString(self):
        string=""
        for i in self.sc:
            string="{0}{1},{2},{3}\n".format(string,i[0],i[1],i[2])
        return string
    
    def getCurrentState(self,currentTime):
        place=len(self.sc)-1
        while place>-1:
            if(self.sc[place][0]<currentTime[0] and self.sc[place][1]<currentTime[1]):
                return self.sc[place][2]
            if(self.sc[place][0]==currentTime[0] and self.sc[place][1]<currentTime[1]):
                return self.sc[place][2]
            place=place-1
        return self.sc[0][2]

    def getBool(self,b):
        if b=="False":
            return 0
        return 1
'''
s=schedule()
s.addTime([1,5,False])
s.addTime([1,1,True])
s.addTime([10,50,False])
s.addTime([12,50,False])
s.addTime([12,25,True])
'''
s=schedule("1,5,False\n1,1,True\n10,50,False\n12,50,False\n12,25,True")


print(s.toString())
print(s.getCurrentState([1,6]))


