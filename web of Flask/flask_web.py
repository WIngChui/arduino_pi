from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, request, render_template, make_response, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

import os

from arduino_function import *

UPLOAD_FOLDER = '/home/pi/microbit'
ALLOWED_EXTENSIONS = set(['hex'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
	------------------------------------------------------------------------
	start_record(time_interval, filename)
	usage:	Start recording data into file specified by variable 'filename' 
			for every 'time_interval' seconds.
			
	return: a Timer object
	
	Timer.cancel() :  stop recording data 
	
	e.g.	Start: recording_process = start_record(time_interval, filename)
			Stop : recording_process.cancel()
	------------------------------------------------------------------------
'''

filename = 'record.csv'
time_interval = 60	# seconds
recording_process = '' #start_record(time_interval, filename)

@app.route("/flask/", methods=['GET'])
def index():
	record_list = read_csv(filename = filename)
	if record_list != []:		
		temp = [int( i[0] ) * 10 for i in record_list]
		humidity = [int( i[1] ) * 10 for i in record_list]
		light_resist = [int( i[2] ) for i in record_list]

		date_time = list(time.strptime(record_list[0][3],"%Y/%m/%d %H:%M:%S"))[:6]
		date_time[1] -= 1
		date_time = tuple(date_time)
	
		return render_template('index.html', time_interval = time_interval, temp = temp, humidity = humidity, light_resist = light_resist, date_time = date_time)
	else :
		return render_template('index.html', time_interval = time_interval, temp = [], humidity = [], light_resist = [])
		
#	To Start Recording Data
@app.route("/flask/start")
def start_timer():
	global recording_process, time_interval, filename
	
	recording_process = start_record(time_interval, filename)
	return redirect(url_for('index'))
	
#	To Stop Recording Data
@app.route("/flask/stop")
def stop_timer():
	global recording_process
	if type(recording_process) != str:
		recording_process.cancel()
	return redirect(url_for('index'))#'Stop recording data.'
	
@app.route('/flask/uploads', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file'))
	return render_template('upload_file.html')
	
@app.route('/flask/microbit')
def uploaded_file():
	file_list = [ f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER,f)) ]
	return render_template('list_file.html', file_list = file_list)
	
@app.route('/flask/delete/<filename>')
def delete(filename):
	target_file =  (os.path.join(UPLOAD_FOLDER,filename))
	os.remove(target_file)
	return redirect(url_for('uploaded_file'))

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':	
	app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)),debug=True)
	
	
	