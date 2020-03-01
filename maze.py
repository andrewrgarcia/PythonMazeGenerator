###################################
# Python maze generator program
# using PyGame for animation
# Davis MT
# Python 3.4
# 10.02.2018
###################################

import pygame
import time
import random

import timeit
start = timeit.default_timer()

random.seed(666)

# set up pygame window
WIDTH = 500
HEIGHT = 600
FPS = 30

maze_len = 20

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
def blue():
    xc,yc = random.randint(0,100),random.randint(0,100)
    return (xc,yc,255)
YELLOW = (255 ,255 ,0)

# initalise Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze PC performance test")
clock = pygame.time.Clock()

# setup maze variables
x = 0                    # x axis
y = 0                    # y axis
w = maze_len                   # width of cell
grid = []
visited = []
stack = []
solution = {}


# build the grid
def build_grid(x, y, w):
    for i in range(1,maze_len+1):
        x = maze_len                                                            # set x coordinate to start position
        y = y + maze_len                                                        # start a new row
        for j in range(1, maze_len+1):
            pygame.draw.line(screen, WHITE, [x, y], [x + w, y])           # top of cell
            pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w])   # right of cell
            pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w])   # bottom of cell
            pygame.draw.line(screen, WHITE, [x, y + w], [x, y])           # left of cell
            grid.append((x,y))                                            # add cell to grid list
            x = x + maze_len                                                    # move cell to new position


def push_up(x, y):
    pygame.draw.rect(screen,blue(), (x + 1, y - w + 1, maze_len-1, 2*maze_len-1), 0)         # draw a rectangle twice the width of the cell
    pygame.display.update()                                              # to animate the wall being removed


def push_down(x, y):
    pygame.draw.rect(screen, blue(), (x +  1, y + 1, maze_len-1, 2*maze_len-1), 0)
    pygame.display.update()


def push_left(x, y):
    pygame.draw.rect(screen, blue(), (x - w +1, y +1, 2*maze_len-1, maze_len-1), 0)
    pygame.display.update()


def push_right(x, y):
    pygame.draw.rect(screen, blue(), (x +1, y +1, 2*maze_len-1, maze_len-1), 0)
    pygame.display.update()


def single_cell( x, y):
    pygame.draw.rect(screen, GREEN, (x +1, y +1, maze_len-2, maze_len-2), 0)          # draw a single width cell
    pygame.display.update()


def backtracking_cell(x, y):
    pygame.draw.rect(screen, blue(), (x +1, y +1, maze_len-2, maze_len-2), 0)        # used to re-colour the path after single_cell
    pygame.display.update()                                        # has visited cell


def solution_cell(x,y):
    pygame.draw.rect(screen, YELLOW, (x+8, y+8, 5, 5), 0)             # used to show the solution
    pygame.display.update()                                        # has visited cell


def carve_out_maze(x,y):
    single_cell(x, y)                                              # starting positing of maze
    stack.append((x,y))                                            # place starting cell into stack
    visited.append((x,y))                                          # add starting cell to visited list
    while len(stack) > 0:                                          # loop until stack is empty
        time.sleep(.07)                                            # slow program now a bit
        cell = []                                                  # define cell list
        if (x + w, y) not in visited and (x + w, y) in grid:       # right cell available?
            cell.append("right")                                   # if yes add to cell list

        if (x - w, y) not in visited and (x - w, y) in grid:       # left cell available?
            cell.append("left")

        if (x , y + w) not in visited and (x , y + w) in grid:     # down cell available?
            cell.append("down")

        if (x, y - w) not in visited and (x , y - w) in grid:      # up cell available?
            cell.append("up")

        if len(cell) > 0:                                          # check to see if cell list is empty
            cell_chosen = (random.choice(cell))                    # select one of the cell randomly

            if cell_chosen == "right":                             # if this cell has been chosen
                push_right(x, y)                                   # call push_right function
                solution[(x + w, y)] = x, y                        # solution = dictionary key = new cell, other = current cell
                x = x + w                                          # make this cell the current cell
                visited.append((x, y))                              # add to visited list
                stack.append((x, y))                                # place current cell on to stack

            elif cell_chosen == "left":
                push_left(x, y)
                solution[(x - w, y)] = x, y
                x = x - w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                push_down(x, y)
                solution[(x , y + w)] = x, y
                y = y + w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                push_up(x, y)
                solution[(x , y - w)] = x, y
                y = y - w
                visited.append((x, y))
                stack.append((x, y))
        else:
            x, y = stack.pop()                                    # if no cells are available pop one from the stack
            single_cell(x, y)                                     # use single_cell function to show backtracking image
            time.sleep(.05)                                       # slow program down a bit
            backtracking_cell(x, y)                               # change colour to green to identify backtracking path


def plot_route_back(x,y):
    solution_cell(x, y)                                          # solution list contains all the coordinates to route back to start
    while (x, y) != (maze_len,maze_len):                                     # loop until cell position == start position
        x, y = solution[x, y]                                    # "key value" now becomes the new key
        solution_cell(x, y)                                      # animate route back
        time.sleep(.1)


x, y = maze_len, maze_len                     # starting position of grid
build_grid(5, 0, maze_len)             # 1st argument = x value, 2nd argument = y value, 3rd argument = width of cell
carve_out_maze(x,y)               # call build the maze  function
plot_route_back(maze_len*maze_len, maze_len*maze_len)         # call the plot solution function

stop = timeit.default_timer()
comptime = round(stop - start,3) 
print('computational time {} seconds'.format(comptime))

# ##### pygame loop #######
running = True
while running:
    # keep running at the at the right speed
#    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False

