#!/usr/bin/env python3

from gns_data import get_json_files, show_in_file
from my_system import Device, create_system, Network
from connection import GNS3_Conn, get_gns3_projects, upload_basic_config, prepare_project
from time import sleep


def init():
    GNSServer = GNS3_Conn()
    return GNSServer


def prompt_menu():
    options_lst = [
        "Show projects from gns3 server.",
        "Set project.",
        "Execute script.",
        "Exit."
    ]

    print("\n")
    print("#" * 10, "MENU", "#" * 10, "\n")

    for i, opt in enumerate(options_lst, start = 1):
        print(f"# {i}) {opt}")

    chose = input("# Chose option: ")

    return chose


def show_projects(GNSServer):
    project_lst = get_gns3_projects(GNSServer)

    print("\n")
    print("#" * 4, "Project list:")

    for i, name in enumerate(project_lst, start = 1):
        tmp_name = name[0].removesuffix(".gns3")
        print(f"# {i:02}) {tmp_name}")
        
    print("\n")
    chose = input("Click any charakter for back to menu...")

    return project_lst


def set_project():
    print("\n")
    print("#" * 26, "\n")
    selected_project = input("# Enter project name or number: ")
    try:
        selected_project = ("number", int(selected_project))
        return selected_project
    except:
        selected_project = ("string", selected_project)
        return selected_project


def execute_script(
        GNSServer: object,
        selected_project: str,
        project_lst: list,
        path: str = "/tmp/gns3_project.gns3"
        ):
    if selected_project == None:
        return print("You need to select project...")
    
    if project_lst == None:
        project_lst = get_gns3_projects(GNSServer)

    if selected_project[0] == "string":
        for project in project_lst:
            if selected_project[1] in project[0]:
                project_to_download = project

    elif selected_project[0] == "number":
        project_to_download = project_lst[selected_project[1] - 1]

    else:
        print("Error with selected_project ocur....")
        exit()

    project_path = prepare_project(GNSServer, project_to_download, path)
    print(project_path)
    if not project_path:
        return False
    else:
        dct_nodes, dct_links = get_json_files(project_path)
        create_system(dct_nodes, dct_links)
        # show_in_file(dct_nodes, "file/dct_nodes_new.json")
        # show_in_file(dct_links, "file/dct_links_new.json")

        for dev in Device.dev_lst:
            print(f"# Start {dev.name}...")
            upload_basic_config(dev)



def main():

    selected_project = ("number", 1)
    project_lst = None
    GNSServer = init()

    while True:
        chose = prompt_menu()

        if chose == "1":
            show_projects(GNSServer)

        elif chose == "2":
            selected_project = set_project()

        elif chose == "3":
            execute_script(GNSServer, selected_project, project_lst)
            sleep(1)

        elif chose == "4":
            print("Exiting...")
            exit()

        else: 
            print("You need to pick valid option...")
            sleep(1)


if __name__ == "__main__":
    main()