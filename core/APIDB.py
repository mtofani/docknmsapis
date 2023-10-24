'''
Created on 22 jul. 2020

@author: avespe
'''
import pymysql

from cfg.ConfigParser import ConfigParser
from pymysql.err import IntegrityError


class APIDB(object):
    
    def __init__(self):
        self.config = ConfigParser().params


    def connect(self):
        self.db = pymysql.connect(host=self.config['APIDB']['host'],
                 user=self.config['APIDB']['user'],
                 password=self.config['APIDB']['pass'],
                 db=self.config['APIDB']['db'],
                 charset='latin1')
    
    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(e.message)
        
        
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
            
    def registerUser(self, username, password):
        try:
            self.connect()
            cur=self.db.cursor()
            
            cur.execute('INSERT INTO users (username, password, created_date) VALUES (%s, %s, now())', (username, password))
        
        except IntegrityError:
            raise
        except Exception:
            raise
        finally:
            self.close()
            
    def deleteUser(self, username):
        try:
            self.connect()
            cur=self.db.cursor()
            
            cur.execute('delete from users where username = %s', (username))
        
        except IntegrityError:
            raise
        except Exception:
            raise
        finally:
            self.close()
            
    def registerUsage(self, username, operation, endpoint, status, ip):
        try:
            self.connect()
            cur=self.db.cursor()
            
            cur.execute('INSERT INTO `requests` (`username`, `operation`, `endpoint`, `status`, `ip`, `stamp`) VALUES (%s, %s, %s,  %s, %s, now());', (username, operation, endpoint, status, ip))
        
        except Exception:
            raise
        finally:
            self.close()
    
    def registerUsageComplete(self, username, operation, endpoint, uri, status, ip):
        try:
            self.connect()
            cur=self.db.cursor()
            
            cur.execute('INSERT INTO `requests` (`username`, `operation`, `endpoint`, `uri`, `status`, `ip`, `stamp`) VALUES (%s, %s, %s, %s, %s, %s, now());', (username, operation, endpoint, uri, status, ip))
        
        except Exception:
            raise
        finally:
            self.close()
    
    def registerUsageRedux(self, request, resp):
        try:
            self.connect()
            cur=self.db.cursor()
            
            cur.execute('INSERT INTO `requests` (`username`, `operation`, `endpoint`, `uri`, `status`, `ip`, `stamp`) VALUES (%s, %s, %s, %s, %s, %s, now());', (request.authorization.username, request.method, request.full_path, request.path, resp.status_code, request.remote_addr))
        
        except Exception:
            raise
        finally:
            self.close()
            
    def getUser(self, cls, username):
        self.connect()
        cursor = self.db.cursor()
        
        try:
            cursor.execute('SELECT username, password FROM users WHERE username=%s', (username,))
            data = cursor.fetchone()
            
            if data:
                return cls(data[0], str(data[1]))
        finally:
            self.close()
