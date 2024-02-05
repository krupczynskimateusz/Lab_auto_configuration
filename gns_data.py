#!/usr/bin/env python3

import json


## Getting lab config from .gns3 file.
def get_json_files(path):
    with open(path) as f:
        dct_file = json.load(f)

    ## Delete usles information and free memory.
    dct_links = dct_file["topology"]["links"] 
    dct_nodes = dct_file["topology"]["nodes"]
    del dct_file

    ## Pull info
    links_fin = get_links_info(dct_links)
    nodes_fin = get_nodes_info(dct_nodes)

    return nodes_fin, links_fin


## Get needed link info from links dct.
def get_links_info(links):
    links_info = []     ## tmp connection lst.
    for link in links:
        connection = []
        for node in link["nodes"]:
            id = node["node_id"]
            int_name = node["label"]["text"]
            connection.append((id, int_name))
        connection_tp = tuple(connection)
        links_info.append(connection_tp)
    return links_info


## Get needed node info from nodes dct.
def get_nodes_info(nodes):
    nodes_info = []

    for node in nodes:
        gns_id = node["node_id"]
        console_port = node["console"]
        node_name = node["name"]

        if "hda_disk_image" in node["properties"].keys():
            if "vios-adventerprisek9" in node["properties"]["hda_disk_image"]:
                vendor = "vIOS"

        elif "image" in node["properties"].keys():
            if "c7200-adventerprisek9-mz" in node["properties"]["image"]:
                vendor = "C7200"

        elif "ethernet_switch" in node["node_type"]:
            vendor = "gns_switch"
            
        else:
            vendor = None

        tmp_tuple = (gns_id, console_port, node_name, vendor)
        nodes_info.append(tmp_tuple)

    return nodes_info


## Only for debug purpose.
def show_in_file(dct: dict, path: str):
    from pathlib import Path
    with open(path, "w") as f:
        f.write(json.dumps(dct, indent = 4))
    my_file = Path(path)


def main():
    pass

if __name__ == "__main__":
    main()