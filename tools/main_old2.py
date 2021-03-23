import socket
import time
import os,re
import socketserver
import threading
import queue
from datetime import datetime
ex_path = os.path.dirname(os.path.abspath(__file__))
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


class decode_data(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self,name='uploader')
        print('uploader start')
        self.data = queue
        self.run()
    def run(self):
        old_data = b''
        while True:
            flag = []
            readonline = self.data.get()
            readin = old_data + readonline
            print('======================================')
            readin = readin.replace(b'\r\n\r\n',b'\r\n')
            readin = readin.split(b'\r\n')
            if len(readin[-1].split()) == 9:
                dummy2 = readin
                old_data = b''
            else:
                dummy2 = readin[0:-1]
                old_data = readin[-1]
            for i,idata in enumerate(dummy2):
                # print('readRawdata',idata)
                if idata[0:1] == b'R':
                    flag.append((i,'R_flag'))
                    break
                elif idata[0:1] == b'P':
                    flag.append((i,'P_flag'))
                else:
                    pass
            if flag != []:
                for iflaging in flag:
                    iflag = iflaging[0]
                    if len(dummy2[iflag:]) >= 6 and iflaging[1] == 'P_flag':
                        P_data =  dummy2[iflag].decode().replace('P','').split()
                        Datetime = datetime(2000+int(P_data[0]),int(P_data[1]),int(P_data[2]),int(P_data[3]),int(P_data[4]),int(P_data[5]))
                        if dummy2[iflag+1][0:1] == b'N':
                            N_data = re.sub(r'[N].','',dummy2[iflag+1].decode()).split()
                            Data['N_data'].append([Datetime]+N_data)
                            read_N_data = ''
                            for i in dummy2[iflag+2:iflag+6]:
                                read_N_data += i.decode()
                            dummy = re.sub(r'[Cc]..','',read_N_data).split()
                            C_data = [int(dummy[i])-int(dummy[i+1]) for i in range(15)]
                            C_data = C_data + [int(dummy[i])-int(dummy[i+1]) for i in range(16,31)] + [int(dummy[-1])]
                            Data['C_data'].append([Datetime]+C_data)
                            old_poped_data = dummy2[iflag+6:]
                        elif dummy2[iflag+1][0:1] == b'K':
                            K_data = dummy2[iflag+1].decode().replace('K','').split()
                            Data['K_data'].append([Datetime]+K_data)
                            old_poped_data = dummy2[iflag+1:]
                    elif len(dummy2[iflag:]) >= 8 and iflaging[1] == 'R_flag':
                        old_poped_data = dummy2[iflag+8:]
                    else:
                        print('too short',len(dummy2[iflag:]))
                old_loop = b''
                for i in old_poped_data:
                    old_loop = old_loop + i + b'\r\n'
                old_data = old_loop + old_data
            else:
                old_loop = b''
                for i in dummy2:
                    old_loop = old_loop + i + b'\r\n'
                old_data = old_loop + old_data
            print('read data for {} times'.format(len(Data['C_data'])))

class ThreadedTCPServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    # pass
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True,
                 queue=None):
        self.queue = queue
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass,
                           bind_and_activate=bind_and_activate)

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.queue = server.queue
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        BUFSIZE = 1024
        print('Connect from: {0}:{1}'.format(self.client_address[0],self.client_address[1]))
        while(True):
            
            data = self.request.recv(BUFSIZE)
            filenowname = 'd11{}.txt'.format(datetime.now().strftime('%Y%m%d_%H'))
            bdata = self.queue.put(data)
            with open(os.path.join(ex_path,'data',filenowname),'a') as filename:
                # filename.write(data.decode('utf-8','ignore'))
            if len(data) == 0: # connection closed
                # self.close()
                print('client closed connection.')
                break
            # print(data.decode('utf-8','ignore'),end='')
            # self.request.sendall(data)
            time.sleep(0.1)
    
    # def handle(self):
    #     BUFSIZE = 1024
    #     print('Connect from: {0}:{1}'.format(self.client_address[0],self.client_address[1]))
    #     data = ''
    #     while(True):
    #         dummy = self.request.recv(BUFSIZE).decode('utf-8','ignore')
    #         filenowname = 'd11{}.txt'.format(datetime.now().strftime('%Y%m%d_%H'))
    #         with open(os.path.join(ex_path,'data',filenowname),'a') as filename:
    #             filename.write(dummy)
    #         if len(dummy) == 0: # connection closed
    #             self.close()
    #             print('client closed connection.')
    #             break
    #         print(dummy,end='')
    #         # self.request.sendall(data)
    #         dummy = dummy.replace('\r\n\r\n','\r\n')
    #         time.sleep(0.1)
                
    def finish(self):
        print("client {0}:{1} disconnect!".format(self.client_address[0],self.client_address[1]))
def connect():
    HOST = socket.gethostname()
    PORT = 4001
    dummy_data = queue.Queue(maxsize=300)
    
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler, queue=dummy_data)
    server_thread = threading.Thread(target=server.serve_forever,name='socket')
    # server_thread.daemon = True
    server_thread.start()
    # threading.Thread.
    uploader = threading.Thread(target=decode_data, args=(dummy_data,),name='uploader')
    uploader.start()
    print(threading.enumerate())
    print('Server is starting up...')
    print('Host: {0}, listen to port: {1}'.format(HOST,PORT))
            
if __name__=='__main__':
    connect()