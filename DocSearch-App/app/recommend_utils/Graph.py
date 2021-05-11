import re
import os
import glob
import json
import jsonpickle 
import math
import nltk
import pandas as pd
import pathlib
import numpy as np # linear algebra
from itertools import combinations 
from collections import defaultdict 
from nltk.corpus import wordnet as wn
from nltk import word_tokenize
from scipy import spatial
from nltk.metrics import edit_distance
from collections import defaultdict 
from .WordNet import WordNet
from .Node import Node

#Class to represent an un-directed graph using adjacency list representation 
class Graph: 
   
    def __init__(self,vertices): 
        self.V = vertices #No. of vertices 
        self.V_org = vertices 
        self.graph = defaultdict(list) # default dictionary to store graph 
        
        
    # function to add an edge to graph 
    def addEdge(self,u,v,w): 
        self.graph[u].append(Node(u,v,w))
        self.graph[v].append(Node(v,u,w))

        
    #function to print graph
    def printGraph(self):
        s = ""
        for i in self.graph:
            s = s + str(i) + " is connected to "
            print(str(i) + " is connected to ")
            for node in self.graph[i]:
                s = s + str(node['dest']) + "(Weight = " + str(node['wt']) + ")" + " "
                print(str(node['dest']) + "(Weight = " + str(node['wt']) + ")" + " ")
            s = s + "\n"
            print("\n")
        return s

    def BFS(self, s, max_levels):
        visited = set()
         
        queue = []
        wordNet = WordNet()
        queue.append((s,0,0,1))
        visited.add(s)
        level = 0
        result = {}
        while queue:
            aux = []
            result[level] = []
            
            while queue:
                s = queue.pop(0)
                visited.add(s[0])
                result[level].append(s)
                for node in self.graph[s[0]]:
                    # print(node)
                    if node['dest'] not in visited:
                        
                        # Wordnet Similarity
                        q1 = wordNet.clean_sentence(s[0])
                        q2 = wordNet.clean_sentence(node['dest'])
                        sim = 0
                        sim = wordNet.semanticSimilarity(q1, q2)

                        sumOfCooccurence = 0
                        for chi in self.graph[node['dest']]:
                            if chi['dest'] in visited:
                                sumOfCooccurence += chi['wt']
                        aux.append((node['dest'], sumOfCooccurence, level+1, sim))
                        visited.add(node['dest'])
            level += 1
            if level > max_levels:
                break
            for node in aux:
                queue.append(node)
            solution = []
            for key in result:
                for tup in result[key]:
                    if tup[2] != 0 and (tup[1] + np.exp(tup[3]))/np.exp(tup[2]) >= 2:
                        solution.append( ( tup[0], (tup[1] + np.exp(tup[3]))/np.exp(tup[2]) ) )
        return solution            
    
    def exportNetwork(self, filename = "output"):
        filename += ".json"
        obj = jsonpickle.encode(self.graph)
        with open(filename, "w") as outfile: 
            json.dump(obj, outfile)

    def importNetwork(self, filename = "output"):
        filename += ".json"
        with open(filename) as json_file:
            data = json.load(json_file)
            self.graph = jsonpickle.decode(data)
            self.V = len(self.graph)
            self.V_org = len(self.graph)