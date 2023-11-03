import argparse
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


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
    parser.add_argument("--scale", type=int, required=True)

    args = parser.parse_args()

    with open(args.input) as f:
        palette = load_JASC(f)

    cols = min(len(palette), 16)            # max 16 columns
    rows = math.ceil(len(palette) / cols)

    S = args.scale
    img = Image.new("RGB", (cols * S, rows * S))
    draw = ImageDraw.Draw(img)

    for i, rgb in enumerate(palette):
        yy = i // cols
        xx = i % cols
        draw.rectangle((xx * S, yy * S, (xx + 1) * S, (yy + 1) * S), fill=tuple(rgb))

    img.save(args.output)
