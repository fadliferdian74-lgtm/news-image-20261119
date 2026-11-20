#!/usr/bin/env python3
"""Entry program for the make.fun bounty news-image-20261119.

Second design of the front page, revised at the entrant's order for a
colour magazine look ("atas kayak majalah" — the top like a magazine):
a colour magazine treatment of the same 25 verified stories of
Thursday 19 November 2026 — a deep-crimson nameplate band with the
title reversed out in cream, a navy date strip with the date in gold,
an oversized colour illustration of the Shenzhen summit spanning the
top width under the masthead, a crimson kicker bar and pull-quote
panel for the lead story, tinted story cards and a navy briefs
banner. The first design was a plain black-and-white newspaper page;
the stories, texts and sourcing did not change between designs.

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
PAGE_SHA256 = "962623924abf1ea33840949e5e00be65c4ccd754ea1ad5aa201c22c6f3f30b5f"
PAGE_BYTES = 514332


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
