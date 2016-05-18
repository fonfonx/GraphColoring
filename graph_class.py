import numpy as np
import random
from math import *
from matplotlib import pyplot as plt
import networkx as nx
import scipy.io


class Graph:
    def __init__(self, nbNodes, nbColors):
        self.adjMat = np.zeros((nbNodes, nbNodes), dtype=np.int)
        self.nbColors = nbColors
        self.nbNodes = nbNodes
        self.coloration = np.zeros(nbNodes, dtype=np.int)
        self.cList = ['#46b94a', '#ff4e50', '#d62971', '#25a1da', '#47f00f', '#345acb', '#fbb904']

    # initialize the graph as an ER graph(n,c/N)
    def erdosRenyi(self, c):
        p = c / (1.0 * self.nbNodes)
        for i in range(self.nbNodes):
            for j in range(i):
                if random.random() < p:
                    self.adjMat[i, j] = 1
                    self.adjMat[j, i] = 1

    # initialize the graph with a .dat file
    def initFromFile(self, file):
        self.adjMat=scipy.io.loadmat(file)['A'].astype(np.int)
        self.nbNodes=self.adjMat.shape[0]
        self.coloration=np.zeros(self.nbNodes,dtype=np.int)
        print self.adjMat

    # random initialization of the coloration
    def randomColoration(self):
        for i in range(self.nbNodes):
            self.coloration[i] = random.randint(0, self.nbColors - 1)

    # vizualisation
    def vizualisation(self):
        colorList = [self.cList[i] for i in self.coloration]
        graph = nx.Graph()
        for node in range(self.nbNodes):
            graph.add_node(node, color=colorList[node])

        for i in range(self.nbNodes):
            for j in range(i):
                if self.adjMat[i, j] == 1:
                    graph.add_edge(i, j)

        pos = nx.spring_layout(graph)
        plt.figure(3, figsize=(12, 9))

        nx.draw_networkx_nodes(graph, pos, nodelist=range(self.nbNodes), node_color=colorList)

        nx.draw_networkx_edges(graph, pos)
        plt.axis('off')
        plt.draw()
        plt.show()

    # hamiltonian value
    def hamiltonian(self):
        H = 0
        for i in range(self.nbNodes):
            for j in range(i):
                if self.adjMat[i, j] == 1 and self.coloration[i] == self.coloration[j]:
                    H += 1
        return H

    # hamiltonian change
    def delta(self, vertex, oldColor):
        delta = 0
        for i in range(self.nbNodes):
            if self.adjMat[vertex, i] == 1:
                if self.coloration[vertex] == self.coloration[i]:
                    delta += 1
                if oldColor == self.coloration[i]:
                    delta -= 1
        return delta

    # Metropolis step
    def metropolisStep(self, T):
        oldH = self.hamiltonian()
        vertex = random.randint(0, self.nbNodes - 1)
        oldColor = self.coloration[vertex]
        possibleColors = range(self.nbColors)
        possibleColors.remove(oldColor)
        newColor = random.choice(possibleColors)
        self.coloration[vertex] = newColor
        Delta = self.delta(vertex, oldColor)
        newH = oldH + Delta
        if Delta >= 0:
            p = random.random()
            if p > exp(-Delta / T):
                self.coloration[vertex] = oldColor
                return oldH
        return newH

    # Metropolis-Hastings algorithm
    # Input: number of iterations, intial temperature, decreasing function for T (for simulated annealing)
    # decreasing function takes as input T0 (initial temperature), T (actual temperature) and i (current number of iteration)
    def metropolisAlgo(self, nbIter, T0, decreasingFunction, plot):
        T = T0
        tabH = np.zeros(nbIter + 1)
        H = self.hamiltonian()
        tabH[0] = H
        minH = H
        H0 = H
        for i in range(1, nbIter + 1):
            T=decreasingFunction(T0,T,i)
            H = self.metropolisStep(T)
            tabH[i] = H
            if H < minH:
                minH = H
                # print H
            if H==0:
                print "Proper Coloring found with "+str(i)+" iterations!"
                break
        print "Final Temperature:",T
        print "Initial Hamiltonian:", H0
        print "Final Hamiltonian:", H
        print "Minimal Hamiltonian:", minH
        if plot:
            plt.plot(np.linspace(0, nbIter, nbIter + 1), tabH)
            plt.axis((0,nbIter,0,int(1.3*H0)))
            plt.show()


    # function finding the initial value of temperature
    def initialTemperature(self, nbIter):
        delta_sum=0
        nb_sum=0
        for i in range(nbIter):
            vertex = random.randint(0, self.nbNodes - 1)
            oldColor = self.coloration[vertex]
            possibleColors = range(self.nbColors)
            possibleColors.remove(oldColor)
            newColor = random.choice(possibleColors)
            self.coloration[vertex] = newColor
            Delta = self.delta(vertex, oldColor)
            self.coloration[vertex]=oldColor
            if Delta>0:
                delta_sum+=Delta
                nb_sum+=1
        if nb_sum>=1:
            delta_mean=delta_sum/(1.0*nb_sum)
            T0=-delta_mean/log(0.8)
            return T0
        else:
            print "division by zero, choosing fixed initial temperature"
            return 10.0

