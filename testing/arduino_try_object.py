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
'''
class arduino_connector():
def __init__(self):
    self.serial = self.connect_arduino()
'''
def connect_arduino():
    global arduino_serial
    dev_port = serial.tools.list_ports.comports()[0].device
    arduino_serial = serial.Serial(port = dev_port, baudrate=9600, parity='N', stopbits=1, timeout=1)
    #arduino_serial.open()
    arduino_serial.reset_output_buffer()
    arduino_serial.reset_input_buffer()
    return arduino_serial

#   Data returned in format : "temperature\r\nhumidity\r\nLight_Resistance\r\n"
#   e.g.    "12\r\n43\r\n1023\r\n"
#           temperature: 12C , humidity:43 , Light_Resistance: 1023
def get_data(choice = b'C'):
    
    arduino_serial.serial.write(choice)
	time.sleep(1)
    read_byte = self.serial.readline(20)
    #data_list = [i for i in read_byte]     #send b'B' to Arduino
    data_list = str(read_byte,'utf8').split('\r\n')     #send b'C' to Arduino
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
    return list(reversed(record_list))

def loop_get():
    data = arduino_serial.get_data()
    write_csv(data)

arduino_serial = connect_arduino()
    
'''
def start_timer(time_interval, funct):
    loop_timer = RepeatingTimer(time_interval, funct)
    loop_timer.start()
    return loop_timer
    
'''