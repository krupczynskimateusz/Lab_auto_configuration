#!/usr/bin/env python3


class Command():
    
    def __init__(self, devobj):
        self.vendor = devobj.vendor
        self.ip_mgmt = devobj.ip_mgmt
        self.name = devobj.name

class Command_IOS(Command):

    def __init__(self, devobj):
        super().__init__(devobj)

    def basic_config():
        lst_commands = [
            "conf t",
            ""
        ]


def create_basic_config(devobj):
    if devobj.vendor == "IOS":
        dev = Command_IOS(devobj)
        return dev.basic_config()


def main():
    pass

if __name__ == "__main__":
    main()