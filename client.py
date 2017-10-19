#!/usr/bin/env python3
import os, sys
import socket
from colours import Colours
from threading import Thread
import time
import subprocess

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

            #send hostname to client
            mac, name = self.get_mac(), socket.gethostname()
            self.c_sock.send("('{}','{}')".format(name, mac).encode())

            self.alive_count = 0
            self.server_alive = True

            alive = Thread(target=self.alive_timer, daemon=True)
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
            if not self.server_alive: print("{}[*] {}Unexpectedly disconnected from server".format(Colours.blue, Colours.white))
            else: print("{}[-]{} The folling error occured: {}".format(Colours.red, Colours.white, err))
        except KeyboardInterrupt:
            pass
        finally:
            if created:
                self.c_sock.close()
                print("{}[*]{} Client closed".format(Colours.red, Colours.white))

    def alive_timer(self):
        while True:
            prev = self.alive_count
            time.sleep(5)
            if prev == self.alive_count:
                self.server_alive = False
                self.c_sock.close()

    def execute_command(self, cmd):
        pass

    ''' Returns MAC Address of client machine with '''
    def get_mac(self):
        cur_ip = self.c_sock.getsockname()[0]

        if cur_ip == "127.0.0.1" or cur_ip == "": return "N/A"

        interfaces = subprocess.getoutput("ifconfig").split("\n\n")
        cur_int = ""

        for i in interfaces:
            if cur_ip in i:
                cur_int = [x for x in i.split(" ") if x]
                break

        mac = "N/A" if not cur_int else cur_int[4]
        return mac

if __name__ == '__main__':
    Client()
