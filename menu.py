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

    print('\n 1) Show Users List')
    print('\n 2) Show User Information')
    print('\n 3) Add User as Friend')
    print('\n 4) Send Private Message ')
    print('\n 5) Define Presence Message ')
    print('\n 6) Delete Account ')
    print('\n 7) Send Group Message ')
    print('\n 8) Send File ')
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
        username = input("Username: ")
        password = input("Password: ")
        email = input("Mail: ")
        xmpp = Register_Account(username, password, email)
        xmpp.connect()
        xmpp.process()
    elif(option1 == 2):
        username = 'Corado@alumchat.fun'
        password = 'Diciembre22'
        exit2 = True
        while(exit2):
            second_menu()
            option2 = int(input("Write your option number: "))

            if(option2 == 1):
                xmpp = Show_Users(username, password)
                xmpp.connect()
                xmpp.process(forever=False)
            
            elif(option2 == 2):
                friend = input("Name of contact you want to get information: ")
                xmpp = Show_User(username, password, friend)
                xmpp.connect()
                xmpp.process(forever=False)
            
            elif(option2 == 3):
                friend = input("Name of contact you want to add: ")
                xmpp = Add_User(username, password, friend)
                xmpp.connect()
                xmpp.process(forever=False)
            
            elif(option2 == 4):
                friend = input("Name of contact you want to send the message: ")
                message = input("Message: ")
                xmpp = Send_Private_Message(username, password, friend, message)
                xmpp.connect()
                xmpp.process(forever=False)
            
            elif(option2 == 5):
                information = input("Information you want to add to your status: ")
                status = input("Status: ")
                xmpp = Change_Presence(username, password, information, status)
                xmpp.connect()
                xmpp.process(forever=False)
            
            elif(option2 == 6):
                xmpp = Delete_Account(username, password)
                xmpp.connect()
                xmpp.process(forever=False)
                exit2 = False
            
            elif(option2 == 7):
                try:
                    nickname = 'corados'
                    room = "python.es@conference.alumchat.fun"
                    xmpp = Send_Group_Message(username, password, room, nickname)
                    xmpp.register_plugin('xep_0030')
                    xmpp.register_plugin('xep_0045')
                    xmpp.register_plugin('xep_0199')
                    xmpp.connect()
                    xmpp.process(forever=False)
                except KeyboardInterrupt as e:
                    print('Group Chat Finished')
                    xmpp.disconnect()

            elif(option2 == 8):
                friend = "javierbot@alumchat.fun"

                with open(r"C:\Users\Joseph\Desktop\Njsccc.txt",'rb') as img:
                    file_ = base64.b64encode(img.read()).decode('utf-8')

                xmpp = Send_File(username, password, friend, file_)
                xmpp.connect()
                xmpp.process(forever=False)

            elif(option2 == 9):
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