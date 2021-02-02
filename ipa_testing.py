import sys

from ipaddress import create_ipa_file, erase_ipa_file
from ipaddress import add_ip, remove_ip, ip_is_in_file
from ipaddress import valid_ipv4, default_path
from ipaddress import get_ip_listdef, add_ip_list
from log_helpers import print_wl_error, print_wl


def display_menu():
    print('*********')
    print('MAIN MENU')
    print('*********')
    print('01. Create default ipa file')
    print('02. Erase default ipa file')
    print('03. Add ip')
    print('04. Remove ip')
    print('05. Check if ip is in file')
    print('06. Check ipv4 validity')
    print('07. Get ip list')
    print('08. Add ip list')
    print('09. Change file name')
    print('10. Set default file name')
    print('11. Set valid to be ipv4 without' +
          ' port number')
    print('**. q, exit, 0\n\n')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '-with-port':
            with_port = True
    fn = default_path
    wp = True
    while True:
        try:
            display_menu()
            inp = input()
            if inp in ['q', 'exit', '0']:
                break
            elif inp == '1':
                create_ipa_file(file=fn)
            elif inp == '2':
                erase_ipa_file(file=fn)
            elif inp == '3':
                add_ip(input('Input ipv4 address: '),
                       file=fn, with_port=wp)
            elif inp == '4':
                remove_ip(input('Input ipv4 address to remove: '),
                          file=fn)
            elif inp == '5':
                ip_is_in_file(input('Input ipv4 address: '),
                              file=fn)
            elif inp == '6':
                valid_ipv4(input('Input ipv4 address: '),
                           with_port=wp)
            elif inp == '7':
                print(get_ip_listdef(file=fn))
            elif inp == '8':
                ip_in = input('Type ip addresses list:')
                ip_eval = eval(ip_in)
                add_ip_list(ip_eval)
            elif inp == '9':
                fn = input('Input file name (full path): ')
            elif inp == '10':
                fn = default_path
            elif inp == '11':
                wp = False
            else:
                print("Please, choose a valid number")
        except:
            e = sys.exc_info()[0]
            print_wl_error("An error ocurred.")
            print_wl_error("Exception message: {}".format(e))
