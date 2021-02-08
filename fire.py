import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
import random
from pint import UnitRegistry
ureg = UnitRegistry()

grid_size = 1 * ureg.km #units?

time_step = 1 * ureg.mins

def fire_speed(point, SSA_count):
    F=4
    V = 8.5
    A = 1
    S = 0
    FSR = ((0.0002*F**2 - 0.008*F+0.1225)*V**2 + (-0.0008*F**2+0.0005*F+0.1823)*V + (0.0019*F**2-0.0924*F+1.2675))*(A)*(S+1) * ureg.miles/ureg.hours
    FSR = FSR * (0.99**(SSA_count/4)) # 4 drones provide 1% reduction in spread
    return (FSR, FSR, FSR, FSR) # N S W E

def drone_decrease(point, Rep_count):
    return .3 # as long as we have repeater drones, firefighters have 30% chance to put out fires

class Point:

    def __init__(self, fire):
        self.fire = fire

    def __repr__(self):
        return str(int(self.fire)) #BAD: REMOVE INT

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
                    grid[row-1, column] = Point(2*(random.random()<=spread_chance_north))
                if (row != (len(grid)-1) and grid[row+1, column] == 0 ):
                    spread_chance_south = (temp_spread[1]*time_step/grid_size).to_base_units()
                    grid[row+1, column] = Point(1*(random.random()<=spread_chance_south))
                if (column != 0 and grid[row, column-1] == 0):
                    spread_chance_west = (temp_spread[2]*time_step/grid_size).to_base_units()
                    grid[row, column-1] = Point(2*(random.random()<=spread_chance_west))
                if (column != (len(grid[0]) - 1)) and grid[row, column+1] == 0:
                    spread_chance_east = (temp_spread[3]*time_step/grid_size).to_base_units()
                    grid[row, column+1] = Point(1*(random.random()<=spread_chance_east))
                # chance of drones to help put out fire
                if random.random()<=drone_decrease(point, drones):
                    point.fire = 0
            if point.fire == 1:
                point.fire = 2

def sim_fire_spread(matrix_size, x_start, y_start, drones, num_steps):
    matrix = np.zeros((matrix_size, matrix_size))
    area = matrix_size**2
    matrix[y_start, x_start] = 2
    grid = np.vectorize(Point)(matrix)
    # print(grid)
    for i in range(num_steps):
        do_timestep(grid, drones, fire_speed, grid_size, time_step)
        # print("Timestep " + str(i) + ":" + str(np.count_nonzero(grid==2)/area))
        # print(grid)
    return np.count_nonzero(grid==2)/area

def mult_trials(matrix_size, x_start, y_start, drones, num_steps, num_trials):
    ratio_sum = 0
    for i in range(num_trials):
        burn_ratio = sim_fire_spread(matrix_size, x_start, y_start, drones, num_steps)
        print("Trial " + str(i) + " burn ratio:" + str(burn_ratio))
        ratio_sum += burn_ratio
    return ratio_sum/num_trials

