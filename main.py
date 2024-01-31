#!/usr/bin/env python3

from gns_data import get_json_files, show_in_file
from my_system import Device, create_system, Network
from connection import get_gns3_projects, upload_basic_config
from time import sleep


def prompt_menu():
    options_lst = [
        "Show projects from gns3 server.",
        "Set project.",
        "Execute script.",
        "Exit."
    ]

    print("\n")
    print("#" * 26)
    print("#" * 10, "MENU", "#" * 10, "\n")

    for i, opt in enumerate(options_lst, start = 1):
        print(f"# {i}) {opt}")

    chose = input("# Chose option: ")

    return chose


def show_projects():
    project_lst = get_gns3_projects()

    print("\n")
    print("#" * 4, "Project list:")

    for i, name in enumerate(project_lst, start = 1):
        tmp_name = name[0].removesuffix(".gns3")
        print(f"# {i:02}) {tmp_name}")
    
    chose = input("# Click any charakter for back to menu...")

    return project_lst


def set_project():
    print("\n")
    selected_project = input("# Enter project name or number: ")

    return selected_project


def execute_script(selected_project, project_lst):
    if selected_project == None:
        print("You need to select project...")
        return
    if project_lst == None:
        project_lst = get_gns3_projects()

    


def main():

    selected_project = None
    project_lst = None

    while True:
        chose = prompt_menu()

        if chose == "1":
            show_projects()

        elif chose == "2":
            selected_project = set_project()

        elif chose == "3":
            execute_script(selected_project, project_lst)

        elif chose == "4":
            print("Exiting...")
            exit()

        else: 
            print("You need to pick valid option...")
            sleep(1)

        print(selected_project)



    # print(show_gns3_projects())
    # ## Get info about links and nodes in lab.
    # path = "gns3_file/automation_test2.gns3"
    # dct_nodes, dct_links = get_json_files(path)
    # # show_in_file(dct_nodes, "file/dct_nodes2.json")
    # # show_in_file(dct_links, "file/dct_links2.json")

    # ## Create device with information from lab.
    # create_system(dct_nodes, dct_links)

    # print("\n")
    # print("#" * 20)
    # print("\n")

    # for dev in Device.dev_lst:
    #     print(dev.name)
    #     upload_basic_config(dev)
    #     print("\n")
    #     print("#" * 20)
    #     print("\n")
    # pass


if __name__ == "__main__":
    main()