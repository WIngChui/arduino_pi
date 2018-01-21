import serial
import datetime
from time import sleep
import atexit
import os
import time

arduino_serial = serial.Serial(port='/dev/ttyACM0', baudrate=9600, parity='N', stopbits=1, timeout=1)


def test():
    print ("START....")

    i = 0

    while i < 2:
# send 0xAA to arduino, wait 0x55        
        d = "\xaa"
        d1=bytes(d,'utf-8')
        arduino_serial.write(d1)
        print("Send 0xAA, i=", i)
        time.sleep(1)
        read_byte = arduino_serial.read(1)
   
        if (len(read_byte) >= 1):
            if read_byte[0] == '\x55':
                print("OK")
            else:
                print("error")
        
# send 0x55 to arduino, wait 0xAA
        d = "\x55"
        d1=bytes(d,'utf-8')
        arduino_serial.write(d1)
        print("Send 0x55, i=", i)
        time.sleep(1)
        read_byte = arduino_serial.read(1)
   
        if (len(read_byte) >= 1):
            if read_byte[0] == '\xAA':
                print("OK")
            else:
                print("error",read_byte[0])
        
# turn on LED 13, sleep 2 sec.
        d = "\x5A"
        d1=bytes(d,'utf-8')
        arduino_serial.write(d1)
        print("Send 0x5A, LED on, i=", i)
        time.sleep(2)

# turn off LED 13, sleep 2 sec.
        d = "\xA5"
        d1=bytes(d,'utf-8')
        arduino_serial.write(d1)
        print("Send 0xA5, LED off, i=", i)
        time.sleep(2)

        i = i+1

    arduino_serial.close()
    print("end")

if __name__ == '__main__':
    print("Wait for Arduinoi...")
    time.sleep(5)
    if arduino_serial.is_open:
        print("Serial Open --> OK")
        arduino_serial.flushOutput()
        print("Flush output --> OK")
        arduino_serial.flushInput()
        print("Flush input --> OK")
        test()
        exit()
    else:
        print("Arduino error")
        exit()

