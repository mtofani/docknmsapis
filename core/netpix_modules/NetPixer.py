
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
parentparent = os.path.dirname(parent)                #/home/desarrollo/NMSAPIPrueba/NMSAPI
sys.path.append(parentparent)


from cfg.Logger import Logger
from core.OIDs import OIDs
from core.SNMPLauncher import SNMPLauncher
from core.netpix_modules.OnuHuawei import OnuHuawei
from core.netpix_modules.OnuZTE import OnuZTE
from core.netpix_modules.UnreachableIPException import UnreachableIPException

class NetPixer:

    ############################################## CONSTRUCTOR ##############################################

    def __init__(self, ip, port):
        self.log = Logger("pixer.log")
        self.ip = ip
        self.port = port
        self.oltModel = -1
        try:
            self.oltModel = self.getOLTModel()
        except UnreachableIPException as e:
            self.log.logError(e)
            raise e

        if self.oltModel == 0:
            prePort = "GPON "
        elif self.oltModel == 1:
            prePort = "gpon_"
        elif self.oltModel == 2:
            prePort = "gpon_olt-"
        self.ndx = self.getIfIndex(prePort+port)
        self.fillOids()
        self.mza = self.getMzaName()

        #Definimos el string que va antes del port, así solo nos pasan el puerto en formato x/x/x independientemente de la OLT

        

    ############################################## SETUP ##############################################


    def fillOids(self):
        print(".-")
        if self.oltModel == 1 or self.oltModel == 2:
            self.oidStatus = OIDs().getOID("status")
            self.oidRXOlt = OIDs().getOID("rxoltpw")
            self.oidRXOnu = OIDs().getOID("rxonupw")
            self.oidDesc = OIDs().getOID("onuDesc")
            self.oidSerialNumber = OIDs().getOID("serialNumber")
            self.oidMzaDesc = OIDs().getOID("ifMza")
            #...
        else:
            self.oidStatus = OIDs().getOID("statushw")
            self.oidRXOlt = OIDs().getOID("rxoltpwhw")
            self.oidRXOnu = OIDs().getOID("rxonupwhw")
            self.oidDesc = OIDs().getOID("onuDeschw")
            self.oidSerialNumber = OIDs().getOID("serialNumberhw")
            self.oidMzaDesc = OIDs().getOID("ifMzahw")
            #...

    def collectOnusInfo(self):
        self.status = self.getStatus() #Lista de objetos: <class 'SNMPResponse.SNMPResponse'>: {'ifIndex': '12', 'value': '7'}
        self.desc = self.getDescr() #Lista de objetos: <class 'SNMPResponse.SNMPResponse'>: {'ifIndex': '60', 'value': '#### Stechs Test2(La Rioja)'}
        self.rxOltPw = self.getRXOlt() #Lista de objetos: <class 'SNMPResponse.SNMPResponse'>: {'ifIndex': '12', 'value': '65535000'}
        self.rxOnuPw = self.getRXOnu()
        self.serialsNum = self.getSerialNumber() #Lista de objetos: <class 'SNMPResponse.SNMPResponse'>: {'ifIndex': '12', 'value': '\x00\x00\x00\x00\x00\x00\x00\x00'}
        self.onus = self.createListOnuInfo()
        # self.mza = self.getMzaName()
        return self.onus

    def createListOnuInfo(self):
        onus = []
        #Creamos el espacio para el máximo de onus (128) y creamos las mismas
        if self.oltModel == 1 or self.oltModel == 2: #ZTE C300 y C600
            for i in range(0,129):
                onus.append(OnuZTE())
                onus[i].setOlt(self.ip)
                onus[i].setIfIndex(self.ndx)
                onus[i].setOltModel(self.oltModel)
                onus[i].setMza(self.mza)
        elif self.oltModel == 0: #Huawei
            for i in range(0,129):
                onus.append(OnuHuawei())
                onus[i].setOlt(self.ip)
                onus[i].setIfIndex(self.ndx)
                onus[i].setOltModel(self.oltModel)
                onus[i].setMza(self.mza)
            
        #Comenzamos a llenar las onus con la info
        for s in self.status:
            index = onus[0].processOnuNumberByIfIndex(s.ifIndex)
            onus[index].setStatus(s.value)
            onus[index].setOnuChannel(index)

        for d in self.desc:
            index = onus[0].processOnuNumberByIfIndex(d.ifIndex)
            onus[index].setDesc(d.value)
            onus[index].setOnuChannel(index)

        for r in self.rxOltPw:
            index = onus[0].processOnuNumberByIfIndex(r.ifIndex)
            onus[index].setRXOlt(r.value)
            onus[index].setOnuChannel(index)

        for ro in self.rxOnuPw:
            index = onus[0].processOnuNumberByIfIndex(ro.ifIndex)
            onus[index].setRXOnu(ro.value)
            onus[index].setOnuChannel(index)

        for s in self.serialsNum:
            index = onus[0].processOnuNumberByIfIndex(s.ifIndex)
            onus[index].setSerial(s.value)
            onus[index].setOnuChannel(index)

        #Acá vamos a filtrar por las ONU que no están vacías
        onusFiltered = []
        for o in onus:
            if not o.isEmpty():
                onusFiltered.append(o)

        return onusFiltered


    ############################################## GETS SNMP ##############################################
    

    def getOLTModel(self):
        oid = OIDs().getOID("sysDescr")
        snmp = SNMPLauncher(self.ip) 
        try:
            out = snmp.executeBulk(oid)
        except Exception as e:
            self.log.logError(e)
            raise e

        descr = "none"

        for res in out:
            if (res.value == 0):
                raise UnreachableIPException("OLT Inválida")
            descr = res.value

        if "C300" in descr:
            self.log.logInfo("ZTE C300") 
            return 1 #ZTE
        if "C600" in descr:
            self.log.logInfo("ZTE C600") 
            return 2 #ZTE
        elif "Huawei" in descr:
            self.log.logInfo("HUAWEI")
            return 0 #HUAWEI
        else:
            self.log.logWarning("Unknown OLT Model")
            return 7

    def getIfIndex(self, port):
        oid = OIDs().getOID("ifName")
        ndx = "404ndx"
        try:
            snmp = SNMPLauncher(self.ip) 
            out = snmp.executeBulk(oid)
            for  obj in out:
                if obj.value == port:
                    ndx = obj.ifIndex
        except Exception as e:
            self.log.logError(e)
            raise
        return ndx


    def getMzaName(self):
        snmp = SNMPLauncher(self.ip) 
        mzaName = "-"
        try:
            out = snmp.executeGet(self.oidMzaDesc+ "." + self.ndx)
            mzaName = out.value
        except Exception as e:
            self.log.logError(e)
            raise e
        return mzaName

    def getStatus(self):
        status = []
        try:
            snmp = SNMPLauncher(self.ip) 
            out = snmp.executeBulk(self.oidStatus + "." + self.ndx)
            state = ""
            for o in out:
                status.append(o)       
        except Exception as e:
            self.log.logError(e)
            raise
        finally:
            return status

    def getDescr(self):
        desc = []
        try:
            snmp = SNMPLauncher(self.ip) 
            out = snmp.executeBulk(self.oidDesc + "." + self.ndx)
            for o in out:
                desc.append(o)      
        except Exception as e:
            self.log.logError(e)
            raise
        finally:
            return desc

    def getRXOlt(self):
        rxPw = []
        try:
            snmp = SNMPLauncher(self.ip) 
            out = snmp.executeBulk(self.oidRXOlt + "." + self.ndx)
            rxPw = out
        except Exception as e:
            self.log.logError(e)
            raise
        finally:
            return rxPw
    
    def getRXOnu(self):
        rxPw = []
        try:
            snmp = SNMPLauncher(self.ip) 
            out = snmp.executeBulk(self.oidRXOnu + "." + self.ndx)
            for o in out:
                o.ifIndex = str(o.ifIndex).split(".")[0]
                rxPw.append(o)
        except Exception as e:
            self.log.logError(e)
            raise e
        finally:
            return rxPw

    def getSerialNumber(self):
        serialNumbers = []
        try:
            snmp = SNMPLauncher(self.ip) 
            out = snmp.executeBulkRaw(self.oidSerialNumber + "." + self.ndx)
            print("------")
            print(out)
            for o in out:
                serialNumbers.append(o) 
                print(o)
        except Exception as e:
            self.log.logError(e)
            print(e)
            raise
        finally:
            return serialNumbers
        

    def getTX(self):
        pass