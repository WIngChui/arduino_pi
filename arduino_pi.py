from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, request, render_template, make_response
import os
from arduino_function import *

filename = 'record.csv'
time_interval = 30	#	seconds
#loop_timer = RepeatingTimer(time_interval, loop_get)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
	record_list = read_csv()
	temp = [i[0] for i in record_list]
	humidity = [i[1] for i in record_list]
	light_resist = [i[2] for i in record_list]
	return render_template('index.html', time_interval = time_interval*1000, temp = temp, humidity = humidity, light_resist = light_resist)

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
	#global loop_timer.start()
	app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)
	
	
	