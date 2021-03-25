"""User script.

>Module that implements a simple server-client that can accept
several clients and connect to several clients

# Usage
CLI application that requires 2 parameters:
1. Server port
2. User name

I also needs to have an .ip file with a list of the different servers it can connect to.
Those files must be in the folder *users*
Example file user1.ip:
```
127.0.0.1:6000
127.0.0.1:7000

```

There is no restriction for the name, but the port must not be from the reserved ones.

Example of usage in CLI:
```bash
user.py 5000 user1
```

## Usage example in different terminal windows

Terminal 1:
```bash
user.py 5000 user1
```
user1.ip:
```
127.0.0.1:6000
127.0.0.1:7000

```

Terminal 2:
```bash
user.py 6000 user2
```
user2.ip:
```
127.0.0.1:5000
127.0.0.1:7000

```

With the previous 2 code lines the two users can message themselves. You can \
add a third user but the can only send to one of the other users (servers):

Terminal 3 (this example connects to user 1 and listens in port 7000):
```bash
user.py 7000 user3
```
user1.ip:
```
127.0.0.1:6000
127.0.0.1:5000

```

# Plan
- [x] Server client user with multiple connections
- [x] Connection to several ip addresses (client)
- [x] Automatic connection to new ip addresses connecting to the user server (client)
- [ ] Send all messages over HTTP
- [ ] Parse GET and POST requests
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
from datetime import datetime

sys.path.insert(1, os.pardir + os.sep + "ip_address")
from client import Client
from ip_address import IPHandler
from request_parsing import *

default_ip = '127.0.0.1'
default_port = 5000


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

    def __init__(self, host=default_ip, port=default_port, name=os.getlogin()):
        """Init function."""
        self.host = host  # server ip address
        self.port = port  # server port
        self.name = name  # user name

        self.TIMEOUT = 5
        self.DATA_SIZE = 1024
        self.closing_msg = 'endconn'

        self.method = 'POST'

        self.help = '\n\n1. Send message\n' + \
            '2. Close client\n' + \
            '3. Close server\n' + \
            '4. Close all\n' + \
            '5. Set request method POST/GET\n\n'
        self.headers_ok = 'HTTP/1.1 200 OK\r\n' + \
            'Date: {time_now}\r\n' + \
            'Server: {host}\r\n' + \
            'Last-Modified: {time_now}\r\n' + \
            'Content-Type: {content_type}\r\n' + \
            'Content-Length: {content_length}\r\n' + \
            'Connection: close\r\n' + \
            '\r\n'

        self.path = os.getcwd() + os.sep  # path of the script

        # path with the json file for handling user data
        self.user_path = self.path + 'users' + os.sep + name + '.json'
        # path with the ip addresses file the user tries to connect at the beginning
        self.ips_path = self.path + 'users' + os.sep + name + '.ip'
        # socket for the server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = None   # Attribute that will contain the thread for the server
        # Helper class for reading and writing to the ip addresses file
        self.iphandler = IPHandler(file=self.ips_path)
        self.clients_list = self.iphandler.get_ip_listdef()
        self.clients = []

        self.write_json(True)
        self.start_user()

    def start_user(self):
        """Executes methods start server and start clients.

        After that starts the cli menu display.
        """
        self.server = threading.Thread(target=self.start_server)
        self.server.start()

        self.start_clients()

        self.menu()

    def start_clients(self):
        """Reads from the clients list which are the clients it should connect
        to.

        It adds each of the client objects to a list with the possible
        clients. Then it starts each one of them in a separate thread.
        """
        for i in range(len(self.clients_list)):
            current_ip, current_port = self.clients_list[i].split(':')
            self.clients.append(
                Client(ip=current_ip, port=int(current_port), name=self.name + 'Client' + str(i)))
            self.client_thread = threading.Thread(
                target=self.clients[i].start_client)
            self.client_thread.start()

    def start_server(self):
        """Starts the server listening and accept any coming connection.

        It has a timeout set as a global variable (TIMEOUT) after which
        stops and retries again. That way it can check (is_open()) if in
        the meanwhile the server should be closed.
        """
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.server_socket.settimeout(self.TIMEOUT)
        while self.is_open():
            self.accept_connection()

    def accept_connection(self):
        """Accepts incoming connections to the server, creating a separate
        thread for each one."""
        try:
            conn, address = self.server_socket.accept()
            # conn.setblocking(False) {}\n'.format(address), end='')
            threading.Thread(target=self.listen_data,
                             args=(conn, address)).start()
        except:
            pass

            pass

    def listen_data(self, conn, address):
        """Starts to received data from the given client. It has a timeout set
        as a global variable (TIMEOUT) after which stops and retries again.
        That way it can check (is_open()) if in the meanwhile the server should
        be closed.

        Parameters
        ----------
        conn : socket.socket
            connection object from server_socket.accept function

        address : (int, int)
            address object from server_socket.accept function. Tuple containing (ip address, port)
        """
        try:
            conn.settimeout(self.TIMEOUT)
            while self.is_open():
                try:
                    data = conn.recv(self.DATA_SIZE).decode()
                    if data == '' or data == None:
                        data = 'void data'
                    else:
                        if is_POST(data):
                            url = get_request_path(data)
                            data = get_request_data(data)
                        elif is_GET(data):
                            url = get_request_path(data)
                            data = get_request_data(data)
                        else: 
                            print('Not a valid request')
                        if data == self.closing_msg:
                            print('Stop listening to client: {}'.format(address))
                            break
                        if url == '/getblocks':
                            body = str(self.clients_list)
                        elif url == '/addips':

                            body = 'Added ip address: {}'.format(data)
                        else:
                            body = 'Received {} bytes properly'.format(len(data))
                        print('\rFrom connected user: {}\n->'.format(data), end='')
                        body_bytes = body.encode('ascii')
                        header_bytes = self.headers_ok.format(
                            time_now=datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                            content_type="text/html",
                            content_length=len(body_bytes),
                            host=str(self.host) + ":" + str(self.port)
                        ).encode('iso-8859-1')

                        payload = header_bytes + body_bytes

                        conn.sendall(payload)
                except:
                    pass
            if not self.is_open():
                try:
                    conn.send((self.closing_msg.encode()))
                except:
                    pass  # client already closed
            conn.close()  # close the connection

        except ConnectionResetError:
            print("Most probably closed the client or something else happened")

    def is_open(self):
        """Returns if the server should be listening or not."""
        while True:
            try:
                with open(self.user_path) as file:
                    json_data = json.load(file)
                return json_data['open_port']
            except:
                pass

    def write_json(self, value):
        """Writes to the json file the given boolean value.

        It indicates if the server should be running or not.

        Parameters
        ----------
        value : boolean
        """
        success = False
        while not success:
            try:
                with open(self.user_path, 'w') as f:
                    json.dump({'open_port': value}, f)
                    success = True
            except:
                pass

    def close_all_clients(self):
        """Iterates over the Client objects lists trying to close each of the
        clients."""
        for client in self.clients:
            try:
                client.close_channel()
            except ConnectionAbortedError:
                print("Already closed client")
            except:
                self.write_json(False)
                self.write_json(False)

    def close_server(self):
        """Indicates that the server shouldn't be running.

        The server will close after the next TIMEOUT.
        """
        self.write_json(False)

    def menu(self):
        """Displays in the cli the different options for the user."""
        while True:
            user_input = input(self.help)
            if user_input == '1':
                self.messaging_selection()  # send message to server
            elif user_input == '2':
                self.close_all_clients()
            elif user_input == '3':
                self.close_server()
            elif user_input == '4':
                try:
                    self.close_server()
                except ConnectionAbortedError:
                    print("Already closed server")
                except:
                    self.write_json(False)
                self.close_all_clients()
                break
            elif user_input == '5':
                self.request_type()
            else:
                print('Please type a valid number')

    def messaging_selection(self):
        """CLI menu for selecting if sending a message to all or only to a
        specific user."""
        print('\n\n   1. Send message to specific user\n' +
              '   2. Send message to all\n' +
              '   0. Go back')
        user_input = input()
        if user_input == '1':
            self.specific_user_messaging()
        elif user_input == '2':
            self.send_to_all()
        elif user_input == '0':
            self.menu()
        else:
            print("Please, select a valid option")
            self.messaging_selection()

    def specific_user_messaging(self):
        """CLI menu for sending a message to a specific user."""
        print("        Select user number to message:")
        for i in range(len(self.clients)):
            print("        " + str(i + 1) + '. ' + str(self.clients[i]))
        print("        0. Go back")
        user_input = input()
        user_input = int(user_input)-1
        if user_input == -1:
            self.messaging_selection()
        elif 0 <= user_input < len(self.clients):
            print("            " + str(self.clients[user_input]))
            msg = self.clients[user_input].validate_msg()
            self.clients[user_input].send_message(msg, method=self.method)
        else:
            print("Please, type a valid option")
            self.specific_user_messaging()

    def request_type(self):
        print ('\n\n   1. Set POST as used method\n' + \
        '   2. Set GET as used method\n' + \
        '   0. Go back')
        user_input = input()
        if user_input == '1':
            self.method = 'POST'
            print('Current method: {}'.format(self.method))
        elif user_input == '2':
            self.method = 'GET'
            print('Current method: {}'.format(self.method))
        elif user_input == '0':
            self.menu()
        else:
            print ("Something went wrong!")
            self.request_type()

    def send_to_all(self):
        msg = self.clients[0].validate_msg()
        for client in self.clients:
            client.send_message(msg, method=self.method)

if __name__ == '__main__':
    server_port, name = int(argv[1]), argv[2]
    user = User(port=server_port, name=name)
