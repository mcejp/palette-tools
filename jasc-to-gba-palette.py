import argparse
from pathlib import Path

import numpy as np


def load_JASC(f):
    # check header and parse palette length
    assert next(f) == "JASC-PAL\n"
    assert next(f) == "0100\n"
    count = int(next(f))

    # parse entries
    colors = np.zeros((count, 3), dtype=np.uint8)
    for i in range(count):
        colors[i, :] = [int(chan) for chan in next(f).split(" ")]

    # this ought to be the end of the file
    assert not f.read()

    return colors


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", dest="output", type=Path, required=True)

    args = parser.parse_args()

    with open(args.input) as f:
        palette = load_JASC(f)

    with open(args.output, "wt") as f:
        f.write("static const COLOR palette[] = {\n")

        for r, g, b in palette:
            f.write(f"    RGB8({r:2d}, {g:2d}, {b:2d}),\n")

        f.write("};\n")
