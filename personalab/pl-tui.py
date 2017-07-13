#from ansible.module_utils import cloud

import conn
import sys
import getpass
import npyscreen


def main():

    #password = raw_input("enter password: ")
    password = getpass.getpass('enter password: ')
    cloud = conn.PersonaLab(password=password)

    form = npyscreen.Form( name = 'personal lab')
    form.edit()


    return


if __name__ == '__main__':
    main()
    sys.exit(0)
