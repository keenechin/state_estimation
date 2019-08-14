import serial
import time
import sys
import numpy as np

num_datapoints = 100
experimental_array = {}

def read_sensor():
    if(sensor.in_waiting):
        raw_bytes = sensor.readline()
        decoded_bytes = raw_bytes.decode('ascii').strip()
        data = [float(x) for x in decoded_bytes.split()]
        print(data)
        return data
    else:
        return [0]

def collectStream(stream):
    while len(stream)<num_datapoints:
        data = read_sensor()
        if (len(data)==3 and any(data)):
            stream.append(data)
    return stream



if __name__ == "__main__":
    sensor = serial.Serial('/dev/ttyS6',9600,timeout=2)
    controller = serial.Serial('/dev/ttyS7',9600)
    print("Connecting serial ports...")
    time.sleep(7)
    print("Sensor port: {}".format(sensor.name))
    print("Controller port: {}".format(controller.name))
    sensor.flushInput()

    positions = ["10300","10512","20300","20512"]
    for target in positions:
        sensor_stream = []
        u = "{}".format(target).encode()
        controller.write(u) 
        time.sleep(2)
        sensor_stream = collectStream(sensor_stream)
        experimental_array[target]=sensor_stream


        

    

    
        
    
    
