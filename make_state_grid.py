import numpy as np
import sys


x_start = int(sys.argv[1])
x_end = int(sys.argv[2])
y_start = int(sys.argv[3])
y_end = int(sys.argv[4])
step = int(sys.argv[5])
fname = sys.argv[6]


with open(fname, "w") as f:
    for x in np.arange(x_start,x_end+step,step):
        for y in np.arange(y_start,y_end+step,step):
            f.write("{:04d}{:04d}\n".format(x,y))
