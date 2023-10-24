from flask_restx import fields

class OnuModel(object):

    def __init__(self, api):
        self.onu = api.model('Onu', {
                            'device_ip': fields.String,
                            'if_index': fields.Integer,
                            'onu_number': fields.Integer,
                            'onu_alias': fields.String,
                            'sn': fields.String,
                            'last_update': fields.DateTime,
                        })
    
    def get(self):
        return self.onu