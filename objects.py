#!/usr/bin/env python3
from telnetlib import Telnet
from netmiko import ConnectHandler
from paramiko import SSHClient
from scp import SCPClient
from hashlib import sha1 as hash_sha1
from time import sleep
from os import remove as os_remove
import json



_lab_ip = "gns3.home"
_options_lst = [
    "Show projects from gns3 server.",
    "Set project.",
    "Execute script.",
    "Free execute",
    "Exit."
]
_local_path = "/tmp/gns3_project.gns3"



class My_Menu():
    """
    Object Menu is responsible for configuration 
    management and basic validation.

    :param _options_lst: List of options that will 
                            appere after execute functions 
                            show_menu()

    :param _local_path: Path to the folder on the local
                            system where the project file 
                            will be downloaded or where it
                            is currently located.

    :param lab_server: Server object. 

    :param data_parser: Object Data_Parser. 

    :param _lab_ip: Server IP. Use to telnet connections 
                            and for SSH connections.

    :param _project_lst: Use later for manage projects.

    :param _selected_project: Use later for manage projects.

    :param _system: Useed for check that system with 
                            devices was already created.
    """

    _system = False
    _lab_ip = _lab_ip


    def __init__(self):
        self._options_lst = _options_lst
        self._local_path = _local_path
        self.lab_server = GNS3_Conn(My_Menu._lab_ip)
        self.data_parser = Data_Parser()
        self._lab_ip = My_Menu._lab_ip
        self._project_lst = None
        self._selected_project = None
        self._system = My_Menu._system


    def show_menu(self):
        """
        Wyświetl menu z możliwymi opcjami.
        Menu execute scripts.
        """
        print("\n")
        print("#" * 10, "MENU", "#" * 10, "\n")

        for i, option in enumerate(self._options_lst, start = 1):
            print(f"# {i}) {option}")

        chose = input("# Chose option: ")

        if chose == "1":
            self.show_projects()

        elif chose == "2":
            self._selected_project = self.set_project()

        elif chose == "3":
            self.execute_script()
            sleep(0.5)

        elif chose == "4":
            self.free_execute()

        elif chose == "5":
            print("Exiting...")
            exit()

        else: 
            print("You need to pick valid option...")
            sleep(1)


    def show_projects(self):
        """The function shows list project that are on lab server."""
        if self._project_lst == None:
            self._project_lst = self.lab_server.get_labs_names()

        print("## Project list:", "\n")

        for _index, _name in enumerate(self._project_lst, start = 1):
            _tmp_name = _name[0].removesuffix(".gns3")
            print(f"# {_index:02}) {_tmp_name}")

        chose = input("Click any charakter for back to menu...")

        return


    def set_project(self):
        """Function to select a project to download."""
        print("\n")
        print("#" * 26)
        _selected_project = input("# Enter project name or number: ")
        try:
            self._selected_project = ("number", int(_selected_project))
            return self._selected_project
        except:
            self._selected_project = ("string", _selected_project)
            return self._selected_project


    def execute_script(self):
        """
        The main task of this function is to download the project file,
        create configuration files and execute them on appropriate devices.
        """
        ## Check if project was selected.
        if self._selected_project == None:
            return print("You need to select project...")
        
        ## If project list don't exist -> download from server.
        if self._project_lst == None:
            print("You need to download available projects from the server...")
            print("Downloading...")
            self._project_lst = self.lab_server.get_labs_names()

        if self._selected_project[0] == "string":
            _project_num = 0
            _tmp_project = None
            print("Looking for project...")

            for project in self._project_lst:

                if self._selected_project[1] in project[0]:
                    _project_num += 1
                    _tmp_project = project

            if _project_num == 1:
                _project_to_download = _tmp_project

            elif _project_num > 1:
                print(
                    "Too many similar project...\n"
                    "Pleas be more specific with name or use number..."
                    )
                return

            else:
                print("Can't find project...")

        elif self._selected_project[0] == "number":
            _project_to_download = self._project_lst[self._selected_project[1] - 1]

        else:
            print("Error with selected_project ocur....")
            exit()

        ## Try download project form server.
        try:
            project_path = self.lab_server.download_project(
                _project_to_download,
                self._local_path
                )
            if project_path == False:
                print("Can't download project to local machine...")
                return

        except:
            return "Can't download project to local machine..."

        try:
            self.data_parser.get_topology_gns3(project_path)
            print("Creating device objects...")
            self.create_system()

            for device in Device.managed_dev_lst:
                print(f"# Start {device.name}...")
                try:
                    print("Create telnet connections...")
                    try:
                        _tc = Telnet_Conn(device)
                    except:
                        print("Can't create Telnet object...")
                        pass
                    
                    ## Later there will be options to chose what to configure.
                    print("Set basic config...")
                    _tc.send_lst(device.commands.basic_config())
                    print("Set ssh configuration..")
                    _tc.send_lst(device.commands.ssh_config())
                    print("Set managment interface...")
                    _tc.send_lst(device.commands.create_mgmt())
                    print("Set interface configuration...")
                    _tc.send_lst(device.commands.create_config_interfaces())


                except:
                    print("Can't create telnet connections...")
                    pass

        except:
            return "Can't finish executing project..."


    def free_execute(self):
        """
        This function create system and print list with
        configuration without downloading file from lab server.
        """
        print("#" * 26)

        try:
            self.data_parser.get_topology_gns3(self._local_path)

            print("## Creating device objects...")
            self.create_system()

            for device in Device.managed_dev_lst:
                print(f"# Start {device.name}...")
                print("Trying create configuration...")
                try:
                    print(device.commands.basic_config())
                    print(device.commands.ssh_config())
                    print(device.commands.create_mgmt())
                    print(device.commands.create_config_interfaces())
                    print("\n")

                except:
                    print("Can't create configuration...")
                    print("\n")
                    pass

        except:
            print("There was a problem with system creating...")
            print("Exiting...")
            exit()


    def create_system(self):
        if self._system == False:
            network_obj = Network(self.data_parser.links)
            nodes_dct = self.data_parser.nodes
            
            for node in nodes_dct:
                network = network_obj.my_links(node[0])
                gns_id = node[0]
                console_port = node[1]
                name = node[2]
                adapters_num = node[4]

                if "vIOS" == node[3]:
                    IOS(
                        network = network,
                        gns_id = gns_id,
                        name = name,
                        console_port = console_port,
                        adapters_num = adapters_num
                        )

                elif "gns_switch" == node[3]:
                    GNS_Switch(
                        network = network,
                        gns_id = gns_id,
                        name = name
                        )

                else:
                    Device(
                        network = network,
                        gns_id = gns_id,
                        name = name
                        )

            self._system = True
            print("Created...")
        else:
            print("System created.")

        return



