# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 18:47:54 2020

@author: Jose Divasón and Ana Romero
"""

 
import gym
import gym.spaces
from gym import spaces
import numpy as np

# La matriz representa desde donde sale y donde llega; y marca un "menor o igual". 
# Por eso es solo una dirección y no es simétrica, aunque se dibuje sin flechas.
# Lo que está por encima es menor o igual

class DVFMatrixEnvMCTS(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, matrix):
        #super(DVFMatrixEnv, self).__init__()
        super().__init__()
        
        self.matrix = matrix        
        self.num_rows = self.matrix.shape[0]
        self.num_columns = self.matrix.shape[1]        
        self.vector_list = self.vectorList() #Guarda la posición de los unos (los posibles vectores a coger)
        self.num_actions = self.vector_list.shape[0]
        self.solution = []
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
        #new_state = self.state
        reward = 0 # default reward when there is no pickup/dropoff
        done = False
        action = self.vector_list[action_index]
        # row = int (action // self.num_rows)
        # col = int (action % self.num_rows)        
        row = action[0]
        col = action[1]
        
        # Comprobamos que no está en los índices para poder añadir (es un vector posible, quizás no admisible):
        # Por ejemplo, si añadimos el vector (0,1) ya no podremos añadir ningun vector de la filas 0 ni de 
        # la 1, ni de las columnas 0 y 1. Es decir, se quitan 2 filas y dos columnas. 
        if ((row in self.matched) or (col in self.matched)):
                # reward = -100
                reward = 0
                done = True
        else:
            rowstatusList = self.statusList[row]
            #colList = matrix[:;col]
            colList = [row[col] for row in self.matrix]
            if (self.nullIntersectionP(rowstatusList, colList) == False): #Si no es admisible
                #reward = -100
                reward = 0
                done = True                
            else:
                reward = 1
                
                #Añadimos el vector que podemos añadir:
                self.solution.append([row,col])
                #Borramos los vectores de vectorList que ya no podremos añadir eligiendo ese:
                self.vector_list = np.array([(x,y) for (x,y) in self.vector_list if (x!=row) and (y!=row) and (x!=col) and (y!=col)])
                self.num_actions = self.vector_list.shape[0]
                    
                done = self.ended() # Recomprueba si es admisible!!!! Y creo que debajo lo vuelve a comprobar!!
                #self.state = new_state
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
      
        return reward, done, {}
    
    
    def render(self, mode='human', close=False):
  # Render the environment to the screen
      print(self.state)
      print(self.decode())
        
    def vectorList (self):
        l = []
        for row in range(self.num_rows):
            for col in range(row +1 , self.num_columns):
                if (self.matrix[row][col] == 1): 
                    l.append([row,col])                  
        return np.array(l)   
    
    
    # def ended (self):
    #     vectorList = self.vector_list
    #     l = self.state_to_binary(self.state)
    #     for i in range(len(l)):
    #         if (l[i] == 0):
    #             v = vectorList[i]
    #             row = v // self.num_rows
    #             col = v % self.num_rows                
    #             if (not(row in self.matched) and not(col in self.matched) and (self.admissible(row,col))):
    #                 return False            
    #    return True 
    
    #Ahora acabamos cuando la lista de posibles vectores a añadir es vacia
    def ended (self):
        return self.vector_list.size == 0        
   
            
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
