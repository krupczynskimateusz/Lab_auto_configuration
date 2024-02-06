#!/usr/bin/env python3

import json





## Only for debug purpose.
def show_in_file(dct: dict, path: str):
    from pathlib import Path
    with open(path, "w") as f:
        f.write(json.dumps(dct, indent = 4))
    my_file = Path(path)


if __name__ == "__main__":
    pass