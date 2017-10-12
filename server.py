#!/usr/bin/env python3
from colours import Colours
from threading import Thread
import os, sys
import socket
import time
from random import getrandbits

#TODO: Setup basic of server, e.g. have it listening and connecting to clients
#TODO: do normal connection first, tls later
#TODO: lock up locking variables used between threads

class Server:
    clients = {}

    #a dict of all commands to be sent to clients
    command_queue = {}

    def __init__(self):
        try:
            sock_created = False
            server_addr = (input("IP Address: "), int(input("Port Number: ")))

            #create server socket and binds to address
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_sock.bind(server_addr)

            sock_created = True

            #start client listener
            listen =


        except ValueError:
            print("{}[-] Server Error: Invalid address{}".format(Colours.red, Colours.white))
            sys.exit(-1)
        except PermissionError:
            print("{}[-] Server Error: Don't have permisson to bind server to address{}".format(Colours.red, Colours.white))
            sys.exit(-1)
        except KeyboardInterrupt:
            pass

        #closed server socket if socket has been created
        if sock_created: self.server_sock.close()

        print("\n{}[*] {}Server closed".format(Colours.blue, Colours.white))

    ''' Listens for clients connecting to the server and passes them off to the client handler method '''
    def client_listner(self):
        while True:
            c_sock, c_addr = self.server_sock.listen()
            ID = getrandbits(32)

            #on the very very small off chance that an ID occurs twice
            while ID in Server.clients: ID = getrandbits(32)

            Server.client[ID] = {"sock": c_sock, "addr": c_addr}
            Server.command_queue[ID] = []
            new_client = Thread(target=Client, args=[ID], daemon=True)

''' Instance of a client, sends messages and recives replys from clients etc. '''
class Client(Server):
    def __init__(self, ID):
        self.id = ID
        self.messages = []

        #start thread to recive messages from client
        r = Thread(target=self.recive, daemon=True)
        r.start()

        #check for messages from client and for any commands to send client
        while True:
            if self.messages:
                pass
            if Server.command_queue[ID]:
                pass
            time.sleep(10)

    def recive(self):
        while True:
            pass


if __name__ == '__main__':
    Server()
