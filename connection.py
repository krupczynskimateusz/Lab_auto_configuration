#!/usr/bin/env python3

from telnetlib import Telnet
from netmiko import ConnectHandler, file_transfer
from paramiko import SSHClient
from scp import SCPClient
from time import sleep
from commands import create_config_obj
from getpass import getpass
from hashlib import sha1 as hash_sha1
from os import remove as os_remove


# class Telnet_Conn():


#     def __init__(self, devobj):
#         self.host = gns_server_ip
#         self.port = devobj.console_port
#         self.name = devobj.name
#         self.username = devobj.username
#         self.password = devobj.password


#     def connect(self):
#         try:
#             self.tc = Telnet(
#                 host = self.host,
#                 port = str(self.port)
#                 )
#             sleep(1)
#         except ConnectionRefusedError:
#             print(f"Can't connect to {self.name}...")
#             print("Check if that device is up...")
#             print("Exiting...\n")
#             return 


#     def authenticate(self, output):
#         if "User" in output or "user" in output:
#             self.tc.write(self.username.encode(), b"\n")
#             sleep(1)
#             self.tc.write(self.password.encode(), b"\n")
#         else:
#             pass


#     def close(self):
#         self.tc.close()


#     def first_send(self, timeout = 1):
#         self.connect()
        
#         ## Don't work. Somehow you need to press enter on remote console.
#         self.tc.write(b"\n")

#         self.close()


#     def send(self, command, timeout = 0.5):
#         self.connect()

#         command = command + "\n"
#         self.tc.write(command.encode())
#         sleep(timeout)

#         self.close()


#     def send_lst(self, commands_lst, timeout = 0.5):
#         self.connect()

#         for cmd in commands_lst:
#             if isinstance(cmd, list):
#                 command = cmd[0] + "\n"
#                 self.tc.write(command.encode())
#                 sleep(cmd[1])
#             else:
#                 cmd = cmd + "\n"
#                 self.tc.write(cmd.encode())
#                 sleep(timeout)

#         self.close()


#     def show_all(self):
#         return self.tc.read_all()



class GNS3_Conn():

    def __init__(self, lab_ip):
        self.host = lab_ip
        self.port = "22"
        self.gns_files_path = "/opt/gns3/projects/"
        print("GNS3 connection parametr:")
        # self.username = input("Username: ")
        # self.password = getpass("Password: ")
        # self.secret = getpass("Secret: ")
        self.username = "mateusz"
        self.password = "admin123"
        self.secret = "admin123"


    def _connect(self):
        """Connect to gns3 server"""
        from netmiko import NetMikoTimeoutException
        from netmiko import NetMikoAuthenticationException
        try:
            self.ssh = ConnectHandler(
                host = self.host,
                port = self.port,
                username = self.username,
                password = self.password,
                secret = self.secret,
                device_type = "linux",
                system_host_keys = True,
                allow_agent = True,
                verbose = False,
            )
        except NetMikoTimeoutException:
            print("\n")
            print("Can't connect to GNS3 server...")
            print("Check your connectivity")
            print("Exiting...\n")
            exit()
        except NetMikoAuthenticationException:
            print("\n")
            print("Can't connect to GNS3 server...")
            print("Authentication problem ocur.")
            print("Exiting...\n")
            exit()
        except Exception as err:
            print("\n")
            print("Can't connect to GNS3 server...")
            print(f"Exception cour: {err}")
            print("Exiting...\n")
            exit()


    def _close(self):
        """Close connection if exist."""
        try:
            self.ssh.disconnect()
        except:
            pass


    def send(self, command: str):
        """Simple sending of command """
        self._connect()

        if "sudo" in command:
            self.ssh.enable()
        output = self.ssh.send_command(command)

        self._close()

        return output


    def get_labs_names(self):
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

        cmd_path = "sudo ls -l " + self.gns_files_path

        ## Get folder names for gns3/project
        output = self.send(cmd_path)
        folder_names = get_folders_name(output)
        project_lst = extract_project_names(cmd_path, folder_names)

        return project_lst


    def download_project(self, project_to_download, path):
        """
        The function is used to download the lab project from
        the GNS3 server. The first part copies the project to
        the tmp/ folder on the server and changes the project
        owner to the user with which we log in to gns3. Then
        the hash is calculated using the sha1 algorithm. After
        moving the project, it is downloaded by scp to the
        path selected by the user. The hash is checked. If it
        does not match, the file is deleted.

        :param: A project that needs to be downloaded.
        :param: Path where a project will be downloaded.
        """
        print(f"Copying project to local device to: {path}")

        copy_command = (
            "sudo cp " 
            f"{self.gns_files_path}{project_to_download[1]}"
            f"/{project_to_download[0]} "
            f"/tmp/{project_to_download[0]}"
            " && "
            f"sudo chown {self.username}:{self.username} "
            f"/tmp/{project_to_download[0]}"
        )
        self.send(copy_command)

        check_sha1_command = f"sha1sum /tmp/{project_to_download[0]}"
        remote_sha1 = self.send(check_sha1_command)
        remote_sha1 = remote_sha1.split()
        remote_sha1 = remote_sha1[0]

        ## SCP implementation. Netmiko don't work corectly.
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(
            hostname = self.host,
            username = self.username,
            password = self.password
        )
        ssh.exec_command
        scp = SCPClient(ssh.get_transport())
        scp.get(
            remote_path = f"/tmp/{project_to_download[0]}",
            local_path = path
            )
        if scp.transport.is_active():
            print("Closing SCP connection...")
            scp.close()
        if ssh.get_transport().is_active():
            print("Closing SSH connection...")
            ssh.close()
        
        with open(path, "br") as f:
            txt = f.read()
        local_sha1 = hash_sha1(txt)
        local_sha1 = local_sha1.hexdigest()
        
        if local_sha1 != remote_sha1:
            print("Files not equal. Deleting...")
            os_remove(path)
            return False
        
        return path



##################################


def get_gns3_projects(GNSServer):
    projects_lst = GNSServer.get_labs_names()

    return projects_lst


def get_project(GNSServer, project_to_download, path):
    path = GNSServer.download_project(project_to_download, path)

    return path


# def upload_basic_config(dev):
#     print("Create config...")

#     if dev.vendor == "vIOS":
#         command_obj = create_config_obj(dev) ## -> commands.py

#     elif dev.vendor == "C7200":
#         command_obj = create_config_obj(dev) ## -> commands.py

#     else:
#         pass

#     print("Sending connfig...")
#     tc = Telnet_Conn(dev)
#     tc.send_lst(command_obj)




if __name__ == "__main__":
    pass
