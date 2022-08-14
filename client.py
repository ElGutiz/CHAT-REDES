from getpass import getpass
from argparse import ArgumentParser
import slixmpp

class Client(slixmpp.ClientXMPP):

    def __init__(self, user, password):
        slixmpp.ClientXMPP.__init__(self, user, password)

        self.user = user
        self.password = password
        
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)