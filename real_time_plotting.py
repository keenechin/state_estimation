import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import serial
import time
import numpy as np
import scipy.io as sio
from serial_handler import read_serial, goPos, serial_setup
from mpl_toolkits import mplot3d

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

xs = []
ys = []
zs = []

# Initialize communication with magnetometer
sensor, controller = serial_setup()

# This function is called periodically from FuncAnimation
def animate(i, xs, ys, zs):

    # Read temperature (Celsius) from TMP102
    data = read_serial(sensor,False)


    # Add x and y to lists
    if len(data)==3 and any(data):
        print(data)
        xs.append(data[0])
        ys.append(data[1])
        zs.append(data[2])

    # Limit x and y lists to 20 items
        xs = xs[-20:]
        ys = ys[-20:]
        zs = zs[-20:]

    # Draw x and y lists
    ax.clear()
    ax.set_xlim([-500,500])
    ax.set_ylim([-500,500])
    ax.scatter(xs, ys)


    # Format plot
    plt.subplots_adjust(bottom=0.30)
    plt.title('Magnetometer Data Over Time')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, zs), interval=20)
plt.show()