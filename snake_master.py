#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adapted from https://gist.github.com/sanchitgangwar/2158089.
@author: jzlin@mit.edu
"""

import curses
import snake
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

x_size = 60
y_size = 20

curses.initscr()
win = curses.newwin(y_size, x_size, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

# Initialization of snake. Offset the map by the appropriate amount so
# the graphics are appropriately offset.
STEP_DIR_MAP = {'N': [-1, 0], 'E': [0, 1], 'S': [1, 0], 'W': [0, -1]}
key = KEY_RIGHT
score = 0
s = snake.Snake(y_size-3, x_size-3, STEP_DIR_MAP)
food = [15,10]                          # First food co-ordinates

win.addch(food[0], food[1], '*')

# While Esc key is not pressed
while key != 27:
    win.border(0)
    win.addstr(0, 2, 'Score : ' + str(score) + ' ')
    win.addstr(0, 20, ' SNAKE ')
    
    # Increases the speed of Snake as its length increases
    win.timeout(150 - (int(len(s.pos)/5) + int(len(s.pos)/10)%120))
    
    prevKey = key  # Previous key pressed
    event = win.getch()
    key = key if event == -1 else event 

    # If SPACE BAR is pressed, wait for another one (Pause/Resume)
    if key == ord(' '):                                            
        key = -1                                                   
        while key != ord(' '):
            key = win.getch()
        key = prevKey
        continue

    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:
        key = prevKey

    # Make one step forward
    last_pos = s.pos[-1]
    key_dict = [KEY_DOWN, KEY_UP, KEY_RIGHT, KEY_LEFT]
    key_dir = ['S', 'N', 'E', 'W']
    s._change_dir(key_dir[key_dict.index(key)])
    res = s._step(food)

    # If snake runs over itself or hits a wall.
    if res == None: break

    # If the snake eats food, generate a new food position.
    if res == True:
        score += 1
        food = [randint(1, y_size - 1), randint(2, x_size - 1)]
        while food in s.pos:
            food = [randint(1, y_size - 1), randint(2, x_size - 1)]
        win.addch(food[0], food[1], '*')

    last = s.pos[-1]
    win.addch(last_pos[0]+1, last_pos[1]+1, ' ')
    win.addch(s.pos[0][0]+1, s.pos[0][1]+1, '#')
    
curses.endwin()
print("\nScore - " + str(score))