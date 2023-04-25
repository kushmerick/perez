### Extremely simple simulation of a vehicle using LIDAR navigation

import math
import random
import os

### ensure we get different random numbers each time we run the program
random.seed() 

### terrain parameters

density = 0.02 # fraction of the terrain that is obstacles

height = 40
width = 200

obstacle_pixel = '#'
closest_pixel = '@'
vehicle_pixel = 'X'
empty_pixel = ' '

### creating terrain

def make_terrain():
    return [row() for i in range(height)]

def row():
    return [pixel() for j in range(width)]

def pixel():
    return 1 if random.random() < density else 0
            
### print the current terrain and the location of the vehicle and closest obstacle

def display(terrain, location, closest):
    os.system('clear' if os.name == 'posix' else 'cls')
    line()
    for i in range(height):
        edge()
        for j in range(width):
            if location == (i,j):
                pixel = vehicle_pixel
            elif closest == (i,j):
                pixel = closest_pixel
            else:
                pixel = obstacle_pixel if terrain[i][j] > 0 else empty_pixel
            print(pixel, sep='', end='')
        edge(end='\n')
    line()

def line():
    print('+', '-' * width, '+', sep='')

def edge(end=''):
    print('|', sep='', end=end)

### move the vehicle

def move(terrain, location):
    # find the closest obstacle
    closest_distance = None
    closest = None
    delta = None
    for i in range(height):
        for j in range(width):
            if terrain[i][j] > 0:
                distance = math.sqrt((location[0] - i)**2 + (location[1] - j)**2)
                if closest_distance is None or closest_distance > distance:
                    closest_distance = distance
                    closest = (i, j)
    # move away from the closest obstacle
    location = (
        bump(height, location[0], closest[0] < location[0]),
        bump(width, location[1], closest[1] < location[1])
    )
    # also move randomly
    location = (
        bump(height, location[0], flip_coin(), 3),
        bump(width, location[1], flip_coin(), 3)
    )
    return location, closest

def bump(maximum, coordinate, condition, delta = 1):
    return bound(maximum, coordinate + (+delta if condition else -delta))

def bound(maximum, value):
    return max(0, min(maximum-1, value))

def flip_coin():
    return random.random() < 0.5

### main loop

def run():
    # create terrain
    terrain = make_terrain()
    # start at a random location
    location = (
        random.randrange(height),
        random.randrange(width)
    )
    while True:
        print("Hit <RETURN> to continue, or <ANYTHING><RETURN> to stop")
        if (input()):
            break;
        location, closest = move(terrain, location)
        display(terrain, location, closest)

run()
