#!/usr/bin/env python3

""" Barcode Builder - trying to get the bot showing images.

Handy Links:
    https://github.com/JesseDyer/barcodeBot - This Library
    https://pillow.readthedocs.io/en/stable/handbook/tutorial.html - Manipulating Images
    https://www.waveshare.com/wiki/2.9inch_e-Paper_Module - My Display
    https://python-barcode.readthedocs.io/en/stable/writers/index.html - Barcode Library

    TODO: If the code is UPC-A valid, use that.  If not, fall back to Code128
    TODO: Add threading
    TODO: Add Cherry Pi web interface
    TODO: Show IP address when Idle
    TODO: Tie it all together; when idle, show wireless state on boot.  Provide 
        web interface to set codes, interval, and paste box for codes.
"""

import barcode
from barcode.writer import ImageWriter
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
from waveshare_epd import epd2in9
from time import sleep
from PIL import Image,ImageDraw,ImageFont, ImageOps
import PIL




# Initialize the display.
epd = epd2in9.EPD()
epd.init(epd.lut_full_update)
epd.Clear(0xFF)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

def createCode128(sku):
    # write a flat file, BMP format, of the barcode.
    code128 = barcode.get('code128', sku, writer=ImageWriter())
    filename = code128.save('code128', 
        {"module_width":0.2,
        "module_height":4,
        "text_distance":2,
        "font_size":8,
        "dpi":250,
        "format":"BMP"
        })
    print(filename)
    return filename

def rotateImage(file):
    # Read the file in
    im1=Image.open(file, 'r')
    # Flip on it's side
    im1 =im1.rotate(90, PIL.Image.NEAREST, expand=1)
    # We have to be monochrome; convert to B&W
    im1 = im1.convert('1')
    # The image is a touch too big, the display has
    # to be 128 x 296 pixels or you end up with a 
    # blank display
    im1 = ImageOps.pad(im1, (128, 296), color='white')
    im1.save(file)

def displayImage(file):
    Himage = Image.open(file)
    epd.display(epd.getbuffer(Himage))


def showCode(code):
    file=createCode128(code)
    rotateImage(file)
    displayImage(file)

for x in range(1000, 2000):
    showCode(str(x).zfill(12))
    sleep(5)




