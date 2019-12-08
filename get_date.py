#!/usr/bin/env python
#title           :get_date.py
#description     :Finding the date from an image.
#author          :Priyojeet Bhunia
#date            :03/12/2019
#version         :0.0
#usage           :python get_date.py
#python_version  :3.7.5  
#==============================================================================





# importing libraries
from custom_tools import simple_ocr, getRaw_date, checkForDate, extraction, set_image_dpi, sl_adaptiveThresold
from datetime import date
from datetime import time
from datetime import datetime


def result(file_name):
	dpi = set_image_dpi(file_name)
	s = simple_ocr(dpi)
	m = getRaw_date(s)
	l = checkForDate(m)
	return l



'''l_date = result('/home/lucifer/acadgild/project/fyle_assignment/0a8a955f.jpeg')

if l_date!=None and len(l_date)!=0:
	for i in l_date:
		print(i)

else:
	print("I can not extract the date")'''