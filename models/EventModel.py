from flask_restx import fields

class EventModel(object):
   
    def __init__(self, api):
        self.event = api.model('Event', {
                            'id': fields.Integer(attribute='id'),
                            'name': fields.String(attribute='name'),
                            'mtt': fields.Integer(attribute='mtt'),
                            'olt': fields.String(attribute='olt'),
                            'port': fields.String(attribute='port'),
                            'cto': fields.String(attribute='cto'),
                            'splitter': fields.String(attribute='splitter'),
                            'event_type': fields.Integer(attribute='event_type'),
                            'event_start': fields.String(attribute='event_start'),
                            'event_finish': fields.String(attribute='event_finish'),
                            'status': fields.Integer(attribute='status'),
                            'user': fields.String(attribute='user'),
                        })
    
    def get(self):
        return self.event