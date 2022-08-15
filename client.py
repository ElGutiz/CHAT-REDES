from getpass import getpass
from argparse import ArgumentParser
import slixmpp
import sys
import asyncio
from slixmpp.exceptions import IqError, IqTimeout
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
        for group in groups:
            print('\033[1;31;40m')
            print('\n%s' % group)
            print('-' * 50 + 'USERS LIST' + '-' * 50)
            for jid in groups[group]:
                name = self.client_roster[jid]['name']
                if self.client_roster[jid]['name']:
                    print(' %s (%s)' % (name, jid))
                else:
                    print('\n',jid)

                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    print('   - %s (%s)' % (res, show))
                    if pres['status']:
                        print('       %s' % pres['status'])
                        print('-' * 72)
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
