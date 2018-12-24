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

map_size = 30

curses.initscr()
win = curses.newwin(map_size, map_size, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

# Initialization of snake.
key = KEY_RIGHT
score = 0
s = snake.Snake(map_size)     # Initial snake co-ordinates
food = [15,10]                # First food co-ordinates

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
        food = [randint(1, map_size - 2), randint(1, map_size - 2)]
        while food in s.pos:
            food = [randint(1, map_size - 2), randint(1, map_size - 2)]
        win.addch(food[0], food[1], '*')

    last = s.pos[-1]
    win.addch(last_pos[0], last_pos[1], ' ')
    win.addch(s.pos[0][0], s.pos[0][1], '#')
    
curses.endwin()
print("\nScore - " + str(score))