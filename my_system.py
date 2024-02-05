#!/usr/bin/env python3

from my_devices import Network, Device, GNS_Switch, IOS, C7200
from connection import GNS3_Conn
from connection import get_gns3_projects
from connection import get_project
from gns_data import get_json_files
from time import sleep



def init_system():
    gns_server_ip = "gns3.home"
    lab = GNS3_Conn(gns_server_ip)
    return lab


class Menu():


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
    def show_projects(cls):

        _project_lst = get_gns3_projects(cls._lab)

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
            cls._project_lst = get_gns3_projects(cls._lab)

        if cls._selected_project[0] == "string":
            for project in cls._project_lst:
                if cls._selected_project[1] in project[0]:
                    project_to_download = project

        elif cls._sselected_project[0] == "number":
            _project_to_download = cls._sproject_lst[cls._sselected_project[1] - 1]

        else:
            print("Error with selected_project ocur....")
            exit()

        project_path = get_project(
            cls._lab,
            _project_to_download,
            path
            )

        if not project_path:
            return False
        
        else:
            from connection import upload_basic_config

            dct_nodes, dct_links = get_json_files(project_path)
            cls.create_system(dct_nodes, dct_links)
            # show_in_file(dct_nodes, "file/dct_nodes_new.json")
            # show_in_file(dct_links, "file/dct_links_new.json")

            for dev in Device.dev_lst:
                print(f"# Start {dev.name}...")
                upload_basic_config(dev)


    @staticmethod
    def create_system(dct_nodes, dct_links):

        network_obj = Network(dct_links)

        for dev in dct_nodes:
            network = network_obj.my_links(dev[0])
            gns_id = dev[0]
            console_port = dev[1]
            name = dev[2]
            
            if "vIOS" == dev[3]:
                IOS(network, gns_id, name, console_port)

            elif "C7200" == dev[3]:
                C7200(network, gns_id, name, console_port)
            
            elif "gns_switch" == dev[3]:
                GNS_Switch(network, gns_id, name, console_port)

            else:
                Device(network, gns_id, name, console_port)

        return 
    
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



if __name__ == "__main__":
    pass