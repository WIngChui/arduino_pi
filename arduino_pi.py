from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, request, render_template, make_response
import os
from arduino_function import *

filename = 'record.csv'
time_interval = 10	#	seconds
arduino_serial = connect_arduino()
if arduino_function,is_open: 
	loop_get()
	loop_timer = RepeatingTimer(time_interval, loop_get)
	loop_timer.start()
else:
	return 'Arduino connection error'

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
	record_list = read_csv()
	temp = [int(i[0])*10 for i in record_list]
	humidity = [int(i[1])*10 for i in record_list]
	light_resist = [int(i[2]) for i in record_list]
	date_time = list(time.strptime(record_list[0][3],"%Y/%m/%d %H:%M:%S"))[:6]
	date_time[1] -= 1
	date_time = tuple(date_time)
	return render_template('index.html', time_interval = time_interval, temp = temp, humidity = humidity, light_resist = light_resist, date_time = date_time)

@app.route("/stop")
def stop_timer():
	loop_timer.cancel()

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
	app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)
	
	
	