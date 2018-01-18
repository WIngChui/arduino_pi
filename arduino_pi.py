from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, request, render_template, make_response
import os
from arduino_function import *

filename = 'record.csv'

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
	return render_template('index.html', file=read_csv(filename))
	
loop_timer = RepeatingTimer(5*60, loop_get)

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
	global loop_timer.start()
	app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)
	
	
	