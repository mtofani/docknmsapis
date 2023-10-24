from flask import jsonify

class SNMPResponse():

    def __init__(self, ifIndex, value):
        self.ifIndex = ifIndex
        self.value = value
        
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __json__(self):
        return jsonify({'value': str(self.value)})