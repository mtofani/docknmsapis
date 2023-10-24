
# from core.Nedy import Nedy
import json
import sys
import os

# from core.netpix_modules.NetPixDB import NetPixDB
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
parentparent = os.path.dirname(parent)                #/home/desarrollo/NMSAPIPrueba/NMSAPI
sys.path.append(parentparent)

from flask import jsonify


from MasivosDB import MasivosDB
# from core.netpix_modules.NetPixer import NetPixer
from netpix_modules.NetPixDB import NetPixDB

# def main(*argv):
#     x = Nedy().getOnuDetailZTE('172.31.148.1', 'nms', 'Lasac01', '1/2/1:127')
    
#     print(x)

# if __name__ == '__main__':
#     main(sys.argv[1:])

# print(MasivosDB().insertNetinfoForEvent("65","172.30.77.1","1/2/1"))

# np = NetPixer("172.30.77.93","0/1/0")
# np.collectOnusInfo()
# onus = np.createListOnuInfo()
# for o in onus:
#     print(o)

db = NetPixDB()
pics = db.selectPics()
objPics = []
for p in pics:
    objPics.append({
        "pic":p[0],
        "name":p[1],
        "date":p[2].strftime("%m/%d/%Y, %H:%M:%S")
    })
# resp = json.loads(json.dumps(objPics))
print(objPics)