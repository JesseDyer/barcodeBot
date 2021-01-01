#!/usr/bin/env python3

""" Barcode Builder - trying to get the bot showing images.

Handy Links:
    https://github.com/JesseDyer/barcodeBot
        - This Library
    https://pillow.readthedocs.io/en/stable/handbook/tutorial.html
        - Manipulating Images
    https://www.waveshare.com/wiki/2.9inch_e-Paper_Module
        - My Display
    https://python-barcode.readthedocs.io/en/stable/writers/index.html
        - Barcode Library

    TODO: Add threading
    TODO: Add Cherry Pi web interface
    TODO: Show IP address when Idle
    TODO: Tie it all together; when idle, show wireless state on boot.  Provide 
        web interface to set codes, interval, and paste box for codes.
"""
# Imports
import checkdigit
from checkdigit import upc
import barcode
from barcode.writer import ImageWriter
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
from waveshare_epd import epd2in9
from time import sleep
from PIL import Image,ImageDraw,ImageFont, ImageOps
import PIL
import re

# Initialize the display.
epd = epd2in9.EPD()
epd.init(epd.lut_full_update)
epd.Clear(0xFF)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

# Functions
def decideFormat(sku):
    # Figure out which symbology to print
    if len(sku) not in (12, 13) or len(re.sub(r'\d', '', sku)) > 0:
        return 'code128'
    elif upc.validate(sku) and len(sku) == 12:
        return 'upca'
    elif upc.validate(sku) and len(sku) == 13:
        return 'ean13'
    else:
        return 'code128'

def createBarcode(sku):
    # write a flat file, BMP format, of the barcode.
    image = barcode.get(decideFormat(sku), sku, writer=ImageWriter())
    filename = image.save(decideFormat(sku), 
        {"module_width":0.2,
        "module_height":4,
        "text_distance":2,
        "font_size":8,
        "dpi":250,
        "format":"BMP"
        })
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
    # Push the image to the display
    Himage = Image.open(file)
    epd.display(epd.getbuffer(Himage))

def showCode(code):
    # Generate the file, manipulate it, and show it.
    file=createBarcode(code)
    rotateImage(file)
    displayImage(file)

################################################################################
# Test it out.
skus = ('1234567890120',
    '123456789012',
    '00123456789')
for x in skus:
    showCode(str(x))
    sleep(5)

epd.init(epd.lut_partial_update)    
epd.Clear(0xFF)
time_image = Image.new('1', (epd.height, epd.width), 255)
time_draw = ImageDraw.Draw(time_image)
time_draw.rectangle((10, 10, 120, 50), fill = 255)
time_draw.text((10, 10), 'barcodeBot!', font = font24, fill = 0)
time_draw.text((10, 34), '   IP 192.168.3.178', font = font24, fill = 0)
time_draw.text((10, 58), '   Ready for Run', font = font24, fill = 0)
time_draw.text((10, 82), '        Jesse Dyer', font = font18, fill = 0)
time_draw.text((10, 102), '        ECR Software Corporation', font = font18, fill = 0)
newimage = time_image.crop([10, 10, 120, 50])
time_image.paste(newimage, (10,10))  
epd.display(epd.getbuffer(time_image))
