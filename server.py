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

    #TODO: sperate into a sperate client sub-class!!!!!!!!

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

            c_id = getrandbits(32)

            #for the very small chance of a repeat id
            while c_id in Server.clients: c_id = getrandbits(32)

            #last item in tuple indicates if client is alive
            Server.clients[c_id] = [c_sock, c_ip, c_port, c_name, True]
            Server.command_queue[c_id] = {}

            print("{}[+]{} Client connected with: ID {}, IP {}, Port {}, Hostname {}".format(Colours.green, Colours.white, c_id, c_ip, c_port, c_name))

            #recieve messages

            #NOTE: have alive thread sperate or mixed in with recieve or send thread?
            #alive thread - check client alive every 5 seconds
            alive = Thread(target=self.is_alive, args=[c_id], daemon=True)
            alive.start()

            #send messages
            self.send(c_id)

    def recieve(self, c_id):
        pass

    def send(self, c_id):
        while Server.clients[c_id][-1]:
            if Server.command_queue[c_id]:
                pass
            time.sleep(100)

    def is_alive(self, c_id):
        try:
            while Server.clients[c_id][-1]:
                Server.clients[c_id][0].send("\0".encode())
                time.sleep(5)

        except socket.error:
            #client closed connection
            self.client_remove(c_id)

    def client_remove(self, c_id):
        Server.clients[c_id][-1] = False

        #enough time for other threads to start a new loop and see client isnt alive
        time.sleep(12)

        del Server.clients[c_id]
        del Server.command_queue[c_id]

        print("{}[-]{} Client {} disconnected".format(Colours.red, Colours.white, c_id))

'Instance of a client'
class Client(ClientHandler):
    def __init__(self, c_id):
        self.c_id = c_id

    def send(self):
        pass

    def recieve(self):
        pass

    def alive(self):
        pass

    def disconnected(self):
        pass

if __name__ == '__main__':
    Server()
