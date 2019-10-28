#%%
import numpy as np
import sys

def write_smooth(grid,fname):
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
def write_smooth2(grid,fname):
    grid = np.array(grid).T.tolist()
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


def write_reading(grid,fname):
    with open(fname,"w") as f:
        for row in grid:
            for element in row:
                f.write(element)

def write_random(array,fname):
    flat = np.ravel(array)
    print(flat)
    np.random.shuffle(flat)
    print(flat)
    with open(fname,"w") as f:
        for element in flat:
            f.write(element)


def make_grid():
    # num_x = int((x_end + x_step - x_start)/x_step)
    # num_y = int((y_end + y_step - y_start)/y_step)
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
    return grid, array


#%%
name  = sys.argv[1]
num_axes = int(sys.argv[2])
x_start = int(sys.argv[3])
x_end = int(sys.argv[4])
x_step = int(sys.argv[5])
axis = int(sys.argv[6])
direction = sys.argv[7]
pair = sys.argv[8]


if num_axes == 2:
    y_start = x_start
    y_end = x_end
    y_step =x_step
else:
    if axis == 1:
        y_start = 512
        y_end = 512
        y_step = 1
    else:
        y_start = x_start
        y_end = x_end
        y_step = x_step
        x_start = 512
        x_end = 512
        x_step = 1

#%%


fname = "{0}_move_axis{1}_{2}_{3}_step_{4}.txt".format(name, axis, direction, pair, max(x_step,y_step))

grid, array = make_grid()

with open(fname,'w') as f:
    if pair == "transverse":
        array = np.flip(array,1)
        
    if axis == 2:
        array = np.transpose(array)

    if direction == "down":
        array = np.flip(array)

    pos_list = array.ravel()
    print(array)
    for pos in pos_list:
        f.write(pos)
print("Wrote data to {}".format(fname))

# sampling_type = ""
# if sampling_type == "smooth":
#     write_smooth(grid, fname)
# if sampling_type == "smooth2":
#     write_smooth2(grid, fname)

# if sampling_type == "reading":
#     write_reading(grid, fname)
# if sampling_type == "random":
#     write_random(array, fname)

