import threading
from sys import argv

from server import server_only
from client import client_only


if __name__ == '__main__':

     server_port, client_port = int(argv[1]), int(argv[2])
     server = threading.Thread(target=server_only, args=('127.0.0.1',server_port,'With_Threads'))
     client = threading.Thread(target=client_only, args=('127.0.0.1',client_port,'With_Threads'))

     server.start()
     client.start()