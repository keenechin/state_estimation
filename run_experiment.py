#%%
import serial
import time
import sys
import numpy as np
import scipy.io as sio
import cv2
#%%

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
    sensor = serial.Serial('COM6',9600,timeout=2)
    controller = serial.Serial('COM7',9600,timeout=2)
    print("Connecting serial ports...")
    time.sleep(10)
    print("Sensor port: {}".format(sensor.name))
    print("Controller port: {}".format(controller.name))
    sensor.flushInput()
    controller.flushInput()
    return sensor,controller

def camSetup(cam_num):
    cv2.namedWindow("Cam{}".format(cam_num))
    cam = cv2.VideoCapture((cam_num-1)+cv2.CAP_DSHOW)
    if cam.isOpened():
        val, frame = cam.read()
    else:
        val = False

    return cam, val, frame

if __name__ == "__main__":
    num_datapoints = int(sys.argv[2])
    experimental_array = np.zeros((1,5))
    save_dict ={}
  
    cam_1, val_1, frame_1 = camSetup(1)
    cam_2, val_2, frame_2 = camSetup(2)

    for i in range(0,100):#give camera a chance to autoadjust brightness
            cv2.imshow("Cam1", frame_1)
            cv2.imshow("Cam2", frame_2)
            val_1, frame_1 = cam_1.read()
            val_2, frame_2 = cam_2.read()
            key = cv2.waitKey(20)
            if key == 27:
                break

    sensor,controller = serial_setup()

    fname = sys.argv[1]
    with open(fname,'r') as f:
        positions = f.readlines()
        num_positions = len(positions)
        stacked_data = np.zeros((num_datapoints,5,num_positions))
        cam1_frames = np.zeros((num_positions,frame_1.shape[0],frame_1.shape[1],frame_1.shape[2]))
        cam2_frames = np.zeros_like(cam1_frames)

        pos_idx = 0
        for target in positions:
            target = target[:-1]
            print(target)
            sensor_stream = []
            goPos(target)
            time.sleep(0.05)
            sensor.flushInput()
            time.sleep(0.05)
            sensor_stream = np.array(collectStream(sensor_stream))          
            val_1, frame_1 = cam_1.read()          
            val_2, frame_2 = cam_2.read()
            if val_1 and val_2:
                cv2.imshow("Cam1",frame_1)
                cv2.imshow("Cam2",frame_2)
            key = cv2.waitKey(20)
            if key == 27:
                break
            time.sleep(0.1)
            print("{} {}".format(val_1,val_2))
            N = len(sensor_stream)
            ys = np.ones((N,2))
            ys[:,0] = target[:4]
            ys[:,1] = target[4:]
            pos_data = np.hstack((sensor_stream,ys))
            experimental_array = np.vstack((experimental_array, pos_data))
            stacked_data[:,:,pos_idx] = pos_data
            cam1_frames[pos_idx,:,:,:] = frame_1
            cam2_frames[pos_idx,:,:,:] = frame_2
            pos_idx+=1

    experimental_array = experimental_array[1:,:]
    print(experimental_array)
    save_dict['data'] = experimental_array
    save_dict['stacked'] = stacked_data
    save_dict['cam1_frames'] = cam1_frames
    save_dict['cam2_frames'] = cam2_frames
    sio.savemat("../data/automated/{}_n_{}.mat".format(fname[2:-4],num_datapoints), save_dict)
    sensor.close()
    controller.close()
    cv2.destroyWindow("Cam1")
    cv2.destroyWindow("Cam2")

        

    

    
        
    
    


#%%
