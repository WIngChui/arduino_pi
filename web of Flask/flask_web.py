from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, request, render_template, make_response
import os
from arduino_function import *

filename = 'record.csv'
time_interval = 60	#seconds
arduino_serial = connect_arduino()
while(True):
	if arduino_serial.is_open:
		break
loop_timer = RepeatingTimer(time_interval, loop_get, (arduino_serial,))
loop_timer.start()

app = Flask(__name__)

@app.route("/flask/", methods=['GET'])
def index():
	record_list = read_csv()
	temperature = []
	humidity = []
	light_resist = []
	for i in record_list:
		date_time = list(time.strptime(i[3], "%Y/%m/%d %H:%M:%S"))[:6]
		date_time[1] -= 1
		date_time = tuple( date_time )
		temperature.append( [date_time, int(i[0]) * 10] )
		humidity.append( [date_time, int(i[1]) * 10] )
		light_resist.append( [date_time, int(i[2])] )

	return render_template('index.html', time_interval = time_interval, temperature = temperature, humidity = humidity, light_resist = light_resist)

@app.route("/flask/stop")
def stop_timer():
	global loop_timer
	loop_timer.cancel()

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':	
	app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)),debug=True)
	
	
	