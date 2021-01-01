#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in9
import time
from PIL import Image,ImageDraw,ImageFont
import traceback


try:
    
    epd = epd2in9.EPD()
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)
    
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    
   # partial update
    #logging.info("5.show time")
    epd.init(epd.lut_partial_update)    
    epd.Clear(0xFF)
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    num = 0
    time_draw.rectangle((10, 10, 120, 50), fill = 255)
    #time_draw.text((10, 10), time.strftime('%H:%M:%S'), font = font24, fill = 0)
    time_draw.text((10, 10), 'IP 192.168.3.178', font = font24, fill = 0)
    newimage = time_image.crop([10, 10, 120, 50])
    time_image.paste(newimage, (10,10))  
    epd.display(epd.getbuffer(time_image))
        
            
    
    epd.Dev_exit()
    
except IOError as e:
    print(e)
    
