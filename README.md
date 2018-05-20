Python PNG Header Injector
==========================

Provides a method of adding, replacing, and removing PNG text headers
(TEXT chunks) without re-encoding the image data (IDAT chunks).


Compatiblity
============

Tested successfully with Python 2.7 and Python 3.6.


Performance
===========

A simple benchmark that performs similar operations using
png_header_injector and Pillow. With png_header_injector a comment is
added while removing any existing comments in the image and keeping
all other TEXT chunks. With Pillow all existing TEXT chunks are
removed and a comment is added.

```
$ python benchmark.py test.png
Pillow total time: 6.868 seconds.
Header injector total time: 0.016 seconds.
```


Installation
============

```
pip install png_header_injector
```


Usage
=====

```
import png_header_injector
with open("input.png", "rb") as input_png:
	with open("output.png", "wb") as output_png:
		png_header_injector.replace_text(
			input_png,
			output_png,
			{"Comment": "Processed with png_header_injector"})
```


Specifying a key (used as the TEXT chunk's keyword) in the
`replace_text()` dictionary will cause any existing TEXT chunks in the
file with that keyword to be removed and one new TEXT chunk with your
value added.

Specifying a key with its value as None will cause any existing
instances of TEXT chunks with the given keyword being removed and no
new TEXT chunk being added.
