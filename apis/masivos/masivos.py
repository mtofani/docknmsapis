from ast import arg
from email.policy import default
from flask_restx import reqparse
from flask_restx import Resource
from flask_restx import Namespace, fields
from flask import jsonify, request,json
from core.CamachoDB import CamachoDB
from core.MasivosDB import MasivosDB
from models.EventModel import EventModel
from datetime import datetime


api = Namespace('operaciones', description='Herramientas para la administracion de Tareas de Operaciones')

@api.route('/getStatusCodes/')
class GetStatusCodes(Resource):
    @api.response(200, description="Todo OK")
    
    def get(self):
        try:
            resp = MasivosDB().getStatusCodes()
            return resp
        except Exception as e:
            raise

@api.route('/getEventTypes/')
class GetEventTypes(Resource):
    @api.response(200, description="Todo OK")
    
    def get(self):
        try:
            resp = MasivosDB().getEventTypes()
            return resp
        except Exception as e:
            raise

@api.route('/getAllEvents/')
class GetAllEvents(Resource):
    @api.marshal_with(EventModel(api).get(), envelope='event')
    @api.response(200, description="Todo OK", model=EventModel(api).get())

    def get(self):
        try:
            resp = MasivosDB().getEvents()
            return resp
        except Exception as e:
            raise

@api.route('/getEventsFiltered/')
@api.doc(params={'event_type': 'Tipo de Evento'})
@api.doc(params={'event_status': 'Estado del Evento'})
class GetEventsFiltered(Resource):
    @api.marshal_with(EventModel(api).get(), envelope='event')
    @api.response(200, description="Todo OK", model=EventModel(api).get())
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('event_type', type=int, default=0)
        parser.add_argument('event_status', type=int, default=0)
        args = parser.parse_args()

        try:
            resp = MasivosDB().getEventsFiltered(type=args['event_type'], status=args['event_status'])
            return resp
        except Exception as e:
            resp = {500, "Error"}
            return resp

@api.route('/getEventById/<int:id>')
@api.doc(params={'id': 'Identificador del evento a buscar'})
class GetEventById(Resource):
    @api.marshal_with(EventModel(api).get(), envelope='event')
    @api.response(200, description="Todo OK", model=EventModel(api).get())
    
    def get(self, id):
        try:
            resp = MasivosDB().getEvent(id)
            return resp
        except Exception as e:
            resp = {500, "Error"}
            return resp

@api.route('/cleanEvent/<int:id>', methods=['PATCH'])
@api.doc(params={'id': 'Identificador del evento a borrar'})
class CleanEvent(Resource):
    
    def patch(self, id):

        try:
            MasivosDB().deleteEvent(id)
            MasivosDB().deleteSubs(id)
            return jsonify({'message': 'Evento eliminado correctamente'})

        except Exception as e:
            return jsonify({'message': e})

@api.route('/getAffectedSubs/<int:id>')
@api.doc(params={'id': 'Identificador del evento a buscar'})
class GetAffectedSubs(Resource):
    @api.response(200, description="Todo OK")
    
    def get(self, id):
        try:
            resp = jsonify(MasivosDB().getAffectedSubsByEvent(id))
            return resp
        except Exception as e:
            resp = {500, "Error"}
            return resp

