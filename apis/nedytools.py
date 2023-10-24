from flask import request
from flask import jsonify
from flask_restx import reqparse
from core.Nedy import Nedy
from flask_restx import Resource
from core.APIDB import APIDB
from models.DeviceModel import DeviceModel
from core.MiscTools import MiscTools
from flask_restx import Namespace
from .nmssec import auth
from pymysql.err import IntegrityError
from models.InterfaceModel import InterfaceModel
from models.OnuModel import OnuModel


api = Namespace('tools', description='Herramientas Nedy')


@api.route('/nedy/getDevice/')
@api.param('ip', 'ip del equipo que queres consultar')
class NedyGetDevice(Resource):
    @auth.login_required
    @api.marshal_with(DeviceModel(api).get(), envelope='device')
    @api.response(200, description="Todo OK", model=DeviceModel(api).get())
    @api.response(406, "IP en formato incorrecto")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        
        try:
            if MiscTools().isIP(ip):
                resp = Nedy().getDevice(ip)
                #resp.status_code = 200
                return resp
            else:
                resp = jsonify({'error': 'La IP ' + ip + ' esta mal formateada.'})
                resp.status_code = 406
                return resp
        except Exception:
            pass
        finally:
            APIDB().registerUsageComplete(request.authorization.username, request.method, request.full_path, request.path, 0, request.remote_addr)

@api.route('/nedy/getDevicebyNetwork/')
@api.param('ip', 'ip del equipo que queres consultar')
class NedyGetDevicebyNetwork(Resource):
    @auth.login_required
    @api.marshal_with(DeviceModel(api).get(), envelope='device')
    @api.response(200, description="Todo OK", model=DeviceModel(api).get())
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        
        resp = Nedy().getDevicebyNetwork(ip)
        #resp.status_code = 200
        return resp
    
@api.route('/nedy/getInfoByHostname/')
@api.param('hostname', 'hostname del equipo que queres consultar')
class NedygetInfoByHostname(Resource):
    @auth.login_required
    @api.marshal_with(DeviceModel(api).get(), envelope='device')
    @api.response(200, description="Todo OK", model=DeviceModel(api).get())
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hostname', required=True, help="El hostname no puede estar en blanco")
        args = parser.parse_args()
        hostname = args['hostname']
        
        resp = Nedy().getInfoByHostname(hostname)
        #resp.status_code = 200
        return resp

@api.route('/nedy/getNetworks/')
class NedyGetRegisteredNetworks(Resource):
    @auth.login_required
    @api.response(200, description="Todo OK")
    def get(self):
        
        try:
            resp = Nedy().getRegisteredNetworks()
            return resp
        except Exception:
            pass
        finally:
            APIDB().registerUsageComplete(request.authorization.username, request.method, request.full_path, request.path, 0, request.remote_addr)
            
@api.route('/nedy/getInfoByAlias/')
@api.param('value', 'Valor por el cual realizar la busqueda')
class NedyGetByAlias(Resource):
    @auth.login_required
    @api.marshal_with(InterfaceModel(api).get(), envelope='Interface')
    @api.response(200, description="Todo OK", model=InterfaceModel(api).get())
    @api.response(406, "Valor inexistente")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('value', required=True, help="El valor no puede estar en blanco")
        args = parser.parse_args()
        value = args['value']
        
        try:
            resp = Nedy().getInfoByAlias(value)
            #resp.status_code = 200
            return resp
        except Exception as e:
            print(e)
        finally:
            APIDB().registerUsageComplete(request.authorization.username, request.method, request.full_path, request.path, 0, request.remote_addr)

@api.route('/nedy/getInfoByPort/')
@api.param('ip', 'IP de la OLT')
@api.param('port', 'Puerto de la OLT (format: gpon_1/2/3)')
@api.param('onu', 'ONU del Puerto')
class NedyGetInfoByPort(Resource):
    #@auth.login_required
    @api.marshal_with(OnuModel(api).get(), envelope='Onus')
    @api.response(200, description="Todo OK", model=InterfaceModel(api).get())
    @api.response(406, "IP Mal formateada")

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="El valor no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        
        parser.add_argument('port', required=True, help="El valor no puede estar en blanco")
        args = parser.parse_args()
        port = args['port']

        parser.add_argument('onu', required=False, default=0)
        args = parser.parse_args()
        onu = args['onu']

        try:
            resp = Nedy().getInfoByPort(ip, port, onu)
            return resp
        except Exception as e:
            resp = {500, e}
            return resp
        

@api.route('/nedy/getInfoByNameOrDescr/')
@api.param('value', 'Valor por el cual realizar la busqueda')
class NedyGetByNameOrDescr(Resource):
    @auth.login_required
    @api.marshal_with(InterfaceModel(api).get(), envelope='Interface')
    @api.response(200, description="Todo OK", model=InterfaceModel(api).get())
    @api.response(406, "Valor inexistente")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('value', required=True, help="El valor no puede estar en blanco")
        args = parser.parse_args()
        value = args['value']
        
        try:
            resp = Nedy().getInfoByNameOrDescr(value)
            #resp.status_code = 200
            return resp
        except Exception as e:
            print(e)
        finally:
            APIDB().registerUsageComplete(request.authorization.username, request.method, request.full_path, request.path, 0, request.remote_addr)