class Network():
    """
    A network object based on which 
    the necessary information about 
    prefixes and free addresses is retrieved.
    """


    ipv4_addresses_pool = [f"192.168.10.{x}" for x in range(11, 40)]
    ipv4_address_gatway = "192.168.10.1"
    ipv4_address_mask = "25"
    used_addresses = []

    multiacces_addresses = [f"10.0.{x}.0" for x in range(1, 10)]
    used_multiacces_addresses = []


    def __init__(self, links):
        self.links = links


    def my_links(self, gns_id):
        """
        The function returns a list of connections in which the device participates.

        :parm: Device GNS_ID
        :return: List of links. 
        """
        
        my_links = []
        for link in self.links:
            for node in link:
                if node[0] == gns_id:
                    my_links.append(link)
        return my_links


    @classmethod
    def get_ip_address(cls):
        """
        The function give free ip address for managment purpose.

        :return: IPv4 address string.
        """
        
        ip = cls.ipv4_addresses_pool[0]
        cls.used_addresses.append(ip)
        cls.ipv4_addresses_pool.remove(ip)
        return ip


    @classmethod
    def get_multiacces_address(cls):
        """
        The function give prefix for switch for multiacces purpose. 

        :return: IPv4 address.
        """
        
        ip = cls.multiacces_addresses[0]
        cls.used_multiacces_addresses.append(ip)
        cls.multiacces_addresses.remove(ip)
        return ip


    @classmethod
    def get_ip_address_mask(cls):
        return cls.ipv4_address_mask


    @staticmethod
    def show_used_addresses():
        return Device.used_addresses


    @staticmethod
    def show_free_addresses():
        return Device.ipv4_addresses_pool



