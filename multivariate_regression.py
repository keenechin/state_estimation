#%%
import numpy as np
import sklearn
import scipy.io as sio
import tkinter as tk
from tkinter.filedialog import askopenfilename
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import copy

#%% Read file

def get_data():
    root = tk.Tk()
    filename = askopenfilename()
    print(filename)
    root.withdraw()
    mat_contents = sio.loadmat(filename)
    data = mat_contents['data']
    return data, mat_contents

data,_ = get_data()

    #%% Train-test split
Xs = data[:,1:3]
ys = data[:,4:5]
N = len(data)
train_portion = 0.8
shuffled = data[np.random.permutation(N),:]
train_test_cutoff = int(np.floor(N*train_portion))
train_data = shuffled[0:train_test_cutoff-1,:]
test_data = shuffled[train_test_cutoff:-1,:]
y_train = train_data[:,-2:]
y_test = test_data[:,-2:]
X_train = train_data[:,:-2]
X_test = test_data[:,:-2]


#%% Evaluate predictions
def predict(regressor, X_test, y_test):
    y_hat_reg = regressor.predict(X_test)
    errors = y_hat_reg-y_test
    bias = np.mean(errors)
    stdev = np.std(errors)
    r2 = r2_score(y_test,y_hat_reg)
    print("Prediction standard deviation: {}".format(stdev))
    print("Prediction R^2: {}".format(r2))

    return [bias,stdev,r2,y_hat_reg]
#%% Init Model

N=20
d = 6
regr1 = RandomForestRegressor(max_depth=d,random_state=0,n_estimators=N)
regr2 = RandomForestRegressor(max_depth=d,random_state=0,n_estimators=N)
#%% Train Model
print("N: {}, d: {}".format(N,d))
print("Training mimo 1...")
regr1.fit(X_train,y_train[:,0].ravel())
bias_mimo1,std_mimo1,r2_1,y_hat_mimo1 = predict(regr1,X_test,y_test[:,0])

print("Training mimo 2...")
regr2.fit(X_train,y_train[:,1].ravel())

bias_mimo2,std_mimo2,r2_2,y_hat_mimo2 = predict(regr2,X_test,y_test[:,1])
print("")
#%%
from joblib import dump,load
dump(regr1,'regr1.joblib')
dump(regr2,'regr2.joblib')
