#%%
import numpy as np
import sklearn
from tkinter.filedialog import askopenfilename
from multivariate_regression import get_data, partition_data, get_trained_models, predict
from joblib import dump,load
import os
import pandas as pd
from sklearn.metrics import r2_score,mean_squared_error
#%%
root = tk.Tk()
root.withdraw()
up_regr1 = load(askopenfilename())
up_regr2 = load(askopenfilename())
down_regr1 = load(askopenfilename())
down_regr2 = load(askopenfilename())
#%%

filename = askopenfilename()
print(filename)
data,_ = get_data(filename)
#%%
y_true = data[:,-2:]
y_pred = pd.DataFrame(columns = ['up1','up2','down1','down2','conditioned1','conditioned2'])

# %%
last_pos = np.array([512,512])
for i in range(len(data)):
    row = data[i]
    mag_data = row[:-2].reshape(1,3)
    y_pred.loc[i]= [up_regr1.predict(mag_data)[0],
     up_regr2.predict(mag_data)[0],
     down_regr1.predict(mag_data)[0],
    down_regr2.predict(mag_data)[0],None,None]




    
    if np.mod(i,100)==0:
        d_pos = y_true[i]-last_pos
        print("{}-{} = {}".format(y_true[i],last_pos,d_pos))
        last_pos = y_true[i]

    if d_pos[0]<0:
        y_pred.loc[i]['conditioned1'] = down_regr1.predict(mag_data)[0]
        print('down')
    else:
        y_pred.loc[i]['conditioned1'] = up_regr1.predict(mag_data)[0]
        print('up')
    
    if d_pos[1]<0:
        y_pred.loc[i]['conditioned2'] = down_regr2.predict(mag_data)[0]
        print('down')
    else:
        y_pred.loc[i]['conditioned2'] = up_regr2.predict(mag_data)[0]
        print('up')
# %%
rmse_up1 =  np.sqrt(mean_squared_error(y_true[:,0],y_pred['up1']))
rmse_up2 =  np.sqrt(mean_squared_error(y_true[:,1],y_pred['up2']))
rmse_down1 =  np.sqrt(mean_squared_error(y_true[:,0],y_pred['down1']))
rmse_down2 =  np.sqrt(mean_squared_error(y_true[:,1],y_pred['down2']))
rmse_cond1 =  np.sqrt(mean_squared_error(y_true[:,0],y_pred['conditioned1']))
rmse_cond2 =  np.sqrt(mean_squared_error(y_true[:,1],y_pred['conditioned2']))
# %%
print([[rmse_up1,rmse_down1,rmse_cond1],[rmse_up2,rmse_down2,rmse_cond2]])

# %%
