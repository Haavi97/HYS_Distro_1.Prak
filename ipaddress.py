"""IP address script.
>Module that handles ip addresses, adding, deleting...
"""
import os
import sys
import itertools as it
from log_helpers import print_wl_error, print_wl

dirname = 'data'
default_path = os.getcwd() + os.sep + dirname + os.sep + 'ipaddresses.txt'


class IPHandler(object):
    r"""Documentation to IPHandler.

    This class handles ip address storing and retrieving them
    from a txt file.

    Parameters
    ----------
    file : str
        (optional argument)
        Text (.txt) file full path where the ip address must be stored.
    """

    def __init__(self, file=default_path, with_port=True):
        """Init function."""
        self.file = file

    def set_path(self, path):
        """Sets the path to the file."""
        self.file = path

    def create_ipa_file(self):
        """Creates an empty file for storing ip addresses.

        If there is already an existing file then it just leaves it as
        it is. It does not erase the content already existing. For that
        is the erase file.
        """
        try:
            if os.path.exists(self.file):
                print_wl('File already exists')
            else:
                if dirname not in os.listdir():
                    os.mkdir(dirname)
                fd = open(self.file, 'x')
                fd.close()
                print_wl('Succeed creating ipa_file')
        except:
            print_wl_error('Some error ocurred trying to create ipa_file')

    def erase_ipa_file(self):
        """Function for erasing the file  storing ip addresses."""
        try:
            os.remove(self.file)
            print_wl('Succeed removing ipa_file')
        except FileNotFoundError:
            print_wl_error('Error trying to erase non existing file')

    def add_ip(self, ip_address, with_port=True):
        """Adds ip address to the given file.

        Parameters
        ----------
        ip_address : str
            string containing a valid ip address

        with_port : bool
            boolean specifying if the ip address must include
            port number to be valid or not
        """
        if self.valid_ipv4(ip_address, with_port=with_port):
            if not self.ip_is_in_file(ip_address):
                try:
                    with open(self.file, 'a') as fd:
                        fd.write(ip_address + '\n')
                        print_wl(
                            'Ip address {} succesfully added'.format(ip_address))
                except FileNotFoundError:
                    self.create_ipa_file()
                    with open(self.file, 'a') as fd:
                        fd.write(ip_address)
                    os.close(fd)
            else:
                print_wl('Ip address already in file')
        else:
            print_wl_error(
                'Failed to add invalid ip address {}'.format(ip_address))

    def remove_ip(self, ip_address):
        """Removes ip address to the given file.

        Parameters
        ----------
        ip_address : str
            string containing a valid ip address
        """
        if self.valid_ipv4(ip_address):
            try:
                with open(self.file, 'r+') as fd:
                    lines = fd.readlines()
                    fd.seek(0)
                    for line in lines:
                        if line.strip('\n') != ip_address:
                            fd.write(line)
                        else:
                            print_wl(
                                'Ip address {} removal succeed'.format(ip_address))
                    fd.truncate()
            except FileNotFoundError:
                print_wl_error('Trying to remove ipa but no file found')
        else:
            print_wl_error(
                'Failed to remove invalid ip address {}'.format(ip_address))

    def ip_is_in_file(self, ip_address):
        """Looks up an ip address in the given file.

        Parameters
        ----------
        ip_address : str
            string containing a valid ip_address

        Returns
        -------
        is_in : bool
            True if the ip address is in the given file.
            False otherwise
        """
        try:
            with open(self.file, "r") as fd:
                lines = fd.readlines()
                for line in lines:
                    if ip_address == line.strip("\n"):
                        fd.close()
                        print_wl('Ip address {} found.'.format(ip_address))
                        return True
                print_wl('Ip address {} not found'.format(ip_address))
            return False
        except FileNotFoundError:
            print_wl_error('Searching ipa but no file found')

    def valid_ipv4(self, ip_address, with_port=True):
        """Looks up an ip address in the given file.

        Parameters
        ----------
        ip_address : str
            string to be check

        with_port : bool
            boolean specifying if the ip address must include
            port number to be valid or not

        Returns
        -------
        valid : bool
            True if the ip address is valid (4 numbers
            separated by . between 0-255 and integer after colon
            in case of with_port being true).
            False otherwise
        """
        try:
            numbers = ip_address.strip('\n').split('.')
            if with_port:
                numbers[-1], port = numbers[-1].split(':')
                if int(port) < 1:
                    return False
            numbers = filter(lambda x: 0 <= int(x) < 256, numbers)
            return len(list(numbers)) == 4
        except ValueError:
            return False

    def get_ip_listdef(self):
        """Gets the list of all the ip address in the file.

        Returns
        -------
        ips : list
            a list containing all ip addresses (str)
        """
        try:
            with open(self.file, "r") as fd:
                ips = fd.read().split('\n')[:-1]
            return ips
        except FileNotFoundError:
            print_wl_error('Could not get ip list from non existing file')

    def add_ip_list(self, ip_list):
        """Adds list of ip address to the given file.

        Parameters
        ----------
        ip_list : str list
            list containing valid ip addresses

        with_port : bool
            boolean specifying if the ip address must include port
            number to be valid or not
        """
        for ip in ip_list:
            self.add_ip(ip)
