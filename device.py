#!/usr/bin/env python3

import ipaddress

class Network():
    pass


class Device():

    def __init__(self, ID: int, gns_id: str, name: str):
        self.ID = ID
        self.gns_id = gns_id
        self.name = name
    
    @property
    def ip_mgmnt(self, network):
        Network
def main():
    pass

if __name__ == "__main__":
    main()