@api.route('/nedy/insertnewnetwork/')
@api.param('net', 'red para agregar al descubrimiento')
class NedyInsertNetwork(Resource):
    @auth.login_required
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(409, "La RED ya Existe")
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('net', required=True, help="La red no puede estar en blanco")
        args = parser.parse_args()
        net = args['net']
        
        ip = net.split("/")[0]
        
        try:
            if MiscTools().isIP(ip):
                Nedy().inserNewNetwork(net)
                resp = jsonify({'message': 'Red cargada correctamente'})
                resp.status_code = 200
                return resp
            else:
                resp = jsonify({'error': 'RED mal formateada'})
                resp.status_code = 406
                return resp
        except IntegrityError:
            resp = jsonify({'error': 'La RED ya Existe'})
            resp.status_code = 409
            return resp
        except Exception:
            pass
        finally:
            APIDB().registerUsageRedux(request, resp)

@api.route('/nedy/inseradditionalinfo/')
@api.param('model', 'Modelo donde se debe aplicar el descubrimiento')
@api.param('name', 'Nombre identificador')
@api.param('oid', 'OID a consultar diariamente')
class NedyInsertAddInfo(Resource):
    @auth.login_required
    @api.response(200, description="Todo OK")
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('model', required=True, help="El modelo no puede estar vacio")
        parser.add_argument('name', required=True, help="El nombre no puede estar vacio")
        parser.add_argument('oid', required=True, help="El OID no puede estar vacio")
        args = parser.parse_args()
        model = args['model']
        name = args['name']
        oid = args['oid']
        
        try:
            Nedy().inserAddInfoRequest(model, name, oid)
            resp = jsonify({'message': 'Pedido cargado correctamente'})
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({'message': str(e.message)})
            resp.status_code = 500
            return resp
        finally:
            APIDB().registerUsageRedux(request, resp)


@api.route('/nedy/fping/')
@api.param('net', 'red a pinggear')
@api.param('mask', 'mascara en formato CIDR o NETMASK')
@api.response(200, "Todo OK")
@api.response(406, "Formato incorrecto")
class NedyPing(Resource):
    @auth.login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('net', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('mask', required=True, help="La mascara no puede estar en blanco")
        args = parser.parse_args()
    
        net = args['net']
        mask = args['mask']
        
        if len(mask) > 2:
            umask = MiscTools().getCIDR(mask)
        else:
            umask = mask
            
        print(umask)
        
        try:
            if MiscTools().isIP(net):
                resp = jsonify(Nedy().ping(net, umask))
                resp.status_code = 200
                return resp
            else:
                resp = jsonify({'error': 'La IP o MASK esta mal formateada.'})
                resp.status_code = 406
                return resp
        finally:
            APIDB().registerUsageRedux(request, resp)


@api.route('/nedy/snmp/')
@api.param('ip', 'ip del equipo a consultar')
@api.param('comm', 'comunidad del equipo')
@api.param('oid', 'oid a consultar')
@api.response(200, "Todo OK")
@api.response(406, "Formato incorrecto")
class NedySNMP(Resource):
    @auth.login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('comm', required=True, help="La comunidad no puede estar en blanco")
        parser.add_argument('oid', required=True, help="El OID no puede estar en blanco")
        args = parser.parse_args()
    
        ip = args['ip']
        comm = args['comm']
        oid = args['oid']
        
        try:
            if MiscTools().isIP(ip):
                resp = jsonify(Nedy().runByRequest(ip, comm, oid))
                resp.status_code = 200
                return resp
            else:
                resp = jsonify({'error': 'La IP ' + ip + ' esta mal formateada.'})
                resp.status_code = 406
                return resp
        finally:
            APIDB().registerUsageRedux(request, resp)
    

@api.route('/nedy/discovery/')
@api.param('ip', 'ip del equipo a descubrir')
@api.response(200, "Todo OK")
@api.response(406, "Formato incorrecto")
class NedyDiscovery(Resource):
    @auth.login_required
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        args = parser.parse_args()
    
        ip = args['ip']
        

        try:
            if MiscTools().isIP(ip):
                resp = jsonify(Nedy().discoByRequest(ip))
                resp.status_code = 200
                return resp
            else:
                resp = jsonify({'error': 'La IP ' + ip + ' esta mal formateada.'})
                resp.status_code = 406 
                return resp
        finally:
            APIDB().registerUsageRedux(request, resp)


@api.route('/nedy/version/')
class NedyVersion(Resource):
    def get(self):
        return jsonify(Nedy().version())
