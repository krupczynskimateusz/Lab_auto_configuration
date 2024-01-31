#!/usr/bin/env python3

from gns_data import get_json_files, show_in_file
from other import nice_print
from my_system import Device, create_system, Network
from connection import gns3_projects, upload_basic_config



def main():
    
    ## Get info about links and nodes in lab.
    path = "gns3_file/automation_test2.gns3"
    dct_nodes, dct_links = get_json_files(path)
    # show_in_file(dct_nodes, "file/dct_nodes2.json")
    # show_in_file(dct_links, "file/dct_links2.json")

    ## Create device with information from lab.
    create_system(dct_nodes, dct_links)

    print("\n")
    print("#" * 20)
    print("\n")

    for dev in Device.dev_lst:
        print(dev.name)
        upload_basic_config(dev)
        print("\n")
        print("#" * 20)
        print("\n")
    pass


if __name__ == "__main__":
    main()