#!/usr/bin/env python3

from telnetlib import Telnet
from netmiko import ConnectHandler
from time import sleep
from commands import create_config_obj
import os
from getpass import getpass


gns_server_ip = "192.168.10.126"


class Telnet_Conn():


    def __init__(self, devobj):
        self.host = gns_server_ip
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



class GNS3_Conn():


    def __init__(self):
        self.host = gns_server_ip
        self.port = "22"
        print("Gns3 connection parametrs:")
        # self.username = input("Username: ")
        # self.password = getpass("Password: ")
        # self.secret = getpass("Secret: ")
        self.username = "mateusz"
        self.password = "admin123"
        self.secret = "admin123"


    def _connect(self):
        self.ssh = ConnectHandler(
            host = self.host,
            port = self.port,
            username = self.username,
            password = self.password,
            secret = self.secret,
            device_type = "linux",
            system_host_keys = True,
            allow_agent = True,
            verbose = True 
        )


    def _close(self):
        self.ssh.disconnect()


    def send(self, command: str):
        self._connect()

        if "sudo" in command:
            self.ssh.enable()
        output = self.ssh.send_command(command)

        self._close()

        return output


    def get_labs_names(self, gns_path: str):
        """
        This function returns all project names from gns3 server.

        :param: str path to gns3 projects folder on remote server.
        :retur: list with project names.
        """

        def get_folders_name(output):
            """Extract folder names"""
            tmp_lst = output.splitlines()

            lst_folder_names = []
            for line in tmp_lst[2:]:
                lst_line = line.split()
                lst_folder_names.append(lst_line[-1])
            
            return lst_folder_names

        def create_command_lst(cmd, lst):
            """
            Creates a commend list with an extended 
            path containing folder names
            """
            command_lst = []

            for item in lst:
                command_lst.append(cmd + item + "/")

            return command_lst
        
        def extract_project_names(cmd, folders_lst):
            """
            Sends command and create list with 
            project names and parent folder.
            """
            self._connect()
            if "sudo" in cmd:
                self.ssh.enable()
            folders = []
            for folder in folders_lst:

                output = self.ssh.send_command(cmd + folder + "/")

                files_lst = get_folders_name(output)
                for file in files_lst:
                    if ".gns3" in file and "backup" not in file:
                        folders.append([file, folder])

            self._close()

            return folders

        cmd_path = "sudo ls -l " + gns_path

        ## Get folder names for gns3/project
        output = self.send(cmd_path)

        ## Extract folder names
        folder_names = get_folders_name(output)

        ## Get priojects name with parent folder. 
        project_lst = extract_project_names(cmd_path, folder_names)

        return project_lst


def gns3_projects(path_to_gns3_folder):
    gns3 = GNS3_Conn()

    return gns3.get_labs_names(path_to_gns3_folder)


def upload_basic_config(dev):
    if dev.vendor == "vIOS":
        command_obj = create_config_obj(dev) ## -> commands.py
        tc = Telnet_Conn(dev)

    else:
        pass


if __name__ == "__main__":
    pass
