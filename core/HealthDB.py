
import pymysql
from cfg.ConfigParser import ConfigParser
from pymysql.err import IntegrityError


class HealthDB(object):
    
    def __init__(self):
        self.config = ConfigParser().params


    def connect(self):
        self.db = pymysql.connect(host=self.config['NETDISCO']['host'],
                 user=self.config['NETDISCO']['user'],
                 password=self.config['NETDISCO']['pass'],
                 db=self.config['NETDISCO']['db'],
                 charset='latin1')
    
    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(e.message)
        
        
    def getProperty(self,name):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute("select value from properties where name = %s",name)
            
            data=cur.fetchone()
            
            
            return data
        
        except Exception:
            raise
        finally:
            self.close() 
    def getLatestGPONDiscovery(self):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            cur.execute ("SELECT hostname,last_update AS fecha, ping, snmp FROM devices d " 
                         "WHERE object_id IN ('1.3.6.1.4.1.2011.2.316', "
                         "  '1.3.6.1.4.1.3902.1082.1001.600.1.1')")
            data=cur.fetchall()
            
        
            return data
        
        except Exception:
            raise
        finally:
            self.close()