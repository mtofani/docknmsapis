
class OIDs():

    def __init__(self):
        self.oids = {}
        
        self.oids["caida"] = '1.3.6.1.4.1.3902.1082.500.10.2.3.8.1.6'#
        self.oids["status"] = '1.3.6.1.4.1.3902.1082.500.10.2.3.8.1.4'#
        self.oids["statushw"] = '1.3.6.1.4.1.2011.5.100.1.1.1.6.1.4'#
        self.oids["profileUp"] = '1.3.6.1.4.1.2011.5.100.1.1.1.11.1.2'
        self.oids["uptimehw"] = '1.3.6.1.4.1.2011.6.145.1.1.1.4.1.1'#
        self.oids["serialNumber"] = '1.3.6.1.4.1.3902.1082.500.20.2.1.2.1.3'# SNMPv2-SMI::enterprises.3902.1082.500.20.2.1.2.1.3.285279491.1 = Hex-STRING: 5A 54 45 47 C8 B0 73 C5  (5A 54 45 47 / ZTEG)
        self.oids["serialNumberhw"] = '1.3.6.1.4.1.2011.5.100.1.1.1.5.1.4'# SNMPv2-SMI::enterprises.2011.5.100.1.1.1.5.1.4.4194353152.1 = Hex-STRING: 48 57 54 43 92 41 60 A2 (48 57 54 43 / HWTC)
        self.oids["firmwarehw"] = '1.3.6.1.4.1.2011.5.100.1.1.1.5.1.20'#
        self.oids["firmware"] = "a resolver"
        self.oids["ipStech"] = '1.3.6.1.4.1.3902.1082.500.20.2.17.2.1.14'#
        self.oids["model"] = '1.3.6.1.4.1.3902.1082.500.20.2.1.2.1.8'#
        self.oids["modelhw"] = '1.3.6.1.4.1.2011.5.100.1.1.1.5.1.19'#
        self.oids["rxoltpw"] = '1.3.6.1.4.1.3902.1082.500.1.2.4.2.1.2'# 65535000 means N/A, ONU is not in service -80000 means no signal received.
        self.oids["txoltpwhw"] = '1.3.6.1.4.1.2011.5.100.1.1.1.53.1.3'#
        self.oids["rxonupwhw"] = '1.3.6.1.4.1.2011.5.100.1.1.1.53.1.4'#
        self.oids["rxoltpwhw"] = '1.3.6.1.4.1.2011.5.100.1.1.1.53.1.6'#
        self.oids["rxonupw"] = '1.3.6.1.4.1.3902.1082.500.20.2.2.2.1.10'#
        self.oids["txmbps"] = '1.3.6.1.4.1.3902.1082.500.4.2.2.2.1.3'#
        self.oids["rxmbpshw"] = '1.3.6.1.4.1.2011.5.100.1.1.2.11.1.4'#
        self.oids["txmbpshw"] = '1.3.6.1.4.1.2011.5.100.1.1.2.11.1.3'#
        self.oids["rxmbps"] = '1.3.6.1.4.1.3902.1082.500.4.2.2.2.1.46'#
        self.oids["ipmng"] = '1.3.6.1.4.1.3902.1082.500.2.2.2.5.1.2'#
        self.oids["ipmnghw"] = '1.3.6.1.4.1.2011.5.100.1.1.1.30.1.2'#

        self.oids["ifMza"] = '1.3.6.1.2.1.2.2.1.2.'#
        self.oids["ifMzahw"] = '1.3.6.1.2.1.31.1.1.1.18'#
        self.oids["ifName"] = '1.3.6.1.2.1.31.1.1.1.1'#
        self.oids["sysDescr"] = '1.3.6.1.2.1.1.1'#
        self.oids["ifIndex"] = '1.3.6.1.2.1.2.2.1.1'#
        self.oids["onuDesc"] = '1.3.6.1.4.1.3902.1082.500.10.2.3.3.1.3' # Específico de ZTE
        self.oids["onuDeschw"] = 'iso.3.6.1.4.1.2011.5.100.1.1.1.5.1.14'
        self.oids["tcontName"] = '1.3.6.1.4.1.3902.1082.500.10.2.3.4.1.2' # SNMPv2-SMI::enterprises.3902.1082.500.10.2.3.4.1.2.285278723.12.1 = STRING: "T1-management"
        self.oids["bwprofile"] = '1.3.6.1.4.1.3902.1082.500.10.2.3.4.1.3' # SNMPv2-SMI::enterprises.3902.1082.500.10.2.3.4.1.3.285278723.12.1 = STRING: "IPLAN-MGMN-10M-UP"
 




        
        
    def getOID(self, name):
        return self.oids[name]