#!/usr/bin/env python3

import my_system


def main():
    menu = my_system.Menu()

    while True:
        menu.show_menu()


if __name__ == "__main__":
    main()