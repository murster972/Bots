#!/usr/bin/env python3
import os, sys
import socket
from colours import Colours
from threading import Thread
import time

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

            #NOTE: split __init__ up into small methods?

            print(socket.gethostname())

            #send hostname to client
            self.c_sock.send(socket.gethostname().encode())

            self.alive_count = 0
            self.server_alive = True

            alive = Thread(target=self.alive_timer(), daemon=True)
            alive.start()

            #listen for cmds from server
            while True:
                cmd = self.c_sock.recv(1024).decode()

                #alive check from server
                if cmd == "\0": self.alive_count += 1


        except ValueError:
            print("{}[-] {}Invalid server address".format(Colours.red, Colours.white))
            sys.exit(-1)
        except ConnectionRefusedError:
            print("{}[-] {}Unable to connect to server".format(Colours.red, Colours.white))
        except BrokenPipeError:
            print("{}[*]{} Server closed".format(Colours.blue, Colours.white))
        except socket.error as err:
            print("{}[-]{} The folling error occured: {}".format(Colours.red, Colours.white, err))
        except KeyboardInterrupt:
            pass
        finally:
            if created:
                self.c_sock.close()
                print("{}[*]{} Client closed".format(Colours.red, Colours.white))

    def alive_timer(self):
        while True:
            prev = self.alive_count
            time.sleep(7)
            if prev == self.alive_count: raise BrokenPipeError()


if __name__ == '__main__':
    Client()
