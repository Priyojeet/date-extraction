#!/usr/bin/env python
#title           :custom_tools.py
#description     :python script for prcessing and extracting the date.
#author          :Priyojeet Bhunia
#date            :03/12/2019
#version         :0.0
#usage           :python custom_tools.py
#python_version  :3.7.5  
#==============================================================================





#importing libraries

from dateutil.parser import parse
import cv2
import numpy as np
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import re
import tempfile
import os
from skimage import data
from skimage.filters import threshold_otsu, threshold_local
from skimage import img_as_ubyte
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


# pytesseract or most of the ocr engines give more accurate result on 300*300 dots per inch images.
def set_image_dpi(file_name):
    im = Image.open(file_name)
    length_x, width_y = im.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False,   suffix='.png')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename



# text extraction process
def extraction(file_name):
    img = Image.open(file_name)
    width, height = img.size # getting the size of the original image.
    new_size = width*6, height*6 # multiplying the size with 6 to get new size.
    img = img.resize(new_size, Image.LANCZOS)# finally resing the original image.
    img = img.convert('L') # converting into L mode(balck and white pixels), or greyscaling
    img = img.point(lambda x: 0 if x < 155 else 255, '1') # color varies from 0 to 255

    imagetext = pytesseract.image_to_string(img)

    return imagetext


# text cleaning of the extracted text
def replaceMultiple(mainString, toBeReplaces, newString):
    for elem in toBeReplaces:
        if elem in mainString:
            mainString = mainString.replace(elem, newString)
        return  mainString

# getting the raw date from the text.
def getRaw_date(text):
    otherStr = replaceMultiple(text, ['\\', '#', '//', '§', '(', ')', '@', '!', '~', ':', ';', '[', ']', '°'] , " ").split() #using of the custom function to filter text.
    s = ""
    for i in otherStr:
        s=s+" "+i
    s = s.replace("’", "'")
    #declaring the regular expression for date formats
    pat = ['\d{1,2}-\w{3}-\d{4}', '\w+\s\d{1,2},\s\d{4}', "\w{3}\d{1,2}'\d{2}", "\w{3}\.\d{1,2}'\d{2}",
    		"\d{1,2}\s\w{3}'\d{2}", '\d{1,2}\s\w{3}\s\d{4}', '\d{1,2}\w{3}\d{2}',
       		'\d{1,2}\s\w{3},\s\d{4}', "\S+'\d{2}", '\d{1,2}/\w{3}/\d{2,4}', '\d{1,4}\.\d{1,2}\.\d{1,4}',
       		'\d{1,4}/\d{1,2}/\d{1,4}', '\d{1,4}-\d{1,2}-\d{1,4}',
           	'\d{1,2}(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d{2}', '\d{1,2}/\d{1,2}/\d{4}',
           	'\d{1,2}-(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{2}']

    l = []
    for regex in pat:
        match = re.search(regex, s)
        if match:
            if len(match.group())>=6:
                l.append(match.group())
    return l


# getting the actual date from the matched patterns.
def checkForDate(arg):
    l = []
    if len(arg)>0:
        for i in arg:
            try:
                l.append(parse(i).strftime("%Y-%m-%d"))
            except ValueError:
                pass
            except:
                pass
        return l
