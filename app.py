#from flask_cors import CORS
from flask import Flask
from apis import api
from flask import json
import logging
app = Flask(__name__)

#CORS(app)

api.init_app(app)



if __name__ == "__main__":
        
        app.run(debug=True, host='0.0.0.0', port=8080)