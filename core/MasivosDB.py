import pymysql

import os 
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)        #/home/desarrollo/NMSAPIPrueba/NMSAPI
sys.path.append(parent)



from cfg.ConfigParser import ConfigParser
from pymysql.err import IntegrityError


class MasivosDB(object):
    
    def __init__(self):
        self.config = ConfigParser().params


    def connect(self):
        self.db = pymysql.connect(host=self.config['MASIVOSDB']['host'],
                 user=self.config['MASIVOSDB']['user'],
                 password=self.config['MASIVOSDB']['pass'],
                 db=self.config['MASIVOSDB']['db'],
                 charset='latin1')
    
    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(e.message)


    def getStatusCodes(self):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute("select * from status_codes")
            
            data = cur.fetchall()
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()

    def getEventTypes(self):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute("select * from event_types")
            
            data = cur.fetchall()
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()

    def getEvents(self):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute("select * from events")
            
            data = cur.fetchall()
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()

    def getEventsFiltered(self, type, status):

        if type == 0 and status == 0:
            query = "select * from events"
        elif type != 0 and status == 0:
             query = f"select * from events where event_type = {type}"
        elif type == 0 and status != 0:
             query = f"select * from events where status = {status}"
        elif type != 0 and status != 0:
             query = f"select * from events where event_type = {type} and status = {status}"

        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute(query)
            
            data = cur.fetchall()
            
            if (cur.rowcount == 0):
                return []

            return data
        
        except Exception:
            raise
        finally:
            self.close()

    def getEvent(self, id):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute(f"select * from events where id = {id}")
            
            data = cur.fetchall()
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()

    def deleteEvent(self, id):
        print("ACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        try:
            self.connect()
            cur=self.db.cursor()
            
            cur.execute("DELETE FROM `events` WHERE id = %s", id)
            cur.execute("commit")
        
        except Exception:
            raise
        finally:
            self.close()

    def deleteSubs(self, id):
        try:
            self.connect()
            cur=self.db.cursor()
            
            cur.execute("DELETE FROM `affected_subs` WHERE event_id = %s", id)
            cur.execute("commit")
            
        except Exception:
            raise
        finally:
            self.close()

    def getAffectedSubsByEvent(self, id):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute(f"select * from affected_subs where event_id = {id}")
            
            data = cur.fetchall()
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()
    
    def getNetinfoForEvent(self, id):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute(f"select * from netinfo_for_event where id_event = {id}")
            
            data = cur.fetchall()
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()

    def getEventPicsForEvent(self, id):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute(f"select * from event_pics where event_id = {id}")
            
            data = cur.fetchall()
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()


    def isSubsAffected(self, subs, status):
        if status == 0:
            query = f"SELECT e.id, e.mtt, et.name as event_name, sc.name as status_value, e.event_start, e.event_finish, e.name as event_descr \
                            FROM events e, affected_subs a, event_types et, status_codes sc \
                            WHERE a.subs_number = {subs} \
                            AND a.event_id = e.id \
                            AND e.event_type = et.id \
                            AND e.`status` = sc.id"
        else:
            query = f"SELECT e.id, e.mtt, et.name as event_name, sc.name as status_value, e.event_start, e.event_finish, e.name as event_descr \
                            FROM events e, affected_subs a, event_types et, status_codes sc \
                            WHERE a.subs_number = {subs} \
                            AND a.event_id = e.id \
                            AND e.event_type = et.id \
                            AND e.`status` = sc.id \
                            AND e.`status` = {status}"
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute(query)
            
            data = cur.fetchall()
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()

    def inserEvent(self, name, mtt, olt, port, cto, splitter, event_type, event_start, event_finish, status, user):
        try:
            self.connect()
            cur=self.db.cursor()
           
            cur.execute(f"INSERT INTO `events` (`name`, `mtt`, `olt`, `port`, `cto`, `splitter`, `event_type`, `event_start`, `event_finish`, `status`, `user`) \
                                        VALUES ('{name}', {mtt}, '{olt}', '{port}', '{cto}', '{splitter}', {event_type}, '{event_start}', '{event_finish}', {status}, '{user}');")
            
            
            lastRowId = cur.lastrowid
            cur.execute("commit")

            return lastRowId
        except Exception as e:
            raise
        finally:
            self.close()

    def insertNetinfoForEvent(self, eventId, olt, port):
        try:
            self.connect()
            cur=self.db.cursor()
           
            cur.execute(f"INSERT INTO `masivos`.`netinfo_for_event` (`id_event`, `olt`, `port`) \
                                        VALUES ('{eventId}', '{olt}', '{port}');")
            
            cur.execute("commit")

        except Exception as e:
            raise
        finally:
            self.close()

    def insertEventPic(self, eventId):
        try:
            self.connect()
            cur=self.db.cursor()
           
            cur.execute(f"INSERT INTO `masivos`.`event_pics` (`event_id`) VALUES ('{eventId}');")
            
            cur.execute("commit")

        except Exception as e:
            raise e
        finally:
            self.close()

    def updateEventInitialPic(self, eventId, initialPic):
        try:
            self.connect()
            cur=self.db.cursor()
           
            cur.execute(f"UPDATE `masivos`.`event_pics` SET `initial_pic`='{initialPic}' WHERE  `event_id`={eventId};")
            
            cur.execute("commit")

        except Exception as e:
            raise e
        finally:
            self.close()

    def updateEventEndPic(self, eventId, endPic):
        try:
            self.connect()
            cur=self.db.cursor()
           
            cur.execute(f"UPDATE `masivos`.`event_pics` SET `end_pic`='{endPic}' WHERE  `event_id`={eventId};")
            
            cur.execute("commit")

        except Exception as e:
            raise e
        finally:
            self.close()

    def updateEvent(self, id, event_start, event_finish, status):
        if event_start == 0:
            query = f"UPDATE `events` SET event_finish = '{event_finish}', STATUS = {status} WHERE id = {id}"
        elif event_finish == 0:
            query = f"UPDATE `events` SET event_start = '{event_start}', STATUS = {status} WHERE id = {id}"
        else:
            query = f"UPDATE `events` SET event_finish = '{event_finish}', event_start = '{event_start}', STATUS = {status} WHERE id = {id}"

        try:
            self.connect()
            cur=self.db.cursor()

            cur.execute(query)
            
            cur.execute("commit")

        except Exception as e:
            raise
        finally:
            self.close()

    def insertAffectedSubs(self, id, subs):
        try:
            self.connect()
            cur=self.db.cursor()
            
            cur.execute(f"INSERT INTO `affected_subs` (`event_id`, `subs_number`) VALUES ({id}, {subs});")
            
            cur.execute("commit")

        except Exception as e:
            raise
        finally:
            self.close()
