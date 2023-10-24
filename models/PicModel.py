from flask_restx import fields

class PicModel(object):

    def __init__(self, api):
        self.device = api.model('Pic', {
                            'id': fields.Integer,
                            'hostname': fields.String,
                            'uptime': fields.Integer,
                            'object_id': fields.String,
                            'description': fields.String,
                            'responded_ping': fields.Integer,
                            'responded_snmp': fields.Integer,
                            'last_update': fields.DateTime,
                        })
    
    def get(self):
        return self.device