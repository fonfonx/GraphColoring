import numpy as np
import random
from math import *
from matplotlib import pyplot as plt
import networkx as nx
import scipy.io
import time


class Graph:
    def __init__(self, nbNodes, nbColors):
        self.adjMat = np.zeros((nbNodes, nbNodes), dtype=np.int)
        self.nbColors = nbColors
        self.nbNodes = nbNodes
        self.coloration = np.zeros(nbNodes, dtype=np.int)
        self.bestColoration = np.zeros(nbNodes, dtype=np.int)
        self.cList = ['#46b94a', '#ff4e50', '#d62971', '#25a1da', '#47f00f', '#345acb', '#fbb904']

    # initialize the graph as an ER graph(n,c/N)
    def erdosRenyi(self, c):
        p = c / (1.0 * self.nbNodes)
        for i in range(self.nbNodes):
            for j in range(i):
                if random.random() < p:
                    self.adjMat[i, j] = 1
                    self.adjMat[j, i] = 1

    # initialize the graph with a .mat file
    def initFromFile(self, file):
        self.adjMat = scipy.io.loadmat(file)['A'].astype(np.int)
        self.nbNodes = self.adjMat.shape[0]
        self.coloration = np.zeros(self.nbNodes, dtype=np.int)
        self.bestColoration = np.zeros(self.nbNodes, dtype=np.int)

    # write a .mat file
    def writeMat(self, file):
        self.coloration = self.bestColoration
        H = self.hamiltonian()
        X = self.coloration + 1
        scipy.io.savemat(file + "_" + str(H) + ".mat", {'X': X})

    # save a graph as a .mat file
    def saveGraph(self,file):
        scipy.io.savemat(file,{'A':self.adjMat})

    # assign a coloration with a .mat file
    def setColorationFromMat(self, file):
        col = np.array(scipy.io.loadmat(file)['X'].astype(np.int))
        col = col.reshape(self.nbNodes)
        self.coloration = col - 1

    # random initialization of the coloration
    def randomColoration(self):
        for i in range(self.nbNodes):
            self.coloration[i] = random.randint(0, self.nbColors - 1)

    # vizualisation of the graph
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

    # vectorized version of delta function
    def delta_vec(self, vertex, oldColor):
        new = self.coloration == self.coloration[vertex]
        old = self.coloration == oldColor
        return np.sum(new * self.adjMat[vertex, :]) - np.sum(old * self.adjMat[vertex, :])

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
    # Input: number of iterations, initial temperature, decreasing function for T (for simulated annealing)
    # decreasing function takes as input T0 (initial temperature), T (actual temperature) and i (current number of iteration)
    def metropolisAlgo(self, nbIter, T0, decreasingFunction, plot, save, file):
        T = T0
        tabH = np.zeros(nbIter + 1)
        H = self.hamiltonian()
        tabH[0] = H
        minH = H
        H0 = H
        for i in range(1, nbIter + 1):
            T = decreasingFunction(T0, T, i)
            H = self.metropolisStep(T)
            tabH[i] = H
            if H < minH:
                minH = H
                self.bestColoration = np.copy(self.coloration)
                # print H
            if H == 0:
                print "Proper Coloring found with " + str(i) + " iterations!"
                break
        print "Final Temperature:", T
        print "Initial Hamiltonian:", H0
        print "Final Hamiltonian:", H
        print "Minimal Hamiltonian:", minH
        if save:
            self.writeMat(file)
        if plot:
            plt.plot(np.linspace(0, nbIter, nbIter + 1), tabH)
            plt.axis((0, nbIter, 0, int(1.3 * H0)))
            plt.show()
        return minH

    # function finding the initial value of temperature
    # the idea is to compute the mean positive variation of the Hamiltonian
    # and to accept such a change with probability 0.8
    def initialTemperature(self, nbIter):
        delta_sum = 0
        nb_sum = 0
        for i in range(nbIter):
            vertex = random.randint(0, self.nbNodes - 1)
            oldColor = self.coloration[vertex]
            possibleColors = range(self.nbColors)
            possibleColors.remove(oldColor)
            newColor = random.choice(possibleColors)
            self.coloration[vertex] = newColor
            Delta = self.delta(vertex, oldColor)
            self.coloration[vertex] = oldColor
            if Delta > 0:
                delta_sum += Delta
                nb_sum += 1
        if nb_sum >= 1:
            delta_mean = delta_sum / (1.0 * nb_sum)
            T0 = -delta_mean / log(0.8)
            return T0
        else:
            print "division by zero, choosing fixed initial temperature"
            return 10.0
