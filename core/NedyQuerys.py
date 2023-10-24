'''
Created on 6 ago. 2020

@author: avespe
'''
import subprocess
import pymysql
from .APIDB import APIDB
from .MiscTools import MiscTools


class Nedy(object):


    def __init__(self):
        pass
    
    
    def connect(self):
    
        self.host = APIDB().getProperty("nedydb.host")
        self.user = APIDB().getProperty("nedydb.user")
        self.db = APIDB().getProperty("nedydb.db")
        self.pswd = MiscTools().decode64(APIDB().getProperty("nedydb.pass"))
        
        self.db = pymysql.connect(host=self.host,
                                    user=self.user,
                                    password=self.pswd,
                                    db=self.db,
                                    charset='latin1')
        
    
    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(e)
    
    def getDevice(self, ip):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute("select * from devices where ip = %s", ip)
            
            data = cur.fetchone()
            
            if (cur.rowcount == 0):
                raise Exception("Equipo desconocido: " + ip)
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()

    def getNetworks(self):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute("SELECT * from networks")
            
            data = cur.fetchall()
            
            if (cur.rowcount == 0):
                  data = "No hay redes a mostrar " 
            
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()
    def getAddInfo(self, ip):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
                
            cur.execute("SELECT * from add_info a where a.ip = %s", ip)
            
            data = cur.fetchall()
            
            if (cur.rowcount == 0):
                 data = "No hay variables adicionales de la ip: " + ip
            
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()
    


    def getInferfacesIP(self, ip):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute("select * from interfaces where device_ip = %s", ip)
            
            data = cur.fetchall()
            
            if (cur.rowcount == 0):
                data = "No hay puertos de la ip: " + ip
            
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()
        
            
    def getAllDevices(self):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute("SELECT * from devices")
            
            data = cur.fetchall()
            
        
            return data
        
        except Exception:
            raise
        finally:
            self.close()

    def getAllbyModel(self, model):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)

            search_string= f"%{model}%"
            cur.execute("select * from devices where descr like %s", search_string)
            
            data = cur.fetchall()

            if (cur.rowcount == 0):
                
                data = "No hay equipos del modelo: " + model
            

            return data
        
        except Exception:
            raise
        finally:
            self.close()

    def getOnus(self, ip, port):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)


            if (port == None):
                #search_string= f"%{ip}%"
                cur.execute("SELECT * from onus where ip = %s", ip)
                data = cur.fetchall()
                
            else:
                
            
                cur.execute("SELECT * from onus where ip = %s and if_index = %s",  (ip, port, ))
                
                data = cur.fetchall()
            if (cur.rowcount == 0):
            
             data = "No hay datos para la consulta solicitada " 

            return data
        
        except Exception:
            raise
        finally:
            self.close()

        
