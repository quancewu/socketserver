from datetime import datetime,timedelta
import queue
import os,re
import socket
import threading
from socket_lib.socet_server import SocketServer,ThreadedTCPServer,ThreadedTCPRequestHandler
from postgresql_NAHO.nahoapi import NahoApi
from file_manager.manager import DataManager,LogManager,LogWriter,SQLiteManager
from info.info import D11dic

class MixinBase:
    def init(self):
        pass

class MainBase(MixinBase):
    def __init__(self, *args, **kwargs):
        self.init()

class ApiForNahoMixin(MixinBase):
    def init(self):
        super().init()
        LogWriter.log('info','Naho api init')
        # print('Api Naho init')
        NahoApi().start()

class LoggerMixin(MixinBase):
    def init(self):
        super().init()
        LogWriter.log('info','logging init')
        # print('log init')
        LogManager().start()
        
class SQLiteMixin(MixinBase):
    def init(self):
        super().init()
        LogWriter.log('info','SQLite init')
        # print('SQLlite save init')
        SQLiteManager().start()

class D11Logger(MixinBase):
    def init(self):
        super().init()
        LogWriter.log('info','D11Logger init')
        # print('D11Logger init')
        self.recive_data = SocktSeverMixin.dummy_data
        self.Data = []
        threading.Thread(target=self.run).start()
    
    def run(self):
        old_data = ''
        old_poped_data = []
        while True:
            self.Data = []
            flag = []
            readonline = self.recive_data.get().decode()
            readin = old_data + readonline
            readin = readin.replace('\r\n\r\n','\r\n')
            readin = readin.split('\r\n')
            if len(readin[-1].split()) == 9 and readin[-1][0] == 'c':
                dummy2 = readin
                old_data = ''
            else:
                dummy2 = readin[0:-1]
                old_data = readin[-1]
            for i,idata in enumerate(dummy2):
                # print(idata)
                if idata[0] == 'R':
                    flag.append((i,'R_flag'))
                elif idata[0] == 'P':
                    flag.append((i,'P_flag'))
                elif idata[0:1] == 'N':
                    flag.append((i,'N_flag'))
                elif idata[0:1] == 'C':
                    flag.append((i,'C_flag'))
                elif idata[0:1] == 'c':
                    flag.append((i,'c_flag'))
                else:
                    pass
            if flag != []:
                print(flag)
                for iflaging in flag:
                    iflag = iflaging[0]
                    print('data len',len(dummy2[iflag:]))
                    # print(data)
                    if len(dummy2[iflag:]) >= 6 and iflaging[1] == 'P_flag':
                        print(len(dummy2[iflag:]),dummy2[iflag])
                        print(len(dummy2[iflag:]),dummy2[iflag:])
                        if dummy2[iflag+1][0] != 'N' and dummy2[iflag+1][0] != 'K':
                            P_data = (dummy2[iflag]+dummy2[iflag+1]).replace('P','').split()
                            P_data = ['Null' if i=='NA' else i for i in P_data]
                            P_data[25] = P_data[25].replace('A','').replace('M','')
                            Datetime = datetime(2000+int(P_data[0]),int(P_data[1]),int(P_data[2]),int(P_data[3]),int(P_data[4]),int(P_data[5]))-timedelta(hours=8)
                            N_data = re.sub(r'[N].','',dummy2[iflag+2]).split()
                            read_N_data = ''
                            for i in dummy2[iflag+3:iflag+7]:
                                read_N_data += i
                            dummy = re.sub(r'[Cc]..','',read_N_data).split()
                            C_data = [str((int(dummy[i])-int(dummy[i+1]))*10) for i in range(15)]
                            C_data = C_data + [str((int(dummy[i])-int(dummy[i+1]))*10) for i in range(16,31)] + [str(int(dummy[-1])*10)]
                            nullfield1 = ['Null' for i in range(31)]
                            nullfield2 = ['Null' for i in range(7)]
                            self.Data.append(["'{}'".format(Datetime.isoformat())]+N_data+C_data+nullfield1+P_data[6:]+nullfield2+["'{}'".format(datetime.now().isoformat()),'0'])
                            old_poped_data = dummy2[iflag+7:]
                        elif dummy2[iflag+1][0] == 'N':
                            P_data = dummy2[iflag].replace('P','').split()
                            P_data = ['Null' if i=='NA' else i for i in P_data]
                            P_data[25] = P_data[25].replace('A','').replace('M','')
                            Datetime = datetime(2000+int(P_data[0]),int(P_data[1]),int(P_data[2]),int(P_data[3]),int(P_data[4]),int(P_data[5]))-timedelta(hours=8)  
                            N_data = re.sub(r'[N].','',dummy2[iflag+1]).split()
                            read_N_data = ''
                            for i in dummy2[iflag+2:iflag+6]:
                                read_N_data += i
                            dummy = re.sub(r'[Cc]..','',read_N_data).split()
                            C_data = [str((int(dummy[i])-int(dummy[i+1]))*10) for i in range(15)]
                            C_data = C_data + [str((int(dummy[i])-int(dummy[i+1]))*10) for i in range(16,31)] + [str(int(dummy[-1])*10)]
                            nullfield1 = ['Null' for i in range(31)]
                            nullfield2 = ['Null' for i in range(7)]
                            self.Data.append(["'{}'".format(Datetime.isoformat())]+N_data+C_data+nullfield1+P_data[6:]+nullfield2+["'{}'".format(datetime.now().isoformat()),'0'])
                            old_poped_data = dummy2[iflag+6:]
                        elif dummy2[iflag+1][0] == 'K':
                            K_data = dummy2[iflag+1].replace('K','').split()
                            K_data = ['Null' if i=='NA' else i for i in K_data]
                            nullfield1 = ['Null' for i in range(75)]
                            self.Data.append(["'{}'".format(Datetime.isoformat())]+nullfield1+P_data[6:]+K_data+["'{}'".format(datetime.now().isoformat()),'0'])
                            old_poped_data = dummy2[iflag+1:]
                    elif len(dummy2[iflag:]) >= 8 and iflaging[1] == 'R_flag':
                        old_poped_data = dummy2[iflag+8:]
                    else:
                        pass
                old_loop = ''
                for i in old_poped_data:
                    old_loop = old_loop + i + '\r\n'
                old_data = old_loop + old_data
            else:
                old_loop = ''
                for i in dummy2:
                    old_loop = old_loop + i + '\r\n'
                old_data = old_loop + old_data
            if len(self.Data) != 0:
                # insert_txt = ' ,'.join(['null'] + self.Data[0])
                SQLiteManager.save_SQLite_data(D11dic.code,D11dic.y,
                                D11dic.m,D11dic.identity,
                                D11dic.filename,self.Data,D11dic.sql_data_format)
                upload_array = [[i for i in idata[:-1]]for idata in self.Data]
                NahoApi.upload_pgsql(D11dic.code,D11dic.y,
                                D11dic.m,D11dic.identity,
                                D11dic.filename,upload_array,D11dic.sql_data_format)
            LogWriter.log(
                        'Success',
                        'read data {} row'.format(len(self.Data))
                        )

    def re_run(self):
        old_data = b''
        old_poped_data = []
        while True:
            self.Data = []
            flag = []
            readonline = self.recive_data.get()
            readin = old_data + readonline
            readin = readin.replace(b'\r\n\r\n',b'\r\n')
            readin = readin.split(b'\r\n')
            if len(readin[-1].split()) == 9:
                dummy2 = readin
                old_data = b''
            else:
                dummy2 = readin[0:-1]
                old_data = readin[-1]
            for i,idata in enumerate(dummy2):
                # print(idata)
                if idata[0:1] == b'R':
                    flag.append((i,'R_flag'))
                elif idata[0:1] == b'P':
                    flag.append((i,'P_flag'))
                # elif idata[0:1] == b'N':
                #     flag.append((i,'N_flag'))
                # elif idata[0:1] == b'C':
                #     flag.append((i,'C_flag'))
                # elif idata[0:1] == b'c':
                #     flag.append((i,'c_flag'))
                else:
                    pass
            if flag != []:
                print(flag)
                for iflaging in flag:
                    iflag = iflaging[0]
                    print('data len',len(dummy2[iflag:]))
                    # print(data)
                    if len(dummy2[iflag:]) >= 6 and iflaging[1] == 'P_flag':
                        print(len(dummy2[iflag:]),dummy2[iflag])
                        print(len(dummy2[iflag:]),dummy2[iflag:])
                        if dummy2[iflag+1][0:1] != b'N' and dummy2[iflag+1][0:1] != b'K':
                            P_data = (dummy2[iflag]+dummy2[iflag+1]).decode().replace('P','').split()
                            P_data = ['Null' if i=='NA' else i for i in P_data]
                            P_data[25] = P_data[25].replace('A','').replace('M','')
                            Datetime = datetime(2000+int(P_data[0]),int(P_data[1]),int(P_data[2]),int(P_data[3]),int(P_data[4]),int(P_data[5]))-timedelta(hours=8)
                            N_data = re.sub(r'[N].','',dummy2[iflag+2].decode()).split()
                            read_N_data = ''
                            for i in dummy2[iflag+3:iflag+7]:
                                read_N_data += i.decode()
                            dummy = re.sub(r'[Cc]..','',read_N_data).split()
                            C_data = [str((int(dummy[i])-int(dummy[i+1]))*10) for i in range(15)]
                            C_data = C_data + [str((int(dummy[i])-int(dummy[i+1]))*10) for i in range(16,31)] + [str(int(dummy[-1])*10)]
                            nullfield1 = ['Null' for i in range(31)]
                            nullfield2 = ['Null' for i in range(7)]
                            self.Data.append(["'{}'".format(Datetime.isoformat())]+N_data+C_data+nullfield1+P_data[6:]+nullfield2+["'{}'".format(datetime.now().isoformat()),'0'])
                            old_poped_data = dummy2[iflag+7:]
                        elif dummy2[iflag+1][0:1] == b'N':
                            P_data = dummy2[iflag].decode().replace('P','').split()
                            P_data = ['Null' if i=='NA' else i for i in P_data]
                            P_data[25] = P_data[25].replace('A','').replace('M','')
                            Datetime = datetime(2000+int(P_data[0]),int(P_data[1]),int(P_data[2]),int(P_data[3]),int(P_data[4]),int(P_data[5]))-timedelta(hours=8)  
                            N_data = re.sub(r'[N].','',dummy2[iflag+1].decode()).split()
                            read_N_data = ''
                            for i in dummy2[iflag+2:iflag+6]:
                                read_N_data += i.decode()
                            dummy = re.sub(r'[Cc]..','',read_N_data).split()
                            C_data = [str((int(dummy[i])-int(dummy[i+1]))*10) for i in range(15)]
                            C_data = C_data + [str((int(dummy[i])-int(dummy[i+1]))*10) for i in range(16,31)] + [str(int(dummy[-1])*10)]
                            nullfield1 = ['Null' for i in range(31)]
                            nullfield2 = ['Null' for i in range(7)]
                            self.Data.append(["'{}'".format(Datetime.isoformat())]+N_data+C_data+nullfield1+P_data[6:]+nullfield2+["'{}'".format(datetime.now().isoformat()),'0'])
                            old_poped_data = dummy2[iflag+6:]
                        elif dummy2[iflag+1][0:1] == b'K':
                            K_data = dummy2[iflag+1].decode().replace('K','').split()
                            K_data = ['Null' if i=='NA' else i for i in K_data]
                            nullfield1 = ['Null' for i in range(75)]
                            self.Data.append(["'{}'".format(Datetime.isoformat())]+nullfield1+P_data[6:]+K_data+["'{}'".format(datetime.now().isoformat()),'0'])
                            old_poped_data = dummy2[iflag+1:]
                    elif len(dummy2[iflag:]) >= 8 and iflaging[1] == 'R_flag':
                        old_poped_data = dummy2[iflag+8:]
                    else:
                        pass
                old_loop = b''
                for i in old_poped_data:
                    old_loop = old_loop + i + b'\r\n'
                old_data = old_loop + old_data
            else:
                old_loop = b''
                for i in dummy2:
                    old_loop = old_loop + i + b'\r\n'
                old_data = old_loop + old_data
            if len(self.Data) != 0:
                # insert_txt = ' ,'.join(['null'] + self.Data[0])
                SQLiteManager.save_SQLite_data(D11dic.code,D11dic.y,
                                D11dic.m,D11dic.identity,
                                D11dic.filename,self.Data,D11dic.sql_data_format)
                upload_array = [[i for i in idata[:-1]]for idata in self.Data]
                NahoApi.upload_pgsql(D11dic.code,D11dic.y,
                                D11dic.m,D11dic.identity,
                                D11dic.filename,upload_array,D11dic.sql_data_format)
            LogWriter.log(
                        'Success',
                        'read data {} row'.format(len(self.Data))
                        )

class SocktSeverMixin(MixinBase):
    dummy_data = queue.Queue(maxsize=300)
    def init(self):
        super().init()
        LogWriter.log('info','Socket server init')
        # print('Socket server init')
        HOST = socket.gethostname()
        PORT = 4001
        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler, queue=SocktSeverMixin.dummy_data)
        server_thread = threading.Thread(target=server.serve_forever,name='socket')
        # server_thread.daemon = True
        server_thread.start()
        # print(threading.enumerate())
        LogWriter.log('info','{}'.format(threading.enumerate()))
        LogWriter.log('info','Server is starting up...')
        LogWriter.log('info','Host: {0}, listen to port: {1}'.format(HOST,PORT))
        # print('Server is starting up...')
        # print('Host: {0}, listen to port: {1}'.format(HOST,PORT))