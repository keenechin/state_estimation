import serial
import time
import numpy as np
import datetime
import random
import sys

mag = serial.Serial('/dev/ttyS6',9600,timeout=2)
print(mag.name)
mag.flushInput()
#time.sleep(1)

fulldata = []
started = False

def readSerial():
    if(mag.in_waiting):
        raw_bytes = mag.readline()
        decoded_bytes = raw_bytes.decode('ascii').strip()
        data = [float(x) for x in decoded_bytes.split()]
        return data
    else:
        return [0]

while started == False:
    data = readSerial()
    if len(data)==1:
        if data[0] == 7777777:
            started = True

while len(fulldata)<100:
    data = readSerial()
    if (len(data)==3 and any(data)):
        print(data)
        fulldata.append(data)

print(sys.argv),
fname = 'servo_{0}_test_{1}.txt'.format(sys.argv[1],sys.argv[2])
print(fname)
with open(fname,"w") as f:
    for item in fulldata:
        f.write("%s\n" % item)
