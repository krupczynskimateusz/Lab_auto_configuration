#!/usr/bin/env python3

import my_devices
import connection
from gns_data import get_topology
from time import sleep


gns_server_ip = "gns3.home"


def init_system():
    set_Telnet_ip = "gns3.home"
    lab = connection.get_lab_conn("GNS3", gns_server_ip)
    return lab


class My_Menu():

    _system = False
    _selected_project = None
    _project_lst = None
    _lab = init_system()
    _options_lst = [
        "Show projects from gns3 server.",
        "Set project.",
        "Execute script.",
        "Exit."
    ]


    def __init__(self):
        pass


    @classmethod
    def show_menu(cls):
        print("\n")
        print("#" * 10, "MENU", "#" * 10, "\n")

        for i, opt in enumerate(cls._options_lst, start = 1):
            print(f"# {i}) {opt}")

        chose = input("# Chose option: ")

        if chose == "1":
            cls.show_projects()

        elif chose == "2":
            cls._selected_project = cls.set_project()

        elif chose == "3":
            cls.execute_script()
            sleep(1)

        elif chose == "4":
            print("Exiting...")
            exit()

        else: 
            print("You need to pick valid option...")
            sleep(1)


    @classmethod
    def show_projects(cls):

        _project_lst = connection.et_gns3_projects(cls._lab)

        print("\n")
        print("#" * 4, "Project list:")

        for i, name in enumerate(_project_lst, start = 1):
            tmp_name = name[0].removesuffix(".gns3")
            print(f"# {i:02}) {tmp_name}")
            
        print("\n")
        chose = input("Click any charakter for back to menu...")

        return


    @classmethod
    def set_project(cls):
        print("\n")
        print("#" * 26, "\n")
        cls._selected_project = input("# Enter project name or number: ")
        try:
            cls._selected_project = ("number", int(cls.show_projects_selected_project))
            return cls._selected_project
        except:
            cls_selected_project = ("string", cls._selected_project)
            return cls._selected_project


    @classmethod
    def execute_script(
            cls,
            path: str = "/tmp/gns3_project.gns3"
            ):
        if cls._selected_project == None:
            return print("You need to select project...")
        
        if cls._project_lst == None:
            cls._project_lst = connection.get_gns3_projects(cls._lab)

        if cls._selected_project[0] == "string":
            for project in cls._project_lst:
                if cls._selected_project[1] in project[0]:
                    project_to_download = project

        elif cls._sselected_project[0] == "number":
            _project_to_download = cls._sproject_lst[cls._sselected_project[1] - 1]

        else:
            print("Error with selected_project ocur....")
            exit()

        project_path = connection.get_project(
            cls._lab,
            _project_to_download,
            path
            )

        if not project_path:
            return False
        
        else:
            cls.get_lab_info(project_path)
            cls.create_system()
            # show_in_file(dct_nodes, "file/dct_nodes_new.json")
            # show_in_file(dct_links, "file/dct_links_new.json")

            for dev in my_devices.Node.dev_lst:
                print(f"# Start {dev.name}...")
                connection.upload_basic_config(dev)

    @classmethod
    def get_lab_info(cls, project_path: str):
        cls.dct_nodes, cls.dct_links = get_topology(project_path)

    @classmethod
    def create_system(cls):
        if cls._system == False:
            network_obj = my_devices.Network(cls.dct_links)

            for node in cls.dct_nodes:
                network = network_obj.my_links(node[0])
                gns_id = node[0]
                console_port = node[1]
                name = node[2]
                
                if "vIOS" == node[3]:
                    my_devices.IOS(
                        network,
                        gns_id,
                        name,
                        console_port,
                        cls._lab.host)

                elif "C7200" == node[3]:
                    my_devices.C7200(
                        network,
                        gns_id,
                        name,
                        console_port,
                        cls._lab.host
                        )
                
                elif "gns_switch" == node[3]:
                    my_devices.GNS_Switch(
                        network,
                        gns_id,
                        name,
                        console_port
                        )

                else:
                    my_devices.Node(
                        network,
                        gns_id,
                        name,
                        console_port
                        )
            cls._system = True
        else:
            print("System created.")
        return 



if __name__ == "__main__":
    pass