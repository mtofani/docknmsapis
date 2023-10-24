import json
from core.netpix_modules.NetPixDB import NetPixDB


class OltModels:

    def __init__(self):
        db = NetPixDB()
        self.models = []
        respDb = db.selectOltModels()
        for r in respDb:
            self.models.append({
                "value":r[0],
                "name":r[1],
                "vendor":r[2]
            })
        pass


    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
