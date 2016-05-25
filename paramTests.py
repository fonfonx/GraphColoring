from graph_class import *
from math import *
import numpy as np
import copy

#Initialization

nbIter = 6000
mat_file="graph_adjacency_matrix.mat"
results = {}
T0 = 10
plot = False
save = False
out_file="coloration"
def metropolisAlgo2(graph, nbIter, T0, decreasingFunction, alpha, plot):
        T = T0
        tabH = np.zeros(nbIter + 1)
        H = graph.hamiltonian()
        tabH[0] = H
        minH = H
        H0 = H
        for i in range(1, nbIter + 1):
            T= decreasingFunction(T0, T, i, alpha)
            H = metropolisStep2(graph, T)
            tabH[i] = H
            if H < minH:
                minH = H
                # print H
            if H==0:
                print "Proper Coloring found with "+str(i)+" iterations!"
                return tabH
        print "Final Temperature:",T
        print "Initial Hamiltonian:", H0
        print "Final Hamiltonian:", H
        print "Minimal Hamiltonian:", minH
        if plot:
            plt.plot(np.linspace(0, nbIter, nbIter + 1), tabH)
            plt.axis((0,nbIter,0,int(1.3*H0)))
            plt.show()
        return tabH
        
def metropolisStep2(graph, T):
        oldH = graph.hamiltonian()
        vertex = random.randint(0, graph.nbNodes - 1)
        oldColor = graph.coloration[vertex]
        possibleColors = range(graph.nbColors)
        possibleColors.remove(oldColor)
        newColor = random.choice(possibleColors)
        graph.coloration[vertex] = newColor
        Delta = graph.delta(vertex, oldColor)
        newH = oldH + Delta
        if Delta >= 0:
            p = random.random()
            if p > exp(-Delta / T):
                graph.coloration[vertex] = oldColor
                return oldH
        return newH
        
def expoDecrease(T, alpha, n, modulo, Tmin):
    if n % modulo == 0 and T > Tmin:
        T *= alpha
    return T
    
def linearDecrease(T, alpha, n, modulo):
    if n % modulo == 0 and T > alpha:
        T -= alpha
    return T    

def powerDecrease(T0, n, gamma):
    return T0 / (n ** gamma)

# decreasingFunction
def decreasingFunction(T0, T, n, param):
    # return identity(T)
    #if n<=100:
    #    return T
    # if n%10>=0 and n<=100:
    #     return powerDecrease(T0, n-30, 1.0)
    # if n>=100 and T>0.1 and n%10>=0:
    #     return powerDecrease(T0,n,0.6)
    # return T   
    if param==1:
        return linearDecrease(T,0.25,n,param)
    if param==2:
        return expoDecrease(T,0.85, n, param, 0.01)
    if param==3:
        return powerDecrease(T0, n, 0.5)


#Build 4 graphs with different topologies to test parameters
G1 = Graph(100, 3)
G1.initFromFile(mat_file)
G1.randomColoration()
T01 = G1.initialTemperature(100)

G2 = Graph(200, 5)
G2.initFromFile("G2.mat")
#G2.erdosRenyi(40)
G2.randomColoration()
T02 = G2.initialTemperature(100)

G3 = Graph(50, 3)
G3.initFromFile("G3.mat")
#G3.erdosRenyi(10)
G3.randomColoration()
T03 = G3.initialTemperature(100)

G4 = Graph(100, 7)
G4.initFromFile("G4.mat")
#G4.erdosRenyi(30)
G4.randomColoration()
T04 = G4.initialTemperature(100)

alphas = np.linspace(0.05, 0.4, 8)
#alphas = np.linspace(0.7, 0.95, 26)
alphas = [1,2,3,5,10]

#for i in alphas:
#    alpha = i
#    print "parameter value:", alpha
#    print "Graph 1"
#    H1 = metropolisAlgo2(copy.deepcopy(G1), nbIter, T01, decreasingFunction, alpha, plot)
#    print "Graph 2"
#    H2 = metropolisAlgo2(copy.deepcopy(G2),nbIter, T02, decreasingFunction, alpha, plot)
#    print "Graph 3"
#    H3 = metropolisAlgo2(copy.deepcopy(G3), nbIter, T03, decreasingFunction, alpha, plot)
#    print "Graph 4"
#    H4 = metropolisAlgo2(copy.deepcopy(G4),nbIter, T04, decreasingFunction, alpha, plot)
#    perf = np.mean([H1,H2,H3,H4])
#    print "average Hmin:", perf
#    results.update({i:perf})

tab_lin = metropolisAlgo2(copy.deepcopy(G4), nbIter, T04, decreasingFunction, 1, plot)
tab_expo = metropolisAlgo2(copy.deepcopy(G4), nbIter, T04, decreasingFunction, 2, plot)
tab_power = metropolisAlgo2(copy.deepcopy(G4), nbIter, T04, decreasingFunction, 3, plot)

plt.plot(np.linspace(0, nbIter, nbIter + 1), tab_lin, 'r', np.linspace(0, nbIter, nbIter + 1), tab_expo, 'b', np.linspace(0, nbIter, nbIter + 1), tab_power, 'g')
plt.xlabel('number of iterations')
plt.ylabel('Energy')
plt.savefig('report/curves.pdf')
plt.show()

