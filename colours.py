#!/usr/bin/env python3

#TODO: create custom print class, which has types of messages
#      makes it cleaner than constantly passing colours as args to print
#      method

class Colours:
    black = "\033[1;30;1m"
    red = "\033[1;31;1m"
    green = "\033[1;32;1m"
    yellow = "\033[1;33;1m"
    blue = "\033[1;34;1m"
    purple = "\033[1;35;1m"
    cyan = "\033[1;36;1m"
    white = "\033[1;37;1m"

    #prints messages in colours based on there type
    msg = {"info": lambda info: print(Colours.blue + "[*] " + Colours.white + info),
           "err": lambda title, err: print(Colours.red + "[!] " + title + Colours.white + err),
           "conn": lambda ID, addr: print(Colours.green + "[+] " + Colours.white + "Client " + Colours.blue + ID + Colours.white + " connected: "  + addr),
           "disconn": lambda ID, addr: print(Colours.red + "[-] " + Colours.white + "Client " + Colours.blue + ID + Colours.white + " disconnected: " + addr),}

if __name__ == "__main__":
    Colours.msg["err"]("An error occured while creating server socket: ", "err")
