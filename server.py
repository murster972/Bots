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

#NOTE: have a single instance of db connecter created before start and then kpass it to both server and server-side for u

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

''' Listens for new clients, recieves and sends messages from clients '''
class ClientHandler(Server):
    def __init__(self):
        print("{}[*]{} Server listening for clients at: {}".format(Colours.blue, Colours.white, Server.addr))

        #listens for clients
        while True:
            c_sock, c_addr = Server.sock.accept()

            try:
                c_ip, c_port = c_sock.getpeername()
                c_name = c_sock.recv(Server.BUFF_SIZE).decode()

            except Exception as err:
                print("{}[-]{} Error occured while getting client information: {}{}".format(Colours.red, Colours.white, Colours.blue, err))
                continue

            self.c_id = getrandbits(32)

            #for the very small chance of a repeat id
            while self.c_id in Server.clients: self.c_id = getrandbits(32)

            Server.clients[self.c_id] = (c_sock, c_ip, c_port, c_name)

            print("{}[+]{} Client connected with: ID {}, IP {}, Port {}, Hostname {}".format(Colours.green, Colours.white, self.c_id, c_ip, c_port, c_name))

            #recieve messages

            #send messages

            #alive thread - check client alive every 5 seconds

            #NOTE: have alive thread sperate or mixed in with recieve or send thread?

    def recieve(self, id):
        pass

    def send(self, id):
        while True:
            if command_queue[self.client_id]:
                pass

if __name__ == '__main__':
    Server()
