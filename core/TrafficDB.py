import cx_Oracle
from core.APIDB import APIDB
from core.MiscTools import MiscTools

class TrafficDB(object):

    def __init__(self):
        pass
    
    
    def connect(self):
        self.host = APIDB().getProperty("trafficdb.host")
        self.user = APIDB().getProperty("trafficdb.user")
        self.db = APIDB().getProperty("trafficdb.db")
        self.pswd = MiscTools().decode64(APIDB().getProperty("trafficdb.pass"))
        
        dsn_tns = cx_Oracle.makedsn(self.host, 1521, service_name=self.db)
        self.conn = cx_Oracle.connect(user=self.user, password=self.pswd, dsn=dsn_tns)
        
    def close(self):
        try:
            self.conn.close()
        except Exception as e:
            print(e)
            
    def getWeeklyData(self, subs):
        self.connect()
        l = []
        try:
            with self.conn.cursor() as cursor:
                # create a new variable to hold the value of the
                # OUT parameter
                out = cursor.var(cx_Oracle.CURSOR)
                # call the stored procedure
                cursor.callproc('RETRIEVE_WEEKLY_TRAFFIC', [int(subs), 0, out])
                data = out.getvalue().fetchall()
                
                for line in data:
                    t = Traffic(line[0], line[1], line[2])
                    l.append(t)
                    

                return l
        except Exception:
            raise
        finally:
            self.close()
            
    def getOnlineData(self, subs):
        self.connect()
        l = []
        try:
            with self.conn.cursor() as cursor:
                # create a new variable to hold the value of the
                # OUT parameter
                out = cursor.var(cx_Oracle.CURSOR)
                # call the stored procedure
                cursor.callproc('RETRIEVE_ONLINE_TRAFFIC', [int(subs), 0, out])
                data = out.getvalue().fetchall()
                
                for line in data:
                    t = Traffic(line[0], line[1], line[2])
                    l.append(t)
                    

                return l
        except Exception:
            raise
        finally:
            self.close()
            
    def getYearlyData(self, subs):
        self.connect()
        l = []
        try:
            with self.conn.cursor() as cursor:
                # create a new variable to hold the value of the
                # OUT parameter
                out = cursor.var(cx_Oracle.CURSOR)
                # call the stored procedure
                cursor.callproc('RETRIEVE_YEARLY_TRAFFIC', [int(subs), 0, out])
                data = out.getvalue().fetchall()
                
                for line in data:
                    t = Traffic(line[0], line[1], line[2])
                    l.append(t)
                    

                return l
        except Exception:
            raise
        finally:
            self.close()
            
    def getMonthlyData(self, subs):
        self.connect()
        l = []
        try:
            with self.conn.cursor() as cursor:
                # create a new variable to hold the value of the
                # OUT parameter
                out = cursor.var(cx_Oracle.CURSOR)
                # call the stored procedure
                cursor.callproc('RETRIEVE_MONTHLY_TRAFFIC', [int(subs), 0, out])
                data = out.getvalue().fetchall()
                
                for line in data:
                    t = Traffic(line[0], line[1], line[2])
                    l.append(t)
                    

                return l
        except Exception:
            raise
        finally:
            self.close()
            
class Traffic():
    
    def __init__(self, idate, up, down):
        self.idate = idate
        self.up = up
        self.down = down

        
        