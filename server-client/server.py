import os
import socket
import threading
from sys import argv

default_ip = '127.0.0.1'
default_port = 5000

DATA_SIZE = 1024
closing_msg = 'endconn'


def server_only(host=default_ip, port=default_port, name=os.getlogin()):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    server_socket.listen()
    while True:
        accept_connection(server_socket)


def accept_connection(ss):
    conn, address = ss.accept()
    # conn.setblocking(False)
    print('\rConnection from: {}\n->'.format(address), end='')
    threading.Thread(target=listen_data, args=(conn, address)).start()


def listen_data(conn, address):
    try:
        while True:
            data = conn.recv(DATA_SIZE).decode()
            if data == closing_msg:
                break
            print('\rFrom connected user: {}\n->'.format(data), end='')
            conn.send(('Received {} bytes properly'.format(len(data))).encode())

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
