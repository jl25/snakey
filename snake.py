#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jzlin@mit.edu
"""

from collections import deque
import threading

class Snake:
    STEP_DIR_MAP = {'N': [0, 1], 'E': [1, 0], 'S': [0, -1], 'W': [-1, 0]}
    
    def __init__(self, map_size):
        # Initialize the position and direction of the snake.
        self.current_dir = self.STEP_DIR_MAP['N']        
        self.pos = deque()
        self.pos.append((int(map_size / 2), int(map_size / 2)))
        
        # Bounds of the map. x/y: [0, map_size]
        self.map_size = map_size
        
        # Protects snake's attributes.
        self.l = threading.Lock()
        
    def _step(self, pos_food):
        self.l.acquire()
        
        # Step the position forward once.
        xp, yp = self.pos[0]
        xs, ys = self.current_dir
        xp += xs
        yp += ys
        
        # Check if the head has eaten food.
        ate_food = False
        xf, yf = pos_food
        if not (xf == xp and yf == yp):
            ate_food = True
            self.pos.pop()             # Discard the last position of the snake
            
        # Check if snake has hit itself or a wall.
        valid = True
        for p in self.pos:
            xs, ys = p
            if (xp == xs and yp == ys) or self._hit_wall(xp, yp):
                valid = False
        
        self.pos.appendleft((xp, yp))
        self.l.release()
        return(valid, ate_food)
    
    def _hit_wall(self, xp, yp):
        w = self.map_size
        if abs(xp) > w or abs(yp) > w:
            return(True)
        else:
            return(False)
    
    def _change_dir(self, direction):
        self.l.acquire()
        self.current_dir = self.STEP_DIR_MAP[direction]
        self.l.release()

def test_snake():
    s = Snake(map_size = 10)
    for i in range(0, 5):
        assert(s._step((10, 10)))
    s._change_dir('E')
    for i in range(0, 5):
        assert(s._step((10, 10)))             # eats food on the last step
    
    assert(s._step((0, 0)) == False)        # hit a wall
    assert(s.pos.pop() == (10, 10))
    assert(s.pos.pop() == (11, 10))