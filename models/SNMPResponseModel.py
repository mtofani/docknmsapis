from flask_restx import fields

class SNMPResponseModel(object):

    def __init__(self, api):
        self.response = api.model('SNMPResponse', {
                            'value': fields.String,
                        })
    
    def get(self):
        return self.response