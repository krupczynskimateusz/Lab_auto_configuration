#!/usr/bin/env python3

from telnetlib import Telnet
from netmiko import ConnectHandler
from time import sleep
from commands import Command


class Telnet_Conn():

    gns_server_ip = "192.168.10.126"

    def __init__(self, devobj):
        self.host = Telnet_Conn.gns_server_ip
        self.port = devobj.console_port
        self.username = devobj.username
        self.password = devobj.password
    
    def connect(self):
        self.tc = Telnet(
            host = self.host,
            port = str(self.port)
            )

    def authenticate(self, output):
        if "User" in output or "user" in output:
            self.tc.write(self.username.encode(), b"\n")
            sleep(1)
            self.tc.write(self.password.encode(), b"\n")
        else:
            pass
    
    def close(self):
        self.tc.close()
    
    def send(self, command, timeout = 0.5):
        self.connect()
        self.tc.write(command)
        sleep(timeout)
    
    def send_lst(self, command_lst, timeout = 0.5):
        self.connect()
        for command in command_lst:
            command = command + "\n"
            self.tc.write(command.encode())
            sleep(timeout)
        self.close()



def basic_config(dev):
    tc = Telnet_Conn(dev)
    tc.connect()
    command_lst = Command(dev.vendor)
    tc.send_lst(command_lst)


def main():
    pass

if __name__ == "__main__":
    main()