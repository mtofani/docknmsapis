'''
Created on 22 jul. 2020

@author: avespe
'''
import base64
import ipaddress


class MiscTools():

    def decode64(self, value):
        base64_message = value
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        return message
    
    def isIP(self, ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except Exception:
            return False

    def isPortGpon(self,port):
        parts = str(port).split("/")
        if(len(parts)!=3):
            return False
        for part in parts:
            if(not part.isnumeric()):
                return False
        return True
        
    def ConvertSectoDay(self, n):
     
        day = n // (24 * 3600)
     
        n = n % (24 * 3600)
        hour = n // 3600
     
        n %= 3600
        minutes = n // 60
     
        n %= 60
        seconds = n
         
        x = str(day) + " dias, " + str(hour) + " horas, " + str(minutes) + " minutos y " + str(seconds) + " segundos."
         
        return x
    
    
    def getCIDR(self, mask):
        return str((sum([ bin(int(bits)).count("1") for bits in mask.split(".") ])))
