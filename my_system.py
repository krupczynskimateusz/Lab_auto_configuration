#!/usr/bin/env python3

import time



class Network():


    ipv4_addresses_pool = [f"192.168.10.{x}" for x in range(11, 40)]
    used_addresses = []


    def __init__(self, links):
        self.links = links


    @classmethod
    def get_ip_address(cls, vendor):
        ip = cls.ipv4_addresses_pool[0]
        cls.used_addresses.append(ip)
        cls.ipv4_addresses_pool.remove(ip)
        return ip


    def my_links(self, gns_id):
        my_links = []
        for link in self.links:
            for node in link:
                if node[0] == gns_id:
                    my_links.append(link)
        return my_links



class Device():

    dev_lst = []


    def __init__(
            self,
            network: object,
            gns_id: str,
            name: str,
            console_port: int
            ):
        self.network = network
        self.gns_id = gns_id
        self.name = name
        self.console_port = console_port
        self.vendor = None
        self.ip_mgmt = None
        self.links = None
        Device.dev_lst.append(self)


    def get_links(self):
        return self.network.connection_create(self.gns_id)


    @staticmethod
    def show_used_addresses():
        return Device.used_addresses


    @staticmethod
    def show_free_addresses():
        return Device.ipv4_addresses_pool



class IOS(Device):


    def __init__(
            self,
            network: object,
            gns_id: str,
            name: str,
            console_port: int
            ):
        super().__init__(network, gns_id, name, console_port)
        self.vendor = "vIOS"
        self.username = "cisco"
        self.password = "cisco"
        self.ip_mgmt = Network.get_ip_address(self)



def create_system(nodes, links):

    network_obj = Network(links)
    nodes_lst = []

    for dev in nodes:
        network = network_obj.my_links(dev[0])
        gns_id = dev[0]
        console_port = dev[1]
        name = dev[2]

        if "vIOS" == dev[3]:
            node = IOS(network, gns_id, name, console_port)

        else:
            node = Device(network, gns_id, name, console_port)
        nodes_lst.append(node)

    return nodes_lst



if __name__ == "__main__":
    pass