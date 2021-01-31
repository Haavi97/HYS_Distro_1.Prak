from ipaddress import create_ipa_file, erase_ipa_file
from ipaddress import add_ip, remove_ip, ip_is_in_file
from ipaddress import valid_ipv4


if __name__ == '__main__':
    erase_ipa_file()
    create_ipa_file()
    add_ip('192.168.1.1')
    add_ip('192.168.1.1')
    add_ip('192.168.1.2')
    add_ip('192.168.1.3')
    remove_ip('192.168.1.1')
    ip_is_in_file('192.168.1.1')
    add_ip('192.168.1.4')
    add_ip('192.168.1.1')
    ip_is_in_file('192.168.1.3')
    create_ipa_file()
    print(valid_ipv4('192.168.1.3'))
    print(valid_ipv4('192.168.1.3.1'))
    print(valid_ipv4('192.'))
    print(valid_ipv4('asdf'))
    print(valid_ipv4('192.168.a.3'))
    