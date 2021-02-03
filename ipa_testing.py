import sys

from ipaddress import IPHandler
from ipaddress import default_path
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

    ip_handler = IPHandler()
    wp = True

    while True:
        try:
            display_menu()
            inp = input()
            if inp in ['q', 'exit', '0']:
                break
            elif inp == '1':
                ip_handler.create_ipa_file()
            elif inp == '2':
                ip_handler.erase_ipa_file()
            elif inp == '3':
                ip_handler.add_ip(input('Input ipv4 address: '), with_port=wp)
            elif inp == '4':
                ip_handler.remove_ip(input('Input ipv4 address to remove: '))
            elif inp == '5':
                ip_handler.ip_is_in_file(input('Input ipv4 address: '))
            elif inp == '6':
                ip_handler.valid_ipv4(input('Input ipv4 address: '),
                                      with_port=wp)
            elif inp == '7':
                print(ip_handler.get_ip_listdef())
            elif inp == '8':
                ip_in = input('Type ip addresses list:')
                ip_eval = eval(ip_in)
                ip_handler.add_ip_list(ip_eval)
            elif inp == '9':
                ip_handler.set_path(input('Input file name (full path): '))
            elif inp == '10':
                ip_handler.set_path(default_path)
            elif inp == '11':
                wp = False
            else:
                print("Please, choose a valid number")
        except:
            e = sys.exc_info()[0]
            print_wl_error("An error ocurred.")
            print_wl_error("Exception message: {}".format(e))
