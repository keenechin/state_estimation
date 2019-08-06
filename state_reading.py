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
"""
pos = int(sys.argv[1])
servoMsg = pos.to_bytes(2,'big')
print(servoMsg)
servo.write(servoMsg)
time.sleep(1)
print(servo.readline())
"""
while len(fulldata)<100:
    if(mag.in_waiting):
        raw_bytes = mag.readline()
        decoded_bytes = raw_bytes.decode('utf-8').strip()

        data = [float(x) for x in decoded_bytes.split()]
        if (len(data)==3 & int(np.linalg.norm(data))!=0):
            print(data)
            fulldata.append(data)
print(sys.argv),
fname = 'servo_{0}_test_{1}.txt'.format(sys.argv[1],sys.argv[2])
print(fname)
with open(fname,"w") as f:
    for item in fulldata:
        f.write("%s\n" % item)
