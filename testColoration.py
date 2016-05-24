from graph_class import *
from math import *
import matplotlib.pyplot as plt

# Parameters
# number of nodes
N = 100
# expected number of neighbors
c = 4
# number of colors
d = 5
# initial temperature
T0 = 10.0

# number of iterations
nbIter = 4000
# number of iterations for initial temperature
nbIterInit = 40

# plot curve or not
plot=True

# save coloration or not
save=False

# mat_file
mat_file="graph_adjacency_matrix.mat"
inputXav="mygraph.mat"

# mat file output (without extension)
out_file="coloration"


#### Decreasing functions ####
# Here are some decreasing functions that we can use
# Parameters: initial Temperature, actual Temperature, current number of iteration

# identity (no simulated annealing)
def identity(T):
    return T


# power decrease
def powerDecrease(T0, n, gamma):
    return T0 / (n ** gamma)


def logDecrease(T0, n):
    return T0 / log(n + 1)


def linearDecrease(T, alpha, n, modulo):
    if n % modulo == 0 and T > alpha:
        T -= alpha
    return T


def expoDecrease(T, alpha, n, modulo, Tmin):
    if n % modulo == 0 and T > Tmin:
        T *= alpha
    return T

def mydecrease(T0,T,n):
    if n<=10:
        return T0
    if n>10:
        if n%(10+n/100)==0:
            #return 0.95*T
            return T0/sqrt(n)
    return T


# decreasingFunction
def decreasingFunction(T0, T, n):
    #return identity(T)
    #return expoDecrease(T,0.85,n,5,0.1)
    return powerDecrease(T0,n,0.5)
    #return mydecrease(T0,T,n)

def test():
    G = Graph(N, d)
    G.erdosRenyi(c)
    #G.initFromFile("G2.mat")
    G.randomColoration()
    #G.setColorationFromMat("coloration_50.mat")
    T0 = G.initialTemperature(nbIterInit)
    print "Initial Temperature:",T0
    # G.vizualisation()
    G.metropolisAlgo(nbIter, T0, decreasingFunction, plot,save,out_file)

def competition(input, nbNodes, nbColors):
    G=Graph(nbNodes,nbColors)
    G.initFromFile(input)
    H=1000
    while H>0:
        G.randomColoration()
        T0=G.initialTemperature(nbIterInit)
        G.metropolisAlgo(nbIter, T0, decreasingFunction, False, False,out_file)
        actH=G.hamiltonian()
        if actH<H:
            H=actH
            print H
            G.writeMat(out_file)
        print "actual best:",H

def valeurs_moy():
    G=Graph(N,d)
    G.initFromFile(inputXav)
    rep=0
    for k in range(10):
        G.randomColoration()
        minH=G.metropolisAlgo(nbIter,T0,decreasingFunction,False,False,out_file)
        rep+=minH
    print "average min H:",rep/(10.0)

def Hmin(q):
    G=Graph(N,q)
    taby=[]
    tabx=[]
    for c in range(1,N,3):
        print c
        val=0
        for k in range(4):
            G.erdosRenyi(c)
            G.randomColoration()
            T0=G.initialTemperature(nbIterInit)
            val+=G.metropolisAlgo(nbIter,T0,decreasingFunction,False,False,out_file)
        taby.append(val/4.0)
        tabx.append(c)
    print tabx,taby
    plt.plot(tabx,taby)
    plt.show()


#competition(mat_file,100,3)
#test()
#valeurs_moy()

Hmin(5)
