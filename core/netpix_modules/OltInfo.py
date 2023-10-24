from core.netpix_modules.NetPixer import NetPixer
import json

class OltInfo:
    
    def __init__(self,ip=None,port=None):
        
        self.ip = ip
        self.port = port
        self.picId = ""
        if ip != None and port != None:
            self.ip = ip
            self.port = port
            try:
                np = NetPixer(self.ip,self.port)       
            except Exception as e:
                raise e 
            self.onus = np.collectOnusInfo()
            self.model = np.getOLTModel()
            self.mza = np.getMzaName()
        else:
            self.onus = []
            self.model = -1
            self.mza = ""

    def __str__(self):
        return f"""
                Ip: {self.ip}
                Port: {self.port}
                Name: {self.name}
                Model: {self.model}
                Mza: {self.mza}
        """

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
