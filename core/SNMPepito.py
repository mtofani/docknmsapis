from cfg.ConfigParser import ConfigParser
from pysnmp.hlapi import *
from core.SNMPResponse import SNMPResponse
from cfg.Logger import Logger
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

class SNMPLauncher():

    def __init__(self, ip):
        self.ip = ip
        self.config = ConfigParser().params
        self.log = Logger("snmp.log")
        self.timeout = self.config['SNMP']['timeout']
        self.retries = self.config['SNMP']['retries']
        self.comm = self.config['SNMP']['community']


################GETS####################

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


###########SETS#########

    def changeUP(self, ifndx, onu, tcont, profile, ip):
        try:
            oid = '.1.3.6.1.4.1.3902.1082.500.10.2.3.4.1.3.' + str(ifndx) + '.' + str(onu) + '.' + str(tcont)
            cg = cmdgen.CommandGenerator()
    
            comm_data = cmdgen.CommunityData('nociplan')
            transport = cmdgen.UdpTransportTarget((ip, 161))
            variables = (oid, rfc1902.OctetString(profile))
            errorIndication, errorStatus, errorIndex, result = cg.setCmd(comm_data, transport, variables)
    
            if not errorIndication and not errorStatus:
                self.log.logInfo(result)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(errorIndication))
        except Exception:
            self.log.logError("Error al ejecutar cambio de UPSTREAM: " + format(errorIndication))
            raise