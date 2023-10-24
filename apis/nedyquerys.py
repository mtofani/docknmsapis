import logging
from flask import jsonify, request,json
from flask_restx import Namespace, Resource, fields
from flask_httpauth import HTTPBasicAuth
from core.NedyQuerys import Nedy
from core.MiscTools import MiscTools
from .nmssec import auth

from core.APIDB import APIDB


# configure root logger
logging.basicConfig(level=logging.INFO)

##ns1 = api.namespace('api/nedy', description='test')
api = Namespace('consultas', description='Consultas NEDY')


@api.route('/alldevices') 
@api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
class AllEquipments(Resource):
    @auth.login_required
    #@api.marshal_with(model)
    def get(self, **kwargs):
        #todoDato = TodoDao(todo_id='my_todo', task='Remember the milk')
        ##return TodoDao(todo_id='my_todo', task='Remember the milk')
        try:
           
            
            rows=Nedy().getAllDevices()
            resp=jsonify(rows)
            
            resp.status_code=200
            
           
           
            #,request.method,request.path,resp.status_code)
            return resp
        except Exception as e:
            print(e)
        finally:
            print("LA IP")
            print(request.remote_addr)  
            APIDB().registerUsage(request.authorization.username, request.method, request.path, resp.status_code, request.remote_addr)

@api.route('/allbymodel/<string:model>')
@api.doc(responses={ 200: 'OK', 400: 'Parametros incorrectos', 500: 'Mapping Key Error' })
@api.doc(params={ 'model': 'El modelo que buscas'})
class ALlByModel(Resource):
    @auth.login_required
    #@api.marshal_with(model)   
   ## def get(self, **kwargs):
    def get(self, model):
      
        try:
            
            modelo=model
            rows=Nedy().getAllbyModel(modelo)
            resp=jsonify(rows)
            resp.status_code=200
            return resp
        except Exception as e:
            print(e)
        finally:
            APIDB().registerUsage(request.authorization.username, request.method, request.path, resp.status_code, request.remote_addr)

@api.route('/interfacesIP/<string:ip>')
@api.doc(responses={ 200: 'OK', 400: 'Parametros NO Correctos', 500: 'Mapping Key Error' })
@api.doc(params={ 'ip': 'la ip del equipo que buscas'})
class InterfacesOfIP(Resource):
    @auth.login_required
    def get(self, ip):
      
        try:
           
            #conn=mysql.connect()
           # cur=conn.cursor(pymysql.cursors.DictCursor)
            if (MiscTools.isIP(self,ip)):
               
                rows=Nedy().getInferfacesIP(ip)
                resp=jsonify(rows)
                #resp=jsonify(rows)
                resp.status_code=200
            else:
              
                resp=jsonify("No ingresaste una ip chantun xD")
                resp.status_code=13000
            
             
            return resp
        except Exception as e:
            print(e)
        finally:
            APIDB().registerUsage(request.authorization.username, request.method, request.path, resp.status_code, request.remote_addr)

@api.route('/getOnus/<string:ip>' , defaults={'port': None})
@api.route('/getOnus/<string:ip>/<int:port>')
@api.doc(responses={ 200: 'OK', 400: 'Parametros incorrectos', 500: 'Mapping Key Error' })
@api.doc(params={ 'ip': 'la ip del equipo que buscas sus ONUS','port': 'Es opcional'})
class getOnus(Resource):
    @auth.login_required
    ##def get(self, ip, puerto):
    def get(self, ip, port):
       
        #todoDato = TodoDao(todo_id='my_todo', task='Remember the milk')
        ##return TodoDao(todo_id='my_todo', task='Remember the milk')
        try:
           
            rows=Nedy().getOnus(ip,port)
            resp=jsonify(rows)
            resp.status_code=200
            APIDB().registerUsage(request.authorization.username, request.method, request.path, resp.status_code, request.remote_addr)
            return resp
        except Exception as e:
            print(e)
        finally:
            pass

@api.route('/getAddInfo/<string:ip>' )
@api.doc(responses={ 200: 'OK', 400: 'Parametros incorrectos', 500: 'Mapping Key Error' })
@api.doc(params={ 'ip': 'la ip del equipo que buscas sus info adicional'})
class getAddInfo(Resource):
    @auth.login_required
    
    def get(self, ip):
       
        try:
           
      
            rows=Nedy().getAddInfo(ip)
            resp=jsonify(rows)
            resp.status_code=200
            return resp

        
        except Exception as e:
            print(e)
        finally:
            APIDB().registerUsage(request.authorization.username, request.method, request.path, resp.status_code, request.remote_addr)
@api.route('/getNetworks' )
@api.doc(responses={ 200: 'OK', 400: 'Parametros incorrectos', 500: 'Mapping Key Error' })
class getNetworks(Resource):
    @auth.login_required
    
    def get(self):
       
        try:
         
            rows=Nedy().getNetworks()
            resp=jsonify(rows)
            resp.status_code=200
            
            return resp
        except Exception as e:
            print(e)
        finally:
            APIDB().registerUsage(request.authorization.username, request.method, request.path, resp.status_code, request.remote_addr)




    
