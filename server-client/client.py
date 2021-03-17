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
        self.closed = False
        
    def start_client(self):
        connected = False
        counter = 0
        while not connected and counter < 3:
            try:
                self.client_socket.connect((self.ip, self.port))  # connect to the server
                connected = True
            except ConnectionRefusedError:
                connected = False
                print("Couldn't connect to server. Retrying...")
                sleep(SLEEP_TIME)
                counter += 1
        print('Stop trying connecting')

    def send_message(self,):
        message = self.validate_msg()
        try:
            if not self.closed:
                self.client_socket.send(message.encode())
                data = self.client_socket.recv(DATA_SIZE).decode()  # receive response

                print('Received from server: ' + data)  # show in terminal
            else:
                print('Server is already closed')
        except ConnectionAbortedError:
            print('Server already closed. Closing client...')
            if not self.closed:
                self.client_socket.close()
                self.closed = True

    def validate_msg(self):
        msg = input(" -> ")  # take input
        while msg == '':
            msg = input(" -> ")  # take input
        return msg

    def close_channel(self):
        if not self.closed:
            self.client_socket.send(closing_msg.encode())
            data = self.client_socket.recv(DATA_SIZE).decode()
            print('Received from server: ' + data)
        self.client_socket.close()  # close the connection
