import os
from sys import argv
from time import sleep


class Ini:

  def __init__(self):
    self.path = os.getcwd() + os.sep
    self.file_path = self.path + 'users' + os.sep + 'conf.txt'
    self.read_ips(self.file_path)
  
  def read_ips(self, path):
    with open(path) as fh:
      fstring = fh.readlines()
    
    ports = []
    for line in fstring:
      ip = line.strip().split(':')
      ports.append(ip[1])
    
    self.create_terminals(ports)
  
  def create_terminals(self, ports):
    
    path_parent = os. path. dirname(os. getcwd())
    os.chdir(path_parent+ os.sep + 'MainNode' + os.sep)
    command = 'python MainNode.py'
    print(command)
    os.system("start cmd /k " + command)
    os.chdir(self.path)
    sleep(3)
    for port in  range(len(ports)):
      command = 'python user.py ' + str(ports[port]) +  ' user' + str(port + 1)
      os.system("start cmd /k " + command)
      sleep(1)

if __name__ == '__main__':
  ini = Ini()