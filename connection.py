#!/usr/bin/env python3

from telnetlib import Telnet
from netmiko import ConnectHandler
from time import sleep
from commands import create_config_obj



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


    def first_send(self, timeout = 1):
        self.connect()
        
        ## Don't work. Somehow you need to press enter on remote console.
        self.tc.write(b"\n")

        self.close()


    def send(self, command, timeout = 0.5):
        self.connect()

        command = command + "\n"
        self.tc.write(command.encode())
        sleep(timeout)

        self.close()


    def send_lst(self, commands_lst, timeout = 0.5):
        self.connect()

        for cmd in commands_lst:
            if isinstance(cmd, list):
                command = cmd[0] + "\n"
                self.tc.write(command.encode())
                sleep(cmd[1])
            else:
                cmd = cmd + "\n"
                self.tc.write(cmd.encode())
                sleep(timeout)

        self.close()


    def show_all(self):
        return self.tc.read_all()

some_lst = [
    "conf t",
    "router ospf 1",
    "net 0.0.0.0 0.0.0.0 area 1",
    "end"
]


def upload_basic_config(dev):
    if dev.vendor == "vIOS":
        command_obj = create_config_obj(dev) ## -> commands.py
        tc = Telnet_Conn(dev)
        tc.first_send()
        tc.send_lst(command_obj.basic_config())
        # tc.send_lst(command_obj.ssh_config())
        # tc.send_lst(command_obj.create_config_interface())
        # tc.send_lst(some_lst)

    else:
        pass




def main():
    pass

if __name__ == "__main__":
    main()