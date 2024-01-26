#!/usr/bin/env python3

from gns_data import get_json_files, show_in_file
from other import nice_print
from my_system import Device, create_system, Network
from connection import upload_basic_config, Telnet_Conn
import time

## temporary
import commands



def main():
    
    ## Get info about links and nodes in lab.
    path = "gns3_file/automation_test.gns3"
    dct_nodes, dct_links = get_json_files(path)
    show_in_file(dct_nodes, "file/dct_nodes.json")
    show_in_file(dct_links, "file/dct_links.json")

    ## Create device with information from lab.
    create_system(dct_nodes, dct_links)


    for dev in Device.dev_lst:
        if dev.vendor != None:
            dev_conf = commands.create_config_obj(dev) ## -> connection.py
            print(dev_conf.basic_config())
            print(dev_conf.ssh_config())
            print(dev_conf.create_config_interface())
            print(dev_conf.create_ip_mgmt())
            print('\n' * 2)
        else:
            pass



if __name__ == "__main__":
    main()