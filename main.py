#!/usr/bin/env python3

from gns_data import get_json_files, show_in_file
from other import nice_print
from my_system import Device, create_system, Network
from connection import start_basic_config, Telnet_Conn
import time



def main():
    
    ## Get info about links and nodes in lab.
    path = "gns3_file/network_automation.gns3"
    dct_nodes, dct_links = get_json_files(path)
    # show_in_file(dct_nodes, "file/dct_nodes.json")
    # show_in_file(dct_links, "file/dct_links.json")

    ## Create device with information from lab.
    create_system(dct_nodes, dct_links)
    lst_devObj = Device.dev_lst

    print(lst_devObj[1].network)

    
    # start_basic_config(lst_devObj[0]) ## -> connection.py
    


if __name__ == "__main__":
    main()