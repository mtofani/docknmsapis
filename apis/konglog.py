from flask import request
from flask_restx import Resource
from core.APIDB import APIDB
from flask_restx import Namespace


api = Namespace('kong', description='Loggeo de Uso de APIs KONG')

@api.route('/log/')
class Log(Resource):
    def post(self):
        data = request.get_json(force=True)

        try:
            if 'consumer' not in data:
                method = data['request']['method']
                full_path = data['request']['uri']
                scode = data['response']['status']
                uname = 'unknown'
                path = data['service']['path']
            else:
                method = data['request']['method']
                full_path = data['request']['uri']
                scode = data['response']['status']
                uname = data['consumer']['username']
                path = data['service']['path']
                
                APIDB().registerUsageComplete(uname, method, full_path, path, scode, request.remote_addr)
        except Exception as e:
            print(e)
