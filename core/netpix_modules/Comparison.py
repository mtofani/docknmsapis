import json


class Comparison():

    def __init__(self,results):
        self.results = results

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)