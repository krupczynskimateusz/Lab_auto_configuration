#!/usr/bin/env python3

from gns_data import get_json_files
from other import nice_print, show_in_file
from my_system import create_devObj
import time

def main():
    
    ## Get info about links and nodes in lab.
    path = "63e3307d-e2c5-499e-a5b7-ddac641770af/network_automation.gns3"
    dct_nodes, dct_links = get_json_files(path)

    print(dct_nodes[0][0], dct_nodes[0][1])
    ## Create device with information from lab.

    start = time.time()
    lst = create_devObj(dct_nodes)
    end = time.time()
    print(f"{round((end - start), 2)} secends")
    print(lst[0].ip_mgmt)


if __name__ == "__main__":
    main()