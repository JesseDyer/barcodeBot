#!/usr/bin/env python3

""" Barcode Builder - trying to get the bot showing images.

Handy Links:
    https://github.com/JesseDyer/barcodeBot - This Library
    https://pillow.readthedocs.io/en/stable/handbook/tutorial.html - Manipulating Images
    https://www.waveshare.com/wiki/2.9inch_e-Paper_Module - My Display
    https://python-barcode.readthedocs.io/en/stable/writers/index.html - Barcode Library
"""

import barcode
from barcode.writer import ImageWriter
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
import logging
from waveshare_epd import epd2in9
import time
from time import sleep
from PIL import Image,ImageDraw,ImageFont, ImageOps
import PIL
import traceback


logging.basicConfig(level=logging.INFO)
epd = epd2in9.EPD()
logging.info("init and Clear")
epd.init(epd.lut_full_update)
epd.Clear(0xFF)

font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

def createCode128(sku):
    #45x120 mill?
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

def displayImage(file):
    # epd.init(epd.lut_full_update)
    # epd.Clear(0xFF)
    logging.info("read bmp file")
    Himage = Image.open(file)
    epd.display(epd.getbuffer(Himage))
    
def rotateImage(file):
    im1=Image.open(file, 'r')
    im1 =im1.rotate(90, PIL.Image.NEAREST, expand=1)
    im1 = im1.convert('1')
    im1 = ImageOps.pad(im1, (128, 296), color='white')
    im1.save(file)

def showCode(code):
    file=createCode128(code)
    rotateImage(file)
    displayImage(file)

for x in range(1000, 2000):
    showCode(str(x).zfill(12))
    sleep(5)