# name, mtt, olt, port, cto, splitter, event_type, event_start, event_finish, status
@api.route('/insertEvent/')
@api.doc(params={'name': 'Nombre del Evento'})
@api.doc(params={'mtt': 'Master Trouble Ticket'})
@api.doc(params={'olt': 'OLT afectada'})
@api.doc(params={'port': 'Puerto(s) afectado(s)'})
@api.doc(params={'cto': 'CTO(s) afectado(s)'})
@api.doc(params={'splitter': 'Splitter(s) afectado(s)'})
@api.doc(params={'event_type': 'Tipo de Evento'})
@api.doc(params={'event_start': 'Fecha y Hora del comienzo del Evento - Formato Y-m-d H:M:S'})
@api.doc(params={'event_finish': 'Fecha y Hora del Final del Evento - Formato Y-m-d H:M:S'})
@api.doc(params={'status': 'Status Actual del Evento'})
@api.doc(params={'user': 'Usuario que solicita la carga'})
class InsertEvent(Resource):
    @api.response(200, description="Todo OK")
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('mtt', type=int)
        parser.add_argument('olt', type=str)
        parser.add_argument('port', type=str)
        parser.add_argument('cto', type=str)
        parser.add_argument('splitter', type=str)
        parser.add_argument('event_type', type=int)
        parser.add_argument('event_start', type=lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
        parser.add_argument('event_finish', type=lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
        parser.add_argument('status', type=int)
        parser.add_argument('user', type=str)
        args = parser.parse_args()
        
        
        try:
            lastId = MasivosDB().inserEvent(name=args['name'], mtt=args['mtt'], olt=args['olt'], port=args['port'], cto=args['cto'], 
                                                splitter=args['splitter'], event_type=args['event_type'], event_start=args['event_start'], 
                                                event_finish=args['event_finish'], status=args['status'], user=args['user'])
                        
            rowId = {
                "Last_ID": lastId,
            }
            resp = jsonify(rowId)
            return resp
        except Exception as e:
            resp = {500, "Error"}
            return resp

@api.route('/updateEvent/')
@api.doc(params={'id': 'Identificador del Evento'})
@api.doc(params={'event_start': 'Fecha y Hora del Inicio del Evento - Formato Y-m-d H:M:S'})
@api.doc(params={'event_finish': 'Fecha y Hora del Final del Evento - Formato Y-m-d H:M:S'})
@api.doc(params={'status': 'Status Actual del Evento'})
class UpdateEvent(Resource):
    @api.response(200, description="Todo OK")
    
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('event_start', type=lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'), default=0)
        parser.add_argument('event_finish', type=lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'), default=0)
        parser.add_argument('status')
        args = parser.parse_args()

        try:
            MasivosDB().updateEvent(id=args['id'], event_start=args['event_start'], event_finish=args['event_finish'], status=args['status'])

            resp = jsonify("Todo OK")
            return resp
        except Exception as e:
            resp = {500, "Error"}
            return resp


@api.route('/insertAffectedSubs/')
@api.doc(params={'id': 'Identificador del Evento'})
@api.doc(params={'affected_subs': 'Listado separado por comas de las subscripciones afectadas'})
class InsertAffectedSubs(Resource):
    @api.response(200, description="Todo OK")
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('affected_subs')
        args = parser.parse_args()

        try:
            subs = args['affected_subs'].split(",")
            for sub in subs:
                MasivosDB().insertAffectedSubs(args['id'], sub)

            resp = jsonify("Todo OK")
            return resp
        except Exception as e:
            resp = {500, e}
            return resp

@api.route('/isSubsAffected/<int:subs>')
@api.doc(params={'subs': 'Identificador del evento a buscar'})
@api.doc(params={'status': 'Estado a buscar'})
class IsSubsAffected(Resource):
    @api.response(200, description="Todo OK")

    def get(self, subs):
        parser = reqparse.RequestParser()
        #parser.add_argument('subs')
        parser.add_argument('status', default = 0)
        args = parser.parse_args()
        try:
            resp = jsonify(MasivosDB().isSubsAffected(subs, args['status']))
            return resp
        except Exception as e:
            raise


@api.route('/getCTOsByName/')
@api.doc(params={'name': 'Nombre de la CTO'})
class GetCTOsByName(Resource):
    @api.response(200, description="Todo OK")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        args = parser.parse_args()

        try:
            resp = CamachoDB().getCTOsByName(args['name'])
            return resp
        except Exception as e:
            resp = {500, "Error"}
            return resp


@api.route('/getSubsByCTO/')
@api.doc(params={'id': 'Identificador de la CTO'})
class GetSubsByCTO(Resource):
    @api.response(200, description="Todo OK")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()

        try:
            resp = CamachoDB().getSubsByCTO(args['id'])
            return resp
        except Exception as e:
            resp = {500, "Error"}
            return resp

##DEFINIR MODEL AFFECTED_EVENT
resource_fields = api.model('Resource', {
    'affected_subs': fields.String,
    'event_id': fields.Integer
})

@api.route('/insertAffectedSubsBulk/')
class InsertAffectedSubsBulk(Resource):
    @api.expect(resource_fields)
    @api.response(200, description="Todo OK")
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('affected_subs')
        parser.add_argument('event_id')
        args = parser.parse_args()
        ##sub_array = []
        counterSubs = 0

        try:
            event_id = args['event_id']
            subs = args['affected_subs'].split(",")
            for sub in subs:
                ##sub_array.append(sub)
                MasivosDB().insertAffectedSubs(args['event_id'], sub)
                counterSubs+=1
            ## ESTO AL LOG
            ##str = ' '.join(sub_array)

            resp = {

                'total_affected_subs': counterSubs,
                'event_id': event_id,
            }

            return resp,200
        except Exception as e:
            resp = {500, e}
            return resp

@api.route('/insertEventPic/')
@api.param('eventId', 'ID de la tarea')
class InsertEventPic(Resource):
    @api.response(200, description="Todo OK")
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('eventId')
        args = parser.parse_args()
        try:
            eventId = args['eventId']
            MasivosDB().insertEventPic(eventId)

            resp = {
                'event':eventId
            }

            return resp,200
        except Exception as e:
            resp = {500, e}
            return resp

@api.route('/updateEventInitialPic/')
@api.param('eventId', 'ID de evento')
@api.param('initialPic', 'Pic inicial de la tarea')
class UpdateEventInitialPic(Resource):
    @api.response(200, description="Todo OK")
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('eventId')
        parser.add_argument('initialPic')
        args = parser.parse_args()
        try:
            eventId = args['eventId']
            initialPic = args['initialPic']
            MasivosDB().updateEventInitialPic(eventId,initialPic)

            resp = {
                'event':eventId,
                'initialPic':initialPic
            }

            return resp,200
        except Exception as e:
            resp = {500, e}
            return resp

@api.route('/updateEventEndPic/')
@api.param('eventId', 'ID de evento')
@api.param('endPic', 'Pic final de la tarea')
class UpdateEventEndPic(Resource):
    @api.response(200, description="Todo OK")
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('eventId')
        parser.add_argument('endPic')
        args = parser.parse_args()
        try:
            eventId = args['eventId']
            endPic = args['endPic']
            MasivosDB().updateEventEndPic(eventId,endPic)

            resp = {
                'event':eventId,
                'end_pic':endPic
            }

            return resp,200
        except Exception as e:
            resp = {500, e}
            return resp

@api.route('/insertNetinfoForEvent/')
@api.param('eventId', 'ID del evento')
@api.param('olt', 'IP de la OLT del evento')
@api.param('port', 'Puerto de la OLT (s/s/p)')
class InsertNetInforForEvent(Resource):
    @api.response(200, description="Todo OK")
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('eventId')
        parser.add_argument('olt')
        parser.add_argument('port')
        args = parser.parse_args()
        try:
            eventId = args['eventId']
            olt = args['olt']
            port = args['port']
            MasivosDB().insertNetinfoForEvent(eventId,olt,port)

            resp = {
                'event':eventId,
                'olt':olt,
                'port':port
            }

            return resp,200
        except Exception as e:
            resp = {500, e}
            return resp

@api.route('/getNetinfoForEvent/')
@api.doc(params={'id': 'ID del evento'})
class GetNetinfoForEvent(Resource):
    @api.response(200, description="Todo OK")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()

        try:
            resp = MasivosDB().getNetinfoForEvent(args["id"])
            return resp
        except Exception as e:
            resp = {500, "Error"}
            return resp

@api.route('/getEventPicsForEvent/')
@api.doc(params={'id': 'ID del evento'})
class GetNetinfoForEvent(Resource):
    @api.response(200, description="Todo OK")
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()

        try:
            resp = MasivosDB().getEventPicsForEvent(args["id"])
            return resp
        except Exception as e:
            resp = {500, "Error"}
            return resp