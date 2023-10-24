from core.netpix_modules.OnuInfo import OnuInfo

class OnuHuawei(OnuInfo):

    def __init__(self):
        super().__init__()
        self.statusOk = 1

    def setStatusStr(self):
        statusProcessed = ""
        if(self.status=="1"):
            statusProcessed="Online"
        elif(self.status=="2"):
            statusProcessed="Offline"
        else:
            statusProcessed = "Unknown("+self.status+")"
        self.statusStr = statusProcessed

    def setRXOlt(self,rx):
        rxProcessed = 0
        if (rx == "2147483647" or rx == "0"):
            rxProcessed = 0
        else:
            #rxProcessed = int(rx)/100
            rxProcessed = (int(rx) - 10000) / 100

        self.rxOlt = round(rxProcessed,2)
    
    def setRXOnu(self,rx):
        rxProcessed = 0
        if (rx == "2147483647" or rx == "0"):
            rxProcessed = 0
        else:
            #rxProcessed = int(rx)/100
            rxProcessed = (int(rx)) / 100

        self.rxOnu = round(rxProcessed,2)
    
    def setSerial(self,serial):
        self.serial = serial.upper()

    def processOnuNumberByIfIndex(self, ifIndex):
        index = int(str(ifIndex).split(".")[-1])
        return index


