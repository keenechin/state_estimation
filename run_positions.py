import serial
import time
import struct
ser = serial.Serial('/dev/ttyS7',9600)
time.sleep(10)
print(ser.name)
command_data = b'10300'
ser.write(command_data)
time.sleep(10)
while ser.in_waiting>0:
    print(ser.read())
