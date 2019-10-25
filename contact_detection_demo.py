#%%
import numpy as np
import sklearn
import tkinter as tk
from tkinter.filedialog import askopenfilename
from sklearn.ensemble import RandomForestRegressor
from joblib import dump,load
from serial_handler import read_serial,serial_setup, goPos
import time
import matplotlib.pyplot as plt
#%%
regr1 = load('regr1.joblib')
regr2 = load('regr2.joblib')
sensor,controller = serial_setup()
root = tk.Tk()
pos_file = open(askopenfilename(),'r')
root.withdraw()
positions = pos_file.readlines()
num_positions = len(positions)
print("Data loaded")
#%%
got_data = True
np.random.seed(0)
err_data = [[]]
num_pos_sampled = 0
while num_pos_sampled < 10:
    sensor.reset_input_buffer()
    if got_data:
        i=0
        pos = "05120512\n"#positions[num_pos_sampled]
        num_pos_sampled+=1
        print(pos)
        goPos(controller,pos)
        time.sleep(2)

    mag_data = np.array(read_serial(sensor,False))
    serv_data = np.array(read_serial(controller,False))
    got_data = False


    if len(mag_data)==3 and mag_data.any() and serv_data.any():
        mag_data = mag_data.reshape(1,3)
        y_hat_1 = regr1.predict(mag_data)
        y_hat_2 = regr2.predict(mag_data)
        err_1 = y_hat_1-serv_data[0]
        err_2 = y_hat_2-serv_data[1]
        err_data[-1] =[num_pos_sampled,err_1,err_2]
        err_data.append([])
        print("err_1: {}, err_2: {}".format(err_1,err_2))
        #print("err_sum: {}".format(err_1+err_2))
        i+=1
        if i==10:
            got_data = True
#%%
err_data = np.array(err_data)
for i in range(len(err_data)-2):
    row = err_data[i]
    plt.scatter(row[0],row[2],color='r')
    plt.scatter(row[0],row[1],color='b')

plt.ylabel("Prediction Error (clicks)")
plt.ylim((-1024,1024))
plt.show()
#%%
