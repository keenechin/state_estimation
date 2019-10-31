#%%
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from tkinter.filedialog import askopenfilename
import tkinter as tk
import numpy as np
#%%
root = tk.Tk()
root.withdraw()
data = pd.read_csv(askopenfilename())


#%% Rmse over time 
df1 = data[data['axis']==1]
df2 = data[data['axis']==2]
up1 = df1[df1['direction']=="up"]
up2 = df2[df2['direction']=="up"]
down1 = df1[df1['direction']=="down"]
down2 = df2[df2['direction']=="down"]
sns.relplot('Unnamed: 0','ax1_rmse',data = up1,kind ="line")
sns.relplot('Unnamed: 0','ax1_rmse',data = down1,kind ="line")
sns.relplot('Unnamed: 0','ax2_rmse',data = up2,kind ="line")
sns.relplot('Unnamed: 0','ax2_rmse',data = down2,kind ="line")
plt.show()
# %%
