import logging
from client import *

logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

exit = True

print('\n \033[1;32;40m WELCOME TO XMPP CHAT \n')

while(exit):
    print('\033[1;37;40m')

    print('\n 1) Register')
    print('\n 2) Log In')
    print('\n 3) Log Out and Close \n')
    
    print('\033[0;37;40m')
    opcion = int(input("Write your option number: "))
    if(opcion == 1):
        user = input("Username: ")
        password = input("Password: ")
        xmpp = Client(user+"@alumchat.xyz",password)
        xmpp.register_plugin('xep_0004') # Data forms
        xmpp.register_plugin('xep_0066') # Out-of-band Data
        xmpp.register_plugin('xep_0077')
        xmpp.register_plugin('xep_0085')
        xmpp['xep_0077'].force_registration = True
        xmpp.connect()
        xmpp.process()
    elif(opcion == 2):
        user = input("Username: ")
        password = input("Password: ")
        xmpp = Client(user+"@alumchat.xyz", password)
        xmpp.register_plugin('xep_0030') # Service Discovery
        xmpp.register_plugin('xep_0199') # XMPP Ping
        xmpp.register_plugin('xep_0085')
        xmpp.register_plugin('xep_0363')
        xmpp.connect()
        xmpp.process(forever=False)
    elif(opcion == 3):
        print('Have a good day')
        exit = False
    else:
        print('\033[1;31;40m')
        print('Please choose a validate option')