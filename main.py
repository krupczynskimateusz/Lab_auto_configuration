#!/usr/bin/env python3

from objects import My_Menu


def main():
    menu = My_Menu()
    
    while True:
        menu.show_menu()

if __name__ == "__main__":
    main()