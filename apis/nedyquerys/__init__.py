from flask_restx import Api
  
from .nedyquerys  import api as nedy

api = Api(
    title='APIS NMS Desarrollo',
    version='1.0',
    description='Herramientas NMS',
)


api.add_namespace(nedy, path="/nms/api/querys")