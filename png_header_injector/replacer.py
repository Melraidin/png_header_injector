import zlib


ENCODING = "iso-8859-1"


def replace_text(in_png, out_png, text):
    """
    Replace text chunks without re-encoding image.

    Replaces the text chunks in the given PNG with new values or
    removes them entirely. Does not remove unspecified keywords.

    Args:
        in_png: Input PNG file object.
        out_png: Output PNG file object.
        text: Dict of text keyword chunks to be replaced/removed. If
            the value is None the chunk will be removed (if present).
    """

    # Magic number.
    out_png.write(in_png.read(8))

    copy_ihdr(out_png, in_png)

    remove_keywords = set()
    for keyword, value in text.items():
        write_text(out_png, keyword, value)
        remove_keywords.add((keyword + "\0").encode(ENCODING))

    while True:
        raw_chunk_size = in_png.read(4)
        if len(raw_chunk_size) == 0:
            break
        chunk_size = int.from_bytes(raw_chunk_size, byteorder="big")

        chunk_type = in_png.read(4)
        if chunk_type != "tEXt".encode(ENCODING):
            copy_chunk_remainder(out_png, in_png, chunk_size, chunk_type)
            continue

        chunk_data = in_png.read(chunk_size)
        for encoded_keyword in remove_keywords:
            if chunk_data.startswith(encoded_keyword):
                # Read past our CRC and we're done with this
                # text chunk we don't want to copy.
                in_png.seek(4, whence=1)
                break
        else:
            # Write the unspecified text chunk and its CRC.
            out_png.write(raw_chunk_size)
            out_png.write(chunk_type)
            out_png.write(chunk_data)
            out_png.write(in_png.read(4))


def copy_chunk_remainder(out, png, chunk_size, chunk_type):
    """
    Copy the remainder of a chunk.

    Args:
        out: Target PNG file object.
        png: Input PNG file object.
        chunk_size: Size of chunk to copy.
        chunk_type: Type of chunk.
    """

    out.write(chunk_size.to_bytes(4, byteorder="big"))
    out.write(chunk_type)

    # Add the 4-byte CRC.
    out.write(png.read(chunk_size + 4))


def copy_ihdr(out, png):
    """
    Copies IHDR chunk.

    Args:
        out: Target PNG file object.
        png: Input PNG file object.
    """

    # IHDR chunk.
    ihdr_size = int.from_bytes(png.read(4), byteorder="big")
    out.write(ihdr_size.to_bytes(4, byteorder="big"))

    # IHDR chunk type.
    out.write(png.read(4))

    # IHDR data block.
    out.write(png.read(ihdr_size))

    # IHDR CRC.
    out.write(png.read(4))


def write_text(out, keyword, value):
    """
    Writes a text chunk.

    Args:
        out: Target PNG file object.
        keyword: Text keyword.
        values: Text value.
    """

    data_block = (keyword + "\0" + value).encode(ENCODING)
    out.write(len(data_block).to_bytes(4, byteorder="big"))
    type_block = "tEXt".encode(ENCODING)
    out.write(type_block)
    out.write(data_block)
    out.write((zlib.crc32(type_block + data_block) & 0xffffffff).to_bytes(4, byteorder="big"))
