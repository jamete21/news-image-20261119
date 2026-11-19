#!/usr/bin/env python3
"""Deliver entry.png to /output/entry.png, byte for byte.

Standard library only, no network. The program reads the image that sits
next to this file, checks it against the competition's limits (whole PNG,
at most 1 MiB), copies it to /output/entry.png, then reads the copy back
and proves it is identical by comparing both the bytes and the SHA-256.
"""
import hashlib
import os
import sys

MAX_BYTES = 1048576  # 1 MiB, the competition's cap for the image
WANT_WIDTH, WANT_HEIGHT = 1024, 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

SOURCE_NAME = "entry.png"
DEST_DIR = "/output"
DEST_NAME = "entry.png"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def digest(data):
    return hashlib.sha256(data).hexdigest()


def png_dimensions(payload):
    """Return (width, height) from the PNG IHDR chunk, or None."""
    if len(payload) < 24 or not payload.startswith(PNG_SIGNATURE):
        return None
    width = int.from_bytes(payload[16:20], "big")
    height = int.from_bytes(payload[20:24], "big")
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(here, SOURCE_NAME)
    dest_path = os.path.join(DEST_DIR, DEST_NAME)

    if not os.path.isfile(source_path):
        return fail(f"source not found: {source_path}")

    with open(source_path, "rb") as handle:
        payload = handle.read()

    if len(payload) > MAX_BYTES:
        return fail(f"{SOURCE_NAME} is {len(payload)} bytes, over the "
                    f"{MAX_BYTES} byte cap")

    dimensions = png_dimensions(payload)
    if dimensions is None:
        return fail(f"{SOURCE_NAME} is not a PNG file")
    if dimensions != (WANT_WIDTH, WANT_HEIGHT):
        return fail(f"{SOURCE_NAME} is {dimensions[0]}x{dimensions[1]}, "
                    f"want {WANT_WIDTH}x{WANT_HEIGHT}")

    source_sha = digest(payload)

    os.makedirs(DEST_DIR, exist_ok=True)
    with open(dest_path, "wb") as handle:
        handle.write(payload)

    with open(dest_path, "rb") as handle:
        written = handle.read()

    if written != payload:
        return fail("copy differs from the source")
    if digest(written) != source_sha:
        return fail("copy sha256 differs from the source")

    print(f"copied {source_path} -> {dest_path}")
    print(f"dimensions: {dimensions[0]}x{dimensions[1]}")
    print(f"bytes: {len(payload)}")
    print(f"sha256: {source_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
