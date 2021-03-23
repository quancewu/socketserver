import socket
import time
import os,re
import queue
import socketserver
import threading
from file_manager.manager import LogWriter
from datetime import datetime

class ThreadedTCPServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
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
        LogWriter.log('info','Connect from: {0}:{1}'.format(self.client_address[0],self.client_address[1]))
        while(True):
            data = self.request.recv(BUFSIZE)
            filenowname = 'd11{}.txt'.format(datetime.now().strftime('%Y%m%d_%H'))
            bdata = self.queue.put(data)
            # with open(os.path.join(ex_path,'data',filenowname),'a') as filename:
                # filename.write(data.decode('utf-8','ignore'))
            if len(data) == 0: # connection closed
                LogWriter.log('info','client closed connection.')
                break
    def finish(self):
        LogWriter.log('info',"client {0}:{1} disconnect!".format(self.client_address[0],self.client_address[1]))

def connect():
    HOST = socket.gethostname()
    PORT = 4001
    
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    print('Server is starting up...')
    print('Host: {0}, listen to port: {1}'.format(HOST,PORT))

class SocketServer(threading.Thread):
    dummy_data = queue.Queue(maxsize=300)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def run(self):
        HOST = socket.gethostname()
        PORT = 4001
        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler, queue=dummy_data)
        server_thread = threading.Thread(target=server.serve_forever,name='socket')
        # server_thread.daemon = True
        server_thread.start()
        uploader = threading.Thread(target=decode_data, args=(dummy_data,),name='uploader')
        uploader.start()
        print(threading.enumerate())
        print('Server is starting up...')
        print('Host: {0}, listen to port: {1}'.format(HOST,PORT))

            
if __name__=='__main__':
    connect()