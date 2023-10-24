import logging
from flask import jsonify, request,json
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
from  core.Nedy import Nedy
auth = HTTPBasicAuth()


# configure root logger
logging.basicConfig(level=logging.INFO)

##ns1 = api.namespace('api/nedy', description='test')
api = Namespace('consultas', description='Consultas NEDY')



def getUsers():
    users = {
    "admin": generate_password_hash("api"),
    "maxi": generate_password_hash("tofa")
    }
    return users

@auth.verify_password
def verify_password(username, password):
    users=getUsers()
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

   
  

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
            return resp
        except Exception as e:
            print(e)
        finally:
           pass

@api.route('/allbymodel/<string:model>')
@api.doc(responses={ 200: 'OK', 400: 'Parametros incorrectos', 500: 'Mapping Key Error' })
@api.doc(params={ 'model': 'El modelo que buscas'})
class ALlByModel(Resource):
    @auth.login_required
    #@api.marshal_with(model)   
   ## def get(self, **kwargs):
    def get(self, model):
        #todoDato = TodoDao(todo_id='my_todo', task='Remember the milk')
        ##return TodoDao(todo_id='my_todo', task='Remember the milk')
        try:
            
            modelo=model
            rows=Nedy().getAllbyModel(modelo)
            resp=jsonify(rows)
            resp.status_code=200
            api.logger.info("HTTP OK 200\n ALL")
            return resp
        except Exception as e:
            print(e)
        finally:
          pass

@api.route('/interfacesIP/<string:ip>')
@api.doc(responses={ 200: 'OK', 400: 'Parametros NO Correctos', 500: 'Mapping Key Error' })
@api.doc(params={ 'ip': 'la ip del equipo que buscas'})
class InterfacesOfIP(Resource):
    def get(self, ip):
      
        try:
           
       
            #conn=mysql.connect()
           # cur=conn.cursor(pymysql.cursors.DictCursor)
            if (esIP(ip)):
               
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
           pass

@api.route('/getOnus/<string:ip>' , defaults={'port': None})
@api.route('/getOnus/<string:ip>/<int:port>')
@api.doc(responses={ 200: 'OK', 400: 'Parametros incorrectos', 500: 'Mapping Key Error' })
@api.doc(params={ 'ip': 'la ip del equipo que buscas sus ONUS','port': 'Es opcional'})
class getOnus(Resource):
    ##def get(self, ip, puerto):
    def get(self, ip, port):
       
        #todoDato = TodoDao(todo_id='my_todo', task='Remember the milk')
        ##return TodoDao(todo_id='my_todo', task='Remember the milk')
        try:
           
            rows=Nedy().getOnus(ip,port)
            resp=jsonify(rows)
            resp.status_code=200
            return resp
        except Exception as e:
            print(e)
        finally:
            pass

@api.route('/getAddInfo/<string:ip>' )
@api.doc(responses={ 200: 'OK', 400: 'Parametros incorrectos', 500: 'Mapping Key Error' })
@api.doc(params={ 'ip': 'la ip del equipo que buscas sus info adicional'})
class getAddInfo(Resource):
    
    def get(self, ip):
       
        try:
           
            query="SELECT * from add_info a where a.ip ='"+ip+"'"
              
            cur.execute(query)
            rows = cur.fetchall()
            resp=jsonify(rows)
            resp.status_code=200
            return resp
        except Exception as e:
            print(e)
        finally:
           pass

@api.route('/getNetworks' )
@api.doc(responses={ 200: 'OK', 400: 'Parametros incorrectos', 500: 'Mapping Key Error' })
class getNetworks(Resource):
    
    def get(self):
       
        try:
         
                
            query="SELECT * from networks"
            cur.execute(query)
            rows = cur.fetchall()
            resp=jsonify(rows)
            resp.status_code=200
            return resp
        except Exception as e:
            print(e)
        finally:
            pass

def esIP(ip):
    addr = ip
  
    try:
        ipaddress.ip_address(addr)
        print("Valid IP")
        return True
    except ValueError as e:
        print("Invalid IP")
        return False
        


    
