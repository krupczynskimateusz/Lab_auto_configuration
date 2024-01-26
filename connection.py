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


    def test_send(self, timeout = 0.5):
        self.connect()

        command = "\n\n\n\n"
        self.tc.write(command.encode())
        sleep(timeout)

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



def upload_basic_config(dev):
    command_obj = create_config_obj(dev) ## -> commands.py
    # tc = Telnet_Conn(dev)
    # tc.test_send()
    # tc.send_lst(command_obj.basic_config())
    # tc.send_lst(command_obj.ssh_config())


def main():
    pass

if __name__ == "__main__":
    main()