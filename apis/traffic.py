from flask_restx import reqparse
from flask_restx import Resource
from models.TrafficModel import TrafficModel
from flask_restx import Namespace
from .nmssec import auth
from core.TrafficDB import TrafficDB
from core.APIDB import APIDB
from flask import request

api = Namespace('traffic', description='Herramientas de Trafico de Clientes')

@api.route('/getweekly/')
@api.param('subscription', 'Numero de subscripcion a consultar')
class getWeeklyTraffic(Resource):
    @auth.login_required
    @api.marshal_with(TrafficModel(api).get(), envelope='Traffic')
    @api.response(200, description="Todo OK")
    @api.response(406, "Subscripcion Inexistente")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('subscription', required=True, help="La subscripcion no puede estar en blanco")
        args = parser.parse_args()
        subscription = args['subscription']
        
        try:
            return TrafficDB().getWeeklyData(subscription)
        finally:
            APIDB().registerUsage(request.authorization.username, request.method, request.full_path, 0, request.remote_addr)
            
@api.route('/getonline/')
@api.param('subscription', 'Numero de subscripcion a consultar')
class getOnlineTraffic(Resource):
    @auth.login_required
    @api.marshal_with(TrafficModel(api).get(), envelope='Traffic')
    @api.response(200, description="Todo OK")
    @api.response(406, "Subscripcion Inexistente")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('subscription', required=True, help="La subscripcion no puede estar en blanco")
        args = parser.parse_args()
        subscription = args['subscription']
        
        try:
            return TrafficDB().getOnlineData(subscription)
        finally:
            APIDB().registerUsage(request.authorization.username, request.method, request.full_path, 0, request.remote_addr)
            
@api.route('/getmonthly/')
@api.param('subscription', 'Numero de subscripcion a consultar')
class getMonthlyTraffic(Resource):
    @auth.login_required
    @api.marshal_with(TrafficModel(api).get(), envelope='Traffic')
    @api.response(200, description="Todo OK")
    @api.response(406, "Subscripcion Inexistente")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('subscription', required=True, help="La subscripcion no puede estar en blanco")
        args = parser.parse_args()
        subscription = args['subscription']
        
        try:
            return TrafficDB().getMonthlyData(subscription)
        finally:
            APIDB().registerUsage(request.authorization.username, request.method, request.full_path, 0, request.remote_addr)
            
@api.route('/getyearly/')
@api.param('subscription', 'Numero de subscripcion a consultar')
class getYearlyTraffic(Resource):
    @auth.login_required
    @api.marshal_with(TrafficModel(api).get(), envelope='Traffic')
    @api.response(200, description="Todo OK")
    @api.response(406, "Subscripcion Inexistente")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('subscription', required=True, help="La subscripcion no puede estar en blanco")
        args = parser.parse_args()
        subscription = args['subscription']
        
        try:
            return TrafficDB().getYearlyData(subscription)
        finally:
            APIDB().registerUsage(request.authorization.username, request.method, request.full_path, 0, request.remote_addr)