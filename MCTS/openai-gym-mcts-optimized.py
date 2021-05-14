import os
import gym
import random
from time import time
from math import sqrt, log
from copy import deepcopy

def ucb(node):
    c = sqrt(2)
    if node.parent is not None and node.visits==0:
        return ucb(node.parent)
    else:
        if node.parent is None:
            return float("inf")
        else:
            return node.value / node.visits + c*sqrt(log(node.parent.visits)/node.visits)


class Node:
    def __init__(self, parent, action):
        self.parent = parent
        self.action = action
        self.children = []
        self.visits = 0
        self.value = 0


class MCTS:
    def __init__(self, env_name, matrix, matrixname, playouts=10000):
        self.env_name = env_name
        self.matrix = matrix
        self.playouts = playouts
        self.matrixname = matrixname

    def run(self):
        start_time = time()
        
        env = gym.make(self.env_name,matrix=self.matrix)

        print (self.env_name)
        print (self.matrix)
        root = Node(None, None)
        best_edges = []
        best_reward = float("-inf")            
        for i in range(self.playouts):
            state = deepcopy(env)
            sum_reward = 0
            node = root
            terminal = False
            actions = []

            # selection phase
            while node.children:                       
                node = max(node.children, key=ucb)                    
                reward, terminal, _ = state.step(node.action)                   
                sum_reward += reward
                actions.append(node.action)
                 
            # expansion phase
            if not terminal:
                node.children = [Node(node, a) for a in range(state.num_actions)]

            # simulation phase
            while not terminal:
                action =  random.randint(0, state.num_actions - 1)
                reward, terminal, _ = state.step(action)
                sum_reward += reward
                actions.append(action)

            if best_reward < sum_reward:
                best_reward = sum_reward
                best_edges = actions

            # backpropagation phase
            while node:
                node.visits += 1
                node.value += sum_reward                   
                node = node.parent
             
        avg_time_playouts = (time()-start_time)/(self.playouts)
                        
        print("\n Best reward:", best_reward)
        print("Average time playouts:", avg_time_playouts)        
        outputfile = open("results.txt", "a")        
        outputfile.write(self.matrixname + " " + str(best_reward) + "\n")        
        outputfile.close()

def main():
    
    from DVFQlearning import _edges_to_matrix
    directorio = r'C:\Users\jodivaso\Anaconda3\Lib\site-packages\gym\envs\matricesMCTS\Test'  
    ficheros = [os.path.join(path, name) for path, subdirs, files in os.walk(directorio) for name in files]
    
    for fichero in ficheros:    
        try:
            f = open(fichero, "r")
            m = _edges_to_matrix(f.read())
            f.close()
            matrixname = os.path.basename(fichero)    
            # The number of playouts is the key: ideally it would depend on the input matrix
            MCTS("MCTS_ISSAC-v0", matrixname = matrixname, matrix = m, playouts=10000).run()
        except:
            pass

    
if __name__ == "__main__":
    main()