####################
### CONNECTIONS ####
####################



class Telnet_Conn():

    host_ip = _lab_ip

    def __init__(self, devobj):
        self.host = Telnet_Conn.host_ip
        self.port = devobj.console_port
        self.name = devobj.name
        self.username = devobj.username
        self.password = devobj.password


    def connect(self):
        try:
            self.tc = Telnet(
                host = self.host,
                port = str(self.port)
                )
            sleep(1)
        except ConnectionRefusedError:
            print(f"Can't connect to {self.name}...")
            print("Check if that device is up...")
            print("Exiting...\n")
            return

    ## Probably dont needed
    # def authenticate(self, output):
    #     if "User" in output or "user" in output:
    #         self.tc.write(self.username.encode(), b"\n")
    #         sleep(1)
    #         self.tc.write(self.password.encode(), b"\n")
    #     else:
    #         pass


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


    def __init__(self, lab_ip):
        self.host = lab_ip
        self.port = "22"
        self.gns_files_path = "/opt/gns3/projects/"
        self._set_con_parametrs = False

    def configure_conn_paramters(self):
        from getpass import getpass

        print("\n")
        print("#" * 26)
        print("GNS3 parametr configuration...")
        self.username = input("Username: ")
        self.password = getpass("Password: ")
        self.secret = getpass("Secret: ")
        self._set_con_parametrs = True
        return

    def _connect(self):
        """Connect to gns3 server"""
        from netmiko import NetMikoTimeoutException
        from netmiko import NetMikoAuthenticationException

        if self._set_con_parametrs == False:
            self.configure_conn_paramters()
            self._connect()
        else:
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
                print("Can't connect to GNS3 server...")
                print("Check your connectivity")
                print("Exiting...\n")
                exit()
            except NetMikoAuthenticationException:
                print("Can't connect to GNS3 server...")
                print("Authentication problem ocur.")
                print("Exiting...\n")
                exit()
            except Exception as err:
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


    def download_project(self, project_to_download, local_path):
        """
        The function is used to download the lab project from
        the GNS3 server. The first part copies the project to
        the tmp/ folder on the server and changes the project
        owner to the user with which we log in to gns3. Then
        the hash is calculated using the sha1 algorithm. After
        moving the project, it is downloaded by scp to the
        local_path selected by the user. The hash is checked. If it
        does not match, the file is deleted.

        :param: A project that needs to be downloaded.
        :param: local_path where a project will be downloaded.
        """
        print(
            "Start procedure copying project" 
            f"to local device to: {local_path}..."
            )

        copy_command = (
            "sudo cp "
            f"{self.gns_files_path}{project_to_download[1]}"
            f"/{project_to_download[0]} "
            f"/tmp/{project_to_download[0]}"
            " && "
            f"sudo chown {self.username}:{self.username} "
            f"/tmp/{project_to_download[0]}"
        )

        print("Remote: Copy to /tmp/...")
        self.send(copy_command)

        print("Remote: Get file hash...")
        check_sha1_command = f"sha1sum /tmp/{project_to_download[0]}"
        remote_sha1 = self.send(check_sha1_command)
        remote_sha1 = remote_sha1.split()
        remote_sha1 = remote_sha1[0]

        ## SCP implementation. Netmiko don't work like i want.
        print("Trying download file...")
        try:
            ssh = SSHClient()
            ssh.load_system_host_keys()
            ssh.connect(
                hostname = self.host,
                username = self.username,
                password = self.password
            )
        except:
            print("Can't connect to server...")
            return False

        scp = SCPClient(ssh.get_transport())

        try:
            scp.get(
                remote_path = f"/tmp/{project_to_download[0]}",
                local_path = local_path
                )
        except:
            print("Can't download file...")
            if scp.transport.is_active():
                print("Closing SCP connection...")
                scp.close()
            if ssh.get_transport().is_active():
                print("Closing SSH connection...")
                ssh.close()
            return
        
        if scp.transport.is_active():
            print("Closing SCP connection...")
            scp.close()
        if ssh.get_transport().is_active():
            print("Closing SSH connection...")
            ssh.close()
        
        with open(local_path, "br") as f:
            txt = f.read()
        print("Get local file hash...")
        local_sha1 = hash_sha1(txt)
        local_sha1 = local_sha1.hexdigest()
        
        print("Compare hash...")
        if local_sha1 != remote_sha1:
            print("Files not equal. Deleting...")
            os_remove(local_path)
            return False
        else:
            print("Correct...")
            return local_path



