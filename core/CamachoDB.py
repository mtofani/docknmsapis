import pymysql

from cfg.ConfigParser import ConfigParser
from pymysql.err import IntegrityError


class CamachoDB(object):
    
    def __init__(self):
        self.config = ConfigParser().params


    def connect(self):
        self.db = pymysql.connect(host=self.config['CAMACHODB']['host'],
                 user=self.config['CAMACHODB']['user'],
                 password=self.config['CAMACHODB']['pass'],
                 db=self.config['CAMACHODB']['db'],
                 charset='latin1')
    
    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(e.message)

    def getCTOsByName(self, name):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            cur.execute("SELECT distinct(cto_id), NAME, address, customer_type, domo FROM ctos c WHERE c.name LIKE '%" + name + "%'")
            
            data = cur.fetchall()
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()

    def getSubsByCTO(self, id):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            cur.execute(f"select crm_code_values.value from subscription_service, crm_code_values,ctos \
                            where ctos.cto_id = {id} \
                            and service_id = reference \
                            and subscription_id = ctos.value \
                            AND crm_code_values.crm_code_defs_id = 1")
            
            data = cur.fetchall()
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()
