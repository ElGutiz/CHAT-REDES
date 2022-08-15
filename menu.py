import logging
import sys
import asyncio
from client import *

logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

exit1 = True
exit2 = True

def second_menu():
    print('\n \033[1;32;40m WELCOME!')

    print('\033[1;37;40m')

    print('\n 1) Show User List')
    print('\n 2) Add User as Friend')
    print('\n 3) Send Message \n')
    print('\n !) Log Out \n')

    print('\033[0;37;40m')

if sys.platform == 'win32' and sys.version_info >= (3, 8):
     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

print('\n \033[1;32;40m WELCOME TO XMPP CHAT')

while(exit1):
    print('\033[1;37;40m')

    print('\n 1) Register')
    print('\n 2) Log In')
    print('\n 3) Close \n')
    
    print('\033[0;37;40m')
    option1 = int(input("Write your option number: "))
    if(option1 == 1):
        user = input("Username: ")
        password = input("Password: ")
        #xmpp = Client(user+"@alumchat.fun",password)
        xmpp.register_plugin('xep_0004') # Data forms
        xmpp.register_plugin('xep_0066') # Out-of-band Data
        xmpp.register_plugin('xep_0077')
        xmpp.register_plugin('xep_0085')
        xmpp['xep_0077'].force_registration = True
        xmpp.connect()
        xmpp.process()
    elif(option1 == 2):
        username = input("Username: ")
        password = input("Password: ")
        exit2 = True
        while(exit2):
            second_menu()
            option2 = int(input("Write your option number: "))

            if(option2 == 1):
                xmpp = Show_Users(username, password)
                xmpp.connect()
                xmpp.process(forever=False)
            
            elif(option2 == 2):
                friend = input("Name of contact you want to add: ")
                xmpp = Add_User(username, password, friend)
                xmpp.connect()
                xmpp.process(forever=False)
            
            elif(option2 == 3):
                friend = input("Name of contact you want to send the message: ")
                message = input("Message: ")
                xmpp = Send_Private_Message(username, password, friend, message)
                xmpp.connect()
                xmpp.process(forever=False)
            
            elif(option2 == 4):
                exit2 = False

            else:
                print('\033[1;31;40m')
                print('Please choose a validate option')
    elif(option1 == 3):
        print('Have a good day')
        exit1 = False
    else:
        print('\033[1;31;40m')
        print('Please choose a validate option')