####################
##### PARSERS ######
####################

class Data_Parser():


    def __init__(self):
        self.links = None
        self.nodes = None


    @staticmethod
    def get_links_info(links):
        links_info = []
        for _link in links:
            connection = []
            for node in _link["nodes"]:
                gns_id = node["node_id"]
                int_name = node["label"]["text"]
                adapter_num = node["adapter_number"]
                connection.append((gns_id, int_name, adapter_num))
            connection = tuple(connection)
            links_info.append(connection)
        return links_info


    @staticmethod
    def get_nodes_info(nodes):
        nodes_info = []

        for _node in nodes:
            gns_id = _node["node_id"]
            console_port = _node["console"]
            node_name = _node["name"]

            if "hda_disk_image" in _node["properties"].keys():
                if "vios-adventerprisek9" in _node["properties"]["hda_disk_image"]:
                    vendor = "vIOS"
                    adapters_num = _node["properties"]["adapters"]

            elif "image" in _node["properties"].keys():
                if "c7200-adventerprisek9-mz" in _node["properties"]["image"]:
                    vendor = "C7200"
                    adapters_num = _node["properties"]["adapters"]

            elif "ethernet_switch" in _node["node_type"]:
                vendor = "gns_switch"
                
            else:
                vendor = None

            tmp_tuple = (gns_id, console_port, node_name, vendor, adapters_num)
            nodes_info.append(tmp_tuple)

        return nodes_info


    def get_topology_gns3(self, path):
        with open(path) as f:
            _dct_file = json.load(f)
        _dct_links = _dct_file["topology"]["links"] 
        _dct_nodes = _dct_file["topology"]["nodes"]
        del _dct_file

        self.links = self.get_links_info(_dct_links)
        self.nodes = self.get_nodes_info(_dct_nodes)


    ## Only for debug purpose.
    def show_in_file(self, path: str):
        from pathlib import Path
        with open(path, "w") as f:
            f.write('{ "links": ')
            f.write(json.dumps(self.nodes, indent = 4))
            f.write(",\n")
            f.write('"nodes": ')
            f.write(json.dumps(self.links, indent = 4))
            f.write("}")
        my_file = Path(path)



####################
##### DEVICES ######
####################


class Device():


    dev_lst = []
    managed_dev_lst = []
    dev_num_lst = []


    def __init__(
            self,
            network: object,
            gns_id: str,
            name: str
            ):
        self.network = network
        self.gns_id = gns_id
        self.name = name
        Device.dev_lst.append(self)


    def get_links(self):
        return self.network.connection_create(self.gns_id)


    def give_number(self):
        _name = self.name
        for num in range(len(_name)):
            if _name[num:].isnumeric():
                number = _name[num:]
            else:
                pass
        if number == None:
            print("Can't create device number. Script will not works...")
            print("Make sure the lab device name ends with a non-duplicate number")
            exit()
        elif number in Device.dev_num_lst:
            print("Can't create device number. Script will not works...")
            print("Make sure the lab device name ends with a non-duplicate number")
            exit()
        else:
            Device.dev_num_lst.append(number)
            return number


