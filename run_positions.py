import serial
import time
ser = serial.Serial('/dev/ttyS7',9600)
time.sleep(0.05)
print(ser.name)
while (1):
    ser.write(b'10300')
    time.sleep(1)
