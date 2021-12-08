#!/usr/bin/python3

import requests
import json

import os, sys
from PIL import Image, ImageEnhance, ImageFont, ImageDraw


screenshot = Image.new(mode="RGB", size=(800, 480), color="#fff")

image_draw = ImageDraw.Draw(screenshot) 
font = ImageFont.truetype(r'ubuntu-font-family-0.83/Ubuntu-R.ttf', 14) 
res = requests.get("https://svatky.vanio.cz/api/", headers={"Accept": "application/json"})
js = json.loads(res.text)
print(js['name'])
image_draw.text((10, 50), js['name'], font = font, align ="left", fill="#000") 

screenshot.show()