class GNS_Switch(Device):


    def __init__(
            self,
            network: object,
            gns_id: str,
            name: str
            ):
        super().__init__(
            network,
            gns_id,
            name
            )
        self.vendor = "gns_switch"
        self.multiacces_prefix = Network.get_multiacces_address()



class IOS(Device):


    def __init__(
            self,
            network: object,
            gns_id: str,
            name: str,
            console_port: int,
            adapters_num: int,
            domain: str = "lab.home"
            ):
        super().__init__(
            network,
            gns_id,
            name
            )
        self.vendor = "vIOS"
        self.console_port = console_port
        self.domain = domain
        self.username = "cisco"
        self.password = "cisco"
        self.adapters_num = adapters_num - 1  ## Count from 0
        self.ip_mgmt = Network.get_ip_address()
        self.ip_mgmt_mask = Network.get_ip_address_mask()
        self.num = self.give_number()
        self.commands = Command_IOS(self)
        Device.managed_dev_lst.append(self)



####################
##### COMANDS ######
####################

class Command():
    """
    A class used to create a basic Command object that is
    later used to create device configurations.

    :parm: The device object.
    """


    def __init__(self, devobj):
        self.gns_id = devobj.gns_id
        self.vendor = devobj.vendor
        self.ip_mgmt = devobj.ip_mgmt
        self.ip_mgmt_mask = devobj.ip_mgmt_mask
        self.name = devobj.name
        self.network = devobj.network
        self.num = devobj.num
        self.domain = devobj.domain
        self.adapters_num = devobj.adapters_num
        self.interface_lst_bool = False


    def get_interface_list(self):
        """
        This function returns interface name and
        gns_id device that interface are connected.
        
        :parm: Device Object
        :return: List of tuple with int. and device connected to.
        """
        if self.interface_lst_bool == False:
            interface_lst = []
            tmp = 0

            for link in self.network:
                if link[tmp][0] == self.gns_id:
                    interface_lst.append((link[tmp][1], link[tmp + 1][0], link[tmp][2]))

                elif link[tmp + 1][0] == self.gns_id:
                    interface_lst.append((link[tmp + 1][1], link[0][0], link[tmp + 1][2]))

            self.interface_lst = interface_lst
            self.interface_lst_bool = True

        else:
            return


    def get_last_interface_name(self):
        """
        """
        if self.interface_lst_bool == True:
            for link in self.interface_lst:

                if link[2] == self.adapters_num:
                    self.last_interface_name = link[0]
        else:
            try:
                self.get_interface_list()
                self.get_last_interface_name()
            except:
                print("Can't create interface list...")

    @staticmethod
    def get_num(gns_id):
        for dev in Device.dev_lst:
            if gns_id == dev.gns_id:

                if hasattr(dev, 'num'):
                    return dev.num
                
                else:
                    return None

    @staticmethod
    def get_multiacces_prefix(gns_id):
        """
        Function used to retrieve the prefix of the switch to which the device is connected.

        :parm: Switch gns_id,
        :retrun: Switch prefix.
        """
        dev_lst = Device.dev_lst

        for dev in dev_lst:

            if dev.gns_id == gns_id:
                return dev.multiacces_prefix[:-2]
            
            else:
                pass



