from argparse import ArgumentParser
import slixmpp
import sys
import asyncio
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET 
import threading

if sys.platform == 'win32' and sys.version_info >= (3, 8):
     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Show_Users(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.presences = threading.Event()

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        try:
            self.get_roster()
        except IqError as e:
            print("Error", e)
        except IqTimeout:
            print("Server Timeout")
        
        self.presences.wait(3)

        groups = self.client_roster.groups()
        print('\033[0;36;40m')
        for group in groups:
            for contact in groups[group]:
                connections = self.client_roster.presence(contact)

                username = 'None'
                status = 'None'
                show = 'None'
                extra = 'None'

                if self.client_roster[contact]['name']:
                    username = self.client_roster[contact]['name']

                for res, pres in connections.items():
                    if pres['show']:
                        show = pres['show']
                    if pres['status']:
                        status = pres['status']
                    
                    extra = res
                
                print("User Mail: ", contact)
                print("Username: ", username)
                print("Status: ", status)
                print("Show: ", show)
                print("Extra: ", extra)
                
                print('\n')
        print('\033[0;37;40m')
        self.disconnect()

class Add_User(slixmpp.ClientXMPP):
    def __init__(self, jid, password, to):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.to = to

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        try:
            self.send_presence_subscription(pto=self.to) 
        except IqTimeout:
            print("Server Timeout") 
        self.disconnect()
    
class Send_Private_Message(slixmpp.ClientXMPP):
     def __init__(self, jid, password, recipient, message):
          slixmpp.ClientXMPP.__init__(self, jid, password)
          self.recipient = recipient
          self.msg = message
          self.add_event_handler("session_start", self.start)

     async def start(self, event):
          self.send_presence()
          await self.get_roster()
          self.send_message(mto=self.recipient,mbody=self.msg,mtype='chat')
          self.disconnect()

class Show_User(slixmpp.ClientXMPP):
    def __init__(self, jid, password, friend):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.presences = threading.Event()
        self.friend = friend

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
    
        try:
            self.get_roster()
        except IqError as e:
            print("Error", e)
        except IqTimeout:
            print("Server Timeout")
        
        self.presences.wait(3)
        response = []

        groups = self.client_roster.groups()
        for group in groups:
            for contact in groups[group]:
                if self.friend == contact:
                    connections = self.client_roster.presence(contact)

                    username = status = show = extra = 'None'

                    if self.client_roster[contact]['name']:
                        username = self.client_roster[contact]['name']

                    for res, pres in connections.items():
                        if pres['show']:
                            show = pres['show']
                        if pres['status']:
                            status = pres['status']
                        
                        extra = res
                    
                    response.append("User Mail: " + contact)
                    response.append("Username: " + username)
                    response.append("Status: " + status)
                    response.append("Show: " + show)
                    response.append("Extra: " + extra)
        
        if len(response) > 0:
            for data in response:
                print('\033[0;36;40m')
                print(data)
        else:
            print('\033[1;31;40m')
            print("The user doesn't exist in your list of contacts")

        print('\033[0;37;40m')
        self.disconnect()

class Change_Presence(slixmpp.ClientXMPP):
    def __init__(self, jid, password, information, status):
          slixmpp.ClientXMPP.__init__(self, jid, password)
          self.information = information
          self.status = status
          self.jid = jid
          self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.send_presence(pstatus="Available")
        await self.get_roster()
        self.disconnect()
    
class Delete_Account(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.user = jid
        self.add_event_handler("session_start", self.start)

    async def start(self, event):  
        self.send_presence()
        await self.get_roster()

        delete = self.Iq()
        delete['type'] = 'set'
        delete['from'] = self.user
        fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        delete.append(fragment)

        try:
            delete.send()
            print('\033[1;31;40m')
            print("Deleted Account")

        except IqError as e:           
            print("Error", e)

        except IqTimeout:
            print("Server Timeout")

        except Exception as e:     
            print(e)  

        self.disconnect()

class Register_Account(slixmpp.ClientXMPP):
    def __init__(self, jid, password, mail):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        
        self.user = jid
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)
    
    def start(self, event):
        self.send_presence()
        self.get_roster()

    def register(self, iq):  
        create = self.Iq()
        create['type'] = 'set'
        fragment = ET.fromstring("<query xmlns='jabber:iq:register'><username>Hekkice</username><password>1213</password><email>cutci7vu@alumchat.fun</email></query>")
        create.append(fragment)
        create.send()
        try:
            #create.send()
            print('\033[1;31;40m')
            print("New Account Created")

        except IqError as e:           
            print("Error", e)

        except IqTimeout:
            print("Server Timeout")

        except Exception as e:     
            print(e)  

        self.disconnect()