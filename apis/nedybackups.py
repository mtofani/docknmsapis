import logging
from flask import jsonify, request,json,make_response
from flask_restx import Namespace, Resource, fields
from flask_httpauth import HTTPBasicAuth
from core.NedyQuerys import Nedy
from core.MiscTools import MiscTools
from .nmssec import auth
import re

from core.APIDB import APIDB
from core.BACKUPSDB import BACKUPSDB


# configure root logger
logging.basicConfig(level=logging.INFO)

##ns1 = api.namespace('api/nedy', description='test')
api = Namespace('backups', description='backups NMS')


def dateValidator(fecha):
    txt = fecha
    x = re.search('^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$', txt)
    return x

def ipValidator(ip):
    txt = ip
    x = re.search('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', txt)
    return x

def tupToJSON(tup):
    outJSON = { 'response': []}
    innerTup = tup
    for response in innerTup:
        ip = response[0]
        fecha = response[1]
        outJSON['response'].append({'ip': ip, 'fecha':str(fecha)})
    return outJSON

def responseValidator(res):
    if res == None:
        return True

@api.route('/getBackUpByIP/<string:ip>/<string:fecha>')
@api.doc(params={ 'ip': 'la ip del equipo que buscas', 'fecha': 'filtro OPCIONAL de fecha  - Formato YYYY-MM-DD'}) 
@api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 406: 'Not Acceptable', 500: 'Mapping Key Error' })
class getBackUpByIP(Resource):
    @auth.login_required
    #@api.marshal_with(model)
    def get(self, ip, fecha):

        if dateValidator(fecha):
            if ipValidator(ip):
                pass
            else:
                response = make_response("Error en formato de IP", 406)
                response.mimetype = "text/plain"
                return response
        else:
            response = make_response("Error en formato de Fecha", 406)
            response.mimetype = "text/plain"
            return response

        try:
            rows=BACKUPSDB().getBackUpByIP(ip, fecha)

            if responseValidator(rows):
                response = make_response({"No hay backup de esa ip mono"}, 406)
                response.mimetype = "text/plain"
                return response
            
            string=str(rows)
            string = string.replace('\\r', '\r').replace('\\n','\n').replace("',))","").replace("(('","")
        
            response = make_response(string, 200)
            response.mimetype = "text/plain"
            return response
        
        except Exception as e:
            resp = {500, "Error - {}".format(e)}
            return resp
        finally:
            print("LA IP")

@api.route('/getBackUpLast/<string:ip>')
@api.doc(params={ 'ip': 'la ip del equipo que buscas'}) 
@api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 406: 'Not Acceptable', 500: 'Mapping Key Error' })
class getBackUpLast(Resource):
    @auth.login_required
    #@api.marshal_with(model)
    def get(self, ip):

        if ipValidator(ip):
            pass
        else:
            response = make_response("Error en formato de IP", 406)
            response.mimetype = "text/plain"
            return response

        try:
            rows=BACKUPSDB().getBackUpLast(ip)

            if responseValidator(rows):
                response = make_response("No hay backup de esa ip mono", 406)
                response.mimetype = "text/plain"
                return response
            
            response = tupToJSON(rows)
            response = make_response(response, 200)
            response.mimetype = "text/plain"
            return response
        
        except Exception as e:
            resp = {500, "Error - {}".format(e)}
            return resp
        finally:
            print("LA IP")

@api.route('/getBackUpList/<string:ip>/<string:fechaInit>/<string:fechaEnd>')
@api.doc(params={ 'ip': 'la ip del equipo que buscas', 'fechaInit':'Fecha de Inicio', 'fechaEnd':'Fecha de Fin'}) 
@api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 406: 'Not Acceptable', 500: 'Mapping Key Error' })
class getBackUpList(Resource):
    @auth.login_required
    #@api.marshal_with(model)
    def get(self, ip, fechaInit, fechaEnd):
        print("fechaEnd - {} / fechaInit - {}".format(fechaEnd, fechaInit))
        if dateValidator(fechaInit) and dateValidator(fechaEnd):
            if ipValidator(ip):
                pass
            else:
                response = make_response("Error en formato de IP", 406)
                response.mimetype = "text/plain"
                return response
        else:
            response = make_response("Error en formato de Fecha", 406)
            response.mimetype = "text/plain"
            return response

        try:
            rows=BACKUPSDB().getBackUpList(ip,fechaInit,fechaEnd)

            if responseValidator(rows):
                response = make_response("No hay backup de esa ip mono", 406)
                response.mimetype = "text/plain"
                return response
            
            response = tupToJSON(rows)
            response = make_response(response, 200)
            response.mimetype = "text/plain"
            return response
        
        except Exception as e:
            resp = {500, "Error - {}".format(e)}
            return resp
        finally:
            print("LA IP")

