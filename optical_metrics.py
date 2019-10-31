#%%
from serial_handler import read_serial,serial_setup,goPos
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import Tk
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import time
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm
from matplotlib import colors
#%%

def camSetup(cam_num):
    cam = cv2.VideoCapture((cam_num-1)+cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_BUFFERSIZE,1)
    if cam.isOpened():
        val, frame = cam.read()
    else:
        val = False
        frame = None

    return cam, val, frame

def get_colors(image):
    pixel_colors = image.reshape((np.shape(image)[0]*np.shape(image)[1], 3))
    norm = colors.Normalize(vmin=-1.,vmax=1.)
    norm.autoscale(pixel_colors)
    pixel_colors = norm(pixel_colors).tolist()
    return pixel_colors

def hsv_plot(image,pixel_colors):
    h, s, v = cv2.split(image)
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1, projection="3d")
    axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
    axis.set_xlabel("Hue")  
    axis.set_ylabel("Saturation")
    axis.set_zlabel("Value")
    plt.show()
    return hsv_frame

def get_mask(rgb_frame):
    hsv_frame = cv2.cvtColor(frame_1,cv2.COLOR_RGB2HSV)
    dark_red = (0,100,0)
    lighter_red = (100,255,255)
    light_red = (155,100,0)
    darker_red = (255,255,255)
    mask_low = cv2.inRange(hsv_frame,dark_red,lighter_red)
    mask_high = cv2.inRange(hsv_frame,light_red,darker_red)
    mask = mask_low+mask_high
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.erode(mask,kernel,iterations=2)
    mask = cv2.dilate(mask,kernel,iterations=2)
    result = cv2.bitwise_and(rgb_frame,rgb_frame,mask = mask)
    return mask,result

#%%



def get_image_features():
    M = cv2.moments(mask)
    cx = M['m10']/M['m00']
    cy = M['m01']/M['m00']
    m20 = M['m20']/M['m00']-cx**2
    m11 = 2*(M['m11']/M['m00']-cx*cy)
    m02 = M['m02']/M['m00']-cy**2
    #cov = np.array([[m20,m11],[m11,m02]])
    #evals, evecs = np.linalg.eig(cov)
    theta = 0.5*np.arctan2(m11,m20-m02) #+(m20<m02)*np.pi/2
    major = np.sqrt(8*(m20+m02+np.sqrt(4*m11**2+(m20-m02)**2)))
    endpoints = np.array([[cx + 0.5*major*np.cos(theta),cy+0.5*major*np.sin(theta)],
    [cx - 0.5*major*np.cos(theta),cy-0.5*major*np.sin(theta)]])
    screen_center = np.array([320,240])
    dists = np.linalg.norm(endpoints-screen_center,axis=1)
    endpoint = endpoints[np.argmax(dists),:]
    return endpoint, major, theta
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    fname = filedialog.askopenfilename()
    cam_1, val_1, frame_1 = camSetup(1)
    for i in range(0,100):
        val_1, frame_1 = cam_1.read()
        
    sensor,controller = serial_setup()
    with open(fname,'r') as f:
        positions = f.readlines()
        for target in positions:
            target = target[:-1]
            print(target)
            goPos(controller,target)
            time.sleep(2)
            for i in range(0,3):
                val_1,frame_1 = cam_1.read()
                frame_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2RGB)

            # plt.imshow(frame_1)
            # plt.show()
            mask,result = get_mask(frame_1)
            endpoint, length, theta = get_image_features()
            plt.scatter(endpoint[0],endpoint[1])
            plt.gca().invert_yaxis()  # Match the image system with origin at top left
            plt.imshow(result)
            plt.pause(0.1)
    plt.show()
    sensor.close()
    controller.close()