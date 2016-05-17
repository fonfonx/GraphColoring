# -*- coding: utf-8 -*-
"""
Created on Sat May 14 11:15:18 2016

@author: Thomas
"""
from __future__ import division
import networkx as nx
import random
import numpy as np
import math
from algorithm import randomColoration,Hamiltonian, metropolisStep
from graph import graphBuild, colorChoice

#Input: adjacency matrix of graph, number of colors, number of iterations
#Ouput: an estimate of the initial temperature for simulated annealing
def findInitialTemp(matrix, nBColors, nBIterations):
    coloration=randomColoration(matrix, nbColors)
    delta = 0
    n,n=matrix.shape
    nBIncreases = 0
    for i in range(nBIterations):
        vertex=random.randint(0,n-1)
        possibleColors=range(nbColors)
        possibleColors.remove(coloration[vertex])
        color=random.choice(possibleColors)
        newColoration=np.copy(coloration)
        newColoration[vertex]=color
        E=Hamiltonian(matrix,newColoration)-Hamiltonian(matrix,coloration)
        if E >0:
            delta +=E
            nBIncreases +=1
    meanIncrease = delta / nBIncreases
    initialTemp = -meanIncrease / math.log(0.8)
    return initialTemp
    
#Input: temperature, alpha parameter (value to tune yet,usually 0.8<alpha<0.995)
#Ouput: updated temperature with exponential schedule
def exponentialUpdateTemp(T,alpha):
    T=alpha*T
    return T

#Input: temperature, alpha parameter (value to tune yet) 
#Output: updated temperature with linear schedule   
def linearUpdateTemp(T,eta):
    T = T - eta
    return T
    
def metropolisAlgo(matrix,coloration,nbColors,iters, initialTemp):
    T = initialTemp
    for i in range(iters):
        if(i%5==0 and T>0.1):
            T = exponentialUpdateTemp(T,0.95)
        coloration=metropolisStep(T,matrix,coloration,nbColors)
        print "H:",Hamiltonian(matrix, coloration)



matrix = graphBuild(500,50)
nbColors = 5
cList = colorChoice(nbColors)
coloration=randomColoration(matrix, nbColors)
T0 = findInitialTemp(matrix,nbColors,100)
print 'Initial temperature: %.2f' %T0
print('simulated annealing with exponential update:')
metropolisAlgo(matrix,coloration,nbColors,200,T0)
