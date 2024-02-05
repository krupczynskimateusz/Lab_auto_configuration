#!/usr/bin/env python3

import my_system 
from time import sleep


def main():
    menu = my_system.My_Menu()

    while True:
        menu.get_lab_info("gns3_file/automation_test2.gns3")
        menu.create_system()
        sleep(1)
        


if __name__ == "__main__":
    main()