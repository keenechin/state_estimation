import serial
import time
import sys
ser = serial.Serial('/dev/ttyS7',9600)
time.sleep(7)
print(ser.name)
command_data = "{}".format(sys.argv[1]).encode()
ser.write(command_data)
input('Press enter when experiment completes.')
