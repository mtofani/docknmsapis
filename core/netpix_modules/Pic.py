from core.netpix_modules.NetPixer import NetPixer
import json

class Pic:

    def __init__(self):
        self.id = 0
        self.name = ""
        self.dateTime = ""
        self.oltsInfo = []

    def __str__(self):
        return f""" 
            Id: {self.id} 
            Name: {self.name} 
            Datetime: {self.dateTime}
            Olts Info: {self.oltsInfo}
            """
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
