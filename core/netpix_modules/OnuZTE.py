from core.netpix_modules.CompareResult import CompareResult
from core.netpix_modules.OnuInfo import OnuInfo

class OnuZTE(OnuInfo):

    def __init__(self):
        super().__init__()
        self.statusOk = 4

    def setStatusStr(self):
        statusProcessed = ""
        if(self.status=="2"):
            statusProcessed="LOS"
        elif(self.status=="4"):
            statusProcessed="Working"
        elif(self.status=="5"):
            statusProcessed="DyingGasp"
        elif(self.status=="7"):
            statusProcessed="Offline"
        else:
            statusProcessed = "Unknown("+self.status+")"
        self.statusStr = statusProcessed

    def setRXOlt(self,rx):
        rxProcessed = 0
        if (rx == "65535000"):
            rxProcessed = 0
        elif(rx == "-80000"):
            rxProcessed = -40
        else:
            rxProcessed = int(rx)/1000
        self.rxOlt = round(rxProcessed,2)
    
    
    def setRXOnu(self,rx):
        self.rxOnu = self.convertRxOnuSNMP(rx)
    
    def setSerial(self,serial):
        self.serial = 'ZTEG' + serial[8:].upper()

    def processOnuNumberByIfIndex(self, ifIndex):
        return int(ifIndex)
    

    #---------------------------MISC-----------------------------
    
    def convertRxOnuSNMP(self,value):
        RxOptLevel = -40
        if int(value) != 65535 and int(value) != 0:
            RxOptLevel = (self.twos_comp(int(value),16) * 0.002) - 30
        return round(RxOptLevel,2)

    def twos_comp(self, val, bits):
        """compute the 2's complement of int value val"""
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits) # compute negative value
        return val   # return positive value as is