# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 18:47:54 2020

@author: Jose Divasón and Ana Romero
"""

 
import gym
from gym import spaces
import numpy as np


class DVFMatrixEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, matrix):
        super(DVFMatrixEnv, self).__init__()

        self.matrix = matrix        
        self.num_rows = self.matrix.shape[0]
        self.num_columns = self.matrix.shape[1]        
        self.vector_list = self.vectorList()
        self.num_actions = self.vector_list.size
        self.num_states = 2 ** self.num_actions
        self.state = 0
        self.action_space = spaces.Discrete(self.num_actions)
        self.observation_space = spaces.Discrete(self.num_states)
        
        self.status = np.zeros(self.num_columns)
        self.statusList = []
        for i in range(self.num_columns):
            self.statusList.append(np.array([]))
        self.matched = np.array([],int)
        
        
    def reset(self):
  # Reset the state of the environment to an initial state
        self.state = 0
        self.status = np.zeros(self.num_columns)
        self.statusList = []
        for i in range(self.num_columns):
            self.statusList.append(np.array([]))
        self.matched = np.array([])
        return 0

        
    def step(self, action_index):
  # Execute one time step within the environment
        new_state = self.state
        l = self.state_to_binary(self.state)
        reward = 0 
        done = False
        action = self.vector_list[action_index]
        row = int (action // self.num_rows)
        col = int (action % self.num_rows)
        
        if ((row in self.matched) or (col in self.matched)):
                reward = -1
                done = True
        else:
            rowstatusList = self.statusList[row]
            #colList = matrix[:;col]
            colList = [row[col] for row in self.matrix]
            if (self.nullIntersectionP(rowstatusList, colList) == False):
                reward = -1
                done = True                
            else:
                reward = 1
                new_state = self.state + 2 ** action_index
                self.matched = np.append(self.matched,row)
                self.matched = np.append(self.matched,col)
                done = self.ended()
                self.state = new_state
                self.status[row]=1
                rowstatusList =  np.append(self.statusList[row],row)
                self.statusList[row]= rowstatusList
                for j in range(len(colList)):
                    item = colList[j]
                    if ((j != row) and (item == 1)):
                        itemStatus = self.status[j]
                        if (itemStatus == 1):
                            for rowk in range(len(colList)):
                                rowkstatus = self.status[rowk]
                                rowkstatusList = self.statusList[rowk]
                                if ((rowkstatus != 1) and (j in rowkstatusList)) :
                                    self.statusList[rowk] = np.concatenate([rowstatusList,rowkstatusList])
                        else:
                            itemStatusList = self.statusList[j]
                            self.statusList[j] = np.concatenate([itemStatusList,rowstatusList])
      
        return new_state, reward, done, {}
    
    
    def render(self, mode='human', close=False):
  # Render the environment to the screen
      print(self.state)
      print(self.decode())
        
    def vectorList (self):
        l = np.array([])
        for row in range(self.num_rows):
            for col in range(row +1 , self.num_columns):
                if (self.matrix[row][col] == 1): 
                    l = np.append(l, row * self.num_rows + col)
        return l   
    
    def ended (self):
        vectorList = self.vector_list
        l = self.state_to_binary(self.state)
        for i in range(len(l)):
            if (l[i] == 0):
                v = vectorList[i]
                row = v // self.num_rows
                col = v % self.num_rows
                
                if (not(row in self.matched) and not(col in self.matched) and (self.admissible(row,col))):
                    return False
                
        return True 
 
          
    def state_to_binary(self, i):
        l = []
        s = i
        for n in range (self.num_actions):
            l.append(s % 2)
            s = s // 2
        return l
    
    def state_num_of_vectors(self, i):
        l = self.state_to_binary(i)
        s = 0
        for n in range (self.num_actions):
            if l[n] == 1:
                s+= 1
        return s
         
    
    def decode(self):
        l = self.state_to_binary(self.state)
        m = [[0 for x in range(self.num_rows)] for y in range(self.num_columns)] 
        for n in range (self.num_actions):
            j = l[n]           
            if (j == 1):
                a = self.vector_list[n]
                row = int(a // self.num_rows)
                col = int(a % self.num_rows)
                m [row][col]= 1
        return m
    
    def nullIntersectionP(self, rowstatusList, colList):
        if (len(rowstatusList) > 0):
            for i in (rowstatusList):
                if (colList[int(i)] != 0):
                    return False
        return True
    
    def admissible(self,row,col):
        rowstatusList = self.statusList[int(row)]
        colList = [row[int(col)] for row in self.matrix]
        return (self.nullIntersectionP(rowstatusList, colList))
