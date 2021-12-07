#!/usr/bin/python3

import socket
import time
import array
import datetime
import time
import requests
import json

import os, sys
from PIL import Image, ImageEnhance, ImageFont, ImageDraw
from io import BytesIO

IP = "192.168.1.52"
PORT = 3333

from selenium import webdriver

#$ adb logcat | grep pocasi-data
#- waiting for device -
#10-24 19:43:46.322 27582 27582 D b.a.a.b.a$a: [main] https://data.pocasi-data.cz/data/pocasi/v1/bulletin/dalsi4dny.json - 200
#10-24 19:43:47.004 27582 27637 D b.a.a.b.a$a: [DefaultDispatcher-worker-1] https://data.pocasi-data.cz/data/pocasi/v1/aladin/2020/10/24/12/178/171/prvni2dny.json - 200
#10-24 19:43:47.192 27582 27714 D b.a.a.b.a$a: [DefaultDispatcher-worker-4] https://data.pocasi-data.cz/data/pocasi/v1/aladin/2020/10/24/12/178/171/prvni2dny.json - 200
#10-24 19:43:47.332 27582 27637 D b.a.a.a.b.a.a.a: [DefaultDispatcher-worker-1] https://data.pocasi-data.cz/data/pocasi/v1/aladin/2020/10/24/12/178/171/dnes.json
#10-24 19:43:47.342 27582 27638 D b.a.a.b.a$a: [DefaultDispatcher-worker-2] https://data.pocasi-data.cz/data/pocasi/v1/aladin/2020/10/24/12/178/171/prvni2dny.json - 200
#10-24 19:43:47.436 27582 27639 D b.a.a.b.a$a: [DefaultDispatcher-worker-3] https://data.pocasi-data.cz/data/pocasi/v1/aladin/2020/10/24/12/178/171/dnes.json - 200
#10-24 19:43:56.864 27582 27582 D b.a.a.f.b$c: [main] https://data.pocasi-data.cz//static/html/srazky/radar/mapa-v5.html
#10-24 19:43:59.476 27582 27582 D b.a.a.f.b$c: [main] https://data.pocasi-data.cz//static/html/aladin/mapa-v5.html#typ=srazky
#10-24 19:44:02.442 27582 27582 D b.a.a.f.b$c: [main] https://data.pocasi-data.cz//static/html/vystrahy/mapa-v5.html#orps=
#10-24 19:44:18.637 27582 27582 D b.a.a.f.b$c: [main] https://data.pocasi-data.cz//static/html/meteogram-v2.html#x=178&y=171

# pm2 start $(pwd)/epaper.py --name rpi-epaper --interpreter python3

url="https://data.pocasi-data.cz//static/html/meteogram-v2.html#x=84&y=407"

#To test the time when the screenshot is made after loading page use the url below and http-server tool from nodejs
#url="http://localhost:8081/"

chrome_options = webdriver.chrome.options.Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=800,480")

DRIVER = 'chromedriver'
driver = webdriver.Chrome(DRIVER, options=chrome_options)
#driver.set_window_size(512, 384)
driver.get(url)
time.sleep(5) # hack to keep page load "completely"
screenshot = driver.get_screenshot_as_png()
driver.quit()
print(5)
screenshot = Image.open(BytesIO(screenshot))

image_draw = ImageDraw.Draw(screenshot) 
font = ImageFont.truetype(r'ubuntu-font-family-0.83/Ubuntu-R.ttf', 14) 
res = requests.get("https://svatky.vanio.cz/api/", headers={"Accept": "application/json"})
js = json.loads(res.text)
print(js['name'])
image_draw.text((10, 120), js['name'], font = font, align ="left", fill="#000") 

screenshot.save("preview.png")

contrast = ImageEnhance.Contrast(screenshot)
screenshot = contrast.enhance(50)

screenshot.save("enhance.png")

target = screenshot.convert('1').convert('RGB').resize((800, 480))

target.save("image.png")


os.system('scp "image.png" "pi@192.168.1.122:/home/pi/rpi-epaper/client/image.png"')
#os.system('scp "image.png" "pi@192.168.1.123:/home/pi/rpi-epaper/client/image.png"')
