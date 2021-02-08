import numpy as np
import sys
from imagehandling import elevation_array
np.set_printoptions(threshold=sys.maxsize)
import random
from pint import UnitRegistry
ureg = UnitRegistry()
from PIL import Image

time_step = 1 * ureg.mins #units

def fire_speed(point, SSA_count):
    F=4
    V = 8.5
    A = 1
    S = 1.13*point.height/2034
    FSR = ((0.0002*F**2 - 0.008*F+0.1225)*V**2 + (-0.0008*F**2+0.0005*F+0.1823)*V + (0.0019*F**2-0.0924*F+1.2675))*(A)*(S+1) * ureg.miles/ureg.hours
    FSR = FSR * (0.94**(SSA_count/1)) # 1 drone provides 6% reduction in spread
    return (FSR, FSR, FSR, FSR) # N S W E

def drone_decrease(point, Rep_count):
    if Rep_count > 0:
        return 0.3 # as long as we have repeater drones, firefighters have 30% chance to put out fires
    else:
        return 0.3 # assume repeater drones are active, allowing firefighters to still do their job

class Point:

    def __init__(self, height):
        self.height = height
        if (self.height <= 6):
            self.fire = 3
        else:
            self.fire = 0
            # 0 = no fire
            # 1 = placeholder value
            # 2 = fire
            # 3 = water
            # 4 = put out fire

    def __repr__(self):
        return str(int(self.fire))

    def __eq__(self, other):
        return self.fire == other

def do_timestep(grid, drones, fire_spread_function, grid_size, time_step):
    for row, row_of_points in enumerate(grid):
        for column, point in enumerate(row_of_points):
            if point == 2:
                temp_spread = fire_spread_function(point, drones)
                # chance to spread in any cardinal direction
                if (row != 0 and grid[row-1, column] == 0):
                    spread_chance_north = (temp_spread[0]*time_step/grid_size).to_base_units()
                    grid[row-1, column].fire = 2*(random.random()<=spread_chance_north)
                if (row != (len(grid)-1) and grid[row+1, column] == 0 ):
                    spread_chance_south = (temp_spread[1]*time_step/grid_size).to_base_units()
                    grid[row+1, column].fire = 1*(random.random()<=spread_chance_south)
                if (column != 0 and grid[row, column-1] == 0):
                    spread_chance_west = (temp_spread[2]*time_step/grid_size).to_base_units()
                    grid[row, column-1].fire = 2*(random.random()<=spread_chance_west)
                if (column != (len(grid[0]) - 1)) and grid[row, column+1] == 0:
                    spread_chance_east = (temp_spread[3]*time_step/grid_size).to_base_units()
                    grid[row, column+1].fire = 1*(random.random()<=spread_chance_east)
                # chance of drones to help put out fire
                if random.random()<=drone_decrease(point, drones):
                    point.fire = 4
            if point.fire == 1:
                point.fire = 2

def sim_fire_spread(elevation_matrix, x_start, y_start, size_start, drones, num_steps):
    area = elevation_matrix.size
    grid = np.vectorize(Point)(elevation_matrix)
    for y in range(size_start):
        for x in range(size_start):
            grid[y_start+y, x_start+x].fire = 2
    for i in range(num_steps):
        do_timestep(grid, drones, fire_speed, grid_size, time_step)
    return (np.count_nonzero(grid==2) + np.count_nonzero(grid == 4))/area

def mult_trials(elevation_matrix, x_start, y_start, size_start, drones, num_steps, num_trials):
    ratio_sum = 0
    for i in range(num_trials):
        burn_ratio = sim_fire_spread(elevation_matrix, x_start, y_start, size_start, drones, num_steps)
        ratio_sum += burn_ratio
    return ratio_sum/num_trials

def drone_test(size_start, max_drones, num_steps, num_trials):
    for i in range(max_drones + 1):
        avg_burned = mult_trials(elevation_array, 100, 100, size_start, i, num_steps, num_trials)
        print("For "+ str(i) + " drones: " + str(avg_burned))

km_size=600 #height of region we're modeling, in km
grid_size = km_size/elevation_array.shape[0] * ureg.km

print(sim_fire_spread(elevation_array, 100, 100, 5, 1, 100))

            # colors = {3:[0,0,255], 0:[0,255,0], 2:[255,170,0], 4:[128,128,128]}
            # temp_img = [[colors[j.fire] for j in i] for i in grid]
            # j = Image.fromarray(np.uint8(temp_img), "RGB")
            # j.show()
