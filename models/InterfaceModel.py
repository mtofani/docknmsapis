from flask_restx import fields

class InterfaceModel(object):

    def __init__(self, api):
        self.interface = api.model('Interface', {
                            'device_ip': fields.String,
                            'if_index': fields.Integer,
                            'if_name': fields.String,
                            'if_descr': fields.String,
                            'if_alias': fields.String,
                            'if_status': fields.Integer,
                            'if_type': fields.Integer,
                            'onu_number': fields.Integer,
                            'onu_alias': fields.String,
                            'sn': fields.String,
                            'last_update': fields.DateTime,
                        })
    
    def get(self):
        return self.interface