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


# adaptive Thresholding using cv2 for clear the noise of the image.
def noise_remove(file_name):
    img = cv2.imread(file_name)
    img = cv2.medianBlur(img,5) # noise removing using medianBlur

    grayscaled = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) # gray scaling the blur image.
    th = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2) # applying theresold.

    cv2.imwrite('temp.png', th) # saving the 
    return os.path.abspath('temp.png') # getting the path of the cleaned image.


# another noise cleaning process or sharpening process using filtration
def remove_noise(file_name):
    image = cv2.imread(file_name)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,10,-1], [-1,-1,-1]]) # creating the kernel to process teh image
    sharpen = cv2.filter2D(gray, -1, sharpen_kernel) # using the 2d convolution using the kernel
    cv2.imwrite('temp.png', sharpen)
    return os.path.abspath('temp.png')


# adaptive Thresholding using sklearn and cv2
def sl_adaptiveThresold(file_name):
    image = cv2.imread(file_name)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # grayscaling
    block_size = 35 # defining the block size
    local_thresh = threshold_local(image, block_size, offset=10) # applying thresold with the offset of 10
    binary_local = image > local_thresh
    img = img_as_ubyte(binary_local) # converting the output into cv2 excecutable format or array.
    cv2.imwrite('temp.png', img)
    return os.path.abspath('temp.png')


# otsuThresolding using sklearn and cv2
def sl_otsuThresold(file_name):
    image = cv2.imread(file_name)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    global_thresh = threshold_otsu(image) # applying otsu thresholding
    binary_global = image > global_thresh
    img = img_as_ubyte(binary_global)
    cv2.imwrite('temp.png', img)
    return os.path.abspath('temp.png')


# text extraction process 1
def extraction(file_name):
    img = Image.open(file_name)
    width, height = img.size # getting the size of the original image.
    new_size = width*6, height*6 # multiplying the size with 6 to get new size.
    img = img.resize(new_size, Image.LANCZOS)# finally resing the original image.
    img = img.convert('L') # converting into L mode(balck and white pixels), or greyscaling
    img = img.point(lambda x: 0 if x < 155 else 255, '1') # color varies from 0 to 255

    imagetext = pytesseract.image_to_string(img)

    return imagetext


# common text extraction process 2.
def simple_ocr(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    return text


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