class Command_IOS(Command):
    """
    Subclass of the Command object. 
    Support for the Cisco IOS devices.
    """


    def __init__(self, devobj):
        super().__init__(devobj)


    def get_mask(self):
        """
        Function convert shortened subnet mask
        to plain subnet mask

        :return: str plain subnet mask
        """
        if self.ip_mgmt_mask == "21":
            return "255.255.248.0"
        elif self.ip_mgmt_mask == "22":
            return "255.255.252.0"
        elif self.ip_mgmt_mask == "23":
            return "255.255.254.0"
        elif self.ip_mgmt_mask == "24":
            return "255.255.255.0"
        elif self.ip_mgmt_mask == "25":
            return "255.255.255.128"
        elif self.ip_mgmt_mask == "26":
            return "255.255.255.192"
        elif self.ip_mgmt_mask == "27":
            return "255.255.255.224"


    def basic_config(self):
        """
        Generet basic config for Cisco IOS device.
        It includes setting the hostname, domain and username.

        :return:  List of commend to execute" 
        """
        lst_commands = [
            "conf t",
            f"hostname {self.name}",
            f"ip domain name {self.domain}",
            "username cisco privilege 15 secret cisco",
            "end"
        ]
        return lst_commands


    def ssh_config(self):
        """
        Create rsa key with key lenght 2048. Enalbe ssh version 2.
        Changes virtual lines to allow connection with ssh.

        :return:  List of commends to execute" 
        """
        lst_commands = [
            "conf t",
            "crypto key generate rsa",
            ["2048", 8],
            "ip ssh version 2",
            "ip ssh pubkey-chain",
            "username cisco",
            "key-hash ssh-rsa 3DDF6DD82060F31277A6004B176786D4",
            "line vty 0 4",
            "exec-timeout 0 0",
            "transport input ssh",
            "login local",
            "end"
        ]
        return lst_commands


    def create_mgmt(self):
        """
        This funtion return commands that are needed to create
        mgmnt interface. For this purpose last interface on device
        is taken. Last in the list of interface in GNS3. Mgmt interface
        is create in separate vrf called mgmt.

        :return: List of commands to execute.
        """
        self.get_interface_list()
        self.get_last_interface_name()

        lst_commands = [
            "conf t",
            "vrf definition mgmt",
            "address-family ipv4 unicast",
            "exit",
            f"interface {self.last_interface_name}",
            "vrf forwarding mgmt",
            f"ip address {self.ip_mgmt} {self.get_mask()}",
            "no shutdown",
            "exit",
            "ip route vrf mgmt 0.0.0.0 0.0.0.0 "
            f"{Network.ipv4_address_gatway}",
            "end"
            ]
        return lst_commands


    def create_config_interfaces(self):
        """
        The function works on a simple interface configuration model.
        When connecting R-a to R-b, the interfaces will be set as follows:
        10.x.y.z, where x is the lower number of device a or b, y is
        the higher number of device a or b, and z is the number of the device
        for which the configuration is generated. In case of connection
        to multi-access networks, the interface will receive the address:
        10.0.x.z, where x is the subnet assigned to the switch, and z is
        the device for which the configuration is generated
        
        :return: List of commands to execute.
        """
        self.get_interface_list()

        lst_commands = ["conf t"]

        for connection in self.interface_lst:
            if connection[0] != self.last_interface_name:
                ## "Get the 'num' of the device I'm connected to"
                dev_connect_to_num = self.get_num(connection[1])

                ## If device is conneto to switch:
                if  dev_connect_to_num == None:
                    lst_commands.append(f"interface {connection[0]}")
                    tmp = (
                        f"ip address "
                        f"{self.get_multiacces_prefix(connection[1])}"
                        f".{self.num} "
                        f"255.255.255.0"
                        )
                    lst_commands.append(tmp)
                    lst_commands.append("no shutdown")

                ## If device is conneto to device with higher number.
                elif dev_connect_to_num > self.num:
                    lst_commands.append(f"interface {connection[0]}")
                    tmp = (
                        f"ip address 10.{self.num}"
                        f".{dev_connect_to_num}.{self.num} "
                        "255.255.255.0"
                        )
                    lst_commands.append(tmp)
                    lst_commands.append("no shutdown")

                ## If device is conneto to device with lower number.
                elif dev_connect_to_num < self.num:
                    lst_commands.append(f"interface {connection[0]}")
                    tmp = (
                        f"ip address 10.{dev_connect_to_num}"
                        f".{self.num}.{self.num} "
                        "255.255.255.0"
                        )
                        
                    lst_commands.append(tmp)
                    lst_commands.append("no shutdown")

        lst_commands.append("end")
        return lst_commands


    def create_loopback(self):
        """
        The function givs commands to configure
        interface loopback on device. 
        """
        num = self.num
        lst_commands = [
            "conf t",
            "interface loopback 0",
            f"ip address 1.1.1.{num} 255.255.255.255",
            "end"
        ]

        return lst_commands



if __name__ == "__main__":
    pass