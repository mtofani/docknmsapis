from datetime import date

import sys
import os
from core.netpix_modules.InvalidPicException import InvalidPicException

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
parentparent = os.path.dirname(parent)                #/home/desarrollo/NMSAPIPrueba/NMSAPI
sys.path.append(parentparent)

from cfg.ConfigParser import ConfigParser
from cfg.Logger import Logger

import pymysql
from pickle import TRUE
from datetime import datetime


class NetPixDB(object):

    #-----------CONSTRUCTOR--------------
    
    def __init__(self):
        self.config = ConfigParser().params

    #-----------CONNECTION TO DB---------------

    def connect(self):
        self.db = pymysql.connect(host=self.config['NETPIXDB']['host'],
                 user=self.config['NETPIXDB']['user'],
                 password=self.config['NETPIXDB']['pass'],
                 db=self.config['NETPIXDB']['db'],
                 charset='latin1')
    
    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(e.message)
            raise e
 
    #-----------------------INSERTS---------------------------

    def insertPic(self,picName):
        #INSERT INTO `net_pics`.`pics` (`name`, `date_time`) VALUES ("ljahsdf", '2022-05-23 12:47:24');
        try:
            self.connect()
            cur = self.db.cursor()
            cur.execute("INSERT INTO `net_pics`.`pics` (`name`, `date_time`) VALUES ('{}', '{}');".format(picName,datetime.today()))
            self.db.commit()
            return cur.lastrowid
        except pymysql.IntegrityError as ie:
            print(ie)
            raise ie
        except Exception as e:
            print(e)
            raise e
        finally:
            self.db.close()

    def insertOltInfo(self,oltInfo):
        #INSERT INTO `net_pics`.`olt_info` (`pic_id`, `ip`, `port`, `model`, `mza`) VALUES ('1', '172.30.77.1', '1/2/1', 'C300', 'PruebaMza');
        try:
            self.connect()
            cur = self.db.cursor()
            cur.execute("INSERT INTO `net_pics`.`olt_info` (`pic_id`, `ip`, `port`, `model`, `mza`) \
                        VALUES ('{}', '{}', '{}', '{}', '{}');".format(oltInfo.picId,oltInfo.ip,oltInfo.port,oltInfo.model,oltInfo.mza))
            self.db.commit()
            return cur.lastrowid
        except Exception as e:
            raise e
        finally:
            self.db.close()

    def insertOnuInfo(self,onusInfo,idOltInfo):
        #INSERT INTO `net_pics`.`onu_info` (`olt_info_id`, `onu_number`, `status`, `descr`, `rxOlt`, `rxOnu`, `sn`) VALUES ('1', '1', '3', 'MZA_Prueba', '-12', '-23.32', 'ZTEHC81273');
        try:
            self.connect()
            cur = self.db.cursor()
            for onuInfo in onusInfo:
                cur.execute("INSERT INTO `net_pics`.`onu_info` (`olt_info_id`, `onu_number`, `status`, `descr`, `rxOlt`, `rxOnu`, `sn`) \
                        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(idOltInfo,onuInfo.channel,onuInfo.status,onuInfo.descr,onuInfo.rxOlt,onuInfo.rxOnu,onuInfo.serial))
            self.db.commit()
        except Exception as e:
            print(e)
        finally:
            self.db.close()

    #----------------------------SELECTS----------------------------------

    def selectStatuses(self):
        try:
            self.connect()
            cur = self.db.cursor()
            cur.execute("SELECT * \
                        FROM statuses ")
            data = cur.fetchall()
            return data
        except Exception as e:
            print(e)
            raise e
            #Guardar en logger en vez de un print todo feo
        finally:
            self.db.close()

    def selectPics(self):
        try:
            self.connect()
            cur = self.db.cursor()
            cur.execute("SELECT * \
                        FROM pics ")
            data = cur.fetchall()
            return data
        except Exception as e:
            raise e
            #Guardar en logger en vez de un print todo feo
        finally:
            self.db.close()


    def selectOltModels(self):
        try:
            self.connect()
            cur = self.db.cursor()
            cur.execute("SELECT * \
                        FROM olt_models ")
            data = cur.fetchall()
            return data
        except Exception as e:
            print(e)
            raise e
            #Guardar en logger en vez de un print todo feo
        finally:
            self.db.close()



    def selectPicById(self,picId):
        try:
            self.connect()
            cur = self.db.cursor()
            cur.execute("SELECT * \
                        FROM pics \
                        WHERE pics.id = '{}';".format(picId))
            data = cur.fetchone()
            if data == None:
                raise InvalidPicException("No se encontró la foto")
            return data
        except Exception as e:
            print(e)
            raise e
            #Guardar en logger en vez de un print todo feo
        finally:
            self.db.close()

    def selectPicByName(self,picName):
        try:
            self.connect()
            cur = self.db.cursor()
            cur.execute("SELECT id \
                        FROM pics \
                        WHERE pics.name = '{}';".format(picName))
            data = cur.fetchone()
            return data
        except Exception as e:
            print(e)
            raise e
            #Guardar en logger en vez de un print todo feo
        finally:
            self.db.close()

    def selectOltInfoByPicId(self,picId):
        try:
            self.connect()
            cur = self.db.cursor()
            cur.execute("SELECT olt_info.id, pic_id, ip, port, model, mza \
                        FROM pics \
                        RIGHT JOIN olt_info ON pics.id = olt_info.pic_id \
                        WHERE pics.id = '{}';".format(picId))
            data = cur.fetchall()
            return data
        except Exception as e:
            print(e)
            raise e
        finally:
            self.db.close()


    def selectOnusFromPicAndOlt(self,picId,oltId):
        try:
            self.connect()
            cur = self.db.cursor()
            cur.execute("SELECT olt_info_id, onu_number, status, descr, rxOlt, rxOnu, sn \
                        FROM pics \
                        RIGHT JOIN olt_info ON pics.id = olt_info.pic_id \
                        RIGHT JOIN onu_info ON olt_info.id = onu_info.olt_info_id \
                        WHERE pics.id = '{}' \
                        AND olt_info.id = '{}';".format(picId,oltId))
            data = cur.fetchall()
            return data
        except Exception as e:
            print(e)
            raise e
            #Guardar en logger en vez de un print todo feo
        finally:
            self.db.close()
