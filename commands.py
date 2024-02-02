#!/usr/bin/env python3

from my_system import Device, Network



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
        self.ip_domain = devobj.ip_domain


    @staticmethod
    def links_interface(dev):
        """
        This function returns interface name and
        gns_id device that interface are connected.
        
        :parm: Device Object
        :return: List of tuple with int. and device connected to.
        """

        interface_lst = []
        tmp = 0

        for link in dev.network:

            if link[tmp][0] == dev.gns_id:
                interface_lst.append((link[tmp][1], link[tmp + 1][0]))

            elif link[tmp + 1][0] == dev.gns_id:
                interface_lst.append((link[tmp + 1][1], link[0][0]))

        return interface_lst


    @staticmethod
    def give_dev_num(gns_id):
        """
        The function is used to find the number of the device to which we are connected.
        """
        dev_lst = Device.dev_lst

        for dev in dev_lst:

            if dev.gns_id == gns_id:
                return dev.num
            
            else:
                pass


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
            f"ip domain name {self.ip_domain}",
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
            "line vty 0 4",
            "transport input ssh",
            "login local",
            "end"
        ]
        return lst_commands


    def create_ip_mgmt(self):
        """
        This funtion return commands that are needed to create
        mgmnt interface. For this purpose last interface on device
        is taken. Last in the list of interface in GNS3. Mgmt interface
        is create in separate vrf called mgmt.

        :return: List of commands to execute.
        """
        connections = Command.links_interface(self)
        lst_commands = [
            "conf t",
            "vrf definition mgmt",
            "exit",
            f"interface {connections[-1][0]}",
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
        connections = Command.links_interface(self)
        lst_commands = ["conf t"]

        for connection in connections[:-1]:
            num = Command.give_dev_num(connection[1])

            if  num == None:
                lst_commands.append(f"interface {connection[0]}")
                tmp = (
                    f"ip address "
                    f"{Command.get_multiacces_prefix(connection[1])}"
                    f".{self.num} "
                    f"255.255.255.0"
                    )
                lst_commands.append(tmp)
                lst_commands.append("no shutdown")


            elif num > self.num:
                lst_commands.append(f"interface {connection[0]}")
                tmp = (
                    f"ip address 10.{self.num}"
                    f".{num}.{self.num} "
                    "255.255.255.0"
                    )
                lst_commands.append(tmp)
                lst_commands.append("no shutdown")

            elif num < self.num:
                lst_commands.append(f"interface {connection[0]}")
                tmp = (
                    f"ip address 10.{num}"
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



class Command_C7200(Command_IOS):
    """
    Subclass of the Command object. 
    Support for the Cisco c7200 devices.
    """

    def __init__(self, devobj):
        super().__init__(devobj)



def create_config_obj(devobj):
    """
    This function support easy way to create Command()
    objects with skipping Device() that are not supported.
    """

    if devobj.vendor == None:
        pass

    elif devobj.vendor == "gns_switch":
        pass

    elif devobj.vendor == "vIOS":
        dev = Command_IOS(devobj)
        return dev
    
    elif devobj.vendor == "c7200":
        dev = Command_C7200(devobj)
        return dev
    
    else:
        pass



if __name__ == "__main__":
    pass