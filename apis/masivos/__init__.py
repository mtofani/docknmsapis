from flask_restx import Api
  
from .masivos import api as masivos

api = Api(
    title='APIS NMS Desarrollo',
    version='1.0',
    description='Herramientas NMS',
)


api.add_namespace(masivos, path="/masivos")