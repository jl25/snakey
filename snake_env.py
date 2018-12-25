#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Snake environment.
@author: jzlin@mit.edu
"""
import logging
import snake
from random import randint

class Snake_Env:
    
    def __init__(self, y_size, x_size, step_map):
        self.x_size = x_size
        self.y_size = y_size
        
        self.s = snake.Snake(y_size-3, x_size-3, step_map)
        self.food = self._gen_food()
        self.score = 0
        
    def _gen_food(self):
        food = [randint(1, self.y_size - 1), randint(2, self.x_size - 1)]
        while food in self.s.pos:
            food = [randint(1, self.y_size - 1), randint(2, self.x_size - 1)]
        return(food)
        
    """
    An action is defined as a direction to move in.
    Returns the next state, the reward, and whether terminal.
    """
    def step(self, action):
        self.s._change_dir(action)
        res = self.s._step(self.food)
        
        isTerminal = False
        
        # If snake runs over itself or hits a wall.
        if res == None:
            logging.debug('Terminal State reached...')
            return(False, True)

        # If the snake eats food, generate a new food position.
        ateFood = False
        if res == True:
            logging.debug('Food ate...')
            self.score += 1
            self.food = self._gen_food()
            ateFood = True

        return(ateFood, isTerminal)
        
def test_snake_env():
    STEP_DIR_MAP = {'N': [-1, 0], 'E': [0, 1], 'S': [1, 0], 'W': [0, -1]}
    env = Snake_Env(10, 10, STEP_DIR_MAP)
    env.food = (6, 6)
    for i in range(0, 3):
        ateFood, isTerminal = env.step('S')
        assert((not ateFood) and (not isTerminal))
    
    for i in range(0, 2):
        ateFood, isTerminal = env.step('E')
        assert((not ateFood) and (not isTerminal))
    ateFood, isTerminal = env.step('E')
    assert(ateFood and (not isTerminal) and env.score == 1)