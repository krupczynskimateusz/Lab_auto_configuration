#!/usr/bin/env python3

from gns_data import get_json_files, show_in_file
from other import nice_print
from my_system import Device, create_devObj
from connection import basic_config, Telnet_Conn
import time



def main():
    
    ## Get info about links and nodes in lab.
    path = "gns3_file/network_automation.gns3"
    dct_nodes, dct_links = get_json_files(path)
    
    path1 = "file/dct_nodes.json"
    path2 = "file/dct_links.json"

    show_in_file(dct_nodes, path1)
    show_in_file(dct_links, path2)

    ## Create device with information from lab.
    lst_devObj = create_devObj(dct_nodes)

    # ## Some debug
    # for node in lst_devObj:
    #     print(node.dev_id)
    #     print(node.ip_mgmt)
    #     print(node.vendor)
    # print(Device.show_used_addresses())
    # print(Device.show_free_addresses())
    # print(lst_devObj[0].console_port)
    # print(lst_devObj[0].name)

    # basic_config(lst_devObj[0])
    


if __name__ == "__main__":
    main()