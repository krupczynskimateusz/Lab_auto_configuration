#!/usr/bin/env python3

from configparser import ConfigParser



def main():
    config = ConfigParser()
    config.read("config.ini")


    if len(config) == 1:
        print("Can't load config file. Be sure that it name is 'config.ini'.")
        exit()



if __name__ == "__main__":
    main()