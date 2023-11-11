#from flask_cors import CORS
from flask import Flask

from flask import json
import logging
import sys
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables de entorno desde el archivo .en


load_dotenv()  # Carga las variables de entorno desde el archivo .env

APP_PORT = os.getenv("APP_PORT")
NAMESPACE= os.getenv("NAMESPACE")

namespace = os.getenv("NAMESPACE") or (sys.argv[1] if len(sys.argv) > 1 else None)

if namespace == 'nedyquerys':
    from apis.nedyquerys import api as namespace_api
elif namespace == 'masivos':
    from apis.masivos import api as namespace_api




app = Flask(__name__)

namespace_api.init_app(app)

#CORS(app)





if __name__ == "__main__":
        
        app.run(debug=True, host='0.0.0.0', port=APP_PORT)