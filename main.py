#!/usr/bin/env python3

from objects import Config_Load, My_Menu 

def main():

    Config_Load()
    menu = My_Menu()

    while True:
        menu.show_main_menu()

if __name__ == "__main__":
    main()