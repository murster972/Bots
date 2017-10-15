#!/usr/bin/env python3
import os, sys
import socket
from colours import Colours

#TODO: Setup basic of client, e.g. have it connecting to server and listenging for messages from server

class Client:
    def __init__(self):
        try:
            created = False

            server_addr = (input("Server IP: "), int(input("Server Port: ")))

            self.c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.c_sock.connect(server_addr)

            created = True

            print("{}[+]{} Client connected to server".format(Colours.green, Colours.white))

            print(self.c_sock.getsockname())
            sys.exit()

            #NOTE: split __init__ up into small methods?

            kill_code = self.c_sock.recv(1024).decode()

            #send server client ip, hostname and port
            info = ()

            #listen for cmds from server
            while True:
                cmd = self.c_sock.recv(1024).decode()


        except ValueError:
            print("{}[-] {}Invalid server address".format(Colours.red, Colours.white))
            sys.exit(-1)
        except ConnectionRefusedError:
            print("{}[-] {}Unable to connect to server".format(Colours.red, Colours.white))
        except socket.error as err:
            print("{}[-]{} The folling error occured: {}".format(Colours.red, Colours.white, err))
        except KeyboardInterrupt:
            pass
        finally:
            if created:
                self.c_sock.close()
                print("{}[*]{} Client closed".format(Colours.red, Colours.white))

if __name__ == '__main__':
    Client()
