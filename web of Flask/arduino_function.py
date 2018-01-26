from threading import Timer, Lock
from datetime import datetime
import serial
import serial.tools.list_ports
import time
import csv

threadLock = Lock() # A thread lock to protect data

"""
	----------------------------------------------------
	Start timer : test.start()
	Stop timer after next loop: test.cancel() 
	
	RepeatingTimer : Override the run function of Timer
	----------------------------------------------------
"""

class RepeatingTimer(Timer):
	def run(self):
		while not self.finished.is_set():
			self.finished.wait(self.interval)
			self.function(*self.args, **self.kwargs)
		self.finished.set()
		
def connect_arduino():
	# Get which port of server is the Arduino board connected to,
	# when only one device is connect to the raspberry pi
	# Otherwise, need specification 
	dev_port = serial.tools.list_ports.comports()[0].device
	
	# Build up and open a serial connection to the Arduino board
	serial_connection = serial.Serial(port = dev_port, baudrate=9600, parity='N', stopbits=1, timeout=1)
	
	# Wait for connection and initialize/flush input and output buffer
	print("Wait for Arduino...")
	time.sleep(5)
	if serial_connection.is_open:
		serial_connection.reset_output_buffer()
		serial_connection.reset_input_buffer()
		return serial_connection
	else:
		raise 'Failed to connect Arduino. Please check hardware connection.'
		
'''
	get_data(serial_connection, choice = b'C')
	Usage: Get data from Arduino through serial_connection
	
	------------------ Serial.write ------------------
			Sending b'B' to Arduino:
			
				using **Serial.write** in Arudino to write data in **byte**:
					
				e.g.
						"\x15*\x00"
						temperature: ord(b'\x15')=21 , humidity: ord(b'*')=42 ,
						Light_Resistance: ord(b'\x00')=0
				
			Read data from Arduino:
				
				serial_connection.read(1)
			
		****************************************
			Sending b'I' to Arduino:
			
				using **Serial.write** in Arudino to write data in **integer**:
					
				e.g.	Same as above
					
	------------------ Serial.print / Serial.println ------------------
		Sending b'C' to Arduino:
		
			using **Serial.println** in Arudino to println data in **integer**:
				"temperature\r\nhumidity\r\nLight_Resistance\r\n"
			e.g.
					"12\r\n43\r\n1023\r\n"
					temperature: 12 , humidity:43 , Light_Resistance: 1023
			
		Read data from Arduino:
			serial_connection.readline(): read data until '\n'
	------------------------------------------------------------------------	
'''
def get_data(serial_connection, choice = b'C'):
	read_byte = []
	serial_connection.write(choice)
	time.sleep(1)
	
	# send b'C' to Arduino 
	if choice == b'C':
		while(True):
			tmp = serial_connection.readline(10)
			if tmp != b'':
				read_byte.append(tmp)
			if read_byte[0] != b'fail\r\n' and len(read_byte) == 3:
				break
			elif len(read_byte) == 4:
				break
				
		data_list = [str(i,'utf8').replace('\r\n', '') for i in read_byte]
		data_list.append(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
			
		if data_list[0] == 'fail':
			data_list.append(data_list.pop(0))
			
	# send b'B' to Arduino 
	elif choice == b'B':
		data_list = [i for i in read_byte]	# Alternative : list(map(ord,str(q,'utf8')))
		data_list.append(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
		
	return data_list

def write_csv(data_list, filename = 'record.csv'):
	with open(filename,'a') as file:
		csv_writer  = csv.writer(file)
		csv_writer.writerow(data_list)
		file.close()

def read_csv(num = 24*60, filename = 'record.csv'):
	with open(filename,'r') as f:
		record_list = list(csv.reader(f))[-num:]
		f.close()
	if ['Start'] in record_list:
		record_list.reverse()
		tmp = record_list.index(['Start'])
		record_list = record_list[:tmp]
		record_list.reverse()
	return list(record_list)

def record_data(serial_connection, filename):
	threadLock.acquire()
	data = get_data(serial_connection)
	write_csv(data, filename)
	threadLock.release()
	
def start_record(time_interval, filename):
	serial_connection = connect_arduino()
	while(True):
		if serial_connection.is_open:
			break
	loop_timer = RepeatingTimer(time_interval-1, record_data, (serial_connection, filename))
	loop_timer.start()
	write_csv(['Start'], filename)
	return loop_timer
	
def stop_record(recording_process):
	recording_process.cancel()
	return 'Stop recording data.'
	

