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
x_start = int(sys.argv[2])
x_end = int(sys.argv[3])
x_step = int(sys.argv[4])
axis = int(sys.argv[5])
direction = sys.argv[6]
pair = sys.argv[7]

#%%
y_start = x_start
y_end = x_end
y_step =x_step

fname = "{0}_move_axis{1}_{2}_{3}_step_{4}.txt".format(name, axis, direction, pair, x_step)

grid, array = make_grid()
print(fname)

with open(fname,'w') as f:
    if pair == "transverse":
        array = np.flip(array,1)
    if axis == 2:
        array = np.transpose(array)
    pos_list = array.ravel()
    if direction == "down":
        pos_list = np.flip(pos_list)
    for pos in pos_list:
        f.write(pos)
# sampling_type = ""
# if sampling_type == "smooth":
#     write_smooth(grid, fname)
# if sampling_type == "smooth2":
#     write_smooth2(grid, fname)

# if sampling_type == "reading":
#     write_reading(grid, fname)
# if sampling_type == "random":
#     write_random(array, fname)

