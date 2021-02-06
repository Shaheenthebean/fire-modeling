import numpy as np
import random

grid_size = 1 #units?

time_step = 1 #units?

def fire_speed(point):
    return (0.25, 0.25, 0.25, 0.25) # N S W E

class Point:

    def __init__(self, fire):
        self.fire = fire

    def __repr__(self):
        return str(int(self.fire)) #BAD: REMOVE INT

    def __eq__(self, other):
        return self.fire == other

def do_timestep(grid, fire_spread_function, grid_size, time_step):
    for row, row_of_points in enumerate(grid):
        for column, point in enumerate(row_of_points):
            if point.fire == 2:
                temp_spread = fire_spread_function(point)
                if (row != 0 and grid[row-1, column] == 0):
                    spread_chance_north = temp_spread[0]/grid_size
                    grid[row-1, column] = Point(2*(random.random()<=spread_chance_north))
                if (row != (len(grid)-1) and grid[row+1, column] == 0 ):
                    spread_chance_south = temp_spread[1]/grid_size
                    grid[row+1, column] = Point(1*(random.random()<=spread_chance_south))
                if (column != 0 and grid[row, column-1] == 0):
                    spread_chance_west = temp_spread[2]/grid_size
                    grid[row, column-1] = Point(2*(random.random()<=spread_chance_west))
                if (column != (len(grid[0]) - 1)) and grid[row, column+1] == 0:
                    spread_chance_east = temp_spread[3]/grid_size
                    grid[row, column+1] = Point(1*(random.random()<=spread_chance_east))
            if point.fire == 1:
                point.fire = 2


matrix = np.zeros((3,4))
matrix[1,2] = 2
grid = np.vectorize(Point)(matrix)
print(grid)
for i in range(5):
    do_timestep(grid, fire_speed, grid_size, time_step)
    print(grid)
    print("\n\n\n")
