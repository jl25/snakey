#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Snake core implementation.
@author: jzlin@mit.edu
"""

from collections import deque
import threading

class Snake:

    def __init__(self, y_size, x_size, step_map):
        # Initialize the position and direction of the snake.
        self.STEP_DIR_MAP = step_map
        self.current_dir = self.STEP_DIR_MAP['N']        
        self.pos = deque()
        self.pos.append((int(y_size / 2), int(x_size / 2)))
        
        # Bounds of the map. x/y: [0, map_size]
        self.x_size = x_size
        self.y_size = y_size
        
        # Protects snake's attributes.
        self.l = threading.Lock()
    
    # Returns true if food is eaten. Returns None if invalid step.
    def _step(self, pos_food):
        self.l.acquire()
        
        # Step the position forward once.
        yp, xp = self.pos[0]
        ys, xs = self.current_dir
        yp += ys
        xp += xs
        
        # Check if the head has eaten food.
        ate_food = True
        yf, xf = pos_food
        if not (xf == xp and yf == yp):
            ate_food = False
            self.pos.pop()             # Discard the last position of the snake
            
        # Check if snake has hit itself or a wall.
        valid = not self._hit_wall(yp, xp)
        for p in self.pos:
            ys, xs = p
            if (xp == xs and yp == ys):
                valid = False
        
        self.pos.appendleft((yp, xp))
        self.l.release()
        return(ate_food if valid else None)
    
    def _hit_wall(self, yp, xp):
        return(yp > self.y_size or yp < 0 or xp > self.x_size or xp < 0)
    
    def _change_dir(self, direction):
        self.l.acquire()
        self.current_dir = self.STEP_DIR_MAP[direction]
        self.l.release()

def test_snake():
    STEP_DIR_MAP = {'N': [-1, 0], 'E': [0, 1], 'S': [1, 0], 'W': [0, -1]}
    s = Snake(10, 10, STEP_DIR_MAP)
    s._change_dir('S')
    for i in range(0, 5):
        assert(not s._step((10, 10)))
    s._change_dir('E')
    for i in range(0, 4):
        assert(not s._step((10, 10)))
    assert(s._step((10, 10)))         # eats food on the last step
    
    assert(s._step((0, 0)) == None)           # hit a wall
    assert(s.pos.pop() == (10, 10))
    assert(s.pos.pop() == (10, 11))
    assert(len(s.pos) == 0)