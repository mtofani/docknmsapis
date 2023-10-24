from flask_restx import reqparse
from flask_restx import Resource
from flask_restx import Namespace
from pymysql import IntegrityError
from core.netpix_modules.InvalidPicException import InvalidPicException
from core.netpix_modules.NetPixDB import NetPixDB
from core.netpix_modules.OltModels import OltModels
from core.netpix_modules.Statuses import Statuses
from core.netpix_modules.UnreachableIPException import UnreachableIPException
from core.MiscTools import MiscTools
from flask import abort
from core.netpix_modules.NetPix import NetPix
from core.MiscTools import MiscTools
import json
from flask import jsonify



api = Namespace('netpix', description='Sistema de fotos de red')


@api.route('/takePic/')
@api.param('ipPorts', 'Contatenacion de IPs y Puertos: 172.16.23.156,1/3/6|172.16.23.154,1/3/3')
@api.param('name', 'Nombre de la tarea')
class TakePic(Resource):
    # @api.marshal_with(PicModel(api).get(), envelope='PicModel')
    @api.response(200, description="Todo OK")
    @api.response(406, "IP o puerto en formato incorrecto")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ipPorts', required=True, help="ipPorts no puede estar en blanco")
        parser.add_argument('name', required=True, help="El nombre no puede estar en blanco")
        args = parser.parse_args()
        ipPorts = args['ipPorts']
        name = args['name']

        np = NetPix()
        

        listIpPort = str(ipPorts).split("|")

        #validaciones - la ip es correcta? el puerto es correcto? hay un caracter que escape?

        for ipPort in listIpPort:
            ip,port = str(ipPort).split(",")
            if MiscTools().isIP(ip) == False:
                abort(406,"IP incorrecta")
            if MiscTools().isPortGpon(port) == False:
                abort(406,"Puerto incorrecto")
        try:
            pic = np.takePicGpon(ipPorts,name)
            picid = np.uploadPicToDB(pic)
            pic.id = picid
            resp = json.loads(json.dumps(pic, default=lambda o: o.__dict__))
            return jsonify(resp)
        except UnreachableIPException as e:
            abort(504,"IP inalcanzable")
        except IntegrityError as ie:
            abort(504,"Nombre de foto duplicada")
        except Exception as e:
            abort(504,e)



@api.route('/getPic/')
@api.param('picId', 'Numero de la foto que se quiere recuperar')
class GetPic(Resource):
    # @api.marshal_with(PicModel(api).get(), envelope='PicModel')
    @api.response(200, description="Todo OK")
    @api.response(406, "Pic ID no encontrado")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('picId', required=True, help="picId no puede estar en blanco")
        args = parser.parse_args()
        picId = args['picId']

        np = NetPix()

        try:
            pic = np.getPicFromDB(picId)
            resp = json.loads(json.dumps(pic, default=lambda o: o.__dict__))
            return jsonify(resp)
        except InvalidPicException as ipe:
            abort(406,"No se encontró la foto")
        except Exception as e:
            abort(504,e)



@api.route('/comparePics/')
@api.param('pic2', 'ID de la foto mas nueva')
@api.param('pic1', 'ID de la foto mas vieja')
class ComparePic(Resource):
    # @api.marshal_with(PicModel(api).get(), envelope='PicModel')
    @api.response(200, description="Todo OK")
    @api.response(406, "Pic ID no encontrado")
    @api.response(504, "Error")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('pic1', required=True, help="pic1 no puede estar en blanco")
        parser.add_argument('pic2', required=True, help="pic2 no puede estar en blanco")
        args = parser.parse_args()
        pic1 = args['pic1']
        pic2 = args['pic2']

        np = NetPix()

        try:
            comparison = np.comparePicsById(pic2,pic1)
            resp = json.loads(json.dumps(comparison,default=lambda o:o.__dict__))
            return jsonify(resp)
        except InvalidPicException:
            abort(406,"No se encontró la foto")
        except Exception as e:
            abort(504,"Falló")



@api.route('/getStatuses/')
class GetStatuses(Resource):
    # @api.marshal_with(PicModel(api).get(), envelope='PicModel')
    @api.response(200, description="Todo OK")
    @api.response(406, "Pic ID no encontrado")
    @api.response(504, "Error")
    
    def get(self):

        try:
            statuses = Statuses()
            resp = json.loads(json.dumps(statuses,default = lambda o:o.__dict__))
            return jsonify(resp)
        except InvalidPicException:
            abort(406,"No se encontró la foto")
        except Exception as e:
            abort(504,"Falló")

@api.route('/getPicsList/')
class GetPicsList(Resource):
    # @api.marshal_with(PicModel(api).get(), envelope='PicModel')
    @api.response(200, description="Todo OK")
    @api.response(406, "Pics no encontradas")
    @api.response(504, "Error")
    
    def get(self):

        try:
            pics = NetPixDB().selectPics()
            objPics = []
            for p in pics:
                objPics.append({
                    "pic":p[0],
                    "name":p[1],
                    "date":p[2].strftime("%m/%d/%Y, %H:%M:%S")
                })
            # resp = json.dumps(objPics)
            return jsonify(objPics)
        except InvalidPicException:
            abort(406,"No se encontró la foto")
        except Exception as e:
            abort(504,"Falló")


@api.route('/getOltModels/')
class GetOltModels(Resource):
    # @api.marshal_with(PicModel(api).get(), envelope='PicModel')
    @api.response(200, description="Todo OK")
    @api.response(406, "Pic ID no encontrado")
    @api.response(504, "Error")
    
    def get(self):

        try:
            oltModels = OltModels()
            resp = json.loads(json.dumps(oltModels,default=lambda o:o.__dict__))
            return jsonify(resp)
        except InvalidPicException:
            abort(406,"No se encontró la foto")
        except Exception as e:
            abort(504,"Falló")
