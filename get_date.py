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
from custom_tools import simple_ocr, getRaw_date, checkForDate, extraction, set_image_dpi, noise_remove, remove_noise, sl_otsuThresold, sl_adaptiveThresold
from datetime import date
from datetime import time
from datetime import datetime


def result(file_name):
	s = extraction(file_name)
	m = getRaw_date(s)
	l = checkForDate(m)
	
	if l==None or len(l)==0 or date.today()<datetime.strptime(l[0], "%Y-%m-%d").date():
		s = simple_ocr(set_image_dpi(file_name))
		m = getRaw_date(s)
		l = checkForDate(m)

	if l==None or len(l)==0 or date.today()<datetime.strptime(l[0], "%Y-%m-%d").date():
		s = extraction(set_image_dpi(file_name))
		m = getRaw_date(s)
		l = checkForDate(m)

	if l==None or len(l)==0 or date.today()<datetime.strptime(l[0], "%Y-%m-%d").date():
		s = simple_ocr(noise_remove(file_name))
		m = getRaw_date(s)
		l = checkForDate(m)

	if l==None or len(l)==0 or date.today()<datetime.strptime(l[0], "%Y-%m-%d").date():
		s = extraction(noise_remove(file_name))
		m = getRaw_date(s)
		l = checkForDate(m)

	if l==None or len(l)==0 or date.today()<datetime.strptime(l[0], "%Y-%m-%d").date():
		s = simple_ocr(remove_noise(file_name))
		m = getRaw_date(s)
		l = checkForDate(m)

	if l==None or len(l)==0 or date.today()<datetime.strptime(l[0], "%Y-%m-%d").date():
		s = extraction(remove_noise(file_name))
		m = getRaw_date(s)
		l = checkForDate(m)

	if l==None or len(l)==0 or date.today()<datetime.strptime(l[0], "%Y-%m-%d").date():
		s = simple_ocr(sl_otsuThresold(file_name))
		m = getRaw_date(s)
		l = checkForDate(m)

	if l==None or len(l)==0 or date.today()<datetime.strptime(l[0], "%Y-%m-%d").date():
		s = extraction(sl_otsuThresold(file_name))
		m = getRaw_date(s)
		l = checkForDate(m)

	if l==None or len(l)==0 or date.today()<datetime.strptime(l[0], "%Y-%m-%d").date():
		s = simple_ocr(sl_adaptiveThresold(file_name))
		m = getRaw_date(s)
		l = checkForDate(m)

	if l==None or len(l)==0 or date.today()<datetime.strptime(l[0], "%Y-%m-%d").date():
		s = extraction(sl_adaptiveThresold(file_name))
		m = getRaw_date(s)
		l = checkForDate(m)

	
	if l==None or len(l) == 0 or date.today()<datetime.strptime(l[0], "%Y-%m-%d").date():
		s = simple_ocr(file_name)
		m = getRaw_date(s)
		l = checkForDate(m)

	return l



'''l_date = result('/home/lucifer/acadgild/project/fyle_assignment/379efbfc.jpeg')

if l_date!=None and len(l_date)!=0:
	for i in l_date:
		print(i)

else:
	print("I can not extract the date")'''