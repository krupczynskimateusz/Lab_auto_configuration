#!/usr/bin/env python3

from gns_data import get_json_files
from other import nice_print, show_in_file


def main():
    path = "63e3307d-e2c5-499e-a5b7-ddac641770af/network_automation.gns3"
    dct_nodes, dct_links = get_json_files(path)





    # print(dct_links)
    # nice_print(f"Links:\n{dct_links}\nNodes:\n{dct_nodes}")
    # show_in_file(dct_nodes, "nodes.json")
    # show_in_file(dct_links, "links.json")

if __name__ == "__main__":
    main()