#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
import logging
import socket
from netifaces import interfaces, ifaddresses, AF_INET
import hashlib

from waveshare_epd import epd7in5_V2

import time
from PIL import Image,ImageDraw,ImageFont
import traceback

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

# pm2 start $(pwd)/epaper.py --name rpi-epaper-client --interpreter python3

global epd

global_image_hash = ''

def file_as_bytes(file):
    with file:
        return file.read()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        global global_image_hash

        print(event)
        if event.is_directory:
            return None
  
        elif event.event_type == 'modified':
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % event.src_path)
            if event.src_path == "./image.png":
                print("IMAGE!!!")
                img_hash = hashlib.md5(file_as_bytes(open(event.src_path, 'rb'))).hexdigest()
                print(img_hash)

                # Do not redraw same image - sshcp and cp commands generate two file systems events
                # this is here so it does not redraw twice
                if global_image_hash == img_hash:
                    print('Same image, do not redraw')
                    return None

                global_image_hash = img_hash

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

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()
    
    logging.info("init")
    epd.init()

    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
   
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 0), ips, font = font24, fill = 0)

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
