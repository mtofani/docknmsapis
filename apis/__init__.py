from flask_restx import Api
  
from .nedyquerys import api as nedy
from .nedytools import api as nedytools
from .nmssec import api as nmssec
from .nedybackups import api as bkps
from .traffic import api as traffic
from .konglog import api as kong
from .gponstatus import api as gponstatus
from .misc import api as misc
from .masivos import api as masivos
from .netpix import api as netpix
from .health import api as health

api = Api(
    title='APIS NMS Desarrollo',
    version='1.0',
    description='Herramientas NMS',
)

api.add_namespace(nedytools, path="/nms/api")
api.add_namespace(nedy, path="/nms/api/querys")
api.add_namespace(nmssec, path="/nmssec")
api.add_namespace(bkps, path="/backups")
api.add_namespace(traffic, path="/traffic")
api.add_namespace(kong, path="/kong")
api.add_namespace(gponstatus, path="/gpon")
api.add_namespace(misc, path="/misc")
api.add_namespace(masivos, path="/masivos")
api.add_namespace(netpix, path="/netpix")
api.add_namespace(health, path="/health")

