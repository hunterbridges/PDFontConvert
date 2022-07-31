#!/usr/bin/python3
#
# NOTE This script requires the `bdfparser` and `pillow` pip packages
#      It also assumes the `otf2bdf` utility is installed

# pip install pypng
# pip install pillow
# pip install bdfparser

import base64
import math
import png
import re
import subprocess
import os
from bdfparser import Font
from PIL import Image
from io import BytesIO
from pathlib import Path

def access_bit(data, num):
    base = int(num // 8)
    shift = 7 - int(num % 8)
    return (data[base] >> shift) & 0x1

p = Path('.')
for font_path in p.glob('ttf/*.ttf'):
    font_name = font_path.stem

    # Detect font pixel size
    px_re = re.search('\d+', font_name)
    px_size = px_re.group(0)
    if px_size is None:
        print(f"\tUnable to detect font size from file name '{font_name}'")
        continue

    # Convert to point size
    px_size = int(px_size)
    pt_size = int(math.floor(px_size * 3 / 4))
    print(f"{font_name}.ttf ({px_size} px -> {pt_size} pt)")

    # Use otf2bdf to convert to bdf
    print("\tConverting to BDF...")
    bdf_path = f"bdf/{font_name}.bdf"
    args = ['otf2bdf', '-p', f"{pt_size}", '-o', bdf_path, str(font_path)];
    print(f"\t{' '.join(args)}")
    rc = subprocess.run(args)
    if os.path.isfile(bdf_path) == False or os.stat(bdf_path).st_size == 0:
        print("\tError converting font!")
        if rc.stderr is not None:
            print(rc.stderr)
        if rc.stdout is not None:
            print(rc.stdout)
        continue
    
    # Attempt to load the BDF
    font = None
    try:
        font = Font(str(bdf_path))
    except:
        print("\tError loading converted font!")
        continue
        
    print(f"\t{font_name} ({font.headers['fbbx']} x {font.headers['fbby']}, {len(font)} glyphs)")

    # Create output dirs if needed
    out_dirs = ['png', 'fnt']
    for out_dir in out_dirs:
        if os.path.exists(out_dir) is False:
            os.makedirs(out_dir)

    # TODO In a production deployment, you would likely
    #      want to ingest your localized strings files
    #      and create a filtered glyph set.
    #
    #      Then, instead of using `font.drawall`, use
    #      `font.draw` with the filtered character set.
    #
    #      Once you do that, when you write the .fnt,
    #      make sure to only write the desired glyphs
    #      in the `font.iterglyphs` loop.

    # Write the PNG image
    font_preview = font.drawall()
    png_pal = png.Reader(filename="pd_palette.png")
    png_pal.preamble()
    png_out = png.Writer(
        width=font_preview.width(),
        height=font_preview.height(),
        bitdepth=1,
        palette=png_pal.palette()
    )
    px_bytes = font_preview.tobytes('1')
    px_byte_arr = [access_bit(px_bytes,i) for i in range(len(px_bytes)*8)]
    png_filename = "png/%s.png" % (font_name)
    png_file = open(png_filename, 'wb')
    buffered = BytesIO()
    png_out.write_array(buffered, px_byte_arr)
    png_out.write_array(png_file, px_byte_arr)
    png_file.close()
    img_str = base64.b64encode(buffered.getvalue())

    # Write the FNT
    print(f"\tWriting out/{font_name}.fnt...")
    with open("fnt/%s.fnt" % (font_name), 'w', encoding='utf-8') as f:
        f.write("datalen=%d\n" % (len(img_str)))
        f.write("data=%s\n" % (img_str.decode('utf8')))
        f.write("width=%d\n" % (font.headers['fbbx']))
        f.write("height=%d\n" % (font.headers['fbby']))

        for glyph in font.iterglyphs(order=1 ,r=(0, 0x3FFFF)):
            g_width = glyph.meta['dwx0']
            if glyph.chr() == ' ':
                f.write("space\t%d\n" % (g_width))
            else:
                f.write("%s\t%d\n" % (glyph.chr(), g_width))
