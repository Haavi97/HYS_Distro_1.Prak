"""User script.

>Module that implements a simple server-client that can accept
several clients...

# Usage
CLI application that requires 3 parameters:
1. Server port
2. Client port
3. User name

There is no restriction for the name, but the port must not be from the reserved ones.

Example:
```bash
user.py 5000 6000 user1
```

## Usage example in different terminal windows

Terminal 1:
```bash
user.py 5000 6000 user1
```

Terminal 2:
```bash
user.py 6000 5000 user2
```

With the previous 2 code lines the two users can message themselves. You can \
add a third user but the can only send to one of the other users (servers):

Terminal 3 (this example connects to user 1 and listens in port 7000):
```bash
user.py 7000 5000 user3
```

# Plan
- [x] Server client user with multiple connections
- [ ] Connection to several ip addresses (client)
- [ ] Automatic connection to new ip addresses connecting to the user server (client)
- [ ] When a client connects to a server somehow send it's server port so the server \
    can also connect to that user.
- [ ] Automatically add the addresses of new clients.
- [ ] Error handling
- [ ] Implement over the internet not only locally
"""

import os
import sys
import socket
import threading
import json
from sys import argv
from time import sleep

from client import Client
sys.path.insert(1, os.pardir + os.sep + "ip_address")
from ip_address import IPHandler

default_ip = '127.0.0.1'
default_port = 5000

DATA_SIZE = 1024
closing_msg = 'endconn'

TIMEOUT = 5
SLEEP_TIME = 2
# socket.setdefaulttimeout(TIMEOUT)


class User():
    r"""Documentation to User class.

    This class handles ip address storing and retrieving them
    from a txt file.

    Parameters
    ----------
    host : str
        (default value = 127.0.0.1)
        Server ip address
    port : int 
        (default value = 5000)
        Server port
    name : str
        User name
    """

    def __init__(self, ip=default_ip, port=default_port, name=os.getlogin(),
                 client_ip=default_ip, client_port=default_port):
        """Init function."""
        self.ip = ip  # server ip address
        self.port = port
        self.name = name
        self.path = os.getcwd() + os.sep
        self.user_path = self.path + 'users' + os.sep + name + '.json'
        self.ips_path = self.path + 'users' + os.sep + name + '.ip'
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.help = '\n\n1. Send message\n' + \
            '2. Close client\n' + \
            '3. Close server\n' + \
            '4. Print help\n' + \
            '5. Close all\n\n'
        self.server = None
        self.iphandler = IPHandler(file=self.ips_path)
        self.clients_list = self.iphandler.get_ip_listdef()
        self.clients = []

        self.write_json(True)
        self.start_user()

    def start_server(self):
        """Starts the server listening and accept any coming connection."""
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen()
        self.server_socket.settimeout(TIMEOUT)
        while self.is_open():
            self.accept_connection()

    def accept_connection(self):
        """Accepts incoming connections to the server."""
        try:
            conn, address = self.server_socket.accept()
            # conn.setblocking(False)
            print('\rConnection from: {}\n'.format(address), end='')
            threading.Thread(target=self.listen_data,
                             args=(conn, address)).start()
        except:
            pass

    def listen_data(self, conn, address):
        """Starts to received data from the given client.

        Parameters
        ----------
        conn : socket.socket
            connection object from server_socket.accept function

        address : (int, int)
            address object from server_socket.accept function. Tuple containing (ip address, port)
        """
        try:
            conn.settimeout(TIMEOUT)
            while self.is_open():
                try:
                    data = conn.recv(DATA_SIZE).decode()
                    if data == closing_msg:
                        print('Stop listening to client: {}'.format(address))
                        break
                    print('\rFrom connected user: {}\n->'.format(data), end='')
                    conn.send(
                        ('Received {} bytes properly'.format(len(data))).encode())
                except:
                    pass

            if not self.is_open():
                conn.send((closing_msg.encode()))
            conn.close()  # close the connection

        except ConnectionResetError:
            print("Most probably closed the client or something else happened")

    def start_user(self):
        self.server = threading.Thread(target=self.start_server)
        self.server.start()

        self.start_clients()

        self.menu()

    def start_clients(self):
        for i in range(len(self.clients_list)):
            current_ip, current_port = self.clients_list[i].split(':')
            self.clients.append(
                Client(ip=current_ip, port=int(current_port), name=self.name + 'Client' + str(i)))
            self.client_thread = threading.Thread(
                target=self.clients[i].start_client)
            self.client_thread.start()

    def is_open(self):
        while True:
            try:
                with open(self.user_path) as file:
                    json_data = json.load(file)
                return json_data['open_port']
            except:
                pass

    def write_json(self, value):
        success = False
        while not success:
            try:
                with open(self.user_path, 'w') as f:
                    json.dump({'open_port': value}, f)
                    success = True
            except:
                pass

    def menu(self):
        while True:
            user_input = input(self.help)
            if user_input == '1':
                self.messaging_selection()  # send message to server
            elif user_input == '2':
                self.close_all_clients()
            elif user_input == '3':
                self.close_server()
            elif user_input == '4':
                print(self.help)
            elif user_input == '5':
                try:
                    self.close_server()
                except ConnectionAbortedError:
                    print("Already closed server")
                except:
                    self.write_json(False)
                self.close_all_clients()
                break
            else:
                print('Please type a valid number')

    def close_all_clients(self):
        for client in self.clients:
            try:
                client.close_channel()
            except ConnectionAbortedError:
                print("Already closed client")
            except:
                self.write_json(False)
                        
    def close_server(self):
        self.write_json(False)

    def messaging_selection(self):
        print ('\n\n   1. Send message to specific user\n' + \
            '   2. Send message to all\n' + \
            '   0. Go back')
        user_input = input()
        if user_input == '1':
            self.specific_user_messaging()
        elif user_input == '2':
            print ("WIP")
        elif user_input == '0':
            self.menu()
        else:
            print ("Please, select a valid option")

    def specific_user_messaging(self):
        print ("        Select user number to message:")
        for i in range(len(self.clients)):
            print ("        " + str(i + 1) + '. ' +  str(self.clients[i]))
        print ("        0. Go back")
        user_input = input()
        user_input = int(user_input)-1
        if user_input == -1:
            self.messaging_selection()
        elif 0 <= user_input < len(self.clients):
            print ("            "+ str(self.clients[i]))
            self.clients[i].send_message()

if __name__ == '__main__':
    server_port, client_port, name = int(argv[1]), int(argv[2]), argv[3]
    user = User(port=server_port, client_port=client_port, name=name)
