'''
Created on 22 jul. 2020

@author: avespe
'''
import pymysql
import re
from cfg.ConfigParser import ConfigParser
from pymysql.err import IntegrityError


class BACKUPSDB(object):
    
    def __init__(self):
        self.config = ConfigParser().params


    def connect(self):
        print("intento cnexion")
        self.db = pymysql.connect(host=self.config['BACKUPSDB']['host'],
                    user=self.config['BACKUPSDB']['user'],
                    password=self.config['BACKUPSDB']['pass'],
                    db='backups',
                    charset='latin1')
        
    def close(self):
            try:
                self.db.close()
            except Exception as e:
                print(str(e))
            
    def getBackUpByIP(self, ip, fecha):
        try:
            self.connect()
            cur = self.db.cursor()
            cur.execute("SELECT FECHA FROM bkp_archives WHERE bkp_archives.fecha = '{}' AND bkp_archives.ip = '{}';".format(fecha,ip))
            data = cur.fetchone()
            if (cur.rowcount == 0):
                data = None
                return data
            return data[0]
        except Exception as e:
            print(e)
        finally:
            self.close()
            
    def getBackUpLast(self, ip):
        try:
            self.connect()
            cur = self.db.cursor()
            cur.execute("SELECT IP, FECHA FROM bkp_archives WHERE bkp_archives.ip = '{}' ORDER BY bkp_archives.fecha DESC;".format(ip))
            
            data = cur.fetchall()
            if (cur.rowcount == 0):
                data = None
                return data             
            return data
        except Exception as e:
            print(e)
        finally:
            self.close()

    def getBackUpList(self, ip, fechaInit, fechaEnd):
        try:
            self.connect()
            cur = self.db.cursor()
            cur.execute("SELECT IP, FECHA FROM bkp_archives WHERE bkp_archives.fecha BETWEEN '{}' AND '{}' AND bkp_archives.ip = '{}';".format(fechaInit,fechaEnd,ip))
            data = cur.fetchall()
            if (cur.rowcount == 0):
                data = None
                return data             
            return data
        except Exception as e:
            print(e)
        finally:
            self.close()
        
    def getProperty(self, name):
        try:
            self.connect()
            cur = self.db.cursor()
            
            cur.execute("select value from properties where name = %s", name)
            
            data = cur.fetchone()
            
            if (cur.rowcount == 0):
                raise Exception("Propiedad desconocida: " + name)
            
            return data[0]
        
        except Exception:
            raise
        finally:
            self.close()
        
