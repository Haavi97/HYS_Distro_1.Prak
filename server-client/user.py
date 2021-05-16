"""User script.

>Module that implements a simple server-client user of a blockchain where different 
transactions are sent and added to blocks that are later mined...

# Usage
CLI application that requires 2 parameters:
1. Server port
2. User name

I also needs to have an .ip file with a list of the different servers it can connect to.
Those files must be in the folder *users*.
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

# Usage example in different terminal windows

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

"""


import os
import os.path
import sys
import socket
import threading
import json
import hashlib
import traceback
import asyncio
from sys import argv
from datetime import datetime
from time import sleep

sys.path.insert(1, os.pardir + os.sep + "ip_address")
from ip_address import IPHandler
sys.path.insert(1, os.pardir + os.sep + "kaevandamine")
from kaevama import kaeva_naivselt, sha256_str
sys.path.insert(1, os.pardir + os.sep + "digital-signature")
from digital_signature import DigitalSignature
from transaction import TransAction
sys.path.insert(1, os.pardir + os.sep + "merkle-puu")
from merklepuu import MerklePuu
sys.path.insert(1, os.pardir + os.sep + "MainNode")
from p2ring import p2ring

from client import Client
from request_parsing import *
from ip_address import IPHandler

default_ip = '127.0.0.1'
default_port = 5000

