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

#NOTE: no-sql options, e.g. JSON, instead of databases?

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

            self.client_handler()

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

    def client_handler(self):
        print("{}[*]{} Server listening for clients at: {}".format(Colours.blue, Colours.white, Server.addr))

        while True:
            c_sock, c_addr = Server.sock.accept()

            c = Thread(target=Client, args=[c_sock, c_addr], daemon=True)
            c.start()

'Instance of a client'
class Client(Server):
    def __init__(self, sock, ip):
        self.c_id = getrandbits(32)
        self.sock = sock

        #on the very small chance c_id repeats
        while self.c_id in Server.clients: self.c_id = getrandbits(32)

        c_ip, c_port = sock.getpeername()
        c_name = sock.recv(Server.BUFF_SIZE).decode()
        self.c_alive = True

        Server.clients[self.c_id] = [self.sock, c_ip, c_port, c_name, self.c_alive]
        Server.command_queue[self.c_id] = {}

        print("{}[+] {}Client connnected:{} ID {}, IP {}, Port {}, Name {},".format(Colours.green, Colours.blue, Colours.white, self.c_id, c_ip, c_port, c_name))

        send = Thread(target=self.send, daemon=True)
        send.start()

        recv = Thread(target=self.recieve, daemon=True)
        recv.start()

        #is_alive called last and not as seperate thread so client doesnt stop running
        #untill after its infos been removed from server
        self.is_alive()

    def send(self):
        while self.c_alive:
            pass

    def recieve(self):
        pass

    #NOTE: Should server being send to client or client sending to server for keep-alive?
    def is_alive(self):
        try:
            while True:
                self.sock.send("\0".encode())
                time.sleep(5)
        except socket.error:
            self.disconnected()

    def disconnected(self):
        self.c_alive = False

        print("{}[-] {}Client {}{}{} disconnected".format(Colours.red, Colours.white, Colours.blue, self.c_id, Colours.white))

        #enough time for send and recieve threads to have seen clients disconnected
        del Server.clients[self.c_id]
        del Server.command_queue[self.c_id]

if __name__ == '__main__':
    Server()
