import os
import socket
from sys import argv
from time import sleep

default_ip = '127.0.0.1'
default_port = 5000

DATA_SIZE = 1024
SLEEP_TIME = 2
closing_msg = 'endconn'

class Client():
    def __init__(self, ip=default_ip, port=default_port, name=os.getlogin()):
        """Init function."""
        self.ip = ip 
        self.port = port
        self.name = name
        self.path = os.getcwd() + os.sep + 'users' + os.sep + name + '.json'
        self.client_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)  # instantiate
        
    def start_client(self):
        connected = False
        while not connected:
            try:
                self.client_socket.connect((self.ip, self.port))  # connect to the server
                connected = True
            except ConnectionRefusedError:
                connected = False
                print("Couldn't connect to server. Retrying...")
                sleep(SLEEP_TIME)

    def send_message(self,):
        message = self.validate_msg()
        self.client_socket.send(message.encode())
        data = self.client_socket.recv(DATA_SIZE).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

    def validate_msg(self):
        msg = input(" -> ")  # take input
        while msg == '':
            msg = input(" -> ")  # take input
        return msg

    def close_channel(self):
        self.client_socket.send(closing_msg.encode())
        data = self.client_socket.recv(DATA_SIZE).decode()
        print('Received from server: ' + data)
        self.client_socket.close()  # close the connection
