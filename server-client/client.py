import os
import socket
import requests
from sys import argv
from time import sleep

from request_parsing import *

default_ip = '127.0.0.1'
default_port = 5000





class Client():
    def __init__(self, ip=default_ip, port=default_port, name=os.getlogin()):
        """Init function."""
        self.ip = ip
        self.port = int(port)
        self.url = 'http://' + ip + ':' + str(port)
        self.name = name
        self.DATA_SIZE = 1024
        self.SLEEP_TIME = 2
        self.MAX_TRIALS = 10
        self.closing_msg = 'endconn'
        self.path = os.getcwd() + os.sep + 'users' + os.sep + name + '.json'
        self.client_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)  # instantiate
        self.closed = False
        self.headers_post = 'POST {url} HTTP/1.1\r\n' + \
            'Content-Type: {content_type}\r\n' + \
            'Content-Length: {content_length}\r\n' + \
            'Host: {host}\r\n' + \
            'Connection: close\r\n\n' + \
            '\r\n'

    def __str__(self):
        return 'Client ip: ' + str(self.ip) + ' port: ' + str(self.port) 

    def start_client(self):
        connected = False
        counter = 0
        while not connected and counter < self.MAX_TRIALS:
            try:
                self.client_socket.connect(
                    (self.ip, self.port))  # connect to the server
                connected = True
            except ConnectionRefusedError:
                connected = False
                print("Couldn't connect to server in port {}. Retrying...".format(
                    str(self.ip)+':'+str(self.port)))
                sleep(self.SLEEP_TIME)
                counter += 1
        print('Stop trying connecting')

    def send_message(self, message, path='/', method='POST'):
        try:
            if not self.closed:                              
                if method == 'POST':
                    data = requests.post(self.url + path, message)
                    print('Received from server: ' + str(data.text))  # show in terminal
                elif method == 'GET':
                    data = requests.get(self.url + path, message)
                    print('Received from server: ' + str(data.text))
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
            try:
                self.send_message(self.closing_msg)
            except:
                pass # meaning that the server had already closed
        self.client_socket.close()  # close the connection

