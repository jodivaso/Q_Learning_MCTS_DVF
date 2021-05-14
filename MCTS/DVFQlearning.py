# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 18:02:07 2020

@author: Jose Divasón and Ana Romero
"""

import gym
from gym import spaces
from gym.envs import registration
from DVFMatrixEnv import DVFMatrixEnvMCTS
import numpy as np
from ast import literal_eval
import random


def _edges_to_matrix(edges):
    list = literal_eval(edges.replace("NIL", "[]").replace("(","[").replace(")","]").replace(" ",","))
    dim = len(list)
    result = np.zeros((dim, dim), dtype=int)
    for j in range(0, dim):
        for i in list[j]:
            result[i-1, j] = 1
    return result

class DVFQlearning():
    
    def __init__(self, matrix):
        self.matrix = matrix    
        self.env = DVFMatrixEnvMCTS(self.matrix)
        print (self.env.observation_space.n)
        print (self.env.action_space.n)
        self.q_table = np.zeros([self.env.observation_space.n, self.env.action_space.n])
        
    def training (self, repetitions):
        # Hyperparameters
        # gamma determines how much the agent prioritizes current over future rewards. 
        # One purpose of gamma is to penalize the agent for taking too long to find a solution
        # Alpha keeps the model from learning too much from random noise and outliers and from 
        # making overly-specific generalizations about the specific data it has already seen.
        # Because of the high number of states we'll be working with, we'll start with a high value for
        # epsilon to encourage a high exploration level. When we choose to decay epsilon, we'll do so
        # slowly to allow for as much exploration as possible in the early stages of the task.
        alpha = 0.1
        gamma = 0.6 
        epsilon = 0.1
        
        # For plotting metrics
        all_epochs = []
        all_penalties = []
        
        for i in range(1, repetitions):
            state = self.env.reset()
        
            epochs, penalties, reward, = 0, 0, 0
            done = False
            
            while not done:
                if random.uniform(0, 1) < epsilon:
                    action = self.env.action_space.sample() # Explore action space
                else:
                    action = np.argmax(self.q_table[state]) # Exploit learned values
        
                next_state, reward, done, info = self.env.step(action) 
                
                old_value = self.q_table[state, action]
                next_max = np.max(self.q_table[next_state])
                
                new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
                self.q_table[state, action] = new_value
        
                if reward == -100:
                    penalties += 1
        
                state = next_state
                epochs += 1
                        
        print("Training finished.\n")


    def computeBestDVF(self):
        self.env.reset()
        while (not(self.env.ended())):
            state = self.env.state
            action = np.argmax(self.q_table[state])
            self.env.step(action)
        binary = self.env.state_to_binary(self.env.state)
        l = 0
        for i in (binary):
            if (i==1):
                l=l+1
        print(l)
        return (l)
        
