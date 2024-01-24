#!/usr/bin/env python3

import time

class Device():

    _ipv4_address_pool = [f"192.168.10.{x}" for x in range(11, 40)]

    def __init__(self, dev_id, gns_id, name, console_port):
        self.dev_id = dev_id
        self.gns_id = gns_id
        self.name = name
        self.console_port = console_port
        self.vendor = None

    @property
    def ip_mgmt(self):
        ip = Device._ipv4_address_pool[0]
        return ip



# class vIOS(Device):

#     def __init__(self, dev_id, gns_id, name, console_port):
#         super().__init__(dev_id, gns_id, name, console_port)
#         self.vendor = "vIOS"



def create_devObj(dct):
    nodes_lst = []
    for dev in dct:
        dev_id = dev[0]
        gns_id = dev[1][0]
        name = dev[1][1]
        console_port = dev[1][2]
        node = Device(dev_id, gns_id, name, console_port)
        nodes_lst.append(node)
    return nodes_lst


if __name__ == "__main__":
    pass