#!/usr/bin/env python3

from time import sleep



def show_menu():
    tmp = 0 
    while tmp < 10:
        print(f"""{"#" * 20}
Auto konfiguration menu:

{"#" * 20}
""")



        tmp += 1


def main():
    show_menu()


if __name__ == "__main__":
    main()