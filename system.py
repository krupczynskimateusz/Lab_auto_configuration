#!/usr/bin/env python3

class Device():

    _ipv4_address_pull = [f"192.168.10.{x}" for x in range(11, 40)]

    def __init__(self, dev_id: int, gns_id: str, name: str):
        self.dev_id = dev_id
        self.gns_id = gns_id
        self.name = name

    @property
    def ip_mngt(self):
        ip = Device._ipv4_address_pull[0]
        Device._ipv4_address_pull.remove(ip)
        return ip

    

def main():
    dev = Device(923487523, "shdlfkzxcv", "R1")
    print(dev.dev_id)
    print(dev.ip_mngt)

if __name__ == "__main__":
    main()