#!/usr/bin/env python3

from telnetlib import Telnet
from netmiko import ConnectHandler
from time import sleep


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
    
    def send(self, command, timeout = 0.5):
        self.tc.write(command)
        sleep(timeout)


commands = "Super\n"

def basic_config(dev):
    print(dev.ip_mgmt)
    tc = Telnet(dev)
    tc.write(commands.encode())


def main():
    tc = Telnet(host = "192.168.10.126", port = "5000")
    tc.write(b"\n")
    print(tc.read_until(b"R1"))

if __name__ == "__main__":
    main()