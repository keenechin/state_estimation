#%%
import numpy as np
from multivariate_regression import get_data, partition_data, get_trained_models,predict
import tkinter as tk
from tkinter import filedialog 
from tkinter import Tk
import os
import pandas as pd
from joblib import load,dump

#%% Get predictive models
root = tk.Tk()
root.withdraw()

regr1_name = filedialog.askopenfilename()
regr1 = load(regr1_name)
print("regr1 is {}".format(regr1_name))
regr2_name = filedialog.askopenfilename()
regr2 = load(regr2_name)
print("regr2 is {}".format(regr2_name))

#%% Get test sets
num_test_sets = 6#int(input("How many files to evaluate?"))
files = []
test_sets = []
for i in range(num_test_sets):
    f = filedialog.askopenfilename()
    files.append(f)
    test_sets.append(get_data(f)[0])

#%% Evaluate predictors
i = 0
for test_data in test_sets:
    print(files[i])
    i+=1
    X_test = test_data[:,0:3]
    y_test = test_data[:,3:5]
    print('ax1:')
    bias_mimo1,std_mimo1,rmse1,r2_1,y_hat_mimo1 = predict(regr1,X_test,y_test[:,0])
    print("rmse: {}, R^2:{}".format(rmse1,r2_1))
    print('ax2:')
    bias_mimo2,std_mimo2,rmse2,r2_2,y_hat_mimo2 = predict(regr2,X_test,y_test[:,1])
    print("rmse: {}, R^2:{}".format(rmse2,r2_2))
    print(" ")


# %%
