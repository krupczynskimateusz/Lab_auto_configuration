#!/usr/bin/env python3



class Network():


    ipv4_addresses_pool = [f"192.168.10.{x}" for x in range(11, 40)]
    ipv4_address_gatway = "192.168.10.1"
    ipv4_address_mask = "25"
    used_addresses = []
    multiacces_addresses = [f"10.0.{x}.0" for x in range(1, 10)]
    used_multiacces_addresses = []


    def __init__(self, links):
        self.links = links


    def my_links(self, gns_id):
        my_links = []
        for link in self.links:
            for node in link:
                if node[0] == gns_id:
                    my_links.append(link)
        return my_links


    @classmethod
    def get_ip_address(cls):
        ip = cls.ipv4_addresses_pool[0]
        cls.used_addresses.append(ip)
        cls.ipv4_addresses_pool.remove(ip)
        return ip


    @classmethod
    def get_multiacces_address(cls):
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



class Device():


    dev_lst = []
    dev_num = 0


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
        self.ip_mgmt_mask = None
        self.links = None
        self.num = None
        Device.dev_lst.append(self)


    def get_links(self):
        return self.network.connection_create(self.gns_id)


    @classmethod
    def give_number(cls):
        cls.dev_num += 1
        return cls.dev_num 



class GNS_Switch(Device):


    def __init__(
            self,
            network: object,
            gns_id: str,
            name: str,
            console_port: int
            ):
        super().__init__(
            network,
            gns_id,
            name,
            console_port
            )
        self.vendor = "gns_switch"
        self.multiacces_prefix = Network.get_multiacces_address()



class IOS(Device):


    def __init__(
            self,
            network: object,
            gns_id: str,
            name: str,
            console_port: int
            ):
        super().__init__(
            network,
            gns_id,
            name,
            console_port
            )
        self.vendor = "vIOS"
        self.username = "cisco"
        self.password = "cisco"
        self.ip_mgmt = Network.get_ip_address()
        self.ip_mgmt_mask = Network.get_ip_address_mask()
        self.num = Device.give_number()



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
        
        elif "gns_switch" == dev[3]:
            node = GNS_Switch(network, gns_id, name, console_port)

        else:
            node = Device(network, gns_id, name, console_port)
        nodes_lst.append(node)

    return nodes_lst



if __name__ == "__main__":
    pass