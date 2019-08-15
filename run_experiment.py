import serial
import time
import sys
import numpy as np
import scipy.io as sio
import cv2

num_datapoints = 100
experimental_array = np.zeros((1,5))

def read_serial(port,verbose):
    if(port.in_waiting):
        try:
            raw_bytes = port.readline()
            decoded_bytes = raw_bytes.decode('utf-8').strip()
            data = [float(x) for x in decoded_bytes.split()]
            if verbose:
                print(data)
        except:
            return [-1]
        return data
    else:
        return [0]


def collectStream(stream):
    while len(stream)<num_datapoints:
        data = read_serial(sensor,False)
        if (len(data)==3 and any(data)):
            stream.append(data)
    return stream

def goPos(target):
    u = "{}".format(target).encode()
    controller.write(u) 
    motionComplete = False
    
    while motionComplete == False:
        try:
            data = read_serial(controller,False)
            if len(data) == 1:
                if data[0] == 7777777:
                    motionComplete = True
        except:
            continue

def serial_setup():
    sensor = serial.Serial('/dev/ttyS6',9600,timeout=2)
    controller = serial.Serial('/dev/ttyS7',9600,timeout=2)
    print("Connecting serial ports...")
    time.sleep(10)
    print("Sensor port: {}".format(sensor.name))
    print("Controller port: {}".format(controller.name))
    sensor.flushInput()
    controller.flushInput()
    return sensor,controller

if __name__ == "__main__":
    sensor,controller = serial_setup()
    fname = sys.argv[1]
    with open(fname,'r') as f:
        positions = f.readlines()
        for target in positions:
            target = target[:-1]
            print(target)
    #positions = ["03000512","04000512","06000512","05120512"]
    #positions = sys.argv[1:]
    
            sensor_stream = []
            goPos(target)
            sensor_stream = np.array(collectStream(sensor_stream))
            N = len(sensor_stream)
            ys = np.ones((N,2))
            ys[:,0] = target[:4]
            ys[:,1] = target[4:]
            experimental_array = np.vstack((experimental_array,(np.hstack((sensor_stream,ys)))))
    experimental_array = experimental_array[1:,:]
    print(experimental_array)
    sio.savemat("{}.mat".format(fname[:-3]), {'data':experimental_array})


        

    

    
        
    
    
