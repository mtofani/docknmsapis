from core.netpix_modules.NetPixDB import NetPixDB
import json


class Statuses:

    def __init__(self):
        db = NetPixDB()
        respDb = db.selectStatuses()
        self.statuses = []
        for r in respDb:
            self.statuses.append({
                "statusNumber" : r[0],
                "statusName" : r[1],
                "oltModel" : r[2]
            })
    
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
