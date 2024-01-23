#!/usr/bin/env python3

import ipaddress

class Network():

    ip_prefix = ipaddress.ip_network("192.168.10.0/25")

class Device():

    def __init__(self, ID: int, gns_id: str, name: str):
        self.ID = ID
        self.gns_id = gns_id
        self.name = name


def main():
    ip_prefix = ipaddress.ip_network("192.168.10.0/25")
    for element in ip_prefix.hosts():
        print(element)
    pass

if __name__ == "__main__":
    main()