#%%
import serial
import time
import sys
import numpy as np
import scipy.io as sio
import cv2
from serial_handler import read_serial,serial_setup, goPos
import numpy.matlib
#%%



def collectStream(stream):
    while len(stream)<num_datapoints:
        data = read_serial(sensor,True)
        if (len(data)==3 and any(data)):
            stream.append(data)
    return stream


def camSetup(cam_num):
    cam = cv2.VideoCapture((cam_num-1)+cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_BUFFERSIZE,1)
    if cam.isOpened():
        val, frame = cam.read()
    else:
        val = False
        frame = None

    return cam, val, frame

if __name__ == "__main__":
    num_datapoints = int(sys.argv[2])
    stime = float(sys.argv[3])
    experimental_array = np.zeros((1,5))
    save_dict ={}
  
    cam_1, val_1, frame_1 = camSetup(1)
    

    for i in range(0,100):#give camera a chance to autoadjust brightness
            val_1, frame_1 = cam_1.read()
            key = cv2.waitKey(20)
            if key == 27:
                break

    sensor,controller = serial_setup()

    fname = sys.argv[1]
    with open(fname,'r') as f:
        positions = f.readlines()
        print(positions)
        num_positions = len(positions)
        stacked_data = np.zeros((num_datapoints,5,num_positions))
        cam1_frames = np.zeros((num_positions,frame_1.shape[0],frame_1.shape[1],frame_1.shape[2]))
        val_1, frame_1 = cam_1.read()          

        experiment_progress = 0

        pos_idx = 0
        for target in positions:
            key = cv2.waitKey(20)
            if key == 27:
                break
            target = target[:-1]
            print(target)
            print("{:5.2f}%% complete".format(experiment_progress*100/num_positions))
            experiment_progress+=1
            sensor_stream = []
            goPos(controller,target)
            time.sleep(stime)
            sensor.reset_input_buffer()
            time.sleep(0.01)
            sensor_stream = np.array(collectStream(sensor_stream))   
            for i in range(0,3):
                val_1, frame_1 = cam_1.read()
            time.sleep(0.1)
            N = len(sensor_stream)
            ys = np.ones((N,2))
            ys[:,0] = target[:4]
            ys[:,1] = target[4:]
            pos_data = np.hstack((sensor_stream,ys))
            experimental_array = np.vstack((experimental_array, pos_data))
            stacked_data[:,:,pos_idx] = pos_data
            cam1_frames[pos_idx,:,:,:] = frame_1
            pos_idx+=1

    experimental_array = experimental_array[1:,:]
    print(experimental_array)
    save_dict['data'] = experimental_array
    save_dict['stacked'] = stacked_data
    save_dict['cam1_frames'] = cam1_frames
    sio.savemat("../data/automated/sleep{}_{}_n_{}.mat".format(stime,fname[2:-4],num_datapoints), save_dict)
    sensor.close()
    controller.close()
    cv2.destroyWindow("Cam1")

        

    

    
        
    
    


#%%
