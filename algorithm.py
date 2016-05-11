# -*- coding: utf-8 -*-

import numpy as np
import numpy.random as rnd
from graph import *
import random
from math import *

# Input: adjacency matrix, number of colors
# Output: Random coloration of the graph (vector of colors)
def randomColoration(matrix,nbColors):
    # adjacency matrix supposed to be squared
    n,n=matrix.shape
    return rnd.randint(0,nbColors,n)


# Input: adjacency matrix, coloration of the nodes
# Output: value of the Hamiltonian (=distance, =cost)
def Hamiltonian(matrix, coloration):
    H=0
    n,n=matrix.shape
    for i in range(n):
        for j in range(i):
            if matrix[i,j]==1 and coloration[i]==coloration[j]:
                H+=1
    return H

# Input: parameter beta, adjacency matrix, current coloration, number of colors
# Performs one step of the Metropolis-Hastings algorithm
# Output: new coloration
def metropolisStep(beta, matrix, coloration, nbColors):
    n,n=matrix.shape
    vertex=random.randint(0,n-1)
    possibleColors=range(nbColors)
    possibleColors.remove(coloration[vertex])
    color=random.choice(possibleColors)
    newColoration=np.copy(coloration)
    newColoration[vertex]=color
    Delta=Hamiltonian(matrix,newColoration)-Hamiltonian(matrix,coloration)
    if Delta<=0:
        return newColoration
    else:
        p=random.random()
        if p<exp(-beta*Delta):
            return newColoration
        else:
            return coloration

def metropolisAlgo(matrix,coloration,nbColors):
    for i in range(200):
        coloration=metropolisStep(10.0,matrix,coloration,nbColors)
        print "H:",Hamiltonian(matrix, coloration)



# Input: maximal number of nodes, number of Colors
# Output: ER graph with random coloration (commented) and performs metropolis on it
def main(nbNodeMax, nbColors):
    n,p=erdosRenyiParam(nbNodeMax)
    print "Number of nodes:",n
    print "Proba of eges:",p
    edges=randomGraph(n,p)
    matrix=adjMatrix(n,edges)
    cList = colorChoice(nbColors)
    coloration=randomColoration(matrix, nbColors)
    H=Hamiltonian(matrix,coloration)
    print "Hamiltonian:",H
    metropolisAlgo(matrix,coloration,nbColors)
    #draw(range(n),colorList(coloration,cList),edges)

main(100,5)