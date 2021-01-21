#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

host = 'www.google.com'
port = 80

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
    
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)
        
        #continuously listen for connections
        while True:
            conn, addr = proxy_start.accept()

            p = Process(target=handle_echo, args=(addr, conn))
            p.daemon = True
            p.start()


def handle_echo(addr, conn):
    print("Connected by", addr)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
        remote_ip = get_remote_ip(host)
        proxy_end.connect((remote_ip, port))
    
        #recieve data, wait a bit, then send it back
        full_data = conn.recv(BUFFER_SIZE)
        proxy_end.sendall(full_data)
        proxy_end.shutdown(socket.SHUT_WR)
        data = proxy_end.recv(BUFFER_SIZE)
        conn.send(data)

    conn.close()

if __name__ == "__main__":
    main()
