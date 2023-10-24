import json


class CompareResult():

    def __init__(self):
        #-1 es peor, 0 es igual y 1 es mejor

        #Agregar puerto, ip olt, sn de la onu, mzaf
        self.descr = "-"
        self.channel = 0
        self.oltIp = 0
        self.oltModel = 0
        self.oltPort = ""
        self.mza = ""
        self.oldRxOlt = 0
        self.newRxOlt = 0
        self.rxOltDiff = 0
        self.oldRxOnu = 0
        self.newRxOnu = 0
        self.rxOnuDiff = 0
        self.oldStatus = 0
        self.statusDiff = 0
        self.newStatus = 0
        self.oldSerial = ""
        self.serialDiff = 0
        self.newSerial = ""

    def __str__(self):
        return f"""
                Onu: {self.channel}
                Descr: {self.descr}
                Rx: {self.rxOlt}
                Diff Rx: {self.rxOltDiff}
                Status: {self.statusDiff}
                Status Dif: {self.statusDiff}
                Status Actual: {self.newStatus}
            """
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)