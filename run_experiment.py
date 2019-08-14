import serial
import time
import sys
import numpy as np
import scipy.io as sio

num_datapoints = 100
experimental_array = {}

def read_serial(port,verbose):
    if(port.in_waiting):
        try:
            raw_bytes = port.readline()
            decoded_bytes = raw_bytes.decode('ascii').strip()
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

if __name__ == "__main__":
    sensor = serial.Serial('/dev/ttyS6',9600,timeout=2)
    controller = serial.Serial('/dev/ttyS7',9600)
    print("Connecting serial ports...")
    time.sleep(7)
    print("Sensor port: {}".format(sensor.name))
    print("Controller port: {}".format(controller.name))
    sensor.flushInput()

    positions = ["10690","10512","20600","20512"]
    for target in positions:
        sensor_stream = []
        goPos(target)
        sensor_stream = np.array(collectStream(sensor_stream))
        print(sensor_stream)
        experimental_array["pos_{}".format(target)] = sensor_stream
    print(experimental_array.keys())
    sio.savemat("{}-{}.mat".format(positions[0], positions[-1]), experimental_array)


        

    

    
        
    
    
