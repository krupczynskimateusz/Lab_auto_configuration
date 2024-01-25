#!/usr/bin/env python3



class Command():


    def __init__(self, devobj):
        self.vendor = devobj.vendor
        self.ip_mgmt = devobj.ip_mgmt
        self.name = devobj.name
        self.network = devobj.network



class Command_IOS(Command):


    def __init__(self, devobj):
        super().__init__(devobj)


    def basic_config(self):
        lst_commands = [
            "conf t",
            f"hostname {self.name}",
            "ip domain name lab.home",
            "end"
        ]
        return lst_commands


    def ssh_config(self):
        lst_commands = [
            "conf t",
            "crypto key generate rsa",
            ["2048", 8],
            "ip ssh version 2"
            "end"
        ]
        return lst_commands
    



def create_basic_config(devobj):
    if devobj.vendor == "vIOS":
        dev = Command_IOS(devobj)
        return dev



def main():
    pass

if __name__ == "__main__":
    main()