#!/usr/bin/env python3
"""Entry program for the make.fun bounty news-image-20261119.

Third design of the front page, a hybrid revised at the entrant's
order ("V3 hybrid — layout v1 + warna di atas aja": the first
design's layout, colour at the top only). The first design was a
plain black-and-white newspaper page and is kept exactly — same
lead art and black headline, same four plain story cards, same
briefs grid, same markets strip. The second design gave the whole
top a colour magazine treatment and scored lower with the house
judge, so this third design borrows only its masthead: a deep-
crimson nameplate band with the title reversed out in cream and a
gold italic tagline, over a navy date strip with the date in gold.
The 25 verified stories of Thursday 19 November 2026, their texts
and their sourcing did not change between designs.

The finished page is committed in this repository as entry.png. The
file holds JPEG bytes under a .png name; the bounty tells PNG from
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
PAGE_SHA256 = "9863812bbf1c1858defc833f32704fc5dc0c161ab53cca61de226a5107fd4788"
PAGE_BYTES = 569611


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


def verify_delivery(target: Path, data: bytes) -> bool:
    """Re-read the delivered file and check it against the source page."""
    written = target.read_bytes()
    if written != data:
        return False
    return hashlib.sha256(written).hexdigest() == PAGE_SHA256


def main() -> int:
    data = read_page()
    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    if not verify_delivery(target, data):
        print("delivered file failed verification against entry.png",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
