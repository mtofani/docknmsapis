from flask_restx import Resource, Namespace
from core.APIDB import APIDB
from core.HealthDB import HealthDB
from flask import Flask, jsonify
import datetime
import time

HTTP_200_OK = 200
HTTP_500_SERVER_ERROR = 500

# Estado de la base de datos
DB_UP = 'OK'
DB_ERROR = 'ERROR'

api = Namespace('health', description='Chequeos de salud')

@api.route('/nedyGPONDiscovery')
class GetDiscoveryHealth(Resource):
    @api.doc(responses={
        HTTP_200_OK: 'Todo OK',
        HTTP_500_SERVER_ERROR: 'Server Error'
    })
    def get(self):
        try:
            start_time = time.time()
            res = HealthDB().getLatestGPONDiscovery()
            fecha_actual = datetime.datetime.now()

            res_error = []  

            for item in res:
                fecha_obj = item['fecha']
                fecha_str = fecha_obj.strftime('%Y-%m-%d %H:%M:%S')  # Formato: 'YYYY-MM-DD HH:mm:SS'
                item['fecha'] = fecha_str

                # Verificar si la fecha es más antigua de 24 horas o SNMP es igual a 0, y agregar a res_error
                diferencia = fecha_actual - fecha_obj
                if diferencia.total_seconds() / 3600 > 24 or item['snmp'] == 0:
                    res_error.append(item)

            print(res_error)
            print(res)
            end_time = time.time()
            elapsed_time_ms = (end_time - start_time) * 1000


            data = {
                'name': 'NEDY',
                'status': 'OK' if not res_error else 'ERROR',
                'elapsed_time_ms': elapsed_time_ms,
                'olts': res if not res_error else res_error,
              
            }

            if not res_error:  # Si res_error está vacío
                return data, HTTP_200_OK
            else:
            
                return data, HTTP_500_SERVER_ERROR

        except Exception as e:
            print(e)

        data = {
            'name': 'NEDY',
            'status': 'ERROR'
        }
        return data, HTTP_500_SERVER_ERROR

@api.route('/nedydb')
class GetNedyDBHealth(Resource):
        @api.doc(responses={
                HTTP_200_OK: 'Todo OK',
                HTTP_500_SERVER_ERROR: 'Server Error'
            })

        def get(self):
            try:
              
                start_time = time.time()

                res = HealthDB().getProperty("snmp_comm")

                end_time = time.time()

                # Calcular la cantidad de tiempo transcurrido en milisegundos
                elapsed_time_ms = (end_time - start_time) * 1000

                # Datos de respuesta
                data = {
                    'name': 'NEDYDB',
                    'status': DB_UP,
                    'elapsed_time_ms': elapsed_time_ms  
                }

                return data, HTTP_200_OK

            except Exception as e:
              
                print(e)
              
                data = {
                    'name': 'NEDYDB',
                    'status': DB_ERROR,
                    'elapsed_time_ms': 0  
                }
                return data, HTTP_500_SERVER_ERROR   


@api.route('/apidb')
class GetApiDBHealth(Resource):
    @api.doc(responses={
        HTTP_200_OK: 'Todo OK',
        HTTP_500_SERVER_ERROR: 'Server Error'
    })
    def get(self):
        try:
            start_time = time.time()
            res = APIDB().getProperty("nedydb.host") 
            end_time = time.time()
            elapsed_time_ms = (end_time - start_time) * 1000
            if (res):  
            
                data = {
                'name': 'APIDB',
                'status': DB_UP,
                'elapsed_time_ms': elapsed_time_ms
                }
                return data, HTTP_200_OK
           

        except Exception as e:
            
            print(e)

            data = {
                'name': 'APIDB',
                'status': DB_ERROR
            }
            return data, HTTP_500_SERVER_ERROR