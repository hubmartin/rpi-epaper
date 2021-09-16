#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
import logging
import socket
from netifaces import interfaces, ifaddresses, AF_INET

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

# pm2 start $(pwd)/epaper.py --name rpi-epaper-client --interpreter python3

global epd

class Handler(FileSystemEventHandler):
  
    @staticmethod
    def on_any_event(event):
        print(event)
        if event.is_directory:
            return None
  
        elif event.event_type == 'modified':
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % event.src_path)
            if event.src_path == "./image.png":
                print("IMAGE!!!")

                epd.init()
                Himage = Image.open('image.png')
                epd.display(epd.getbuffer(Himage))
                logging.info("Goto Sleep...")
                epd.sleep()

# 800×480
pathh = "."
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

ips = ""

for ifaceName in interfaces():
    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
    print(' '.join(addresses))
    ips = ips + ' '.join(addresses) + ", "

print(libdir)

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in5_V2
from waveshare_epd import epd2in9
from waveshare_epd import epd2in9_V2
from waveshare_epd import epd2in9b_V3
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()
    #epd = epd2in9b_V3.EPD()
    
    logging.info("init")
    epd.init()
    #epd.init(epd.lut_full_update)  #2in9


    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
   
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 0), ips, font = font24, fill = 0)

    #HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126  ryimage: red or yellow image  

    #epd.display(epd.getbuffer(Himage),epd.getbuffer(HRYimage)))
    epd.display(epd.getbuffer(Himage))
   
    logging.info("Goto Sleep...")
    epd.sleep()


    event_handler = Handler() #LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, pathh, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()    
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
