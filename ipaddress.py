import os
import sys
from log_helpers import print_wl_error, print_wl

dirname = 'data'
default_path = os.getcwd() + os.sep + dirname + os.sep + 'ipadresses.txt'


def create_ipa_file(file=default_path):
    try:
        if dirname not in os.listdir():
            os.mkdir(dirname)
        # TODO! Check first if file already exists
        fd = open(file, 'x')
        fd.close()
        print_wl('Succeed creating ipa_file')
    except:
        print_wl_error('Some error ocurred trying to create ipa_file')


def erase_ipa_file(file=default_path):
    try:
        os.remove(file)
        print_wl('Succeed removing ipa_file')
    except FileNotFoundError:
        print_wl_error('Error trying to erase non existing file')


def add_ip(ip_address, file=default_path):
    if not ip_is_in_file(ip_address):
        try:
            with open(default_path, 'a') as fd:
                fd.write(ip_address + '\n')
                print_wl(
                        'Ip address {} succesfully added'.format(ip_address))
        except FileNotFoundError:
            create_ipa_file()
            with open(default_path, 'a') as fd:
                fd.write(ip_address)
            os.close(fd)
    else:
        print_wl('Ip address already in file')


def remove_ip(ip_address, file=default_path):
    try:
        with open(default_path, 'r+') as fd:
            lines = fd.readlines()
            fd.seek(0)
            for line in lines:
                if line.strip('\n') != ip_address:
                    fd.write(line)
                else:
                    print_wl(
                        'Ip address {} succesfully removed'.format(ip_address))
            fd.truncate()
    except FileNotFoundError:
        print_wl_error('Trying to remove ipa but no file found')


def ip_is_in_file(ip_address, file=default_path):
    try:
        with open(default_path, "r") as fd:
            lines = fd.readlines()
            for line in lines:
                if ip_address == line.strip("\n"):
                    fd.close()
                    return True
            print_wl('Ip address {} not found'.format(ip_address))
        return False
    except FileNotFoundError:
        print_wl_error('Searching ipa but no file found')


# TODO! Check ip address validity
# TODO! Add verbosity to messages
