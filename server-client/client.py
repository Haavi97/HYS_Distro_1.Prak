import os
import socket
import requests
from sys import argv
from time import sleep

default_ip = '127.0.0.1'
default_port = 5000





class Client():
    def __init__(self, ip=default_ip, port=default_port, name=os.getlogin()):
        """Init function."""
        self.ip = ip
        self.port = int(port)
        self.url = 'http://' + ip + ':' + str(port) + '/'
        self.name = name
        self.DATA_SIZE = 1024
        self.SLEEP_TIME = 2
        self.MAX_TRIALS = 10
        self.closing_msg = 'endconn'
        self.path = os.getcwd() + os.sep + 'users' + os.sep + name + '.json'
        self.client_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)  # instantiate
        self.closed = False
        self.headers_post = """\
            POST HTTP/1.1\r
            Content-Type: {content_type}\r
            Content-Length: {content_length}\r
            Host: {host}\r
            Connection: close\r
            \r\n"""

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

    def send_message(self, message):
        try:
            if not self.closed:                              
                # body_bytes = message.encode('ascii')
                # header_bytes = self.headers_post.format(
                #     content_type="application/x-www-form-urlencoded",
                #     content_length=len(body_bytes),
                #     host=str(self.ip) + ":" + str(self.port)
                # ).encode('iso-8859-1')

                # payload = header_bytes + body_bytes
                data = requests.post(self.url, message)
                # self.client_socket.send(payload)
                # data = self.client_socket.recv(
                #     self.DATA_SIZE).decode()  # receive response
                print('Received from server: ' + str(data.text))  # show in terminal
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
