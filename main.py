#!/usr/bin/env python3
"""news-image-20261121 entrypoint (pure standard library only).

The poster image is rendered at build time by draw_poster.py and committed
as entry.png. This program does exactly one thing: it copies entry.png from
the repository root to /output/entry.png, where the gate reads it. No
network, no image libraries, no other dependencies.

Run locally with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as err:
        print("cannot create output directory %s: %s" % (out_dir, err),
              file=sys.stderr)
        return 1
    dst = os.path.join(out_dir, "entry.png")
    try:
        shutil.copyfile(src, dst)
    except OSError as err:
        print("entry.png could not be copied from %s: %s" % (here, err),
              file=sys.stderr)
        return 1
    print("entry.png copied to %s" % dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
