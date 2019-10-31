#%%
import numpy as np
from multivariate_regression import get_data, partition_data, get_trained_models, predict
import tkinter as tk
from tkinter import filedialog 
from tkinter import Tk
import os
import pandas as pd
from joblib import load,dump

#%%
root = tk.Tk()
folder = filedialog.askdirectory()
root.withdraw()
files = os.listdir(folder)
os.chdir(folder)

#%%
col_names = ['batch','axis','direction','parity',
'resolution','sleep_time','N',
'ax1_bias','ax1_rmse','ax1_r^2','ax2_bias','ax2_rmse','ax2_r^2']
batch_data = pd.DataFrame(columns = col_names )

def parse_name(fname):
    strings = fname.split("_")
    return [strings[0],int(strings[2][-1]),strings[3],strings[4],
    int(strings[6]),int(strings[7][-1]),int(strings[9][:-4])]
#%%
i=0
for f in files:
    if f.endswith(".mat"):
        print(f)
        fparams = parse_name(f)
        data,_ = get_data(f)
        Xs, ys, X_train, y_train, X_test, y_test = partition_data(data)
        N = 40
        d = 6
        regr1, regr2 = get_trained_models(X_train,y_train,N,d)
        if fparams[1]==1:
            dump(regr1,"{}.joblib".format(f[:-4]))
        if fparams[1]==2:
            dump(regr2,"{}.joblib".format(f[:-4]))
        bias_mimo1,std_mimo1,rmse1,r2_1,y_hat_mimo1 = predict(regr1,X_test,y_test[:,0])
        bias_mimo2,std_mimo2,rmse2,r2_2,y_hat_mimo2 = predict(regr2,X_test,y_test[:,1])
        row = [fparams[0], fparams[1], fparams[2], fparams[3], fparams[4],
        fparams[5], fparams[6], bias_mimo1, rmse1, r2_1, bias_mimo2, rmse2, r2_2]
        batch_data.loc[i]=row
        i+=1
batch_data.to_csv('aggregate_data.csv')
# %%
