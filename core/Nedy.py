import subprocess
import pymysql
from .APIDB import APIDB
from .MiscTools import MiscTools
from pymysql.err import IntegrityError
import pexpect
from datetime import datetime


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
#------------------------------------------QUERIES-----------------------------------------------------------

    def getDevice(self, ip):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute("select ip, hostname, model, uptime, object_id, descr AS description, ping AS responded_ping, snmp AS responded_snmp, last_update from devices where ip = %s", ip)
            
            data = cur.fetchone()
            
            if (cur.rowcount == 0):
                return "Equipo desconocido: " + ip
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()

    def getDevicebyNetwork(self, ip):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute("select ip, hostname, model, uptime, object_id, descr AS description, ping AS responded_ping, snmp AS responded_snmp, last_update from devices where ip like '" + ip + "%' and snmp = 1")
            
            data = cur.fetchall()
            
            if (cur.rowcount == 0):
                return "Equipo desconocido: " + ip
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()
            
    def getRegisteredNetworks(self):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute("select network from networks")
            
            data = cur.fetchall()
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()
    
    def getInfoByHostname(self, value):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute("select ip, hostname, model, uptime, object_id, descr AS description, ping AS responded_ping, snmp AS responded_snmp, last_update from devices where hostname like '%" + value + "%' and snmp = 1")
            
            data = cur.fetchall()
            
            if (cur.rowcount == 0):
                return "Equipo desconocido: " + value
            
            return data
        
        except Exception:
            raise
        finally:
            self.close()

    def getInfoByNameOrDescr(self, value):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute("SELECT device_ip, i.if_index, if_name, if_descr, if_alias, if_status, if_type, 0 as onu_number, 'none' as onu_alias, last_update FROM interfaces i where i.if_name LIKE '%" + value + "%'")
            
            
            if (cur.rowcount == 0):
                cur.execute("SELECT device_ip, i.if_index, if_name, if_descr, if_alias, if_status, if_type, 0 as onu_number, 'none' as onu_alias, last_update FROM interfaces i where i.if_descr LIKE '%" + value + "%'")
                
                if (cur.rowcount == 0):
                    return "Valor no encontrado"
                else:
                    data = cur.fetchall()
            else:
                data = cur.fetchall()
                
            return data
        
        except Exception:
            raise
        finally:
            self.close()

    def getInfoByAlias(self, value):
        try:
            self.connect()
            cur=self.db.cursor(pymysql.cursors.DictCursor)
            
            cur.execute("SELECT device_ip, i.if_index, if_name, if_descr, if_alias, if_status, if_type, 0 as onu_number, 'none' as onu_alias, last_update FROM interfaces i where i.if_alias LIKE '%" + value + "%'")
            if (cur.rowcount != 0):
                data = cur.fetchall()
            else:
                data = []
            
            cur.execute("SELECT device_ip, i.if_index, if_name, if_descr, if_alias, if_status, if_type, onu as onu_number, alias as onu_alias, o.sn, o.last_update FROM interfaces i, onus o WHERE i.if_index = o.if_index AND i.device_ip = o.ip AND o.alias LIKE '%" + value + "%'")
            data2 = cur.fetchall()
            
            for d in data2:
                data.append(d)
                
            return data
        
        except Exception:
            raise
        finally:
            self.close()



    def getInfoByPort(self, ip, port, onu):
        try:
                self.connect() 
                cur = self.db.cursor(pymysql.cursors.DictCursor)
                

                # Consulta SQL básica
                sql_query = "SELECT device_ip, i.if_index, if_alias, onu AS onu_number, alias AS onu_alias, o.sn, o.last_update \
                            FROM interfaces i, onus o \
                            WHERE i.if_index = o.if_index AND i.device_ip = o.ip \
                            AND ip = %s \
                            AND if_name = %s"

                # Si onu es diferente de 0, añadimos la condición a la consulta
                if onu != 0:
                    sql_query += " AND onu = %s"
                    cur.execute(sql_query, (ip, port, onu))
                else:
                    cur.execute(sql_query, (ip, port))

                # Validar rowcount y asignar data en consecuencia
                if cur.rowcount != 0:
                    data = cur.fetchall()
                else:
                    data = []

                return data

        except Exception as e:
            raise e
        finally:
                self.close()
            
    def inserAddInfoRequest(self, model, name, oid):
        try:
            self.connect()
            cur=self.db.cursor()
            
            cur.execute("INSERT INTO `add_disco_requests` (`model`, `name`, `oid`) VALUES (%s, %s, %s);", (model, name, oid))
        
        except Exception:
            raise
        finally:
            self.close()
            
    def inserNewNetwork(self, net):
        try:
            self.connect()
            cur=self.db.cursor()
            
            cur.execute("INSERT INTO `networks` (`network`) VALUES (%s);", (net))
            
        except IntegrityError:
            raise
        except Exception:
            raise
        finally:
            self.close()

