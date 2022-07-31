# PDFontConvert

TTF -> BDF -> FNT batch UTF8 font conversion utility for Playdate
by [@HunterBridges](https://twitter.com/HunterBridges)

## Overview

This is a utility to help convert UTF8 TTF fonts into the Playdate
proprietary FNT format.

## Requirements

First, you need to install these dependencies:

* Python 3
* `otf2bdf` (Install via apt-get, brew, etc)
* `pip install bdfparser`
* `pip install pillow`
* `pip install pypng`

## How to use

`cd` to the repo root directory and run `python3 font_convert.py`

The script scans all TTF files in the `ttf` directory, and attempts
the conversion process for each found TTF file.

First, the conversion attempts to figure out the pixel-based line height
from the TTF file name. It does this with a simple regex, searching for the
first instance of `\d+` (One or more numeric digit characters) in the
file's basename.

It then converts the pixel size to a point size, using the conversion
`pt_size = int(math.floor(px_size * 3 / 4))`. Then, it converts
the TTF to BDF using `otf2bdf` using the derived point size.

From there, the script uses bdfparser to open the BDF font, and
renders out a PNG of all glyphs via Pillow. A copy of the PNG
is saved in the `png/` folder for verification. (Users may wish
to modify the script at this point to filter the character set
down based on a strings file)

Finally, the script writes out the FNT in the `fnt/` folder. The
PNG data is embedded into the FNT's `data=` section.

## Bundled Fonts

This utility comes bundled with several fonts from the [JFDotFont](http://jikasei.me/font/jf-dotfont/) and [KHDotFont](http://jikasei.me/font/kh-dotfont/) open font sets.

Processed FNT files from these sets can be found in the `fnt/` folder.

Font specimens can be previewed on their respective pages, or in the `png/` folder
of this repository.

## Acknowledgements

* Thanks to [@gingerbeardman](https://github.com/gingerbeardman) for pointing
  to the original set of resources in [this thread](https://devforum.play.date/t/japanese-pixel-fonts-with-kanji-support/1807)
* Information about the FNT format specification from [jaames/playdate-reverse-engineering](https://github.com/jaames/playdate-reverse-engineering)
* Acknowledgements and license information for the [JFDotFont](http://jikasei.me/font/jf-dotfont/)
  set can be found in `acknowledgements/jfdotfont`
* Acknowledgements and license information for the [KHDotFont](http://jikasei.me/font/kh-dotfont/)
  set can be found in `acknowledgements/khdotfont`
