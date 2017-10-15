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
#TODO: write class for printing colour instead of passing colours as args to format

class Server:
    clients = {}

    #a dict of all commands to be sent to clients
    #{"client_id": (cmd_id, cmd)}
    command_queue = {}
    command_results = {}

    sock = ""
    addr = ""

    #code sent to clients to end connection
    # kill_code = getrandbits(32)

    BUFF_SIZE = 1024

    def __init__(self):
        try:
            sock_created = False
            Server.addr = (input("IP Address: "), int(input("Port Number: ")))

            #create server socket and binds to address
            Server.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Server.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            Server.sock.bind(Server.addr)
            Server.sock.listen(5)

            sock_created = True

            #start client listener
            # listen = Thread(target=ClientHandler, daemon=False)
            # listen.start()
            ClientHandler()

        except ValueError:
            print("{}[x] Server Error: Invalid address{}".format(Colours.red, Colours.white))
        except PermissionError:
            print("{}[x] Server Error: Don't have permisson to bind server to address{}".format(Colours.red, Colours.white))
        except socket.error as err:
            print("{}[x]{} The folling error occured: {}".format(Colours.red, Colours.white, err))
        except KeyboardInterrupt:
            pass
        finally:
            #closed server socket if socket has been created
            if sock_created:
                Server.sock.close()
                print("\n{}[*] {}Server closed".format(Colours.blue, Colours.white))

    ''' Listens for clients connecting to the server and passes them off to the client handler method '''
    def client_listner(self):
        while True:
            c_sock, c_addr = self.sock.listen()
            ID = getrandbits(32)

            #on the very very small off chance that an ID occurs twice
            while ID in Server.clients: ID = getrandbits(32)

            Server.client[ID] = {"sock": c_sock, "addr": c_addr}
            Server.command_queue[ID] = []
            new_client = Thread(target=Client, args=[ID], daemon=True)

''' Listens for new clients, recieves and sends messages from clients '''
class ClientHandler(Server):
    def __init__(self):
        #listens for clients
        while True:
            print("{}\n[+]{} Server listening for clients at: {}".format(Colours.green, Colours.white, Server.addr))
            c_sock, c_addr = Server.sock.accept()

            try:
                #recv client info - hostname, ip, addr as tuple
                #c_info = eval(c_sock.recv(Server.BUFF_SIZE).decode())
                c_ip, c_port = c_sock.getpeername()
                c_name = c_sock.gethostname()
                print(c_ip, c_port, c_name)

            except Exception as err:
                print("{}[-]{} Error occured while recieving client information: {}{}".format(Colours.red, Colours.white, Colours.blue, Colours.white, err))

            self.c_id = getrandbits(32)

            #for the very small chance of a repeat id
            while self.c_id in Server.clients: self.c_id = getrandbits(32)

            #{"client": (hostname, ip_addr, port)}
            Server.clients[self.c_id] = ()

            #recieve messages

            #send messages

    def recieve(self):
        pass

    def send(self):
        while True:
            if command_queue[self.client_id]:
                pass


if __name__ == '__main__':
    Server()
