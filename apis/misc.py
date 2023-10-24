from flask_restx import reqparse
from flask_restx import Resource
from flask_restx import Namespace
from core.Tenfold import Tenfold

api = Namespace('misc', description='Herramientas varias')

@api.route('/tenfold/getSubsNumberById/')
@api.param('idSubs', 'Id de Subscripcion')
class GetSubsNumberById(Resource):
    @api.response(200, description="Todo OK")
    
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('idSubs', required=True)
            args = parser.parse_args()
            
            idSubs = args['idSubs']
            resp = Tenfold().getSubsNumber(idSubs)
            return resp
        except Exception as e:
            print(e)
        finally:
            pass