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
from sklearn.metrics import mean_squared_error
import copy


def get_data(filename):
    mat_contents = sio.loadmat(filename)
    data = mat_contents['data']
    return data, mat_contents

def predict(regressor, X_test, y_test):
    y_hat_reg = regressor.predict(X_test)
    errors = y_hat_reg-y_test
    bias = np.mean(errors)
    stdev = np.std(errors)
    rmse = np.sqrt(mean_squared_error(y_test,y_hat_reg))
    r2 = r2_score(y_test,y_hat_reg)
    print("Prediction RMSE: {}".format(rmse))
    print("Prediction R^2: {}".format(r2))
    return [bias,stdev,rmse,r2,y_hat_reg]

def partition_data(data):
    Xs = data[:,1:3]
    ys = data[:,4:5]
    N = len(data)
    train_portion = 0.8
    np.random.seed(0)
    shuffled = data[np.random.permutation(N),:]
    train_test_cutoff = int(np.floor(N*train_portion))
    train_data = shuffled[0:train_test_cutoff-1,:]
    test_data = shuffled[train_test_cutoff:-1,:]
    y_train = train_data[:,-2:]
    y_test = test_data[:,-2:]
    X_train = train_data[:,:-2]
    X_test = test_data[:,:-2]
    return Xs, ys, X_train, y_train, X_test, y_test

def get_trained_models(X_train, y_train, N,d):
    regr1 = RandomForestRegressor(max_depth=d,random_state=0,n_estimators=N)
    regr2 = RandomForestRegressor(max_depth=d,random_state=0,n_estimators=N)
    print("N: {}, d: {}".format(N,d))
    print("Training mimo 1...")
    regr1.fit(X_train,y_train[:,0].ravel())
    print("Training mimo 2...")
    regr2.fit(X_train,y_train[:,1].ravel())
    return regr1, regr2


if __name__ == "__main__":
    root = tk.Tk()
    filename = askopenfilename()
    print(filename)
    root.withdraw()
    data,_ = get_data(filename)
    Xs, ys, X_train, y_train, X_test, y_test = partition_data(data)
    N = 40
    d = 6
    regr1, regr2 = get_trained_models(X_train,y_train,N,d)


    bias_mimo1,std_mimo1,rmse1,r2_1,y_hat_mimo1 = predict(regr1,X_test,y_test[:,0])
    bias_mimo2,std_mimo2,r2_2,rmse2,y_hat_mimo2 = predict(regr2,X_test,y_test[:,1])
    print("")    #%% save models
    from joblib import dump,load
    dump(regr1,'regr1.joblib')
    dump(regr2,'regr2.joblib')
