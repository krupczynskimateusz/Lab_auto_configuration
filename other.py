#!/usr/bin/env python3

import json

## Only for debug purpose.
def nice_print(*x):
    for element in x:
        print(json.dumps(element, indent = 4))

## Only for debug purpose.
def show_in_file(dct: dict, file: str):
    with open(file, "w") as f:
        f.write(json.dumps(dct, indent = 4))
    with open("all_info.json", "a") as f:
        f.write(json.dumps(dct, indent = 4))

def main():
    pass

if __name__ == "__main__":
    main()