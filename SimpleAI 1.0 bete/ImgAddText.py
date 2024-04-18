#!/usr/bin/python3
#coding:utf8
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def cv2ImgAddText(image, text, x, y, textColor=(0, 255, 0), textSize=20):

    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  
    draw = ImageDraw.Draw(image)
    fontText = ImageFont.truetype("/usr/share/fonts/chinese/simsun.ttc", textSize, encoding="utf-8")
    draw.text((x, y), text, textColor, font=fontText)    
    return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
