import socket
import time
import os
from datetime import datetime

HOST = '0.0.0.0'
PORT = 4001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

while True:
    conn, addr = server.accept()
    print('connected by ' + str(addr))

    while True:
        ex_path = os.path.dirname(os.path.abspath(__file__))
        indata = conn.recv(1024)
        filenowname = 'd11{}.txt'.format(datetime.now().strftime('%Y%m%d'))
        with open(os.path.join(ex_path,'data',filenowname),'a') as filename:
            filename.write(indata.decode('utf-8'))
        if len(indata) == 0: # connection closed
            conn.close()
            print('client closed connection.')
            break
        print('recv: ' + indata.decode())

        outdata = 'echo ' + indata.decode()
        # conn.send(outdata.encode())