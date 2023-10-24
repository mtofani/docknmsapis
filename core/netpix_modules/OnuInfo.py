from abc import abstractmethod
import json

from core.netpix_modules.CompareResult import CompareResult


class OnuInfo:


    def __init__(self):
        self.descr = ""
        self.olt = ""
        # self.ifIndex = ""
        self.rxOnu = 0
        self.rxOlt = 0
        self.serial = ""
        self.status = ""
        # self.statusStr = ""
        self.channel = ""
        # self.oltModel = ""
        # self.mza = ""
        self.statusOk = 0

    @abstractmethod
    def setStatus(self, status):
        self.status = status

    @abstractmethod
    def setStatusStr(self):
        pass

    @abstractmethod
    def setMza(self, mza):
        self.mza = mza
        
    @abstractmethod
    def setRXOlt(self,rx):
        pass

    @abstractmethod
    def setRXOnu(self,rx):
        pass
    
    @abstractmethod
    def setMza(self,mza):
        self.mza = mza
    
    @abstractmethod
    def setSerial(self,serial):
        pass

    @abstractmethod
    def processOnuNumberByIfIndex(self):
        pass

    def setOlt(self, olt):
        self.olt = olt

    def setOltModel(self, model):
        self.oltModel = model
    
    def setIfIndex(self, ifIndex):
        self.ifIndex = ifIndex

    def setOnuChannel(self,channel):
        self.channel = channel
        
    def setDesc(self, descr):
        self.descr = descr

    def isEmpty(self):
        return self.channel == ""

    def compareThis(self, onu2):
        comparison = CompareResult()

         #Agregar IP de la OLT y SN de la onu

         
        comparison.channel = onu2.channel
        comparison.oltIp = onu2.olt
        comparison.oldStatus = self.status
        comparison.oldRxOnu = self.rxOnu
        comparison.oldRxOlt = self.rxOlt
        comparison.newRxOlt = onu2.rxOlt
        comparison.newRxOnu = onu2.rxOnu
        comparison.newSerial = onu2.serial
        comparison.newStatus = onu2.status
        comparison.descr = onu2.descr
        comparison.oldSerial = self.serial
        comparison.serial = onu2.serial


        comparison.rxOltDiff = self.comparePw(self.rxOlt, onu2.rxOlt)
        
        comparison.rxOnuDiff = self.comparePw(self.rxOnu, onu2.rxOnu)

        comparison.statusDiff = self.compareStatus(onu2.status)

        comparison.serialDiff = self.compareSerial(onu2.serial)

        return comparison

    def compareStatus(self, status2):
        status = 0
        if self.status==self.statusOk:
            if status2!=self.statusOk:
                status = -1
            else:
                status = 0
        elif (status2 ==self.statusOk):
            status = 1 
        return status
    
    def compareSerial(self,serial):
        if self.serial == serial:
            return 0
        else:
            return 1

    
    def comparePw(self, onu1Pw,onu2Pw):
        diffPw = onu1Pw - onu2Pw
        return round(-diffPw,2)


    def __str__(self):
        #return "Vacía" if (self.isEmpty()) else "Onu: "+str(self.channel)+" Cliente: "+self.desc+ " Estado: "+self.status+" Rx Power: "+str(self.rx)+" Serial: "+self.serial 
        return "Vacía" if (self.isEmpty()) else """
            Onu: {} 
            Cliente: {} 
            Estado: {} 
            RxOlt Power: {}
            RxOnu Power: {}
            Serial: {}
            IfIndex: {}

        """.format(self.channel,self.descr,self.status,str(self.rxOlt),str(self.rxOnu),self.serial,self.ifIndex)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
