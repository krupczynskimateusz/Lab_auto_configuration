#!/usr/bin/env python3

from time import sleep



def show_menu():
    tmp = 0 
    option_lst = ["Start", "Chose path to lab configuration.", "Chose option to konfiguration.", "Enter configuration for managment network.", "Exit"]
    while tmp < 2:
        print("#" * 20)
        print("KONFIGURATION MENU")
        for index, option in enumerate(option_lst, start = 1):
            print(f"{index:02}. {option}")
        chosed_option = input("Chose option number: ")
        if chosed_option == ""
        tmp += 1


def main():
    show_menu()


if __name__ == "__main__":
    main()