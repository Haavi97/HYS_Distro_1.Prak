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
- [ ] Automatic connection to new ip addresses connecting to the user server (client)
- [ ] Error handling
- [ ] Implement over the internet not only locally
"""

import os
import socket
import threading
from sys import argv
from time import sleep

default_ip = '127.0.0.1'
default_port = 5000

DATA_SIZE = 1024
closing_msg = 'endconn'


class User():
    r"""Documentation to User class.

    This class handles ip address storing and retrieving them
    from a txt file.

    Parameters
    ----------
    host : int
        (default value = 127.0.0.1)
        Server ip address
    port : int 
        (default value = 5000)
        Server port
    name : str
        User name
    """

    def __init__(self, host=default_ip, port=default_port, name=os.getlogin()):
        """Init function."""
        self.host = host
        self.port = port
        self.name = name
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        """Starts the server listening and accept any coming connection."""
        self.server_socket.bind((self.host, self.port))

        self.server_socket.listen()
        while True:
            self.accept_connection()

    def accept_connection(self):
        """Accepts incoming connections to the server."""
        conn, address = self.server_socket.accept()
        # conn.setblocking(False)
        print('\rConnection from: {}\n->'.format(address), end='')
        threading.Thread(target=self.listen_data, args=(conn, address)).start()

    def listen_data(self, conn, address):
        """Starts to received data from the given client.

        Parameters
        ----------
        conn : ______
            connection object from server_socket.accept function

        address : ______
            address object from server_socket.accept function
        """
        try:
            while True:
                data = conn.recv(DATA_SIZE).decode()
                if data == closing_msg:
                    break
                print('\rFrom connected user: {}\n->'.format(data), end='')
                conn.send(
                    ('Received {} bytes properly'.format(len(data))).encode())

            conn.close()  # close the connection

        except ConnectionResetError:
            print("Most probably closed the client or something else happened")

    def start_client(self, ip, host_port):
        """Starts client connection to the given server ip address and port.

        Parameters
        ----------
        ip : str
            ip address of the server

        host_port : int
            port number of the server
        """
        client_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)  # instantiate
        connected = False
        while not connected:
            try:
                client_socket.connect((ip, host_port))  # connect to the server
                connected = True
            except ConnectionRefusedError:
                connected = False
                print("Couldn't connect to server. Retrying...")
                sleep(2)

        message = self.validate_msg()

        while message.lower().strip() not in ['bye', 'q', '0', 'exit', 'quit']:
            print('Client {} connected to {} in port {}'.format(
                self.name, ip, host_port))
            client_socket.send(message.encode())  # send message
            data = client_socket.recv(DATA_SIZE).decode()  # receive response

            print('Received from server: ' + data)  # show in terminal

            message = self.validate_msg()

        client_socket.send(closing_msg.encode())  # send closing message
        client_socket.close()  # close the connection

    def validate_msg(self):
        msg = input(" -> ")  # take input
        while msg == '':
            msg = input(" -> ")  # take input
        return msg


if __name__ == '__main__':

    server_port, client_port, name = int(argv[1]), int(argv[2]), argv[3]
    user = User(port=server_port, name=name)

    server = threading.Thread(target=user.start_server)
    client = threading.Thread(target=user.start_client,
                              args=(default_ip, client_port))

    server.start()
    client.start()
