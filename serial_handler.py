import serial
import time

def serial_setup():
    sensor = serial.Serial('COM6',9600,timeout=2)
    controller = serial.Serial('COM7',9600,timeout=2)
    print("Connecting serial ports...")
    time.sleep(10)
    print("Sensor port: {}".format(sensor.name))
    print("Controller port: {}".format(controller.name))
    sensor.flushInput()
    controller.flushInput()
    return sensor,controller

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

def goPos(controller, target):
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