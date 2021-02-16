import os
import socket
from sys import argv
from time import sleep

default_ip = '127.0.0.1'
default_port = 5000

def client_only(host=default_ip, port=default_port, name=os.getlogin()):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    connected = False
    while not connected:
        try:
            client_socket.connect((host, port))  # connect to the server
            connected = True
        except ConnectionRefusedError:
            connected = False
            print("Couldn't connect to server. Retrying...")
            sleep(2)

    closing_msg = 'endconn'

    message = validate_msg()

    while message.lower().strip() not in ['bye', 'q', '0', 'exit', 'quit']:
        print('Client {} connected to {}'.format(name, host))
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = validate_msg()

    client_socket.send(closing_msg.encode())  # send closing message
    client_socket.close()  # close the connection

def validate_msg():
    msg = input(" -> ")  # take input
    while msg == '':
        msg = input(" -> ")  # take input
    return msg

if __name__ == '__main__':
    if len(argv)>3:
        try:
            client_only(host=argv[1], port=argv[2], name=argv[3])
        except:
            print('Some error happened')
    else:
        client_only()
