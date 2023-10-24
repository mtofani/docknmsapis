from uuid import RESERVED_FUTURE

import sys
import os

from pymysql import IntegrityError
from core.netpix_modules.Comparison import Comparison
from core.netpix_modules.InvalidPicException import InvalidPicException
from core.netpix_modules.UnreachableIPException import UnreachableIPException

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
parentparent = os.path.dirname(parent)                #/home/desarrollo/NMSAPIPrueba/NMSAPI
sys.path.append(parentparent)

from cfg.Logger import Logger
from core.netpix_modules.NetPixDB import NetPixDB
from core.netpix_modules.OnuInfo import OnuInfo
from core.netpix_modules.Pic import Pic
from core.netpix_modules.OltInfo import OltInfo

class NetPix: #Antes era APINetPix.py

    #------------CONSTRUCTOR------------------

    def __init__(self):
        
        self.log = Logger("api.log")
        self.db = NetPixDB()
        self.pic = Pic()
        pass

    #------------PUBLIC METHODS --------------

    def takePicGpon(self,ipPorts,name):
        try:
            self.pic.oltsInfo = self.__processOltsInfo(ipPorts)
        except UnreachableIPException as e:
            raise e
        self.pic.name = name
        self.log.logInfo(f"Se tomó la foto {name}")
        return self.pic


    def uploadPicToDB(self,pic):
        #Insertar Pic y obtener picId
        try:
            pic.id = self.__insertPic(pic)
            #Asignar PicId a las OltInfo
            for oltInfo in pic.oltsInfo:
                oltInfo.picId=pic.id
            #insertar OltsInfo y OnusInfo a la DB
            self.__insertOltsInfo(pic)
            self.log.logInfo(f"Se subió la foto {self.pic.name}")
            return pic.id
        except Exception as e:
            self.log.logError(e)
            raise e

    

    def getPicFromDB(self,picId):
        pic = Pic()
        responseDb = ()
        #Obtener info PIC
        try:
            responseDb = self.db.selectPicById(picId)
            pic.id = responseDb[0]
            pic.name = responseDb[1]
            pic.dateTime = str(responseDb[2])
        except InvalidPicException as ipe:
            print("ay")
            raise ipe
        except Exception as e:
            self.log.logError(e)
            raise e
        #Obtener OLTs y puertos asociados
        try:
            responseDb = self.db.selectOltInfoByPicId(picId)
            for resp in responseDb:
                oltInfo = OltInfo()
                oltInfo.id = resp[0]
                oltInfo.picId = resp[1]
                oltInfo.ip = resp[2]
                oltInfo.port = resp[3]
                oltInfo.model = resp[4]
                oltInfo.mza = resp[5]
                pic.oltsInfo.append(oltInfo)
        except Exception as e:
            self.log.logError(e)
            raise
        #Obtener Onus asociadas a la OLT
        for olt in pic.oltsInfo:
            try:
                responseDb = self.db.selectOnusFromPicAndOlt(pic.id, olt.id)
                for resp in responseDb:
                    onu = OnuInfo()
                    #olt_info_id, onu_number, status, descr, rx, tx, sn
                    onu.olt = olt.ip
                    onu.channel = resp[1]
                    onu.status = resp[2]
                    onu.descr = resp[3]
                    onu.rxOlt = resp[4]
                    onu.rxOnu = resp[5]
                    onu.serial = resp[6]
                    olt.onus.append(onu)
            except Exception as e:
                self.log.logError(e)
                print(e)
                raise e
        return pic

    def comparePics(self, pic2, pic1):
        results = []
        #Recorrer todas las onus de Pic 2 (la mas nueva)
        for olt2 in pic2.oltsInfo:
            #Buscar la onu que le corresponde en la Pic 1 (la mas vieja)
            for onu2 in olt2.onus:
                for olt1 in pic1.oltsInfo:
                    if olt2.port == olt1.port:
                        for onu1 in olt1.onus:
                            if onu1.channel == onu2.channel:
                                comparison = onu2.compareThis(onu1)
                                comparison.oltPort = olt2.port
                                comparison.oltModel = olt1.model
                                results.append(comparison)
        #Retornar una lista de CompareResult
        comp = Comparison(results)
        return comp

    def comparePicsById(self,picId2,picId1):
        resultado = None
        try:
            pic2 = self.getPicFromDB(picId2)
            pic1 = self.getPicFromDB(picId1)
            resultado = self.comparePics(pic2,pic1)
        except InvalidPicException as ipe:
            print("fallo")
            raise ipe
        return resultado


    def comparePicsByName(self, namePic):
        #Obtenemos el ID de la foto con el nombre namePic
        picId = self.db.selectPicByName(namePic)[0]
        ipPorts = ""
        #Buscamos las OLT y puerto de esa foto y recorremos para crear un nuevo string de ip+puerto y sacar la nueva foto
        oltsInfo = self.db.selectOltInfoByPicId(picId)
        for olt in oltsInfo:
            ipPorts += f"{olt[2]},{olt[3]}|"
        #Borramos el último |
        ipPorts=ipPorts[0:-1]

        #Recuperamos la foto original y creamos la nueva pero no la subimos a la DB
        pic1 = self.getPicFromDB(picId)
        pic2 = self.takePicGpon(ipPorts,"Volando")

        #Obtenemos la comparación
        result = self.comparePics(pic2, pic1)
        return result

    #--------------PRIVATE METHODS------------------

    def __strToListIpPorts(self,strIpPorts):
        ipPorts = strIpPorts.split("|")
        listIpPort = []
        for ipPort in ipPorts:
            aux = ipPort.split(",")
            listIpPort.append({
                "ip":aux[0],
                "port":aux[1]
            })
        return listIpPort

    def __processOltsInfo(self,ipPorts):
        listObjIpPort = self.__strToListIpPorts(ipPorts)
        oltsInfo = []
        for ipPort in listObjIpPort:
            try:
                oltsInfo.append(OltInfo(ipPort["ip"],ipPort["port"]))
            except Exception as e:
                raise e
        return oltsInfo
    
    def __insertPic(self,pic):
        idPic = ""
        try:
            idPic = self.db.insertPic(pic.name)
        except IntegrityError as e:
            self.log.logError(e)
            print(e)
            raise e
        return idPic
    
    def __insertOltsInfo(self,pic):
        for oltInfo in pic.oltsInfo:
            try:
                idOltInfo = self.db.insertOltInfo(oltInfo)
                self.db.insertOnuInfo(oltInfo.onus,idOltInfo)
            except Exception as e:
                self.log.logError(e)



