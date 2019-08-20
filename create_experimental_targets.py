import numpy as np
import sys


x_start = int(sys.argv[1])
x_end = int(sys.argv[2])
x_step = int(sys.argv[3])
y_start = int(sys.argv[4])
y_end = int(sys.argv[5])
y_step = int(sys.argv[6])
fname = sys.argv[7]


with open(fname, "w") as f:
    for x in np.arange(x_start,x_end+x_step,x_step):
        for y in np.arange(y_start,y_end+y_step,y_step):
            f.write("{:04d}{:04d}\n".format(x,y))
