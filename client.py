#!/usr/bin/env python3
import os, sys
import socket
from colours import Colours
from threading import Thread
import time
import subprocess
import re

#TODO: Setup basic of client, e.g. have it connecting to server and listenging for messages from server


#NOTE: If unable to connect check firewall rules...

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
        #cur_ip = self.c_sock.getsockname()[0]
        cur_ip = "10.216.71.197"

        if cur_ip == "127.0.0.1" or cur_ip == "": return "N/A"

        interfaces = subprocess.getoutput("ifconfig").split("\n\n")
        cur_int = ""

        for i in interfaces:
            if cur_ip in i:
                cur_int = [x for j in i.split("\n") for x in j.split(" ") if x]
                break

        #primitive regex to check for mac: [A-Fa-f0-9]{2,2}[:][A-Fa-f0-9]{2,2}[:][A-Fa-f0-9]{2,2}[:][A-Fa-f0-9]{2,2}[:][A-Fa-f0-9]{2,2}[:][A-Fa-f0-9]{2,2}$
        #cleaner regex for mac check: ([A-Fa-f0-9]{2,2}[:]){5,5}[A-Fa-f0-9]{2,2}$
        #                             [A-Fa-f0-9]{2,2}[:] - checks for pairs of hex ending in ':'
        #                             (...){5,5} - repeats '[A-Fa-f0-9]{2,2}[:]' 5 times, i.e. onlyy returns a match if 5 hex pairs ending with ':'
        #                             [A-Fa-f0-9]{2,2}$ - find last hex pair at end
        for i in cur_int:
            r = re.search(r'([A-Fa-f0-9]{2,2}[:]){5,5}[A-Fa-f0-9]{2,2}$', i)
            if r: break

        mac = "N/A" if not r else r.group()
        return mac

if __name__ == '__main__':
    Client()
