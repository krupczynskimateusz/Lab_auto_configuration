#!/usr/bin/env python3

import time

class Device():

    ipv4_addresses_pool = [f"192.168.10.{x}" for x in range(11, 40)]
    used_addresses = []

    dev_lst = []

    def __init__(self, dev_id: int, gns_id: str, name: str, console_port: int):
        self.dev_id = dev_id
        self.gns_id = gns_id
        self.name = name
        self.console_port = console_port
        self.vendor = None
        self.ip_mgmt = None
        Device.dev_lst.append(self)

    @classmethod
    def get_ip_address(cls, vendor):
        ip = cls.ipv4_addresses_pool[0]
        cls.used_addresses.append(ip)
        cls.ipv4_addresses_pool.remove(ip)
        return ip

    @staticmethod
    def show_used_addresses():
        return Device.used_addresses

    @staticmethod
    def show_free_addresses():
        return Device.ipv4_addresses_pool
    

class IOS(Device):

    def __init__(self, dev_id: int, gns_id: str, name: str, console_port: int):
        super().__init__(dev_id, gns_id, name, console_port)
        self.vendor = "vIOS"
        self.username = "cisco"
        self.password = "cisco"
        self.ip_mgmt = Device.get_ip_address(self)



def create_devObj(dct):
    nodes_lst = []
    for dev in dct:
        dev_id = dev[0]
        gns_id = dev[1][0]
        console_port = dev[1][1]
        name = dev[1][2]
        if "vIOS" is dev[1][3]:
            node = IOS(dev_id, gns_id, name, console_port)
        else:
            node = Device(dev_id, gns_id, name, console_port)
        nodes_lst.append(node)
    return nodes_lst


if __name__ == "__main__":
    pass