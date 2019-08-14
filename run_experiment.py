import serial
import time
import sys

if __name__ == "__main__":
    sensor = serial.Serial('/dev/ttyS6',9600,timeout=2)
    controller = serial.Serial('/dev/ttyS7',9600)
    print("Connecting serial ports...")
    time.sleep(7)
    print("Sensor port: {}".format(sensor.name))
    print("Controller port: {}".format(controller.name))
    sensor.flushInput()
    
    while True:
        if(sensor.in_waiting):
            raw_bytes = sensor.readline()
            decoded_bytes = raw_bytes.decode('utf-8').strip()
            data = [float(x) for x in decoded_bytes.split()]
            print(data)
        
    
    
