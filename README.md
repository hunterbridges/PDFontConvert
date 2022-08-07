# PDFontConvert

TTF -> BDF -> FNT batch UTF8 font conversion utility for Playdate
by [@HunterBridges](https://twitter.com/HunterBridges)

## Overview

This is a utility to help convert UTF8 TTF fonts into the Playdate
proprietary FNT format.

## Requirements

First, you need to install these dependencies:

* Python 3
* `pip install bdfparser`
* `pip install pillow`
* `pip install pypng`

Then you need to build the `submodules/otf2bdf` submodule from source.
This utility uses a custom fork which permits conversion using the
raw bitmap strike data in the font.

## How to use

`cd` to the repo root directory and run `python3 font_convert.py`

The script scans all TTF files in the `ttf` directory, and attempts
the conversion process for each found TTF file.

Then, it converts the TTF to BDF with `otf2bdf`, using the first
available bitmap strike in each TTF.

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
