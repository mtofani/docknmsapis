from flask_restx import fields

class TrafficModel(object):
   
    def __init__(self, api):
        self.traffic = api.model('Traffic', {
                            'INTERVAL_DATE': fields.String(attribute='idate'),
                            'UPSTREAM': fields.Integer(attribute='up'),
                            'DOWNSTREAM': fields.Integer(attribute='down'),
                        })
    
    def get(self):
        return self.traffic
