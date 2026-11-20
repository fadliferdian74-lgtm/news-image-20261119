#!/usr/bin/env python3
"""Entry program for the make.fun bounty news-image-20261119.

The finished front page is committed in this repository as entry.png.
The file holds JPEG bytes under a .png name; the bounty tells PNG from
JPEG by the first bytes, so this is exactly what its rules allow.
Running this program delivers that page, byte for byte, to the output
location the grader uses: $MAKEFUN_OUTPUT_DIR/entry.png when the
variable is set, /output/entry.png otherwise.

Before writing, the program checks the committed page against the
sha256 recorded below, so a corrupted or swapped image fails loudly
instead of being delivered. Standard library only, no network, no
randomness and no clock: the repository file never changes, so two
runs always write two identical files, as the bounty requires.
"""

import hashlib
import os
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
PAGE_FILE = REPO_DIR / "entry.png"
PAGE_SHA256 = "e6bef01aa729f411f89d32403f971cdeca6d924edd4e632f525963ad5d263764"
PAGE_BYTES = 567425


def output_path() -> Path:
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip() or "/output"
    return Path(folder) / "entry.png"


def read_page() -> bytes:
    data = PAGE_FILE.read_bytes()
    if len(data) != PAGE_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, expected {PAGE_BYTES}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != PAGE_SHA256:
        raise SystemExit(f"entry.png sha256 is {digest}, expected {PAGE_SHA256}")
    return data


def main() -> int:
    data = read_page()
    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    if target.read_bytes() != data:
        print("delivered file differs from entry.png", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