MAX_ZEROS = 4
MAX_MINE_S = 5 # sekundid
DEFAULT_MINE = 1 # minutid


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

        self.ip = str(self.host) + ':' + str(self.port)

        self.TIMEOUT = 1
        self.DATA_SIZE = 1024
        self.BROADCAST_DELAY = 2
        self.closing_msg = 'endconn'

        self.client_counter = 0
        self.CLIENT_TIMEOUT = 2

        self.method = 'POST'

        self.help = '\n\n1. Actions\n' + \
            '4. Close all\n\n'
            #'2. Close client\n' + \
            #'3. Close server\n' + \
            
        self.headers_ok = 'HTTP/1.1 200 OK\r\n' + \
            'Date: {time_now}\r\n' + \
            'Server: {host}\r\n' + \
            'Last-Modified: {time_now}\r\n' + \
            'Content-Type: {content_type}\r\n' + \
            'Content-Length: {content_length}\r\n' + \
            'Connection: close\r\n' + \
            '\r\n'

        self.path = os.getcwd() + os.sep + 'users' + os.sep + \
            self.name + os.sep  # path of the script
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        # path with the json file for handling user data
        self.user_path = self.path + self.name + '.json'
        self.check_file_exists(self.user_path)

        # path with the ip addresses file the user tries to connect at the beginning
        self.ips_path = self.path + self.name + '.ip'
        
        # Helper class for reading and writing to the ip addresses file
        self.check_file_exists(self.ips_path)
        self.iphandler = IPHandler(file=self.ips_path)
        print('Adding ips from Main Node')
        asyncio.get_event_loop().run_until_complete(p2ring(self.host, self.port, self.iphandler))
        
        # path with the blocks file the user tries to connect at the beginning
        self.blocks_path = self.path + self.name + '.blocks'
        self.check_file_exists(self.blocks_path)
        # path with the unconfirmed transactions
        self.transactions_path = self.path + 'transactions' + '.json'
        if not self.check_file_exists(self.transactions_path):
            with open(self.transactions_path, 'w') as tr_f:
                tr_f.write('[]')
                tr_f.close()
        # socket for the server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = None   # Attribute that will contain the thread for the server
        self.clients_list = self.iphandler.get_ip_listdef()
        self.clients = []
        self.last_client_index = 0
        for i in range(len(self.clients_list)):
            current_ip, current_port = self.clients_list[i].split(':')
            self.clients.append(
                Client(ip=current_ip, port=int(current_port), name=self.name + 'Client' + str(i)))
            self.last_client_index = i

        self.last_client_index += 1

        self.last_mine = datetime.now()
        self.mining = None
        self.kaevandamas = False

        self.digital_signature = DigitalSignature()
        self.digital_signature.create_key(name)

        self.transaction = TransAction()

        self.write_json(True)
        self.start_user()

    def start_user(self):
        """Executes methods start server and start clients.

        After that starts the cli menu display.
        """
        self.server = threading.Thread(target=self.start_server)
        self.server.start()

        self.mining = threading.Thread(target=self.kaevandamine_thread)
        self.mining.start()

        self.start_clients()
        threading.Thread(target=self.delayed_broadcasts).start()
        self.menu()

    def start_clients(self):
        """Reads from the clients list which are the clients it should connect
        to.

        It adds each of the client objects to a list with the possible
        clients. Then it starts each one of them in a separate thread.
        """
        for client in self.clients:
            if not client.is_active():
                self.client_thread = threading.Thread(
                    target=client.start_client)
                self.client_thread.start()

    def delayed_broadcasts(self):
        sleep(self.BROADCAST_DELAY)
        self.broadcast_blocks()
        self.broadcast_users()

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
            self.client_counter += 1
            # print(self.client_counter)
            now = datetime.now()
            current = datetime.now()
            while self.is_open() and (current - now).seconds < self.CLIENT_TIMEOUT:
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
                            data = ''
                        else:
                            print('Not a valid request')
                        if data == self.closing_msg:
                            print('Stop listening to client: {}'.format(address))
                            break
                        body = self.parse_client_request(url, data)
                        # print('\rFrom connected user: {}\n->'.format(data), end='')
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
                current = datetime.now()
            if not self.is_open():
                try:
                    conn.send((self.closing_msg.encode()))
                except:
                    pass  # client already closed
            conn.close()  # close the connection
            self.client_counter -= 1
            # print(self.client_counter)

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
                self.actions()
          #  elif user_input == '2':
          #      self.close_all_clients()
          #  elif user_input == '3':
           #     self.close_server()
            elif user_input == '4':
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

    def actions(self):
        print('\n\n\t1. Print my active clients\n' +
              '\t2. Print my blocks\n' +
              '\t3. Ask blocks (/getblocks)\n' +
              '\t4. Get block data (/getdata)\n' +
              '\t5. Get users (/addr)\n' +
              #'\t6. Send message (/message)\n' +
             # '\t7. Broadcast users (/addips)\n' +
              '\t8. Add new block\n' +
              '\t9. Broadcast blocks (/addblocks)\n' +
              '\t10. Add transaction (/transaction)\n' +
              '\t0. Go back')
        user_input = input()
        if user_input == '1':
            self.print_active_clients()
        elif user_input == '2':
            print(self.my_blocks())
        elif user_input == '3':
            self.get_blocks_menu()
        elif user_input == '4':
            self.get_block_data()
        elif user_input == '5':
            self.get_users()
    #    elif user_input == '6':
     #       self.messaging_selection()
     #   elif user_input == '7':
     #       self.broadcast_users()
        elif user_input == '8':
            data = self.clients[0].validate_msg()
            self.add_new_block(data)
        elif user_input == '9':
            self.broadcast_blocks()
        elif user_input == '10':
            self.add_transaction()
        elif user_input == '0':
            self.menu()
        else:
            print("Please, select a valid option")
            self.actions()

    def messaging_selection(self):
        """CLI menu for selecting if sending a message to all or only to a
        specific user."""
        print('\n\n\t\t1. Send message to specific user\n' +
              '\t\t2. Send message to all\n' +
              '\t\t0. Go back')
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
        print("\t\t\tSelect user number to message:")
        self.print_active_clients(self.active_clients_list())
        print("\t\t\t0. Go back")
        user_input = input()
        user_input = int(user_input)-1
        if user_input == -1:
            self.messaging_selection()
        elif 0 <= user_input < len(self.clients):
            print("            " + str(self.clients[user_input]))
            msg = self.clients[user_input].validate_msg()
            data = self.clients[user_input].send_message(
                msg, method=self.method)
            if data.ok:
                print('Properly sent.')
            else:
                print('Didn\'t get ok reponse from server')
        else:
            print("Please, type a valid option")
            self.specific_user_messaging()

    def request_type(self):
        print('\n\n   1. Set POST as used method\n' +
              '   2. Set GET as used method\n' +
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
            print("Something went wrong!")
            self.request_type()

    def send_to_all(self):
        msg = self.clients[0].validate_msg()
        counter = 0
        for client in self.clients:
            data = client.send_message(msg, method=self.method)
            if data.ok:
                counter += 1
        print('Message succesfully send to {} servers'.format(counter))

    def print_active_clients(self):
        self.pritn_list_3d_level(self.active_clients_list())

    def pritn_list_3d_level(self, l):
        for i in range(len(l)):
            print("\t\t\t" + str(i + 1) + '. ' + str(l[i]))

    def my_blocks(self):
        bf = open(self.blocks_path, mode='r')
        data = bf.read()
        bf.close()
        return data

    def my_blocks_list(self):
        return self.my_blocks().split('\n')[:-1]

    def get_last_block_hash(self):
        blocks = self.my_blocks()
        if blocks != '':
            return self.my_blocks_list()[-1]
        else:
            return ''

    def get_last_block(self):
        try:
            with open(self.path + self.get_last_block_hash() + '.block') as lb:
                return lb.read()
        except:
            print('There is no block file or no block at all')
            return ''

    def add_new_block(self, data, bhash='', broadcast=True):
        if bhash == '':
            h = hashlib.sha256()
            h.update((self.get_last_block() + data).encode('utf-8'))
            hash_block = h.hexdigest()
        else:
            hash_block = bhash
        with open(self.blocks_path, 'a+') as bf:
            bf.write(hash_block + '\n')
        with open(self.path + hash_block + '.block', 'w+') as hb:
            hb.write(data)
        if broadcast:
            self.broadcast_blocks()

    def get_blocks_menu(self):
        print('\n\n\t\t1. From last block and ahead\n' +
              '\t\t2. Get all\n' +
              '\t\t0. Go back')
        user_input = input()
        if user_input == '1':
            self.get_blocks(from_last=True)
        elif user_input == '2':
            self.get_blocks()
        elif user_input == '0':
            self.actions()
        else:
            print("Please, select a valid option")
            self.get_blocks_menu()

    def get_blocks(self, from_last=False):
        url = '/getblocks'
        if from_last:
            last_block = self.get_last_block_hash()
            if last_block != '':
                url += '/' + last_block
        total_blocks = ''
        all_last = []
        for client in self.active_clients_list():
            data = client.send_message('', path=url, method='GET')
            self.add_blocks(data.text)
            total_blocks += data.text
            all_last.append(list(filter(lambda x: x != '' and x != None, (data.text).split('\n')))[-1])
        print('All blocks received:\n{}'.format(total_blocks))
        return all_last

    def get_block_data(self):
        print('Select block to get data:')
        bl = self.my_blocks_list()
        self.pritn_list_3d_level(bl)
        try:
            user_input = int(input())
            if user_input < 1 or user_input > len(bl):
                raise ValueError
        except:
            print('Please choose a valid number')
            self.get_block_data()
        bh = bl[user_input - 1]
        try:
            with open(self.path + bh + '.block', 'r') as bd:
                print(bd.read())
        except:
            url = '/getdata/' + bh
            data = []
            for client in self.active_clients_list():
                data.append((client.send_message(
                    '', path=url, method='GET')).text)
            with open(self.path + bh + '.block', 'w+') as bd:
                for d in data:
                    if d != '':
                        bd.write(d)
                        print(d)
                        # We assume all are the same so once we get data that's it
                        break

    def get_users(self):
        url = '/addr'
        for client in self.active_clients_list():
            self.parse_new_ips(
                (client.send_message('', path=url, method='GET')).text)

    def broadcast_users(self):
        to_send = self.active_clients_list_repr()
        to_send += '\n' + self.ip
        active_clients = self.active_clients_list()
        if active_clients != []:
            for client in active_clients:
                client.send_message(to_send, path='/addips', method='POST')

    def broadcast_blocks(self):
        to_send = self.my_blocks()
        active_clients = self.active_clients_list()
        if active_clients != []:
            for client in active_clients:
                client.send_message(to_send, path='/addblocks', method='POST')

    def parse_client_request(self, url,  data):
        if url == '/getblocks':
            print('Received /getblocks request. Answering...')
            body = self.my_blocks()
        elif '/getblocks' in url:
            block_hash = url.split('/')[1]
            blocks = self.my_blocks()
            if block_hash in blocks:
                try:
                    body = blocks[blocks.split('\n').index(block_hash):]
                except:
                    body = ''
            print('Received /getblocks request. Answering...')
        elif url == '/addips':
            self.parse_new_ips(data)
            body = 'Added ip address: {}'.format(data)
        elif url == '/addblocks':
            self.add_blocks(data)
            body = 'Received blocks: {}'.format(data)
        elif url == '/addr':
            print('Received /addr request. Answering...')
            body = self.active_clients_list_repr()
        elif url == '/transaction':
            self.add_new_transaction(data)
            body = 'Added transaction: {}'.format(data)
        elif '/getdata' in url:
            block_hash = url.split('/')[-1]
            try:
                with open(self.path + block_hash + '.block', 'r') as bd:
                    body = bd.read()
            except:
                body = ''
        else:
            print('\rFrom connected user: {}\n->'.format(data), end='')
            body = 'Received {} bytes properly'.format(len(data))
        return body

    def active_clients_list(self):
        result = []
        for client in self.clients:
            if client.is_active():
                result.append(client)
        return result

    def active_clients_list_repr(self):
        return '\n'.join(list(map(lambda x: repr(x), self.active_clients_list())))

    def check_file_exists(self, path):
        if not os.path.exists(path):
            open(path, 'a').close()
            return False
        return True

    def parse_new_ips(self, data):
        try:
            new_ips = ''
            for ip in data.split('\n'):
                if ip not in self.clients_list and ip != self.ip:
                    self.iphandler.add_ip(ip)
                    self.clients_list.append(ip)
                    current_ip, current_port = ip.split(':')
                    self.clients.append(
                        Client(ip=current_ip, port=int(current_port), name=self.name + 'Client' + str(self.last_client_index)))
                    self.last_client_index += 1
                    new_ips += '{}\t'.format(ip)
            if new_ips != '':
                print('New added: \n')
                print(new_ips)
                self.start_clients()
                threading.Thread(target=self.delayed_broadcasts).start()
        except:
            print(sys.exc_info()[0])
    
    def add_transaction(self):
        to = input('Send to: ')
        sum = input('Sum to send: ')
        try:
            to_send = self.transaction.create_transaction(self.name, to, float(sum))
            active_clients = self.active_clients_list()
            if active_clients != []:
                for client in active_clients:
                    client.send_message(to_send, path='/transaction', method='POST')
            self.add_new_transaction(to_send)
        except:
            print('Incorrect transaction inputs')
    
    def add_blocks(self, blocks):
        my_blocks = self.my_blocks()
        try:
            with open(self.blocks_path, 'a+') as bf:
                for block in blocks.split('\n'):
                    if block not in my_blocks:
                        bf.write(block + '\n')
        except:
            print('While trying to add blocks:\n{}'.format(sys.exc_info()[0]))

    def add_new_transaction(self, new_t):
        try:
            new_t = json.loads(new_t)
            with open(self.transactions_path, 'r') as tr_f:
                transactions = json.load(tr_f)
                found = False
                for e in transactions:
                    if e == new_t:
                        tr_f.close()
                        return False
                transactions.append(new_t)
                tr_f.close()
            with open(self.transactions_path, 'w') as tr_f:
                to_write = json.dumps(transactions)
                tr_f.write(to_write)
                tr_f.close()
        except:
            traceback.print_exc()
            print('Some error happened while adding a transaction')

    def kaevandamine(self, already=0):
        MAX_TRY = 3
        try:
            if already+1 >= MAX_TRY:
                return False
            success = False
            with open(self.transactions_path, 'r') as tr_f:
                transactions = json.loads(tr_f.read())
                merkle = MerklePuu()
                bloki_merkle_hash = merkle.ehita_nimekirjast(transactions)
                print(bloki_merkle_hash)
                new_hash = kaeva_naivselt(
                    bloki_merkle_hash, self.get_last_block_hash(), n=MAX_ZEROS, t=MAX_MINE_S)
                self.add_new_block(json.dumps(transactions), bhash=new_hash, broadcast=False)
                tr_f.close()
                success = True
            if success:
                with open(self.transactions_path, 'w') as tr_f:
                    tr_f.write('[]')
                    tr_f.close()
        except AssertionError:
            print('Cannot mine empty transactions list')
        except:
            traceback.print_exc()
            print('Could not mine')
            sleep(0.5)
            self.kaevandamine(already=(already+1))

    def kaevandamine_thread(self, t=DEFAULT_MINE):
        sleep(60*t)
        while self.is_open():
            praegu = datetime.now()
            if praegu != self.last_mine and (praegu.minute-self.last_mine.minute == t):
                print('Kaevandamine')
                self.kaevandamas = True
                self.kaevandamine()
                self.last_mine = praegu
                self.kaevandamas = False
                sleep(5)
                self.checkmining()
    
    def checkmining(self):
        last_mined_hashes = self.get_blocks()
        counters = list(map(lambda x: last_mined_hashes.count(x), last_mined_hashes))
        most_repeated_hash = last_mined_hashes[counters.index(max(counters))]
        if self.get_last_block_hash() != most_repeated_hash:
            print('Syncronazing my last block hash. Found missmatch')
            print('My last hash: {}'.format(self.get_last_block_hash()))
            print('Majority last hash: {}'.format(most_repeated_hash))

if __name__ == '__main__':
    server_port, name = int(argv[1]), argv[2]
    user = User(port=server_port, name=name)