#-----------------------------------------/EXECS-----------------------------------------------------------

    def ping(self, net, mask):
        nedy = APIDB().getProperty("nedy.path")
        
        out = subprocess.run([nedy, "-fping", net + "/" + mask], capture_output=True, universal_newlines=True)
        ips = out.stdout.split()
        
        
        return ips
    
    def version(self):
        nedy = APIDB().getProperty("nedy.path")
        
        out = subprocess.run([nedy, "-v"], capture_output=True, universal_newlines=True)
        l = out.stdout.split("\n")
        
        return l
    
    
    def runByRequest(self, ip, comm, oid):
        nedy = APIDB().getProperty("nedy.path")
        
        out = subprocess.run([nedy, "-runbyrequest", ip, comm, oid], capture_output=True, universal_newlines=True)
        
        response = out.stdout.split("\n")
        
        return response
    
    def discoByRequest(self, ip):
        nedy = APIDB().getProperty("nedy.path")
        
        out = subprocess.run([nedy, "-discoverbyrequest", ip], capture_output=True, universal_newlines=True)
        
        return out.stdout
    
    
#-----------------------------------------/EXPECT-----------------------------------------------------------

    def getOnuDetailZTE(self, ip, user, password, portOnu, prompt="#$"):
        toShow = {}
        outs = []
        cont = 0
        
        try: 
            print("1")
            with pexpect.spawn ('telnet ' + ip, timeout=10, encoding="utf-8") as telnet:
                telnet.expect('Username:')
                telnet.sendline(user)
                telnet.expect('Password:')
                telnet.sendline(password)
                telnet.expect(prompt)
                telnet.sendline("terminal length 0")
                telnet.expect(prompt)
                print("2")
                telnet.sendline('show gpon onu detail-info ' + self.getModelPromptText(ip) + portOnu) #1/2/1:127
                match = telnet.expect([prompt, pexpect.TIMEOUT, pexpect.EOF])
                print("3")
                if match == 1:
                    print(f"Symbol {prompt} is not found in output. Resulting output is written to dictionary")
                    print(telnet.before)
                elif match == 2:
                    print("Connection was terminated by server")
                    return toShow
                else:
                    print("4")
                    cmd_show_data = telnet.before
                    cmd_output = cmd_show_data.split('\r\n')
                
            # Aca nos traemos las variables y las armamos con un dict asi las mostramos
            for data in cmd_output:
                try: 
                    if "-------" in data:
                        break
                    
                    l = data.split(':')
                    key = str(l[0]).strip()
                    value = str(l[1]).strip()
                    
                    toShow[key] = value
                except Exception:
                    pass
            
            print(toShow)
            # En este FOR calculamos cantidad de caidas el dia de hoy
            for i in range(len(cmd_output) - 13, len(cmd_output) - 3):
                out = []
                d = cmd_output[i].split("  ")
                print("5")
                d.remove('')
                print(d)
                nro = str(d[0]).strip()
                ap = str(d[1]).strip()
                ot = str(d[3]).strip()
                cause = str(d[5]).strip()
                if "0000-00-00 00:00:00" not in ot:
                    offlineTime = datetime.strptime(ot, '%Y-%m-%d %H:%M:%S')
                    if offlineTime.date() == datetime.today().date():
                        cont = cont + 1
                
                out.append(nro)
                out.append(ap)
                out.append(ot)
                out.append(cause)
                
                outs.append(out)
            
            toShow['Cantidad de caidas de hoy'] = str(cont)
            toShow['Detalle de Caidas'] = outs
                
            return toShow
    
        except Exception:
            raise
        
    
    def getOnuDetailHuawei(self, ip, user, password, serial, prompt=">$", ena="#$"):
        toShow = {}
        n = 5
        
        try: 
            print("1")
            with pexpect.spawn ('telnet ' + ip, timeout=10, encoding="utf-8") as telnet:
                telnet.expect('>>User name:')
                telnet.sendline(user)
                telnet.expect('>>User password:')
                telnet.sendline(password)
                telnet.expect(prompt)
                telnet.sendline("enable")
                telnet.expect(ena)
                telnet.sendline("scroll 512")
                telnet.expect(ena)
                print("2")
                telnet.sendline('display ont info by-sn ' + serial + ' | include :')
                telnet.expect("<cr>||<K>")
                telnet.sendline("\r\n")
                match = telnet.expect([ena, pexpect.TIMEOUT, pexpect.EOF])
                print("3")
                if match == 1:
                    print(f"Symbol {prompt} is not found in output. Resulting output is written to dictionary")
                    print(telnet.before)
                elif match == 2:
                    print("Connection was terminated by server")
                    return toShow
                else:
                    print("4")
                    cmd_show_data = telnet.before
                    cmd_output = cmd_show_data.split('\r\n')
                
            del cmd_output[:n]
            # Aca nos traemos las variables y las armamos con un dict asi las mostramos
            for data in cmd_output:
                try: 
                    l = data.split(':$')
                    key = str(l[0]).strip()
                    value = str(l[1]).strip()
                    
                    toShow[key] = value
                except Exception:
                    pass
            
            print(toShow)
                
            return toShow
    
        except Exception:
            raise
    
    
    def getModelPromptText(self, ip):
        device = self.getDevice(ip)
        
        print(device)
        
        model = device['model']
        
        if "C600" in model:
            return 'gpon_onu-'
        else:
            return 'gpon-onu_'
        
  
 