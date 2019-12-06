#!/usr/bin/env python
#title           :date_extractionWeb.py
#description     :Flask application for the date extraction.
#author          :Priyojeet Bhunia
#date            :03/12/2019
#version         :0.0
#usage           :python date_extractionWeb.py
#python_version  :3.7.5  
#==============================================================================





# importing libraries
import os
from flask import Flask, render_template, request
import cv2
from get_date import result
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename


# define a folder to store and later serve the images
UPLOAD_FOLDER = 'static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# function to check the file extension
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page
@app.route('/')
def home_page():
	return render_template('index.html')

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
	if request.method == 'POST':
		# check if there is a file in the request
		if 'file' not in request.files:
			return render_template('upload.html', msg='No file selected')
		file = request.files['file']
		# if no file is selected
		if file.filename == '':
			return render_template('upload.html', msg='No file selected')

		if file and allowed_file(file.filename):
			#s = str(file).split(" ")
			#print(str(s[1]))
			#print(file.filename)
			#path = s[1].replace("'", "")
			#print(path)
			#file.save(secure_filename(file.filename))
			#path = UPLOAD_FOLDER+file.filename
			# uploading and saving the file in UPLOAD_FOLDER
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			#print(filename)
			# call the function on it
			extracted_date = result(UPLOAD_FOLDER+filename)
			dates = ', '
			if extracted_date != None and len(extracted_date)!=0:
				dates = dates.join(extracted_date)
			else:
				dates = "sorry! I can not find the date, please try with another image."

			# extract the text and display it
			return render_template('result.html',
								   msg='Successfully processed',
								   extracted_date=dates,
								   img_src=UPLOAD_FOLDER + file.filename)
	elif request.method == 'GET':
		return render_template('upload.html')

if __name__ == '__main__':
	app.run()