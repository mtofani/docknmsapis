from flask_restx import reqparse
from flask_restx import Resource
from flask_restx import Namespace
from .nmssec import auth
from core.OIDs import OIDs
from core.SNMPLauncher import SNMPLauncher
from models.SNMPResponseModel import SNMPResponseModel
from core.MiscTools import MiscTools
from core.SNMPResponse import SNMPResponse
from flask import abort
from core.Nedy import Nedy

api = Namespace('status', description='Herramientas de Status GPON')

@api.route('/zte/onu/getStatus/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetStatus(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
        
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
        
        try:
            oid = OIDs().getOID("status") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGet(oid)
            
            return out
        except Exception as e:
            abort(504, str(e))
        finally:
            pass
        
@api.route('/zte/onu/getIpMgmt/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetIpMgmt(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
        
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            oid = OIDs().getOID("ipmng") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGetHex(oid)
            
            y = '.'.join(['%d' % x for x in out])
            
            sr = SNMPResponse(str("ipmgmt"), str(y))
            
            return sr
        except Exception as e:
            abort(504, str(e))
        finally:
            pass

@api.route('/zte/onu/getIpStechs/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetIpStechs(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
        
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
        
        try:
            oid = OIDs().getOID("ipStech") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGetRaw(oid)
            
            sr = SNMPResponse(str("ipstechs"), str(out))
            
            return sr
        except Exception as e:
            abort(504, str(e))
        finally:
            pass

@api.route('/zte/onu/getCaida/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetCaida(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
        
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            oid = OIDs().getOID("caida") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGetHex(oid)
            
            y = '.'.join(['%d' % x for x in out])
            
            sr = SNMPResponse(str("caida"), str(y))
            
            return sr
        except Exception as e:
            abort(504, str(e))
        finally:
            pass

@api.route('/huawei/onu/getStatus/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetHWStatus(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            oid = OIDs().getOID("statushw") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGet(oid)
            
            return out
        except Exception as e:
            abort(504, str(e))
        finally:
            pass

@api.route('/zte/onu/getSerialNumber/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetSerialNumber(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
        
        try:
            oid = OIDs().getOID("serialNumber") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGet(oid)
            
            return out
        except Exception as e:
            abort(504, str(e))
        finally:
            pass

@api.route('/zte/onu/getModel/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetModel(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            oid = OIDs().getOID("model") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGet(oid)
            
            return out
        except Exception as e:
            abort(504, str(e))
        finally:
            pass
        
@api.route('/zte/olt/getRxPw/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetRxPw(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            
            oid = OIDs().getOID("rxoltpw") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGet(oid)
            
            rxpw = int(out.value)
            
            if (rxpw != 65535000 and rxpw != -80000):
                rxpw = rxpw / 1000
            
            sr = SNMPResponse(str("rxpw"), str(rxpw))
            return sr
        except Exception as e:
            abort(504, str(e))
        finally:
            pass

@api.route('/zte/onu/getRxPw/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetOnuRxPw(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            
            oid = OIDs().getOID("rxonupw") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGet(oid)
            
            rxpw = int(out.value)
            
            if (rxpw != 65535 and rxpw != 0):
                rxpw = (rxpw * 0.002) - 30
            
            sr = SNMPResponse(str("rxpw"), str(rxpw))
            return sr
        except Exception as e:
            abort(504, str(e))
        finally:
            pass
        
@api.route('/zte/mbps/getTxMbps/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetTxMbps(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            
            oid = OIDs().getOID("txmbps") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGet(oid)
            
            mbps = (int(out.value) * 8) / 1000 / 1000
            
            sr = SNMPResponse(str("mbps"), str(mbps))
            return sr
        except Exception as e:
            abort(504, str(e))
        finally:
            pass
        
@api.route('/zte/mbps/getRxMbps/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetRxMbps(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            
            oid = OIDs().getOID("rxmbps") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGet(oid)
            
            mbps = (int(out.value) * 8) / 1000 / 1000
            
            sr = SNMPResponse(str("mbps"), str(mbps))
            return sr
        except Exception as e:
            abort(504, str(e))
        finally:
            pass

@api.route('/zte/onu/getDetail/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('user', 'Usuario de la OLT')
@api.param('password', 'Password de la OLT')
@api.param('port', 'Puerto a consultar')
@api.param('onu', 'Puerto a consultar')
class GetOnuDetailZTE(Resource):
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('user', required=True, help="El User no puede estar en blanco")
        parser.add_argument('password', required=True, help="El Password no puede estar en blanco")
        parser.add_argument('port', required=True, help="El puerto no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        user = args['user']
        password = args['password']
        port = args['port']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            portOnu = str(port) + ":" + str(onu)
            resp = Nedy().getOnuDetailZTE(ip, user, password, portOnu)
            
            return resp
        except Exception as e:
            abort(504, str(e))
        finally:
            pass

@api.route('/huawei/onu/getDetail/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('user', 'Usuario de la OLT')
@api.param('password', 'Password de la OLT')
@api.param('serial', 'SN de la ONU a consultar')
class GetOnuDetailHuawei(Resource):
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('user', required=True, help="El User no puede estar en blanco")
        parser.add_argument('password', required=True, help="El Password no puede estar en blanco")
        parser.add_argument('serial', required=True, help="El serial no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        user = args['user']
        password = args['password']
        serial = args['serial']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            resp = Nedy().getOnuDetailHuawei(ip, user, password, serial)
            
            return resp
        except Exception as e:
            abort(504, str(e))
        finally:
            pass


@api.route('/huawei/onu/getSerialNumber/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetHWSerialNumber(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            
            oid = OIDs().getOID("serialNumberhw") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGetHex(oid)
            
            y = '.'.join(['%d' % x for x in out])
            
            sr = SNMPResponse(str("sn"), str(y))
            return sr
        except Exception as e:
            abort(504, str(e))
        finally:
            pass

@api.route('/huawei/olt/getTxPw/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetHWTxPw(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            
            oid = OIDs().getOID("txoltpwhw") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGet(oid)
            
            txpw = int(out.value) / 100
            
            sr = SNMPResponse(str("txpw"), str(txpw))
            return sr
        except Exception as e:
            abort(504, str(e))
        finally:
            pass
        
@api.route('/huawei/mbps/getRxMbps/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetHWRxMbps(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            
            oid = OIDs().getOID("rxmbpshw") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGet(oid)
            
            mbps = (int(out.value) * 8) / 1000 / 1000
            
            sr = SNMPResponse(str("mbps"), str(mbps))
            return sr
        except Exception as e:
            abort(504, str(e))
        finally:
            pass

@api.route('/huawei/mbps/getTxMbps/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetHWTxMbps(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            
            oid = OIDs().getOID("txmbpshw") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGet(oid)
            
            mbps = (int(out.value) * 8) / 1000 / 1000
            
            sr = SNMPResponse(str("mbps"), str(mbps))
            return sr
        except Exception as e:
            abort(504, str(e))
        finally:
            pass
        

@api.route('/huawei/onu/getRxPw/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetHWRxPw(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            
            oid = OIDs().getOID("rxonupwhw") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGet(oid)
            
            rxpw = int(out.value) / 100
            
            sr = SNMPResponse(str("rxpw"), str(rxpw))
            return sr
        except Exception as e:
            abort(504, str(e))
        finally:
            pass

@api.route('/huawei/onu/getModel/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetHWModel(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            
            oid = OIDs().getOID("modelhw") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGet(oid)
            
            return out
        except Exception as e:
            abort(504, str(e))
        finally:
            pass

@api.route('/huawei/onu/getUptime/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetHWUptime(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            
            oid = OIDs().getOID("uptimehw") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGet(oid)
            
            upt = MiscTools().ConvertSectoDay((int(out.value)))
            
            sr = SNMPResponse(str("upt"), str(upt))
            return sr
        except Exception as e:
            abort(504, str(e))
        finally:
            pass

@api.route('/huawei/onu/getFirmware/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetHWFirmware(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
            
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            
            oid = OIDs().getOID("firmwarehw") + "." + if_index + "." + onu
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGet(oid)
            
            return out
        except Exception as e:
            abort(504, str(e))
        finally:
            pass
        
@api.route('/huawei/onu/getIpMgmt/')
@api.param('ip', 'ip del equipo que queres consultar')
@api.param('if_index', 'if index de la interface a consultar')
@api.param('onu', 'onu a consultar')
class GetHWIpMgmt(Resource):
    @auth.login_required
    @api.marshal_with(SNMPResponseModel(api).get(), envelope='SNMPResponse')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, help="La ip no puede estar en blanco")
        parser.add_argument('if_index', required=True, help="El Index no puede estar en blanco")
        parser.add_argument('onu', required=True, help="La ONU no puede estar en blanco")
        args = parser.parse_args()
        ip = args['ip']
        if_index = args['if_index']
        onu = args['onu']
        
        if MiscTools().isIP(ip) == False:
            abort(406, "IP en formato incorrecto")
            
        try:
            oid = OIDs().getOID("ipmnghw") + "." + if_index + "." + onu + ".0"
            snmp = SNMPLauncher(str(ip)) 
            out = snmp.executeGetHex(oid)
            
            y = '.'.join(['%d' % x for x in out])
            
            sr = SNMPResponse(str("ipmgmt"), str(y))
            return sr
        except Exception as e:
            abort(504, str(e))
        finally:
            pass