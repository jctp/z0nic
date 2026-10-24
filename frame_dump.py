# Temp AI-generated shim for testing

import struct
import zlib


def _chunk(chunk_type, data):
    crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)


def write_png(path, rows):
    height = len(rows)
    width = len(rows[0])

    raw = bytearray()
    for row in rows:
        raw.append(0)  # filter type: none
        for red, green, blue in row:
            raw.extend((red, green, blue))

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", header)
        + _chunk(b"IDAT", zlib.compress(bytes(raw)))
        + _chunk(b"IEND", b"")
    )

    with open(path, "wb") as file:
        file.write(png)
