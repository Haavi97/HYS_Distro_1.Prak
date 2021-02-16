import os
import socket
import threading
from sys import argv

default_ip = '127.0.0.1'
default_port = 5000


def server_only(host=default_ip, port=default_port, name=os.getlogin()):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen()
    while True:
        accept_connection(server_socket)


def accept_connection(ss):
    conn, address = ss.accept()  # accept new connection
    # conn.setblocking(False)
    print('Connection from: {}'.format(address))
    threading.Thread(target=listen_data, args=(conn, address)).start()

    
def listen_data(conn, address):
    closing_msg = 'endconn'

    try:
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            print('From connected user: {}'.format(data))
            # send data to the client
            conn.send(('Received {} bytes properly'.format(len(data))).encode())
            if data == closing_msg:
                break

        conn.close()  # close the connection
    except ConnectionResetError:
        print("Most probably closed the client or something else happened")


if __name__ == '__main__':
    if len(argv) > 3:
        try:
            server_only(host=argv[1], port=int(argv[2]), name=argv[3])
        except:
            print('Some error happened')
    else:
        server_only()
