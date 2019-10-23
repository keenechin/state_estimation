#%%
import serial
import time
import sys
import numpy as np
import scipy.io as sio
from serial_handler import read_serial, goPos, serial_setup
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits import mplot3d

#%%
sensor, controller = serial_setup()
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

"""
try:
    while True:
        data = read_serial(sensor,False)
        if len(data)==3 and any(data):
            print(data)
            ax.scatter(data[0], data[1], data[2])
            plt.show()

except KeyboardInterrupt:
    sensor.close()
    controller.close()
    pass
except Exception:
    sensor.close()
    controller.close()

"""
def animate(sensor):
    data = read_serial(sensor,False)
    ax.clear()
    if len(data)==3 and any(data):
            print(data)
            ax.scatter(data[0], data[1], data[2])


ani = animation.FuncAnimation(fig,animate,fargs=(sensor),interval = 1000)
plt.show()
#%%
