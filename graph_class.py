import numpy as np
import random
from math import *
from matplotlib import pyplot as plt
import networkx as nx

class Graph:

    def __init__(self,nbNodes, nbColors):
        self.adjMat=np.zeros((nbNodes,nbNodes),dtype=np.int)
        self.nbColors=nbColors
        self.nbNodes=nbNodes
        self.coloration=np.zeros(nbNodes,dtype=np.int)
        self.cList=['#46b94a', '#ff4e50', '#d62971', '#25a1da', '#47f00f', '#345acb', '#fbb904']

    # initialize the graph as an ER graph(n,c/N)
    def erdosRenyi(self,c):
        p=c/(1.0*self.nbNodes)
        for i in range(self.nbNodes):
            for j in range(i):
                if random.random()<p:
                    self.adjMat[i,j]=1
                    self.adjMat[j,i]=1

    # random initialization of the coloration
    def randomColoration(self):
        for i in range(self.nbNodes):
            self.coloration[i]=random.randint(0,self.nbColors-1)

    # vizualisation
    def vizualisation(self):
        colorList=[self.cList[i] for i in self.coloration]
        graph = nx.Graph()
        for node in range(self.nbNodes):
            graph.add_node(node, color=colorList[node])

        for i in range(self.nbNodes):
            for j in range(i):
                if self.adjMat[i,j]==1:
                    graph.add_edge(i,j)

        pos = nx.spring_layout(graph)
        plt.figure(3, figsize=(12, 9))

        nx.draw_networkx_nodes(graph, pos, nodelist=range(self.nbNodes), node_color=colorList)

        nx.draw_networkx_edges(graph, pos)
        plt.axis('off')
        plt.draw()
        plt.show()

    # hamiltonian value
    def hamiltonian(self):
        H=0
        for i in range(self.nbNodes):
            for j in range(i):
                if self.adjMat[i,j]==1 and self.coloration[i]==self.coloration[j]:
                    H+=1
        return H

    # Metropolis step
    def metropolisStep(self,T):
        oldH=self.hamiltonian()
        vertex = random.randint(0, self.nbNodes - 1)
        oldColor=self.coloration[vertex]
        possibleColors = range(self.nbColors)
        possibleColors.remove(oldColor)
        newColor = random.choice(possibleColors)
        self.coloration[vertex]=newColor
        newH=self.hamiltonian()
        Delta=newH-oldH
        if Delta>=0:
            p = random.random()
            if p > exp(-Delta / T):
                self.coloration[vertex]=oldColor

    # Metropolis-Hastings algorithm
    def metropolisAlgo(self,nbIter):
        T=0.1
        tabH=np.zeros(nbIter+1)
        H=self.hamiltonian()
        tabH[0]=H
        print "Initial Hamiltonian:",H
        minH=H
        for i in range(1,nbIter+1):
            self.metropolisStep(T)
            H=self.hamiltonian()
            tabH[i]=H
            if H<minH:
                minH=H
            #print H
        print "Final Hamiltonian:",H
        print "Minimal Hamiltonian:",minH
        #plt.plot(np.linspace(0,nbIter,nbIter+1),tabH)
        #plt.show()

