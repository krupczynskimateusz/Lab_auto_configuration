#!/usr/bin/env python3

from my_system import Device, Network



class Command():


    def __init__(self, devobj):
        self.gns_id = devobj.gns_id
        self.vendor = devobj.vendor
        self.ip_mgmt = devobj.ip_mgmt
        self.ip_mgmt_mask = devobj.ip_mgmt_mask
        self.name = devobj.name
        self.network = devobj.network
        self.num = devobj.num


    def get_mask(self):
        pass


    def basic_config(self):
        pass


    def ssh_config(self):
        pass


    @staticmethod
    def give_dev_num(gns_id):
        # print(gns_id)
        dev_lst = Device.dev_lst
        # print(dev_lst[0].num)
        for dev in dev_lst:
            # print(dev.num)
            if dev.gns_id == gns_id:
                return dev.num
            else:
                pass


    @staticmethod
    def interface(dev):
        interface_lst = []
        tmp = 0

        for link in dev.network:

            if link[tmp][0] == dev.gns_id:
                interface_lst.append((link[tmp][1], link[tmp + 1][0]))

            elif link[tmp + 1][0] == dev.gns_id:
                interface_lst.append((link[tmp + 1][1], link[0][0]))

        return interface_lst



class Command_IOS(Command):


    def __init__(self, devobj):
        super().__init__(devobj)


    def get_mask(self):
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
        lst_commands = [
            "conf t",
            f"hostname {self.name}",
            "ip domain name lab.home",
            "username cisco privilege 15 secret cisco",
            "end"
        ]
        return lst_commands


    def ssh_config(self):
        lst_commands = [
            "conf t",
            "crypto key generate rsa",
            ["2048", 8],
            "ip ssh version 2",
            "end"
        ]
        return lst_commands


    def create_ip_mgmt(self):
        connections = Command.interface(self)
        lst_commands = [
            "conf t",
            "vrf definition mgmt",
            "exit",
            f"interface {connections[-1][0]}",
            "vrf forwarding mgmt",
            f"ip address {self.ip_mgmt} {self.get_mask()}",
            "no shutdown",
            "end"
            ]
        return lst_commands


    def create_config_interface(self):
        connections = Command.interface(self)
        lst_commands = ["conf t"]

        for connection in connections[:-1]:
            num = Command.give_dev_num(connection[1])

            if  num == None:
                prefix = Network.get_multiacces_prefix()
                lst_commands.append(f"interface {connection[0]}")
                tmp = (
                    f"{prefix}{self.num} "
                    "255.255.255.0"
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



def create_config_obj(devobj):
    if devobj.vendor == "vIOS":
        dev = Command_IOS(devobj)
        return dev
    else:
        pass


def main():
    pass


if __name__ == "__main__":
    main()