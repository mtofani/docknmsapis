from cfg.ConfigParser import ConfigParser
from pysnmp.hlapi import *
from core.SNMPResponse import SNMPResponse
from cfg.Logger import Logger

class SNMPLauncher():

    def __init__(self, ip):
        self.ip = ip
        self.config = ConfigParser().params
        self.log = Logger("/home/nms/REST/core/snmp.log")
        self.timeout = self.config['SNMP']['timeout']
        self.retries = self.config['SNMP']['retries']
        self.comm = self.config['SNMP']['community']

    def executeBulk(self, oid):
        mylist = []
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in bulkCmd(SnmpEngine(),
                                  CommunityData(self.comm),
                                  UdpTransportTarget((self.ip, 161), timeout=int(self.timeout), retries=int(self.retries)),
                                  ContextData(),
                                  0, 100,
                                  ObjectType(ObjectIdentity(oid)),
                                  lexicographicMode=False):
            
            if errorIndication:
                self.log.logError(errorIndication)
                mylist.append(SNMPResponse(0, 0))
                return mylist
            elif errorStatus:
                self.log.logError(str(errorStatus) + "(" + str(errorIndex) + ")" + str(errorIndication))
                break
            else:
                for varBind in varBinds:
                    loid, value = varBind
                    y = str(loid)
                    x = y.replace(oid+".", "")
                    sr = SNMPResponse(str(x), str(value))
                    #self.logInfo(sr)
                    mylist.append(sr)
                
        return mylist

    def executeBulkRaw(self, oid):
        mylist = []
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in bulkCmd(SnmpEngine(),
                                  CommunityData(self.comm),
                                  UdpTransportTarget((self.ip, 161), timeout=int(self.timeout), retries=int(self.retries)),
                                  ContextData(),
                                  0, 500,
                                  ObjectType(ObjectIdentity(oid)),
                                  lexicographicMode=False):
            
            if errorIndication:
                self.log.logError(errorIndication)
                raise Exception(errorIndication)
            elif errorStatus:
                self.log.logError(str(errorStatus) + "(" + str(errorIndex) + ")" + str(errorIndication))
                e = str(errorStatus) + "(" + str(errorIndex) + ")" + str(errorIndication)
                self.log.logError(e)
                raise Exception(e)
            else:
                for varBind in varBinds:
                    loid, value = varBind
                    y = str(loid)
                    x = y.replace(oid+".", "")
                    oct = value.asOctets()
                    mylist.append(SNMPResponse(str(x), ''.join(['%.2x' % x for x in oct])))
        return mylist

                    
    def executeGet(self, oid):
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in getCmd(SnmpEngine(),
                                  CommunityData(self.comm),
                                  UdpTransportTarget((self.ip, 161), timeout=int(self.timeout), retries=int(self.retries)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity(oid)),
                                  lexicographicMode=False):
            
            if errorIndication:
                self.log.logError(errorIndication)
                raise Exception(errorIndication)
            elif errorStatus:
                self.log.logError(str(errorStatus) + "(" + str(errorIndex) + ")" + str(errorIndication))
                e = str(errorStatus) + "(" + str(errorIndex) + ")" + str(errorIndication)
                self.log.logError(e)
                raise Exception(e)
            else:
                for varBind in varBinds:
                    loid, value = varBind
                    y = str(loid)
                    x = y.replace(oid+".", "")
                
                sr = SNMPResponse(str(x), str(value))
                self.log.logInfo(sr)
                return sr
            
    def executeGetHex(self, oid):
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in getCmd(SnmpEngine(),
                                  CommunityData(self.comm),
                                  UdpTransportTarget((self.ip, 161), timeout=int(self.timeout), retries=int(self.retries)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity(oid)),
                                  lexicographicMode=False):
            
            if errorIndication:
                self.log.logError(errorIndication)
                raise Exception(errorIndication)
            elif errorStatus:
                e = str(errorStatus) + "(" + str(errorIndex) + ")" + str(errorIndication)
                self.log.logError(e)
                raise Exception(e)
            else:
                for varBind in varBinds:
                    loid, value = varBind

                return value.asNumbers()
            
    def executeGetRaw(self, oid):
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in getCmd(SnmpEngine(),
                                  CommunityData(self.comm),
                                  UdpTransportTarget((self.ip, 161), timeout=int(self.timeout), retries=int(self.retries)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity(oid)),
                                  lexicographicMode=False):
            
            if errorIndication:
                self.log.logError(errorIndication)
                raise Exception(errorIndication)
            elif errorStatus:
                self.log.logError(str(errorStatus) + "(" + str(errorIndex) + ")" + str(errorIndication))
                e = str(errorStatus) + "(" + str(errorIndex) + ")" + str(errorIndication)
                self.log.logError(e)
                raise Exception(e)
            else:
                for varBind in varBinds:
                    loid, value = varBind

                return value
                    
    def executeBulkOnCommand(self, oid, ip):
        mylist = []
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in bulkCmd(SnmpEngine(),
                                  CommunityData(self.comm),
                                  UdpTransportTarget((ip, 161), timeout=int(self.timeout), retries=int(self.retries)),
                                  ContextData(),
                                  0, 100,
                                  ObjectType(ObjectIdentity(oid)),
                                  lexicographicMode=False):
            
            if errorIndication:
                self.log.logError(errorIndication)
                break
            elif errorStatus:
                self.log.logError(str(errorStatus) + "(" + str(errorIndex) + ")" + str(errorIndication))
                break
            else:
                for varBind in varBinds:
                    loid, value = varBind
                    self.logInfo(str(loid) + " : " + str(value))
                    mylist.append(SNMPResponse(str(loid), str(value)))
                    
        return mylist
        
