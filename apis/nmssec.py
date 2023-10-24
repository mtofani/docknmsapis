from flask import json
from flask import request, Response
from flask import jsonify
from flask_restx import reqparse
from flask_restx import Namespace
from flask_restx import Resource
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from core.APIDB import APIDB
from pymysql.err import IntegrityError


api = Namespace('sec', description='Centro de login NMS')


auth = HTTPBasicAuth()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def save_to_db(self):
        APIDB().registerUser(self.username, self.password)
    
    @classmethod
    def find_by_username(cls, username):
        return APIDB().getUser(cls, username)


@api.route('/register')
@api.param('username', 'nombre de usuario')
@api.param('password', 'password del usuario')
@api.response(409, "El usuario ya existe")
@api.response(200, "Usuario creado correctamente")
class register_user(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', required=True)
            parser.add_argument('password', required=True)
            args = parser.parse_args()
            
            username = args['username']
            password = args['password']
        
            User(username, generate_password_hash(password)).save_to_db()
            
            resp = jsonify({'message': "Usuario creado correctamente"})
            resp.status_code = 200
            return resp
        except IntegrityError:
            resp = jsonify({'error': "El usuario " + username + " ya existe."})
            resp.status_code = 409
            return resp
        except Exception as e:
            resp = jsonify({'error': "Error desconocido"})
            resp.status_code = 401
            print(e)
            return resp
        finally:
            APIDB().registerUsage(username, request.method, request.path, resp.status_code, request.remote_addr)


@api.route('/deleteuser')
@api.param('user', 'Usuario a Eliminar')
class DeleteUser(Resource):
    @auth.login_required
    def delete(self):
        req_data = {}
        parser = reqparse.RequestParser()
        parser.add_argument('user', required=True, help="El Usuario a Eliminar")
        args = parser.parse_args()
    
        user = args['user']
        
        try:
            APIDB().deleteUser(user)
            return jsonify({'message': 'Usuario eliminado correctamente'})
        finally:
            resp = Response(json.dumps(req_data, indent=4, default=str), mimetype='application/json')
            APIDB().registerUsage(request.authorization.username, request.method, request.full_path, resp.status_code)


@auth.verify_password
def login_user(username, password):
    user = User.find_by_username(username)
    
    if user and check_password_hash(user.password, password):
        return True
    else:
        return False
