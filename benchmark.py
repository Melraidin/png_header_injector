import io
import sys
import time

import PIL.Image
import png_header_injector


ITERATIONS = 32


def main(input_path):
    use_pil(input_path)

    use_header_injector(input_path)


def use_header_injector(input_path):
    start = time.time()

    for i in range(ITERATIONS):
        inject_comment(input_path)

    end = time.time()

    print(
        "Header injector total time: %0.3f seconds." % (end - start))


def inject_comment(input_path):
    with open(input_path, "rb") as png:
        out = io.BytesIO()
        png_header_injector.replace_text(
            png, out, {"Comment": "Test comment data."})


def use_pil(input_path):
    start = time.time()

    for i in range(ITERATIONS):
        with PIL.Image.open(input_path) as png:
            png_info = PIL.PngImagePlugin.PngInfo()
            png_info.add_text("Comment", "Test comment data.")
            out = io.BytesIO()
            png.save(out, format="PNG", pnginfo=png_info)

    end = time.time()

    print(
        "Pillow total time: %0.3f seconds." % (end - start))


if __name__ == "__main__":
    main(sys.argv[1])
