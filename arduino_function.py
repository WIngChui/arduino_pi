from threading import Timer
from datetime import datetime
import serial
import serial.tools.list_ports
import time
import csv

"""
	
	Start timer : test.start()
	Stop timer after next loop: test.cancel() 
	
	RepeatingTimer : Override the run function of Timer
	
"""

class RepeatingTimer(Timer):
	def run(self):
		while not self.finished.is_set():
			self.finished.wait(self.interval)
			self.function(*self.args, **self.kwargs)
		self.finished.set()

def	connect_arduino():
	arduino_serial = serial.Serial(baudrate=9600, parity='N', stopbits=1, timeout=1)
	arduino_serial.port = serial.tools.list_ports.comports()[0].device
	arduino_serial.open()
	arduino_serial.reset_output_buffer()
	arduino_serial.reset_input_buffer()
	return arduino_serial

#	Data returned in format : "temperature\r\nhumidity\r\nLight_Resistance\r\n"
#	e.g.	"12\r\n43\r\n1023\r\n"
#			temperature: 12C , humidity:43 , Light_Resistance: 1023
def get_data(choice = b'C'):
	global arduino_serial
	arduino_serial.write(choice)

	read_byte = arduino_serial.read(100)
	#data_list = [i for i in read_byte]		#send b'B' to Arduino
	data_list = str(read_byte,'utf8').split('\r\n')		#send b'C' to Arduino
	data_list[3] = (datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
	
	return data_list

def write_csv(data_list, file_name = 'record.csv'):
	with open(file_name,'a') as file:
		csv_writer  = csv.writer(file)
		csv_writer.writerow(data_list)
		file.close()
		
def read_csv(file_name = 'record.csv'):
	with open(file_name,'r') as f:
		record_list = list(csv.reader(f))[-24:]
		f.close()
	return reversed(record_list)

def loop_get():
	data = get_data(b'C')
	write_csv(data)
	
def start_timer(time_interval, funct):
	global loop_timer
	loop_timer = RepeatingTimer(time_interval, funct)
	loop_timer.start()
	return loop_timer
	
arduino_serial = connect_arduino()