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
    for conn_id, link in enumerate(links, start = 1):
        connection = [conn_id]
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
        if "Switch" in node["name"]:
            pass
        elif node["console"] == None:
            pass
        else:
            gns_id = node["node_id"]
            console_port = node["console"]
            node_name = node["name"]
            tmp_tuple = (gns_id, console_port, node_name)
            dev_id = id(tmp_tuple)
            nodes_info.append((dev_id, tmp_tuple))
    return nodes_info


## Only for debug purpose.
def show_in_file(dct: dict, file: str):
    with open(file, "w") as f:
        f.write(json.dumps(dct, indent = 4))
    with open("all_info.json", "a") as f:
        f.write(json.dumps(dct, indent = 4))


def main():
    pass

if __name__ == "__main__":
    main()