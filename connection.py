#!/usr/bin/env python3

import telnetlib
from netmiko import ConnectHandler



class Telnet_Conn():

    def __init__(self, devobj):
        self.host = "192.168.10.126"
        self.port = devobj.console_port
        self.username = 
        pass
    host = "192.168.10.126"
    port = "5014"
    username = "cisco"
    password = "cisco"




def main():
    pass

if __name__ == "__main__":
    main()