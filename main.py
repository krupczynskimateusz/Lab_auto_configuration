#!/usr/bin/env python3

from gns_data import get_json_files
from other import nice_print, show_in_file
from my_system import Device, create_devObj
import time



def main():
    
    ## Get info about links and nodes in lab.
    path = "63e3307d-e2c5-499e-a5b7-ddac641770af/network_automation.gns3"
    dct_nodes, dct_links = get_json_files(path)

    ## Create device with information from lab.
    lst_devObj = create_devObj(dct_nodes)

    # ## Some debug
    # for node in lst_devObj:
    #     print(node.dev_id)
    #     print(node.ip_mgmt)
    #     print(node.vendor)
    # print(Device.show_used_addresses())
    # print(Device.show_free_addresses())

    

    


if __name__ == "__main__":
    main()