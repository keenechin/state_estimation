#%%
import numpy as np
import sys

try:
    x_start = int(sys.argv[1])
    x_end = int(sys.argv[2])
    x_step = int(sys.argv[3])
    y_start = int(sys.argv[4])
    y_end = int(sys.argv[5])
    y_step = int(sys.argv[6])
    fname = sys.argv[7]
except():
    print("improper")
    x_start = 0
    y_start = 0
    x_end = 1024
    y_end = 1024
    x_step = 256
    y_step = 512
    fname = "snake.txt"

num_x = int((x_end + x_step - x_start)/x_step)
num_y = int((y_end + y_step - y_start)/y_step)
grid = []
i = 0
j = 0
for x in np.arange(x_start,x_end+x_step,x_step):
    grid.append([])
    for y in np.arange(y_start,y_end+y_step,y_step):
        grid[-1].append("{:04d}{:04d}\n".format(x,y))
        j+=1
    i+=1
    j=0

array = np.array(grid)
print(array)



with open(fname, "w") as f:
    direction = 1
    for row in grid:
        if direction > 0:
            for element in row:
                f.write(element)
        else:
            for element in reversed(row):
                f.write(element)

        direction*=-1

#%%
